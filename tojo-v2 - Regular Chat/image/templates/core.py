"""Tojo image system v2 — renderer core.

Primitives every form renderer is built from. The rules a hand-drawn SVG has to
remember, this file enforces structurally:

  * every container is sized from its actual content, never from a constant
  * every wrap estimate carries a safety margin, and a single word too wide for
    its container raises at build time rather than clipping at render time
  * the page title and subtitle are wrapped against canvas width like any other
    text, and the layout below shifts to follow
  * one font-size variable drives titles, values, labels and effect boxes
  * content that overruns the canvas raises rather than clipping silently
"""

import re

from tokens import (BASE_SIZE, BOX_PAD_X, BOX_PAD_Y, CANVAS, CHAR_W, DASH,
                    FONT_STACK, MARGIN, RADIUS, Scale, theme)


class LayoutError(Exception):
    """Raised when a layout cannot be built honestly at the requested size."""


# ------------------------------------------------------------ measuring ----

def text_w(s, fs):
    """Conservative width estimate. Deliberately wider than the tightest
    plausible figure, because a local QA render can use a narrower fallback
    font than the one that reaches the reader."""
    return len(s) * CHAR_W * fs


def wrap(s, fs, avail, where="text"):
    """Greedy word wrap inside `avail` pixels. Raises rather than splitting a
    word or letting a line overflow."""
    words = str(s).split()
    if not words:
        return [""]
    for w in words:
        if text_w(w, fs) > avail:
            raise LayoutError(
                f"{where}: word {w!r} needs {text_w(w, fs):.0f}px, "
                f"container gives {avail:.0f}px — widen the box or shorten the word")
    lines, cur = [], words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if text_w(trial, fs) <= avail:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    for ln in lines:
        if text_w(ln, fs) > avail:
            raise LayoutError(f"{where}: line {ln!r} overflows {avail:.0f}px")
    return lines


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def minify(svg):
    svg = re.sub(r">\s+<", "><", svg)
    svg = re.sub(r"\n\s*", "", svg)
    return svg.strip()


# ----------------------------------------------------------------- box -----

DESCENT = 0.28          # allowance below a baseline, as a fraction of size


