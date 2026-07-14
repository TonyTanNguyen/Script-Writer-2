# Design: `/generate-media` — Script-Writer → G-Labs image pipeline

**Date:** 2026-07-09
**Status:** Approved (brainstorming) → ready for implementation plan

## Purpose

Wire the Script-Writer content pipeline into the **G-Labs Automation Webhook API**
so that one episode's generated prompt files are turned into a complete,
index-aligned image set — with each character's look held consistent across every
shot via the API's `@tag` reference-image binding.

The G-Labs API is documented at
`https://github.com/duckmartians/G-Labs-Automation/blob/main/WEBHOOK_INTEGRATION.en.md`.
It is a local-only REST API (`http://127.0.0.1:8765`) with a **submit → poll →
download** async workflow.

## Inputs (produced by the existing Script-Writer pipeline)

For an episode with basename `<name>` (e.g. `ep-01-sample`), the
`/cut-and-prompt` step emits (among others):

- `<name>_characters.txt` — numbered character sheet. Each line:
  `N. @tag (full description …), … character reference sheet, no text, no subtitles.`
  The whole line after the number **is** a ready-to-use image prompt.
- `<name>_scenes.txt` — one image prompt per SRT line (~230 for the sample).
  Each numbered entry is a self-contained prompt that references one or more
  `@tag`s (and may also mention anonymous, untagged people).

The **1:1 count contract** holds: scene-prompt count == SRT block count == TTS
line count. Scene image N must align by index to SRT/TTS line N.

## Output

Inside the episode folder, a new `<name>_media/` directory:

```
<name>_media/
  manifest.json            # per-item state: id, kind, task_id, status, error_code, error, file
  refs/<tag>.png           # one reference-sheet image per @tag  (e.g. refs/adaora.png)
  scenes/scene-001.png     # one image per scene line, zero-padded, index-aligned to SRT
  scenes/scene-002.png
  ...
```

## Two-phase generation

### Phase 1 — Character reference sheets
For each `N. @tag (…)` line in `<name>_characters.txt`:
- Submit `POST /api/image/generate` with `prompt` = the line text (minus the
  leading `N. `), **no reference images**, `aspect_ratio: "16:9"`.
- On `completed`, download the single result to `refs/<tag>.png`.

`<tag>` is the slug captured from `@tag` (lowercase `[a-z0-9_]+`). The saved
filename **is** `<tag>.png` so that §6.1 name-binding works in Phase 2: a scene
prompt containing `@<tag>` will bind to the image whose `name` is `<tag>.png`
(keyword = case-insensitive substring of filename without extension).

