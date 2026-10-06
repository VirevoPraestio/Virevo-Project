#!/usr/bin/env python3
"""
bm_automations_html — the Bed Management Automations generator (v1, 1 Oct 2026).

How it works
  Claude writes one JSON spec per turn: the user's message, the chat parts (text, bullets, Tojo's note, @points,
  three prompts) and the canvas as blocks with slot values. This program validates the spec and draws it. No model
  writes HTML.

  The drawing comes from the Automations part of the Tojo block library (Common Elements/automations-html-generator):
  its renderers and automations.css, with the switch-room motifs of 07 §1.4 (switches, the main switch, lamps, the brain).
  Bed Management's Automations look (the night shift, from the approved landing page) is set through the library's colour
  variables. Every drawing carries the common tool layer (Common Elements/tool-layer/tojo_layer.py): the first item
  raised with its sheet open, each sheet under its item on a phone, entries typed in the drawing and added to the
  chat message. Bed Management's own drawings are in bm_au_blocks.py, built from the library's motifs.

  The page is the Bed Management app shell (bm_common.py). On a phone the turn is one feed: the user's message,
  Tojo's text, the drawing, then the note, points and prompts (rules/08 §4).

  python3 bm_automations_html.py validate SPEC.json
  python3 bm_automations_html.py render SPEC.json --view desktop|mobile -o OUT.html
  python3 bm_automations_html.py samples SPEC.json [SPEC.json ...] -o OUT.html --pages DIR   # one turn, several samples, stacked
Standard library only.
"""
import argparse, copy, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BM = os.path.dirname(HERE)
ROOT = os.path.join(os.path.dirname(BM), 'Common Elements')
SOLG = os.path.join(ROOT, 'automations-html-generator')
sys.path[:0] = [BM, os.path.join(BM, 'diagnosis-html-generator'), SOLG, os.path.join(ROOT, 'diagnosis-html-generator'),
                os.path.join(ROOT, 'landing-common'), os.path.join(ROOT, 'tool-layer')]
import diagnosis_html as dh        # noqa: E402  validator pieces, plain English, fonts
import automations_html as au     # noqa: E402  the library's Automations renderers and motifs
import bm_common as C              # noqa: E402  the Bed Management app shell
import tojo_layer as L             # noqa: E402  the common tool layer
import bm_diagnosis_html as bmd    # noqa: E402  shared Bed Management pieces: chat split, simple English, review page
import bm_au_blocks                # noqa: E402  Bed Management Automations drawings
import bm_au_blocks2               # noqa: E402  more drawings: helper, relay, agent, night shift

REG_PATH = os.path.join(HERE, 'registry.json')
GEN = 'bm_automations_html 1.0'
TOOL, PLACE = 'Bed Management', 'Automations'
e = dh.e
RAIL = ['#DAD9E3', '#E0DFE8', '#D8D7E2', '#DEDDE7', '#D9D8E2']

def load_registry():
    reg = json.load(open(REG_PATH, encoding='utf-8'))
    reg['plain_english'] = dh.load_registry()['plain_english']
    lib = json.load(open(os.path.join(SOLG, 'registry.json'), encoding='utf-8'))
    reg['library_blocks'] = {b['id']: b for b in lib['blocks'] if b['status'] == 'approved' and b.get('scope') in ('all', 'Automations')}
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
    if tone == 'night': k.update({x: reg['tones']['list']['night'][x] for x in ('ground', 'card', 'muted')})
    return C.theme(k['ground'], k['card'], k['ink'], k['muted'], k['line'], k['soft'], k['grey'], RAIL, '12px', '--acc:%s;--accl:#C9C2F5' % k['accent'])

# ============================================================================================ blocks
RENDER = bm_au_blocks.register({'e': e, 'L': L, 'au': au, 'C': C})
RENDER.update(bm_au_blocks2.register())

def block_def(reg, t):
    return reg['own_blocks'].get(t)