class Box:
    """A content box. Knows how tall it has to be; nothing else decides that.

    One pass produces both the height and the baselines, so the two cannot
    drift apart — the failure that put a stat card through the canvas edge in
    the hand-built era.

    kind    'process' | 'muted' | 'effect'
    state   'plain' | 'target' | 'outcome' | 'start' | 'dashed'
    """

    def __init__(self, title, values=(), *, kind="process", state="plain",
                 tag=None, badge=None, caption=None):
        self.title = title
        self.values = [v for v in values if v not in (None, "")]
        self.kind = kind
        self.state = state
        self.tag = tag
        self.badge = badge          # ('tick'|'cross', 'short caption')
        self.caption = caption
        self._laid = None
        self._last_top = None

    # -- geometry ---------------------------------------------------------
    def layout(self, w, sc):
        """Wrap against a known width; return the height required. Caches the
        rows, each as (text, role, size, baseline_offset)."""
        if self._laid and self._laid[0] == (w, sc.s):
            return self._laid[1]

        avail = w - BOX_PAD_X
        tag_w = text_w(self.tag, sc.cap) + 14 if self.tag else 0
        # A tag shares the title's line only while it leaves the title a
        # workable share of the width; otherwise it takes its own row above,
        # rather than squeezing the title into a column of single words.
        tag_inline = bool(self.tag) and tag_w <= 0.45 * avail
        if self.tag and not tag_inline:
            tag_w = 0

        rows, y = [], BOX_PAD_Y

        def emit(text, role, size, gap):
            nonlocal y
            y += gap
            y += size
            rows.append((text, role, size, y))
            y += round(size * DESCENT)

        if self.tag and not tag_inline:
            emit(self.tag, "tag", sc.cap, 0)
        for i, ln in enumerate(wrap(self.title, sc.s, avail - tag_w,
                                    where="box title")):
            emit(ln, "title", sc.s, (6 if self.tag and not tag_inline else 0)
                 if i == 0 else 1)
        vlines = []
        for v in self.values:
            vlines += wrap(v, sc.s, avail, where="box value")
        for i, ln in enumerate(vlines):
            emit(ln, "value", sc.s, 8 if i == 0 else 2)
        if self.badge and self.badge[1]:
            mark = "\u2713" if self.badge[0] == "tick" else "\u2717"
            for i, ln in enumerate(wrap(self.badge[1], sc.cap, avail,
                                        where="badge caption")):
                emit((mark + " " + ln) if i == 0 else ln, "badge", sc.cap,
                     6 if i == 0 else 1)
        if self.caption:
            for i, ln in enumerate(wrap(self.caption, sc.cap, avail,
                                        where="box caption")):
                emit(ln, "caption", sc.cap, 6 if i == 0 else 1)

        h = y + BOX_PAD_Y
        self._laid = ((w, sc.s), h, rows, tag_w, tag_inline)
        return h

    def slot(self, role):
        """Where a row of the given role actually sits, in absolute
        coordinates, after the box has been drawn. A form that overlays
        something on a value line asks for the line rather than guessing at the
        box's midpoint."""
        if self._laid is None or self._last_top is None:
            raise LayoutError("slot() is only meaningful after draw()")
        rows = [r for r in self._laid[2] if r[1] == role]
        if not rows:
            raise LayoutError(f"this box has no {role} row")
        size = rows[0][2]
        top = self._last_top + rows[0][3] - size
        bottom = self._last_top + rows[-1][3] + round(size * DESCENT)
        return top, bottom - top

    def height(self, w, sc):
        return self.layout(w, sc)

    # -- drawing ----------------------------------------------------------
    def draw(self, x, y, w, h, sc, t):
        nh = self.layout(w, sc)
        _, _, rows, tag_w, tag_inline = self._laid
        # In a height-matched row a shorter box centres its content block
        # rather than leaving it stranded against the top edge.
        top = y + max(0, (h - nh) / 2)
        self._last_top = top

        if self.kind == "effect":
            fill, stroke = t["effect_fill"], t["effect_stroke"]
            tcol, vcol, ccol = t["effect_label"], t["effect_value"], t["effect_cap"]
        elif self.kind == "muted":
            fill, stroke = t["muted_fill"], t["muted_stroke"]
            tcol, vcol, ccol = t["muted_title"], t["muted_value"], t["muted_title"]
        else:
            fill, stroke = t["proc_fill"], t["proc_stroke"]
            tcol, vcol, ccol = t["proc_title"], t["proc_value"], t["caption"]

        dash, sw = "", 1.2
        if self.state == "target":
            stroke, sw = t["state_target"], 2
        elif self.state == "outcome":
            stroke, sw = t["state_outcome"], 2
            if self.kind != "effect":
                vcol = t["state_outcome"]
        elif self.state == "start":
            stroke, sw = t["state_start"], 2
        elif self.state == "dashed":
            dash = f' stroke-dasharray="{DASH}"'

        tag_col = {"target": t["state_target"], "outcome": t["state_outcome"],
                   "start": t["state_start"]}.get(
                       self.state,
                       t["effect_value"] if self.kind == "effect"
                       else t["proc_value"])
        badge_col = {"tick": t["state_start"], "cross": t["state_target"]}.get(
            self.badge[0] if self.badge else None, ccol)

        p = [f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
             f'rx="{RADIUS}" fill="{fill}" stroke="{stroke}" '
             f'stroke-width="{sw}"{dash}/>']
        cx = x + w / 2
        tcx = x + (w - tag_w) / 2      # tag width comes out of the title's centre

        style = {"tag": ("v", tag_col, cx), "title": ("t", tcol, tcx),
                 "value": ("v", vcol, cx), "badge": ("c", badge_col, cx),
                 "caption": ("c", ccol, cx)}
        for text, role, size, dy in rows:
            cls, col, px = style[role]
            p.append(f'<text x="{px:.0f}" y="{top + dy:.0f}" class="{cls}" '
                     f'fill="{col}" font-size="{size}">{esc(text)}</text>')

        if self.tag and tag_inline:
            p.append(f'<text x="{x + w - 8:.0f}" y="{top + BOX_PAD_Y + sc.cap:.0f}" '
                     f'class="g" fill="{tag_col}" font-size="{sc.cap}">'
                     f'{esc(self.tag)}</text>')
        return "".join(p)


