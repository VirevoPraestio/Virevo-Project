#!/usr/bin/env python3
"""
bm_diagnosis_html — the Bed Management Diagnosis generator (v2, 30 Sep 2026).

How it works
  Claude writes one JSON spec per turn: the user's message, the chat parts (text, Tojo's note, @points, one
  question, three prompts) and the canvas as blocks with slot values. This program validates the spec and draws it.
  No model writes HTML.

  The drawing comes from the approved Tojo block library: the block renderers in diagnosis_html.py and the
  stylesheet tojo.css, listed in blocks/registry.json. Only blocks whose scope is "all" and status "approved" may be
  used (07 §1.3 scope, §9.3). They are redrawn in Bed Management's own look by setting the library's colour
  variables (07 §1.1 "colour lives in variables"), never by copying another tool's colours.

  On top of a library block, Bed Management adds one layer (registry.json "layers"):
    * sheets  — each item of the drawing (an event, a step, a row) can be picked. The first is raised with its
                sheet open; on a phone each sheet opens right under its item, on desktop one shared sheet.
    * entries — "Add yours" opens a field inside the sheet. Whatever is typed is written into the chat message
                with the place it came from. Each new entry is added to the message; none replaces another.

  python3 bm_diagnosis_html.py validate SPEC.json
  python3 bm_diagnosis_html.py render SPEC.json --view desktop|mobile -o OUT.html
  python3 bm_diagnosis_html.py samples SPEC.json [SPEC.json ...] -o OUT.html   # one turn, several samples, stacked
  python3 bm_diagnosis_html.py prompt
Standard library only.
"""
import argparse, copy, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BM = os.path.dirname(HERE)
ROOT = os.path.join(os.path.dirname(BM), 'Common Elements')     # shared: block library, rules, generators, tool layer
DIAG = os.path.join(ROOT, 'diagnosis-html-generator')
sys.path[:0] = [BM, DIAG, os.path.join(ROOT, 'landing-common'), os.path.join(ROOT, 'tool-layer')]
import diagnosis_html as dh                    # noqa: E402  the approved block renderers, validator pieces and fonts
import bm_common as C                          # noqa: E402  the Bed Management app shell and bed mark
from preview import chat_parts                 # noqa: E402
import tojo_layer as L                         # noqa: E402  the common tool layer: picking and entries

REG_PATH = os.path.join(HERE, 'registry.json')
GEN = 'bm_diagnosis_html 2.0'
TOOL, PLACE = 'Bed Management', 'Diagnosis'
e = dh.e
RAIL = ['#D6DDE8', '#E1E7EF', '#D8DEE9', '#DDE2EC', '#D6DCE6']

# ============================================================================================ registry
def load_registry():
    reg = json.load(open(REG_PATH, encoding='utf-8'))
    lib = dh.load_registry()
    reg['plain_english'] = lib['plain_english']
    reg['library_blocks'] = {b['id']: b for b in lib['blocks'] if b.get('scope', 'all') == 'all' and b['status'] == 'approved'}
    reg['own_blocks'] = {b['id']: b for b in reg['blocks']}
    return reg

def block_def(reg, t):
    if t in reg['own_blocks']: return reg['own_blocks'][t]
    b = reg['library_blocks'].get(t)
    if not b: return None
    if t in reg['layers']['applies_to']:
        b = copy.deepcopy(b)
        b['slots']['sheets'] = reg['layers']['sheets']; b['slots']['ask_more'] = reg['layers']['ask_more']
    return b

# ============================================================================================ theme
def turn_no(spec):
    m = re.search(r'(\d+)$', spec['turn'].get('id', '1')); return int(m.group(1)) if m else 1

