# CLAUDE.md — <YOUR NICHE NAME>

> **This is a template.** Copy the `example-niche/` folder to `<your-niche>/`, then
> replace every `TODO`/`<…>` placeholder below with your channel's specifics. The
> *structure* (three layers, the count contract, the uniqueness gate) is the part you
> keep; the *content* (genre, setting, plot engines, style rules) is what you write.

This file provides guidance to Claude Code when working with code in this niche.

## What this niche is

`<YOUR NICHE NAME>` is one **niche** in a multi-niche content assembly line. It turns
story ideas into finished YouTube-narration assets: full narration scripts → SRT +
TTS-ready line files → a character sheet + one image prompt per line. There is no
build/lint/test suite; the only executable code is the shared Python image pipeline
(`tools/glabs`, at the repo root). Everything else is Markdown "brains" that Claude
executes.

- **Genre / channel:** TODO — one sentence describing the channel (e.g. "short moral
  tales", "true-crime retellings", "cozy romance"). Do NOT copy someone else's genre.
- **Language:** TODO (e.g. English). English niches MUST use `--normalize` when
  cutting; non-English niches must NOT.
- **Image mode:** TODO — **multi-image** (one image per SRT line, feeds `tools/glabs`)
  or **single-image** (one static image for the whole video, no SRT/no `_scenes.txt`).
- **Output prefix:** TODO — the filename prefix for episodes (e.g. `ep`), so scripts
  land at `output/<prefix>-NN-<slug>.txt`.

**Shared vs. niche-specific.** The cut → SRT/TTS → image-prompt tooling is
niche-agnostic and lives at the repo root under `.claude/` (`srt-cut.py`,
`srt-to-image-prompts/`, `/cut-and-prompt`, `/generate-media`). This folder holds only
*this* niche's brain: the writer skill, its `/write-batch` and `/ideas-from-channel`
commands, and its `knowledge/`/`inbox/`/`output/`.

## The pipeline (commands)

```
/ideas-from-channel [N|url]  → inbox/briefs.md   (mine a reference channel → fresh de-duped briefs)
/write-batch <N>             → output/<prefix>-NN-*.txt   (generate N ideas, then write them)
/write-batch [briefs-file]   → output/<prefix>-NN-*.txt   (write one script per existing brief)
/cut-and-prompt <script.txt> [--normalize]  → SRT + TTS + character/scene prompts (root command)
```

- `/write-batch <N>` runs the ideator flow (see `.claude/agents/ideator.md`), records
  briefs to `inbox/briefs.md`, runs the uniqueness gate, writes one script per brief
  via a fresh `writer` sub-agent, and appends each written story's core situation to
  `knowledge/used-scenarios.txt`.
- `/write-batch [briefs-file]` writes one script per existing brief in the file.
- **Run `/cut-and-prompt` with `--normalize` only for English niches.**

## Three-layer architecture

The design deliberately separates three concerns (see `README.md`):

- **Skill = quality.** `skills/writer/SKILL.md` holds the invariant writing formula —
  the rules that never change per run.
- **Clean-context sub-agent = consistency at scale.** Each script runs in its own fresh
  sub-agent so the 10th script is written under the same clean conditions as the 1st.
  `.claude/agents/writer.md` is the writer sub-agent.
- **Command orchestrator = the loop.** `.claude/commands/*.md` drive the batch, keep
  records, and enforce the gates. The orchestrator writes no prose itself.

## Where the "brains" live

- `skills/writer/SKILL.md` — TODO: your writing formula (plot engines, structure,
  style rules, self-check).
- `.claude/agents/writer.md` — the writer sub-agent (one script per invocation).
- `.claude/agents/ideator.md` — the analysis+ideation sub-agent used by `/write-batch <N>`.
- `knowledge/` — reference competitor scripts + channel screenshots (the tone + virality
  anchor). TODO: drop your own reference material here.
- `knowledge/used-scenarios.txt` — the anti-repeat ledger (one line per core situation
  already produced).
- `inbox/briefs.md` — the input queue (STORY BRIEFs separated by `---`).
- `output/` — deliverables plus `_batch-log.md` (the run log).

## Invariants (violating these breaks the pipeline)

- **1:1 count contract, end to end** (multi-image niches). One brief → one script; SRT
  block count **must equal** TTS line count **must equal** scene-prompt count. Photos
  and audio align **by order/index**, so any count mismatch desyncs the video.
- **`used-scenarios.txt` is the originality ledger.** It is only appended to by
  `/write-batch` when a script is actually written — idea generation deliberately does
  *not* touch it (discarded ideas must not pollute the taken-list). Both flows run a
  uniqueness gate against it.
- **Character-sheet lines lead with the `@tag`, not the character's name** (e.g.
  `1. @mia (...)`), so a generated reference image files under its tag. Scene prompts
  reuse that same `@tag`.
- **Language split.** Narration/TTS lines stay in the script's language; image prompts
  are always written in **English**.
- **Image safety is built into prompt generation.** See the root skill
  `.claude/skills/srt-to-image-prompts/references/minor-and-policy-safety.md`.
- **Originality over cloning.** Mine reference channels for *premises/engines* only,
  then reshape specifics into new stories — never beat-for-beat copies (YouTube
  reused-content compliance).

## Human-review reality

Automation replicates good and bad alike. Always spot-read the first 2–3 scripts of any
batch before trusting the rest.
