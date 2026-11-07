# Dictionary lookup sources

Use these to verify word choices. Look up only "hard" words (see SKILL.md step 4).

## Contents
- Which site for what
- Fallback order when a word is missing
- Dictionary limits (old dictionary, homonyms, cross-references, verbal nouns)
- Browser rules
- URL patterns
- Reading an izoh.uz entry
- Recording results

## Which site for what

| Need | Site | Access |
|---|---|---|
| Does this Uzbek word mean what I think? Which sense? Usage examples | **izoh.uz** — explanatory dictionary based on *Oʻzbek tilining izohli lugʻati* (2006–2008) | Browser only |
| Same definitions plus newer words; root of an inflected word | **savodxon.uz/izoh** — 2.5M word forms, splits words into root + suffixes; accepts Latin or Cyrillic | Browser only (entry drawn by JavaScript) |
| Spell-check a whole Uzbek text | **savodxon.uz** home page editor ("Tahrir") | Browser; sends text to the site — non-confidential text only |
| Synonyms, register choice | **sinonim.uz** | Plain fetch works; results in Cyrillic |
| Cyrillic spelling | **lotin.uz** (also linked from izoh.uz entries) | Browser or fetch |
| English ↔ Uzbek equivalents | **en.wiktionary.org**, **uz.wiktionary.org** | Fetch works; many gaps |
| English ↔ Uzbek equivalents, example sentences | **glosbe.com** (`/en/uz/<word>`, `/uz/en/<word>`) | Fetch works; many gaps |
| Meaning of an English word (to pick the right sense before translating) | Cambridge, Merriam-Webster, Wiktionary | Fetch works |

izoh.uz, savodxon.uz and sinonim.uz are monolingual Uzbek. They confirm the Uzbek side; they do not give English translations.

**When no bilingual source has the word** (common for culture-bound words like *andisha*): read the izoh.uz senses, translate the definition into English yourself, then pick the English word or short phrase that covers it. Check that English word in an English dictionary. Say in the notes that the English equivalent was derived from the Uzbek definition.

## Fallback order when a word is missing
izoh.uz returns **HTTP 410** for words it lacks (seen: *hamjamiyat*, *baribir*, *mehr-oqibat*). Then:
1. **savodxon.uz** (`https://savodxon.uz/izoh?<word>`) — same base dictionary plus newer words. For a word with no definition it still confirms spelling, syllables and part of speech (*ot*, *yordamchi soʻz*…).
2. **Paired or compound words** (*mehr-oqibat*, *ota-ona*): look up each half (*oqibat*).
3. **Inflected form**: strip suffixes and look up the root.
4. Still nothing: use your own knowledge, mark the term "unverified" in translator notes.

