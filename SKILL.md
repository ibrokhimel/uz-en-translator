---
name: uz-en-translator
description: Translate text between English and Uzbek (both directions) with native-quality meaning, correct Uzbek Latin orthography (oʻ, gʻ, ʼ), and dictionary-verified word choices from izoh.uz, savodxon.uz and other sources. Use this skill whenever the user wants anything translated, localized, adapted, proofread or checked between English and Uzbek — articles, posts, messages, documents, captions, single words or phrases — even if they don't say "translate" (e.g. "oʻzbekchaga oʻgir", "inglizchaga tarjima qil", "how do I say this in Uzbek", "what does this Uzbek word mean", "is this Uzbek text correct", "convert to Cyrillic Uzbek"). Also use it when reviewing or fixing an existing Uzbek translation.
---

# English ↔ Uzbek Translator

Goal: a translation a native reader would not notice is a translation. Meaning first, then natural Uzbek (or English) structure, then exact orthography.

Machine-style Uzbek fails in predictable ways: wrong apostrophes in oʻ/gʻ, English word order kept, Russian loanwords where a native word exists, plural after numbers, inconsistent siz/sen, over-literal idioms. This skill exists to prevent those. Uzbek→English fails differently: dropped subjects, wrong gender for "u", lost evidential nuance (-ekan, -ibdi), honorific plurals read as real plurals.

## Defaults

- **Uzbek script:** official Latin alphabet. Cyrillic only when the user asks or writes in Cyrillic. For Cyrillic output, translate in Latin first, then run `scripts/transliterate.py --to cyrillic` and review the result.
- **Register:** match the source tone. Formal/neutral source → *siz*, literary vocabulary. Casual source → conversational vocabulary, still *siz* unless the source is clearly friend-to-friend, a child, or slang where *sen* is natural. Keep one register through the whole text. Example: casual "Don't give up — the ball is in your court!" → *Boʻsh kelmang — endi navbat sizda!* (preferred by the user in testing over the *sen* version).
- **Dialect:** standard literary Uzbek (Tashkent norm), not regional forms.
- **Domain:** general / web content. (Other domain glossaries are planned — see `ROADMAP.md`.)

## Workflow

### 1. Analyze the source
Decide: direction, text type (news, blog, message, caption…), audience, tone, and source script. Note names, brands, numbers, dates and anything that must not change.

### 2. Protect non-translatable parts
Keep exactly as-is: code, `{placeholders}`, `%s`, URLs, emails, HTML/markdown syntax, hashtags, product names, @handles. Translate link text and alt text, not the URL.

Inline code (`` `…` ``): keep identifiers, commands, file names, keys and values a program reads (`npm install`, `user_id`, `Ctrl+S`). Translate text a person reads that was only styled as code (`` `5 minutes` `` → `` `5 daqiqa` ``), keeping the backticks. When you translated any inline code, run normalize with `--include-inline-code` in step 6.

Suffixes after inline code: never attach a suffix to the code itself. Add a noun that takes it: `` `npm install` buyrugʻini ``, `` `config.json` faylini ``, `` `Ctrl+S` tugmalarini ``.

Suffixes after markup or brand names: prefer a postposition that avoids splitting the markup (*ilovani **App Store** orqali yuklab oling*). If a suffix is needed, put it right after the closing marker (***App Store**dan*), never inside it.

### 3. Draft by meaning
Read the whole sentence (or paragraph) before translating any of it. Then rebuild it in the target language's own structure. Read `references/grammar-pitfalls.md` for the direction you are translating — it lists the structural rewrites (SOV order, participial clauses, number + singular noun, subject dropping, evidentials) that make the biggest quality difference. Idioms: check `references/idioms.md`; translate the meaning, never word-for-word.

### 4. Verify hard words with dictionaries
Look up only words where a wrong choice is likely — not every word. A word is "hard" when it is:
- polysemous and the sense matters (*challenge, issue, deliver, experience*),
- rare, technical, archaic or a neologism,
- an Uzbek word you are not fully sure of (meaning, spelling or register),
- a Russian/English loanword that may have a better native Uzbek equivalent,
- an idiom or fixed phrase.

Budget: about 10 lookups per text; for a single word or phrase request, look it up thoroughly. Read `references/lookup-sources.md` for which site to use, how to build lookup URLs (`scripts/lookup_urls.py`), and how to read the results. Key points:
- izoh.uz and savodxon.uz are **Uzbek-only** dictionaries: use them to confirm that the Uzbek word you chose really means what you intend, and to see real usage examples. For the English side, use Wiktionary or Glosbe.
- izoh.uz and savodxon.uz's search need a real browser (the built-in browser pane, or Claude in Chrome). Plain fetch/curl is blocked by a bot check — do not try to get around it; use the browser.
- Look up the dictionary form: nouns without suffixes (*kitob*, not *kitoblarimizdan*), verbs as the bare stem (*oʻqi*, not *oʻqimoq*). savodxon.uz splits inflected words into root + suffixes.
- izoh.uz returns HTTP 410 for missing words. Fall back to savodxon.uz, then to each half of a paired word, then the root (`references/lookup-sources.md` → "Fallback order").
- Watch for a narrower dictionary sense than you assumed: *klinika* is a specialised teaching/research hospital, not any clinic. When the dictionary sense conflicts with yours, change the word — that is the whole point of the lookup.
- But the dictionary is from 2006–2008: modern senses are often simply missing (*ilova* = app, *obuna* = subscription). A missing sense is not a conflict; keep a word that is in wide current use. See "Dictionary limits" in `references/lookup-sources.md` for homonyms, cross-references and verbal nouns.
- If a site is down or blocks you, continue without it and mark the term as unverified in the notes.

