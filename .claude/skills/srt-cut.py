#!/usr/bin/env python3
"""
srt-cut.py — faithful Python port of the chunker in skills/srt-cleaner.html
(dual mode: "Script -> SRT + Text"), so the cut can be run programmatically
instead of pasting into the HTML tool.

Given a plain prose script, it writes TWO index-matched files:
  <name>.srt        — subtitle blocks (30-40 words by default) with estimated
                      timestamps. Feed this to the srt-to-image-prompts skill.
  <name>_tts.txt    — the SAME blocks, one per line, plain text only (no numbers,
                      no timestamps). Feed this to your TTS (splits by linebreak):
                      block N in the SRT == line N here == prompt N later.

Defaults mirror the HTML tool exactly:
  min=30, max=40, overflow=4, clause-split ON, ms-per-char=60, gap=150ms.

Usage:
  python3 srt-cut.py <input.txt>
  python3 srt-cut.py output/ep-01-sample.txt --out-dir output
  python3 srt-cut.py in.txt --name my-story --min 30 --max 40 --mpc 60 --gap 150
  python3 srt-cut.py in.txt --no-clause        # split by words, not clauses
"""

import argparse
import os
import sys

# Matches CLAUSE_PUNCT in srt-cleaner.html (Latin + CJK sentence punctuation).
CLAUSE_PUNCT = ".!?…;。！？；"


def count_words(t):
    t = t.strip()
    return len(t.split()) if t else 0


def split_clauses(text):
    """Port of splitClauses(): break on clause punctuation, keep the punctuation."""
    parts, buf = [], ""
    for ch in text:
        buf += ch
        if ch in CLAUSE_PUNCT:
            if buf.strip():
                parts.append(buf.strip())
            buf = ""
    if buf.strip():
        parts.append(buf.strip())
    return [p for p in parts if p]


def do_split(text, min_w, max_w, ovfl, by_clause):
    """Port of doSplit(): greedily pack clause/word units into min..max-word chunks."""
    import re
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    all_units = []
    for para in paras:
        units = split_clauses(para) if by_clause else para.split()
        all_units.extend(units)

    chunks, cur, cw = [], [], 0
    for u in all_units:
        uw = count_words(u)
        if cw == 0:
            cur.append(u)
            cw += uw
        elif cw < min_w:
            cur.append(u)
            cw += uw
            if cw >= max_w:
                chunks.append(" ".join(cur).strip())
                cur, cw = [], 0
        else:
            if cw + uw <= max_w:
                cur.append(u)
                cw += uw
                if cw >= max_w:
                    chunks.append(" ".join(cur).strip())
                    cur, cw = [], 0
            elif cw + uw <= max_w + ovfl:
                cur.append(u)
                cw += uw
                chunks.append(" ".join(cur).strip())
                cur, cw = [], 0
            else:
                chunks.append(" ".join(cur).strip())
                cur, cw = [u], uw

    if cur:
        joined = " ".join(cur).strip()
        if cw < min_w and chunks:
            last = chunks[-1]
            if count_words(last) + cw <= max_w + ovfl:
                chunks[-1] = last + " " + joined
            else:
                chunks.append(joined)
        else:
            chunks.append(joined)

    return [c for c in chunks if c.strip()]


def fmt_time(ms):
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    cs = ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{cs:03d}"


def make_srt(lines, mpc, gap):
    """Port of makeSRT(): estimate a duration per block and lay out timestamps."""
    ms_per_word = max(int(mpc * 5.83), 50)
    floor_ms = max(int(mpc * 13), 200)
    out, t, idx = [], 0, 1
    for line in lines:
        if not line.strip():
            continue
        dur = max(len(line) * mpc, len(line.split()) * ms_per_word, floor_ms)
        out.append(f"{idx}\n{fmt_time(t)} --> {fmt_time(t + dur)}\n{line}\n")
        t += dur + gap
        idx += 1
    return "\n".join(out).strip()


def main():
    ap = argparse.ArgumentParser(description="Cut a prose script into an SRT + a TTS line-file.")
    ap.add_argument("input", help="path to the prose script (.txt)")
    ap.add_argument("--out-dir", default=None, help="output directory (default: input's dir)")
    ap.add_argument("--name", default=None, help="output base name (default: input filename stem)")
    ap.add_argument("--min", type=int, default=30, dest="min_w", help="min words per block (default 30)")
    ap.add_argument("--max", type=int, default=40, dest="max_w", help="max words per block (default 40)")
    ap.add_argument("--ovfl", type=int, default=4, help="overflow tolerance in words (default 4)")
    ap.add_argument("--mpc", type=int, default=60, help="ms per character for timing (default 60)")
    ap.add_argument("--gap", type=int, default=150, help="gap in ms between blocks (default 150)")
    ap.add_argument("--no-clause", action="store_true", help="split by words instead of clauses")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        sys.exit(f"error: input not found: {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    max_w = max(args.max_w, args.min_w)
    lines = do_split(text, args.min_w, max_w, args.ovfl, not args.no_clause)
    lines = [l for l in lines if l.strip()]
    if not lines:
        sys.exit("error: no text to cut (input empty after parsing)")

    srt = make_srt(lines, args.mpc, args.gap)
    tts = "\n".join(lines)

    out_dir = args.out_dir or os.path.dirname(os.path.abspath(args.input))
    name = args.name or os.path.splitext(os.path.basename(args.input))[0]
    os.makedirs(out_dir, exist_ok=True)
    srt_path = os.path.join(out_dir, f"{name}.srt")
    tts_path = os.path.join(out_dir, f"{name}_tts.txt")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt + "\n")
    with open(tts_path, "w", encoding="utf-8") as f:
        f.write(tts + "\n")

    wc = count_words(text)
    print(f"blocks: {len(lines)}  (from {wc} words)")
    print(f"SRT:    {srt_path}")
    print(f"TTS:    {tts_path}")


if __name__ == "__main__":
    main()