## Dictionary limits
- **Old dictionary, missing modern senses.** izoh.uz (and savodxon's definitions) come from a 2006–2008 dictionary. Tech and recent senses are often missing: *ilova* = app, *sayt*, *obuna* = subscription, *post*, *kontent*. A missing modern sense is **not** a reason to reject a word that is in wide current use. Reject only when the dictionary shows a sense that conflicts with yours (like *klinika* = specialised teaching hospital) or marks the word as archaic, colloquial or dialect.
- **Homonyms.** Entries can have several homonyms marked *(i)*, *(ii)* (e.g. *bogʻ* garden / *bogʻ* bundle; *qor* snow / *qor-* verb). Check every homonym and pick the one with the right part of speech; savodxon may show the verb first. On izoh.uz the second homonym comes after all of the first one's phrases, so a shortened `get_page_text` can cut it off. List every homonym with `javascript_tool`:
  ```js
  [...document.querySelectorAll('[id^="def-"]')].map(e => e.innerText.replace(/\s+/g, ' ').slice(0, 300))
  ```
  One array item per homonym.
- **Cross-reference entries.** An entry may say only "toʻgʻrisi X" (the correct form is X) or "qarang: X" (see X). Follow it and look up X. Two-word forms often 410; look up the headword (*qorbobo*, or each word).
- **Verbal nouns.** Many *-(i)sh / -lish* nouns are listed only under the verb, without the noun sense you need (*yigʻilish* "meeting" → see *yigʻil-* "gather"). Look up the verb stem and derive the noun sense; confirm the noun use with sinonim.uz or your own knowledge.

## Browser rules
- izoh.uz serves a JavaScript cookie check to non-browsers (HTTP 403). Open it in the built-in browser pane (`mcp__Claude_Browser__navigate` then `get_page_text`) or Claude in Chrome. Do not fake cookies or headers to get around the check.
- If the browser pane cannot reach a site (e.g. `ERR_QUIC_PROTOCOL_ERROR`), retry once, then skip the site and mark the term as unverified.
- Single-word lookups send nothing sensitive. Pasting the user's full text into a website does — ask first if the text might be private.

## URL patterns
Run `python scripts/lookup_urls.py <word>` (Uzbek word) or `python scripts/lookup_urls.py <word> --en` (English word) to print ready URLs.

Each site spells the apostrophes differently in its addresses (tested 2026-11-07); `lookup_urls.py` handles this:

| Site | oʻ / gʻ | tutuq ʼ |
|---|---|---|
| izoh.uz | `‘` U+2018 (`bog%E2%80%98`) | `ʼ` U+02BC (`ma%CA%BCno`) |
| sinonim.uz | `‘` U+2018 | `’` U+2019 (`ma%E2%80%99no`) |
| savodxon.uz | `ʻ` U+02BB (official) | `ʼ` U+02BC |

- izoh.uz: `https://izoh.uz/word/<word>`. If the direct URL 404s or 410s, see "Fallback order".
- savodxon.uz: `https://savodxon.uz/izoh?<word>` (Latin or Cyrillic). `savodxon.uz/izoh/<word>` is a 404. The entry is drawn by JavaScript, so `get_page_text` can miss it. Read it with `mcp__Claude_Browser__javascript_tool`:
  ```js
  await new Promise(r => setTimeout(r, 2500)); document.body.innerText.replace(/\s+/g, ' ').slice(0, 2000)
  ```
  If the result has no entry (only the search-box text), run it again with a 4000 ms wait before giving up.
  For an inflected word it shows the split (*kitob · lar · imiz · dan* with case names), but the definition shown may be wrong (it labelled *kitoblarimizdan* a toponym). Take the root from the split and look the root up again.
- sinonim.uz: `https://sinonim.uz/words/<word>` — plain fetch works. Verbs are listed **with *-moq*** (*oʻqimoq*, *yugurmoq*), unlike izoh.uz's bare stems; the bare stem returns 404. The page is in Cyrillic: the synonym list follows "синонимлари". Transliterate with `scripts/transliterate.py --to latin` if needed.
- Wiktionary: `https://en.wiktionary.org/wiki/<word>` (look for the "Uzbek" section).
- Glosbe: `https://glosbe.com/en/uz/<word>`, `https://glosbe.com/uz/en/<word>`.

## Reading an izoh.uz entry
An entry shows: the headword, part of speech (*ot* noun, *feʼl* verb, *sifat* adjective, *ravish* adverb), numbered senses, and example sentences with author and source.
- Match your intended meaning to a numbered sense. If none matches, the word is probably wrong — try a synonym (but see "Dictionary limits" for modern senses).
- Labels like *eskirgan* (archaic), *soʻzlashuv* (colloquial), *kitobiy* (bookish), *dial.* (dialect) tell you the register. Avoid archaic and dialect words in neutral web text.
- Entries list verbs as bare stems (*kisirlat*, *abadiylashtir*), so search *oʻqi*, not *oʻqimoq*.
- The "Next/Previous 10 words" lists show derived words (*kitob* → *kitobxon*, *kitobxona*) — useful for finding the exact derived form you need.

## Recording results
After a lookup confirms a non-obvious choice, add it to the "Confirmed terms" table in `references/glossary-general.md`.
