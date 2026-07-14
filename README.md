# Script-Writer Kit

A Claude Code starter kit for running a **multi-niche YouTube content assembly line** —
turning story ideas into finished TTS-narration assets (scripts → SRT + TTS lines →
character sheet + one image prompt per line → generated images).

You drive the whole thing from **Claude Code** with a working directory set to this
folder. Nothing here is a hosted service; it's a set of Markdown "brains" (skills,
agents, commands) plus one small Python image-generation tool.

## What's in the box

| Path | What it is |
|------|-----------|
| `example-niche/` | A **blank channel skeleton** you copy per niche. The structure and orchestration are done; the *writing formula* is left as `TODO` fill-ins. |
| `.claude/skills/` | Shared, niche-agnostic tooling: SRT cutter, SRT→image-prompts, English TTS normalization. |
| `.claude/commands/` | Shared slash commands: `/cut-and-prompt`, `/generate-media`. |
| `tools/glabs/` | Python package (stdlib-only) that turns an episode's prompt files into images via the G-Labs API. Fully tested. |
| `docs/` | Design spec for the media pipeline. |
| `CLAUDE.md` | Architecture guide Claude reads automatically. |

## Quick start

1. **Open this folder in Claude Code** (`cd` here, run `claude`). Claude auto-detects
   `.claude/skills` and `.claude/commands`.
2. **Make your first niche:**
   ```bash
   cp -R example-niche my-channel
   ```
   Then open `my-channel/README.md` and `my-channel/CLAUDE.md` and fill in every
   `TODO` — that's where your channel's genre, structure, and writing rules go.
   The `example-niche/skills/writer/SKILL.md` is the fill-in-the-blanks formula.
3. **Write scripts:** from `my-channel/`, run `/write-batch 5` (once you've defined
   your ideator) or drop briefs into `inbox/briefs.md` and run `/write-batch`.
4. **Cut + prompt:** `/cut-and-prompt output/<script>.txt --normalize`
   (`--normalize` for English scripts only).
5. **Generate images** (multi-image niches): start the local G-Labs API, copy
   `.glabs.example.json` → `.glabs.json` and add your key, then
   `/generate-media <episode-basename>`.

## Requirements

- **Claude Code** (this is a Claude Code project).
- **Python 3.11+** for `tools/glabs` (stdlib only — no `pip install` needed).
  Verify with: `python -m pytest tools/glabs/tests/ -q` → 68 passing.
- For image generation: a running **G-Labs Automation** local API and an API key.
  See `docs/generate-media-design.md` and the linked webhook contract.

## Read next

- `CLAUDE.md` — the full architecture (three-layer design, count contract, `@tag` contract).
- `example-niche/README.md` — how a niche brain is built, layer by layer.
- `docs/generate-media-design.md` — how `tools/glabs` works.