def tone_of(spec, reg):
    if spec.get('canvas', {}).get('tone'): return spec['canvas']['tone']
    t = reg['tones']; return t['rotation'][((max(turn_no(spec), 1) - 1) // t['set_size']) % len(t['rotation'])]

def theme_css(reg):
    k = reg['theme']['tokens']
    base = ('.tj[data-theme="bm"]{--ground:%(ground)s;--card:%(card)s;--ink:%(ink)s;--muted:%(muted)s;--faint:%(faint)s;--gold-text:%(gold_text)s;'
            '--red:%(red)s;--green:%(green)s;--later:%(later)s;--paper:%(paper)s;--st-plain:%(ink)s;--st-target:%(target)s;--st-outcome:%(red)s;'
            '--st-start:%(green)s;--acc:%(accent)s;--shadow:%(shadow)s}') % k
    lamp = reg['tones']['list']['lamp']
    base += ('.tj[data-theme="bm"][data-tone="lamp"]{--ground:%s;--card:%s;--paper:%s;--muted:%s;--faint:%s;'
             'background-image:radial-gradient(rgba(26,43,69,.10) 1px,transparent 1.3px);background-size:18px 18px}') % (
        lamp['ground'], lamp['card'], lamp['card'], lamp['muted'], lamp['faint'])
    return base

def shell_theme(reg, tone):
    k = dict(reg['theme']['tokens'])
    if tone == 'lamp': k.update({x: reg['tones']['list']['lamp'][x] for x in ('ground', 'card', 'muted')})
    return C.theme(k['ground'], k['card'], k['ink'], k['muted'], '#B2BED0', '#E9EFF7', k['later'], RAIL, '6px', '--acc:%s' % k['accent'])

# ============================================================================================ the Bed Management layer
BED_WORD = {'in': 'Patient in the bed', 'leaving': 'Patient still in the bed', 'empty': 'Bed empty', 'next': 'Next patient in'}
BILL_WORD = {'on': 'Billing', 'off': 'Nothing billing', 'new': 'New bill open'}

def bedmark(state, size=30):
    return '<span class="bm-bed bm-bed-%s" aria-hidden="true">%s</span>' % (state, C.bed_svg(size))

pick_attrs = L.pick_attrs

def sheet(s, grp, first, where):
    entry = L.entry('%s · %s' % (s['when'], s['title']), s['entry'], s.get('entry_hint', 'Type what is different here')) if s.get('entry') else ''
    kv = ('<div class="bm-kv"><div class="bm-kv-r"><span class="tj-label">The bed</span>%s<b>%s</b></div>'
          '<div class="bm-kv-r bill-%s"><span class="tj-label">The bill</span><span class="bm-billmark" aria-hidden="true"></span><b>%s</b></div></div>') % (
        bedmark(s['bed'], 22), e(s['bed_line']), e(s['bill']), e(s['bill_line']))
    inner = ('<div><div class="bm-sh-hd"><span class="tj-label bm-when">%s</span></div><h3 class="tj-big">%s</h3><p class="tj-text">%s</p>%s</div>%s') % (
        e(s['when']), e(s['title']), e(s['text']), kv, '<div>%s</div>' % entry if entry else '')
    tag = 'li' if where == 'mob-li' else 'div'
    w = 'mob' if where.startswith('mob') else 'desk'
    return '<%s class="bx bx-%s tj-card tj-shadow tj-callout bm-sheet%s" data-box="%s:%s"%s>%s</%s>' % (
        tag, w, '' if entry else ' one', grp, e(s['key']), '' if first else ' hidden', inner, tag)

def ask_more(b):
    a = b.get('ask_more')
    return L.entry('Anything else about our setup', a['label'], a['hint'], 'tl-more-entry tj-card') if a else ''

hint = L.hint

# ---- library block, with the layer.  Markup and classes are the library's own (diagnosis_html.py v1), so tojo.css draws it.
def r_time_window(b, ctx):
    sheets = b.get('sheets')
    if not sheets: return dh.r_time_window(b, ctx)
    grp = ctx.uid('bmtw')
    html = dh.r_time_window(b, ctx)
    evs = sorted(range(len(b['events'])), key=lambda i: b['events'][i]['time'])
    first = 0
    # desktop: each event on the line becomes pickable
    parts = html.split('<div class="ev ')
    out = parts[0]
    for n, p in enumerate(parts[1:]):
        s = sheets[evs[n]]
        out += '<div role="button" tabindex="0"%s data-tw-ev><div class="ev ' % pick_attrs(grp, s['key'], n == first, 'bm-ev') + p
    html = out
    # the wrapper divs must close: add one </div> after each event's own closing (event markup ends with </span></div></div>)
    html = re.sub(r'(<div role="button" tabindex="0"[^>]*data-tw-ev><div class="ev [^>]*><i></i><div class="lab"><b>[^<]*</b><span>[^<]*</span></div></div>)', r'\1</div>', html)
    # phone: each event row is pickable, and its sheet opens right under it
    parts = html.split('<li class="vev"')
    out = parts[0]
    for n, p in enumerate(parts[1:]):
        s = sheets[evs[n]]
        close = p.index('</li>') + 5
        out += '<li%s' % pick_attrs(grp, s['key'], n == first, 'vev').replace(' class="tl-pick', ' tabindex="0" role="button" class="tl-pick') + p[:close] + sheet(s, grp, n == first, 'mob-li') + p[close:]
    html = out
    desk = '<div class="bx-desk-wrap">%s</div>' % ''.join(sheet(sheets[evs[n]], grp, n == first, 'desk') for n in range(len(evs)))
    html = html.replace('</ol></div>', '</ol></div>' + hint('Tap a moment on the line to see what happens to the bed and the bill.') + desk, 1)
    return html.replace('</section>', ask_more(b) + '</section>')

def r_chain(b, ctx):
    sheets = b.get('sheets')
    if not sheets: return dh.r_chain(b, ctx)
    grp = ctx.uid('bmch'); steps = b['steps']; parts, desk = [], []
    if b.get('zone'): parts.append('<div class="zone">%s</div>' % e(b['zone']))
    for i, s in enumerate(steps):
        sh = sheets[i]; first = i == 0
        state = s.get('state') or ('outcome' if i == len(steps) - 1 else 'plain')
        flag = '<span class="tj-tag flag">%s</span>' % e(s['flag']) if s.get('flag') else ''
        val = '<div class="tj-val">%s</div>' % e(s['value']) if s.get('value') else ''
        parts.append('<button type="button"%s data-state="%s"%s>%s%s<div class="t">%s</div>%s<span class="bm-billtag bill-%s">%s</span></button>%s' % (
            pick_attrs(grp, sh['key'], first, 'box'), e(state), dh.pt(s), flag, bedmark(sh['bed']), e(s['title']), val, e(sh['bill']), e(BILL_WORD[sh['bill']]),
            sheet(sh, grp, first, 'mob')))
        desk.append(sheet(sh, grp, first, 'desk'))
    label = '<div class="tj-label">%s</div>' % e(b['label']) if b.get('label') else ''
    return ('<section class="tj-block bm-chain" data-block="chain" style="display:flex;flex-direction:column;gap:14px">%s<div class="tj-chain%s">%s</div>%s'
            '<div class="bx-desk-wrap">%s</div>%s%s</section>') % (
        label, ' long' if len(steps) > 5 else '', '<span class="arr" aria-hidden="true">→</span>'.join(parts),
        hint('Tap a step to see what happens to the bed and the bill.'), ''.join(desk), dh.divider(b.get('caption')), ask_more(b))

def r_two_flow(b, ctx):
    sheets = b.get('sheets')
    if not sheets: return dh.r_two_flow(b, ctx)
    grp = ctx.uid('bm2f')
    cells = ['<div></div><div class="hd">%s</div><div class="hd">%s</div>' % (e(b['left_title']), e(b['right_title']))]
    desk = []
    for i, r in enumerate(b['rows']):
        sh = sheets[i]; first = i == 0
        lv = '<div class="tj-val">%s</div>' % e(r['left_value']) if r.get('left_value') else ''
        rv = '<div class="tj-val">%s</div>' % e(r['right_value']) if r.get('right_value') else ''
        flag = '<span class="tj-tag flag">%s</span>' % e(r['flag']) if r.get('flag') else ''
        cells.append('<button type="button"%s%s><span class="bm-rl-t">%s</span><span class="bm-rl-go" aria-hidden="true"></span></button>' % (pick_attrs(grp, sh['key'], first, 'rl'), dh.pt(r), e(r['label'])))
        cells.append('<div class="cell bm-bedcell%s" data-state="%s">%s%s<span class="ct">%s</span><span class="t">%s</span>%s</div>' % (
            ' flagged' if flag else '', e(r.get('left_state') or ('target' if flag else 'plain')), flag, bedmark(sh['bed'], 26), e(b['left_title']), e(r['left']), lv))
        cells.append('<div class="cell bm-billcell bill-%s" data-state="%s"><span class="ct">%s</span><span class="bm-billmark" aria-hidden="true"></span><span class="t">%s</span>%s</div>' % (
            e(sh['bill']), e(r.get('right_state') or 'plain'), e(b['right_title']), e(r['right']), rv))
        cells.append(sheet(sh, grp, first, 'mob').replace('class="bx bx-mob', 'style="grid-column:1/-1" class="bx bx-mob', 1))
        desk.append(sheet(sh, grp, first, 'desk'))
    return ('<section class="tj-block bm-2f" data-block="two-flow" style="display:flex;flex-direction:column;gap:14px"><div class="tj-2f">%s</div>%s'
            '<div class="bx-desk-wrap">%s</div>%s%s</section>') % (''.join(cells), hint('Tap a time of day to see it on the bed and on the bill.'), ''.join(desk), dh.divider(b.get('caption')), ask_more(b))

def r_effect(b, ctx):
    return ('<section class="tj-block bm-effect" data-block="effect" data-state="%s"><div class="bm-eff-mark" aria-hidden="true">%s<span class="bm-eff-line"></span>'
            '<span class="bm-billmark"></span></div><div class="bm-eff-body"><div class="tj-label">%s</div><div class="tj-big bm-eff-v">%s</div><p class="tj-text">%s</p></div></section>') % (
        e(b.get('state', 'plain')), bedmark('empty', 34), e(b['label']), e(b['value']), e(b['sub']))

RENDER = dict(dh.RENDER)
RENDER.update({'time-window': r_time_window, 'chain': r_chain, 'two-flow': r_two_flow, 'effect': r_effect})

# ============================================================================================ validation
SIMPLE = {'via': 'through', 'ensure': 'make sure', 'prior to': 'before', 'additional': 'more', 'approximately': 'about', 'obtain': 'get',
          'require': 'need', 'regarding': 'about', 'assist': 'help', 'initiate': 'start', 'implement': 'put in place', 'optimal': 'best',
          'enable': 'let', 'allocate': 'give', 'allocation': 'giving a bed', 'isolated': 'measured on its own', 'documentation': 'paperwork',
          'billable': 'charged', 'adequate': 'enough', 'diagnostics': 'tests and scans'}
SKIP = {'id', 'type', 'register', 'tool', 'tab', 'context', 'source', 'status', 'state', 'mode', 'key', 'bed', 'bill', 'user_tag', 'user_message',
        'user_words', 'transcript', 'redraw_of', 'tone', 'sample', 'review'}

def simple_check(spec):
    out = []
    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k not in SKIP: walk(v, '%s.%s' % (path, k) if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o): walk(v, '%s[%d]' % (path, i))
        elif isinstance(o, str) and o.strip():
            for sent in re.split(r'(?<=[.?!])\s+', o):
                if len(sent.split()) > 20: out.append('%s: a sentence of %d words; keep each under 21' % (path, len(sent.split())))
            if re.search(r'\s[—–]\s|;', o): out.append('%s: a dash or semicolon joins two thoughts' % path)
            if re.search(r'\btabs?\b', o, re.I): out.append('%s: never say “tab”' % path)
            if re.search(r'\bgraphic\b', o, re.I): out.append('%s: name the drawing instead of “graphic”' % path)
            low = ' %s ' % re.sub(r'[^a-z ]', ' ', o.lower())
            for w, rep in SIMPLE.items():
                if ' %s ' % w in low: out.append('%s: “%s” → “%s”' % (path, w, rep))
    walk({'chat': spec.get('chat', {}), 'canvas': spec.get('canvas', {})}, '')
    return out

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
        if not d:
            errs.append('%s: not an approved library block with scope "all", nor a Bed Management block' % path); continue
        dh.check_fields(path, d['slots'], b, errs, warns)
        items = b.get('events') or b.get('steps') or b.get('rows') or []
        if b.get('sheets') and len(b['sheets']) != len(items):
            errs.append('%s: %d sheets for %d items; one sheet per item, in order' % (path, len(b['sheets']), len(items)))
        if t == 'time-window' and b.get('sheets') and [x['time'] for x in items] != sorted(x['time'] for x in items):
            errs.append('%s: list the events in time order' % path)
    s2 = copy.deepcopy(spec); s2['turn'].pop('user_message', None)
    errs += ['plain English: ' + p for p in dh.plain_check(s2, reg)]
    errs += ['simple English: ' + x for x in simple_check(spec)]
    if len(chat.get('prompts', [])) != 3: errs.append('chat.prompts: exactly 3')
    for i, p in enumerate(chat.get('points', [])):
        if p.get('n') != i + 1: errs.append('chat.points[%d].n must be %d' % (i, i + 1))
    for k in ('pointer', 'invite'):
        if chat.get(k) and re.search(r'\b(left|right|above|below|sidebar)\b', chat[k], re.I): errs.append('chat.%s: name the drawing, not where it is' % k)
    return errs, warns

# ============================================================================================ runtime (picking, entries, chat)
RUNTIME = L.RUNTIME

LAYER_CSS = L.CSS + r'''
/* ---- Bed Management look on the library blocks ---- */
.tj[data-theme="bm"] .tj-eyebrow{color:var(--acc)}
.tj[data-theme="bm"] .tj-shadow{box-shadow:8px 8px 0 var(--shadow)}
.tj[data-theme="bm"] .tj-chain .zone{background:repeating-linear-gradient(135deg,rgba(26,43,69,.08) 0 6px,transparent 6px 12px)}
.tj[data-theme="bm"] .tj-tw .win{border-color:var(--red);background:repeating-linear-gradient(135deg,rgba(142,47,28,.14) 0 6px,transparent 6px 12px)}
.tj[data-theme="bm"] .tj-tw .win .wl b{color:var(--red)}
.tj[data-theme="bm"] .tj-twv .vwin{border-color:var(--red)!important;background:repeating-linear-gradient(135deg,rgba(142,47,28,.12) 0 6px,transparent 6px 12px)!important}
.tj[data-theme="bm"] .tj-twv .vwin b{color:var(--red)!important}
/* bed mark (from the Bed Management home page) */
.bm-bed{display:inline-flex;flex-shrink:0}
.bm-bed svg .h{fill:var(--ink)}.bm-bed svg .f{fill:var(--card);stroke:var(--ink);stroke-width:2.2}.bm-bed svg .p{fill:var(--ground);stroke:var(--ink);stroke-width:1.4}.bm-bed svg .k{fill:var(--ink)}
.bm-bed-leaving svg .k{fill:var(--st-target)}
.bm-bed-empty svg .f{fill:transparent;stroke:var(--st-target);stroke-dasharray:4 3}.bm-bed-empty svg .k{fill:none}.bm-bed-empty svg .p{fill:transparent;stroke:var(--st-target)}.bm-bed-empty svg .h{fill:var(--st-target)}
.bm-bed-next svg .k{fill:var(--green)}.bm-bed-next svg .h{fill:var(--green)}
.bm-billmark{display:inline-block;width:14px;height:18px;flex-shrink:0;border:2px solid var(--ink);border-radius:2px;background:linear-gradient(var(--ink) 0 0) 3px 4px/6px 2px no-repeat,linear-gradient(var(--ink) 0 0) 3px 8px/6px 2px no-repeat}
.bill-off .bm-billmark{border-color:var(--red);border-style:dashed;background:none}
.bill-new .bm-billmark{border-color:var(--green);background:linear-gradient(var(--green) 0 0) 3px 4px/6px 2px no-repeat,linear-gradient(var(--green) 0 0) 3px 8px/6px 2px no-repeat}
/* sheets reuse the library callout (tj-card tj-shadow tj-callout) */
.bm-sheet{border-left:6px solid var(--gold)!important}
.bm-sheet.one{grid-template-columns:1fr}
.bm-sheet .bm-when{color:var(--acc)}
.bm-sheet h3.tj-big{font-size:34px;margin:0}
.bm-kv{display:flex;flex-direction:column;gap:8px;margin-top:4px;padding-top:12px;border-top:1px solid var(--faint)}
.bm-kv-r{display:grid;grid-template-columns:78px 26px minmax(0,1fr);align-items:center;gap:8px;font-size:14px}
.bm-kv-r .tj-label{font-size:11px}
.bm-kv-r.bill-off b{color:var(--red)}.bm-kv-r.bill-new b{color:var(--green)}
.bm-kv-r .bm-billmark{justify-self:center}
/* time-window: each moment on the line is pickable */
.bm-ev.tl-pick,.bm-ev.tl-pick.is-up{position:absolute;left:0;top:0;width:100%;height:0}
.bm-ev .ev .lab{cursor:pointer;padding:4px 8px;border-radius:6px;background:transparent;transition:transform .18s,box-shadow .18s,background .18s}
.bm-ev.is-up{transform:none;box-shadow:none!important;background:transparent!important}
.bm-ev.is-up .ev .lab{transform:translateY(-4px);background:#FFF8E6;box-shadow:0 0 0 2.5px var(--gold),0 6px 0 -1px rgba(26,43,69,.2),0 14px 22px -8px rgba(26,43,69,.3)}
.bm-ev.is-up .ev i{background:var(--gold);border-color:var(--ink)}
.tj-tw .bm-ev .ev{pointer-events:auto}
.tj-twv li.tl-pick{border-radius:8px;padding:6px 8px}
.tj-twv li.tl-pick.is-up{transform:none}
/* chain: boxes are buttons, with the bed and the bill in each */
.bm-chain .tj-chain .box{text-align:left;font:inherit;color:inherit}
.bm-chain .tj-chain .box .bm-bed{margin-bottom:2px}
.bm-billtag{display:inline-flex;align-self:flex-start;margin-top:auto;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;padding:2px 8px;border-radius:10px;border:1.5px solid var(--ink)}
.bm-billtag.bill-off{border:1.5px dashed var(--red);color:var(--red)}.bm-billtag.bill-new{border-color:var(--green);color:var(--green)}
.bm-chain .bx-desk-wrap{margin-top:6px}
/* two-flow: the time of day is the picker */
.bm-2f .tj-2f .rl{display:flex;align-items:center;justify-content:space-between;gap:6px;text-align:left;font:inherit;font-size:13px;font-weight:600;color:var(--ink);background:var(--card);border:2px solid var(--ink);border-radius:6px;padding:10px 10px;min-height:44px}
.bm-rl-go{width:8px;height:8px;border-right:2.5px solid currentColor;border-bottom:2.5px solid currentColor;transform:rotate(-45deg);flex-shrink:0}
.bm-2f .cell{flex-direction:row!important;align-items:center;gap:10px!important}
.bm-2f .cell .t{flex:1}
.bm-2f .bm-billcell.bill-off{border-style:dashed;border-color:var(--red)}.bm-2f .bm-billcell.bill-off .t{color:var(--red)}
.bm-2f .bm-billcell.bill-new{border-color:var(--green)}
/* effect box: the different fill of 07 §5.2 */
.bm-effect{display:flex;flex-direction:row;align-items:center;gap:22px;padding:20px 24px;background:#EDE3D9;border:2px solid var(--ink)}
.bm-effect[data-state="outcome"]{border-color:var(--red)}
.bm-eff-mark{display:flex;align-items:center;gap:8px;flex-shrink:0}
.bm-eff-line{width:46px;border-top:3px dashed var(--red)}
.bm-effect .bm-billmark{border-color:var(--red);border-style:dashed;background:none}
.bm-eff-body{display:flex;flex-direction:column;gap:6px}
.bm-eff-v{font-size:44px;color:var(--ink)}
.bm-effect[data-state="outcome"] .bm-eff-v{color:var(--red)}
.bm-effect .tj-text{color:var(--ink)}
@container tj (max-width:699px){
 .bm-sheet{position:relative}
 .bm-sheet::before{content:"";position:absolute;left:24px;top:-10px;width:16px;height:16px;background:var(--card);border-left:1.5px solid var(--ink);border-top:1.5px solid var(--ink);transform:rotate(45deg)}
 .bm-sheet h3.tj-big{font-size:28px}
 .bm-effect{flex-direction:column;align-items:flex-start;gap:12px;padding:16px}
 .bm-eff-v{font-size:36px}
 .bm-2f .tj-2f .rl{grid-column:1/-1;border-top:2px solid var(--ink)}
 .bm-chain .tj-chain .box{flex-direction:row!important;flex-wrap:wrap;align-items:center}
 .bm-chain .tj-chain .box .t{flex:1 1 60%}
 .bm-chain .bm-billtag{margin-top:0}
 li.bx-mob{list-style:none}
}
@media (prefers-reduced-motion:reduce){.tl-pick,.tl-pick.is-up,.bm-ev .lab{transition:none;transform:none!important}}
/* phone feed: user's message, Tojo's text, the drawing, then the rest */
.bm-m .sh-mc > .sh-mpanel{height:auto!important;min-height:0!important;overflow:visible!important}
.bm-m .sh-mc > .tj{flex:none}
#tojo-input{resize:none;overflow-y:auto;line-height:1.45}
.sh-box #tojo-input{border:0;outline:0;background:transparent;font:inherit;font-size:15px;flex:1;padding:10px 4px;min-height:24px;max-height:260px}
'''

# ============================================================================================ pages
def render_canvas(spec, reg):
    ctx = dh.Ctx()
    inner = ''.join(RENDER[b['type']](b, ctx) for b in spec['canvas']['blocks'])
    return '<div class="tj" data-theme="bm" data-tone="%s" data-turn="%s" data-generator="%s"><div class="tj-stack">%s</div></div>' % (
        tone_of(spec, reg), e(spec['turn']['id']), GEN, inner)

def split_chat(chat):
    whole = chat_parts(chat); cut = whole.index('</div>') + 6
    return whole[:cut], whole[cut:]

def user_bubble(spec):
    t = spec['turn']
    return '<div class="sh-um">%s%s</div>' % ('<b>%s</b>' % e(t['user_tag']) if t.get('user_tag') else '', e(t['user_message']))

def render_page(spec, view, reg, fonts=True):
    tone = tone_of(spec, reg); th = shell_theme(reg, tone)
    canvas = render_canvas(spec, reg)
    text, rest = split_chat(spec['chat'])
    if view == 'desktop':
        body = C.desktop(th, PLACE, canvas, user_bubble(spec) + text + rest)
    else:
        body = C.mobile(th, PLACE, '@@CANVAS@@', '@@CHAT@@')
        body = body.replace('<div class="sh-mc">', '<div class="sh-mc">' + user_bubble(spec), 1)
        body = body.replace('@@CANVAS@@<div class="sh-mpanel">@@CHAT@@</div>',
                            '<div class="sh-mpanel bm-mt">%s</div>%s<div class="sh-mpanel bm-mr">%s</div>' % (text, canvas, rest))
        body = re.sub(r'<input id="tojo-input"[^>]*>', '<textarea id="tojo-input" rows="1" placeholder="Write to Tojo…"></textarea>', body)
    css = dh.asset('tojo.css') + theme_css(reg) + LAYER_CSS
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s · %s %s</title><style>%s</style><style>%s%s%s.bm-app .sh-bar{background:%s}%s</style></head><body>%s<script>%s</script><script>%s</script></body></html>') % (
        e(spec['turn']['id']), TOOL, PLACE, dh.font_css() if fonts else '', C.SHELL_CSS, C.shell_css(th), C.SHELL_V3_CSS, th['ground'], css,
        body, dh.asset('tojo.js'), RUNTIME)

# ============================================================================================ review page: samples of one turn, stacked
REVIEW_CSS = r'''
:root{--bg:#EEF1F5;--panel:#FFFFFF;--ink:#1A2B45;--muted:#56637C;--line:#CBD3DF;--accent:#2F5E9E}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151D;--panel:#19212C;--ink:#E6EBF2;--muted:#9BA8BA;--line:#2B3645;--accent:#8DB2E6;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#10151D;--panel:#19212C;--ink:#E6EBF2;--muted:#9BA8BA;--line:#2B3645;--accent:#8DB2E6;color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Poppins','Segoe UI',system-ui,sans-serif}
.rv{box-sizing:border-box;max-width:1880px;margin:0 auto;padding:22px 16px 80px}
.rv *{box-sizing:border-box}
.rv h1{margin:0;font-family:'Bebas Neue','Arial Narrow',sans-serif;font-weight:400;font-size:46px;line-height:.95}
.rv-intro{margin:8px 0 0;font-size:13.5px;line-height:1.6;color:var(--muted);max-width:1000px}
.rv-rec{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:14px}
.rv-box{background:var(--panel);border:1.5px solid var(--line);border-radius:8px;padding:10px 12px;font-size:13px;line-height:1.5}
.rv-box b{display:block;font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin-bottom:3px}
.rv-box ol{margin:0;padding-left:18px}
.rv-s{padding:34px 0 30px;border-top:1.5px dashed var(--line);margin-top:26px}
.rv-sh{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:6px}
.rv-sh h2{margin:0;font-family:'Bebas Neue','Arial Narrow',sans-serif;font-weight:400;font-size:36px;line-height:1}
.rv-chip{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:12px;background:var(--panel);border:1.5px solid var(--line)}
.rv-what{margin:0 0 14px;font-size:14px;line-height:1.55;max-width:980px}
.rv-views{display:grid;grid-template-columns:minmax(0,1fr) 410px;gap:20px;align-items:start}
.rv-lab{font-size:11.5px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.rv-screen{position:relative;width:100%;overflow:hidden;border-radius:10px;border:1.5px solid var(--line);background:#fff}
.rv-screen iframe{position:absolute;left:0;top:0;width:1440px;height:900px;border:0;transform-origin:0 0}
.rv-hand{width:410px;max-width:100%;border:10px solid #1b2129;border-radius:36px;overflow:hidden;background:#fff}
.rv-hand iframe{display:block;width:390px;height:844px;border:0}
@media (max-width:1180px){.rv-views{grid-template-columns:minmax(0,1fr)}.rv-rec{grid-template-columns:1fr}.rv-hand{justify-self:center}}
@media (max-width:640px){.rv-hand{width:100%;border-width:6px;border-radius:24px}.rv-hand iframe{width:100%}}
'''
REVIEW_JS = r'''
(function(){
  var T=JSON.parse(document.getElementById('rv-data').textContent),F=document.getElementById('rv-fonts').textContent;
  document.getElementById('rv-top-fonts').textContent=F;
  function fit(){[].slice.call(document.querySelectorAll('.rv-screen')).forEach(function(s){var sc=Math.min(1,s.clientWidth/1440);s.querySelector('iframe').style.transform='scale('+sc+')';s.style.height=Math.ceil(900*sc)+'px';});}
  [].slice.call(document.querySelectorAll('.rv-s')).forEach(function(s){var t=T[+s.getAttribute('data-i')];
    [].slice.call(s.querySelectorAll('iframe[data-v]')).forEach(function(f){f.srcdoc=t[f.getAttribute('data-v')].replace('</head>','<style>'+F+'</style></head>');});});
  fit();window.addEventListener('resize',fit);
})();
'''

def samples_page(specs, reg, title):
    first = specs[0]; t = first['turn']; q = first['chat'].get('question')
    data, secs = [], []
    for i, s in enumerate(specs):
        sm = s['turn'].get('sample', {})
        data.append({'desktop': render_page(s, 'desktop', reg, fonts=False), 'mobile': render_page(s, 'mobile', reg, fonts=False)})
        blocks = [b['type'] for b in s['canvas']['blocks'][1:]]
        chips = ''.join('<span class="rv-chip">%s</span>' % e(x) for x in
                        ['Library block: ' + ', '.join(b for b in blocks if b in reg['library_blocks'])] +
                        ['Bed Management block: ' + ', '.join(b for b in blocks if b in reg['own_blocks'])] + ['Theme: ' + reg['tones']['list'][tone_of(s, reg)]['name']])
        secs.append(('<section class="rv-s" data-i="%d"><div class="rv-sh"><h2>Sample %s · %s</h2>%s</div><p class="rv-what">%s</p>'
                     '<div class="rv-views"><div><div class="rv-lab">Desktop · 1440 × 900 · scroll inside it</div><div class="rv-screen"><iframe data-v="desktop" title="Sample %s on desktop"></iframe></div></div>'
                     '<div><div class="rv-lab">Phone · 390 × 844 · scroll inside it</div><div class="rv-hand"><iframe data-v="mobile" title="Sample %s on a phone"></iframe></div></div></div></section>') % (
            i, e(sm.get('letter', '')), e(sm.get('name', '')), chips, e(sm.get('what', '')), e(sm.get('letter', '')), e(sm.get('letter', ''))))
    rec = ('<div class="rv-rec"><div class="rv-box"><b>The user’s message (recorded in the spec)</b>%s</div><div class="rv-box"><b>The three prompts</b><ol>%s</ol></div>'
           '<div class="rv-box"><b>Transcript</b>%s</div></div>') % (e(t['user_message']), ''.join('<li>%s</li>' % e(p) for p in first['chat']['prompts']), e(t.get('transcript', {}).get('label', '')))
    fonts = dh.font_css()
    intro = ('The same turn drawn three ways, so you can pick one. Each sample is drawn by %s from its own spec, using the approved Tojo block library '
             '(diagnosis_html.py and tojo.css) in Bed Management’s colours, with the Bed Management picking layer and entries on top. '
             'Try it: tap a moment, press Add yours, type something, then add a second one. Both land in the chat message.') % GEN
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>'
            '<style>%s</style><style id="rv-top-fonts"></style></head><body><script type="application/json" id="rv-data">%s</script><script type="text/plain" id="rv-fonts">%s</script>'
            '<div class="rv"><h1>%s</h1><p class="rv-intro">%s</p>%s%s</div><script>%s</script></body></html>') % (
        e(title), REVIEW_CSS, json.dumps(data, ensure_ascii=False).replace('</', '<\\/'), fonts, e(title), e(intro), rec, ''.join(secs), REVIEW_JS)

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
            print('%-40s %s' % (os.path.basename(f), 'valid' if not errs else 'INVALID'))
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
