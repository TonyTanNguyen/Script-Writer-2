# Camera Angles, Location Formula, Lighting & Locked Style String

## Camera-angle rotation pool

Each scene prompt names one camera framing. Rotate through these so consecutive prompts feel like a cut sequence, not the same shot repeated. Don't use the same angle three times in a row unless the action genuinely continues.

- `seen from a wide front-facing perspective`
- `seen from a low angle across the marble floor` (swap floor noun to fit the room)
- `seen from a high angle looking down at the floor`
- `seen from a high three-quarter angle`
- `seen from a side profile` / `seen from a side-angle perspective`
- `seen from an elevated rear perspective`
- `seen from over his shoulder` / `seen from over her shoulder` (over-the-shoulder of the subject — use the **pronoun**, never re-tag the subject)
- `seen from over the shoulder of @<second tag>` (only when that character is NOT already tagged elsewhere in the prompt — their tag may be used here exactly once)
- `seen from behind his shoulder` / `seen from behind her shoulder`
- `seen through the glass of a display case` / `seen through the glass of an office partition`
- `seen from inside looking out through the storefront glass`
- `framed wide with the full environment dominating the composition` (for "small figure in big space" beats)
- `characters small within an expansive setting` / `viewed from a distance that captures the entire location around them`

**Tagged-once rule for camera phrases:** if the over-the-shoulder / behind-the-shoulder framing points at a character already tagged in the prompt, use a pronoun (his/her). Using the same `@tag` twice makes the image tool render a duplicate. Only put a `@tag` in the camera phrase if that character appears nowhere else in the prompt.

Pacing tip (mirrors good storyboard practice): vary wide → medium → close across a sequence. Use wide/`framed wide` for establishing or isolation beats; over-the-shoulder for confrontations; high angle for someone being diminished; low angle for someone gaining power.

## Location formula (a DESCRIBED place, not a bare label)

After the action and characters, state the setting. The image tool has no memory of other prompts and cannot resolve a proper-noun label, so **describe the place concretely every time** — the space plus its key objects:

`located in <concrete physical description of the place> during <time of day / lighting condition>`

Examples (note each spells out what is actually in the frame):
- `located in a grand hotel lobby entrance with tall revolving glass doors, polished marble floors and a long concierge desk during thin October afternoon sun through the glass`
- `located in a corporate boardroom with a long black walnut table, leather chairs and a wall of windows during morning haze burning off outside`
- `located in a cramped cinderblock office with a metal desk, a folding chair and a single small window during bright clear daylight`
- `located in a worn tow-truck cab with a cluttered dashboard and a fogged windshield during dead-of-winter night`
- `located in a living room with a low gray fabric sofa, a wooden bookshelf and framed photographs on the wall during soft evening light`

Decide each location's concrete description once (store it in the JSON scene-layout map's `location` field) and reuse the **same features** in every block set there, and in any later scene that returns to the same place — so the environment reads as one consistent location across the video. Do NOT shorten a recurring place to a bare name ("the Voss Road living room") or a comparison ("a similar kitchen", "the same office") — the tool will not understand it. The examples above are illustrative; build the description from the script's own world (a village market, a hospital ward, a 1920s tenement, a spaceship corridor, whatever the story implies).

## SCENE STYLE TAIL = LIGHTING CLAUSE (flexible) + LOCKED STYLE STRING (fixed)

The end of every scene prompt has TWO parts. Only the second part is byte-for-byte fixed. The first part — the **lighting clause** — MUST match the actual time of day and weather of the scene. Do not paste "Natural daylight, bright clear lighting" onto a night, evening, stormy, or firelit scene; that is the exact mistake to avoid.

### Part A — Lighting clause (CHOOSE to fit the scene)
Write a short clause describing the light/weather of THIS scene. It should agree with the `during …` you used in the location phrase. Pick or adapt from the pool below (or write your own that fits):

- **Bright midday / clear day** → `Natural daylight, bright clear lighting, soft natural shadows, no artificial lights`
- **Thin/low autumn or winter sun** → `Soft natural daylight, thin pale sunlight, long soft shadows`
- **Overcast / grey day** → `Soft diffused overcast light, flat grey tones, muted shadows`
- **Golden hour / late afternoon** → `Warm golden-hour light, long amber shadows, soft natural glow`
- **Soft evening / dusk** → `Soft fading evening light, cool dim tones, gentle shadows`
- **Night, interior lamplight** → `Low warm lamplight, deep ambient shadows, soft pools of light`
- **Night, firelight** → `Warm flickering firelight, deep shadows, soft amber glow`
- **Rain / storm** → `Cool overcast storm light, wet reflective surfaces, soft diffused shadows`
- **Harsh sun / heat** → `Strong direct sunlight, hard bright highlights, sharp short shadows`
- **Window-lit interior, daytime** → `Warm natural sunlight through tall windows, soft interior shadows`

Always close Part A with `, pro color grading.` (the color-grade note stays in every scene).

### Part B — Locked style string (copy EXACTLY, every scene)
```
Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.
```

### Putting it together
`<Part A lighting clause>, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.`

Examples:
- Day lobby → `Natural daylight, bright clear lighting, soft natural shadows, no artificial lights, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.`
- Night room at the end → `Warm flickering firelight, deep shadows, soft amber glow, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.`
- Disgraced manager, evening office → `Soft fading evening light, cool dim tones, gentle shadows, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.`

### Consistency rule
The lighting clause MUST agree with the `during …` cue in the same prompt. If `located in … during soft evening light`, the tail must be an evening clause — never "bright clear lighting". Scenes set in the same place at the same time of day should share the same lighting clause so the location reads consistently.

## Note on the two different style strings

- The **character sheet** lines end with the multi-view reference-sheet string (see `character-formula.md`): "...Clean white background, flat lighting, no shading, no shadows. Cinematic realism, photorealistic, character reference sheet, no text, no subtitles." The character sheet is a neutral white-background reference, so it has no scene lighting — never apply scene weather to the sheet.
- The **scene prompts** end with the **lighting clause + locked style string** described above. The lighting clause varies per scene; the "Rendered in the style of Cinematic realistic 35mm. No text, no subtitles." part is fixed.
Don't mix them up: the multi-view reference-sheet string for the character sheet, lighting clause + locked style string for scenes.