# ------------------------------------------------------------ connectors ---

HEAD = 7


def arrow(x1, x2, y, t):
    """Drawn, not a glyph: a font substitution cannot change its weight or
    shift it off the line it belongs on."""
    c = t["arrow"]
    return (f'<path d="M{x1:.0f} {y:.0f}H{x2 - HEAD:.0f}" stroke="{c}" '
            f'stroke-width="1.6" fill="none"/>'
            f'<path d="M{x2:.0f} {y:.0f}l-{HEAD} -{HEAD * 0.62:.0f}'
            f'v{HEAD * 1.24:.0f}z" fill="{c}"/>')


def arrow_down(x, y1, y2, t):
    c = t["arrow"]
    return (f'<path d="M{x:.0f} {y1:.0f}V{y2 - HEAD:.0f}" stroke="{c}" '
            f'stroke-width="1.6" fill="none"/>'
            f'<path d="M{x:.0f} {y2:.0f}l-{HEAD * 0.62:.0f} -{HEAD}'
            f'h{HEAD * 1.24:.0f}z" fill="{c}"/>')


def divider(x1, x2, y, caption, sc, t):
    p = [f'<line x1="{x1:.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y:.0f}" '
         f'stroke="{t["divider"]}" stroke-width="1" stroke-dasharray="{DASH}"/>']
    if caption:
        lines = wrap(caption, sc.cap, x2 - x1 - 20, where="divider caption")
        for i, ln in enumerate(lines):
            p.append(f'<text x="{(x1 + x2) / 2:.0f}" '
                     f'y="{y + sc.cap + 8 + i * (sc.cap + 3):.0f}" class="i" '
                     f'fill="{t["caption"]}" font-size="{sc.cap}">{esc(ln)}</text>')
    return "".join(p), (len(wrap(caption, sc.cap, x2 - x1 - 20)) * (sc.cap + 3) + 10
                        if caption else 6)


# --------------------------------------------------------------- canvas ----

STYLE = ("text{text-anchor:middle}"
         ".t{font-weight:600}.v{font-weight:700}.c{font-weight:400}"
         ".i{font-weight:400;font-style:italic}"
         ".g{font-weight:700;text-anchor:end}"
         ".h{font-weight:700;text-anchor:start}"
         ".s{font-weight:400;text-anchor:start}"
         ".f{font-weight:400;text-anchor:start}")


