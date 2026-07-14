"""Thin transport layer over the G-Labs Automation webhook REST API.

Uses only the Python standard library (urllib) so the tool needs no installs,
matching the repo's dependency-free convention. All pipeline logic lives
elsewhere; this class just does submit / poll / download.

See WEBHOOK_INTEGRATION.en.md for the API contract.
"""
from pathlib import Path
from urllib.error import HTTPError
import json
import os
import urllib.request

DEFAULT_BASE_URL = "http://127.0.0.1:8765"


class GLabsError(RuntimeError):
    """Raised for non-2xx responses (config / request errors, not task failures)."""
    def __init__(self, status, body):
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status}: {body}")


def load_config(api_key=None, base_url=None, config_path=None):
    """Resolve base_url + api_key: explicit arg > env var > .glabs.json > default.

    Raises if no API key can be found anywhere.
    """
    file_cfg = {}
    if config_path is not None:
        p = Path(config_path)
        if p.exists():
            with open(p, encoding="utf-8") as f:
                file_cfg = json.load(f)

    resolved_key = (api_key
                    or os.environ.get("GLABS_API_KEY")
                    or file_cfg.get("api_key"))
    if not resolved_key:
        raise GLabsError(0, "No API key: set GLABS_API_KEY, pass --api-key, "
                            "or add api_key to .glabs.json")

    resolved_base = (base_url
                     or os.environ.get("GLABS_BASE_URL")
                     or file_cfg.get("base_url")
                     or DEFAULT_BASE_URL)
    return {"api_key": resolved_key, "base_url": resolved_base.rstrip("/"),
            "file": file_cfg}


class GLabsClient:
    def __init__(self, base_url, api_key, opener=urllib.request.urlopen, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._opener = opener
        self.timeout = timeout

    # --- low-level ----------------------------------------------------------

    def _request(self, method, path, body=None, with_key=True):
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        data = json.dumps(body).encode() if body is not None else None
        headers = {}
        if body is not None:
            headers["Content-Type"] = "application/json"
        if with_key:
            headers["X-API-Key"] = self.api_key
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with self._opener(req, timeout=self.timeout) as resp:
                return resp.read()
        except HTTPError as e:
            raise GLabsError(e.code, e.read().decode(errors="replace")) from None

    def _json(self, method, path, body=None, with_key=True):
        raw = self._request(method, path, body=body, with_key=with_key)
        return json.loads(raw.decode())

    # --- API surface --------------------------------------------------------

    def health(self):
        return self._json("GET", "/api/health", with_key=False)

    def submit(self, endpoint, body):
        """POST /api/{endpoint}/generate -> 202 body with task_id."""
        return self._json("POST", f"/api/{endpoint}/generate", body=body)

    def status(self, task_id):
        return self._json("GET", f"/api/status/{task_id}")

    def download(self, url, dest):
        """GET a /api/files URL (no key) and write raw bytes to ``dest``."""
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        raw = self._request("GET", url, with_key=False)
        dest.write_bytes(raw)
        return dest