ITEM_KEYS = ('sources', 'passes', 'automations', 'items', 'asks', 'legs', 'steps', 'stations')

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
        if not d: errs.append('%s: not a Bed Management Automations block (registry.json)' % path); continue
        dh.check_fields(path, d['slots'], b, errs, warns)
        items = next((b[k] for k in ITEM_KEYS if isinstance(b.get(k), list)), [])
        if b.get('sheets') and t not in ('foundation', 'gap-knots') and len(b['sheets']) != len(items):
            errs.append('%s: %d sheets for %d items; one sheet per item, in order' % (path, len(b['sheets']), len(items)))
        if t == 'sources':
            ids = {x.get('id') for x in b.get('sources', [])} | {b.get('main', {}).get('id')}
            for j, a in enumerate(b.get('automations', [])):
                for x in a.get('needs', []):
                    if x not in ids: errs.append('%s.automations[%d].needs: "%s" is not a record' % (path, j, x))
            for j, p in enumerate(b.get('presets', [])):
                for x in p.get('on', []):
                    if x not in ids: errs.append('%s.presets[%d].on: "%s" is not a record' % (path, j, x))
        if t == 'brain':
            ks = {k.get('k') for k in b.get('kinds', [])}
            for j, o in enumerate(b.get('outputs', [])):
                for k in o.get('from', []):
                    if k not in ks: errs.append('%s.outputs[%d].from: "%s" is not a kind' % (path, j, k))
            for j, p in enumerate(b.get('passes', [])):
                for k in p.get('brings', []):
                    if k not in ks: errs.append('%s.passes[%d].brings: "%s" is not a kind' % (path, j, k))
        if t == 'panel':
            n = len(b.get('phases', []))
            for j, a in enumerate(b.get('automations', [])):
                st = a.get('stages', [])
                if len(st) != n or any(x not in (-1, 0, 1, 2, 3) for x in st): errs.append('%s.automations[%d].stages: one stage (-1 to 3) for each of the %d phases' % (path, j, n))
        if t == 'agent':
            ids = {l.get('id') for l in b.get('loop', [])}
            for j, x in enumerate(b.get('steps', [])):
                for k in x.get('stages', []):
                    if k not in ids: errs.append('%s.steps[%d].stages: "%s" is not on the loop' % (path, j, k))
        keys = [s.get('key') for s in b.get('sheets', [])]
        if len(set(keys)) != len(keys): errs.append('%s: sheet keys must differ' % path)
    if not canvas.get('actions'): errs.append('canvas.actions: the three buttons are on every turn (Proceed with next step, Add more, Jump to the next place)')
    else: dh.check_fields('canvas.actions', reg['actions']['slots']['fields'], canvas['actions'], errs, warns)
    s2 = copy.deepcopy(spec); s2['turn'].pop('user_message', None)
    errs += ['plain English: ' + p for p in dh.plain_check(s2, reg)]
    errs += ['simple English: ' + x for x in bmd.simple_check(spec)] + ['simple English: ' + x for x in au_words(spec)]
    if len(chat.get('prompts', [])) != 3: errs.append('chat.prompts: exactly 3')
    for i, p in enumerate(chat.get('points', [])):
        if p.get('n') != i + 1: errs.append('chat.points[%d].n must be %d' % (i, i + 1))
    for k in ('pointer', 'invite'):
        if chat.get(k) and re.search(r'\b(left|right|above|below|sidebar)\b', chat[k], re.I): errs.append('chat.%s: name the drawing, not where it is' % k)
    rc_errs, rc_warns = bmd.RC.check(spec); errs += rc_errs; warns += rc_warns   # rule 09
    return errs, warns

AU_WORDS = {'api': 'link', 'database': 'records', 'server': 'computer', 'interface': 'screen', 'algorithm': 'rules', 'data': 'records', 'sync': 'keep in step',
            'real-time': 'as it happens', 'realtime': 'as it happens', 'pipeline': 'line', 'integration': 'link', 'integrate': 'link'}
def au_words(spec):
    out = []
    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k not in ('id', 'type', 'k', 'key', 'from', 'needs', 'on', 'brings', 'link', 'state', 'tab'): walk(v, '%s.%s' % (path, k) if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o): walk(v, '%s[%d]' % (path, i))
        elif isinstance(o, str):
            low = ' %s ' % re.sub(r'[^a-z\- ]', ' ', o.lower())
            for w, rep in AU_WORDS.items():
                if ' %s ' % w in low: out.append('%s: “%s” → “%s”' % (path, w, rep))
    walk({'chat': spec.get('chat', {}), 'canvas': spec.get('canvas', {})}, '')
    return out

