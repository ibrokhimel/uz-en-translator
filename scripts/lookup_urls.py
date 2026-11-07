#!/usr/bin/env python3
"""Print dictionary lookup URLs for a word.

Usage:
  python lookup_urls.py <uzbek word>        # Uzbek word
  python lookup_urls.py <english word> --en # English word

Open izoh.uz and savodxon.uz in a real browser (they need JavaScript).
"""
import argparse
import sys
from urllib.parse import quote

APOS = "'‘’`´ʻʼ"


def site_form(word, okina, tutuq):
    """Write oʻ/gʻ and the tutuq belgisi with the characters a site expects."""
    out = []
    for i, ch in enumerate(word):
        if ch in APOS:
            prev = word[i - 1].lower() if i else ""
            out.append(okina if prev in "og" else tutuq)
        else:
            out.append(ch)
    return "".join(out)


# Tested 2026-11-07:
#   izoh.uz     oʻ/gʻ = U+2018 ‘, tutuq = U+02BC ʼ  (bog%E2%80%98, ma%CA%BCno)
#   sinonim.uz  oʻ/gʻ = U+2018 ‘, tutuq = U+2019 ’  (bog%E2%80%98, ma%E2%80%99no)
def izoh_form(word):
    return site_form(word, "‘", "ʼ")


def sinonim_form(word):
    return site_form(word, "‘", "’")


def standard_form(word):
    # official: oʻ/gʻ -> U+02BB, tutuq -> U+02BC
    return site_form(word, "ʻ", "ʼ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("word")
    ap.add_argument("--en", action="store_true", help="the word is English")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    w = a.word.strip()
    if a.en:
        print("Wiktionary (EN):  https://en.wiktionary.org/wiki/" + quote(w))
        print("Glosbe EN->UZ:    https://glosbe.com/en/uz/" + quote(w))
        print("Cambridge:        https://dictionary.cambridge.org/dictionary/english/" + quote(w))
    else:
        print("izoh.uz:          https://izoh.uz/word/" + quote(izoh_form(w).lower()))
        print("savodxon.uz:      https://savodxon.uz/izoh?" + quote(standard_form(w).lower())
              + "  (read with javascript_tool after ~2.5 s)")
        print("sinonim.uz:       https://sinonim.uz/words/" + quote(sinonim_form(w).lower())
              + "  (plain fetch works; results in Cyrillic)")
        print("Wiktionary (UZ):  https://en.wiktionary.org/wiki/" + quote(standard_form(w)))
        print("Glosbe UZ->EN:    https://glosbe.com/uz/en/" + quote(standard_form(w)))


if __name__ == "__main__":
    main()
