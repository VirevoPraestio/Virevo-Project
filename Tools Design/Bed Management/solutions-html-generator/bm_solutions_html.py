#!/usr/bin/env python3
"""
bm_solutions_html — the Bed Management Solutions generator (v1, 1 Oct 2026).

How it works
  Claude writes one JSON spec per turn: the user's message, the chat parts (text, bullets, Tojo's note, @points,
  three prompts) and the canvas as blocks with slot values. This program validates the spec and draws it. No model
  writes HTML.

  The drawing comes from the Solutions part of the Tojo block library (Common Elements/solutions-html-generator):
  its renderers and solutions.css, with the Solutions motifs of 07 §1.3 (lightbulb, jigsaw, route, drafting sheet).
  Bed Management's Solutions look (the fit-out, from the approved landing page) is set through the library's colour
  variables. Every drawing carries the common tool layer (Common Elements/tool-layer/tojo_layer.py): the first item
  raised with its sheet open, each sheet under its item on a phone, entries typed in the drawing and added to the
  chat message. Bed Management's own drawings are in bm_so_blocks.py, built from the library's motifs.

  The page is the Bed Management app shell (bm_common.py). On a phone the turn is one feed: the user's message,
  Tojo's text, the drawing, then the note, points and prompts (rules/08 §4).

  python3 bm_solutions_html.py validate SPEC.json
  python3 bm_solutions_html.py render SPEC.json --view desktop|mobile -o OUT.html
  python3 bm_solutions_html.py samples SPEC.json [SPEC.json ...] -o OUT.html --pages DIR   # one turn, several samples, stacked
Standard library only.
"""
import argparse, copy, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BM = os.path.dirname(HERE)
ROOT = os.path.join(os.path.dirname(BM), 'Common Elements')
SOLG = os.path.join(ROOT, 'solutions-html-generator')
sys.path[:0] = [BM, os.path.join(BM, 'diagnosis-html-generator'), SOLG, os.path.join(ROOT, 'diagnosis-html-generator'),
                os.path.join(ROOT, 'landing-common'), os.path.join(ROOT, 'tool-layer')]
import diagnosis_html as dh        # noqa: E402  validator pieces, plain English, fonts
import solutions_html as so        # noqa: E402  the library's Solutions renderers and motifs
import bm_common as C              # noqa: E402  the Bed Management app shell
import tojo_layer as L             # noqa: E402  the common tool layer
import bm_diagnosis_html as bmd    # noqa: E402  shared Bed Management pieces: chat split, simple English, review page
import bm_so_blocks                # noqa: E402  Bed Management Solutions drawings

REG_PATH = os.path.join(HERE, 'registry.json')
GEN = 'bm_solutions_html 1.0'
TOOL, PLACE = 'Bed Management', 'Solutions'
e = dh.e
RAIL = ['#D6E0DC', '#DDE5E1', '#D3DED9', '#DBE3DF', '#D5DFDA']

def load_registry():
    reg = json.load(open(REG_PATH, encoding='utf-8'))
    reg['plain_english'] = dh.load_registry()['plain_english']
    lib = json.load(open(os.path.join(SOLG, 'registry.json'), encoding='utf-8'))
    reg['library_blocks'] = {b['id']: b for b in lib['blocks'] if b['status'] == 'approved' and b.get('scope') in ('all', 'Solutions')}
    reg['own_blocks'] = {b['id']: b for b in reg['blocks']}
    return reg

# ============================================================================================ theme
def turn_no(spec):
    m = re.search(r'(\d+)$', spec['turn'].get('id', '1')); return int(m.group(1)) if m else 1

