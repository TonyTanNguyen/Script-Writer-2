# Character Description Formula

Every character gets ONE fixed full description inside parentheses on the **character sheet** — a multi-view reference-sheet prompt that **leads with the character's `@tag` in place of their name** and generates the reference image. Leading with the tag means the image it produces can be saved straight under that tag (e.g. `@denzel.png`) — the exact handle the scene prompts call — so there's no manual renaming after generation. Scene prompts do NOT repeat the clause or the full name; they refer to the character by that same **`@tag`** derived from their name (e.g. `@denzel`), which the user has pre-loaded as a reference image. This file defines the attribute order and vocabulary so the sheet reads consistently, how to build the tag, and how a character is referred to in a scene prompt.

## Attribute order (inside the parentheses)

`(<ethnicity> <gender>, <age>, <build>, <skin>, <hair>, <eyes + "quality">, <facial hair / makeup>, wearing <garment>, <full lower-body outfit + footwear>)`

Concretely, in this order:
1. **Ethnicity + gender** — match whatever the script implies, e.g. "Black American male", "white European female", "East Asian male", "South Asian female", "Hispanic American male", "Middle Eastern male".
2. **Age** — exact ("56 years old", "41 years old") or banded ("mid 20s", "late 30s", "early 40s"). Pick one and never change it for that character.
3. **Build** — "broad solid build", "lean medium build", "slim athletic build", "slender elegant build". For very large characters, fold height in: "broad solid build standing six foot four with a thick neck".
4. **Skin** — "deep mahogany skin tone", "fair skin with cool undertones", "warm caramel skin tone", "olive-tan skin tone", "fair pale skin tone".
5. **Hair** — color + length + style: "short salt-and-pepper cropped hair with a natural coarse texture", "blonde hair pulled back into a tight chignon bun", "silver hair combed straight back with a precise part".
6. **Eyes + quality** — ALWAYS pair an eye color with a character "quality" that signals their role/temperament: "dark brown eyes with a sharp disciplined and piercing quality", "sharp green eyes with a piercing weaponized quality", "soft hazel eyes with a soulful weary quality", "cold blue eyes with a sharp superior quality", "dark brown eyes with a soulful uneasy and sympathetic quality". This quality word is the emotional fingerprint — keep it stable per character. On the **sheet** the face stays neutral (it is only a reference image), but in **scene prompts** you must *act this fingerprint out* with an explicit, block-specific expression every single scene — see `scene-prompt-formula.md` rule 4 and its emotion pool. A character with no stated feeling renders lifeless.
7. **Facial hair / makeup** — "clean-shaven", "clean-shaven sharp jawline", "heavy 5-day stubble pattern", "neat mustache", "moderate makeup with glossy lips", "polished professional makeup", "minimal elegant makeup".
8. **Garment** — start with "wearing a/an …", be specific about fabric + cut + color: "wearing a soft gray cotton polo shirt with a relaxed fit", "wearing a tailored navy blue polyester blend suit jacket over a crisp white cotton button-down shirt", "wearing a dark navy blue polyester security uniform jacket with silver law-enforcement style patches on the shoulders". This is the **reference/default garment** worn on the character reference sheet. Scene prompts may specify a different garment appropriate to each scene's context — see `scene-prompt-formula.md`.
9. **Lower body + footwear (ALWAYS include — characters are never barefoot unless the script explicitly calls for it)** — because the character sheet is a **full-body** image, you must state the trousers/skirt AND the shoes, or the model renders bare feet. Continue the clause with a lower garment + specific footwear: "with charcoal wool trousers and polished black leather oxford shoes", "with dark blue denim jeans and tan work boots", "with a long gray wool skirt and black ankle boots", "with khaki chino trousers and brown leather loafers". Make the footwear fit the character's era, region, and profession (period boots for an 1880s frontier character, plain sandals for an ancient setting, sneakers for a modern teen). **Only** omit shoes if the script explicitly places the character barefoot (e.g. on a beach, in bed) — and in that case write "barefoot" deliberately, never leave it unstated.

