"""
dp_common — what every Discharge Process turn generator shares (5 Oct 2026).

The Discharge Process turns are drawn with the latest generators: the ones built for Bed Management
(Bed Management/<place>-html-generator/bm_<place>_html.py and their drawings), which carry the common tool layer,
the three buttons, the background that changes every four turns, the phone order and the checks.
Each Discharge generator loads that generator as its own copy and points it at Discharge Process:
  - its own registry.json (Discharge colours, its two backgrounds, its blocks and its three buttons),
  - its own drawings where Discharge needs one Bed Management does not have,
  - the Discharge app shell (tool name and the practice hospital: 250 beds, Bhubaneswar).
Nothing in Bed Management changes: the copy is loaded under another name and only the copy is pointed elsewhere.

Colours follow the approved Discharge landing pages (LANDING-PAGES.md):
  Diagnosis sage and forest ink · Solutions the blueprint, navy · Automations the switch room, steel and teal ·
  Processes the ward board, heather and aubergine.
Standard library only.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))          # the Discharge Process folder
TOOLS = os.path.dirname(HERE)
BM = os.path.join(TOOLS, 'Bed Management')
COMMON = os.path.join(TOOLS, 'Common Elements')
TOOL = 'Discharge Process'
HOSPITAL = '250-bed hospital, Bhubaneswar'                  # the Discharge practice hospital (playbook §0)
PLACES = ['Diagnosis', 'Solutions', 'Automations', 'Processes']

def _paths(place):
    g = os.path.join(BM, '%s-html-generator' % place)
    for p in [g, BM, os.path.join(BM, 'diagnosis-html-generator'), os.path.join(BM, 'solutions-html-generator'), os.path.join(BM, 'automations-html-generator'),
              os.path.join(COMMON, '%s-html-generator' % place), os.path.join(COMMON, 'diagnosis-html-generator'), os.path.join(COMMON, 'solutions-html-generator'),
              os.path.join(COMMON, 'processes-html-generator'), os.path.join(COMMON, 'landing-common'), os.path.join(COMMON, 'tool-layer')]:
        if p not in sys.path: sys.path.append(p)
    return g

def load_base(place, name=None):
    """A private copy of the latest generator for a place ('diagnosis', 'solutions', 'automations')."""
    g = _paths(place)
    path = os.path.join(g, 'bm_%s_html.py' % place)
    name = name or 'dp_base_%s' % place
    if name in sys.modules: return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

def point_at_discharge(base, reg_path, gen, rail, place=None):
    base.REG_PATH = reg_path
    base.GEN = gen
    base.TOOL = TOOL
    base.RAIL = rail
    if place: base.PLACE = place

def shell_for_discharge(C):
    """The app shell for a standalone Discharge page (only when a page is written, never in the library)."""
    C.TOOL = TOOL
    C.HOSPITAL[:] = [HOSPITAL]

# ------------------------------------------------------------------------------------------ rules across turns
def book_check(specs, reg, tone_of):
    """rules/08 §2-3: a main block is used once in a place, two turns in a row share nothing but the heading and the effect,
    specs store no colour. A fill-in-the-blank and its filled redraw (turn.redraw_of) may share the main block."""
    errs, rep = [], {'heading', 'effect'}
    main, types, seen = {}, {}, {}
    for sp in specs:
        bl = [b['type'] for b in sp['canvas']['blocks']]
        main[sp['turn']['id']] = bl[1] if len(bl) > 1 else 'heading'; types[sp['turn']['id']] = set(bl)
    for i, sp in enumerate(specs):
        tid = sp['turn']['id']; red = sp['turn'].get('redraw_of')
        if main[tid] in seen and seen[main[tid]] != red: errs.append('%s: main block %s is already the main block of %s' % (tid, main[tid], seen[main[tid]]))
        seen.setdefault(main[tid], tid)
        if i:
            prev = specs[i - 1]['turn']['id']; shared = (types[tid] & types[prev]) - rep
            if red == prev: shared -= {main[tid]}
            if shared: errs.append('%s: shares %s with the turn before; two turns in a row must look different' % (tid, ', '.join(sorted(shared))))
            if red == prev and len(types[tid] - types[prev] - rep) == 0: errs.append('%s: a redraw adds a block of its own' % tid)
        if sp.get('canvas', {}).get('tone') and not red: errs.append('%s: specs store no colour' % tid)
    return errs

# ------------------------------------------------------------------------------------------ build: every turn of a place, then the review page
def build(base, reg, place, ex_dir, out_dir, validate, render_page, tone_of, bmd, dh, gen):
    man = json.load(open(os.path.join(ex_dir, 'turns.json'), encoding='utf-8'))
    specs, bad = [], 0
    for t in man['turns']:
        sp = json.load(open(os.path.join(ex_dir, t['file']), encoding='utf-8')); errs, warns = validate(sp, reg)
        print('%-24s %s  theme: %s' % (t['file'][:-5], 'valid' if not errs else 'INVALID', tone_of(sp, reg)))
        for x in errs + warns: print('   ', x)
        bad += bool(errs); sp['turn']['note_for_review'] = t.get('note', ''); specs.append(sp)
    berrs = book_check(specs, reg, tone_of)
    for x in berrs: print('BOOK ERROR:', x)
    if bad or berrs: sys.exit(1)
    pages = os.path.join(out_dir, 'pages'); os.makedirs(pages, exist_ok=True)
    for sp in specs:
        for vw in ('desktop', 'mobile'):
            open(os.path.join(pages, '%s.%s.html' % (sp['turn']['id'], vw)), 'w', encoding='utf-8').write(render_page(sp, vw, reg))
    out = os.path.join(out_dir, '%s-turns.html' % place.lower())
    open(out, 'w', encoding='utf-8').write(book_page(specs, reg, place, render_page, tone_of, bmd, dh, gen))
    print('wrote', out)
    return specs

def book_page(specs, reg, place, render_page, tone_of, bmd, dh, gen):
    e = dh.e
    data, secs = [], []
    nxt = {'Diagnosis': 'Solutions', 'Solutions': 'Automations', 'Automations': 'Processes', 'Processes': 'Diagnosis'}[place]
    for i, s in enumerate(specs):
        data.append({'desktop': render_page(s, 'desktop', reg, fonts=False), 'mobile': render_page(s, 'mobile', reg, fonts=False)})
        t = s['turn']
        chips = ''.join('<span class="rv-chip">%s</span>' % e(x) for x in ['Drawn with: ' + ', '.join(b['type'] for b in s['canvas']['blocks'][1:])] +
                        ['Theme: ' + reg['tones']['list'][tone_of(s, reg)]['name']] + (['Was: ' + t['was']] if t.get('was') else []))
        rec = ('<div class="rv-rec" style="margin:0 0 14px"><div class="rv-box"><b>%s · the user’s message</b>%s</div><div class="rv-box"><b>The three prompts</b><ol>%s</ol></div>'
               '<div class="rv-box"><b>Where it comes from</b>%s</div></div>') % (
            e(t.get('transcript', {}).get('label', '')), e(t['user_message']), ''.join('<li>%s</li>' % e(p) for p in s['chat']['prompts']), e(t.get('context', '')))
        title = s['canvas']['blocks'][0]['title']
        secs.append(('<section class="rv-s" id="%s" data-i="%d"><div class="rv-sh"><h2>%s · %s</h2>%s</div><p class="rv-what">%s</p>%s'
                     '<div class="rv-views"><div><div class="rv-lab">Desktop · 1440 × 900 · scroll inside it</div><div class="rv-screen"><iframe data-v="desktop" title="%s on desktop"></iframe></div></div>'
                     '<div><div class="rv-lab">Phone · 390 × 844 · scroll inside it</div><div class="rv-hand"><iframe data-v="mobile" title="%s on a phone"></iframe></div></div></div></section>') % (
            e(t['id']), i, e(t['id']), e(title), chips, e(t.get('note_for_review', '')), rec, e(t['id']), e(t['id'])))
    nav = '<nav class="rv-jump">%s</nav>' % ''.join('<a href="#%s">%s</a>' % (e(s['turn']['id']), e(s['turn']['id'])) for s in specs)
    intro = ('%d turns, in conversation order, each drawn by %s from its spec: the latest Tojo generators in the Discharge Process %s colours, with the common tool layer '
             '(the first item raised with its sheet open, entries typed in the drawing and added to the message). Every turn ends with the three buttons: '
             'Proceed with next step, Add more, Jump to %s. The background changes every four turns.') % (len(specs), gen, place, nxt)
    title = 'Discharge Process · %s turns' % place
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>'
            '<style>%s</style><style id="rv-top-fonts"></style></head><body><script type="application/json" id="rv-data">%s</script><script type="text/plain" id="rv-fonts">%s</script>'
            '<div class="rv"><h1>%s</h1><p class="rv-intro">%s</p>%s%s</div><script>%s</script></body></html>') % (
        e(title), bmd.REVIEW_CSS, json.dumps(data, ensure_ascii=False).replace('</', '<\\/'), dh.font_css(), e(title), e(intro), nav, ''.join(secs), bmd.REVIEW_JS)

def cli(place, base, reg_loader, validate, render_page, tone_of, bmd, dh, gen, ex_dir, out_dir, C):
    import argparse
    ap = argparse.ArgumentParser(description='Discharge Process · %s turns' % place)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate'); v.add_argument('spec')
    r = sub.add_parser('render'); r.add_argument('spec'); r.add_argument('--view', default='desktop', choices=['desktop', 'mobile']); r.add_argument('-o', '--out')
    bd = sub.add_parser('build'); bd.add_argument('dir', nargs='?', default=ex_dir); bd.add_argument('-o', '--out', default=out_dir)
    a = ap.parse_args(); reg = reg_loader()
    shell_for_discharge(C)
    if a.cmd == 'build': build(base, reg, place, a.dir, a.out, validate, render_page, tone_of, bmd, dh, gen)
    if a.cmd == 'validate':
        spec = json.load(open(a.spec, encoding='utf-8')); errs, warns = validate(spec, reg)
        for x in warns: print('warn:', x)
        for x in errs: print('ERROR:', x)
        print('valid' if not errs else 'INVALID'); sys.exit(1 if errs else 0)
    if a.cmd == 'render':
        spec = json.load(open(a.spec, encoding='utf-8')); errs, _ = validate(spec, reg)
        if errs: print('\n'.join(errs), file=sys.stderr); sys.exit(1)
        out = render_page(spec, a.view, reg); (open(a.out, 'w', encoding='utf-8').write(out) if a.out else sys.stdout.write(out))
