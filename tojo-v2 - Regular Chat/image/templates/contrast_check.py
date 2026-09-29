"""Verification: every text colour the system can put on every fill it can put
it on, checked against WCAG contrast. Run this after any palette edit.

Body text must clear 4.5:1. The page title is the only large-text exemption
(3:1), and it is checked at 4.5 anyway because it is cheap to keep.
"""

import sys

from tokens import THEMES

BODY, LARGE = 4.5, 3.0


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def lum(hexstr):
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(fg, bg):
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


# (text token, background token, minimum, what it is)
PAIRS = [
    ("h1", "canvas", LARGE, "page title"),
    ("sub", "canvas", BODY, "page subtitle"),
    ("caption", "canvas", BODY, "divider caption"),
    ("footer", "canvas", 3.0, "provenance footer"),

    ("proc_title", "proc_fill", BODY, "box title"),
    ("proc_value", "proc_fill", BODY, "box value"),
    ("caption", "proc_fill", BODY, "box caption"),
    ("state_outcome", "proc_fill", BODY, "outcome value text"),
    ("state_target", "proc_fill", BODY, "tag on a target box"),
    ("state_start", "proc_fill", BODY, "tag on a start box"),

    ("muted_title", "muted_fill", BODY, "muted box title"),
    ("muted_value", "muted_fill", BODY, "muted box value"),

    ("effect_label", "effect_fill", BODY, "effect box label"),
    ("effect_value", "effect_fill", BODY, "effect box value"),
    ("effect_cap", "effect_fill", BODY, "effect box caption"),

    # borders and rules are not text, but must still separate from the canvas
    ("proc_stroke", "canvas", 1.6, "process border on canvas"),
    ("divider", "canvas", 1.6, "dashed divider on canvas"),
    ("arrow", "canvas", 2.5, "arrow on canvas"),
]


def main():
    bad = 0
    for name, t in THEMES.items():
        print(f"\n{name}")
        for fg, bg, minimum, what in PAIRS:
            r = ratio(t[fg], t[bg])
            ok = r >= minimum
            bad += not ok
            print(f"  {'ok ' if ok else 'FAIL'} {r:5.2f} (min {minimum:.1f})  "
                  f"{what}: {fg} on {bg}")
    print(f"\n{bad} failure(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
