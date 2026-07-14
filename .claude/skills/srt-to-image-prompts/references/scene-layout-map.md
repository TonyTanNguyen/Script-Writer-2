# Internal JSON Scene-Layout Map (planning step — NOT a delivered file)

Before generating any character sheet or scene prompt, build a **JSON scene-layout map** for the whole script. This is a **planning artifact you keep for your own use** — it is NOT saved and NOT presented to the user. The only files you deliver are `<name>_characters.txt` and `<name>_scenes.txt`. The JSON is the structured source-of-truth that those two files are derived from.

## Why this step exists

A long SRT (often 100–400 blocks) drifts badly if you generate prompts blindly from top to bottom: a character's clothing changes mid-scene, the lighting says "bright daylight" three blocks after a night scene started, a character who left the room is still in frame, someone present gets dropped, or the wrong person is shown performing the action. The JSON map fixes the **scene-level facts once** — location, time/weather, who is present, where they stand, what each person wears, who performs the main action, the emotional tone — so that every block inside that scene inherits the same locked context. You build the map, then read its locked facts and write all the blocks against them. This is what makes the output internally consistent.

The JSON is more disciplined than free prose: every scene must explicitly answer *who is in frame*, *who is only mentioned*, *who leads the action*, and *what each person wears and where they stand*. Forcing those fields to be filled is what catches drift before it reaches a prompt.

## How to build it — cross-reference the story AND the SRT

The SRT was generated from a story (the most recent full story written in this conversation, if there is one; otherwise the SRT itself is the only source). Work line by line:

- Identify which story event each SRT block corresponds to, who is present, and where it takes place.
- Every character name, location, scene, and action in the JSON must be traceable to a specific part of the story/SRT. Do not rely on memory or invention — if a detail is not in the source, do not add it.
- All characters must match the source: correct name, appearance, age, role. Do not invent or omit anyone.
- **Scene boundaries follow the story's logic:** a change in location OR a change in time anchor = a new scene. Scenes group blocks; they never split a block. Every block belongs to exactly one scene, and the scenes in order cover the entire SRT with no gaps and no overlaps.

## JSON structure (all English, even if the SRT is another language)

```json
{
  "language": "Vietnamese | English",
  "storyContext": "4–5 sentence summary: plot + setting + time anchors + emotional theme",
  "mainSetting": "primary location of the story",
  "storyType": "character_driven | action | romance | thriller | horror | philosophical | mixed",

  "characters": [
    {
      "name": "character name exactly as used in the story (full name)",
      "role": "4–6 word role description",
      "firstAppearanceLine": 1,
      "tag": "@firstname (lowercase, derived per character-formula.md)",
      "suggestedDescription": "Fixed full visual description in English, used to build this character's sheet entry. Mandatory order: [ethnicity + nationality][gender], [exact age at first appearance], [build], [skin tone], [hair: color + texture + length + style], [eyes: color + quality], [face: stubble / glasses / makeup if applicable], wearing [reference top garment: color + fabric + cut]. Must END with the lower garment + footwear, e.g. 'with charcoal wool trousers and polished black oxford shoes' — the sheet is a full-body image, so footwear is mandatory and the character is never barefoot unless the script explicitly calls for it."
    }
  ],

  "sceneMap": [
    {
      "startLine": 1,
      "endLine": 16,
      "location": "CONCRETE physical description of this scene's space + key objects + layout — NOT a bare label. This exact description is folded into every block's `located in …`.",
      "timeOfDay": "time of day + year/anchor if known, e.g. 'early morning, present day 2024' | '11:47 pm, year 1991' | 'flashback 20 years ago, late afternoon'",
      "lighting": "context-accurate lighting clause for image generation (from camera-and-style.md pool), e.g. 'amber streetlight glow, deep shadows' | 'soft natural morning light through window' — never generic, must agree with timeOfDay",
      "sceneSummary": "one sentence describing the dramatic action of this scene",
      "charactersPresent": ["Full Name 1", "Full Name 2"],
      "characterPositions": {
        "Full Name 1": "position + posture, e.g. standing in the center of the room, arms crossed",
        "Full Name 2": "position + posture"
      },
      "sceneOutfits": {
        "Full Name 1": "wearing [color][fabric][garment] with [detail] — appropriate for this scene's time and context (wardrobe-by-act)",
        "Full Name 2": "wearing ..."
      },
      "characterAges": {
        "Full Name 1": "FILL ONLY when this scene's time anchor differs from the character's firstAppearanceLine. Format: [ethnicity][gender], [N] years old, [build], [skin], [hair], [eyes], [face] — NO 'wearing', NO parentheses"
      },
      "leadSubject": "name of the character performing the MAIN action across these blocks — cross-reference each line, do not default to the protagonist",
      "inFrame": ["characters physically present in frame, including anyone visible through a doorway from an adjacent room"],
      "mentioned": ["characters referenced in dialogue only — NOT physically present in this scene"],
      "dramaticRelationship": "power dynamic and tension between characters in this scene",
      "crowdNotes": "background crowd description if the story calls for it, e.g. 'commuters moving through the station' | none"
    }
  ]
}
```

