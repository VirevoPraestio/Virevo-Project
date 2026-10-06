#!/usr/bin/env python3
"""
dp_processes_html — the Discharge Process Processes generator (v1, 5 Oct 2026).

Processes had no layered generator yet. This one is a copy of the latest Solutions generator
(Bed Management/solutions-html-generator/bm_solutions_html.py, loaded under its own name; see ../dp_common.py) pointed at
Processes: the same spec, checks, tool layer, three buttons, background every four turns and phone order. It draws:
  - the Processes motifs of the block library, layered (dp_pr_blocks.py): the ward board heading, swap, trial, badges,
    seats, readouts, loop, and two new ones, the timesheet and the night lanes;
  - the layered Solutions drawings that fit process work (people, sizing, gauges, owners, findings, circuit, effect).
The canvas carries both the Solutions and the Processes class (sx px), in the Discharge Processes look: the ward board.

  python3 dp_processes_html.py build                 # every turn in ../examples/processes/turns.json -> ../out/processes/
Standard library only.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.dirname(HERE)
sys.path[:0] = [HERE, DP]
import dp_common as D          # noqa: E402

base = D.load_base('solutions', 'dp_base_processes')
D.point_at_discharge(base, os.path.join(HERE, 'registry.json'), 'dp_processes_html 1.0', ['#DDD5E1', '#E3DCE6', '#DAD2DE', '#E0D9E4', '#DCD4DF'], 'Processes')
import dp_pr_blocks            # noqa: E402
base.RENDER = dict(base.RENDER)
base.RENDER.update(dp_pr_blocks.register({'e': base.e, 'L': base.L, 'B': base.bm_so_blocks}))
base.ITEM_KEYS = tuple(base.ITEM_KEYS) + ('rows', 'people', 'phases', 'lanes')

DP_CSS = r'''
/* ---- Discharge Process Processes: the ward board ---- */
.sx.px[data-theme="dp"]{--ground:#ECE8EE;--sheet:#FCFBFD;--card:#FCFBFD;--board:#FCFBFD;--ink:#2A1E30;--muted:#5A4D60;--line:#6D4A77;--acc:#6D4A77;--plum:#6D4A77;--plum-2:#8E6A98;--plum-l:#E9C8F0;
  --wash:#F4F0F6;--off:#9C92A1;--grid:rgba(42,30,48,0);--gold:#d4a94f;--gold-t:#6B4F16;--amber:#8A5608;--green:#2F6B4F;--red:#8E2F1C;--faint:rgba(42,30,48,.40);--wire:#9C92A1;--soft:#F4F0F6;
  --pxline:rgba(42,30,48,.14);color:var(--ink);background-color:var(--ground);background-image:linear-gradient(rgba(42,30,48,.045) 1px,transparent 1px);background-size:100% 26px;padding:26px 34px 34px}
.sx.px[data-theme="dp"][data-tone="paper"]{--ground:#E6E0E9;--sheet:#FFFFFF;--card:#FFFFFF;--board:#FFFFFF;--soft:#F1ECF3;background-image:radial-gradient(rgba(42,30,48,.14) 1px,transparent 1.3px);background-size:20px 20px}
@container sx (max-width:699px){.sx.px[data-theme="dp"]{padding:18px 14px 26px}}
'''
base.PAGE_CSS = base.PAGE_CSS + dp_pr_blocks.CSS + DP_CSS

_canvas = base.render_canvas
def render_canvas(spec, reg):
    return (_canvas(spec, reg).replace('style="container-name:sx tj"', 'style="container-name:sx px tj"', 1)
            .replace('<div class="sx" data-theme="bm"', '<div class="sx px" data-theme="dp" data-tool="dp" data-place="pr"', 1))
base.render_canvas = render_canvas

_page = base.render_page
def render_page(spec, view, reg, fonts=True):
    return _page(spec, view, reg, fonts).replace('</body></html>', '<script>%s</script></body></html>' % dp_pr_blocks.JS, 1)
base.render_page = render_page

load_registry, validate, render_page, tone_of = base.load_registry, base.validate, base.render_page, base.tone_of

if __name__ == '__main__':
    D.cli('Processes', base, load_registry, validate, render_page, tone_of, base.bmd, base.dh, base.GEN,
          os.path.join(DP, 'examples', 'processes'), os.path.join(DP, 'out', 'processes'), base.C)
