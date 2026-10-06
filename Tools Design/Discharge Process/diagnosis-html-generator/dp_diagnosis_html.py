#!/usr/bin/env python3
"""
dp_diagnosis_html — the Discharge Process Diagnosis generator (v1, 5 Oct 2026).

Draws each Discharge Diagnosis turn from its JSON spec with the latest Diagnosis generator
(Bed Management/diagnosis-html-generator/bm_diagnosis_html.py, loaded as its own copy; see ../dp_common.py):
the library's universal patterns and layered drawings, the common tool layer, the three buttons, the background
that changes every four turns, and the phone order. Discharge's colours come from registry.json; its own drawings
are in dp_dg_blocks.py.

  python3 dp_diagnosis_html.py build                 # every turn in ../examples/diagnosis/turns.json -> ../out/diagnosis/
  python3 dp_diagnosis_html.py validate SPEC.json
  python3 dp_diagnosis_html.py render SPEC.json --view desktop|mobile -o OUT.html
Standard library only.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.dirname(HERE)
sys.path[:0] = [HERE, DP]
import dp_common as D          # noqa: E402

base = D.load_base('diagnosis', 'dp_base_diagnosis')
D.point_at_discharge(base, os.path.join(HERE, 'registry.json'), 'dp_diagnosis_html 1.0', ['#D2DBD0', '#DAE2D7', '#D0D9CE', '#D7DFD4', '#D1DACF'])
import dp_dg_blocks            # noqa: E402
base.RENDER.update(dp_dg_blocks.register({'sheet': base.sheet, 'pick_attrs': base.pick_attrs, 'bedmark': base.bedmark, 'L': base.L, 'dh': base.dh}))
base.LAYER_CSS = base.LAYER_CSS + dp_dg_blocks.CSS

_tw = base.RENDER['time-window']
def _time_window(b, ctx):
    """The layered time-window, with the turn's own hint in place of the Bed Management one."""
    out = _tw(b, ctx)
    return out.replace(base.dh.e('Tap a moment on the line to see what happens to the bed and the bill.'), base.dh.e(b.get('hint') or 'Tap a moment on the line to see what happens then.'), 1)
base.RENDER['time-window'] = _time_window

def theme_css(reg):
    """The Discharge Diagnosis colours on the layered blocks (selector .tj[data-theme=bm][data-tool=dp])."""
    k = reg['theme']['tokens']
    css = ('.tj[data-theme="bm"][data-tool="dp"]{--ground:%(ground)s;--card:%(card)s;--ink:%(ink)s;--muted:%(muted)s;--faint:%(faint)s;--gold-text:%(gold_text)s;'
           '--red:%(red)s;--green:%(green)s;--later:%(later)s;--paper:%(paper)s;--st-plain:%(ink)s;--st-target:%(target)s;--st-outcome:%(red)s;'
           '--st-start:%(green)s;--acc:%(accent)s;--shadow:%(shadow)s}') % k
    lamp = reg['tones']['list']['lamp']
    css += ('.tj[data-theme="bm"][data-tool="dp"][data-tone="lamp"]{--ground:%s;--card:%s;--paper:%s;--muted:%s;--faint:%s;'
            'background-image:radial-gradient(rgba(16,36,26,.11) 1px,transparent 1.3px);background-size:18px 18px}') % (
        lamp['ground'], lamp['card'], lamp['card'], lamp['muted'], lamp['faint'])
    return css
base.theme_css = theme_css

_canvas = base.render_canvas
def render_canvas(spec, reg):
    return _canvas(spec, reg).replace('<div class="tj" data-theme="bm"', '<div class="tj" data-theme="bm" data-tool="dp"', 1)
base.render_canvas = render_canvas

load_registry, validate, render_page, tone_of = base.load_registry, base.validate, base.render_page, base.tone_of

if __name__ == '__main__':
    D.cli('Diagnosis', base, load_registry, validate, render_page, tone_of, base, base.dh, base.GEN,
          os.path.join(DP, 'examples', 'diagnosis'), os.path.join(DP, 'out', 'diagnosis'), base.C)
