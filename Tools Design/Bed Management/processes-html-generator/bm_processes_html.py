#!/usr/bin/env python3
"""
bm_processes_html — the Bed Management Processes generator (v1, 6 Oct 2026).

A copy of the latest Solutions generator (bm_solutions_html.py, loaded under its own name) pointed at Processes:
the same spec, checks (plain and simple English, word limits, one sheet per item), tool layer, three buttons,
background every four turns and phone order. It draws, in the look of the approved Processes landing page
(B, the trial ward: pale clay, deep brown, rust, pill buttons):
  - the Processes motifs of the block library, layered (the ward board heading, swap, trial, badges, seats,
    readouts, loop; ../../Discharge Process/processes-html-generator/dp_pr_blocks.py, loaded as a private copy);
  - Bed Management's own Processes drawings (bm_pr_blocks.py): day-dial, ward-pins, round-cards, slip, clipboard;
  - the layered Solutions drawings that fit process work (effect, notes).

  python3 bm_processes_html.py build          # every turn in ../examples/processes/turns.json -> ../out/processes/
Standard library only.
"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BM = os.path.dirname(HERE)
TOOLS = os.path.dirname(BM)
DPPR = os.path.join(TOOLS, 'Discharge Process', 'processes-html-generator')
sys.path[:0] = [HERE, os.path.join(TOOLS, 'Discharge Process')]

def _load(path, name):
    if name in sys.modules: return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

import dp_common as D                                                    # noqa: E402  build and review page helpers
base = D.load_base('solutions', 'bm_base_processes')
base.REG_PATH = os.path.join(HERE, 'registry.json')
base.GEN = 'bm_processes_html 1.0'
base.TOOL, base.PLACE = 'Bed Management', 'Processes'
base.RAIL = ['#E3D9D5', '#E8DFDB', '#E1D7D3', '#E6DDD9', '#E2D8D4']       # the Processes landing page rail

px = _load(os.path.join(DPPR, 'dp_pr_blocks.py'), 'bm_px_motifs')       # the library's Processes motifs, layered
px.PH = ['#A08E8A', '#8C4B3F', '#8A5608', '#2F6B4F', '#3A2522']          # trial bands in the trial ward colours
import bm_pr_blocks                                                       # noqa: E402
base.RENDER = dict(base.RENDER)
base.RENDER.update(px.register({'e': base.e, 'L': base.L, 'B': base.bm_so_blocks}))
base.RENDER.update(bm_pr_blocks.register({'e': base.e, 'L': base.L, 'B': base.bm_so_blocks}))
base.ITEM_KEYS = tuple(base.ITEM_KEYS) + ('rows', 'people', 'phases', 'lanes', 'times', 'changes', 'patients', 'fields', 'asks')

BM_CSS = r'''
/* ---- Bed Management Processes: the trial ward (approved landing page B) ---- */
.sx.px[data-tool="bm"]{--ground:#EDE6E3;--sheet:#FDFAF9;--card:#FDFAF9;--board:#FDFAF9;--ink:#3A2522;--muted:#69514D;--line:#8C4B3F;--acc:#8C4B3F;--plum:#8C4B3F;--plum-2:#A8665A;--plum-l:#F2CFC5;
  --wash:#F5ECEA;--off:#A08E8A;--grid:rgba(58,37,34,0);--gold:#d4a94f;--gold-t:#6B4F16;--amber:#8A5608;--green:#2F6B4F;--red:#8E2F1C;--faint:rgba(58,37,34,.40);--wire:#A08E8A;--soft:#F5ECEA;
  --pxline:rgba(58,37,34,.14);color:var(--ink);background-color:var(--ground);
  background-image:linear-gradient(90deg,rgba(58,37,34,.05) 1px,transparent 1px),linear-gradient(rgba(58,37,34,.05) 1px,transparent 1px);background-size:44px 44px;padding:26px 34px 34px}
.sx.px[data-tool="bm"][data-tone="paper"]{--ground:#E4D9D4;--sheet:#FFFFFF;--card:#FFFFFF;--board:#FFFFFF;--soft:#F3EAE7;--wash:#F3EAE7;
  background-image:radial-gradient(rgba(58,37,34,.16) 1.2px,transparent 1.5px);background-size:18px 18px}
.sx.px[data-tool="bm"] .xh-rule,.sx.px[data-tool="bm"] .xc-boss{color:#F7EEEB}
.sx.px[data-tool="bm"] .xc-boss span{color:#E2CFC9}
.sx.px[data-tool="bm"] .xc-win{background:rgba(140,75,63,.16)}
.sx.px[data-tool="bm"] .xr-confirmed .xr-w{box-shadow:inset 0 0 0 2px #5A3C37,inset 0 8px 14px rgba(0,0,0,.35)}
.sx.px[data-tool="bm"] .xr-confirmed .xr-v{color:#F7EEEB}
.sx.px[data-tool="bm"] .sh-acts .sh-act,.sx.px[data-tool="bm"] .dg-act{border-radius:22px}
.sx.px[data-tool="bm"] .xc-roles[style*="--r:4"],.sx.px[data-tool="bm"] .xc-roles[style*="--r:3"]{grid-template-columns:repeat(2,minmax(0,1fr))}
@container sx (max-width:699px){.sx.px[data-tool="bm"]{padding:18px 14px 26px}}
'''
base.PAGE_CSS = base.PAGE_CSS + px.CSS + bm_pr_blocks.CSS + BM_CSS

_canvas = base.render_canvas
def render_canvas(spec, reg):
    return (_canvas(spec, reg).replace('style="container-name:sx tj"', 'style="container-name:sx px tj"', 1)
            .replace('<div class="sx" data-theme="bm"', '<div class="sx px" data-theme="bm" data-tool="bm" data-place="pr"', 1))
base.render_canvas = render_canvas

_page = base.render_page
def render_page(spec, view, reg, fonts=True):
    return _page(spec, view, reg, fonts).replace('</body></html>', '<script>%s</script><script>%s</script></body></html>' % (px.JS, bm_pr_blocks.JS), 1)
base.render_page = render_page

load_registry, validate, tone_of = base.load_registry, base.validate, base.tone_of
EX, OUT = os.path.join(BM, 'examples', 'processes'), os.path.join(BM, 'out', 'processes')

def book_page(specs, reg):
    """The review page: dp_common's, with the Bed Management names."""
    html = D.book_page(specs, reg, 'Processes', render_page, tone_of, base.bmd, base.dh, base.GEN)
    return (html.replace('Discharge Process · Processes turns', 'Bed Management · Processes turns')
                .replace('in the Discharge Process Processes colours', 'in the Bed Management Processes colours (the trial ward)'))

