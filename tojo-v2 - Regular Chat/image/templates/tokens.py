"""Tojo image system v2 — design tokens.

Single source of truth for colour, type and spacing. No renderer may hard-code a
hex value or a font size; everything comes from here so a restyle is one edit.

Two themes, used in alternation across a conversation (see THEME_ORDER and
pick_theme). The semantic roles are identical in both themes — only the values
flip. In particular the effect/parameter box is always the tonal inverse of the
process box, so it reads as a different kind of object in either theme.
"""

# ---------------------------------------------------------------- type ------

FONT_STACK = "Poppins,'Segoe UI',Verdana,sans-serif"

# One variable drives box titles, box values, section labels and effect-box
# label/value together. Captions are the single exception and stay smaller.
BASE_SIZE = {"wide": 13, "tall": 16}

WEIGHT = {"h1": 700, "sub": 400, "title": 600, "value": 700,
          "label": 500, "caption": 400, "footer": 400}


class Scale:
    """Derived sizes. Never set a font size that is not on this object."""

    def __init__(self, base):
        self.s = base                       # titles, values, labels, effects
        self.h1 = round(base * 1.75)
        self.sub = round(base * 1.05)
        self.cap = max(10, round(base * 0.82))
        self.footer = max(9, round(base * 0.72))
        self.arrow = round(base * 1.35)


# ------------------------------------------------------------- geometry -----

CANVAS = {                      # default pixel size per ratio; may scale up
    "wide": (1000, 600),        # 5:3  desktop
    "tall": (900, 1200),        # 3:4  mobile
}
RATIO = {"wide": 5 / 3, "tall": 3 / 4}

MARGIN = {"wide": 40, "tall": 60}
CHAR_W = 0.60          # conservative average glyph width, as a fraction of size
BOX_PAD_X = 24         # combined internal horizontal padding before a line fits
BOX_PAD_Y = 10
RADIUS = 8
DASH = "5 4"

# --------------------------------------------------------------- colour -----

THEMES = {
    # ---- night: dark canvas, light process boxes, dark-on-light effect box --
    "night": {
        "canvas":        "#0f2740",
        "h1":            "#ffffff",
        "sub":           "#9fb8cf",
        "caption":       "#9fb8cf",
        "footer":        "#6d88a3",
        "divider":       "#3a5f84",
        "arrow":         "#7be0b8",

        "proc_fill":     "#1c3f61",
        "proc_stroke":   "#2c5580",
        "proc_title":    "#eaf1f8",
        "proc_value":    "#7be0b8",

        "muted_fill":    "#16324f",
        "muted_stroke":  "#244562",
        "muted_title":   "#93aec6",
        "muted_value":   "#93aec6",

        "effect_fill":   "#d9dde3",
        "effect_stroke": "#aab2bc",
        "effect_label":  "#0f2740",
        "effect_value":  "#7a4f00",
        "effect_cap":    "#43505e",

        "state_target":  "#ffb400",
        "state_outcome": "#ff8b82",
        "state_start":   "#7be0b8",
    },
    # ---- day: light canvas, white process boxes, light-on-dark effect box ---
    "day": {
        "canvas":        "#f1f5f9",
        "h1":            "#0f2740",
        "sub":           "#4d6076",
        "caption":       "#4d6076",
        "footer":        "#71839a",
        "divider":       "#a6b8cb",
        "arrow":         "#0c6b4f",

        "proc_fill":     "#ffffff",
        "proc_stroke":   "#b0c0d1",
        "proc_title":    "#0f2740",
        "proc_value":    "#0c6b4f",

        "muted_fill":    "#e4eaf1",
        "muted_stroke":  "#cfd9e4",
        "muted_title":   "#57687d",
        "muted_value":   "#57687d",

        "effect_fill":   "#0f2740",
        "effect_stroke": "#2c5580",
        "effect_label":  "#b9cee0",
        "effect_value":  "#f0b74a",
        "effect_cap":    "#9fb8cf",

        "state_target":  "#9a6205",
        "state_outcome": "#b7352b",
        "state_start":   "#0c6b4f",
    },
}
STATE_KEYS = ("plain", "target", "outcome", "start", "dashed")

THEME_ORDER = ("night", "day")


def pick_theme(graphic_index, continuity_of=None):
    """Which theme this graphic uses.

    graphic_index   0-based count of graphic-bearing SUBJECTS so far in this
                    conversation, not of files. Both files of one turn share a
                    theme, and a continuity redraw does not advance the count —
                    otherwise the graphic after the redraw inherits the redraw's
                    parity and two unrelated subjects end up on the same ground.
    continuity_of   the graphic_index of the earlier graphic this one redraws
                    (fill-in-the-blank -> filled, before -> after). Continuity
                    beats alternation: the redraw keeps the original theme,
                    because the point of it is that it is the same picture, now
                    answered.
    """
    idx = continuity_of if continuity_of is not None else graphic_index
    return THEME_ORDER[idx % len(THEME_ORDER)]


def theme(name):
    if name not in THEMES:
        raise KeyError(f"unknown theme {name!r}; have {list(THEMES)}")
    return THEMES[name]
