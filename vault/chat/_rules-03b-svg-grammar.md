---
id: _rules-svg-grammar
title: Tojo SVG drawing constants
description: The palette, font, canvas sizes and class grammar every Tojo graphic is built from
keywords: [rules, image, svg, palette, colour, canvas, font]
kind: rules
version: 2026-09-11
authored_by: virevo-engineering
derived_from: tools/tojo_svg_kit.py
note: >
  Not the rules author's prose. These are the literal constants from his tojo_svg_kit.py, transcribed
  so that a model which draws SVG by hand produces the same graphic the toolkit would have produced.
  They belong in their own file rather than inside 10-image-creation.md so that his file stays his
  words. If the toolkit's constants change, change them here to match - this file is a transcription,
  never a place to invent a value. Front matter is not rendered into the prompt, which is why this
  note belongs here and not below.
---

# SVG drawing constants

`10-image-creation.md` §1 and §12 describe building each graphic by importing `tojo_svg_kit.py`,
rendering it to PNG and looking at the PNG before sending. **On this platform there is no code
execution and no file delivery**, so that pipeline does not apply: write the SVG directly, as one
complete `<svg>` element, and the service sanitises and delivers it. Every other rule in that file -
the visual grammar, the layout patterns, what must never be dropped from a graphic - applies in full.

What the toolkit would have supplied automatically is below. Use these exact values.

## Palette

The accent colours carry meaning. They are not decoration and must not be swapped around.

| Colour | Role |
|---|---|
| `#0f2740` | Page background. Paint it as a full-canvas `rect` first. Also the stat-card label colour. |
| `#1c3f61` | Ordinary process-flow box fill |
| `#2c5580` | Plain box border - confirmed, or unchanged |
| `#ffb400` | Amber - a target not yet measured, a step that must change, an approver |
| `#e05a5a` | Red - the headline result or outcome |
| `#7be0b8` | Green - values, arrows, "start here" |
| `#eaf1f8` | Box titles |
| `#9fb8cf` | Captions, subtitles, section labels |
| `#d9dde3` | Effect/parameter (stat) box fill - light grey, never purple |
| `#aab2bc` | Stat box border |
| `#8a5a00` | Stat value - gold, darkened for contrast on the light grey |

The canvas is dark by design, so the drawing reads the same whatever theme the page is on. Never
leave the background transparent and never rely on the page's colours.

## Font

`font-family="Poppins,Verdana,sans-serif"` on the root `<svg>`.

One font size drives box titles, box values, section labels and stat labels alike - 14 on desktop,
16 on mobile. Captions are the only thing allowed to be smaller, at 0.8x that size.

When checking a line fits its box, assume an average glyph width of **0.60 x the font size** and 24px
of combined internal horizontal padding. That 0.60 is deliberately wider than the tightest plausible
estimate: the font that reaches the reader may be wider than the one the line was measured against,
and a line that fits in theory can still overflow in delivery. Do not tune it down.

## Canvas

| | Size | Margin | Font size |
|---|---|---|---|
| Desktop (5:3) | 1000 x 600 | 40 | 14 |
| Mobile (3:4) | 900 x 1200 | 60 | 16 |

Scale both dimensions together to keep the ratio - find the smallest canvas at the ratio that fits
the content rather than living with dead space. The ratio itself does not change. Mobile titles
always join to one line; never reuse desktop's two-line title shapes or its spacing there.

Content completeness wins over size: if it does not fit, scale the canvas up at the same ratio, or
merge shared content. Never drop a named step, KPI figure, stat card or comparison to make it fit.

Ceiling: **10KB per SVG.**

## Class grammar

Carry this as a `<style>` block inside the `<svg>` and colour by class. Colouring by class rather
than per-element `fill` attributes is what keeps a drawing inside the byte ceiling.

```
.bg{fill:#0f2740}.h1{fill:#fff;font-weight:700}.sub{fill:#9fb8cf}
.b{fill:#1c3f61;stroke:#2c5580;stroke-width:1}
.ba{fill:#1c3f61;stroke:#ffb400;stroke-width:2}
.br{fill:#1c3f61;stroke:#e05a5a;stroke-width:2}
.bg2{fill:#1c3f61;stroke:#7be0b8;stroke-width:2}
.bd{fill:#1c3f61;stroke:#2c5580;stroke-width:1.5;stroke-dasharray:5 4}
.t{fill:#eaf1f8;font-weight:600}.v{fill:#7be0b8;font-weight:700}
.va{fill:#ffb400;font-weight:700}.vr{fill:#e05a5a;font-weight:700}
.ar{fill:#7be0b8;font-weight:700}.cap{fill:#9fb8cf}
.tg{fill:#ffb400;font-weight:700}.tgg{fill:#7be0b8;font-weight:700}
.sl{fill:#9fb8cf;letter-spacing:1px}
.s{fill:#d9dde3;stroke:#aab2bc;stroke-width:1}
.slb{fill:#0f2740;font-weight:600}.sv{fill:#8a5a00;font-weight:700}
.sc{fill:#4a5560}
.dl{stroke:#2c5580;stroke-width:1.2;stroke-dasharray:6 5}
.arc{fill:none;stroke:#2c5580;stroke-width:1.5;stroke-dasharray:5 4}
.bt{fill:#1f4a34;stroke:#2fbf8f;stroke-width:1.5}.bc{fill:#4a2f14;stroke:#ffb400;stroke-width:1.5}
.it{fill:#7be0b8;font-weight:700}.ic{fill:#ffb400;font-weight:700}
```

