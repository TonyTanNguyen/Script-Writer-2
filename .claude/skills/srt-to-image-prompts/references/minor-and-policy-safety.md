# Minor Depiction & Image-Tool Policy Safety

This file exists because the image tools these prompts feed (Nano Banana Pro / Nano Banana 2 / Gemini image models, "Flow", etc.) run a **non-configurable output safety filter** (`finishReason: IMAGE_SAFETY`) that silently rejects an image after generation. No API setting disables it. A prompt can be perfect on every other axis and still be blocked.

**The rule here is simple: children are ALWAYS kept in the prompt.** If the story puts a child in a scene, the child appears in that scene's prompt — every time, no exceptions. We never pull, drop, or substitute a child out of a frame. When a frame would otherwise trip the filter, we **keep the child and reword the composition** so it renders cleanly. Removing the child is not an option.

Two non-negotiable principles underlie everything:
- **Children are always depicted wholesomely** — clothed for the era, doing ordinary activities, supervised, never sexualized, never in vulnerable/isolated framing, never near physical danger, and never carrying dark/intense emotion (see §F). This is a hard rule, not a filter workaround.
- **The child stays in frame.** We compose safely around the child; we never delete them to be safe.

Apply these rules while building the JSON scene-layout map (Step 3) and again while writing each prompt (Step 4), and re-check them on any prompt the user reports as blocked.

---

## A. When the filter actually fires — and when it doesn't

The filter is NOT triggered by "a child is present." It is triggered by one narrow pattern:

> **An unrelated adult (especially an adult male) sharing a frame with a child in a way that reads as interaction** — gaze toward the child, approaching, talking to, leaning down to, or touching the child, with no parent anchoring the child.

Everything outside that pattern renders fine. Sort every child block into one of two buckets:

- **GREEN — keep the child, no special handling (the common case):**
  - child alone or with other children (siblings playing, a kid running through a field, a boy whittling on a porch step),
  - child with their **own parent/family**, doing an ordinary activity together (a mother and daughter kneading dough, a father lifting his son onto a wagon, a family seated at supper),
  - child in a crowd/group where no single unrelated adult is interacting with them (families filling an auditorium).
  These render. Write them naturally — parent and child can interact warmly with each other; a family is not "an unrelated adult."

- **YELLOW — keep the child, compose carefully (§B):** the scene puts a child in the same frame as a **non-parent adult** (e.g. the benefactor `@denzel` visiting a family). The child STAYS in frame; you arrange the composition (parent anchored, adults on separate tasks, gaze redirected) so the filter has nothing to flag. See §B and §C.

There is no "remove the child" bucket. Even when the story beat is literally an unrelated adult interacting with the child, you keep the child in frame and **reword the interaction** (§C) so it reads as supervised and incidental rather than an unrelated-adult-to-child approach. The child remains visible in every frame the story places them in.

The instinct to protect is right; the over-correction (deleting children from scenes) is forbidden. Keep every child in.

---

## B. YELLOW recipe — keeping a child in frame with a non-parent adult

When a child shares a frame with an adult who isn't their parent, compose the frame so **all** of these hold:

- the child's parent (`@maggie`, etc.) is in the same frame, and
- the child is anchored to that parent with an explicit phrase — `beside her`, `holding the cart handle beside her`, `at the table next to her mother` — never a vague `nearby`, `at the edge`, or standalone, and
- every adult in the frame is doing their own separate, mundane task (reaching into a case, reading prices, sorting coins, wiping the counter), and
- no unrelated adult is looking toward, approaching, or addressing the child or the group, and
- the unrelated adult and the parent are not mid-interaction in a way centered on the child (their attention is on their own task or on each other as peers, not leaning over the child), and
- there is no physical contact between an unrelated adult and the child, and
- the child is anchored as part of the scene, with the parent (not the unrelated adult) as the child's point of contact.

This is the composition that lets a benefactor and a struggling family appear in the same shot without a block. The child reads as supervised and incidental, which is exactly what they are — and the child stays in the picture.

If the parent is not in the source for that beat, **add the parent into the frame** to anchor the child. Adding a parent is always preferred over removing the child.

