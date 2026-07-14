# example-niche — a blank channel brain

This folder is a **skeleton**. Copy it once per channel and fill in the blanks:

```bash
cp -R example-niche my-channel
```

Everything here works *except* the parts that are your creative secret sauce — those
are left as `TODO`. Filling them in is the whole job.

## The three layers (why it's built this way)

A niche brain separates three concerns so quality stays constant across a long batch:

1. **Skill = quality.** `skills/writer/SKILL.md` is the invariant formula: genre, plot
   engines, structure, style rules, self-check. It never changes per run. **This is the
   file that makes your channel yours — write it carefully.**
2. **Sub-agent = consistency at scale.** `.claude/agents/writer.md` runs one script in a
   fresh context, so script #10 is written under the same clean conditions as script #1
   (no drift from a filling context window).
3. **Command = the loop.** `.claude/commands/write-batch.md` dispatches the sub-agents,
   runs the uniqueness gate, and records results. It writes no prose itself.

## Fill-in checklist

Work through these in order. Search for `TODO` in each file.

- [ ] `CLAUDE.md` — set niche name, genre, language, image mode, output prefix.
- [ ] `skills/writer/SKILL.md` — **the formula.** Define your plot engines, structure,
      style rules, and self-check. This is the bulk of the work.
- [ ] `.claude/agents/writer.md` — usually only needs the brief fields updated to match
      your SKILL.
- [ ] `.claude/agents/ideator.md` — set your reference-analysis rules and the brief
      shape the ideator emits.
- [ ] `.claude/commands/write-batch.md` — set the output prefix; the orchestration logic
      is reusable as-is.
- [ ] `.claude/commands/ideas-from-channel.md` — set your default reference channel.
- [ ] `knowledge/` — drop in reference scripts + channel screenshots (see its README).
- [ ] `inbox/briefs.md` — leave empty; the ideator fills it.
- [ ] `knowledge/used-scenarios.txt` — leave empty; `/write-batch` appends to it.

## Then run it

From inside `my-channel/`:

```
/write-batch 5                      # generate 5 ideas and write them
/cut-and-prompt output/<file>.txt   # add --normalize for English scripts
/generate-media <episode-basename>  # multi-image niches only
```