class Canvas:
    """Page frame: background, wrapped title/subtitle, footer provenance tag,
    and the hard assertion that the content actually fits."""

    def __init__(self, ratio, title, subtitle, *, theme_name,
                 provenance, w=None, h=None, base=None):
        self.ratio = ratio
        self.W, self.H = (w, h) if w and h else CANVAS[ratio]
        self.m = MARGIN[ratio]
        self.sc = Scale(base or BASE_SIZE[ratio])
        self.t = theme(theme_name)
        self.theme_name = theme_name
        self.provenance = provenance
        self.head = []
        self.parts = []
        self.head_h = self._head(title, subtitle)

    @property
    def inner_w(self):
        return self.W - 2 * self.m

    def _head(self, title, subtitle):
        sc, t = self.sc, self.t
        y = self.m - 6 + sc.h1
        tl = wrap(title, sc.h1, self.inner_w, where="page title")
        for i, ln in enumerate(tl):
            self.head.append(f'<text x="{self.m}" y="{y + i * (sc.h1 + 4):.0f}" '
                              f'class="h" fill="{t["h1"]}" font-size="{sc.h1}">'
                              f'{esc(ln)}</text>')
        y += (len(tl) - 1) * (sc.h1 + 4)
        if subtitle:
            sl = wrap(subtitle, sc.sub, self.inner_w, where="page subtitle")
            y += 8 + sc.sub
            for i, ln in enumerate(sl):
                self.head.append(f'<text x="{self.m}" y="{y + i * (sc.sub + 3):.0f}" '
                                  f'class="s" fill="{t["sub"]}" font-size="{sc.sub}">'
                                  f'{esc(ln)}</text>')
            y += (len(sl) - 1) * (sc.sub + 3)
        return y + 22          # first free y for body content

    def add(self, svg):
        self.parts.append(svg)

    def check(self, content_bottom):
        """Hard fit assertion: an overrun fails loudly rather than clipping."""
        limit = self.H - self.m - self.sc.footer - 10
        if content_bottom > limit:
            raise LayoutError(
                f"content bottom {content_bottom:.0f} exceeds {limit:.0f} on a "
                f"{self.W}x{self.H} canvas — grow the canvas, merge shared "
                f"content, or split the graphic. Never cut a named step.")
        return True

    def finish(self, content_bottom, path):
        sc, t = self.sc, self.t
        self.check(content_bottom)
        foot_y = self.H - self.m + sc.footer
        self.head.append(f'<text x="{self.m}" y="{foot_y:.0f}" class="f" '
                          f'fill="{t["footer"]}" font-size="{sc.footer}">'
                          f'{esc(self.provenance)}</text>')
        # Whatever height the ratio forces beyond what the content needs is
        # split above and below the body, so the page reads as composed rather
        # than as content that ran out.
        dy = max(0, (self.H - self.m - sc.footer - 10 - content_bottom) / 2)
        body = "".join(self.parts)
        if dy >= 4:
            body = f'<g transform="translate(0 {dy:.0f})">{body}</g>'
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
               f'viewBox="0 0 {self.W} {self.H}" font-family="{FONT_STACK}">'
               f'<style>{STYLE}</style>'
               f'<rect width="{self.W}" height="{self.H}" fill="{t["canvas"]}"/>'
               f'{"".join(self.head)}{body}</svg>')
        svg = minify(svg)
        with open(path, "w") as f:
            f.write(svg)
        return len(svg.encode())


# ----------------------------------------------------------- provenance ----

FIT_BOUNDS = {"wide": (880, 1480), "tall": (660, 1140)}
# How far the one type-size variable may scale up to fill a canvas.
BASE_HEADROOM = 4


def build_fitted(ratio, title, subtitle, theme_name, prov, compose, path,
                 *, w=None, h=None, base_lock=None, step=20):
    """Search for the smallest canvas at the required ratio that holds the
    content, rather than picking a size and living with the dead space.

    compose(canvas) draws the body and returns the y of its lowest pixel.
    """
    from tokens import RATIO
    if w and h:
        cv = Canvas(ratio, title, subtitle, theme_name=theme_name,
                    provenance=prov, w=w, h=h, base=base_lock)
        return {"bytes": cv.finish(compose(cv), path), "w": cv.W, "h": cv.H,
                "base": cv.sc.s}

    lo, hi = FIT_BOUNDS[ratio]
    base0 = BASE_SIZE[ratio]
    bases = ([base_lock] if base_lock
             else range(base0, base0 + BASE_HEADROOM + 1))
    best, last_err = None, None
    for base in bases:
        for W in range(hi, lo - 1, -step):
            H = round(W / RATIO[ratio])
            try:
                cv = Canvas(ratio, title, subtitle, theme_name=theme_name,
                            provenance=prov, w=W, h=H, base=base)
                bottom = compose(cv)
                cv.check(bottom)
            except LayoutError as e:
                last_err = e
                continue
            slack = (H - cv.m - cv.sc.footer - 10 - bottom) / H
            # Prefer the canvas the content most nearly fills; among equals,
            # the smaller canvas and the larger type.
            key = (round(slack, 2), W, -base)
            if best is None or key < best[0]:
                best = (key, cv, bottom)
    if best is None:
        raise LayoutError(f"no canvas in {lo}-{hi}px at the {ratio} ratio fits "
                          f"this content. Last failure: {last_err}")
    cv = best[1]
    return {"bytes": cv.finish(best[2], path), "w": cv.W, "h": cv.H,
            "base": cv.sc.s}


