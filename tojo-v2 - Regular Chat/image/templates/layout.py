"""Shared layout helpers. Every one of these sizes from measured content."""

from core import Box, LayoutError, arrow, arrow_down, divider

ARROW_GAP = {"wide": 30, "tall": 26}

# A box narrower than this wraps every title into a column of single words.
MIN_BOX_W = 150


def row(cv, boxes, y, *, gap=None, arrows=True, x0=None, width=None):
    """Boxes left to right, equal width, height matched to the tallest.
    Returns the y below the row."""
    gap = ARROW_GAP["wide"] if gap is None else gap
    m = cv.m if x0 is None else x0
    avail = (cv.inner_w if width is None else width)
    n = len(boxes)
    bw = (avail - gap * (n - 1)) / n
    if bw < MIN_BOX_W:
        raise LayoutError(f"{n} boxes in one row leaves {bw:.0f}px each — too "
                          f"narrow to read; wrap the chain or widen the canvas")
    h = max(b.height(bw, cv.sc) for b in boxes)
    x = m
    for i, b in enumerate(boxes):
        cv.add(b.draw(x, y, bw, h, cv.sc, cv.t))
        x += bw
        if i < n - 1:
            if arrows:
                cv.add(arrow(x + 6, x + gap - 6, y + h / 2, cv.t))
            x += gap
    return y + h


def column(cv, boxes, y, *, gap=None, arrows=True, x0=None, width=None):
    """Boxes top to bottom, each as tall as its own content needs."""
    gap = ARROW_GAP["tall"] if gap is None else gap
    x = cv.m if x0 is None else x0
    bw = (cv.inner_w if width is None else width)
    for i, b in enumerate(boxes):
        h = b.height(bw, cv.sc)
        cv.add(b.draw(x, y, bw, h, cv.sc, cv.t))
        y += h
        if i < len(boxes) - 1:
            if arrows:
                cv.add(arrow_down(x + bw / 2, y + 5, y + gap - 3, cv.t))
            y += gap
    return y


def effect_row(cv, effects, y, *, gap=20):
    """Effect/parameter boxes. On the tall ratio three never stack in a line:
    two go side by side and the third spans beneath, so they stay comparable."""
    if not effects:
        return y
    if cv.ratio == "wide" or len(effects) <= 2:
        return row(cv, effects, y, gap=gap, arrows=False)
    if len(effects) == 3:
        y2 = row(cv, effects[:2], y, gap=gap, arrows=False)
        return row(cv, effects[2:], y2 + gap, gap=gap, arrows=False)
    raise LayoutError("more than three effect boxes — split the graphic rather "
                      "than shrinking them")


def note(cv, y, caption, *, gap=18):
    """Dashed divider plus an italic caption: the point that spans the whole
    sequence rather than belonging to any one step."""
    svg, h = divider(cv.m, cv.W - cv.m, y + gap, caption, cv.sc, cv.t)
    cv.add(svg)
    return y + gap + h


def to_boxes(specs, kind="process"):
    return [Box(s["title"], s.get("values", ()),
                kind=s.get("kind", kind),
                state=s.get("state", "plain"),
                tag=s.get("tag"), badge=s.get("badge"),
                caption=s.get("caption"))
            for s in specs]
