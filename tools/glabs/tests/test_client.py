"""Tests for GLabsClient and config resolution (no live server)."""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from glabs import client as client_mod
from glabs.client import GLabsClient, load_config


class FakeResponse(io.BytesIO):
    def __init__(self, payload, status=200):
        super().__init__(payload if isinstance(payload, bytes) else json.dumps(payload).encode())
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()
        return False


class FakeOpener:
    """Records requests and returns queued responses."""
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def __call__(self, request, timeout=None):
        self.requests.append(request)
        return self.responses.pop(0)


# --- load_config ------------------------------------------------------------

def test_config_explicit_beats_env(monkeypatch):
    monkeypatch.setenv("GLABS_API_KEY", "envkey")
    cfg = load_config(api_key="explicit", base_url="http://x:1", config_path=None)
    assert cfg["api_key"] == "explicit"
    assert cfg["base_url"] == "http://x:1"


def test_config_env_beats_file(monkeypatch, tmp_path):
    p = tmp_path / ".glabs.json"
    p.write_text(json.dumps({"api_key": "filekey", "base_url": "http://file:9"}))
    monkeypatch.setenv("GLABS_API_KEY", "envkey")
    monkeypatch.delenv("GLABS_BASE_URL", raising=False)
    cfg = load_config(config_path=p)
    assert cfg["api_key"] == "envkey"
    # base_url not in env -> falls through to file
    assert cfg["base_url"] == "http://file:9"


def test_config_default_base_url(monkeypatch, tmp_path):
    monkeypatch.setenv("GLABS_API_KEY", "k")
    monkeypatch.delenv("GLABS_BASE_URL", raising=False)
    cfg = load_config(config_path=tmp_path / "nope.json")
    assert cfg["base_url"] == "http://127.0.0.1:8765"


def test_config_missing_key_raises(monkeypatch, tmp_path):
    monkeypatch.delenv("GLABS_API_KEY", raising=False)
    with pytest.raises(Exception):
        load_config(config_path=tmp_path / "nope.json")


# --- GLabsClient requests ---------------------------------------------------

def test_health_gets_health_endpoint_without_key():
    opener = FakeOpener(FakeResponse({"status": "ok"}))
    c = GLabsClient("http://127.0.0.1:8765", "secret", opener=opener)
    out = c.health()
    assert out == {"status": "ok"}
    req = opener.requests[0]
    assert req.full_url == "http://127.0.0.1:8765/api/health"
    assert req.get_method() == "GET"
    assert req.get_header("X-api-key") is None


def test_submit_posts_json_with_api_key():
    opener = FakeOpener(FakeResponse({"task_id": "abc12345", "status": "pending"}, status=202))
    c = GLabsClient("http://127.0.0.1:8765", "secret", opener=opener)
    out = c.submit("image", {"prompt": "a cat"})
    assert out["task_id"] == "abc12345"
    req = opener.requests[0]
    assert req.full_url == "http://127.0.0.1:8765/api/image/generate"
    assert req.get_method() == "POST"
    assert req.get_header("X-api-key") == "secret"
    assert req.get_header("Content-type") == "application/json"
    assert json.loads(req.data.decode()) == {"prompt": "a cat"}


def test_status_gets_task_with_key():
    opener = FakeOpener(FakeResponse({"task_id": "abc12345", "status": "completed"}))
    c = GLabsClient("http://127.0.0.1:8765", "secret", opener=opener)
    out = c.status("abc12345")
    assert out["status"] == "completed"
    req = opener.requests[0]
    assert req.full_url == "http://127.0.0.1:8765/api/status/abc12345"
    assert req.get_method() == "GET"
    assert req.get_header("X-api-key") == "secret"


def test_download_writes_bytes_without_key(tmp_path):
    opener = FakeOpener(FakeResponse(b"\x89PNG\r\n"))
    c = GLabsClient("http://127.0.0.1:8765", "secret", opener=opener)
    dest = tmp_path / "out" / "img.png"
    c.download("http://127.0.0.1:8765/api/files/image_001.png", dest)
    assert dest.read_bytes() == b"\x89PNG\r\n"
    req = opener.requests[0]
    assert req.get_header("X-api-key") is None
