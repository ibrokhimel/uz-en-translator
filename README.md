# uz-en-translator

A [Claude](https://claude.com) skill for translating between **English and Uzbek** in both directions: meaning first, then natural sentence structure, then exact Uzbek orthography.

It targets the mistakes machine translation into Uzbek makes most often:

- wrong apostrophes in oʻ / gʻ and the tutuq belgisi ʼ
- English word order kept instead of Uzbek SOV order
- Russian loanwords where a native Uzbek word exists
- plural after numbers, inconsistent *siz / sen*
- word senses that look right but aren't (*klinika* ≠ any clinic)

Uzbek → English it handles dropped subjects, the genderless *u*, evidential forms (*-ibdi*, *ekan*), honorific plurals and patronymics.

## What it does

1. Translates by meaning, following a grammar and style guide for each direction.
2. Checks "hard" words in Uzbek dictionaries — [izoh.uz](https://izoh.uz), [savodxon.uz](https://savodxon.uz), [sinonim.uz](https://sinonim.uz) — plus Wiktionary and Glosbe for the English side.
3. Fixes orthography with a script (oʻ/gʻ → U+02BB, tutuq → U+02BC, hidden Cyrillic look-alike letters), leaving code, URLs, placeholders and English words alone.
4. Converts Latin ↔ Cyrillic Uzbek.
5. Also answers "is this translation correct?" and "what does this word mean?".
6. Keeps a glossary of confirmed terms so translations stay consistent.

Defaults: Latin script, register matched to the source, standard literary Uzbek, general / web content.

## Requirements

- Claude Code or the Claude desktop app (the skill uses scripts and a browser).
- Python 3 (standard library only).
- A browser tool for izoh.uz and savodxon.uz (the built-in browser pane, or Claude in Chrome). They block plain HTTP fetches; the skill does not try to get around that. Without a browser it still works, but marks dictionary checks as unverified.

## Install

Clone into your personal skills folder:

```bash
git clone https://github.com/ibrokhimel/uz-en-translator ~/.claude/skills/uz-en-translator
```

Then ask Claude things like "translate this into Uzbek", "oʻzbekchaga oʻgir", or "what does *andisha* mean?".

## Layout

```
SKILL.md                     workflow and rules
references/
  grammar-pitfalls.md        structural rewrites, both directions
  style-guide.md             register, loanwords, numbers, dates, UI strings, names
  orthography.md             alphabet, apostrophe characters, Cyrillic mapping
  lookup-sources.md          dictionary sites, URL formats, how to read entries
  idioms.md                  idiom equivalents
  glossary-general.md        tricky terms + confirmed-terms log
scripts/
  normalize.py               fix Uzbek Latin orthography
  transliterate.py           Latin <-> Cyrillic
  lookup_urls.py             dictionary links for a word
ROADMAP.md                   planned domains and tooling
```

## Scripts on their own

```bash
python scripts/normalize.py text.txt --check       # list orthography problems
python scripts/transliterate.py --to cyrillic text.txt
python scripts/lookup_urls.py "so'z"
```

## Status

Early version, tested on 18 sample sentences across three rounds. The idiom pairs and the loanword table have not yet been reviewed by a native speaker; corrections are welcome. See [ROADMAP.md](ROADMAP.md) for business/legal, tech and marketing glossaries.
