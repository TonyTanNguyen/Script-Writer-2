# Scene Prompt Assembly Formula

One SRT block → one **self-contained** scene prompt. The image tool has no memory of any other prompt, so each prompt must carry its whole world: who is in frame, what they wear, what they are doing, the camera, **the concretely described setting**, and the light. Build each prompt as flowing prose (not bullet points):

```
@<primary tag> [<age phrase — flashbacks only>] wearing <scene garment>, <action / expression>, <camera angle>[, with @<secondary tag> wearing <their garment> <their action>][, and <anonymous background figures> <their state>], located in <CONCRETE description of the place> during <time/light>. <LIGHTING CLAUSE>, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.
```

**Tag + garment only — no other physical description in scene prompts.** Each character is referred to by their `@tag` (the reference handle from the character sheet), never by full name. The sheet defines face, build, skin, hair, eyes. A scene prompt adds only the garment for that scene, plus an age phrase if (and only if) the block is a flashback.

## Four rules that prevent the most common failures

1. **No dialogue, ever.** Never write spoken words or quotation marks. A block of narration may quote a character ("All right," he said) — render only the *visible act*: "speaking with a quiet, resolved expression", "saying something that makes the young man stand straighter" → instead write "gesturing toward the young man, who straightens in response". The finished image must contain no text and no subtitles.

2. **Use each `@tag` at most once per prompt.** Repeating a tag (e.g. tagging the subject again inside the camera phrase) makes the image tool render a second copy of that person. If the camera refers to the subject, use a pronoun: "seen from over his shoulder", not "seen from over the shoulder of @marcus". A second person's tag is used once, where they first appear.

3. **Describe the setting concretely; never reference other prompts.** The tool can't resolve "the same office", "a similar kitchen", "the Voss Road living room", or "as before". Fold the scene's locked physical description into the location phrase: not `located in the Voss Road living room` but `located in a living room with a low gray fabric sofa, a wooden bookshelf, and framed photographs on the wall`. When a location recurs in a later scene, re-state the **same concrete features** so it reads as one place.

4. **Every character carries a visible emotion — never a lifeless face.** The primary subject **and every secondary character in the frame** must show a specific, readable feeling that fits the block's emotional beat, carried by the **face plus posture/gesture**. A character given only a neutral action ("standing by the desk", "holding a folder", "looking at the door") renders blank and soulless — a mannequin. Always attach the feeling: "standing by the desk with quiet, simmering resentment", "gripping the folder with white-knuckled dread", "looking at the door with aching, fragile hope". Match each person's emotion to their sheet eye-"quality" (their fixed temperament) **and** to what this specific moment does to them. This is for **scene prompts only** — the character **sheet** stays `Calm neutral expression`, because it is a reference image, not a story beat.

## The parts

1. **Primary subject** — the character's `@tag` exactly as on the sheet, an age phrase only for flashbacks, then `wearing <scene garment>` (use the fabric/garment vocabulary from `character-formula.md`; the garment fits the scene's setting/profession/time). No other physical description. **If the shot shows the character full-body / head-to-toe (any wide or standing framing), the scene garment must name the lower garment AND footwear** ("wearing a charcoal overcoat over charcoal trousers and polished black oxford shoes") so the model does not render bare feet — see `character-formula.md`. Upper-body-only framings (close-up, seated at a table, over-the-shoulder) need only the top garment.

2. **Action / expression (emotion is MANDATORY)** — translate the block's text into something a camera sees: posture, gesture, and a **named facial emotion**. Every prompt must state what the subject *feels*, not only what they *do* — "bending to pick up a pocket watch" is incomplete; "bending to pick up a pocket watch with quiet, trembling focus" is complete. Keep it visual. Examples: "stumbling forward near the revolving glass doors with a tense look of restrained anger", "sitting quietly at the far end of the long table with a deeply focused, guarded expression", "bending to pick up a vintage pocket watch from the floor with quiet, aching focus".

3. **Camera angle** — one from the rotation pool (see `camera-and-style.md`), rotated across consecutive prompts. If the angle phrase would name the subject, switch to a pronoun (rule 2).

4. **Secondary characters** — anyone else present. Introduce with "with", "while", "as", then their **`@tag`** + `wearing <their garment>` + their own action **and their own visible emotion** (rule 4 above) — never just a posture. "with @trent standing behind the desk" is a mannequin; "with @trent standing behind the desk watching with subtle, cold amusement" has a face. Anonymous, non-sheet figures use phrases ("and twelve other staff standing silent around the room", "while a few diners watch from nearby booths"), and where a background figure is individuated enough to read a face, give it a brief mood cue too ("a server watching the scene with wary unease").

