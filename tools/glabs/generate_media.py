#!/usr/bin/env python3
"""Generate an episode's image set from Script-Writer prompt files via G-Labs.

Two phases:
  1. refs   — one reference-sheet image per @tag in <name>_characters.txt
  2. scenes — one image per line in <name>_scenes.txt, with each @tag bound to
              its reference image so the character stays consistent across shots

Async submit -> poll -> download, with a bounded concurrency window and a
resumable manifest. Standard library only.

Usage:
    python tools/glabs/generate_media.py <episode-basename-or-path> [options]
"""
import argparse
import base64
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

# Allow running as a script (python tools/glabs/generate_media.py ...)
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from glabs import parsing, payloads, rotate as rotate_mod
    from glabs.client import GLabsClient, GLabsError, load_config
    from glabs.manifest import Manifest
    from glabs.rotate import RotatePolicy, should_rotate
else:
    from . import parsing, payloads, rotate as rotate_mod
    from .client import GLabsClient, GLabsError, load_config
    from .manifest import Manifest
    from .rotate import RotatePolicy, should_rotate

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_KNOWN_SUFFIXES = ("_characters.txt", "_scenes.txt", "_tts.txt",
                   "_normalized.txt", ".srt", ".txt")
_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".webp": "image/webp"}


# --- pure helpers -----------------------------------------------------------

def scene_stem(index):
    return f"scene-{index:03d}"


def ext_from_url(url):
    """Extension of the file the result URL points at, lowercased; default .png."""
    name = unquote(urlparse(url).path).rsplit("/", 1)[-1]
    dot = name.rfind(".")
    return name[dot:].lower() if dot != -1 else ".png"


def output_path(stem_path, url):
    """Final destination: the stem plus the extension the server actually returned."""
    stem_path = Path(stem_path)
    return stem_path.with_name(stem_path.name + ext_from_url(url))


def to_data_uri(path):
    path = Path(path)
    mime = _MIME.get(path.suffix.lower(), "image/png")
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def _strip_suffixes(name):
    for suf in _KNOWN_SUFFIXES:
        if name.endswith(suf):
            return name[: -len(suf)]
    return name


@dataclass
class Episode:
    name: str
    characters_path: Path
    scenes_path: Path
    media_dir: Path


def resolve_episode(arg, search_roots=None):
    """Locate an episode's files from a basename or a path to one of its files."""
    p = Path(arg)
    if p.exists() and p.is_file():
        folder = p.parent
        name = _strip_suffixes(p.name)
    else:
        name = _strip_suffixes(p.name)
        folder = None
        for root in (search_roots or [Path.cwd(), REPO_ROOT]):
            match = next(Path(root).rglob(f"{name}_scenes.txt"), None)
            if match:
                folder = match.parent
                break
        if folder is None:
            raise FileNotFoundError(
                f"Could not find {name}_scenes.txt under any search root")
    return Episode(
        name=name,
        characters_path=folder / f"{name}_characters.txt",
        scenes_path=folder / f"{name}_scenes.txt",
        media_dir=folder / f"{name}_media",
    )


# --- planning ---------------------------------------------------------------

@dataclass
class Item:
    item_id: str
    body: dict
    dest_stem: Path   # destination without extension; the server picks the ext


def _load_refs_map(refs_dir):
    """tag -> data URI, for every reference image already on disk (any extension)."""
    refs = {}
    if refs_dir.exists():
        for f in sorted(refs_dir.iterdir()):
            if f.is_file() and f.suffix.lower() in _MIME:
                refs[f.stem] = to_data_uri(f)
    return refs


def plan_refs(episode, model, aspect):
    if not episode.characters_path.exists():
        return []
    chars = parsing.parse_characters(episode.characters_path.read_text(encoding="utf-8"))
    refs_dir = episode.media_dir / "refs"
    return [
        Item(item_id=f"ref:{c.tag}",
             body=payloads.build_ref_payload(c.prompt, model=model, aspect_ratio=aspect),
             dest_stem=refs_dir / c.tag)
        for c in chars
    ]


def plan_scenes(episode, model, aspect, limit=None):
    scenes = parsing.parse_scenes(episode.scenes_path.read_text(encoding="utf-8"))
    if limit:
        scenes = scenes[:limit]
    refs_map = _load_refs_map(episode.media_dir / "refs")
    scenes_dir = episode.media_dir / "scenes"
    items = []
    for s in scenes:
        body = payloads.build_scene_payload(s.prompt, s.tags, refs_map,
                                            model=model, aspect_ratio=aspect)
        items.append(Item(item_id=f"scene:{s.index:03d}",
                          body=body,
                          dest_stem=scenes_dir / scene_stem(s.index)))
    return items


