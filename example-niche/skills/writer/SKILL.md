---
name: writer
description: TODO — Write one complete <GENRE> narration script for the <YOUR CHANNEL> YouTube channel. Use this whenever the task is to turn a STORY BRIEF into a full single-voice narration script, or when writing/expanding beats of such a story. This skill defines the channel formula, style rules, and the file-writing workflow. Do NOT use it for other genres or for titles/thumbnails alone.
---

# Writer — <YOUR CHANNEL>

> **This is a template.** The *workflow* (the core loop, the TTS rules, the self-check
> shape) is reusable. The *formula* (genre, plot engines, structure, style, setting) is
> yours to write — replace every `TODO`/`<…>`. A rich, specific formula here is what
> makes your channel distinct and hard to copy.

Write ONE complete `<GENRE>` narration script from a STORY BRIEF, saving it
beat-by-beat to a target `.txt` file so length never breaks quality.

## How to run (the core loop)

You are given: a STORY BRIEF (or an idea to expand into one), a target word count
(default `<TODO e.g. 8,000>` words), and an OUTPUT FILE PATH.

1. **Plan silently first.** Before writing a word, decide and hold for the whole script:
   TODO — list the elements your genre must keep consistent (e.g. character names,
   setting, the central conflict, any twist/reveal, the ending). Write this plan to the
   TOP of the output file inside an HTML comment `<!-- PLAN: ... -->` so it stays
   consistent and is easy to strip later. This block is the only non-narration text
   allowed in the file.
2. **Write the story to the file in passes of ~2000 words each**, appending as you go.
   After each pass, re-read the tail of the file so the next pass continues seamlessly.
   Do NOT stop to ask for permission between passes — drive the whole script yourself.
3. **After finish, run the self-check** (below) against the file and fix any misses.
4. **Strip the `<!-- PLAN -->` comment** so the final file is clean narration only.

Never pad. If a beat runs short of its word budget, add real scene detail (dialogue,
sensory texture), not filler.

## Structure — TODO

Define your channel's fixed structure. Example shape (replace entirely):

- **HOOK + CTA (~120w):** open with a curiosity teaser that compresses the premise
  WITHOUT spoiling any reveal. Then a subscribe/notification CTA — **rewrite it every
  time; never reuse the same wording.**
- **BEATS:** TODO — your fixed beat structure (e.g. a 10-beat arc). List each beat and
  what it must accomplish.
- **MORAL / PAYOFF + CTA (~250w):** TODO — the closing address, the takeaway, one
  opinion question, and the full CTA (comment, subscribe, bell, like, share).
- **DISCLAIMER:** TODO — any verbatim disclaimer your channel uses (e.g. fictional
  dramatization).

## Plot engines — TODO

List the recurring premise engines your channel rotates through, so every script has a
spine but no two feel the same. Example (replace):

1. `<Engine A — short name + one-line description>`
2. `<Engine B — …>`
3. `<Engine C — …>`

Rotate engines across a batch; never run the same engine twice in a row unnoticed.

## TTS OUTPUT RULES (READ-READY) — reusable, keep these

The final story is narration fed directly into a text-to-speech engine. It must be
clean, plain, "read-ready" text:

- Plain text ONLY. No markdown, no bold, no headers, no scene labels, no bracketed
  stage directions.
- Write numbers and money the way they should be SPOKEN ("four thousand two hundred
  seventeen dollars and eighty-three cents", "ten forty-seven in the morning").
- Expand abbreviations and initialisms into spoken form ("Mister", "Doctor").
- Use natural sentence-level punctuation for pacing; split long sentences so the voice
  doesn't run on.
- Write "percent", "and", "dollars" instead of %, &, $.
- No emojis, no parentheticals, no footnotes. One continuous, flowing narration.
- Write brand/foreign names as they'd naturally be spoken in the target accent.

(The shared `english-tts-normalization` skill can also normalize a finished English
script — but writing read-ready in the first place is cleaner.)

## Style rules (hard — never break) — TODO

Replace with your channel's voice. Example categories to fill in:

- **Reading level:** TODO (e.g. simple English, short sentences for non-native listeners).
- **Dialogue ratio:** TODO (e.g. 40–50% spoken lines, simple speech tags only).
- **Emotional register:** TODO (how much melodrama, which beats to repeat for emphasis).
- **Setting texture:** TODO (the concrete daily-life details that ground your world).
- **Specificity:** prefer precise odd numbers and exact times to create a "sense of
  truth" — TODO adapt to your genre.
- **Age / safety:** TODO — e.g. no named character under 18; children may exist but stay
  unnamed and are never the focus of conflict. Keep this aligned with the image-safety
  rules in the root `srt-to-image-prompts` skill.
- **NO TEMPLATE FEEL:** do not reuse the same hooks, emotional beats, or reveal mechanics
  across stories. Middle acts must never be swappable with a previous script unnoticed.
- **Anti-repeat:** rotate through your palette of distinctive signals; track what the
  previous script used and avoid repeating the same combination.

## Self-check (run against the file before finishing)

TODO — adapt this list to your formula. Example:

Consistent names/details throughout · reading level held · dialogue ratio met · opening
has hook + subscribe CTA · structure beats all present · any reveal lands as designed ·
closing payoff + opinion question + full CTA · file is clean plain text with the PLAN
comment removed · total length within ±5% of target.

List any misses briefly, fix them in the file, then report done with the final word count.

## Language

All narration output is in `<TODO: language>`. Notes back to the operator may be in any
language you prefer.