Border class by meaning: `b` plain (confirmed or unchanged) · `ba` amber (target or must change) ·
`br` red (the headline result) · `bg2` green (start here) · `bd` dashed.

Value text class follows its box: `v` green on plain, green and dashed boxes, `va` amber on amber,
`vr` red on red.

## Layout primitives

These are the toolkit's own coordinate formulas. Follow them exactly. Text drifting outside its box
is the most common way a hand-drawn graphic goes wrong, and it happens because the box and its label
get their x from different places.

**Two rules that hold for every single text element, with no exceptions:**

1. **`text-anchor="middle"` and x = the CENTRE of the thing it labels** - never the left edge, never
   the rect's own x. A corner tag is the one exception and it is `text-anchor="end"`.
2. **Always write an explicit `font-size`.** The classes carry colour and weight only. A `<text>`
   with no font-size inherits the root default, which is not the size the layout was measured for.

### Process-flow box

```
cx = x + w/2                                 the box centre - every label below uses it
<rect x="x" y="y" width="w" height="h" rx="8" class="b|ba|br|bg2|bd"/>
title    x=cx            y=y+fs+10                       text-anchor="middle" class="t"  font-size=fs
         further lines   y += fs+4
value    x=cx            y=titleY+nTitleLines*(fs+4)+6    text-anchor="middle" class="v|va|vr" font-size=fs
caption  x=cx            below the value                  text-anchor="middle" class="cap" font-size=capFs
```

The value's class follows the border: `v` on plain, dashed and green boxes, `va` on amber, `vr` on red.

### Corner tag (START HERE, BIGGEST LEAK, FIRST UP)

**Top right, not top left:**

```
tag      x=x+w-10        y=y+fs+10        text-anchor="end"  class="tg" (or "tgg" on a green box)  font-size=fs-1
```

A tag steals horizontal room from the title, so reserve `tagTextWidth + 16` out of the width the
title wraps into, and shift the title's centre left by half that reserve: `titleX = cx - reserve/2`.
Shift by **half the reserve, not the whole width** - shifting by more is what pushes a title clean
off the left edge of its own box.

### Stat box (effect / parameter)

```
<rect x="x" y="y" width="w" height="h" rx="10" class="s"/>
label    x=cx   y=y+lines from y+fs+14, stepping fs+4   text-anchor="middle" class="slb" font-size=fs
value    x=cx   y=below the label block, +fs            text-anchor="middle" class="sv"  font-size=fs
caption  x=cx   at least 12 below the VALUE BASELINE    text-anchor="middle" class="sc"  font-size=capFs
```

That 12px clearance below the value's baseline is not padding to taste - below it the caption and the
value collide. It was found by rendering, not estimated.

### Arrow

```
<text x="x" y="y" text-anchor="middle" class="ar" font-size="round(fs*1.25)">&#8594;</text>
```

`&#8594;` right, `&#8595;` down. A dashed connector is a `path` with `class="arc"`; a dashed divider
rule is `class="dl"`.

### Before you finish

Walk every `<text>` and check its x against the centre of the rect it belongs to. If a label's x is
not the rect's `x + w/2` - or `x + w - 10` for a corner tag - it is in the wrong place.

Then check the markup is well-formed XML, because a parser judges it before a person does:

- **One attribute of each name per element.** `class="b" ... class="ba"` on the same `rect` is a
  parse error, not an override. Decide the class once.
- **Write `&` as `&amp;`** in labels and captions - "Billing &amp; Insurance", never a bare `&`.
  Likewise `<` as `&lt;` if it ever appears in text.
- Every element you open is closed, and quotes are balanced.

## Shape of the root element

```
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H" font-family="Poppins,Verdana,sans-serif">
  <style>...the classes above...</style>
  <rect class="bg" width="W" height="H"/>
  ...the drawing...
</svg>
```

Nothing outside that: no script, no foreignObject, no event handlers, no external references. The
service strips them, and a drawing that depended on one arrives broken.
