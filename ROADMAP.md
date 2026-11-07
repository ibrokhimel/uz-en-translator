# Roadmap — future development

Version 1 covers general / web content. Planned additions:

## Domain glossaries
Each becomes its own `references/glossary-<domain>.md`, plus a line in SKILL.md telling Claude when to read it.

- **Business / legal** — contracts, official letters, government documents. Formal register, fixed legal phrasing (*shartnoma*, *tomonlar*, *majburiyat*), official document formats, rules for names in passports and legal text.
- **Tech / software UI** — app strings, docs, IT terms. Placeholder safety (`{name}`, `%s`, ICU plurals), string length limits, imperative button labels (*Saqlash*, *Bekor qilish*), consistent UI terminology.
- **Marketing / social** — ads, posts, slogans. Transcreation instead of literal translation, brand voice, hashtags, the *sen*/*siz* choice for brand tone, character limits.
- Later candidates: medical, academic, subtitles (timing and line length).

## Tooling
- **Savodxon API** (optional, paid): `/spellcheck`, `/suggestions`, `/convert` for automatic spell-checking without the browser. Needs an API key kept outside the skill folder (environment variable).
- **check.py**: flag Russian loanwords from the style-guide table, plural after numbers, untranslated English words.
- Better `ts` → `ц` handling in `transliterate.py` using a loanword list.

## Quality
- Eval set: 10–20 real texts (both directions) with checks for orthography, meaning and naturalness; reviewed by a native speaker.
- Description tuning so the skill triggers on Uzbek-language requests (*tarjima qil*, *oʻgir*).
- Grow `idioms.md` and the confirmed-terms log from real use.
