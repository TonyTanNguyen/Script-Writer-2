---
description: Generate an episode's character-reference + scene images via the G-Labs webhook API
argument-hint: <episode-basename> [--limit N] [--model nano_banana_pro] [--phase refs|scenes] [--dry-run] [--retry-failed]
---

# /generate-media

Turn one episode's Script-Writer prompt files (`<name>_characters.txt` +
`<name>_scenes.txt`) into a complete, index-aligned image set using the local
**G-Labs Automation** webhook API. Character `@tag`s are bound to their
reference images so each character stays consistent across every shot.

Arguments (verbatim): `$ARGUMENTS`

The heavy lifting is done by a resumable Python runner — do **not** hand-drive
the ~240 async generations yourself. Your job is to launch it, monitor, and
report.

## Steps

1. **Preflight.** Confirm the runner and config exist and the server is up:
   ```bash
   test -f .glabs.json && curl -sS -m 10 http://127.0.0.1:8765/api/health
   ```
   - If health fails: the G-Labs app's **Webhook** tab isn't started — tell the
     user to open it and click **Start**, then stop.
   - Remind the user (once) that the image endpoint needs logged-in, **enabled
     Google Flow/Veo accounts** in the app, or every task fails with
     `No active accounts available`.

2. **Dry-run first** (zero quota) to show the plan and catch parsing issues:
   ```bash
   python tools/glabs/generate_media.py <episode-basename> --dry-run
   ```
   Report the ref count + scene count back to the user.

3. **Smoke test** before the full batch — generate refs + a few scenes:
   ```bash
   python tools/glabs/generate_media.py <episode-basename> --limit 5
   ```
   Run this **in the background** (it polls for minutes). When it finishes,
   report how many completed/failed and where the files landed
   (`<...>_media/refs/`, `<...>_media/scenes/`). Ask the user to eyeball the
   images before the full run.

4. **Full run** once the user approves the smoke test:
   ```bash
   python tools/glabs/generate_media.py <episode-basename>
   ```
   Run in the background. It resumes automatically if interrupted (skips
   already-completed items via `<...>_media/manifest.json`). On a `429` it stops
   the phase (daily quota) — report that and suggest re-running later or
   `--continue-on-quota`.

5. **Report** the final `completed=/failed=` summary. If any failed, read the
   manifest and summarize the `error_code`s (e.g. `429` = quota, `403` =
   session/permission, `0` = no accounts / validation). Suggest
   `--retry-failed` for transient failures.

## Notes
- Pass extra flags straight through: `--model nano_banana_pro`, `--phase refs`,
  `--aspect 16:9` (default), `--window N` (concurrency, default 8).
- Output images align 1:1 by index to the SRT/TTS lines (`scene-001.png` = line 1),
  preserving the pipeline's count contract.
- The API key lives in `.glabs.json` (gitignored). Never print it.
