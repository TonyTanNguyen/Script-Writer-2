# Claude bundle for the Script-Writer Kit

These skills + commands travel with this repo, so any niche folder opened under it
(or the repo root) can use them.

## Contents

**Skills** (`.claude/skills/`)
- `srt-to-image-prompts` — turn an SRT into a character sheet + one image prompt per block
- `english-tts-normalization` — clean an English script into read-ready TTS text
- `srt-cut.py`, `srt-cleaner.html` — shared helpers used by the SRT pipeline

**Commands** (`.claude/commands/`)
- `cut-and-prompt` — one script → SRT + TTS-script + image prompts
- `generate-media` — generate an episode's images via the G-Labs API (wraps `tools/glabs`)

## Using on another machine

When you open this folder (or a niche subfolder) as the working directory, Claude Code
auto-detects the project-level `.claude/skills` and `.claude/commands`.

To make them available **globally** (in every project) instead, copy them up:

```bash
cp -R .claude/skills/*   ~/.claude/skills/
cp -R .claude/commands/* ~/.claude/commands/
```

> A niche's own `.claude/agents` and `.claude/commands` (e.g. `write-batch`) live
> inside that niche folder, not here — this bundle is only the shared, niche-agnostic
> tooling.
