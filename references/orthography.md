# Uzbek orthography

## Latin alphabet (official)
A a, B b, D d, E e, F f, G g, H h, I i, J j, K k, L l, M m, N n, O o, P p, Q q, R r, S s, T t, U u, V v, X x, Y y, Z z, Oʻ oʻ, Gʻ gʻ, Sh sh, Ch ch, ng, and the tutuq belgisi ʼ.

There is no c, w as native letters (only in foreign names). *ts* appears in loanwords.

Savodxon also offers a "new Latin" (*yangi lotin*) option. It reflects a proposed reform that is not the standard in use. Do not use it unless the user explicitly asks.

## The apostrophe characters — the most common error

| Use | Character | Code point | Example |
|---|---|---|---|
| oʻ, gʻ (modifier) | ʻ | U+02BB MODIFIER LETTER TURNED COMMA | *oʻzbek*, *bogʻ* |
| tutuq belgisi (glottal stop) | ʼ | U+02BC MODIFIER LETTER APOSTROPHE | *maʼno*, *sanʼat*, *taʼlim* |

Wrong but common: `'` (U+0027), `‘` (U+2018), `’` (U+2019), `` ` `` (U+0060), `´` (U+00B4). They break search, sorting, hyphenation and spell-checkers.

`scripts/normalize.py` converts all of these: after o/O/g/G → ʻ; between other letters → ʼ.

Exception: when the user explicitly wants plain ASCII (old systems, SMS, filenames), use `'` and say so.

Note: izoh.uz URLs use `‘` (U+2018) for oʻ/gʻ (e.g. `izoh.uz/word/so%E2%80%98rat`). `scripts/lookup_urls.py` handles this.

## Common spelling traps
- *-gi / -ki / -qi* suffix: *uydagi*, *ertangi*, *tashqi*.
- Doubled consonants are kept: *katta*, *ikki*, *tayyor*, *amma*.
- *i* vs *u* in suffixes follows standard forms, not pronunciation: *kitobim* (not *kitobum*).
- Verb + *-moq*, *-ish*: *oʻqimoq*, *oʻqish*.
- Hyphen in paired words: *ota-ona*, *qora-qura*; and before *chi*, *a*, *ku*, *da* particles only in specific cases — when unsure, check savodxon.uz.
- Loanwords follow established Uzbek spelling, not English or Russian: *kompyuter*, *feyk*, *startap*, *menejer*.

## Cyrillic ↔ Latin mapping
| Cyrillic | Latin | Notes |
|---|---|---|
| А Б В Г Д | A B V G D | |
| Е | Ye / E | *Ye* at word start and after a vowel, ъ or ь; *e* elsewhere |
| Ё | Yo | |
| Ж | J | |
| З И Й | Z I Y | |
| К Л М Н О П Р С Т У Ф | K L M N O P R S T U F | |
| Х | X | |
| Ҳ | H | |
| Ц | S / Ts | *s* at word start and after a consonant, *ts* after a vowel |
| Ч | Ch | |
| Ш | Sh | |
| Ъ | ʼ | dropped before е, ё, ю, я (*объект* → *obyekt*) |
| Ь | — | dropped |
| Э | E | |
| Ю | Yu | |
| Я | Ya | |
| Ў | Oʻ | |
| Қ | Q | |
| Ғ | Gʻ | |

Latin → Cyrillic direction: *e* at word start or after a vowel → **Э**, else **Е**; *ye* at word start or after a vowel → **Е**, after a consonant → **ъе**. *ts* is ambiguous (*otsiz* = **отсиз**, but *konsert* = **концерт**), so `transliterate.py` keeps т+с: review loanwords by hand.
