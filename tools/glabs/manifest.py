"""Resumable per-episode manifest.

Tracks the state of every generation item (character ref or scene) so a run can
resume where a prior run stopped. One JSON file per episode media folder.

Item ids look like ``ref:adaora`` or ``scene:001``. Each record carries a
``status`` (``completed`` | ``failed``), plus the output ``file`` (completed) or
the ``error_code`` / ``error`` / ``error_detail`` (failed).
"""
from collections import Counter
from pathlib import Path
import json


class Manifest:
    def __init__(self, path, items=None):
        self.path = Path(path)
        self.items = items or {}

    # --- construction -------------------------------------------------------

    @classmethod
    def load(cls, path):
        p = Path(path)
        if not p.exists():
            return cls(p)
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        return cls(p, items=data.get("items", {}))

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"items": self.items}, f, indent=2, ensure_ascii=False)
        tmp.replace(self.path)

    # --- queries ------------------------------------------------------------

    def get(self, item_id):
        return self.items.get(item_id)

    def status_of(self, item_id):
        item = self.items.get(item_id)
        return item["status"] if item else None

    def should_run(self, item_id, retry_failed=False):
        status = self.status_of(item_id)
        if status == "completed":
            return False
        if status == "failed":
            return retry_failed
        return True

    def counts(self):
        return dict(Counter(i["status"] for i in self.items.values()))

    # --- mutation -----------------------------------------------------------

    def mark_completed(self, item_id, file):
        self.items[item_id] = {"status": "completed", "file": file}

    def mark_failed(self, item_id, error_code, error, error_detail):
        self.items[item_id] = {
            "status": "failed",
            "error_code": error_code,
            "error": error,
            "error_detail": error_detail,
        }
