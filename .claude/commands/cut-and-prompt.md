---
description: One script → (optional TTS normalization) → SRT + TTS-script + image prompts. Cuts a finished prose script with the shared srt-cut.py, then a subagent runs the srt-to-image-prompts skill on the SRT. Niche-agnostic — works in any niche folder. Pass --normalize for English scripts to make the TTS read-ready first.
---

You are the pipeline ORCHESTRATOR for one finished script. You do NOT write prose or prompts yourself — you (optionally) normalize, run the cutter, dispatch the prompt subagent, then verify and report.

This command and its tools are installed globally under `~/.claude/`, so it works from any niche's working directory. Outputs always land next to the input script (in that niche's folder), never in `~/.claude`.

**Input:** the path to a finished prose script, given after the command (e.g. `/cut-and-prompt output/ep-01-sample.txt`). If none is given, ask which script — do not guess.

**Flag — `--normalize`** (a.k.a. `--tts-normalize`): if present anywhere in the arguments, run the English TTS normalization step (Step 2) before cutting. **Default: OFF.** Only pass it for **English** scripts — the normalization skill is American-English and would corrupt a non-English (e.g. Vietnamese) script. When off, the cutter runs on the original prose exactly as before.

Do this in order:

1. **Resolve paths.** Let `SCRIPT` = the input path (strip the `--normalize`/`--tts-normalize` flag out of it first). Let `NAME` = the input filename without extension. Outputs go in the same directory as `SCRIPT`. Note whether `--normalize` was passed.

2. **(Only if `--normalize`) Normalize the script for TTS.** Spawn ONE `general-purpose` subagent (fresh context) with this task (fill in the real paths):

   > Follow a skill exactly to normalize an English script into read-ready plain text for a text-to-speech engine. This is a plain text file (not source code), so use the Read tool directly; no code search is needed (mcp__codesift__search_text exists but is irrelevant here).
   >
   > - Skill: `/Users/tannguyen/.claude/skills/english-tts-normalization/SKILL.md`. Read it fully, then apply ALL of its rules across the WHOLE script.
   > - Input script (read this): `<abs path to SCRIPT>`
   > - Output (write this): `<abs path to NAME_normalized.txt>` in the SAME directory as the input.
   > - Do exactly what the skill says: convert numbers to words, expand abbreviations, space out initialisms, respell tricky names/heteronyms, turn symbols into words, strip all non-speech formatting/markdown, and split long sentences for natural pacing — WITHOUT changing the meaning, wording order, tone, or removing/adding any content. Keep paragraph breaks (one blank line between paragraphs). Output plain text only — no markdown, no notes, no list of changes.
   > - Reply with ONE short line: the output path, the word count, and flag anything unusual (heavy number/abbreviation load, foreign words respelled, or nothing needed).

   Let `CUTSRC` = `NAME_normalized.txt`. (If `--normalize` was NOT passed, `CUTSRC` = `SCRIPT`.)

3. **Cut the script.** Run (note `--name "NAME"` forces clean output names even when cutting the `_normalized` intermediate):
   ```
   python3 ~/.claude/skills/srt-cut.py "CUTSRC" --name "NAME"
   ```
   A faithful port of `~/.claude/skills/srt-cleaner.html` at its default settings (min 30 / max 40 words, clause-split, mpc 60, gap 150). It writes two index-matched files next to the script:
   - `NAME.srt` — numbered blocks with estimated timestamps (drives the image prompts).
   - `NAME_tts.txt` — the same blocks, one clean spoken line each, for the user's TTS (splits by linebreak). When `--normalize` ran, these lines are already read-ready.
   Read the command's stdout for the block count. If it errors or produces 0 blocks, stop and report.

4. **Confirm the two cut files match** before the prompt step: SRT block count must equal TTS line count.
   ```
   echo "SRT: $(grep -cE '^[0-9]+$' NAME.srt)  TTS: $(wc -l < NAME_tts.txt)"
   ```
   They must be equal. If not, stop and report.

5. **Generate the prompts.** Spawn ONE `general-purpose` subagent (fresh context) with this task (fill in the real paths):

   > Execute this task by following a skill exactly. These are plain markdown/text files (not source code), so use the Read tool directly; no code search is needed (mcp__codesift__search_text exists but is irrelevant here).
   >
   > - Skill path: `/Users/tannguyen/.claude/skills/srt-to-image-prompts/SKILL.md`. FIRST read SKILL.md and ALL of its reference files in its `references/` folder, then follow its workflow exactly (internal JSON scene-layout map first, then the character sheet, then one scene prompt per SRT block).
   > - Input SRT (authoritative for block boundaries and count — exactly one prompt per block, in order): `<abs path to NAME.srt>`
   > - Source story for cross-referencing (the full prose the SRT was cut from; use it for characters, locations, wardrobe, blocking — but the SRT's block count is authoritative): `<abs path to SCRIPT>`
   > - Save two files to the SAME directory as the SRT: `NAME_characters.txt` and `NAME_scenes.txt`.
   > - Requirements: the scenes file has EXACTLY as many numbered prompts as the SRT has blocks (verify before finishing); each character-sheet line LEADS WITH the `@tag` (not the name); each `@tag` used at most once per prompt; no dialogue/quotes; concrete self-contained settings; visible emotion on every character; a scene-appropriate lighting clause + the locked style string on every prompt.
   > - Reply with ONE short paragraph: the two output paths, SRT block count vs. number of prompts (confirm equal), how many characters on the sheet, and flag any hard blocks or safety rewrites.

6. **Verify and report.** Confirm the scenes file's prompt count equals the SRT block count:
   ```
   echo "blocks: $(grep -cE '^[0-9]+$' NAME.srt)  prompts: $(grep -cE '^[0-9]+\. ' NAME_scenes.txt)"
   ```
   Then print a short summary listing the deliverables (`NAME.srt`, `NAME_tts.txt`, `NAME_characters.txt`, `NAME_scenes.txt`, plus `NAME_normalized.txt` if `--normalize` ran), the block/line/prompt count (all equal), the character count, and anything the subagent flagged. Remind the user: block N ↔ TTS line N ↔ prompt N, so photos and audio line up by order.

Never skip the count checks in steps 4 and 6 — the whole pipeline depends on the SRT, TTS, and prompts staying 1:1:1.
