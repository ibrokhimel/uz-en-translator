#!/usr/bin/env python3
"""Normalize Uzbek Latin orthography.

Fixes:
  - o'/g' written with ' ‘ ’ ` ´ ʼ ′  ->  oʻ / gʻ  (U+02BB)
  - tutuq belgisi between letters      ->  ʼ       (U+02BC)
  - Cyrillic look-alike letters inside Latin words -> Latin letters

Leaves alone: fenced and inline code, URLs, emails, {placeholders}, %s-style
format specifiers, HTML tags, and English apostrophe words (don't, app's,
you're, I'm, o'clock, O'Brien), so mixed English/Uzbek text is safe.

  --include-inline-code  also fix `inline code` (when its text was translated)

Usage:
  python normalize.py [FILE] [--check] [--in-place]
  (no FILE: read stdin)
  --check     only report problems; exit code 1 if any found
  --in-place  rewrite FILE
"""
import argparse
import re
import sys

OKINA = "ʻ"   # ʻ  for oʻ gʻ
TUTUQ = "ʼ"   # ʼ  tutuq belgisi
APOS = "'‘’`´ʻʼ′ʹ"

PROTECT = re.compile(
    r"```.*?```"                      # fenced code
    r"|(?<!\w)`[^`\n]+`(?!\w)"        # inline code (not a backtick typed as oʻ)
    r"|https?://\S+|www\.\S+"         # URLs
    r"|[\w.+-]+@[\w-]+\.[\w.]+"       # emails
    r"|\{[^{}\n]*\}"                  # {placeholders}
    r"|%[-+ #0]*\d*(?:\.\d+)?[sdifxXeEgGcr%]"  # %s format specs
    r"|<[^<>\n]+>",                   # HTML tags
    re.S,
)

# Cyrillic letters that look like Latin ones
HOMOGLYPHS = {
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y",
    "к": "k", "м": "m", "т": "t", "н": "h", "в": "b", "і": "i",
    "А": "A", "Е": "E", "О": "O", "Р": "P", "С": "C", "Х": "X", "У": "Y",
    "К": "K", "М": "M", "Т": "T", "Н": "H", "В": "B", "І": "I",
}
CYR = re.compile(r"[Ѐ-ӿ]")
LAT = re.compile(r"[A-Za-z]")
WORD = re.compile(r"[\w" + re.escape(APOS) + r"]+")

OG_RE = re.compile(r"([oOgG])[" + re.escape(APOS) + r"]")
TUTUQ_RE = re.compile(
    r"(?<=[^\W\doOgG_])[" + re.escape(APOS) + r"](?=[^\W\d_])"
)


# English words whose apostrophes must stay plain: contractions/possessives
# (don't, app's, you're, we've, I'll, she'd, I'm), o'clock, O'Brien.
ENGLISH_APOS = re.compile(
    r"\b(?:[A-Za-z]+n['’]t"
    r"|[A-Za-z]+['’](?:s|re|ve|ll|d)"
    r"|I['’]m"
    r"|[oO]['’]clock"
    r"|O['’][A-Z][a-z]+)\b"
)


def fix_segment(text, stats):
    # Shield English apostrophe words, fix the rest, then restore them.
    shielded = []

    def shield(m):
        shielded.append(m.group(0))
        return "\x00%d\x00" % (len(shielded) - 1)

    text = ENGLISH_APOS.sub(shield, text)

    def og(m):
        if m.group(0)[1] != OKINA:
            stats["okina"] += 1
        return m.group(1) + OKINA

    text = OG_RE.sub(og, text)

    def tq(m):
        if m.group(0) != TUTUQ:
            stats["tutuq"] += 1
        return TUTUQ

    text = TUTUQ_RE.sub(tq, text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: shielded[int(m.group(1))], text)

    def mixed(m):
        w = m.group(0)
        if CYR.search(w) and LAT.search(w):
            fixed = "".join(HOMOGLYPHS.get(ch, ch) for ch in w)
            if fixed != w:
                stats["homoglyph"] += 1
                if CYR.search(fixed):
                    stats["mixed_unfixed"].append(w)
                return fixed
            stats["mixed_unfixed"].append(w)
        return w

    return WORD.sub(mixed, text)


# Inline code that reads as plain words (e.g. `5 daqiqa`): letters, digits,
# spaces, basic punctuation, apostrophes only *inside* words. Anything with
# quotes around words, $ / \ = ( ) [ ] { } | ; < > " or - flags is treated as
# real code and left alone.
READABLE_INLINE = re.compile(
    r"`(?:[^\W_]+(?:[" + re.escape(APOS) + r"][^\W_]+)*[.,!?:]?\s*)+`"
)


def readable_inline(span):
    return bool(READABLE_INLINE.fullmatch(span))


def normalize(text, include_inline_code=False):
    stats = {"okina": 0, "tutuq": 0, "homoglyph": 0, "mixed_unfixed": []}
    out, pos = [], 0
    for m in PROTECT.finditer(text):
        span = m.group(0)
        if include_inline_code and span.startswith("`") and not span.startswith("```") \
                and readable_inline(span):
            continue  # translated readable text in backticks: fix like normal text
        out.append(fix_segment(text[pos:m.start()], stats))
        out.append(m.group(0))
        pos = m.end()
    out.append(fix_segment(text[pos:], stats))
    return "".join(out), stats


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--in-place", action="store_true")
    ap.add_argument("--include-inline-code", action="store_true",
                    help="also fix `single backtick` spans that read as plain words "
                         "(e.g. `5 daqiqa`); real code like `echo 'go'` is still skipped")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    if a.file:
        with open(a.file, encoding="utf-8") as f:
            src = f.read()
    else:
        sys.stdin.reconfigure(encoding="utf-8")
        src = sys.stdin.read()

    fixed, s = normalize(src, a.include_inline_code)
    report = (f"oʻ/gʻ fixed: {s['okina']}, tutuq fixed: {s['tutuq']}, "
              f"look-alike words fixed: {s['homoglyph']}")
    if s["mixed_unfixed"]:
        report += "; mixed-script words to check by hand: " + ", ".join(s["mixed_unfixed"])

    if a.check:
        print(report)
        # name each changed word with its line number
        for n, (old, new) in enumerate(zip(src.splitlines(), fixed.splitlines()), 1):
            if old != new:
                for wo, wn in zip(old.split(), new.split()):
                    if wo != wn:
                        print(f"  line {n}: {wo} -> {wn}")
        sys.exit(1 if fixed != src or s["mixed_unfixed"] else 0)
    if a.in_place and a.file:
        with open(a.file, "w", encoding="utf-8", newline="") as f:
            f.write(fixed)
    else:
        sys.stdout.write(fixed)
    print(report, file=sys.stderr)


if __name__ == "__main__":
    main()