5. **Location (described, not labelled)** — `located in <concrete physical description of the place> during <time/light>`. Spell out the space and its key objects every time. Keep the described features stable across all blocks set there.

6. **Lighting clause + `pro color grading` + locked style string** — end with a lighting clause matching the scene's time/weather (it must agree with the `during …` cue), then `, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.` See `camera-and-style.md`. Never reuse a bright-day clause on a night/evening/stormy scene.

## Expression / emotion cues (include at least one per character)

Build each character's emotion as **face cue + body cue** so it reads at a glance. Don't settle for "sad" or "angry" — pick a precise, cinematic shade and show it in the body too. A small pool to draw from (mix and extend; match the block's beat and the character's sheet eye-"quality"):

- **Anger / defiance:** tense restrained anger, jaw set hard, a cold flat stare, nostrils flared, fists clenched at the sides, a slow controlled fury.
- **Grief / pain:** silent tears tracking down the face, a crumpling chin, a hollow thousand-yard stare, shoulders caving inward, a hand pressed to the mouth.
- **Hope / tenderness:** aching fragile hope, eyes glistening, a tentative half-smile, a warm softening around the eyes, leaning slightly forward.
- **Fear / dread:** wide alert eyes, a tight swallow, white-knuckled grip, a flinch held half-finished, breath caught.
- **Shame / regret:** eyes cast down and away, a deflating posture, a tight apologetic mouth, a hand rubbing the back of the neck.
- **Contempt / superiority:** a faint condescending smirk, a raised chin, a slow dismissive glance down the nose, arms folded.
- **Resolve / dignity:** a steady unflinching gaze, squared shoulders, a calm composed set to the mouth, chin level.
- **Shock / disbelief:** parted lips, frozen mid-motion, eyes locked wide, a half-step back.
- **Joy / relief:** an open unguarded smile reaching the eyes, a breath of laughter, shoulders dropping loose, head tipped back.

Two people in one frame should usually feel **different** things (the beat is the gap between them) — e.g. one watching with quiet hope while the other looks away in guarded shame. Identical expressions on everyone flatten the drama.

**Children get a softer sub-range — never the full pool above.** A child's emotion stays mild and age-appropriate: curiosity, shyness, quiet worry, delight, surprise, a small pout, a hopeful or uncertain look. Never give a child the darker/heavier entries (grief/pain, fear/dread, shame/regret, contempt, or anything reading as `terror`, `anguish`, `despair`, `rage`, `trauma`, a `hollow thousand-yard stare`). If the block's beat is genuinely heavy, put that full intensity on the nearby **adult** and give the child a lighter watching reaction instead (`beside her mother with a small worried frown`, not `frozen in silent terror`). Full rules in `minor-and-policy-safety.md` §F.

## Special cases

### Pure-narration blocks
Some blocks are narrator commentary with no on-screen action. Render the relevant character in a fitting still pose that matches the emotional beat ("standing perfectly still with an unyielding calm in his face"), or use a metaphorical image. Never skip a block — every block gets a prompt.

### Object-only / insert shots
When the beat is about a thing (a pocket watch rolling, a folded letter, banded cash in a folio), the object can be the subject. A character may appear once in the background:
```
A small brass pocket watch rolling across a polished wood floor away from a scattered red-stamped folder, seen from a low angle across the floor, while @marcus wearing a soft gray cotton polo shirt looks down at it with quiet shock, located in a corner office with floor-to-ceiling glass and a dark walnut desk during warm morning sun. Warm natural sunlight through tall windows, soft interior shadows, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.
```

### Scenes with children (read `minor-and-policy-safety.md`)
**Children are ALWAYS kept in every frame the story places them in — never pulled or substituted.** Most child scenes are fine as-is: a child alone or with other children, a child with their own parent/family doing an ordinary activity together (a mother and son baking, a father lifting his daughter onto a wagon), or children folded into a crowd. Write those naturally — a parent and child can interact warmly with each other. The filter only fires on one narrow pattern: an **unrelated** adult interacting with a child (gaze, approach, kneel-down, touch) with no parent anchoring them. When a child shares a frame with a non-parent adult — including a beat whose point is that adult — keep the child and compose safely: parent in frame, child anchored (`beside her`), every adult on a separate mundane task, no unrelated-adult gaze/contact toward the child, and the adult's focus + any contact redirected through the parent or a prop (the gift in the parent's hands, a stuffed rabbit the child holds). If the parent is missing from the source for that beat, ADD the parent to anchor the child — never remove the child. Always keep children awake, upright, clothed for the era, and supervised. **Also keep a child's expression in the mild, age-appropriate range (see the emotion-pool note above) and never place a child near a physical hazard — fire, a weapon, a height, water, or a moving vehicle — showing the moment of safety instead if the source implies danger.** See both worked examples below and the full bucketed rules in `references/minor-and-policy-safety.md` (§F for tone/danger).