def main():
    import argparse
    ap = argparse.ArgumentParser(description='Bed Management · Processes turns')
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate'); v.add_argument('spec')
    bd = sub.add_parser('build'); bd.add_argument('dir', nargs='?', default=EX); bd.add_argument('-o', '--out', default=OUT)
    a = ap.parse_args(); reg = load_registry()
    if a.cmd == 'validate':
        spec = json.load(open(a.spec, encoding='utf-8')); errs, warns = validate(spec, reg)
        for x in warns: print('warn:', x)
        for x in errs: print('ERROR:', x)
        print('valid' if not errs else 'INVALID'); sys.exit(1 if errs else 0)
    man = json.load(open(os.path.join(a.dir, 'turns.json'), encoding='utf-8'))
    specs, bad = [], 0
    for t in man['turns']:
        sp = json.load(open(os.path.join(a.dir, t['file']), encoding='utf-8')); errs, warns = validate(sp, reg)
        print('%-14s %s  theme: %s' % (t['file'][:-5], 'valid' if not errs else 'INVALID', tone_of(sp, reg)))
        for x in errs + warns: print('   ', x)
        bad += bool(errs); sp['turn']['note_for_review'] = t.get('note', ''); specs.append(sp)
    berrs = D.book_check(specs, reg, tone_of)
    for x in berrs: print('BOOK ERROR:', x)
    if bad or berrs: sys.exit(1)
    pages = os.path.join(a.out, 'pages'); os.makedirs(pages, exist_ok=True)
    for sp in specs:
        for vw in ('desktop', 'mobile'):
            open(os.path.join(pages, '%s.%s.html' % (sp['turn']['id'], vw)), 'w', encoding='utf-8').write(render_page(sp, vw, reg))
    out = os.path.join(a.out, 'processes-turns.html')
    open(out, 'w', encoding='utf-8').write(book_page(specs, reg))
    print('wrote', out)

if __name__ == '__main__':
    main()