## Character-sheet line format (the `<name>_characters.txt` file)

The character sheet is a **multi-view reference-sheet prompt** for generating each reference image (full body, several angles on a plain white background). Each line **leads with the character's `@tag` in place of their name** — that way the image it generates can be saved directly under that tag, matching what the scene prompts call, with no renaming. Each numbered line:

```
N. @tag (<full attribute clause>), full body, multiple views: front view, 3/4 view, side view, back view, all in one image. Calm neutral expression, standing upright, hands relaxed at sides. Clean white background, flat lighting, no shading, no shadows. Cinematic realism, photorealistic, character reference sheet, no text, no subtitles.
```

Worked example:

```
1. @denzel (Black American male, 56 years old, broad solid build, deep mahogany skin tone, short salt-and-pepper cropped hair with a natural coarse texture, dark brown eyes with a soulful commanding quality, clean-shaven sharp jawline, wearing a soft gray cotton polo shirt with a relaxed fit, with dark blue denim jeans and tan work boots), full body, multiple views: front view, 3/4 view, side view, back view, all in one image. Calm neutral expression, standing upright, hands relaxed at sides. Clean white background, flat lighting, no shading, no shadows. Cinematic realism, photorealistic, character reference sheet, no text, no subtitles.
```

- The multi-view framing and trailing style string are FIXED for the character sheet. Only the `@tag` and parenthetical attribute clause change per character.
- **Footwear is mandatory on the sheet.** The sheet renders the full body from front, side, and back, so the feet are always visible. Every attribute clause MUST end with the lower-body + footwear (item 9) — e.g. "… wearing a soft gray cotton polo shirt with a relaxed fit, with dark blue denim jeans and tan work boots". A sheet line that stops at the top garment leaves the model to invent bare feet. Never deliver a sheet line without shoes (unless the script explicitly makes that character barefoot, in which case write "barefoot").
- The `@tag` **opens each sheet line** (in place of the name) and is the same handle the scene prompts use — so the reference image this line generates gets filed under that exact tag. On the sheet itself the tag has nothing to point to yet (this line is what *creates* the reference image); it rides along purely as the line's identifier so the output can be named for that tag. From then on, scene prompts load that saved image by the same tag. Do NOT write the character's full name at the start of the line — the tag replaces it. (The full name still lives in the internal JSON map, so nothing is lost.)

### How to build the `@tag` (leads each sheet line AND is reused in every scene prompt)
- `@` + the character's **first name in lowercase**, with no spaces, titles, or punctuation: "Denzel Washington" → `@denzel`, "Doctor Renaldo Foster" → `@renaldo`, "Hollis Pemberton the Fourth" → `@hollis`.
- **Collisions:** if two characters share a first name, disambiguate by appending the last name (`@earltomlin` vs `@earlgrey`) or a short suffix. Each tag must be unique across the whole video.
- **Unnamed recurring roles** get a short descriptive tag: "the Uniformed Officer" → `@officer`, "the Valet Supervisor" → `@valet`, "the Old Man" → `@oldman`.
- One tag per character, fixed for the entire video. Anonymous, non-sheet background figures get **no tag** (they stay plain phrases).

## Fabric / garment vocabulary (for variety + realism)

cotton, polyester blend, wool, wool-blend, silk, knit, polyester. Cuts: tailored, structured, fitted, relaxed fit, loose-fitting. Use brand-neutral but specific items: polo shirt, button-down shirt, pencil skirt, structured blouse, security uniform jacket, bellman jacket with gold trim and brass buttons, military dress service jacket with brass buttons and ribbons, housekeeping uniform dress, manager's blazer. (Pull garments that fit the script's own setting — period, region, profession.)

## Eye-"quality" pool (match to role)