### Single-character shots
Fine to have one character alone. No need to force everyone into every frame.

### Group / establishing shots
For "small figure in big space" use `framed wide with the full environment dominating the composition` or `characters small within an expansive setting`, and still describe the place concretely.

## Worked example (block → prompt)

SRT block:
> Get out. Now. The guard shoves the man toward the revolving doors. You people can't read? This is a luxury hotel, not a homeless shelter.

Scene prompt (no dialogue; each tag used once; concrete setting; daytime lighting clause):
> @marcus wearing a soft gray cotton polo shirt with a relaxed fit, stumbling forward with a tense look of restrained anger, seen from a wide front-facing perspective, with @trent wearing a tailored navy blue suit jacket standing behind a marble concierge desk watching with subtle amusement, located in a grand hotel lobby entrance with tall revolving glass doors, polished marble floors and a long concierge desk, during thin October afternoon sun through the glass. Soft natural daylight, thin pale sunlight, long soft shadows, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.

## Second worked example (a NIGHT scene — lighting must change)

SRT block:
> He set the brass pocket watch on the nightstand. We did it, Pop, he whispered. He cried.

Scene prompt (firelight clause, NOT daylight; the whispered line becomes a visible expression, not quoted):
> @marcus wearing a soft gray cotton polo shirt with a relaxed fit, sitting in a chair beside a window setting a small brass pocket watch on a nightstand with single tears rolling down his cheeks in profound emotional release, seen from a side profile that catches the watch in the warm glow, located in a simple hotel king room with a low bed, a single nightstand and a curtained window, during night warm firelight. Warm flickering firelight, deep shadows, soft amber glow, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.

## Third worked example (a CHILD kept in frame — the common case)

A child with their own mother doing an ordinary activity. No unrelated adult, so the child stays in frame and the two can interact warmly.

SRT block:
> In the warm kitchen, Maggie guided her daughter's small hands as they pressed the biscuit dough together, both of them laughing.

Scene prompt (child kept; mother and child interact; no unrelated adult in frame):
> @maggie wearing a faded calico work dress with rolled sleeves, smiling warmly as she guides the small hands of her young daughter pressing biscuit dough on a flour-dusted table, the girl beside her in a simple homespun pinafore laughing up at her mother, seen from a gentle three-quarter angle, located in a rustic 1880s farmhouse kitchen with a cast-iron stove, open shelves of tin crockery and a window over a dry sink, during soft mid-morning light through gingham curtains. Soft natural daylight, warm diffused glow, gentle shadows, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.

The mother is the child's parent, so warmth, eye contact, and touch between them are fine — this renders.

## Fourth worked example (a child + an unrelated adult — child KEPT, focus redirected)

A benefactor and a struggling mother share a diner booth with her son. The beat involves an unrelated adult, so the child stays in frame and the composition keeps the adult's focus on the mother (a peer), with the child anchored beside her reacting on his own — no unrelated-adult-to-child gaze or contact.

SRT block:
> Across the booth, Maggie's son watched the stranger with careful hope while she set down her coffee, unsure whether to trust him.

WRONG (unrelated adult engaging the child directly — blocked):
> @maggie wearing a thin denim jacket setting down a coffee mug, with @denzel wearing a worn navy barn coat leaning toward the boy and looking down at him warmly, and a boy of about eight looking up at the stranger with hope, located in a small diner booth...

RIGHT (child kept beside his mother; the stranger's attention is on the mother, not the child; the boy reacts on his own):
> @maggie wearing a thin denim jacket setting down a coffee mug with an uncertain, guarded expression, her young son of about eight beside her in a striped tee leaning into her side and watching the table with careful, hopeful eyes, seen from a side profile, with @denzel wearing a worn navy barn coat sitting across the red vinyl booth speaking toward the mother with quiet, respectful understanding, a half-eaten plate of pancakes and a small crayon drawing on the table between them, located in a small neighborhood diner with red vinyl booths and a Formica table during soft warm interior light. Low warm lamplight, deep ambient shadows, soft pools of light, pro color grading. Rendered in the style of Cinematic realistic 35mm. No text, no subtitles.

The child stays on screen anchored to his mother; the unrelated adult addresses the parent (peer-to-peer), not the child; the props add warmth. The filter has no unrelated-adult-to-child interaction to flag, and the child is never removed.

The viewer still reads "a single mother with a child here"; the filter sees only two adults and some props.