## Field rules

- **`suggestedDescription`** is the canonical look for that character. It feeds the character sheet (Step 2) and must be complete English with every physical detail, ending with the top garment `wearing [reference garment]` then the lower garment + footwear (the sheet is full-body, so shoes are mandatory). Lock items 1–7 (ethnicity, age, build, skin, hair, eyes+quality, face) for the entire video; only the garment/footwear changes per scene.
- **`location`** is a *concrete description* (the space + its key objects), never a bare proper-noun label — the image tool has no memory and cannot resolve a name. Reuse the **same concrete features** for any later scene set in the same place.
- **`timeOfDay` drives `lighting`.** Decide the lighting clause once per scene (from `camera-and-style.md`) and apply it to every block in the scene. This is the single biggest source of drift if left per-block. Night = streetlight/candlelight/darkness; indoor daytime = natural window light. Never a bright-daylight clause on a night/evening/stormy scene.
- **`charactersPresent` / `inFrame` is the cast contract.** Every character listed must appear — as their `@tag` + that scene's outfit, tag used once — in each block where the text shows them on screen. If a block only shows a subset, use that subset, but never introduce someone not in `charactersPresent`. `inFrame` is the literal-in-frame subset (use it when it differs from the broader present cast, e.g. someone glimpsed through a doorway).
- **`mentioned`** lists characters named in dialogue but NOT physically present — they must never be drawn in that scene's prompts.
- **`sceneOutfits`** records each present character's garment for this scene (their act). It is the only part of a character's description allowed to change between scenes; everything else stays identical to the sheet.
- **`characterAges`** is filled ONLY when a scene sits at a different time anchor than the character's first appearance (flashbacks, time jumps). A character who is 20 in 1995 must be 50 in a 2025 scene. Leave it empty for present-anchor scenes.
- **`leadSubject`** names who performs the main action across the block range — read the lines, do not default to the protagonist. This becomes the primary subject of those prompts.
- **`dramaticRelationship`** captures the power dynamic/tension so the per-character emotions in prompts stay consistent with the scene.

## How the JSON feeds the rest of the workflow

1. **Character sheet (Step 2):** build one sheet line per entry in `characters[]`, using its `suggestedDescription` (and `tag`). The JSON is where you first commit each character's locked look.
2. **Scene prompts (Step 4):** generate prompts **scene by scene, in order**, walking `sceneMap[]`. For each scene object, re-read it, then write one prompt for each block in `startLine`–`endLine` — folding in the locked `location`, the scene's single `lighting` clause, the `inFrame` cast (each as `@tag` + that scene's `sceneOutfits` garment, **tag used once**, with an age phrase from `characterAges` only when present), the `characterPositions` blocking, and the per-block action/expression from the block text. The `leadSubject` is the primary subject. Never quote dialogue — render speaking as a visible expression.

A scene whose span is `startLine: 30, endLine: 44` must produce exactly 15 prompts (44 − 30 + 1). The sum of all scene spans must equal the total SRT block count — use this as a built-in count check before you finish.