- Protagonist / disciplined: "sharp disciplined and piercing quality", "calm knowing quality"
- Antagonist / cold: "sharp superior quality", "piercing weaponized quality", "sharp condescending quality", "sharp mocking quality", "weary cold quality"
- Sympathetic / kind: "soulful weary quality", "soulful uneasy and sympathetic quality", "soulful commanding quality", "quiet holding-still quality"
- Authority / neutral: "stern focused quality", "sharp confident quality", "focused inquisitive quality"

## How a character is referred to inside a scene prompt (CRITICAL)

Scene prompts do **not** use the character's full name and do **not** repeat the full parenthetical attribute clause. Inside a scene prompt a character is referred to by their **`@tag`** (the reference handle), written as:

`@<tag> [<age phrase — flashbacks only>] wearing <that scene's garment>`

Rules:
- Use the **exact `@tag`** from the sheet every time (e.g. `@denzel`, `@renaldo`) — never the full name, never abbreviated, never an epithet like "the physician".
- Append `wearing <garment>` for that scene (the wardrobe-by-act garment). Do **not** add ethnicity, age band, build, skin, hair, eyes, or facial hair — those stay on the sheet only.
- **Include footwear (and the lower garment) whenever the shot would show the legs or feet** — any full-body, wide, or standing shot where the character is seen head-to-toe. The scene garment for those shots must name the shoes (e.g. "wearing a charcoal overcoat over charcoal trousers and polished black oxford shoes", "wearing a faded calico work dress and worn leather ankle boots"), so the model doesn't render bare feet. For tight framings that only show the upper body (close-up, head-and-shoulders, over-the-shoulder, seated-at-a-table), the top garment alone is fine — the feet aren't in frame. When unsure, include the footwear. Match the shoes to the character's era/region/profession, consistent with their sheet.
- Add an **age phrase ONLY when the block is a flashback / a younger or older version**: `young @denzel as a twelve-year-old boy`, `a younger @marcus in his 30s`, `an elderly @marcus in his 80s`. For present-day blocks, no age phrase.
- **Use each `@tag` at most ONCE in the whole prompt.** Repeating a tag makes the image tool draw a duplicate of that person. If a camera phrase points back at the subject, use a pronoun ("over his shoulder"), never the tag again. A second character's tag is used once, at their first mention.
- Only truly anonymous, non-sheet background figures (crowds, unnamed staff) use short descriptive phrases like "a few hotel guests" or "a server in a white jacket" — they have no tag.

Correct (two tags, each used once, with scene garment):
> @marcus wearing a soft gray cotton polo shirt, leaning forward over the table with an earnest frown, seen from a side-angle perspective, with @elena wearing a tailored navy blazer looking down at her files, located in …

Correct (flashback, age phrase added):
> young @marcus as a ten-year-old boy wearing a faded red hand-me-down sweater, sitting on the front steps with a hopeful look, seen from a wide front-facing perspective, located in …

Wrong (full name / attribute clause used — do NOT do this):
> Marcus Bell (East Asian male, 56 years old, …) wearing a gray polo, leaning forward over the table, …

Wrong (same tag used twice — causes a duplicate person):
> @marcus wearing a gray polo, leaning forward, seen from over the shoulder of @marcus toward the window, …

Wrong (character collapsed to epithet — do NOT do this):
> @marcus wearing a gray polo, leaning forward, with the security chief watching nearby, …

## Consistency guardrails

- Lock each character's items 1–7 (ethnicity, age, build, skin, hair, eyes+quality, facial hair) for the entire video. These never change.
- Item 8 (garment) is written on the sheet as a reference default, but **may and should change** in scene prompts to match each scene's context (setting, profession, time of day, story act).
- Never let the protagonist's age or skin tone drift between sheet entries. (Common failure: protagonist becomes "mid 40s, warm brown" when he started "56, deep mahogany" — pick one and hold it.)
- All English. No stray foreign words.
