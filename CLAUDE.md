# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **starter kit** for a multi-niche YouTube content assembly line. Two things live
side by side:

1. **A content assembly line** — one or more *niche* folders, each a self-contained
   "brain" (Markdown skills/agents/commands) that turns story ideas into finished
   TTS-narration assets. This kit ships **one worked example niche** (`example-niche/`)
   that you copy and fill in per channel. **Each niche has its own `CLAUDE.md` — read
   it before doing any work in that niche.** There is no build/lint/test for this
   part; it is prose pipelines executed by Claude.
2. **`tools/glabs/`** — a real Python package (stdlib-only) that wires an episode's
   generated prompt files into a local **G-Labs Automation** image-generation API.
   This is the only part with code and tests.

> This is a template. `example-niche/` is a skeleton with the writing/prompt formulas
> left as `TODO` fill-ins — the shared *engine* is complete and ready to run. Copy
> `example-niche/` to `your-niche/`, fill in its `CLAUDE.md` + `skills/writer/SKILL.md`,
> and you have a working channel brain. See `example-niche/README.md`.

## tools/glabs — the media generation pipeline

Turns a multi-image episode's `<name>_characters.txt` + `<name>_scenes.txt` into an
index-aligned image set, using the G-Labs webhook API (`http://127.0.0.1:8765`,
async submit → poll → download). Full design: `docs/generate-media-design.md`.
API contract: https://github.com/duckmartians/G-Labs-Automation/blob/main/WEBHOOK_INTEGRATION.en.md

### Commands
```bash
# Run all tests
python -m pytest tools/glabs/tests/ -q
# Run one test
python -m pytest tools/glabs/tests/test_parsing.py::test_extract_tags_single -q

# Preview the plan for an episode (zero quota, no network)
python tools/glabs/generate_media.py <episode-basename> --dry-run
# Smoke test: char refs + first N scenes
python tools/glabs/generate_media.py <episode-basename> --limit 5
# Full episode (resumes automatically if interrupted)
python tools/glabs/generate_media.py <episode-basename>
# Re-run only the items that failed
python tools/glabs/generate_media.py <episode-basename> --retry-failed
```
`<episode-basename>` is resolved by searching the niche `output/` folders for
`<name>_scenes.txt`; a direct path to any of the episode's files also works. The
`/generate-media` slash command wraps this — it is the intended entry point (it does
health-check + monitoring); **do not hand-drive the ~240 async generations yourself.**

### Module layout (pure logic separated from I/O)
- `parsing.py` — extract `@tags`; parse character/scene files → dataclasses. Pure.
- `payloads.py` — build `/api/image/generate` bodies; binds each `@tag` to its ref. Pure.
- `manifest.py` — resumable per-episode state (`<name>_media/manifest.json`).
- `rotate.py` — bounded VPN-rotation policy (pure `should_rotate` + a shell-command runner).
- `client.py` — thin `urllib` transport (submit/status/download/health). Injectable
  opener so it is testable without a live server.
- `generate_media.py` — two-phase orchestration + CLI.

### Non-obvious invariants (violating these silently breaks output)
- **Refs must exist on disk before scenes are planned.** Phase 1 (refs) downloads
  `<name>_media/refs/<tag>.<ext>`; Phase 2 reads them back and attaches each as a
  reference image whose `name` is `<tag>.png`, so `@tag` in the scene prompt binds
  to that character (webhook §6.1 name-binding). `run()` enforces this ordering.
- **Extensions are server-decided, not assumed.** The API returns JPEG or PNG; the
  actual extension comes from the result URL. The ref lookup must match *any* image
  extension, and done-detection consults the manifest's recorded file.
- **1K only, always 16:9.** No `upscale` is ever sent; aspect is `16:9` for both phases.
- **Resume key:** an item is "done" iff the manifest marks it `completed` *and* the
  recorded file still exists. `--retry-failed` re-runs `failed` items.
- **Transient `400 INVALID_ARGUMENT`** usually clears on retry; a `429` stops the
  phase (daily quota). Per-item failures never abort the batch.

### Config / secrets
API key + base URL come from `--api-key`/`--base-url`, then `GLABS_API_KEY`/
`GLABS_BASE_URL`, then `.glabs.json` at repo root, then the default base URL.
**Copy `.glabs.example.json` to `.glabs.json` and put your own key in it.**
`.glabs.json` and all `*_media/` output are gitignored — the key is never committed.

## Content-pipeline architecture (the niches)

Every niche shares one design (details in each niche's CLAUDE.md):

- **Three layers:** `skills/*/SKILL.md` = the invariant writing/prompt *formula*
  (quality); a fresh clean-context **sub-agent per script** = consistency at scale
  (the 10th script is written under the same clean conditions as the 1st); a
  **command orchestrator** (`.claude/commands/*.md`) = the batch loop that dispatches,
  gates, and records. The orchestrator writes no prose itself.
- **Per-niche flow:** `/ideas-from-channel` (or a viral ideator) → `inbox/briefs.md`;
  `/write-batch` → `output/<prefix>-NN-*.txt` (one clean-context writer sub-agent per
  brief); then the shared `/cut-and-prompt <script> --normalize`.
- **Shared cut → SRT/TTS → image-prompt tooling ships in `.claude/`** here
  (`skills/srt-cut.py`, `skills/srt-to-image-prompts/`, the `/cut-and-prompt`
  command). Niche folders hold only their own brain + `knowledge/`/`inbox/`/`output/`.
- **Anti-repeat ledgers** (`knowledge/used-*.txt`) are the originality guarantee:
  both idea generation and `/write-batch` gate against them, but **only `/write-batch`
  appends** (on an actual write) so discarded ideas never pollute the taken-list.

### Two contracts that connect the pipeline to tools/glabs
- **Count contract (multi-image niches):** SRT block N == TTS line N == scene-prompt N
  == generated image N. Everything aligns by order/index; any mismatch desyncs the
  video.
- **`@tag` contract:** character-sheet lines *lead with the `@tag`* (e.g.
  `1. @mia (...)`), and scene prompts reuse those same tags. This is exactly what
  `tools/glabs` keys on for character consistency. Image prompts are always English.

### Multi-image vs single-image niches
- **Multi-image** niches produce `_characters.txt` + `_scenes.txt` (~one image per
  SRT line) via `/cut-and-prompt`. These feed `tools/glabs`.
- **Single-image** niches use one static image for the whole video, so they produce
  only prompt(s) for that image and **no SRT / no `_scenes.txt`**. `tools/glabs` (as
  built) does not apply to them.
- `--normalize` is mandatory in **English** niches (TTS-normalizes before cutting);
  it is OFF by default in the global command because non-English niches must skip it.
