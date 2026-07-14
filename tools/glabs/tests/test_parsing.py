"""Tests for parsing character-sheet and scene prompt files."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from glabs import parsing


# --- extract_tags -----------------------------------------------------------

def test_extract_tags_single():
    assert parsing.extract_tags("@adaora holding an orange") == ["adaora"]


def test_extract_tags_multiple_in_order():
    prompt = "@adaora talks to @leonard at the stall"
    assert parsing.extract_tags(prompt) == ["adaora", "leonard"]


def test_extract_tags_none():
    assert parsing.extract_tags("a middle-aged market woman pauses") == []


def test_extract_tags_deduplicates_preserving_first_order():
    prompt = "@adaora looks at @leonard while @adaora smiles"
    assert parsing.extract_tags(prompt) == ["adaora", "leonard"]


def test_extract_tags_stops_at_punctuation():
    # tag followed by comma / apostrophe-s should capture only the slug
    assert parsing.extract_tags("@ngozika, weary, lies down") == ["ngozika"]
    assert parsing.extract_tags("@adaora's basket") == ["adaora"]


def test_extract_tags_allows_digits_and_underscore():
    assert parsing.extract_tags("@red_car2 parked") == ["red_car2"]


def test_extract_tags_email_not_matched_as_multiple():
    # a bare '@' inside an email-like token still only grabs the slug after '@'
    assert parsing.extract_tags("mail user@gmail here") == ["gmail"]


# --- parse_characters -------------------------------------------------------

def test_parse_characters_extracts_tag_and_prompt():
    text = "1. @mia (a woman in her 30s), full body reference sheet, no text."
    chars = parsing.parse_characters(text)
    assert len(chars) == 1
    assert chars[0].tag == "mia"
    # prompt is the line with the leading "N. " stripped
    assert chars[0].prompt.startswith("@mia (a woman in her 30s)")
    assert "1." not in chars[0].prompt.split("@")[0]


def test_parse_characters_multiple_lines_blank_separated():
    text = (
        "1. @adaora (a) reference sheet.\n"
        "\n"
        "2. @leonard (b) reference sheet.\n"
    )
    chars = parsing.parse_characters(text)
    assert [c.tag for c in chars] == ["adaora", "leonard"]


def test_parse_characters_ignores_lines_without_tag():
    text = "1. @adaora (a) sheet.\nsome stray note\n2. @leonard (b) sheet.\n"
    chars = parsing.parse_characters(text)
    assert [c.tag for c in chars] == ["adaora", "leonard"]


# --- parse_scenes -----------------------------------------------------------

def test_parse_scenes_indexes_from_one():
    text = (
        "1. @adaora at the stall. No text.\n"
        "\n"
        "2. @adaora and @leonard talk. No text.\n"
    )
    scenes = parsing.parse_scenes(text)
    assert [s.index for s in scenes] == [1, 2]


def test_parse_scenes_prompt_strips_leading_number():
    text = "1. @adaora at the stall. No text, no subtitles.\n"
    scenes = parsing.parse_scenes(text)
    assert scenes[0].prompt.startswith("@adaora at the stall")


def test_parse_scenes_collects_tags_per_scene():
    text = "1. @adaora and @leonard talk. No text.\n"
    scenes = parsing.parse_scenes(text)
    assert scenes[0].tags == ["adaora", "leonard"]


def test_parse_scenes_scene_with_no_tag():
    text = "1. A wide basket of oranges in the corner. No text.\n"
    scenes = parsing.parse_scenes(text)
    assert scenes[0].tags == []


def test_parse_scenes_multiline_entry_joined():
    # a numbered entry that wraps across physical lines is one scene
    text = "1. @adaora at the stall,\ncalling out to the crowd. No text.\n"
    scenes = parsing.parse_scenes(text)
    assert len(scenes) == 1
    assert "calling out to the crowd" in scenes[0].prompt


# --- against a bundled sample file -----------------------------------------

def _sample(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", name)


def test_real_characters_file_parses_all():
    path = _sample("sample_characters.txt")
    with open(path, encoding="utf-8") as f:
        chars = parsing.parse_characters(f.read())
    tags = [c.tag for c in chars]
    assert tags == ["mia", "noah", "ivy"]


def test_real_scenes_file_indices_are_contiguous():
    path = _sample("sample_scenes.txt")
    with open(path, encoding="utf-8") as f:
        scenes = parsing.parse_scenes(f.read())
    assert len(scenes) > 0
    assert [s.index for s in scenes] == list(range(1, len(scenes) + 1))