# ============================================================================================ pages
PAGE_CSS = r'''
.ax-host{container-type:inline-size}
.bm-m .sh-mc > .sh-mpanel{height:auto!important;min-height:0!important;overflow:visible!important}
.bm-m .sh-mc > .ax-host{flex:none}
#tojo-input{resize:none;overflow-y:auto;line-height:1.45}
.sh-box #tojo-input{border:0;outline:0;background:transparent;font:inherit;font-size:15px;flex:1;padding:10px 4px;min-height:24px;max-height:260px}
'''

def render_canvas(spec, reg):
    ctx = dh.Ctx(); ctx.turn = turn_no(spec); ctx.eff = 0
    ctx.sample = ' ABCDEFG'.find((spec['turn'].get('sample') or {}).get('letter', ' ') or ' ')
    ctx.sample = max(ctx.sample, 0)
    inner = ''.join(RENDER[b['type']](b, ctx) for b in spec['canvas']['blocks']) + bm_au_blocks.actions(spec['canvas']['actions'])
    return ('<div class="ax-host" style="container-name:ax tj"><div class="ax" data-theme="bm" data-tone="%s" data-turn="%s" data-generator="%s"><div class="ax-stack">%s</div></div></div>' % (
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
    css = open(au.CSS_PATH, encoding='utf-8').read() + L.CSS + bm_au_blocks.CSS + bm_au_blocks2.CSS + PAGE_CSS
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s · %s %s</title><style>%s</style><style>%s%s%s.bm-app .sh-bar{background:%s}%s</style></head><body>%s<script>%s</script><script>%s</script></body></html>') % (
        e(spec['turn']['id']), TOOL, PLACE, dh.font_css() if fonts else '', C.SHELL_CSS, C.shell_css(th), C.SHELL_V3_CSS, th['ground'], css,
        body, L.RUNTIME, bm_au_blocks.JS + bm_au_blocks2.JS)

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
    intro = intro or ('The same turn drawn three ways, so you can pick one. Each sample is drawn by %s from its own spec, using the Automations part of the Tojo block library '
                      '(the switchboard, the brain and the station panel, from automations_html.py and automations.css) in Bed Management’s Automations colours, with the common picking layer '
                      'and entries on top. Try it: pick an item, press Add yours and type, then add a second one on another item. Both land in the chat message.') % GEN
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>'
            '<style>%s</style><style id="rv-top-fonts"></style></head><body><script type="application/json" id="rv-data">%s</script><script type="text/plain" id="rv-fonts">%s</script>'
            '<div class="rv"><h1>%s</h1><p class="rv-intro">%s</p>%s%s</div><script>%s</script></body></html>') % (
        e(title), bmd.REVIEW_CSS, json.dumps(data, ensure_ascii=False).replace('</', '<\\/'), dh.font_css(), e(title), e(intro), rec, ''.join(secs), bmd.REVIEW_JS)

# ============================================================================================ rules across turns (rules/08 §2, §3)
def book_check(specs, reg):
    return _book(specs, reg)

def _book(specs, reg):
    errs, rep = [], {'heading', 'effect'}
    main, types, seen = {}, {}, {}
    for sp in specs:
        bl = [b['type'] for b in sp['canvas']['blocks']]
        main[sp['turn']['id']] = bl[1] if len(bl) > 1 else 'heading'; types[sp['turn']['id']] = set(bl)
    for i, sp in enumerate(specs):
        tid = sp['turn']['id']
        if main[tid] in seen: errs.append('%s: main block %s is already the main block of %s' % (tid, main[tid], seen[main[tid]]))
        seen.setdefault(main[tid], tid)
        if i:
            prev = specs[i - 1]['turn']['id']; shared = (types[tid] & types[prev]) - rep
            if shared: errs.append('%s: shares %s with the turn before; two turns in a row must look different' % (tid, ', '.join(sorted(shared))))
        if sp.get('canvas', {}).get('tone'): errs.append('%s: specs store no colour' % tid)
    return errs

def build(a, reg):
    man = json.load(open(os.path.join(a.dir, 'turns.json'), encoding='utf-8'))
    specs, bad = [], 0
    for t in man['turns']:
        sp = json.load(open(os.path.join(a.dir, t['file']), encoding='utf-8')); errs, warns = validate(sp, reg)
        print('%-24s %s  theme: %s' % (t['file'][:-5], 'valid' if not errs else 'INVALID', tone_of(sp, reg)))
        for x in errs + warns: print('   ', x)
        bad += bool(errs); sp['turn']['note_for_review'] = t.get('note', ''); specs.append(sp)
    berrs = _book(specs, reg)
    for x in berrs: print('BOOK ERROR:', x)
    if bad or berrs: sys.exit(1)
    pages = os.path.join(a.out, 'pages'); os.makedirs(pages, exist_ok=True)
    for sp in specs:
        for vw in ('desktop', 'mobile'):
            open(os.path.join(pages, '%s.%s.html' % (sp['turn']['id'], vw)), 'w', encoding='utf-8').write(render_page(sp, vw, reg))
    out = os.path.join(a.out, 'automations-turns.html')
    open(out, 'w', encoding='utf-8').write(book_page(specs, reg))
    print('wrote', out)

