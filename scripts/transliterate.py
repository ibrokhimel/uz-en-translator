#!/usr/bin/env python3
"""Transliterate Uzbek between Latin and Cyrillic script.

Usage:
  python transliterate.py --to cyrillic [FILE]
  python transliterate.py --to latin [FILE]
  (no FILE: read stdin; output to stdout)

Leaves code, URLs, emails, {placeholders} and HTML tags untouched.
Known limits (review by hand):
  - Latin "ts" stays т+с (otsiz = отсиз), so loanwords like konsert need ц.
  - Foreign names and brands are transliterated too; restore them if needed.
"""
import argparse
import re
import sys

PROTECT = re.compile(
    r"```.*?```|(?<!\w)`[^`\n]+`(?!\w)|https?://\S+|www\.\S+|[\w.+-]+@[\w-]+\.[\w.]+"
    r"|\{[^{}\n]*\}|<[^<>\n]+>",
    re.S,
)
APOS = "'‘’`´ʻʼ"
VOWELS_LAT = set("aeiouAEIOU")
VOWELS_CYR = set("аеёиоуэюяўАЕЁИОУЭЮЯЎ")

# ---------- Latin -> Cyrillic ----------
L2C_DI = {
    "sh": "ш", "ch": "ч", "yo": "ё", "yu": "ю", "ya": "я",
}
L2C = {
    "a": "а", "b": "б", "d": "д", "f": "ф", "g": "г", "h": "ҳ", "i": "и",
    "j": "ж", "k": "к", "l": "л", "m": "м", "n": "н", "o": "о", "p": "п",
    "q": "қ", "r": "р", "s": "с", "t": "т", "u": "у", "v": "в", "x": "х",
    "y": "й", "z": "з", "c": "ц", "w": "в",
}


def case_like(src, out):
    if src.isupper() and (len(src) > 1 or len(out) == 1):
        return out.upper()
    if src[0].isupper():
        return out[0].upper() + out[1:]
    return out


def lat_to_cyr_word(w):
    res, i, n = [], 0, len(w)
    while i < n:
        ch = w[i]
        lo = ch.lower()
        nxt = w[i + 1] if i + 1 < n else ""
        prev = w[i - 1] if i > 0 else ""
        at_start = i == 0 or not w[i - 1].isalpha()
        after_vowel = prev in VOWELS_LAT
        # oʻ / gʻ
        if lo in "og" and nxt and nxt in APOS:
            src = w[i:i + 2]
            out = "ў" if lo == "o" else "ғ"
            res.append(out.upper() if ch.isupper() else out)
            i += 2
            continue
        # tutuq
        if ch in APOS:
            res.append("ъ")
            i += 1
            continue
        pair = w[i:i + 2]
        lp = pair.lower()
        if lp == "ye":
            if at_start or after_vowel:
                res.append(case_like(pair, "е"))
            else:
                res.append(case_like(pair, "ъе"))
            i += 2
            continue
        if lp in L2C_DI and len(pair) == 2:
            res.append(case_like(pair, L2C_DI[lp]))
            i += 2
            continue
        if lo == "e":
            out = "э" if (at_start or after_vowel) else "е"
            res.append(out.upper() if ch.isupper() else out)
            i += 1
            continue
        if lo in L2C:
            out = L2C[lo]
            res.append(out.upper() if ch.isupper() else out)
        else:
            res.append(ch)
        i += 1
    s = "".join(res)
    # all-caps word: make every letter upper
    if w.isupper() and len(w) > 1:
        s = s.upper()
    return s


# ---------- Cyrillic -> Latin ----------
C2L = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ё": "yo", "ж": "j",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n",
    "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f",
    "х": "x", "ч": "ch", "ш": "sh", "щ": "sh", "ы": "i", "э": "e",
    "ю": "yu", "я": "ya", "ў": "oʻ", "қ": "q", "ғ": "gʻ", "ҳ": "h",
}


def cyr_to_lat_word(w):
    res, n = [], len(w)
    all_caps = w.isupper() and len(w) > 1
    for i, ch in enumerate(w):
        lo = ch.lower()
        prev = w[i - 1].lower() if i > 0 else ""
        nxt = w[i + 1].lower() if i + 1 < n else ""
        at_start = i == 0 or not w[i - 1].isalpha()
        if lo == "е":
            out = "ye" if (at_start or prev in VOWELS_CYR or prev in "ъь") else "e"
        elif lo == "ц":
            out = "ts" if prev in VOWELS_CYR else "s"
        elif lo == "ъ":
            out = "" if nxt in "еёюя" else "ʼ"
        elif lo == "ь":
            out = ""
        elif lo in C2L:
            out = C2L[lo]
        else:
            res.append(ch)
            continue
        if out and ch.isupper():
            out = out.upper() if all_caps else out[0].upper() + out[1:]
        res.append(out)
    return "".join(res)


WORD_LAT = re.compile(r"[A-Za-z" + re.escape(APOS) + r"]+")
WORD_CYR = re.compile(r"[Ѐ-ӿ]+")


def convert(text, to):
    fn = (lambda m: lat_to_cyr_word(m.group(0))) if to == "cyrillic" \
        else (lambda m: cyr_to_lat_word(m.group(0)))
    rx = WORD_LAT if to == "cyrillic" else WORD_CYR
    out, pos = [], 0
    for m in PROTECT.finditer(text):
        out.append(rx.sub(fn, text[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(rx.sub(fn, text[pos:]))
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--to", required=True, choices=["cyrillic", "latin"])
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.file:
        with open(a.file, encoding="utf-8") as f:
            src = f.read()
    else:
        sys.stdin.reconfigure(encoding="utf-8")
        src = sys.stdin.read()
    sys.stdout.write(convert(src, a.to))


if __name__ == "__main__":
    main()