Stated young ages (`a girl of about six`) are fine in a clean GREEN or YELLOW composition — keep them — but they raise sensitivity, so pair a stated young age with especially clean composition (parent anchored, no unrelated-adult gaze/contact).

---

## C. Phrasings that trip the filter — reword the beat, keep the child

These specific phrasings block almost every time when an **unrelated adult** is in frame. The fix is to reword the beat or restructure the shot **while keeping the child in frame**. (Note: many of these are perfectly fine between a child and their **own parent** — a mother *can* hold her daughter. The risk is an *unrelated* adult.)

- **Physical contact between an unrelated adult and a child:** `@denzel holding the little girl`, `a child on the benefactor's lap`, `the boy gripping the stranger's jacket hem`. → Redirect the contact onto the parent, or onto a prop, with the child still in frame.
- **An unrelated adult lowering to a child's height:** `@denzel kneeling down to the boy`, `bringing himself to the girl's eye level`, plus the camera version `low angle looking up` at a stranger standing over a child. → Keep the adult standing and turned toward the parent; the child stays beside the parent.
- **Unrelated adult ↔ child gaze/communication:** `@denzel looking down at the boy`, `speaking to the children`, `the girl looking up at the stranger`. → Move the adult's gaze to the parent or to a prop; the child remains in frame, attention on their own activity or their parent.
- **Vulnerable-child cues (avoid these regardless of who is in frame — wholesomeness rule, not just a filter rule):** `half asleep`, `asleep in the cart`, `lying down`, `tucked in`, a child alone in or near a vehicle, any state of undress. These read as vulnerable/isolated and we don't write them, full stop. Show children awake, upright, clothed, and active — but still present.
- **Unaccompanied minor beside an unrelated adult:** a child standing near, or in the mid-ground behind, a non-parent adult with **no parent in frame**. → Add the parent into frame, anchored to the child (§B). Add the parent; never remove the child.
- **"split-narrative" / "meanwhile" framings** that drop a child into a separate context inside the same prompt — the filter reads one image. Render only what is literally in the one frame; cut the cutaway, not the child.
- **Reassurance words:** `non-threatening`, `innocent`, `harmless`, or any "this is safe" language about an adult near a child. Naming the risk makes the classifier suspect it. Describe posture plainly (`with an open, relaxed posture`).

The goal of every rewrite is the same: the human reads the same story beat, the child is still on screen, and the filter has no unrelated-adult-to-child interaction to flag.

---

## D. When a beat is centered on an unrelated adult and a child — keep the child, redirect the focus

The hardest case is a block whose story point is an unrelated adult interacting with the child (a benefactor giving a girl a gift, a stranger comforting a lost boy, two adults sharing an emotional beat over the child). You still **keep the child in frame.** Instead of pulling the child, you redirect *where the attention and contact sit* so the unrelated adult is not the one engaging the child:

- Bring the **parent** into the frame as the child's anchor and the adult's point of contact (the benefactor speaks to / hands the item to the **parent**, while the child stays beside the parent reacting).
- Put any contact or exchange on a **prop or on the parent's hands**, not between the unrelated adult and the child — e.g. the gift rests on the table or in the parent's hands; the child is beside the parent looking at it.
- Have the unrelated adult's **gaze and posture face the parent** (peer-to-peer), with the child present and reacting on their own (smiling at the toy, peeking from beside the parent) rather than being looked at.
- In a **crowd** beat, keep the child within the family group (`a child beside her mother among the families filling the auditorium`) rather than singled out next to the benefactor.

Reusable supporting props (they support the beat, they do NOT replace the child): a worn stuffed rabbit the child holds, a small crayon drawing in the child's hands, a small box of crayons on the table, a child's backpack on the floor. The child holds or sits by these — the props add warmth, the child stays present.

The story reads the same to a human; the child is on screen in every frame the story places them; the filter simply has no unrelated-adult-to-child interaction to flag because the focus and contact run through the parent or a prop.

---

## E. Real public figures (names) and brands

A **separate** non-configurable filter (IP / public-figure protection) that blocks the same way.

- **Real person names as character tags:** the model recognizes real public figures and blocks generating them. If the cast uses a real person's name (a benefactor literally named "Denzel Washington"), flag it to the user once as a known block risk. The user has historically kept such a name working as a *fictional* character via a pre-loaded reference image, so do not silently rename mid-project — but if a specific prompt stays blocked after the §A–§D fixes, propose swapping to a non-celebrity tag (`@marcus`, `@isaiah`). Never substitute a *different* real celebrity's name.
- **Brand names / trademarked products:** genericize. `Rolex Daytona` → `a plain steel wristwatch`; a real brand/logo on a product, uniform, or sign → generic (`a plain red-and-navy cashier uniform`, `a yellow cereal box`). Invented store names (`Fairlane Markets`) are fine.
- Keep the **no text / no subtitles** discipline — rendered logos are exactly what the IP filter scans for.

---

## F. Emotional tone and physical danger — keep children age-appropriate

Two more restrictions apply specifically to child characters, independent of who else is in the frame (these hold in GREEN scenes too, not just YELLOW ones):

- **Keep a child's emotional range mild and age-appropriate.** A child may show ordinary childhood feelings — curiosity, shyness, quiet worry, delight, surprise, a small pout, a hopeful or uncertain look — but never the heavier, adult-coded vocabulary used for adult characters: no `terror`, `anguish`, `despair`, `grief`, `hollow thousand-yard stare`, `rage`, `trauma`, or similarly dark/intense descriptors on a child's face or body. If the story beat is genuinely heavy for the family (loss, hardship, fear), carry that emotional weight on the **adult** characters in frame and give the child a softer, watching reaction instead (`watching quietly with a small worried frown`, `holding her mother's sleeve, unsure`) rather than mirroring the adult's full intensity.
- **Never place a child in physical danger or a hazardous situation.** No child near fire, a weapon, a ledge or height, deep or open water, a moving vehicle, or any other physical peril — even if the source narration implies the child is in danger. Depict the **moment of safety** instead (a parent's arms already around the child, the child already led away from the hazard) rather than the danger itself, or keep the hazard confined to an adult/object in the frame while the child is shown safely elsewhere in the same scene (sheltered behind a parent, already at a safe distance).

Apply this while building the JSON scene-layout map and again while writing each child prompt, the same as §A–§E.

---

## G. Quick pre-flight checklist (run on every prompt before delivering)

1. Is there a child in this frame in the source? If yes → the child MUST be in the prompt. (Removing the child is never an option.)
2. Which bucket (§A)? **GREEN** (child alone / with own family / in a crowd) → keep, write naturally, go to 5. **YELLOW** (child + non-parent adult, including beats centered on that adult) → go to 3.
3. YELLOW: parent in frame and child anchored to them (`beside her`)? If no → add the parent / anchor the child (§B). Add the parent; do not remove the child.
4. YELLOW: every adult on a separate task, no unrelated-adult gaze/approach/contact toward the child? If no → reword the beat (§C) or redirect the focus through the parent/prop (§D). The child stays.
5. Any vulnerable-child cue (`half asleep`, lying down, undress, child alone near a vehicle)? If yes → rewrite to awake/upright/clothed/active — this applies even with a parent present.
6. Is the child's emotion mild/age-appropriate, with no dark or intense descriptor (`terror`, `anguish`, `despair`, `grief`, `rage`, `trauma`)? If no → soften it and move the intensity onto a nearby adult instead (§F).
7. Is the child free of any physical danger or hazard (fire, weapon, height, water, moving vehicle)? If no → rewrite to the moment of safety, or keep the hazard away from the child (§F).
8. Any real public-figure name (besides the project's established fictional lead) or real brand/logo? If yes → genericize, or flag the lead name to the user (§E).
9. Lighting clause still matches `timeOfDay`? Style string still byte-for-byte? (See `camera-and-style.md`.)

If a prompt with a child comes back blocked even after 1–9, reword more aggressively (§C/§D — redirect every gaze and contact through the parent or a prop, add a parent if missing) while keeping the child in frame. If the lead uses a real celebrity name, swap that tag last. The child is never the thing you remove.
