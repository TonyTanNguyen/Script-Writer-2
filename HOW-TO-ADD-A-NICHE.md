# How to add a niche

A **niche** is one channel's "brain": its writing formula, its idea generator, and the
batch loop that runs them. This kit ships a blank skeleton (`example-niche/`) that you
copy once per channel and fill in. This guide shows both ways to do it.

If you already have a **master prompt** for your niche (a big blob describing the genre,
structure, and rules), the whole job is just distributing that prompt into the right
files. The skeleton's `TODO` placeholders are where each part goes.

---

## Step 0 — copy the skeleton

From the repo root:

```bash
cp -R example-niche my-niche
```

Use a short, filename-safe name (`my-niche`, `true-crime`, `cozy-romance`, …).

---

## The fast way (let Claude Code do it)

Open the repo in Claude Code and say:

> Here's my master prompt for a niche. Turn `my-niche/` into a working brain from it:
> fill in `my-niche/CLAUDE.md`, `my-niche/skills/writer/SKILL.md`, and the ideator +
> writer agents, and keep the brief fields identical across all of them. Then paste
> your master prompt.

Claude distributes the prompt into the right files. This is the intended workflow — the
skeleton exists so a master prompt has a clean home. Skip to **Run it** below.

---

## The manual way (what actually needs to happen)

A master prompt is usually one big blob. In the kit it gets split across the three
layers. Search each file for `TODO` and fill it in.

| Part of your master prompt | Goes into |
|---|---|
| Genre, language, single- vs multi-image, filename prefix | `my-niche/CLAUDE.md` (top TODOs) |
| **The writing formula** — plot engines, structure/beats, style rules, hook/CTA, self-check | `my-niche/skills/writer/SKILL.md` ← *most of the master prompt lands here* |
| The brief fields (what a story idea must specify) | keep **identical** in the writer skill, both agents, and both commands |
| How ideas are generated / reference channel | `my-niche/.claude/agents/ideator.md` + `.claude/commands/ideas-from-channel.md` |
| Reference scripts + channel screenshots | drop files into `my-niche/knowledge/` |

Leave `inbox/briefs.md` and `knowledge/used-scenarios.txt` empty — the pipeline fills
them.

### Fill-in checklist

- [ ] `CLAUDE.md` — niche name, genre, language, image mode, output prefix.
- [ ] `skills/writer/SKILL.md` — **the formula.** Plot engines, structure, style, self-check.
- [ ] `.claude/agents/writer.md` — update the brief fields to match your SKILL.
- [ ] `.claude/agents/ideator.md` — your reference-analysis rules + the brief shape it emits.
- [ ] `.claude/commands/write-batch.md` — set the output prefix (the loop is reusable as-is).
- [ ] `.claude/commands/ideas-from-channel.md` — set your default reference channel.
- [ ] `knowledge/` — add reference scripts + channel screenshots.

---

## The one gotcha: brief fields must match everywhere

A **brief** is the little spec for one story that the ideator produces and the writer
consumes. Its field names must be spelled **identically** in all of these:

- `skills/writer/SKILL.md`
- `.claude/agents/writer.md`
- `.claude/agents/ideator.md`
- `.claude/commands/write-batch.md`
- `.claude/commands/ideas-from-channel.md`

Example: if a story needs `TITLE / SETTING / TWIST / MORAL`, every file above must use
those same field names. If the ideator emits a field the writer doesn't expect (or vice
versa), the writer gets a brief it can't read. The fast way handles this automatically;
if you do it by hand, double-check this.

---

## Run it

From inside your niche folder:

```
cd my-niche
/write-batch 3                                  # generate 3 ideas and write them
/cut-and-prompt output/<file>.txt --normalize   # add --normalize for ENGLISH scripts only
/generate-media <episode-basename>              # multi-image niches only
```

- **`--normalize`** is for English scripts only — it makes the text TTS-read-ready
  before cutting. Non-English niches must omit it.
- **`/generate-media`** applies only to **multi-image** niches (those that produce a
  `_scenes.txt`). Single-image niches skip it. It needs the local G-Labs API running and
  your key in `.glabs.json` (copy `.glabs.example.json` and add your key).

---

## Sanity check before a big batch

1. Run `/write-batch 1` first and read the single script end-to-end.
2. Confirm the brief the ideator produced has the exact fields the writer expected.
3. For multi-image niches, run `/generate-media <ep> --dry-run` (zero quota) to confirm
   the character/scene prompts parse before spending any generation quota.

Once one clean episode runs end to end, scale up the batch size.
