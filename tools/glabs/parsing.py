"""Parse Script-Writer prompt files into structured character / scene records.

The pipeline emits two files per episode:

- ``<name>_characters.txt`` — numbered lines ``N. @tag (description ...) ...``
  where the text after the number is a ready-to-use character-sheet prompt.
- ``<name>_scenes.txt`` — numbered entries (one per SRT block), each a
  self-contained image prompt that references one or more ``@tag``s.

Everything here is pure: string in, dataclasses out. No I/O.
"""
from dataclasses import dataclass, field
from typing import List
import re

# A tag is the slug right after '@': lowercase letters, digits, underscores.
_TAG_RE = re.compile(r"@([A-Za-z0-9_]+)")

# A numbered entry starts with e.g. "12. " at the start of a line.
_NUM_RE = re.compile(r"^\s*(\d+)\.\s*")


@dataclass
class Character:
    tag: str
    prompt: str


@dataclass
class Scene:
    index: int
    prompt: str
    tags: List[str] = field(default_factory=list)


def extract_tags(prompt: str) -> List[str]:
    """Return ``@tag`` slugs in first-appearance order, de-duplicated, lowercased."""
    seen = set()
    out = []
    for m in _TAG_RE.finditer(prompt):
        tag = m.group(1).lower()
        if tag not in seen:
            seen.add(tag)
            out.append(tag)
    return out


def _strip_leading_number(line: str) -> str:
    return _NUM_RE.sub("", line, count=1).strip()


def parse_characters(text: str) -> List[Character]:
    """One ``Character`` per numbered line that contains a ``@tag``."""
    chars = []
    for line in text.splitlines():
        if not _NUM_RE.match(line):
            continue
        tags = extract_tags(line)
        if not tags:
            continue
        chars.append(Character(tag=tags[0], prompt=_strip_leading_number(line)))
    return chars


def parse_scenes(text: str) -> List[Scene]:
    """One ``Scene`` per numbered entry; wrapped continuation lines are joined."""
    scenes: List[Scene] = []
    for raw in text.splitlines():
        m = _NUM_RE.match(raw)
        if m:
            prompt = _strip_leading_number(raw)
            scenes.append(Scene(index=int(m.group(1)), prompt=prompt,
                                tags=extract_tags(prompt)))
        elif scenes and raw.strip():
            # continuation of the current entry (wrapped physical line)
            cur = scenes[-1]
            cur.prompt = (cur.prompt + " " + raw.strip()).strip()
            cur.tags = extract_tags(cur.prompt)
    return scenes