## Worked fragment (illustrative; names are placeholders)

```json
{
  "language": "English",
  "storyContext": "A single mother and her young son are refused service at a small-town diner; years later the grown son, now a wealthy executive, quietly buys the building. The story spans a 1980s winter and the present day. It contrasts public cruelty with quiet, deferred justice. The emotional theme is dignity withheld and reclaimed.",
  "mainSetting": "Riverside Diner and a downtown penthouse office",
  "storyType": "character_driven",
  "characters": [
    {
      "name": "Mara Quinn",
      "role": "struggling single mother",
      "firstAppearanceLine": 1,
      "tag": "@mara",
      "suggestedDescription": "White American female, 34 years old, lean tired build, fair skin with cool undertones, dark brown hair pulled into a loose low bun with loose strands, soft hazel eyes with a soulful weary quality, no makeup, wearing a frayed navy wool-blend coat, with a thin gray cotton dress and scuffed brown lace-up shoes"
    },
    {
      "name": "Eli Quinn",
      "role": "her young son, later grown",
      "firstAppearanceLine": 2,
      "tag": "@eli",
      "suggestedDescription": "White American male, 38 years old, lean medium build, fair skin, short dark brown neatly combed hair, calm gray-blue eyes with a quiet knowing quality, clean-shaven, wearing a charcoal cardigan over a plain white tee, with dark charcoal wool trousers and polished black leather oxford shoes"
    }
  ],
  "sceneMap": [
    {
      "startLine": 1,
      "endLine": 7,
      "location": "Small-town diner interior: heavy oak entry door, a long service counter with stools, a dozen dining tables, a brass coat rack by the front window",
      "timeOfDay": "cold overcast winter afternoon, year 1986",
      "lighting": "flat gray overcast daylight through steamed windows, cool tones",
      "sceneSummary": "A mother brings her young son into a diner and is refused a table.",
      "charactersPresent": ["Mara Quinn", "Eli Quinn"],
      "characterPositions": {
        "Mara Quinn": "standing just inside the door, one hand resting protectively on her son's shoulder",
        "Eli Quinn": "standing close at his mother's side, holding her hand"
      },
      "sceneOutfits": {
        "Mara Quinn": "wearing a frayed navy wool-blend coat over a thin gray dress",
        "Eli Quinn": "wearing a small red knit coat with mittens"
      },
      "characterAges": {
        "Eli Quinn": "White American male, 7 years old, small slight build, fair skin, short dark brown hair, wide gray-blue eyes with an uncertain quality, no facial hair"
      },
      "leadSubject": "Mara Quinn",
      "inFrame": ["Mara Quinn", "Eli Quinn"],
      "mentioned": [],
      "dramaticRelationship": "A powerless mother shielding her child from a humiliation she cannot prevent.",
      "crowdNotes": "Four occupied tables of diners watching; seven empty tables"
    },
    {
      "startLine": 8,
      "endLine": 21,
      "location": "Corner penthouse office with floor-to-ceiling glass, a large dark walnut desk in the center, a leather chair, a low credenza along one wall",
      "timeOfDay": "warm morning, present day 2024",
      "lighting": "soft warm morning sun streaming through tall glass windows",
      "sceneSummary": "The now-grown son reviews a deed of sale for the old diner building.",
      "charactersPresent": ["Eli Quinn"],
      "characterPositions": {
        "Eli Quinn": "seated behind the walnut desk, leaning back, a single document in his hands"
      },
      "sceneOutfits": {
        "Eli Quinn": "wearing a charcoal cardigan over a plain white tee"
      },
      "characterAges": {},
      "leadSubject": "Eli Quinn",
      "inFrame": ["Eli Quinn"],
      "mentioned": ["Mara Quinn"],
      "dramaticRelationship": "A man holding quiet power over the place that once humiliated his family.",
      "crowdNotes": "none"
    }
  ]
}
```

Note how `characterAges` is filled for Eli in the 1986 scene (he is 7, not his 38-year-old sheet age) and left empty in the present-day scene; how `mentioned` carries Mara into the office scene without drawing her; and how each `location` is a concrete description, not a name.
