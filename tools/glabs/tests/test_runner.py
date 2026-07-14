"""Tests for the runner's pure helpers (filenames, data-uri, episode resolution)."""
import base64
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from glabs import generate_media as gm


def test_scene_stem_zero_pads():
    assert gm.scene_stem(1) == "scene-001"
    assert gm.scene_stem(42) == "scene-042"
    assert gm.scene_stem(230) == "scene-230"


def test_ext_from_url():
    assert gm.ext_from_url("http://x/api/files/image_001.jpg") == ".jpg"
    assert gm.ext_from_url("http://x/api/files/image_001.png") == ".png"
    assert gm.ext_from_url("http://x/api/files/clip.mp4") == ".mp4"
    # url-encoded name still resolves
    assert gm.ext_from_url("http://x/api/files/my%20image.jpeg") == ".jpeg"
    # no extension -> default png
    assert gm.ext_from_url("http://x/api/files/noext") == ".png"


def test_output_path_uses_url_extension(tmp_path):
    stem = tmp_path / "scenes" / "scene-001"
    out = gm.output_path(stem, "http://x/api/files/image_001.jpg")
    assert out.name == "scene-001.jpg"


def test_load_refs_map_finds_any_image_extension(tmp_path):
    refs = tmp_path / "refs"
    refs.mkdir()
    (refs / "adaora.jpg").write_bytes(b"\xff\xd8\xff")
    (refs / "leonard.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    refs_map = gm._load_refs_map(refs)
    assert set(refs_map.keys()) == {"adaora", "leonard"}
    assert refs_map["adaora"].startswith("data:image/jpeg;base64,")
    assert refs_map["leonard"].startswith("data:image/png;base64,")


def test_to_data_uri_png(tmp_path):
    p = tmp_path / "x.png"
    p.write_bytes(b"\x89PNG\r\n\x1a\n")
    uri = gm.to_data_uri(p)
    assert uri.startswith("data:image/png;base64,")
    assert base64.b64decode(uri.split(",", 1)[1]) == b"\x89PNG\r\n\x1a\n"


def test_to_data_uri_jpeg(tmp_path):
    p = tmp_path / "x.jpg"
    p.write_bytes(b"\xff\xd8\xff")
    uri = gm.to_data_uri(p)
    assert uri.startswith("data:image/jpeg;base64,")


def test_resolve_episode_by_direct_scenes_path(tmp_path):
    (tmp_path / "tap-01-foo_scenes.txt").write_text("1. a scene\n")
    (tmp_path / "tap-01-foo_characters.txt").write_text("1. @x sheet\n")
    ep = gm.resolve_episode(tmp_path / "tap-01-foo_scenes.txt")
    assert ep.name == "tap-01-foo"
    assert ep.scenes_path.name == "tap-01-foo_scenes.txt"
    assert ep.characters_path.name == "tap-01-foo_characters.txt"
    assert ep.media_dir.name == "tap-01-foo_media"


def test_resolve_episode_by_basename_search(tmp_path):
    out = tmp_path / "niche" / "output"
    out.mkdir(parents=True)
    (out / "tap-02-bar_scenes.txt").write_text("1. a scene\n")
    (out / "tap-02-bar_characters.txt").write_text("1. @x sheet\n")
    ep = gm.resolve_episode("tap-02-bar", search_roots=[tmp_path])
    assert ep.scenes_path == out / "tap-02-bar_scenes.txt"
    assert ep.media_dir == out / "tap-02-bar_media"


def test_resolve_episode_missing_raises(tmp_path):
    with pytest.raises(Exception):
        gm.resolve_episode("does-not-exist", search_roots=[tmp_path])
