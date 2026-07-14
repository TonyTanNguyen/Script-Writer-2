---
name: english-tts-normalization
description: Normalize an English script (American English by default) into clean, plain "read-ready" text so a TTS engine speaks it correctly and naturally with the fewest mistakes — especially for local/open neural models like OmniVoice (Xiaomi), MiMo-V2-TTS, VieNeu-TTS, Kokoro, Piper, or XTTS, which usually have NO built-in text normalization. Use whenever the user has an English script or passage and wants to "clean it up for TTS", "prep a script for voice", "make it read-ready", "fix it so the AI voice reads numbers/abbreviations/symbols right", "stop my TTS mispronouncing things", or mentions feeding text into a text-to-speech / voice-cloning tool. It converts numbers to words, expands abbreviations, spaces out initialisms, respells tricky names and heteronyms, turns symbols into words, strips non-speech formatting, and splits long sentences for natural pacing — WITHOUT changing the meaning or wording. Do NOT use it to write new scripts, translate, or generate subtitles.
---

# English TTS Script Normalization

## What this skill does and why it matters

The user has a finished English script and wants to feed it into a TTS (text-to-speech) engine. The job is to turn the raw script into **read-ready plain text**: paste it straight into the engine and it pronounces everything correctly, sounds natural, and rarely stumbles.

Why this is needed: local and open neural TTS models — OmniVoice, MiMo-V2-TTS, VieNeu-TTS, Kokoro, Piper, XTTS, and similar — typically have **no strong text-normalization front-end**. Many feed characters almost directly into the model. A big cloud service might read "$3.50" as "three dollars and fifty cents" on its own, but a local model often will not. OmniVoice in particular maps text directly to acoustic tokens with no separate text-modeling stage, so anything unusual — a number, an abbreviation, a stray symbol — is likely to be read wrong or skipped. So the text has to be normalized *before* it reaches the model.

One principle runs through everything: **write for the ear, not the eye.** The listener can't re-read, so each sentence has to land the first time, and the pacing has to feel natural when spoken aloud.

## Process

1. Take the English script from the user (pasted directly or as an attached file).
2. Apply all the normalization rules below across the whole script.
3. Return the normalized script as clean plain text, in the output format described at the end.

## Top rules (never break these)

- **Don't change the content.** Only adjust the *written form* so the machine reads it right. Don't add sentences, cut sentences, summarize, paraphrase the meaning, or add commentary. Keep the author's voice, tone, emphasis, and sentence order intact. Rewording is allowed *only* in the narrow case of resolving an ambiguous pronunciation (see Rule 6), and even then keep the meaning identical.
- **Output is plain text.** No markdown, no SSML tags, no emoji, no decorative symbols, no bullet characters. A local TTS will read every stray character out loud — including tags — so everything in the output must be a readable word or normal punctuation.
- **Correct spelling, full punctuation.** Every sentence ends with a clear period, question mark, or exclamation point. Misspellings can throw off pronunciation, so fix obvious typos (but never alter intended wording or style).

## Normalization rules

### 1. Numbers become words
Write every number out the way an American would say it aloud, choosing the most natural reading for the context. This is the single biggest source of TTS errors because local models rarely handle digits on their own.

- Counts / quantities: `1,500` → "one thousand five hundred"; `27` → "twenty-seven".
- Years: `2026` → "twenty twenty-six"; `1984` → "nineteen eighty-four"; `2000` → "two thousand"; `2007` → "two thousand seven".
- Money: `$300` → "three hundred dollars"; `$3.50` → "three dollars and fifty cents" (or "three fifty" if that fits the tone); `$1.2 million` → "one point two million dollars".
- Percent: `50%` → "fifty percent"; `0.5%` → "zero point five percent".
- Decimals: `3.5` → "three point five".
- Fractions: `1/2` → "one half"; `3/4` → "three quarters"; `2 1/2` → "two and a half".
- Ordinals: `1st` → "first"; `21st` → "twenty-first"; `March 3rd` → "March third".
- Phone numbers: read digit by digit, grouped naturally: `(555) 123-4567` → "five five five, one two three, four five six seven".
- Dates: `3/15/2026` → "March fifteenth, twenty twenty-six"; `March 3, 2026` → "March third, twenty twenty-six".
- Times: `10:30 a.m.` → "ten thirty in the morning"; `8 p.m.` → "eight o'clock at night" (or "eight p m" if the tone is clipped/casual — pick what reads naturally).
- Ranges: `2014-2018` → "twenty fourteen to twenty eighteen"; `5-10` → "five to ten".
- Large/round numbers: `1,000,000` → "one million"; `$2.5B` → "two and a half billion dollars".
- Roman numerals: "World War II" → "World War Two"; "Henry VIII" → "Henry the Eighth"; "Super Bowl LVIII" → "Super Bowl fifty-eight".
- Mixed alphanumerics (model/product names): `iPhone 15 Pro` → "iPhone fifteen Pro"; `Boeing 737` → "Boeing seven thirty-seven".

### 2. Expand abbreviations to full words
The model can't reliably infer abbreviations, especially domain-specific ones. Spell them out by meaning:

- Titles: `Dr.` → "Doctor"; `Mr.` → "Mister"; `Mrs.` → "Missus"; `Ms.` → "Miz"; `Prof.` → "Professor"; `Sr.`/`Jr.` → "Senior"/"Junior".
- `St.` is ambiguous — decide from context and spell it out: `St. Louis` → "Saint Louis", but `Main St.` → "Main Street".
- Latin/list abbreviations: `e.g.` → "for example"; `i.e.` → "that is"; `etc.` → "and so on"; `vs.` → "versus"; `approx.` → "approximately".
- Units: `km` → "kilometers"; `kg` → "kilograms"; `lb` / `lbs` → "pounds"; `ft` → "feet"; `mph` → "miles per hour"; `°F` → "degrees Fahrenheit"; `°C` → "degrees Celsius".
- US state and place abbreviations read as the full name when spoken that way: `CA` → "California"; `NYC` → "New York City"; `U.S.` → "United States" (or "U S" if used adjectivally and that reads better).

### 3. Acronyms and initialisms
Decide how each one is meant to be said, and force it.

- **Read as a word** (acronyms) — usually safe to leave as is: `NASA`, `NATO`, `radar`, `scuba`. If the engine mangles one, respell it phonetically (e.g. `NASA` → "Nassa").
- **Read letter by letter** (initialisms) — local models often stumble, so space the letters out: `FBI` → "F B I"; `CEO` → "C E O"; `USB` → "U S B"; `FAQ` → "F A Q"; `ATM` → "A T M". Spacing the letters is the most reliable way to force a letter-by-letter reading.
- When in doubt, test the bare form first; only space it out if the engine gets it wrong.

### 4. Symbols become words
- `&` → "and"; `@` → "at"; `#` → "number" (or "hashtag" if that's the meaning); `%` → "percent"; `+` → "plus"; `=` → "equals"; `~` → "about"; `/` → "slash" or "or" or "per" depending on meaning.
- `$` → "dollars"; `€` → "euros"; `£` → "pounds"; `°` → "degrees".
- A hyphen or dash between two numbers means "to": `8-10 a.m.` → "eight to ten in the morning".
- URLs and emails: spell them out — `example.com` → "example dot com"; `info@example.com` → "info at example dot com".
- Strip all decorative symbols, emoji, asterisks, bullet characters, and leftover brackets.

### 5. Sentences and pacing (so the voice sounds natural)
The ear is very sensitive to flow and pause placement. Long sentences make the model breathe in the wrong spot or run out of air.

- Split long sentences into shorter ones — aim for roughly 14 to 20 words each. One idea, one sentence.
- Make sure every sentence ends with a clear period, question mark, or exclamation point.
- Use commas to create short pauses where a speaker would naturally pause.
- Avoid em-dashes and semicolons — many local engines ignore them or pause oddly. Replace them with a period or comma as the sense requires.
- Use ellipses (…) sparingly for a soft trailing pause; a period is usually more reliable.
- Rewrite parentheticals as plain clauses or separate sentences — parentheses often produce a weird pause or get read as "open paren".
- Put a blank line between paragraphs so the model takes a breath between sections.
- Don't write whole words in ALL CAPS — some engines spell capitalized words out letter by letter. Use normal capitalization and let the words carry emphasis.
- Keep contractions ("don't", "we'll", "it's") — they read naturally and match spoken English.

### 6. Heteronyms and ambiguous pronunciations
TTS uses surrounding context to pick a pronunciation and a stress pattern. Some English words are spelled the same but pronounced differently depending on meaning ("read", "lead", "tear", "live", "wind", "bow", "produce", "record", "present", "object", "content", "desert", "close", "wound"). If a sentence leaves the reading ambiguous, either keep enough context so the right reading is forced, or gently reword (without changing the meaning) so the engine reads it correctly. As a last resort, respell the word phonetically (see Rule 7).

### 7. Tricky names and foreign words
If a name or place is likely to be mispronounced, respell it phonetically with hyphenated syllables and the stressed syllable in CAPS if helpful — but test the original first and only respell the ones that actually break.

- `Yosemite` → "yo-SEM-it-ee".
- `Worcestershire` → "WUUS-ter-sher".
- `Nguyen` → "win" (or "NOO-yen", depending on the intended pronunciation).
- `GIF` → "jiff" or "ghiff" depending on which the user wants.

Respelling changes spelling only to fix sound; it never changes the word's meaning.

## Example

**Before:**
> In 2026, ~30% of U.S. drivers said they'd pay $3.50/gallon for gas, according to the CEO of AAA — a 15% jump vs. last year.

**After:**
> In twenty twenty-six, about thirty percent of United States drivers said they would pay three dollars and fifty cents per gallon for gas. That's according to the C E O of Triple A. It was a fifteen percent jump versus last year.

## Output format

- Return **only** the normalized script, as plain text.
- Keep the original paragraph structure (one blank line between paragraphs).
- No explanations, no notes, no list of the changes you made. Just the text, ready to paste straight into the TTS engine.
- If the script is long, still return the whole thing; the user will chunk it on input (many local TTS engines read best in chunks of roughly 1,000 characters or a few sentences at a time).

## A note on emotion / paralinguistic tags (default: off)

OmniVoice and some other engines support inline paralinguistic tags placed directly in the text, like `[laughter]` or `[sigh]`, plus question-intonation control. **By default, do not insert these tags.** They often backfire on serious narration (health, documentary, educational, spiritual). Add them only when the user explicitly asks and confirms their engine supports them.