def tone_of(spec, reg):
    if spec.get('canvas', {}).get('tone'): return spec['canvas']['tone']
    t = reg['tones']; return t['rotation'][((max(turn_no(spec), 1) - 1) // t['set_size']) % len(t['rotation'])]

def shell_theme(reg, tone):
    k = dict(reg['theme']['tokens'])
    if tone == 'paper': k.update({x: reg['tones']['list']['paper'][x] for x in ('ground', 'card', 'muted')})
    return C.theme(k['ground'], k['card'], k['ink'], k['muted'], k['line'], k['soft'], k['grey'], RAIL, '4px', '--acc:%s' % k['accent'])

# ============================================================================================ blocks
RENDER = bm_so_blocks.register({'e': e, 'L': L, 'so': so, 'C': C})

def block_def(reg, t):
    return reg['own_blocks'].get(t)

ITEM_KEYS = ('steps', 'pieces', 'items', 'stations')

def validate(spec, reg=None):
    reg = reg or load_registry()
    errs, warns = [], []
    turn, chat, canvas = spec.get('turn', {}), spec.get('chat', {}), spec.get('canvas', {})
    for k in ('id', 'type', 'user_message'):
        if not turn.get(k): errs.append('turn.%s: required' % k)
    blocks = canvas.get('blocks', [])
    if not blocks or blocks[0].get('type') != 'heading': errs.append('canvas: first block must be "heading"')
    if len(blocks) - 1 > reg['budget']['max_blocks']: errs.append('canvas: too many blocks')
    for i, b in enumerate(blocks):
        t = b.get('type'); path = 'canvas.blocks[%d](%s)' % (i, t)
        d = block_def(reg, t)
        if not d: errs.append('%s: not a Bed Management Solutions block (registry.json)' % path); continue
        dh.check_fields(path, d['slots'], b, errs, warns)
        items = next((b[k] for k in ITEM_KEYS if isinstance(b.get(k), list)), [])
        if b.get('sheets') and len(b['sheets']) != len(items):
            errs.append('%s: %d sheets for %d items; one sheet per item, in order' % (path, len(b['sheets']), len(items)))
        if t == 'circuit' and len(items) % 2: errs.append('%s: an even number of steps (two rows on a desktop)' % path)
        if t == 'jigsaw':
            for j, p in enumerate(items):
                for r in p.get('relies_on', []):
                    if not 1 <= r <= len(items) or r == j + 1: errs.append('%s.pieces[%d].relies_on: %s is not another piece' % (path, j, r))
        keys = [s.get('key') for s in b.get('sheets', [])]
        if len(set(keys)) != len(keys): errs.append('%s: sheet keys must differ' % path)
    s2 = copy.deepcopy(spec); s2['turn'].pop('user_message', None)
    errs += ['plain English: ' + p for p in dh.plain_check(s2, reg)]
    errs += ['simple English: ' + x for x in bmd.simple_check(spec)]
    if len(chat.get('prompts', [])) != 3: errs.append('chat.prompts: exactly 3')
    for i, p in enumerate(chat.get('points', [])):
        if p.get('n') != i + 1: errs.append('chat.points[%d].n must be %d' % (i, i + 1))
    for k in ('pointer', 'invite'):
        if chat.get(k) and re.search(r'\b(left|right|above|below|sidebar)\b', chat[k], re.I): errs.append('chat.%s: name the drawing, not where it is' % k)
    return errs, warns

# ============================================================================================ pages
PAGE_CSS = r'''
.sx-host{container-type:inline-size}
.bm-m .sh-mc > .sh-mpanel{height:auto!important;min-height:0!important;overflow:visible!important}
.bm-m .sh-mc > .sx-host{flex:none}
#tojo-input{resize:none;overflow-y:auto;line-height:1.45}
.sh-box #tojo-input{border:0;outline:0;background:transparent;font:inherit;font-size:15px;flex:1;padding:10px 4px;min-height:24px;max-height:260px}
'''

def render_canvas(spec, reg):
    ctx = dh.Ctx(); ctx.turn = turn_no(spec); ctx.eff = 0
    ctx.sample = ' ABCDEFG'.find((spec['turn'].get('sample') or {}).get('letter', ' ') or ' ')
    ctx.sample = max(ctx.sample, 0)
    inner = ''.join(RENDER[b['type']](b, ctx) for b in spec['canvas']['blocks'])
    return ('<div class="sx-host" style="container-name:sx tj"><div class="sx" data-theme="bm" data-tone="%s" data-turn="%s" data-generator="%s"><div class="sx-stack">%s</div></div></div>' % (
        tone_of(spec, reg), e(spec['turn']['id']), GEN, inner))

def render_page(spec, view, reg, fonts=True):
    tone = tone_of(spec, reg); th = shell_theme(reg, tone)
    canvas = render_canvas(spec, reg)
    text, rest = bmd.split_chat(spec['chat'])
    if view == 'desktop':
        body = C.desktop(th, PLACE, canvas, bmd.user_bubble(spec) + text + rest)
    else:
        body = C.mobile(th, PLACE, '@@CANVAS@@', '@@CHAT@@')
        body = body.replace('<div class="sh-mc">', '<div class="sh-mc">' + bmd.user_bubble(spec), 1)
        body = body.replace('@@CANVAS@@<div class="sh-mpanel">@@CHAT@@</div>',
                            '<div class="sh-mpanel bm-mt">%s</div>%s<div class="sh-mpanel bm-mr">%s</div>' % (text, canvas, rest))
        body = re.sub(r'<input id="tojo-input"[^>]*>', '<textarea id="tojo-input" rows="1" placeholder="Write to Tojo…"></textarea>', body)
    css = open(so.CSS_PATH, encoding='utf-8').read() + L.CSS + bm_so_blocks.CSS + PAGE_CSS
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s · %s %s</title><style>%s</style><style>%s%s%s.bm-app .sh-bar{background:%s}%s</style></head><body>%s<script>%s</script><script>%s</script></body></html>') % (
        e(spec['turn']['id']), TOOL, PLACE, dh.font_css() if fonts else '', C.SHELL_CSS, C.shell_css(th), C.SHELL_V3_CSS, th['ground'], css,
        body, L.RUNTIME, bm_so_blocks.JS)

# ============================================================================================ review page: samples of one turn, stacked
def samples_page(specs, reg, title, intro=None):
    first = specs[0]; t = first['turn']
    data, secs = [], []
    for i, s in enumerate(specs):
        sm = s['turn'].get('sample') or {'letter': '', 'name': '', 'what': ''}
        data.append({'desktop': render_page(s, 'desktop', reg, fonts=False), 'mobile': render_page(s, 'mobile', reg, fonts=False)})
        blocks = [b for b in s['canvas']['blocks'][1:]]
        chips = ''.join('<span class="rv-chip">%s</span>' % e(x) for x in
                        ['Drawn from: ' + ' · '.join('%s (%s)' % (b['type'], reg['own_blocks'][b['type']]['from']) for b in blocks)] +
                        ['Theme: ' + reg['tones']['list'][tone_of(s, reg)]['name']])
        secs.append(('<section class="rv-s" id="%s" data-i="%d"><div class="rv-sh"><h2>Sample %s · %s</h2>%s</div><p class="rv-what">%s</p>'
                     '<div class="rv-views"><div><div class="rv-lab">Desktop · 1440 × 900 · scroll inside it</div><div class="rv-screen"><iframe data-v="desktop" title="Sample %s on desktop"></iframe></div></div>'
                     '<div><div class="rv-lab">Phone · 390 × 844 · scroll inside it</div><div class="rv-hand"><iframe data-v="mobile" title="Sample %s on a phone"></iframe></div></div></div></section>') % (
            e(s['turn']['id'] + sm['letter']), i, e(sm['letter']), e(sm['name']), chips, e(sm.get('what', '')), e(sm['letter']), e(sm['letter'])))
    rec = ('<div class="rv-rec"><div class="rv-box"><b>The user’s message (recorded in the spec)</b>%s</div><div class="rv-box"><b>The three prompts</b><ol>%s</ol></div>'
           '<div class="rv-box"><b>Transcript</b>%s</div></div>') % (e(t['user_message']), ''.join('<li>%s</li>' % e(p) for p in first['chat']['prompts']), e(t.get('transcript', {}).get('label', '')))
    intro = intro or ('The same turn drawn three ways, so you can pick one. Each sample is drawn by %s from its own spec, using the Solutions part of the Tojo block library '
                      '(the lightbulb, the jigsaw and the route, from solutions_html.py and solutions.css) in Bed Management’s Solutions colours, with the common picking layer '
                      'and entries on top. Try it: pick an item, press Add yours and type, then add a second one on another item. Both land in the chat message.') % GEN
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>'
            '<style>%s</style><style id="rv-top-fonts"></style></head><body><script type="application/json" id="rv-data">%s</script><script type="text/plain" id="rv-fonts">%s</script>'
            '<div class="rv"><h1>%s</h1><p class="rv-intro">%s</p>%s%s</div><script>%s</script></body></html>') % (
        e(title), bmd.REVIEW_CSS, json.dumps(data, ensure_ascii=False).replace('</', '<\\/'), dh.font_css(), e(title), e(intro), rec, ''.join(secs), bmd.REVIEW_JS)