# --- execution --------------------------------------------------------------

def _is_done(manifest, item, media_dir, retry_failed):
    rec = manifest.get(item.item_id)
    if not rec:
        return False
    if rec["status"] == "completed":
        # only truly done if the recorded output file still exists on disk
        f = rec.get("file")
        return bool(f) and (media_dir / f).exists()
    if rec["status"] == "failed":
        return not retry_failed
    return False


def run_phase(name, items, client, manifest, media_dir, *, endpoint="image",
              window=8, poll_interval=4, retry_failed=False,
              continue_on_quota=False, dry_run=False, rotate_policy=None,
              rotate_fn=rotate_mod.run_rotate_command, sleep_fn=time.sleep, log=print):
    """Submit -> poll -> download a list of items. Returns True unless quota-stopped."""
    rotate_policy = rotate_policy or RotatePolicy()
    todo = [it for it in items if not _is_done(manifest, it, media_dir, retry_failed)]
    skipped = len(items) - len(todo)
    log(f"[{name}] {len(todo)} to generate, {skipped} already done/skipped")

    if dry_run:
        for it in todo:
            refs = it.body.get("reference_images", [])
            names = ", ".join(r["name"] for r in refs) or "-"
            log(f"  DRY {it.item_id} -> {it.dest_stem.name}.* | model={it.body['model']} "
                f"aspect={it.body['aspect_ratio']} refs=[{names}]")
        return True

    queue = list(todo)
    inflight = {}   # task_id -> Item
    quota_stopped = False
    rotations_used = 0
    requeues = {}   # item_id -> count

    while queue or inflight:
        while queue and len(inflight) < window and not quota_stopped:
            it = queue.pop(0)
            resp = client.submit(endpoint, it.body)
            inflight[resp["task_id"]] = it

        if inflight:
            sleep_fn(poll_interval)

        for task_id, it in list(inflight.items()):
            s = client.status(task_id)
            status = s.get("status")
            if status in ("pending", "running"):
                continue
            del inflight[task_id]
            if status == "completed":
                results = s.get("results", [])
                first_dest = None
                for i, url in enumerate(results):
                    stem = it.dest_stem if i == 0 else it.dest_stem.with_name(
                        f"{it.dest_stem.name}-{i}")
                    dest = output_path(stem, url)
                    client.download(url, dest)
                    if i == 0:
                        first_dest = dest
                rel = str(first_dest.relative_to(media_dir)) if first_dest else ""
                manifest.mark_completed(it.item_id, rel)
                log(f"  ok  {it.item_id} -> {first_dest.name if first_dest else '(no file)'}")
            else:  # failed
                ec = s.get("error_code")
                if should_rotate(rotate_policy, ec, rotations_used, requeues.get(it.item_id, 0)):
                    rotations_used += 1
                    requeues[it.item_id] = requeues.get(it.item_id, 0) + 1
                    log(f"  ROTATE {it.item_id} [{ec}] {s.get('error')} -> "
                        f"rotating VPN ({rotations_used}/{rotate_policy.max_rotations}) & requeueing")
                    ok, out = rotate_fn(rotate_policy.cmd)
                    if out:
                        log(f"    rotate: {out.splitlines()[-1] if out.splitlines() else out}")
                    sleep_fn(rotate_policy.cooldown)
                    queue.append(it)   # re-queue for a fresh submit on the new IP
                else:
                    manifest.mark_failed(it.item_id, ec, s.get("error"), s.get("error_detail"))
                    log(f"  FAIL {it.item_id} [{ec}] {s.get('error')}")
                    if ec == 429 and not continue_on_quota:
                        quota_stopped = True
            manifest.save()

        if quota_stopped and not inflight:
            log(f"[{name}] stopped: daily quota / rate limit (429). "
                f"Re-run later or pass --continue-on-quota.")
            manifest.save()
            return False

    manifest.save()
    return True


def run(episode, client, *, model, aspect, phase, limit, dry_run, retry_failed,
        continue_on_quota, window, poll_interval, rotate_policy=None, log=print):
    media_dir = episode.media_dir
    media_dir.mkdir(parents=True, exist_ok=True)
    manifest = Manifest.load(media_dir / "manifest.json")

    if phase in ("all", "refs"):
        ok = run_phase("refs", plan_refs(episode, model, aspect), client, manifest,
                       media_dir, window=window, poll_interval=poll_interval,
                       retry_failed=retry_failed, continue_on_quota=continue_on_quota,
                       dry_run=dry_run, rotate_policy=rotate_policy, log=log)
        if not ok:
            return manifest

    if phase in ("all", "scenes"):
        # refs must exist on disk before scenes are planned (for @tag binding)
        run_phase("scenes", plan_scenes(episode, model, aspect, limit=limit), client,
                  manifest, media_dir, window=window, poll_interval=poll_interval,
                  retry_failed=retry_failed, continue_on_quota=continue_on_quota,
                  dry_run=dry_run, rotate_policy=rotate_policy, log=log)

    return manifest