def elbow(x1, y1, x2, y2, t, *, mid=None):
    """Out of the bottom of one box, across, and down into the top of the next
    — the connector that joins the rows of a wrapped chain."""
    c = t["arrow"]
    m = mid if mid is not None else (y1 + y2) / 2
    return (f'<path d="M{x1:.0f} {y1:.0f}V{m:.0f}H{x2:.0f}V{y2 - HEAD:.0f}" '
            f'stroke="{c}" stroke-width="1.6" fill="none"/>'
            f'<path d="M{x2:.0f} {y2:.0f}l-{HEAD * 0.62:.0f} -{HEAD}'
            f'h{HEAD * 1.24:.0f}z" fill="{c}"/>')


def rail(x1, x2, y, t, *, stems=(), stem_from=None):
    """A rail spanning a whole block, with a short stem down from each member.
    An arrow rising out of the gap between two boxes reads as coming from
    nowhere; a rail says the whole block is the source."""
    c = t["arrow"]
    p = [f'<path d="M{x1:.0f} {y:.0f}H{x2:.0f}" stroke="{c}" '
         f'stroke-width="1.6" fill="none"/>']
    for sx in stems:
        p.append(f'<path d="M{sx:.0f} {stem_from:.0f}V{y:.0f}" stroke="{c}" '
                 f'stroke-width="1.6" fill="none"/>')
    return "".join(p)


def bypass_arc(x1, x2, y, clearance, label, sc, t):
    """An arc carrying one path over a step the other path skips.

    The visual apex of a symmetric quadratic bezier sits at half the control
    point's offset from the chord, so the control offset is twice the clearance
    actually wanted. Estimating this is what once put an arc through the box it
    was meant to clear.
    """
    c = t["arrow"]
    ctrl = 2 * clearance
    mx = (x1 + x2) / 2
    p = [f'<path d="M{x1:.0f} {y:.0f}Q{mx:.0f} {y - ctrl:.0f} '
         f'{x2 - HEAD:.0f} {y:.0f}" stroke="{c}" stroke-width="1.6" '
         f'fill="none" stroke-dasharray="{DASH}"/>'
         f'<path d="M{x2:.0f} {y:.0f}l-{HEAD} -{HEAD * 0.62:.0f}'
         f'v{HEAD * 1.24:.0f}z" fill="{c}"/>']
    if label:
        p.append(f'<text x="{mx:.0f}" y="{y - clearance - 4:.0f}" class="i" '
                 f'fill="{t["caption"]}" font-size="{sc.cap}">{esc(label)}</text>')
    return "".join(p), clearance + sc.cap + 8


def band_label(x, y, text, sc, t):
    """A section label. Labels sit above the band they introduce — under an
    arrow band they make the arrows read as pointing at the label."""
    return (f'<text x="{x:.0f}" y="{y:.0f}" class="s" fill="{t["caption"]}" '
            f'font-size="{sc.s}" font-weight="500">{esc(text)}</text>')


def blank_field(x, y, w, h, t):
    """The dashed blank a fill-in-the-blank diagram hands over to be completed."""
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'rx="4" fill="none" stroke="{t["caption"]}" stroke-width="1.2" '
            f'stroke-dasharray="{DASH}" opacity="0.75"/>')


def provenance(form, version=2, mode="tpl"):
    """The visible footer mark. `mode` is 'tpl' or 'freehand'."""
    if mode == "freehand":
        return "freehand · logged"
    return f"tpl · {form} · v{version}"
