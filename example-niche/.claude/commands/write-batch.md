---
description: Orchestrate a batch. Give a NUMBER to auto-generate that many ideas from knowledge/ and write them; give a briefs FILE (or none) to write from existing briefs. One clean writer sub-agent per script.
---

You are the batch ORCHESTRATOR. You do NOT write any story prose or thumbnail prompts
yourself. Your job is to dispatch work, gate for uniqueness, and keep records.

> TODO: set your output prefix. Scripts are written to `output/<prefix>-NN-<slug>.txt`.

**Choose the flow from the argument:**
- The argument is a **number** `N` (e.g. `/write-batch 5`) → **IDEATOR FLOW** (generate
  N ideas from `knowledge/`, then write them).
- The argument is a **file path**, or there is **no argument but `inbox/briefs.md`
  already holds briefs** → **BRIEFS FLOW** (write from those briefs).

---

## IDEATOR FLOW (`/write-batch <N>`)

1. **Dispatch the `ideator` sub-agent** (fresh context): "N = <N>. Analyze `knowledge/`
   and return <N> idea bundles per your instructions." It returns N bundles, each with a
   `--- BRIEF ---`, an English `--- THUMBNAIL ---` prompt, and a `--- VIRAL RATIONALE ---`.
2. **Parse the bundles** into N triples `{brief, thumbnail_prompt, viral_rationale}` by
   splitting on `=== IDEA n ===` and the `--- … ---` markers.
3. **Record the briefs** to `inbox/briefs.md`: write the N briefs separated by a line of
   `---`, keeping the file's header comment lines at the top, replacing any spent briefs.
4. **Uniqueness gate — run BEFORE writing anything.** Read `knowledge/used-scenarios.txt`.
   For each brief, distill its CORE SITUATION into one line (engine + who-does-what +
   central mechanic) and compare against **(a)** every line in `used-scenarios.txt` and
   **(b)** the other briefs this run. A COLLISION is a substantial overlap of the central
   mechanic (same engine AND same core act/scheme) — not merely a shared engine or
   setting. Because this flow is automated, **do not stop to ask**: for each collision,
   **re-dispatch `ideator` for one replacement idea** ("give 1 new idea, avoid these core
   situations: <list>"), re-screen it, repeat (cap 3 rounds per slot; if still colliding,
   drop the slot and note it).
5. For EACH surviving brief, in turn:
   - Spawn ONE `writer` sub-agent (fresh context). Give it: the single brief text, the
     target word count, and the output path `output/<prefix>-NN-<short-slug>.txt`.
   - Wait for its one-line report (path + word count).
   - **Save the paired thumbnail prompt** to `output/<prefix>-NN-<short-slug>_thumbnail.txt`.
   - Append that brief's core situation as a new line to `knowledge/used-scenarios.txt`.
   - Log the result to `output/_batch-log.md`.
   Run sequentially by default so context stays clean and files don't collide.
6. **Summary table:** number · file · word count · status · **viral rationale**. List any
   ideas reshaped or dropped at the gate. Next step: `/cut-and-prompt output/<prefix>-NN-<slug>.txt`
   (add `--normalize` for English niches).

---

## BRIEFS FLOW (`/write-batch [briefs-file]`)

Input: a briefs file (default `inbox/briefs.md`) with several STORY BRIEFs separated by
a line of `---`. If the user named a different file, use that.

1. Read the briefs file and split it into individual briefs. Number them 01, 02, 03, …
2. Read `knowledge/used-scenarios.txt` so you know what is already taken.
3. **Uniqueness gate — run BEFORE writing anything.** For each brief, distill its CORE
   SITUATION into one line. Compare against **(a)** every existing line in
   `used-scenarios.txt` AND **(b)** the other briefs in this batch. A brief COLLIDES only
   when the central mechanic substantially overlaps. **If any collisions are found, STOP
   and do not write those briefs.** Print a short table and ask the user how to handle
   each — **skip**, **revise**, or **proceed anyway**. Only unique or cleared briefs move on.
4. For EACH brief that passed: spawn ONE `writer` sub-agent (fresh context) with the
   single brief, the target word count, and output path
   `output/<prefix>-NN-<short-slug>.txt`; wait for its one-line report; append the core
   situation to `knowledge/used-scenarios.txt`; log to `output/_batch-log.md`. Sequential
   by default.
5. Print a short summary table: number, file, word count, status. Include briefs
   skipped/revised at the gate.

---

Never skip the `used-scenarios.txt` update — that is what keeps a long run from drifting
into repeats.