def book_page(specs, reg):
    data, secs = [], []
    for i, s in enumerate(specs):
        data.append({'desktop': render_page(s, 'desktop', reg, fonts=False), 'mobile': render_page(s, 'mobile', reg, fonts=False)})
        t = s['turn']; q = s['chat'].get('question')
        chips = ''.join('<span class="rv-chip">%s</span>' % e(x) for x in ['Drawn with: ' + ', '.join(b['type'] for b in s['canvas']['blocks'][1:])] + ['Theme: ' + reg['tones']['list'][tone_of(s, reg)]['name']])
        rec = ('<div class="rv-rec" style="margin:0 0 14px"><div class="rv-box"><b>%s · the user’s message</b>%s</div><div class="rv-box"><b>The three prompts</b><ol>%s</ol></div>'
               '<div class="rv-box"><b>The question</b>%s</div></div>') % (e(t.get('transcript', {}).get('label', '')), e(t['user_message']), ''.join('<li>%s</li>' % e(p) for p in s['chat']['prompts']),
                ('%s<ol>%s</ol>' % (e(q['text']), ''.join('<li>%s</li>' % e(o) for o in q['options']))) if q else 'None. The user answers in their own words.')
        title = s['canvas']['blocks'][0]['title']
        secs.append(('<section class="rv-s" id="%s" data-i="%d"><div class="rv-sh"><h2>%s · %s</h2>%s</div><p class="rv-what">%s</p>%s'
                     '<div class="rv-views"><div><div class="rv-lab">Desktop · 1440 × 900 · scroll inside it</div><div class="rv-screen"><iframe data-v="desktop" title="%s on desktop"></iframe></div></div>'
                     '<div><div class="rv-lab">Phone · 390 × 844 · scroll inside it</div><div class="rv-hand"><iframe data-v="mobile" title="%s on a phone"></iframe></div></div></div></section>') % (
            e(t['id']), i, e(t['id']), e(title), chips, e(t.get('note_for_review', '')), rec, e(t['id']), e(t['id'])))
    nav = '<nav class="rv-jump">%s</nav>' % ''.join('<a href="#%s">%s</a>' % (e(s['turn']['id']), e(s['turn']['id'])) for s in specs)
    intro = ('%d turns, in conversation order, each drawn by %s from its spec, with the Automations templates of the block library in Bed Management’s Automations colours and the common tool layer. '
             'Every turn ends with the three buttons: Proceed with next step, Add more, Jump to Processes. The background changes every four turns.') % (len(specs), GEN)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bed Management · Automations turns</title>'
            '<style>%s</style><style id="rv-top-fonts"></style></head><body><script type="application/json" id="rv-data">%s</script><script type="text/plain" id="rv-fonts">%s</script>'
            '<div class="rv"><h1>Bed Management · Automations turns</h1><p class="rv-intro">%s</p>%s%s</div><script>%s</script></body></html>') % (
        bmd.REVIEW_CSS, json.dumps(data, ensure_ascii=False).replace('</', '<\\/'), dh.font_css(), e(intro), nav, ''.join(secs), bmd.REVIEW_JS)

# ============================================================================================ CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate'); v.add_argument('spec')
    r = sub.add_parser('render'); r.add_argument('spec'); r.add_argument('--view', default='desktop', choices=['desktop', 'mobile']); r.add_argument('-o', '--out')
    s = sub.add_parser('samples'); s.add_argument('specs', nargs='+'); s.add_argument('-o', '--out', required=True); s.add_argument('--pages')
    bd = sub.add_parser('build'); bd.add_argument('dir', nargs='?', default=os.path.join(BM, 'examples', 'automations')); bd.add_argument('-o', '--out', default=os.path.join(BM, 'out', 'automations'))
    a = ap.parse_args(); reg = load_registry()
    if a.cmd == 'build': build(a, reg)
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
