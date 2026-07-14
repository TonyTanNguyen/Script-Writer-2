"""Build request bodies for POST /api/image/generate.

Pure functions: no network. A scene binds each ``@tag`` to its character
reference image by giving the reference object a ``name`` of ``<tag>.png`` so
the webhook's §6.1 name-binding pins that character in the shot.
"""
from typing import Dict, List

DEFAULT_MODEL = "nano_banana_2"
DEFAULT_ASPECT = "16:9"
MAX_IMAGE_REFS = 10  # per the image endpoint's documented maximum


def build_ref_payload(prompt: str, model: str = DEFAULT_MODEL,
                      aspect_ratio: str = DEFAULT_ASPECT) -> dict:
    """Character reference sheet: prompt only, no reference images."""
    return {"prompt": prompt, "model": model, "aspect_ratio": aspect_ratio}


def build_scene_payload(prompt: str, tags: List[str], refs: Dict[str, str],
                        model: str = DEFAULT_MODEL,
                        aspect_ratio: str = DEFAULT_ASPECT,
                        max_refs: int = MAX_IMAGE_REFS) -> dict:
    """Scene image: attach the ref image for each tag that has one.

    ``refs`` maps ``tag -> base64/data-URI string``. Tags with no ref are
    skipped (never an error). Duplicates are dropped preserving first order,
    and the list is capped at ``max_refs``.
    """
    body = {"prompt": prompt, "model": model, "aspect_ratio": aspect_ratio}

    reference_images = []
    used = set()
    for tag in tags:
        if tag in used or tag not in refs:
            continue
        used.add(tag)
        reference_images.append({"data": refs[tag], "name": f"{tag}.png"})
        if len(reference_images) >= max_refs:
            break

    if reference_images:
        body["reference_images"] = reference_images
    return body
