"""Tests for building /api/image/generate request bodies."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from glabs import payloads


# --- build_ref_payload ------------------------------------------------------

def test_ref_payload_has_prompt_model_aspect():
    body = payloads.build_ref_payload("@adaora reference sheet", model="nano_banana_2")
    assert body["prompt"] == "@adaora reference sheet"
    assert body["model"] == "nano_banana_2"
    assert body["aspect_ratio"] == "16:9"


def test_ref_payload_has_no_reference_images():
    body = payloads.build_ref_payload("@adaora sheet", model="nano_banana_pro")
    assert "reference_images" not in body


def test_ref_payload_respects_model_and_aspect_overrides():
    body = payloads.build_ref_payload("x", model="nano_banana_pro", aspect_ratio="9:16")
    assert body["model"] == "nano_banana_pro"
    assert body["aspect_ratio"] == "9:16"


# --- build_scene_payload ----------------------------------------------------

REFS = {
    "adaora": "data:image/png;base64,AAAA",
    "leonard": "data:image/png;base64,BBBB",
}


def test_scene_payload_binds_matching_tags_as_named_refs():
    body = payloads.build_scene_payload(
        "@adaora and @leonard talk", ["adaora", "leonard"], REFS, model="nano_banana_2")
    assert body["prompt"] == "@adaora and @leonard talk"
    assert body["model"] == "nano_banana_2"
    assert body["aspect_ratio"] == "16:9"
    assert body["reference_images"] == [
        {"data": "data:image/png;base64,AAAA", "name": "adaora.png"},
        {"data": "data:image/png;base64,BBBB", "name": "leonard.png"},
    ]


def test_scene_payload_no_tags_omits_reference_images():
    body = payloads.build_scene_payload(
        "a basket of oranges", [], REFS, model="nano_banana_2")
    assert "reference_images" not in body


def test_scene_payload_skips_tags_without_a_ref_file():
    # @chidi has no ref in REFS -> only adaora attached, no error
    body = payloads.build_scene_payload(
        "@adaora meets @chidi", ["adaora", "chidi"], REFS, model="nano_banana_2")
    names = [r["name"] for r in body["reference_images"]]
    assert names == ["adaora.png"]


def test_scene_payload_all_tags_missing_omits_reference_images():
    body = payloads.build_scene_payload(
        "@nobody here", ["nobody"], REFS, model="nano_banana_2")
    assert "reference_images" not in body


def test_scene_payload_dedupes_and_preserves_order():
    body = payloads.build_scene_payload(
        "@leonard then @adaora then @leonard", ["leonard", "adaora", "leonard"],
        REFS, model="nano_banana_2")
    names = [r["name"] for r in body["reference_images"]]
    assert names == ["leonard.png", "adaora.png"]


def test_scene_payload_caps_reference_images_at_max():
    many = {f"c{i}": f"data:image/png;base64,{i}" for i in range(15)}
    tags = list(many.keys())
    body = payloads.build_scene_payload("scene", tags, many, model="nano_banana_2", max_refs=10)
    assert len(body["reference_images"]) == 10
    # keeps the first 10 in order
    assert [r["name"] for r in body["reference_images"]] == [f"c{i}.png" for i in range(10)]
