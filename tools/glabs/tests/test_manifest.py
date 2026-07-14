"""Tests for the resumable manifest."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from glabs.manifest import Manifest


def test_unknown_item_should_run(tmp_path):
    m = Manifest(tmp_path / "manifest.json")
    assert m.should_run("scene:001") is True
    assert m.status_of("scene:001") is None


def test_completed_item_is_not_rerun(tmp_path):
    m = Manifest(tmp_path / "manifest.json")
    m.mark_completed("scene:001", file="scenes/scene-001.png")
    assert m.status_of("scene:001") == "completed"
    assert m.should_run("scene:001") is False
    assert m.should_run("scene:001", retry_failed=True) is False


def test_failed_item_skipped_by_default_retried_on_flag(tmp_path):
    m = Manifest(tmp_path / "manifest.json")
    m.mark_failed("scene:002", error_code=429, error="quota", error_detail="429: quota")
    assert m.status_of("scene:002") == "failed"
    assert m.should_run("scene:002") is False
    assert m.should_run("scene:002", retry_failed=True) is True


def test_completed_record_keeps_file_path(tmp_path):
    m = Manifest(tmp_path / "manifest.json")
    m.mark_completed("ref:adaora", file="refs/adaora.png")
    assert m.get("ref:adaora")["file"] == "refs/adaora.png"


def test_failed_record_keeps_error_fields(tmp_path):
    m = Manifest(tmp_path / "manifest.json")
    m.mark_failed("scene:003", error_code=403, error="PERMISSION_DENIED", error_detail="403: nope")
    item = m.get("scene:003")
    assert item["error_code"] == 403
    assert item["error"] == "PERMISSION_DENIED"
    assert item["error_detail"] == "403: nope"


def test_save_and_reload_roundtrip(tmp_path):
    path = tmp_path / "manifest.json"
    m = Manifest(path)
    m.mark_completed("scene:001", file="scenes/scene-001.png")
    m.mark_failed("scene:002", error_code=429, error="quota", error_detail="x")
    m.save()

    reloaded = Manifest.load(path)
    assert reloaded.status_of("scene:001") == "completed"
    assert reloaded.status_of("scene:002") == "failed"
    assert reloaded.get("scene:001")["file"] == "scenes/scene-001.png"


def test_load_missing_file_starts_empty(tmp_path):
    m = Manifest.load(tmp_path / "does-not-exist.json")
    assert m.status_of("anything") is None


def test_counts_summary(tmp_path):
    m = Manifest(tmp_path / "manifest.json")
    m.mark_completed("a", file="a.png")
    m.mark_completed("b", file="b.png")
    m.mark_failed("c", error_code=429, error="q", error_detail="q")
    counts = m.counts()
    assert counts["completed"] == 2
    assert counts["failed"] == 1