### 5. Self-review
Re-read the target text alone, as a native reader would, then against the source:
- Nothing added, dropped or changed in meaning; numbers, names and negations intact.
- Natural word order and sentence length (split long English sentences).
- One register throughout; one term per concept throughout.
- Native word preferred over Russian loanword where both are normal (`references/style-guide.md`).
- Formatting conventions: numbers, dates, quotes, capitalization (`references/style-guide.md`).

### 6. Normalize orthography (Uzbek output)
Run `python scripts/normalize.py <file>` (or pipe text on stdin) on the final Uzbek text. It fixes oʻ/gʻ to U+02BB, tutuq belgisi to U+02BC, and Cyrillic look-alike letters hidden in Latin words, while leaving code, URLs, placeholders and English apostrophe words (*don't, app's, o'clock*) alone. Use `--check` to only report, `--include-inline-code` when inline code was translated. Details in `references/orthography.md`.

Run it on Uzbek text only. For English output (UZ → EN) skip this step; if translator notes quote Uzbek words, make sure those use ʻ and ʼ.

Optional, for important texts: spell-check on savodxon.uz's free web editor in the browser. That sends the text to a third-party site, so do it only for non-confidential text or with the user's OK.

### 7. Deliver
Output the translation first. Then, only when useful, a short **Translator notes** section:
- terms verified, with the source (e.g. "*dolzarb* — confirmed on izoh.uz, sense 1"),
- terms that could not be verified,
- real ambiguities and the choice made (e.g. "*u* → *she*, from context"),
- cultural adaptations (idioms replaced, units or formats changed).

Skip notes for short, unambiguous texts. If the user wants only the translation, give only the translation.

## Other request types

### "Is this translation correct?" (review)
1. Translate the source yourself first (steps 1–4), without looking at the given translation, so it doesn't bias you.
2. Compare. Classify each problem: **meaning** (wrong, added, missing), **grammar** (word order, agreement, calque like *qaysiki*, reason marked twice), **word choice / register**, **orthography** (run `normalize.py --check`; it lists each wrong word with its line). Separate real **errors** from **style suggestions** (e.g. *koʻp talabalar* is common, *koʻp talaba* more careful — a suggestion, see grammar-pitfalls §4).
3. Answer: a one-line verdict (correct / mostly correct / incorrect), the list of problems with short reasons, then the corrected version. Keep the original's good choices; change only what is wrong. If it is correct, say so and stop — don't rewrite for taste.

### "What does this word mean?" (word or phrase question)
1. Look it up thoroughly (no 10-lookup budget): izoh.uz senses and register labels, savodxon.uz for the root if inflected, sinonim.uz for near-synonyms, a bilingual source if one has it.
2. Answer: the main English equivalent(s), each numbered sense with an English gloss, one short example per main sense (Uzbek + English), register or cultural notes, and when the English words don't fit (e.g. *andisha* has no single English equivalent; it ranges from "tact" to "modesty").
3. Name the sources. If the English equivalent was derived from the Uzbek definition (no bilingual entry), say so.

## Remembering confirmed terms
When a lookup confirms a non-obvious term choice, add a row to the "Confirmed terms" table in `references/glossary-general.md` (term, chosen translation, sense, source, date). Check that table before looking a word up again. This keeps terminology consistent across sessions.

## Reference files
- `references/grammar-pitfalls.md` — structural rewrites, both directions. Read for every translation longer than a sentence.
- `references/style-guide.md` — register, loanwords, numbers, dates, punctuation, capitalization.
- `references/orthography.md` — Latin alphabet, apostrophe characters, Cyrillic mapping.
- `references/lookup-sources.md` — dictionary sites, URL patterns, how to read entries.
- `references/idioms.md` — idiom equivalents both directions.
- `references/glossary-general.md` — tricky general terms + confirmed-terms log.

## Scripts
- `scripts/normalize.py` — fix Uzbek Latin orthography (`--check` to report only, `--include-inline-code` for translated inline code).
- `scripts/transliterate.py --to cyrillic|latin` — Latin ↔ Cyrillic Uzbek.
- `scripts/lookup_urls.py <word> [--en]` — print dictionary lookup URLs for a word.

All scripts read a file path argument or stdin, write UTF-8 to stdout, and need only Python 3.