### Phase 2 — Scene images
For each numbered entry in `<name>_scenes.txt` (index = its SRT block number):
- Extract all `@tag`s in the prompt via regex `@([a-z0-9_]+)`.
- For each extracted tag that has a `refs/<tag>.png`, attach a reference image
  object: `{"data": "data:image/png;base64,<...>", "name": "<tag>.png"}`.
  (Cap at the image endpoint's max of 10; de-duplicate repeated tags.)
- Submit `POST /api/image/generate` with `prompt` = the entry text (minus the
  leading `N. `), the reference list above, `aspect_ratio: "16:9"`,
  `model` = configured model.
- On `completed`, download the single result to `scenes/scene-<NNN>.png`
  (`<NNN>` = zero-padded index, matching SRT block order).

Scenes whose prompt has no `@tag`, or tags with no matching ref file, simply
submit with fewer/zero references — never an error (per §6.1, unmatched tags stay
as literal text).

## Components

| File | Responsibility |
|------|----------------|
| `tools/glabs/client.py` | `GLabsClient`: `health()`, `submit(endpoint, body)`, `status(task_id)`, `download(url, dest)`. Reads base URL + API key from config/env. No business logic; a thin transport layer over the REST API. |
| `tools/glabs/generate_media.py` | Batch runner. Parses the two `.txt` files, builds payloads, runs Phase 1 then Phase 2 with a bounded concurrency window, polls, downloads, and maintains `manifest.json`. This is where all pipeline logic lives. |
| `.claude/commands/generate-media.md` | `/generate-media <episode-basename>` — checks server health, invokes the runner once via Bash, monitors, and reports a summary. |

## Configuration & secrets

- **Base URL:** default `http://127.0.0.1:8765`, override via `GLABS_BASE_URL`.
- **API key:** read from `GLABS_API_KEY` env var, or a **gitignored** `.glabs.json`
  at repo root (`{"api_key": "...", "base_url": "..."}`). The key is **never
  committed**. `.glabs.json` is added to `.gitignore`.
- **Model:** default `nano_banana_2`; `--model nano_banana_pro` for higher quality.
- **Aspect ratio:** `16:9` for both phases (this channel is always landscape).
- **Upscale:** off by default (2K/4K need ULTRA accounts + extra quota).

## Execution model

- **Concurrency window:** keep up to ~8 tasks in flight (server processes 10
  concurrently). Submit to fill the window, poll every ~4s, download each on
  completion, then submit the next.
- **Resume / idempotency:** on start, load `manifest.json`; skip any item already
  `completed` (verified by the presence of its output file). A re-run continues
  where a prior run stopped.
- **`--retry-failed`:** re-submit only items marked `failed`.
- **Precondition:** the Image (Flow) endpoint requires logged-in, enabled Google
  (Flow/Veo) accounts in the G-Labs app. If none are available, tasks fail with
  `error_code 0` / `No active accounts available` — surfaced in the summary.

## Error handling

- Per-item failure → record `error_code`, `error`, `error_detail` in the manifest;
  the batch continues to the next item.
- First `429` (daily quota / rate limit) → **stop submitting new tasks** in that
  phase and report; `--continue-on-quota` overrides.
- Submit-time HTTP errors (e.g. `401` bad key, `400` empty body) → abort with a
  clear message (these are config bugs, not per-item failures).
- A server-side watchdog fails tasks stuck with no result; the runner treats a
  `failed` status as terminal for that item.

## CLI surface (`generate_media.py`)

```
python tools/glabs/generate_media.py <episode-basename-or-path> \
    [--model nano_banana_2|nano_banana_pro] \
    [--phase all|refs|scenes] \
    [--limit N]            # only first N scenes (smoke test) \
    [--dry-run]            # build & print payloads, submit nothing \
    [--retry-failed] \
    [--continue-on-quota]
```

The command resolves `<episode-basename>` to the folder containing
`<name>_characters.txt` and `<name>_scenes.txt` (searches the niche `output/`
folders).

## Testing strategy

- **Unit tests (mocked HTTP), test-first:**
  - `@tag` extraction from prompt lines (single, multiple, none, repeated,
    punctuation-adjacent).
  - Character-sheet parsing: `N. @tag (…)` → `(tag, prompt)`.
  - tag → ref-file mapping, incl. missing-ref and >10-tag cap / de-dup.
  - Payload construction for both phases (correct `model`, `aspect_ratio`,
    reference `name` fields).
  - Manifest resume: completed items skipped, failed items retried.
  - Filename / index alignment (scene N → `scene-<NNN>.png`).
- **`--dry-run`** against a real episode's files
  (`<niche>/output/<episode>_characters.txt` + `_scenes.txt`) — verifies
  end-to-end parsing with zero quota cost.
- **`--limit` live smoke test:** generate character refs + first few scenes,
  eyeball consistency, before running the full ~230 batch.

## Out of scope (YAGNI for this build)

- Video / Grok / Meta endpoints (image only; `@tag` binding is image+Veo only,
  and stills match the one-image-per-line slideshow model).
- Upscaling.
- Automatic video assembly (stitching images + TTS audio into an .mp4).
- Multi-episode batch orchestration (this tool does one episode; a loop over
  episodes can wrap it later).