# --- CLI --------------------------------------------------------------------

def build_rotate_policy(args, file_cfg):
    """Merge rotation settings: CLI flag > .glabs.json > default."""
    fc = file_cfg or {}
    cmd = args.rotate_cmd if args.rotate_cmd is not None else fc.get("rotate_cmd")
    raw_codes = args.rotate_on if args.rotate_on is not None else fc.get("rotate_on_codes")
    if isinstance(raw_codes, str):
        codes = {int(x) for x in raw_codes.split(",") if x.strip()}
    elif isinstance(raw_codes, (list, tuple)):
        codes = {int(x) for x in raw_codes}
    else:
        codes = {403}
    max_rot = args.max_rotations if args.max_rotations is not None else fc.get("max_rotations", 3)
    cooldown = (args.rotate_cooldown if args.rotate_cooldown is not None
                else fc.get("rotate_cooldown", 25.0))
    return RotatePolicy(cmd=cmd, codes=codes, max_rotations=max_rot, cooldown=cooldown)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate episode images via G-Labs webhook API")
    ap.add_argument("episode", help="episode basename (e.g. ep-01-sample) or a path to one of its files")
    ap.add_argument("--model", default=payloads.DEFAULT_MODEL,
                    choices=["nano_banana_2", "nano_banana_2_lite", "nano_banana_pro"])
    ap.add_argument("--aspect", default=payloads.DEFAULT_ASPECT)
    ap.add_argument("--phase", default="all", choices=["all", "refs", "scenes"])
    ap.add_argument("--limit", type=int, default=None, help="only the first N scenes")
    ap.add_argument("--dry-run", action="store_true", help="build & print payloads; submit nothing")
    ap.add_argument("--retry-failed", action="store_true")
    ap.add_argument("--continue-on-quota", action="store_true")
    ap.add_argument("--window", type=int, default=8, help="max concurrent tasks in flight")
    ap.add_argument("--poll-interval", type=float, default=4.0)
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--config", default=str(REPO_ROOT / ".glabs.json"))
    # VPN auto-rotation on IP/geo failures (e.g. 403). Off unless --rotate-cmd or config given.
    ap.add_argument("--rotate-cmd", default=None,
                    help="shell command to switch VPN; run when an item fails with a rotate code")
    ap.add_argument("--rotate-on", default=None,
                    help="comma-separated error codes that trigger rotation (default 403)")
    ap.add_argument("--max-rotations", type=int, default=None,
                    help="phase-wide cap on VPN rotations (default 3)")
    ap.add_argument("--rotate-cooldown", type=float, default=None,
                    help="seconds to wait after rotating before retrying (default 25)")
    args = ap.parse_args(argv)

    episode = resolve_episode(args.episode)

    client = None
    rotate_policy = None
    if not args.dry_run:
        cfg = load_config(api_key=args.api_key, base_url=args.base_url, config_path=args.config)
        client = GLabsClient(cfg["base_url"], cfg["api_key"])
        try:
            health = client.health()
            print(f"Server: {health.get('server')} ({health.get('status')}), "
                  f"base={cfg['base_url']}")
        except GLabsError as e:
            print(f"ERROR: cannot reach G-Labs server at {cfg['base_url']}: {e}", file=sys.stderr)
            return 2
        rotate_policy = build_rotate_policy(args, cfg.get("file"))
        if rotate_policy.enabled:
            print(f"VPN auto-rotate: ON (codes={sorted(rotate_policy.codes)}, "
                  f"max={rotate_policy.max_rotations}, cooldown={rotate_policy.cooldown}s)")

    print(f"Episode: {episode.name}  ->  {episode.media_dir}")
    manifest = run(episode, client, model=args.model, aspect=args.aspect,
                   phase=args.phase, limit=args.limit, dry_run=args.dry_run,
                   retry_failed=args.retry_failed,
                   continue_on_quota=args.continue_on_quota,
                   window=args.window, poll_interval=args.poll_interval,
                   rotate_policy=rotate_policy)

    if not args.dry_run:
        counts = manifest.counts()
        print(f"Done. completed={counts.get('completed', 0)} "
              f"failed={counts.get('failed', 0)}  ({episode.media_dir})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