# ============================================================================================ CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate'); v.add_argument('spec')
    r = sub.add_parser('render'); r.add_argument('spec'); r.add_argument('--view', default='desktop', choices=['desktop', 'mobile']); r.add_argument('-o', '--out')
    s = sub.add_parser('samples'); s.add_argument('specs', nargs='+'); s.add_argument('-o', '--out', required=True); s.add_argument('--pages')
    a = ap.parse_args(); reg = load_registry()
    if a.cmd == 'validate':
        spec = json.load(open(a.spec, encoding='utf-8')); errs, warns = validate(spec, reg)
        for x in warns: print('warn:', x)
        for x in errs: print('ERROR:', x)
        print('valid' if not errs else 'INVALID'); sys.exit(1 if errs else 0)
    if a.cmd == 'render':
        spec = json.load(open(a.spec, encoding='utf-8')); errs, _ = validate(spec, reg)
        if errs: print('\n'.join(errs), file=sys.stderr); sys.exit(1)
        out = render_page(spec, a.view, reg); (open(a.out, 'w', encoding='utf-8').write(out) if a.out else sys.stdout.write(out))
    if a.cmd == 'samples':
        specs, bad = [], 0
        for f in a.specs:
            spec = json.load(open(f, encoding='utf-8')); errs, warns = validate(spec, reg)
            print('%-28s %s  theme: %s' % (os.path.basename(f), 'valid' if not errs else 'INVALID', tone_of(spec, reg)))
            for x in errs + warns: print('   ', x)
            bad += bool(errs); specs.append(spec)
        if bad: sys.exit(1)
        if a.pages:
            os.makedirs(a.pages, exist_ok=True)
            for sp in specs:
                for vw in ('desktop', 'mobile'):
                    open(os.path.join(a.pages, '%s-%s.%s.html' % (sp['turn']['id'], sp['turn']['sample']['letter'], vw)), 'w', encoding='utf-8').write(render_page(sp, vw, reg))
        open(a.out, 'w', encoding='utf-8').write(samples_page(specs, reg, '%s · three samples' % specs[0]['turn']['id']))
        print('wrote', a.out)

if __name__ == '__main__':
    main()
