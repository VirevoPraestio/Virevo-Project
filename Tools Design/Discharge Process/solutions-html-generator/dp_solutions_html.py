#!/usr/bin/env python3
"""
dp_solutions_html — the Discharge Process Solutions generator (v1, 5 Oct 2026).

Draws each Discharge Solutions turn from its JSON spec with the latest Solutions generator
(Bed Management/solutions-html-generator/bm_solutions_html.py, loaded as its own copy; see ../dp_common.py): the
Solutions motifs of the library (the lightbulb, the jigsaw, the maze, the knots, the route, the door plates) layered with
the common tool layer, the three buttons, the background that changes every four turns and the phone order.
Discharge's look (the blueprint) is set in registry.json and DP_CSS below.

  python3 dp_solutions_html.py build                 # every turn in ../examples/solutions/turns.json -> ../out/solutions/
  python3 dp_solutions_html.py validate SPEC.json
Standard library only.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.dirname(HERE)
sys.path[:0] = [HERE, DP]
import dp_common as D          # noqa: E402

base = D.load_base('solutions', 'dp_base_solutions')
D.point_at_discharge(base, os.path.join(HERE, 'registry.json'), 'dp_solutions_html 1.0', ['#D6DFE8', '#DDE5EC', '#D3DCE6', '#DAE2EA', '#D5DEE7'])

DP_CSS = r'''
/* ---- Discharge Process Solutions: the blueprint on the library's drafting table ---- */
.sx[data-theme="dp"]{--ground:#E3EAF0;--sheet:#F8FAFC;--card:#F8FAFC;--ink:#15304D;--muted:#4A5D72;--line:#2E5E8E;--acc:#2E5E8E;--grid:rgba(21,48,77,.07);
  --gold:#d4a94f;--gold-t:#6B4F16;--amber:#8A5608;--green:#2F6B4F;--red:#8E2F1C;--faint:rgba(21,48,77,.40);--wire:#8A9BB0;--soft:#E9EFF5;padding:26px 34px 34px}
.sx[data-theme="dp"][data-tone="paper"]{--ground:#EEF3F7;--sheet:#FFFFFF;--card:#FFFFFF;--soft:#F1F5F9;--grid:rgba(21,48,77,0);
  background-image:radial-gradient(rgba(21,48,77,.14) 1px,transparent 1.3px);background-size:20px 20px}
@container sx (max-width:699px){.sx[data-theme="dp"]{padding:18px 14px 26px}}
'''
base.PAGE_CSS = base.PAGE_CSS + DP_CSS

_canvas = base.render_canvas
def render_canvas(spec, reg):
    return _canvas(spec, reg).replace('<div class="sx" data-theme="bm"', '<div class="sx" data-theme="dp" data-tool="dp"', 1)
base.render_canvas = render_canvas

load_registry, validate, render_page, tone_of = base.load_registry, base.validate, base.render_page, base.tone_of

if __name__ == '__main__':
    D.cli('Solutions', base, load_registry, validate, render_page, tone_of, base.bmd, base.dh, base.GEN,
          os.path.join(DP, 'examples', 'solutions'), os.path.join(DP, 'out', 'solutions'), base.C)
