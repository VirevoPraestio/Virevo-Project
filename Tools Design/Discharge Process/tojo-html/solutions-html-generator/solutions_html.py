#!/usr/bin/env python3
"""
solutions_html — the Solutions tab generator.

Claude (through the API) writes a response spec: JSON with the turn, the chat parts and the canvas
blocks with their slots. This generator validates the spec against the Solutions registry and draws
the canvas offline in the Solutions look (the drafting table), inside the app shell. No model writes HTML.

  python3 solutions_html.py validate SPEC.json
  python3 solutions_html.py render SPEC.json --view desktop|mobile|canvas -o OUT.html
  python3 solutions_html.py sample SPEC.json -o OUT.html         # one turn: desktop and phone side by side, both live
  python3 solutions_html.py build [SPEC_DIR] [-o OUT_DIR]       # every turn in SPEC_DIR/turns.json: one review file each + the tab book
  python3 solutions_html.py prompt                              # the Solutions part of the API system prompt
  python3 solutions_html.py catalog
Standard library only.
"""
import argparse, copy, glob, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIAG = os.path.join(ROOT, 'diagnosis-html-generator')
COMMON = os.path.join(ROOT, 'landing-common')
sys.path[:0] = [DIAG, COMMON]
import diagnosis_html as dh          # noqa: E402  shared validator pieces (slot checks, plain English, chat rules)
import landing_common as lc          # noqa: E402  shared shell, stamp and buttons
from preview import chat_parts, user_msg   # noqa: E402  the chat panel is the same in every tab
import review_page                       # noqa: E402  desktop + phone review pages, shared by every tab

REG_PATH = os.path.join(HERE, 'registry.json')
CSS_PATH = os.path.join(HERE, 'assets', 'solutions.css')
GEN = 'solutions_html 1.0'
e = lc.e
TAB = 'Solutions'
THEME = {'ground': '#E3EAF0', 'rail_bg': '#15304D', 'rail_fg': '#F1D493'}
STATUS = {'idea': 'Idea', 'shaping': 'Being shaped', 'tested': 'Tested with you', 'agreed': 'Agreed', 'new': 'New', 'waiting': 'Waiting on you', 'parked': 'Parked'}
STAGE_AT = {'idea': 0, 'new': 0, 'waiting': 0, 'parked': 0, 'shaping': 1, 'tested': 2, 'agreed': 3}
SRC = {'yours': 'Your number', 'derived': 'Worked out from yours', 'estimate': 'Tojo’s guess', 'illustrative': 'Example only', 'target': 'Goal', 'needed': 'Need from you'}

def load_registry():
    reg = json.load(open(REG_PATH, encoding='utf-8'))
    reg['plain_english'] = dh.load_registry()['plain_english']     # one plain-English list for every tab
    return reg

# ---------------------------------------------------------------------------------------------- pieces
def pt(o):
    return ' data-pt="%d"' % o['point'] if isinstance(o, dict) and o.get('point') is not None else ''

def tri(n, small=False):
    return ('<span class="sx-tri%s" title="Revision %d"><svg viewBox="0 0 26 23" aria-hidden="true"><path d="M13 2L24.5 21.5H1.5z"/></svg><b>%d</b><span class="sr">Revision %d</span></span>'
            % (' sx-tri-s' if small else '', n, n, n))

def chip(status):
    return '<span class="sx-chip sx-st-%s">%s</span>' % (status, STATUS[status])

def more(o):
    if not o.get('more_points'): return ''
    return '<details class="sx-more"><summary>%s</summary><ul>%s</ul></details>' % (e(o.get('more_label') or 'See the detail'), ''.join('<li>%s</li>' % e(p) for p in o['more_points']))

def mark(settled):
    return '<span class="sx-cm sx-c-%s" aria-hidden="true"></span><span class="sr">%s</span>' % ('ok' if settled else 'open', 'settled' if settled else 'still open')

# ---------------------------------------------------------------------------------------------- blocks
def r_heading(b):
    return '<header class="sx-hd"><div class="sx-eyebrow">%s</div><h2 class="sx-title">%s</h2>%s</header>' % (
        e(b['eyebrow']), e(b['title']), '<p class="sx-deck">%s</p>' % e(b['deck']) if b.get('deck') else '')

def r_sheets(b):
    out = []
    for s in b['items']:
        layers = ''.join('<span class="sx-layer" style="--k:%d" aria-hidden="true"></span>' % k for k in range(min(s['rev'], 2), 0, -1))
        cons = ''.join('<li>%s<span>%s</span></li>' % (mark(c['settled']), e(c['text'])) for c in s.get('cons', []))
        built = '<span class="sx-built">Worked through in %s</span>' % e(s['built_in']) if s.get('built_in') else ''
        out.append('<article class="sx-sheet sx-st-%s"%s>%s<div class="sx-sh-in"><div class="sx-sh-head"><span class="sx-sh-n">Solution %d</span>%s%s</div>'
                   '<h3 class="sx-sh-t">%s</h3><div class="sx-from">From: %s</div>%s%s%s</div></article>' % (
                       s['status'], pt(s), layers, s['n'], tri(s['rev']), chip(s['status']), e(s['title']), e(s['from']),
                       '<ul class="sx-cons">%s</ul>' % cons if cons else '', built, more(s)))
    cols = 3 if len(b['items']) in (3, 5, 6) else 2
    return '<section class="sx-block sx-sheets" data-block="sheets" style="--cols:%d">%s</section>' % (cols, ''.join(out))

def tracks_html(items, stages):
    head = ('<div class="sx-tk-head" aria-hidden="true"><span>Solution</span><span class="sx-tk-scale" style="--n:%d">%s</span><span>Depends on</span></div>' %
            (len(stages), ''.join('<b>%s</b>' % e(x) for x in stages)))
    rows = []
    for s in items:
        at = min(STAGE_AT[s['status']], len(stages) - 1)
        stops = ''.join('<li class="%s"><span class="sx-tk-dot"></span><span class="sx-tk-l">%s</span></li>' % (
            'is-done' if i < at else ('is-at' if i == at else ''), e(n)) for i, n in enumerate(stages))
        rev = '<div class="sx-tk-rev">%s<span>%s</span></div>' % (tri(s['rev'], True) if s['rev'] else '<span class="sx-new">New</span>', e(s['changed']))
        ok, tot = s['settled'], s['total']
        dots = ''.join('<i class="ok"></i>' for _ in range(ok)) + ''.join('<i></i>' for _ in range(max(tot - ok, 0)))
        rows.append('<li class="sx-tk sx-st-%s"%s><div class="sx-tk-name"><span class="sx-tk-n">%d</span><span class="sx-tk-t">%s</span>%s</div>'
                    '<ol class="sx-tk-line" style="--n:%d">%s</ol><div class="sx-tk-dep"><span class="sx-marks" aria-hidden="true">%s</span><span>%d of %d settled</span></div></li>' % (
                        s['status'], pt(s), s['n'], e(s['title']), rev, len(stages), stops, dots, ok, tot))
    return head + '<ol>%s</ol>' % ''.join(rows)

def r_tracks(b):
    return '<section class="sx-block sx-tracks" data-block="tracks">%s</section>' % tracks_html(b['items'], b.get('stages') or ['Idea', 'Shaped', 'Tested with you', 'Agreed'])

def r_weigh(b):
    sup = []
    for l in b['lenses']:
        sup.append('<li class="sx-sup sx-w-%s"%s><span class="sx-post" aria-hidden="true"></span><div class="sx-foot"><div class="sx-lens">%s<b>%s</b></div><p>%s</p>%s</div></li>' % (
            l['state'], pt(l), '<span class="sx-wtag">%s</span>' % {'settled': 'Settled', 'open': 'Still open', 'risk': 'Could break it'}[l['state']], e(l['lens']), e(l['finding']), more(l)))
    n = {k: sum(1 for l in b['lenses'] if l['state'] == k) for k in ('settled', 'open', 'risk')}
    return ('<section class="sx-block sx-weigh" data-block="weigh" style="--n:%d"><div class="sx-beam"><span class="sx-beam-l">What it stands on</span><b>%s</b>%s'
            '<span class="sx-beam-c">%d settled · %d open · %d could break it</span></div><ol class="sx-sups">%s</ol><p class="sx-cond">%s</p></section>') % (
        len(b['lenses']), e(b['solution']), tri(b['rev']), n['settled'], n['open'], n['risk'], ''.join(sup), e(b['condition']))

def r_signoff(b):
    lv = {'most': 3, 'some': 2, 'little': 1}; lab = {'most': 'Most to give up', 'some': 'Some to give up', 'little': 'Little to give up'}
    doers = []
    for d in b['doers']:
        meter = ''.join('<i class="%s"></i>' % ('on' if i < lv[d['resistance']] else '') for i in range(3))
        said = '<p class="sx-said">“%s”</p>' % e(d['said']) if d.get('said') else ''
        doers.append('<li class="sx-doer sx-r-%s"%s><div class="sx-dh"><b>%s</b><span class="sx-meter" aria-hidden="true">%s</span><span class="sx-rl">%s</span></div>%s'
                     '<dl><dt>Gives up</dt><dd>%s</dd><dt>The ask</dt><dd>%s</dd></dl></li>' % (
                         d['resistance'], pt(d), e(d['role']), meter, lab[d['resistance']], said, e(d['gives_up']), e(d['ask'])))
    a = b['approver']
    appr = ('<div class="sx-appr"%s><span class="sx-stamp" aria-hidden="true">Approves</span><div class="sx-label">Signs off, does not do the work</div><b>%s</b><p>%s</p>'
            '<p class="sx-fails"><span>If they never say yes:</span> %s</p></div>') % (pt(a), e(a['role']), e(a['why']), e(a['fails']))
    return '<section class="sx-block sx-signoff" data-block="signoff"><ol class="sx-doers" style="--n:%d">%s</ol>%s</section>' % (len(b['doers']), ''.join(doers), appr)

def r_split(b):
    said = '<p class="sx-heard"><span class="sx-label">What you told us</span><q>%s</q></p>' % e(b['said']) if b.get('said') else ''
    def side(o, cls, cap):
        return '<div class="sx-side %s"><div class="sx-label">%s</div><b>%s</b><ul>%s</ul></div>' % (cls, cap, e(o['title']), ''.join('<li>%s</li>' % e(x) for x in o['items']))
    return ('<section class="sx-block sx-split" data-block="split">%s<div class="sx-pair">%s<div class="sx-dimv" aria-hidden="true"><span></span></div>%s</div>'
            '<p class="sx-cond"><span>Where the answer changes:</span> %s</p></section>') % (
        said, side(b['supplied'], 'sx-sup-side', 'Tojo adds'), side(b['required'], 'sx-req-side', 'Must already be there'), e(b['threshold']))

def r_revisions(b):
    rows = ''.join('<li%s>%s<div class="sx-rv"><b>Solution %d · %s</b><p class="sx-was"><span>Was</span>%s</p><p class="sx-now"><span>Now</span>%s</p>'
                   '<span class="sx-because">Because of %s</span></div></li>' % (
                       pt(x), tri(x['rev']) if x['rev'] else '<span class="sx-new">New</span>', x['n'], e(x['title']), e(x['was']), e(x['now']), e(x['because'][0].lower() + x['because'][1:])) for x in b['entries'])
    return '<section class="sx-block sx-revisions" data-block="revisions"><ol>%s</ol></section>' % rows

def r_scales(b):
    c, s = b['cost'], b['stake']
    big = max(c['amount'], s['amount']) or 1
    def bar(o, cls):
        w = max(100.0 * o['amount'] / big, 1.2)
        note = '<span class="sx-bn">%s</span>' % e(o['note']) if o.get('note') else ''
        # a line under 6% of the scale is too short to read as a line: point at it and say what it is
        tip = ('<span class="sx-tip" style="left:calc(%.2f%% + 14px)">&larr; %s, drawn to the same scale</span>' % (w, e(o['value']))) if w < 6 else ''
        return ('<div class="sx-bar %s"><div class="sx-bl"><span>%s</span><b>%s</b><span class="sx-src sx-src-%s">%s</span></div>'
                '<div class="sx-dim"><span class="sx-dline" style="width:%.2f%%"></span>%s</div>%s</div>') % (cls, e(o['label']), e(o['value']), o['source'], SRC[o['source']], w, tip, note)
    ratio = s['amount'] / c['amount'] if c['amount'] else 0
    times = '<p class="sx-times"><b>About %s times</b> the cost is at stake <span class="sx-src sx-src-derived">%s</span></p>' % (
        '{:,}'.format(int(float('%.2g' % ratio))), SRC['derived']) if ratio >= 2 else ''
    trig = ''
    if b.get('trigger'):
        t = b['trigger']
        trig = '<div class="sx-trig"><span class="sx-label">%s</span><b>%s</b><span>%s</span></div>' % (e(t['label']), e(t['value']), e(t['line']))
    return ('<section class="sx-block sx-scales" data-block="scales"><div class="sx-label">Drawn to the same scale</div>%s%s%s%s<p class="sx-cond">%s</p></section>') % (
        bar(s, 'sx-stake'), bar(c, 'sx-cost'), times, trig, e(b['condition']))

def r_plan(b):
    steps = ''.join('<li class="sx-step"%s><span class="sx-sn">%d</span><div><b>%s</b><p>%s</p><dl><dt>Needs</dt><dd>%s</dd><dt>Measures</dt><dd>%s</dd></dl></div></li>' % (
        pt(s), i + 1, e(s['title']), e(s['what']), e(s['needs']), e(s['measure'])) for i, s in enumerate(b['steps']))
    fork = ''
    if b.get('fork'):
        f = b['fork']; o = f['options']
        fork = ('<div class="sx-fork"><div class="sx-fq">%s</div><div class="sx-fo"><div class="sx-opt"><b>%s</b><span>%s</span></div><span class="sx-or">or</span>'
                '<div class="sx-opt"><b>%s</b><span>%s</span></div></div></div>') % (e(f['question']), e(o[0]['label']), e(o[0]['what']), e(o[1]['label']), e(o[1]['what']))
    return '<section class="sx-block sx-plan" data-block="plan"><ol class="sx-steps" style="--n:%d">%s</ol>%s</section>' % (len(b['steps']), steps, fork)

def r_register(b):
    rows = []
    for s in b['items']:
        w = 100 * s['settled'] // s['total'] if s['total'] else 0
        rows.append('<li class="sx-rg sx-st-%s"%s><span class="sx-rg-n">%d</span><div><div class="sx-rg-t">%s</div><div class="sx-rg-l">%s</div></div>'
                    '<div class="sx-rg-r">%s<span class="sx-rg-bar" aria-label="%d of %d settled"><span style="width:%d%%"></span></span><span class="sx-rg-c">%d of %d settled</span></div></li>' % (
                        s['status'], pt(s), s['n'], e(s['title']), ' · '.join(e(x) for x in s['lenses']), chip(s['status']), s['settled'], s['total'], w, s['settled'], s['total']))
    return '<section class="sx-block sx-register" data-block="register"><ol>%s</ol></section>' % ''.join(rows)

def r_landing(b, state):
    """The approved landing template (Solutions B), drawn from the spec's data."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('so_landing', os.path.join(HERE, 'landing.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    sols = [{'n': s['n'], 'title': s['title'], 'rev': s['rev'], 'status': 'shaping' if s['status'] == 'tested' else s['status'], 'from': '', 'changed': s['changed'], 'why': '', 'when': '',
             'point': s.get('point'), 'cons': [('', 1, '')] * s['settled'] + [('', 0, '')] * max(s['total'] - s['settled'], 0)} for s in b['solutions']]
    if not sols:
        sols = copy.deepcopy(mod.DATA['empty']['solutions'])
    data = {'stamp': b['stamp'], 'standing': b['standing'], 'deck': b['deck'], 'solutions': sols,
            'pending': [dict(p, pt=p.get('point')) for p in b['pending']], 'actions': b['actions']}
    # the landing template reads point numbers from each solution's n; keep the spec's own point links
    m = lc.Mode('html', state, {state: data})
    html_s = mod.sample_b(m)
    return html_s



# ---------------------------------------------------------------------------------------------- puzzle (Solutions only)
BULB = ('<svg class="sx-bulb" viewBox="0 0 48 58" aria-hidden="true"><g class="sx-rays"><path d="M24 1v6M7 8l4.5 4.5M41 8l-4.5 4.5M1 25h6M41 25h6"/></g>'
        '<path class="sx-glass" d="M24 10a14 14 0 0 0-8.2 25.3c1.6 1.2 2.7 3 2.7 5V43h11v-2.7c0-2 1.1-3.8 2.7-5A14 14 0 0 0 24 10z"/>'
        '<path class="sx-fil" d="M19.5 32l2.2-5 2.3 4 2.3-4 2.2 5"/><path class="sx-base" d="M18.5 46.5h11M19.5 50.5h9M21.5 54.5h5"/></svg>')

KNOB = [(0.36, 0), (0.42, 0), (0.38, 0.10), (0.36, 0.16), (0.32, 0.26), (0.40, 0.30), (0.50, 0.30), (0.60, 0.30), (0.68, 0.26), (0.64, 0.16), (0.62, 0.10), (0.58, 0), (0.64, 0)]

def _edge(x0, y0, x1, y1, d, K):
    """One side of a jigsaw piece, drawn clockwise. d = +1 knob out, -1 knob in, 0 flat."""
    if not d: return 'L%.1f %.1f' % (x1, y1)
    L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5; ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = uy, -ux
    def P(u, v):
        a = L / 2 + (u - .5) * K; b = v * K * d
        return '%.1f %.1f' % (x0 + ux * a + nx * b, y0 + uy * a + ny * b)
    k = KNOB
    return 'L%s C%s %s %s C%s %s %s C%s %s %s C%s %s %s L%.1f %.1f' % (
        P(*k[0]), P(*k[1]), P(*k[2]), P(*k[3]), P(*k[4]), P(*k[5]), P(*k[6]), P(*k[7]), P(*k[8]), P(*k[9]), P(*k[10]), P(*k[11]), P(*k[12]), x1, y1)

def _piece_path(r, c, rows, cols, w, h, K):
    rd = lambda r, c: (1 if (r + c) % 2 == 0 else -1) if c < cols - 1 else 0      # right edge of cell (r, c)
    bd = lambda r, c: (1 if (r + c) % 2 == 1 else -1) if r < rows - 1 else 0      # bottom edge of cell (r, c)
    x, y = c * w, r * h
    top = -bd(r - 1, c) if r > 0 else 0
    left = -rd(r, c - 1) if c > 0 else 0
    return 'M%.1f %.1f %s %s %s %s Z' % (x, y, _edge(x, y, x + w, y, top, K), _edge(x + w, y, x + w, y + h, rd(r, c), K),
                                         _edge(x + w, y + h, x, y + h, bd(r, c), K), _edge(x, y + h, x, y, left, K))

PZ_LAYOUT = {  # cell of the idea (0) and of parts 1..5, as (row, col)
    'wide': {'rows': 2, 'cols': 3, 'w': 300, 'h': 190, 'cells': {0: (0, 1), 1: (0, 0), 2: (0, 2), 3: (1, 0), 4: (1, 1), 5: (1, 2)}},
    'narrow': {'rows': 6, 'cols': 1, 'w': 360, 'h': 122, 'cells': {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0), 4: (4, 0), 5: (5, 0)}},
}

def r_puzzle(b):
    idea, ps = b['idea'], {p['n']: p for p in b['pieces']}
    sel = b.get('default', 1)
    names = {p['n']: p['name'] for p in b['pieces']}
    layouts = []
    for key, L in PZ_LAYOUT.items():
        W, H = L['cols'] * L['w'], L['rows'] * L['h']; K = min(110, .8 * min(L['w'], L['h']))
        shapes, faces = [], []
        for n, (r, c) in sorted(L['cells'].items()):
            d = _piece_path(r, c, L['rows'], L['cols'], L['w'], L['h'], K)
            shapes.append('<path class="sx-pz-shape%s" data-piece="%d" style="--i:%d" d="%s"/>' % (' sx-pz-idea' if n == 0 else '', n, n, d))
            pos = 'left:%.3f%%;top:%.3f%%;width:%.3f%%;height:%.3f%%;--i:%d' % (100.0 * c * L['w'] / W, 100.0 * r * L['h'] / H, 100.0 * L['w'] / W, 100.0 * L['h'] / H, n)
            if n == 0:
                faces.append('<button type="button" class="sx-pz-face sx-pz-f0" data-piece="0" style="%s" aria-pressed="%s">%s<span><small>The idea</small><b>%s</b><em>%s</em></span></button>' % (
                    pos, 'true' if sel == 0 else 'false', BULB, e(idea['title']), e(idea['line'])))
            else:
                p = ps[n]
                faces.append('<button type="button" class="sx-pz-face" data-piece="%d"%s style="%s" aria-pressed="%s"><span><small>Part %d</small><b>%s</b><em>%s</em></span></button>' % (
                    n, pt(p), pos, 'true' if sel == n else 'false', n, e(p['name']), e(p['line'])))
        layouts.append('<div class="sx-pz-board sx-pz-%s" style="aspect-ratio:%d/%d"><svg viewBox="-6 -6 %d %d" aria-hidden="true">%s</svg>%s</div>' % (
            key, W, H, W + 12, H + 12, ''.join(shapes), ''.join(faces)))
    # the detail sheet under the picture, one per piece; only the chosen one shows
    det = ['<div class="sx-pz-d" data-piece="0"%s><div class="sx-pz-dh"><small>The idea</small><b>%s</b><p>%s</p></div>'
           '<div class="sx-pz-dl"><span class="sx-label">What Diagnosis found</span><ul>%s</ul></div>'
           '<div class="sx-pz-dl"><span class="sx-label">How the five parts answer it</span><p>%s</p></div></div>' % (
               '' if sel == 0 else ' hidden', e(idea['title']), e(idea['line']), ''.join('<li>%s</li>' % e(x) for x in idea['causes']), e(idea['how']))]
    for p in b['pieces']:
        rel = ''.join('<button type="button" class="sx-pz-go" data-go="%d">Part %d · %s</button>' % (r, r, e(names[r])) for r in p.get('relies_on', []))
        det.append(('<div class="sx-pz-d" data-piece="%d"%s><div class="sx-pz-dh"><small>Part %d</small><b>%s</b><p>%s</p>'
                    '<button type="button" class="sx-ask" data-text="%s"%s>Ask Tojo about this part</button></div>'
                    '<dl class="sx-pz-dl"><dt>It answers</dt><dd>%s</dd><dt>Needed first</dt><dd>%s</dd><dt>It relies on</dt><dd class="sx-pz-rel">%s</dd><dt>Worked through in</dt><dd>%s</dd></dl>'
                    '<div class="sx-pz-dl"><span class="sx-label">What changes</span><ul>%s</ul></div></div>') % (
            p['n'], '' if sel == p['n'] else ' hidden', p['n'], e(p['name']), e(p['line']), e(p['ask']), ' data-ask-pt="%d"' % p['point'] if p.get('point') else '',
            e(p['answers']), e(p['needs_first']), rel or 'Nothing else', e(p['where']), ''.join('<li>%s</li>' % e(x) for x in p['changes'])))
    return ('<section class="sx-block sx-puzzle" data-block="puzzle" data-sel="%d"><div class="sx-pz-hint"><span class="sx-pz-hand" aria-hidden="true"></span>%s</div>%s'
            '<div class="sx-pz-sheet" aria-live="polite">%s</div></section>') % (sel, e(b.get('hint') or 'Pick a piece to see what it does and what it relies on.'), ''.join(layouts), ''.join(det))


# ---------------------------------------------------------------------------------------------- untangle (Solutions only)
UT_T0, UT_T1 = 18.0, 40.0          # the drawing runs from 6 PM to 4 PM the next day

def _ut_x(t):
    h, m = [int(x) for x in t.split(':')]; v = h + m / 60.0
    if v < UT_T0: v += 24
    return max(0.0, min(1000.0, 1000.0 * (v - UT_T0) / (UT_T1 - UT_T0)))

def _clock(t):
    h, m = [int(x) for x in t.split(':')]
    if h == 0 and m == 0: return 'midnight'
    if h == 12 and m == 0: return 'noon'
    ap = 'AM' if h < 12 else 'PM'; hh = h % 12 or 12
    return '%d%s %s' % (hh, (':%02d' % m) if m else '', ap)

def r_untangle(b):
    th = b['threads']; n = len(th); RH = 48; H = n * RH; sel = b.get('default', 1)
    kx = _ut_x(b['knot']['at']); ky = H / 2.0
    today, withp = [], []
    for i, t in enumerate(th):
        y = RH / 2.0 + i * RH
        x0 = _ut_x(b['decided']); xw = _ut_x(b['work_starts']); xe = _ut_x(t['today_end'])
        sag = 16 + (i % 3) * 6
        # evening decision, slack all night, then everything pulled into one knot, then out to its real end
        today.append('<path class="ut-w" data-row="%d" d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f"/>' % (
            i + 1, x0, y, x0 + (xw - x0) * .3, y + sag, x0 + (xw - x0) * .7, y + sag, xw, y,
            xw + (kx - xw) * .5, y, kx - 30, ky + (i - n / 2.0) * 10, kx, ky + (i - n / 2.0) * 2,
            kx + 30, ky - (i - n / 2.0) * 12, xe - (xe - kx) * .45, y, xe, y))
        withp.append('<path class="ut-w ut-w-new" data-row="%d" d="M%.1f %.1f L%.1f %.1f"/>' % (i + 1, _ut_x(t['with_start']), y, _ut_x(t['with_end']), y))
    knot = ''.join('<ellipse class="ut-knot" cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%d %.1f %.1f)"/>' % (kx + (k % 2) * 4 - 2, ky + (k % 3) * 2 - 2, 44 - k * 6, 12 + k * 4, k * 33 - 20, kx, ky) for k in range(5))
    svg = ('<svg class="ut-svg" viewBox="0 0 1000 %d" preserveAspectRatio="none" aria-hidden="true"><g class="ut-today">%s%s</g><g class="ut-with">%s</g></svg>' % (H, ''.join(today), knot, ''.join(withp)))
    def at(t, cls, inner, extra=''):
        flip = ' ut-flip' if _ut_x(t) > 780 and ('ut-end' in cls or 'ut-leave' in cls) else ''
        return '<span class="%s%s" style="left:%.2f%%"%s>%s</span>' % (cls, flip, _ut_x(t) / 10.0, extra, inner)
    rows = []
    for i, t in enumerate(th):
        r = i + 1
        rows.append('<button type="button" class="ut-lab" data-row="%d"%s style="grid-row:%d" aria-pressed="%s"><b>%s</b></button>' % (
            r, pt(t), r + 1, 'true' if r == sel else 'false', e(t['name'])))
        rows.append('<div class="ut-lane" data-row="%d" style="grid-row:%d">%s%s%s%s</div>' % (
            r, r + 1,
            at(b['decided'], 'ut-dot ut-today', ''), at(t['today_end'], 'ut-end ut-today', '<i></i><span>%s</span>' % e(_clock(t['today_end'])), ' data-src="%s"' % t['today_source']),
            at(t['with_start'], 'ut-dot ut-with', ''), at(t['with_end'], 'ut-end ut-with', '<i></i><span>%s</span>' % e(_clock(t['with_end'])), ' data-src="%s"' % t['with_source'])))
    ticks = ''.join(at(x, 'ut-tick', e(_clock(x))) for x in ('18:00', '21:00', '00:00', '03:00', '06:00', '09:00', '12:00', '15:00'))
    night = b['unused']
    band = '<span class="ut-night" style="left:%.2f%%;width:%.2f%%"><em class="ut-today">%s</em><em class="ut-with">%s</em></span>' % (
        _ut_x(night['from']) / 10.0, (_ut_x(night['to']) - _ut_x(night['from'])) / 10.0, e(night['label']), e(night['label_with']))
    knotlab = at(b['knot']['at'], 'ut-knotlab ut-today', e(b['knot']['label']))
    lt, lw = b['leaves_today'], b['leaves_with']
    leave = (at(lt['at'], 'ut-leave ut-today', '<span>%s<br><b>%s</b> %s</span>' % (e(lt['label']), e(_clock(lt['at'])), '<i class="sx-src sx-src-%s">%s</i>' % (lt['source'], SRC[lt['source']]))) +
             at(lw['at'], 'ut-leave ut-with', '<span>%s<br><b>%s</b> %s</span>' % (e(lw['label']), e(_clock(lw['at'])), '<i class="sx-src sx-src-%s">%s</i>' % (lw['source'], SRC[lw['source']]))))
    det = []
    for i, t in enumerate(th):
        r = i + 1
        det.append(('<div class="ut-d" data-row="%d"%s><div class="ut-dh"><small>Thread %d</small><b>%s</b></div>'
                    '<dl><dt>Today</dt><dd>%s <span class="ut-t">%s</span> <i class="sx-src sx-src-%s">%s</i></dd>'
                    '<dt>With the automations</dt><dd>%s <span class="ut-t">%s</span> <i class="sx-src sx-src-%s">%s</i></dd></dl>'
                    '<dl><dt>What Tojo does</dt><dd>%s</dd><dt>Hold-up it removes</dt><dd>%s</dd><dt>Needed first</dt><dd>%s</dd></dl></div>') % (
            r, '' if r == sel else ' hidden', r, e(t['name']), e(t['today']), e(_clock(t['today_end'])), t['today_source'], SRC[t['today_source']],
            e(t['with']), e(_clock(t['with_end'])), t['with_source'], SRC[t['with_source']], e(t['tojo_does']), e(t['removes']), e(t['needs'])))
    cap = b['captions']
    return ('<section class="sx-block sx-untangle" data-block="untangle" data-state="today" data-sel="%d">'
            '<div class="ut-bar"><div class="ut-switch" role="group" aria-label="Which picture"><button type="button" data-state="today" aria-pressed="true">Today</button>'
            '<button type="button" data-state="with" aria-pressed="false">%s</button></div><p class="ut-cap"><span class="ut-today">%s</span><span class="ut-with">%s</span></p></div>'
            '<div class="ut-grid" style="--rows:%d"><div class="ut-axis">%s%s</div><div class="ut-lanes" style="grid-row:2/%d">%s%s%s</div>%s</div>'
            '<div class="ut-sheet" aria-live="polite">%s</div>%s</section>') % (
        sel, e(b['with_label']), e(cap['today']), e(cap['with']), n, band, ticks, n + 2, svg, knotlab, leave, ''.join(rows), ''.join(det),
        '<p class="sx-cond">%s</p>' % e(b['condition']) if b.get('condition') else '')

# ---------------------------------------------------------------------------------------------- maze (Solutions only)
# A fixed labyrinth on a 15 x 7 grid. The way through runs from the entrance (left) to the bulb (right);
# up to three dead ends branch off it. The spec only names the routes; the corridors are the template's.
MZ_COLS, MZ_ROWS = 15, 7
MZ_WAY = [(0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (11, 4), (11, 3), (12, 3), (13, 3), (14, 3)]
MZ_DEAD = [[(3, 3), (3, 5), (1, 5), (1, 6)],
           [(7, 3), (5, 3), (5, 5), (4, 5), (4, 6)],
           [(11, 5), (13, 5), (13, 6), (10, 6)]]
MZ_EXTRA = [[(5, 1), (5, 0), (9, 0)], [(9, 5), (9, 2), (10, 2), (10, 1)], [(1, 3), (1, 0), (2, 0)],
            [(12, 3), (12, 0), (14, 0)], [(7, 5), (7, 6), (8, 6)], [(14, 3), (14, 5)]]   # blind alleys with no label

def _mz_links(paths):
    cells, links = set(), set()
    for pth in paths:
        for a, c in zip(pth, pth[1:]):
            # fill straight runs between listed corners
            (x0, y0), (x1, y1) = a, c
            sx = (x1 > x0) - (x1 < x0); sy = (y1 > y0) - (y1 < y0); x, y = x0, y0
            while (x, y) != (x1, y1):
                nx, ny = x + sx, y + sy; cells.update([(x, y), (nx, ny)]); links.add(frozenset([(x, y), (nx, ny)])); x, y = nx, ny
    return cells, links

def r_maze(b):
    routes = b['routes']; dead = [r for r in routes if r['kind'] == 'dead']; way = [r for r in routes if r['kind'] == 'way'][0]
    C = 36; W, H = MZ_COLS * C, MZ_ROWS * C
    paths = [MZ_WAY] + MZ_DEAD[:len(dead)] + MZ_EXTRA
    cells, links = _mz_links(paths)
    walls, blocks = [], []
    for y in range(MZ_ROWS):
        for x in range(MZ_COLS):
            if (x, y) not in cells:
                blocks.append('<rect x="%d" y="%d" width="%d" height="%d"/>' % (x * C, y * C, C, C)); continue
            for dx, dy, seg in ((0, -1, (0, 0, 1, 0)), (1, 0, (1, 0, 1, 1)), (0, 1, (0, 1, 1, 1)), (-1, 0, (0, 0, 0, 1))):
                nb = (x + dx, y + dy)
                if frozenset([(x, y), nb]) in links: continue
                if (x, y) == MZ_WAY[0] and dx == -1: continue          # the entrance
                if (x, y) == MZ_WAY[-1] and dx == 1: continue          # the way out to the bulb
                walls.append('M%d %dL%d %d' % ((x + seg[0]) * C, (y + seg[1]) * C, (x + seg[2]) * C, (y + seg[3]) * C))
    def trail(pth, first=None):
        pts = [pth[0]] + [c for c in pth[1:]]
        return ' '.join('%s%d %d' % ('M' if k == 0 else 'L', x * C + C // 2, y * C + C // 2) for k, (x, y) in enumerate(pts))
    trails = ['<path class="mz-trail mz-way" data-route="%d" d="%s L%d %d"/>' % (len(dead) + 1, trail(MZ_WAY), W + 30, 3 * C + C // 2)]
    pins = []
    for k, r in enumerate(dead):
        pth = MZ_DEAD[k]; tx, ty = pth[-1]
        trails.append('<path class="mz-trail mz-dead" data-route="%d" d="%s"/>' % (k + 1, trail(pth)))
        pins.append('<g class="mz-pin" data-route="%d"><circle cx="%d" cy="%d" r="11"/><text x="%d" y="%d">%d</text></g>' % (
            k + 1, tx * C + C // 2, ty * C + C // 2, tx * C + C // 2, ty * C + C // 2 + 4, k + 1))
    svg = ('<svg class="mz-svg" viewBox="-40 -4 %d %d" aria-hidden="true"><g class="mz-blocks">%s</g><path class="mz-walls" d="%s"/>%s%s'
           '<g class="mz-start"><path d="M-36 %d h30 m-8 -7 l8 7 l-8 7"/></g><g class="mz-goal" transform="translate(%d %d)">%s</g></svg>') % (
        W + 110, H + 8, ''.join(blocks), ' '.join(walls), ''.join(trails), ''.join(pins), 3 * C + C // 2, W + 8, 3 * C - 10, BULB.replace('class="sx-bulb"', 'class="sx-bulb" width="40" height="50" x="0" y="0"'))
    sel = b.get('default', len(dead) + 1)
    items = []
    for k, r in enumerate(dead + [way]):
        n = k + 1; isway = r['kind'] == 'way'
        items.append('<li><button type="button" class="mz-r%s" data-route="%d"%s aria-pressed="%s"><span class="mz-n">%s</span><span><small>%s</small><b>%s</b></span></button></li>' % (
            ' mz-r-way' if isway else '', n, pt(r), 'true' if n == sel else 'false', '' if isway else str(n), 'The way through' if isway else 'Ruled out', e(r['name'])))
    det = []
    for k, r in enumerate(dead + [way]):
        n = k + 1; isway = r['kind'] == 'way'
        needs = '<div><span class="sx-label">What your hospital must already have</span><ul>%s</ul></div>' % ''.join('<li>%s</li>' % e(x) for x in r['needs']) if r.get('needs') else ''
        det.append('<div class="mz-d%s" data-route="%d"%s><div><small>%s</small><b>%s</b><p>%s</p></div>%s</div>' % (
            ' mz-d-way' if isway else '', n, '' if n == sel else ' hidden', 'The way through' if isway else 'Why it is ruled out', e(r['name']), e(r['why']), needs))
    return ('<section class="sx-block sx-maze" data-block="maze" data-sel="%d"><div class="mz-top"><div class="mz-board"><div class="mz-q"><span>Start</span>%s</div>%s<div class="mz-goal-l"><span>Goal</span>%s</div></div>'
            '<div class="mz-side"><div class="sx-pz-hint"><span class="sx-pz-hand" aria-hidden="true"></span>%s</div><ol class="mz-list">%s</ol></div></div>'
            '<div class="mz-sheet" aria-live="polite">%s</div></section>') % (
        sel, e(b['start']), svg, e(b['goal']), e(b.get('hint') or 'Pick a route to follow it through the maze.'), ''.join(items), ''.join(det))


# ---------------------------------------------------------------------------------------------- knots (Solutions only)
def _mins(t):
    h, m = [int(x) for x in t.split(':')]; return h * 60 + m

def _dur(m):
    h, r = divmod(int(m), 60)
    return ' '.join(x for x in ['%d hour%s' % (h, '' if h == 1 else 's') if h else '', '%d minutes' % r if r else ''] if x)

KNOT_SVG = ('<svg viewBox="0 0 44 30" aria-hidden="true"><path class="kn-rope" d="M0 15 H10"/><path class="kn-rope" d="M34 15 H44"/>'
            '<path class="kn-tie" d="M10 15 C14 2 26 2 26 13 C26 24 12 26 14 15 C16 6 30 4 34 15"/><path class="kn-tie" d="M14 15 C18 26 30 28 34 15"/>'
            '<path class="kn-flat" d="M0 15 H44"/></svg>')

def r_knots(b):
    segs, parts = b['segments'], {p['n']: p for p in b['parts']}
    t0, t1 = _mins(segs[0]['from']), _mins(segs[-1]['to']); span = float(t1 - t0)
    total = sum(_mins(g['to']) - _mins(g['from']) for g in segs)
    on = b.get('default_on', [])
    knots, labs, marks = [], [], []
    for i, g in enumerate(segs):
        a, z = (_mins(g['from']) - t0) / span * 100, (_mins(g['to']) - t0) / span * 100
        need = g['undone_by']
        knots.append('<button type="button" class="kn-k" data-seg="%d" data-need="%s" data-min="%d"%s style="--a:%.2f%%;--w:%.2f%%" aria-pressed="false">'
                     '<span class="kn-rope-l" aria-hidden="true"></span>%s<span class="kn-need">%s</span><span class="sr">%s</span></button>' % (
                         i + 1, ','.join(str(x) for x in need), _mins(g['to']) - _mins(g['from']), pt(g), a, z - a, KNOT_SVG,
                         ' + '.join('Part %d' % x for x in need), e(g['name'])))
        labs.append('<span class="kn-lab" style="--a:%.2f%%;--w:%.2f%%"><b>%s</b><em>%s</em></span>' % (a, z - a, e(g['name']), e(_dur(_mins(g['to']) - _mins(g['from'])))))
        marks.append('<span class="kn-time" style="--a:%.2f%%">%s</span>' % (a, e(_clock(g['from']))))
    marks.append('<span class="kn-time kn-time-end" style="--a:100%%">%s</span>' % e(_clock(segs[-1]['to'])))
    ev = '<p class="kn-src">%s</p>' % e(b['times_note'])
    btns = ''.join('<button type="button" class="kn-p" data-part="%d" aria-pressed="%s"><span>Part %d</span><b>%s</b></button>' % (
        p['n'], 'true' if p['n'] in on else 'false', p['n'], e(p['name'])) for p in b['parts'])
    rows = []
    for i, g in enumerate(segs):
        how = ''.join('<li><b>Part %d · %s</b> %s</li>' % (h['part'], e(parts[h['part']]['name']), e(h['how'])) for h in g['how'])
        rows.append('<div class="kn-d" data-seg="%d"%s><div class="kn-dh"><small>Knot %d · %s to %s</small><b>%s</b><p>%s</p><span class="sx-src sx-src-%s">%s</span></div>'
                    '<div><span class="sx-label">What undoes it</span><ul>%s</ul></div></div>' % (
                        i + 1, '' if i == 0 else ' hidden', i + 1, e(_clock(g['from'])), e(_clock(g['to'])), e(g['name']), e(g['today']),
                        g['source'], SRC[g['source']], how))
    return ('<section class="sx-block sx-knots" data-block="knots" data-total="%d" data-count="%d">'
            '<div class="kn-bar"><div class="kn-ps" role="group" aria-label="Parts to try">%s<button type="button" class="kn-all">All five</button><button type="button" class="kn-clear">Clear</button></div>'
            '<p class="kn-read" aria-live="polite"><b class="kn-n">0 of %d</b> knots undone · <span class="kn-h">the wait is %s</span></p></div>'
            '<div class="kn-board"><div class="kn-times">%s</div><div class="kn-line">%s</div><div class="kn-labs">%s</div>%s</div>'
            '<div class="kn-sheet" aria-live="polite">%s</div><p class="sx-cond">%s</p></section>') % (
        total, len(segs), btns, len(segs), e(_dur(total)), ''.join(marks), ''.join(knots), ''.join(labs), ev, ''.join(rows), e(b['condition']))

# ---------------------------------------------------------------------------------------------- stake (Solutions only): cost against what is at stake, with a share you choose
def r_stake(b):
    c, s_, sh = b['cost'], b['stake'], b['share']
    beam = ('<svg class="st-beam" viewBox="0 0 240 150" aria-hidden="true"><path class="st-post" d="M120 60 L104 140 H136 Z"/><g class="st-arm">'
            '<path class="st-rod" d="M20 60 H220"/><circle class="st-pin" cx="120" cy="60" r="6"/>'
            '<g class="st-pan st-pan-l"><path d="M20 60 V86 M0 86 H40 L32 98 H8 Z"/><circle class="st-w-l" cx="20" cy="80" r="4"/></g>'
            '<g class="st-pan st-pan-r"><path d="M220 60 V86 M200 86 H240 L232 98 H208 Z"/><circle class="st-w-r" cx="220" cy="78" r="9"/></g></g>'
            '<text class="st-bl" x="20" y="116">Team</text><text class="st-bl" x="220" y="116">Won back</text></svg>')
    presets = ''.join('<button type="button" class="st-pre" data-v="%d">%d%%</button>' % (v, v) for v in sh['presets'])
    trig = b.get('trigger')
    trig = '<div class="st-trig"><span class="sx-label">%s</span><b>%s</b><span>%s</span><span class="sx-src sx-src-yours">%s</span></div>' % (
        e(trig['label']), e(trig['value']), e(trig['line']), SRC['yours']) if trig else ''
    return ('<section class="sx-block sx-stake" data-block="stake" data-stake="%s" data-cost="%s">'
            '<div class="st-top">%s<div class="st-bars">'
            '<div class="st-row"><div class="st-l"><span>%s</span><b class="st-red">%s</b><span class="sx-src sx-src-%s">%s</span></div><div class="st-track"><span class="st-fill st-f-stake" style="width:100%%"></span></div><small>%s</small></div>'
            '<div class="st-row"><div class="st-l"><span>Won back each year, if the trial wins back <b class="st-pc">%d%%</b></span><b class="st-green st-won"></b><span class="sx-src sx-src-derived">%s</span></div><div class="st-track"><span class="st-fill st-f-won"></span></div></div>'
            '<div class="st-row"><div class="st-l"><span>%s</span><b>%s</b><span class="sx-src sx-src-%s">%s</span></div><div class="st-track"><span class="st-fill st-f-cost"></span><span class="st-tip">&larr; the team, drawn to the same scale</span></div><small>%s</small></div>'
            '</div></div>'
            '<div class="st-ctl"><label for="st-share-%s">%s</label><input id="st-share-%s" class="st-range" type="range" min="%d" max="%d" step="%d" value="%d"><div class="st-pres">%s</div>'
            '<p class="st-read" aria-live="polite"></p></div>%s<p class="sx-cond">%s</p></section>') % (
        s_['amount'], c['amount'], beam, e(s_['label']), e(s_['value']), s_['source'], SRC[s_['source']], e(s_['note']),
        sh['default'], SRC['derived'], e(c['label']), e(c['value']), c['source'], SRC[c['source']], e(c['note']),
        b.get('id', 'a'), e(sh['label']), b.get('id', 'a'), sh['min'], sh['max'], sh['step'], sh['default'], presets, trig, e(b['condition']))

# ---------------------------------------------------------------------------------------------- route (Solutions only): the steps in order, ending at the doors to the next tabs
TAB_KEY = {'Automations': 'au', 'Processes': 'pr', 'Solutions': 'so', 'Diagnosis': 'di'}

def r_route(b):
    st = b['steps']; sel = b.get('default', 1)
    stations = ''.join('<li><button type="button" class="rt-s" data-step="%d"%s aria-pressed="%s"><span class="rt-n">%d</span><span><b>%s</b><em>%s</em></span></button></li>' % (
        i + 1, pt(s), 'true' if i + 1 == sel else 'false', i + 1, e(s['title']), e(s['what'])) for i, s in enumerate(st))
    det = ''.join('<div class="rt-d" data-step="%d"%s><div><small>Step %d</small><b>%s</b><p>%s</p></div><dl><dt>Needs</dt><dd>%s</dd><dt>We measure</dt><dd>%s</dd><dt>How long</dt><dd>%s</dd></dl></div>' % (
        i + 1, '' if i + 1 == sel else ' hidden', i + 1, e(s['title']), e(s['what']), e(s['needs']), e(s['measure']), e(s['when'])) for i, s in enumerate(st))
    f = b['fork']
    doors = ''.join('<button type="button" class="rt-door rt-%s" data-text="%s"><span class="rt-tab">Opens %s</span><b>%s</b><em>%s</em></button>' % (
        TAB_KEY[o['tab']], e(o['say']), e(o['tab']), e(o['label']), e(o['what'])) for o in f['options'])
    return ('<section class="sx-block sx-route" data-block="route"><ol class="rt-line" style="--n:%d">%s</ol><div class="rt-sheet" aria-live="polite">%s</div>'
            '<div class="rt-fork"><div class="rt-q"><span class="rt-bulb">%s</span><b>%s</b></div><div class="rt-doors">%s</div></div></section>') % (
        len(st), stations, det, BULB, e(f['question']), doors)

RENDER = {'heading': r_heading, 'sheets': r_sheets, 'tracks': r_tracks, 'weigh': r_weigh, 'signoff': r_signoff, 'split': r_split,
          'revisions': r_revisions, 'scales': r_scales, 'plan': r_plan, 'register': r_register,
          'puzzle': r_puzzle, 'untangle': r_untangle, 'maze': r_maze,
          'knots': r_knots, 'stake': r_stake, 'route': r_route}

# ---------------------------------------------------------------------------------------------- validation

# ---------------------------------------------------------------------------------------------- simple English, stricter than the shared list
SIMPLE = {'via': 'through', 'ensure': 'make sure', 'prior to': 'before', 'additional': 'more', 'approximately': 'about', 'utilise': 'use',
          'numerous': 'many', 'obtain': 'get', 'require': 'need', 'requires': 'needs', 'regarding': 'about', 'assist': 'help', 'initiate': 'start',
          'component': 'part', 'components': 'parts', 'implement': 'put in place', 'implementation': 'putting it in place', 'optimal': 'best',
          'streamline': 'simplify', 'visibility': 'a clear view', 'alignment': 'agreement', 'enable': 'let', 'enables': 'lets', 'key stakeholders': 'people involved'}
SKIP_KEYS = {'id', 'type', 'register', 'tool', 'tab', 'context', 'source', 'status', 'state', 'lens', 'kind', 'user_tag', 'resistance'}
MAX_SENTENCE = 20

def simple_check(spec):
    """Sentences of at most 20 words, no dash or semicolon joining two thoughts, and a few more plain words (06 §5.8)."""
    out = []
    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k not in SKIP_KEYS: walk(v, '%s.%s' % (path, k) if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o): walk(v, '%s[%d]' % (path, i))
        elif isinstance(o, str) and o.strip():
            if path.startswith('turn.user_message'): return
            for sent in re.split(r'(?<=[.?!])\s+', o):
                n = len(sent.split())
                if n > MAX_SENTENCE: out.append('%s: a sentence of %d words; keep each under %d' % (path, n, MAX_SENTENCE + 1))
            if re.search(r'\s[—–]\s|;', o): out.append('%s: a dash or semicolon joins two thoughts; make two sentences' % path)
            if re.search(r'\btabs?\b', o, re.I): out.append('%s: never say “tab” to the user; name the place (Solutions, Automations, Processes)' % path)
            low = ' %s ' % re.sub(r'[^a-z ]', ' ', o.lower())
            for w, rep in SIMPLE.items():
                if ' %s ' % w in low: out.append('%s: “%s” → write “%s”' % (path, w, rep))
    walk(spec, '')
    return out

def validate(spec, reg=None):
    reg = reg or load_registry()
    ttype = spec.get('turn', {}).get('type')
    blocks = spec.get('canvas', {}).get('blocks', [])
    if ttype == 'landing':
        errs, warns = [], []
        if len(blocks) != 1 or blocks[0].get('type') != 'landing':
            errs.append('canvas: a landing turn has exactly one block, "landing"')
        else:
            rb = {b['id']: b for b in reg['blocks']}['landing']
            dh.check_fields('canvas.blocks[0](landing)', rb['slots'], blocks[0], errs, warns)
        s2 = copy.deepcopy(spec); s2['canvas'] = {'blocks': [{'type': 'heading', 'eyebrow': 'x', 'title': 'x'}]}
        e2, w2 = dh.validate(s2, reg)
        errs += [x for x in e2 if not x.startswith('canvas')]
        warns += [x for x in w2 if not x.startswith('canvas') and 'no canvas item has point' not in x]
        errs += ['plain English: ' + p for p in dh.plain_check(spec, reg) if 'canvas' in p]
        if spec.get('chat', {}).get('question'): errs.append('chat.question: a landing turn has no structured question (06 §11.3)')
        if spec.get('chat', {}).get('invite'): errs.append('chat.invite: a landing turn has no invitation (06 §11.3)')
        errs += ['simple English: ' + x for x in simple_check(spec)]
        return errs, warns
    errs, warns = dh.validate(spec, reg)
    errs = [x for x in errs if 'only “sage” exists' not in x]
    for i, b in enumerate(blocks):
        if b.get('type') == 'landing':
            errs.append('canvas.blocks[%d]: "landing" is only for landing turns' % i)
        if ttype in ('question', 'data-ask') and b.get('type') in reg['withheld_in_fact_turns']:
            errs.append('canvas.blocks[%d](%s): not allowed in a %s turn — a cost set against a return is a recommendation; hold it back (06 §4)' % (i, b['type'], ttype))
    rec = reg['turn_recipes'].get(ttype)
    if rec:
        for i, b in enumerate(blocks):
            if b.get('type') not in ('heading',) and b.get('type') not in rec:
                warns.append('canvas.blocks[%d](%s): not in the %s recipe %s — check it is the right block' % (i, b.get('type'), ttype, rec))
    for i, b in enumerate(blocks):   # block-specific checks, for every block
        if b.get('type') == 'puzzle':
            ns = sorted(p.get('n') for p in b.get('pieces', []))
            if ns != [1, 2, 3, 4, 5]: errs.append('canvas.blocks[%d](puzzle): pieces must be numbered 1 to 5' % i)
            for j, p in enumerate(b.get('pieces', [])):
                for r in p.get('relies_on', []):
                    if r not in ns or r == p.get('n'): errs.append('canvas.blocks[%d](puzzle).pieces[%d].relies_on: %s is not another piece' % (i, j, r))
            if b.get('default') is not None and b['default'] not in [0] + ns: errs.append('canvas.blocks[%d](puzzle).default: pick 0 (the idea) or a piece number' % i)
        if b.get('type') == 'maze':
            k = [r.get('kind') for r in b.get('routes', [])]
            if k.count('way') != 1 or not 2 <= k.count('dead') <= 3 or k[-1] != 'way':
                errs.append('canvas.blocks[%d](maze): 2 or 3 dead ends, then exactly one way through, last' % i)
        if b.get('type') == 'untangle':
            for j, t in enumerate(b.get('threads', [])):
                for f in ('today_end', 'with_start', 'with_end'):
                    if not re.match(r'^\d{1,2}:\d{2}$', str(t.get(f, ''))): errs.append('canvas.blocks[%d](untangle).threads[%d].%s: a time like 13:30' % (i, j, f))
        if b.get('type') == 'knots':
            for j, g in enumerate(b.get('segments', [])):
                for h in g.get('how', []):
                    if h.get('part') not in g.get('undone_by', []): errs.append('canvas.blocks[%d](knots).segments[%d]: "how" names part %s, which is not in undone_by' % (i, j, h.get('part')))
            segs = b.get('segments', [])
            for j in range(1, len(segs)):
                if segs[j].get('from') != segs[j - 1].get('to'): errs.append('canvas.blocks[%d](knots).segments[%d]: starts at %s but the one before ends at %s' % (i, j, segs[j].get('from'), segs[j - 1].get('to')))
        if b.get('type') == 'route':
            for j, o in enumerate(b.get('fork', {}).get('options', [])):
                if o.get('tab') not in TAB_KEY: errs.append('canvas.blocks[%d](route).fork.options[%d].tab: one of %s' % (i, j, ', '.join(TAB_KEY)))
        if b.get('type') == 'register':
            for j, it in enumerate(b.get('items', [])):
                if len(it.get('lenses', [])) != it.get('total'):
                    errs.append('canvas.blocks[%d](register).items[%d]: lists %d areas but counts "of %d"; they must match' % (i, j, len(it.get('lenses', [])), it.get('total')))
                if it.get('status') == 'agreed' and it.get('settled') != it.get('total'):
                    errs.append('canvas.blocks[%d](register).items[%d]: "agreed" needs every area settled (%s of %s)' % (i, j, it.get('settled'), it.get('total')))
    if spec.get('turn', {}).get('tab', 'Solutions') != 'Solutions':
        errs.append('turn.tab: this generator only draws Solutions turns')
    errs += ['simple English: ' + x for x in simple_check(spec)]
    errs += moves_check(spec)
    return errs, warns

def moves_check(spec):
    out = []
    ch = spec.get('chat', {}); prompts = ch.get('prompts', [])
    for j, m in enumerate(ch.get('moves', [])):
        if m.get('prompt') not in prompts: out.append('chat.moves[%d]: "%s" is not one of the prompts' % (j, m.get('prompt')))
        if m.get('tab') not in ('Automations', 'Processes', 'Diagnosis'): out.append('chat.moves[%d].tab: Automations, Processes or Diagnosis' % j)
    return out

def tone_of(spec, reg):
    if spec.get('canvas', {}).get('tone'): return spec['canvas']['tone']
    if spec['turn'].get('type') == 'landing': return 'blueprint'
    m = re.search(r'(\d+)$', spec['turn'].get('id', '1'))
    n = int(m.group(1)) if m else 1
    rot = reg['tones']['rotation']
    return rot[(max(n, 1) - 1) % len(rot)]

# ---------------------------------------------------------------------------------------------- pages
def render_canvas(spec, reg=None):
    reg = reg or load_registry()
    blocks = spec['canvas']['blocks']
    if spec['turn']['type'] == 'landing':
        return r_landing(blocks[0], spec['canvas'].get('state', 'filled'))
    inner = ''.join(RENDER[b['type']](b) for b in blocks)
    return ('<div class="sx-host"><div class="sx" data-tone="%s" data-turn="%s" data-generator="%s"><div class="sx-stack">%s</div></div></div>' % (
        tone_of(spec, reg), e(spec['turn']['id']), GEN, inner))

PAGE_JS = r'''
(function(){
  var input=document.getElementById('tojo-input');
  var pts=[].slice.call(document.querySelectorAll('.sh-pt'));
  function sel(){return pts.filter(function(p){return p.getAttribute('aria-pressed')==='true';}).map(function(p){return p.getAttribute('data-n');});}
  function tags(){return sel().map(function(n){return '@Point'+n;}).join(' ');}
  function say(t){var g=tags();input.value=(g?g+' ':'')+t;input.focus();}
  pts.forEach(function(p){p.addEventListener('click',function(){
    p.setAttribute('aria-pressed',p.getAttribute('aria-pressed')==='true'?'false':'true');
    var s=sel();[].slice.call(document.querySelectorAll('[data-pt]')).forEach(function(el){el.classList.toggle('is-lit',s.indexOf(el.getAttribute('data-pt'))>=0);});
    var g=tags();input.value=(g?g+' ':'')+input.value.replace(/@Point\d+\s*/g,'');});});
  [].slice.call(document.querySelectorAll('.sh-pr,.sh-opt,.lp-act,.rt-door')).forEach(function(b){b.addEventListener('click',function(){say(b.getAttribute('data-text'));});});
  [].slice.call(document.querySelectorAll('.lp-refresh')).forEach(function(b){b.addEventListener('click',function(){
    var s=b.closest('.lp-stamp');s.querySelector('.lp-stamp-at').textContent=b.getAttribute('data-fresh');
    s.querySelector('.lp-stamp-since').textContent=b.getAttribute('data-fresh-since');b.classList.add('is-done');});});
  // puzzle: pick a piece to lift it, outline what it relies on, and show its sheet
  [].slice.call(document.querySelectorAll('.sx-puzzle')).forEach(function(pz){
    var rel={};[].slice.call(pz.querySelectorAll('.sx-pz-d')).forEach(function(d){
      rel[d.getAttribute('data-piece')]=[].slice.call(d.querySelectorAll('.sx-pz-go')).map(function(g){return g.getAttribute('data-go');});});
    function pick(n){n=String(n);pz.setAttribute('data-sel',n);
      [].slice.call(pz.querySelectorAll('.sx-pz-shape')).forEach(function(s){var k=s.getAttribute('data-piece');
        s.classList.toggle('is-sel',k===n);s.classList.toggle('is-rel',(rel[n]||[]).indexOf(k)>=0);});
      [].slice.call(pz.querySelectorAll('.sx-pz-face')).forEach(function(f){f.setAttribute('aria-pressed',f.getAttribute('data-piece')===n?'true':'false');});
      [].slice.call(pz.querySelectorAll('.sx-pz-d')).forEach(function(d){d.hidden=d.getAttribute('data-piece')!==n;});}
    var sheet=pz.querySelector('.sx-pz-sheet');
    [].slice.call(pz.querySelectorAll('.sx-pz-face')).forEach(function(f){f.addEventListener('click',function(){pick(f.getAttribute('data-piece'));
      if(f.closest('.sx-pz-narrow')){try{sheet.scrollIntoView({block:'nearest',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}catch(e){}}});});
    [].slice.call(pz.querySelectorAll('.sx-pz-go')).forEach(function(g){g.addEventListener('click',function(){pick(g.getAttribute('data-go'));});});
    pick(pz.getAttribute('data-sel'));});
  // untangle: Today / With switch, and pick a thread for its detail
  [].slice.call(document.querySelectorAll('.sx-untangle')).forEach(function(u){
    function row(n){n=String(n);u.setAttribute('data-sel',n);
      [].slice.call(u.querySelectorAll('.ut-lab')).forEach(function(l){l.setAttribute('aria-pressed',l.getAttribute('data-row')===n?'true':'false');});
      [].slice.call(u.querySelectorAll('.ut-w')).forEach(function(w){w.classList.toggle('is-sel',w.getAttribute('data-row')===n);});
      [].slice.call(u.querySelectorAll('.ut-d')).forEach(function(d){d.hidden=d.getAttribute('data-row')!==n;});}
    [].slice.call(u.querySelectorAll('.ut-switch button')).forEach(function(b){b.addEventListener('click',function(){
      u.setAttribute('data-state',b.getAttribute('data-state'));
      [].slice.call(u.querySelectorAll('.ut-switch button')).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});});});
    [].slice.call(u.querySelectorAll('.ut-lab')).forEach(function(l){l.addEventListener('click',function(){row(l.getAttribute('data-row'));});});
    row(u.getAttribute('data-sel'));});
  // maze: pick a route to walk it; the bulb lights on the way through
  [].slice.call(document.querySelectorAll('.sx-maze')).forEach(function(m){
    function route(n){n=String(n);m.setAttribute('data-sel',n);
      var way=m.querySelector('.mz-r[data-route="'+n+'"]');m.setAttribute('data-way',way&&way.classList.contains('mz-r-way')?'on':'off');
      [].slice.call(m.querySelectorAll('.mz-r')).forEach(function(r){r.setAttribute('aria-pressed',r.getAttribute('data-route')===n?'true':'false');});
      [].slice.call(m.querySelectorAll('.mz-trail,.mz-pin')).forEach(function(t){t.classList.toggle('is-sel',t.getAttribute('data-route')===n);});
      [].slice.call(m.querySelectorAll('.mz-d')).forEach(function(d){d.hidden=d.getAttribute('data-route')!==n;});}
    [].slice.call(m.querySelectorAll('.mz-r')).forEach(function(r){r.addEventListener('click',function(){route(r.getAttribute('data-route'));});});
    route(m.getAttribute('data-sel'));});
  // knots: pick parts; a knot comes undone only when every part it needs is picked
  [].slice.call(document.querySelectorAll('.sx-knots')).forEach(function(k){
    var total=+k.getAttribute('data-total'),count=+k.getAttribute('data-count');
    function dur(m){var h=Math.floor(m/60),r=m%60;return [h?(h+' hour'+(h===1?'':'s')):'',r?(r+' minutes'):''].filter(Boolean).join(' ');}
    function on(){return [].slice.call(k.querySelectorAll('.kn-p[aria-pressed=true]')).map(function(b){return b.getAttribute('data-part');});}
    function upd(){var o=on(),n=0,m=0;
      [].slice.call(k.querySelectorAll('.kn-k')).forEach(function(x){var need=x.getAttribute('data-need').split(',');
        var done=need.every(function(p){return o.indexOf(p)>=0;});var part=!done&&need.some(function(p){return o.indexOf(p)>=0;});
        x.classList.toggle('is-undone',done);x.classList.toggle('is-half',part);if(done){n++;m+=+x.getAttribute('data-min');}});
      k.querySelector('.kn-n').textContent=n+' of '+count;
      k.querySelector('.kn-h').textContent=n?('they cover '+dur(m)+' of the '+dur(total)):('the wait is '+dur(total));}
    function seg(n){n=String(n);[].slice.call(k.querySelectorAll('.kn-k')).forEach(function(x){x.setAttribute('aria-pressed',x.getAttribute('data-seg')===n?'true':'false');});
      [].slice.call(k.querySelectorAll('.kn-d')).forEach(function(d){d.hidden=d.getAttribute('data-seg')!==n;});}
    [].slice.call(k.querySelectorAll('.kn-p')).forEach(function(b){b.addEventListener('click',function(){b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');upd();});});
    k.querySelector('.kn-all').addEventListener('click',function(){[].slice.call(k.querySelectorAll('.kn-p')).forEach(function(b){b.setAttribute('aria-pressed','true');});upd();});
    k.querySelector('.kn-clear').addEventListener('click',function(){[].slice.call(k.querySelectorAll('.kn-p')).forEach(function(b){b.setAttribute('aria-pressed','false');});upd();});
    [].slice.call(k.querySelectorAll('.kn-k')).forEach(function(x){x.addEventListener('click',function(){seg(x.getAttribute('data-seg'));});});
    seg(1);upd();});
  // stake: the share won back moves the green bar and tips the beam
  [].slice.call(document.querySelectorAll('.sx-stake')).forEach(function(st){
    var S=+st.getAttribute('data-stake'),C=+st.getAttribute('data-cost'),r=st.querySelector('.st-range');
    function money(l){return l>=100?('₹'+(Math.round(l)/100).toString()+' crore'):('₹'+Math.round(l)+' lakh');}
    st.querySelector('.st-f-cost').style.width=Math.max(100*C/S,0.4)+'%';
    function upd(){var v=+r.value,w=S*v/100,times=w/C;
      st.querySelector('.st-pc').textContent=v+'%';st.querySelector('.st-won').textContent=money(w);
      st.querySelector('.st-f-won').style.width=v+'%';
      var ang=Math.max(-14,Math.min(14,Math.log(times)/Math.log(10)*6));st.querySelector('.st-arm').style.transform='rotate('+ang+'deg)';
      st.querySelector('.st-w-r').setAttribute('r',Math.max(4,Math.min(16,4+Math.log(times+1)*3)));
      st.querySelector('.st-read').textContent=(times>=1?('That covers the team about '+Math.round(times)+' times over.'):('That covers less than the team costs.'))+' Worked out from your figures.';
      [].slice.call(st.querySelectorAll('.st-pre')).forEach(function(b){b.setAttribute('aria-pressed',+b.getAttribute('data-v')===v?'true':'false');});}
    r.addEventListener('input',upd);
    [].slice.call(st.querySelectorAll('.st-pre')).forEach(function(b){b.addEventListener('click',function(){r.value=b.getAttribute('data-v');upd();});});
    upd();});
  // route: pick a step for its sheet
  [].slice.call(document.querySelectorAll('.sx-route')).forEach(function(rt){
    [].slice.call(rt.querySelectorAll('.rt-s')).forEach(function(b){b.addEventListener('click',function(){var n=b.getAttribute('data-step');
      [].slice.call(rt.querySelectorAll('.rt-s')).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
      [].slice.call(rt.querySelectorAll('.rt-d')).forEach(function(d){d.hidden=d.getAttribute('data-step')!==n;});});});
    [].slice.call(rt.querySelectorAll('.rt-door')).forEach(function(d){d.addEventListener('click',function(){
      [].slice.call(rt.querySelectorAll('.rt-door')).forEach(function(x){x.classList.toggle('is-picked',x===d);});});});});
  // "Ask Tojo about this part\": attach its point and write the message
  [].slice.call(document.querySelectorAll('.sx-ask')).forEach(function(b){b.addEventListener('click',function(){
    var n=b.getAttribute('data-ask-pt');if(n){pts.forEach(function(p){if(p.getAttribute('data-n')===n&&p.getAttribute('aria-pressed')!=='true')p.click();});}
    say(b.getAttribute('data-text'));});});
  // tell a review page how tall this page is
  function tell(){try{parent.postMessage({tojoHeight:document.documentElement.scrollHeight,tojoId:document.documentElement.getAttribute('data-frame')},'*');}catch(e){}}
  window.addEventListener('load',tell);setTimeout(tell,900);
})();
'''

def css_all():
    import importlib.util
    spec = importlib.util.spec_from_file_location('so_landing', os.path.join(HERE, 'landing.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return lc.LP_BASE_CSS + mod.CSS + open(CSS_PATH, encoding='utf-8').read()

def render_page(spec, view='desktop', reg=None, fonts=True):
    reg = reg or load_registry()
    canvas = render_canvas(spec, reg)
    chat = user_msg(spec) + chat_parts(spec['chat'])
    for m in spec['chat'].get('moves', []):
        key = 'data-text="%s">' % e(m['prompt'])
        chat = chat.replace(key, key + '<span class="sh-move sh-move-%s">Opens %s</span>' % (TAB_KEY.get(m['tab'], 'x'), e(m['tab'])), 1)
    if view == 'canvas':
        body = '<div style="background:%s;max-width:936px">%s</div>' % (THEME['ground'], canvas)
    elif view == 'desktop':
        body = lc.desktop(TAB, THEME, canvas, chat, False, 0)
    else:
        body = lc.mobile(TAB, THEME, canvas, chat, False, 0)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<title>%s · %s</title>%s<style>%s%s%s</style></head><body>%s<script>%s</script></body></html>') % (
        e(spec['turn']['id']), e(TAB), lc.embedded_fonts() if fonts else '', lc.SHELL_CSS, lc.LP_SHELL_CSS, css_all(), body, PAGE_JS)

TYPE_NAMES = {'landing': 'Landing page', 'overview': 'Overview', 'part': 'One part', 'question': 'Question', 'data-ask': 'Asking for figures',
              'data-back': 'Real numbers in', 'findings': 'Findings', 'diagnosis': 'Diagnosis', 'elaboration': 'Going deeper', 'progress': 'Progress',
              'challenge': 'A challenge', 'recommendation': 'Recommendation', 'scripted': 'Scripted'}

def review_turn(spec, reg, note=''):
    blocks = spec['canvas']['blocks']
    title = next((b.get('title') for b in blocks if b.get('type') == 'heading'), None) or (blocks[0].get('standing') if blocks else '')
    return {'id': spec['turn']['id'], 'type': TYPE_NAMES.get(spec['turn']['type'], spec['turn']['type']), 'user': spec['turn'].get('user_message', ''),
            'title': title, 'note': note, 'desktop': render_page(spec, 'desktop', reg, fonts=False), 'mobile': render_page(spec, 'mobile', reg, fonts=False)}

# ---------------------------------------------------------------------------------------------- prompt
def catalog(reg):
    out = ['# Solutions canvas blocks — catalogue (registry v%d, %s)\n' % (reg['registry_version'], reg['updated']),
           'Use only these blocks in a Solutions turn. First block is always `heading` (except a `landing` turn, whose only block is `landing`). At most %d blocks after the heading.\n' % reg['budget']['max_blocks']]
    for b in reg['blocks']:
        out.append('## `%s` (%s)\n%s\n- Use when: %s\n- Avoid when: %s\n- Slots: %s\n' % (b['id'], b['status'], b['purpose'], '; '.join(b['use_when']), '; '.join(b['avoid_when']), json.dumps(slot_summary(b['slots']), ensure_ascii=False)))
    out.append('## Recipes by turn type\n' + '\n'.join('- `%s`: %s' % (k, ', '.join(v)) for k, v in reg['turn_recipes'].items()))
    return '\n'.join(out)

def slot_summary(slots):
    def one(s):
        t = s['type']
        opt = '' if s.get('required', True) else '?'
        if t == 'text': return 'text≤%dw%s' % (s.get('max_words', 99), opt)
        if t == 'enum': return 'one of %s%s' % ('|'.join(s['values']), opt)
        if t == 'number': return 'number' + opt
        if t == 'bool': return 'true/false' + opt
        if t == 'list': return ['%d–%d ×' % (s['min'], s['max']), one(s['item'])] + ([opt] if opt else [])
        if t == 'object': return {k + ('' if v.get('required', True) else '?'): one(v) for k, v in s['fields'].items()}
    return {k + ('' if v.get('required', True) else '?'): one(v) for k, v in slots.items()}

def prompt(reg):
    tpl = open(os.path.join(ROOT, 'prompts', 'tojo-api-system-prompt.md'), encoding='utf-8').read()
    rules = open(os.path.join(ROOT, 'rules', '06-html-response-rules.md'), encoding='utf-8').read()
    extra = ('\n\n# This turn is in the Solutions tab\nSet `turn.tab` to "Solutions". Use the Solutions catalogue below, not the Diagnosis one. '
             'A `landing` turn has one block, `landing`, and its chat has text, pointer, note, points and prompts only.\n\n')
    return tpl.replace('{{RULES_06}}', rules).replace('{{CATALOG}}', extra + catalog(reg))

# ---------------------------------------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate'); v.add_argument('spec')
    r = sub.add_parser('render'); r.add_argument('spec'); r.add_argument('--view', default='desktop', choices=['desktop', 'mobile', 'canvas']); r.add_argument('-o', '--out')
    b = sub.add_parser('build'); b.add_argument('dir', nargs='?', default=os.path.join(ROOT, 'examples', 'solutions')); b.add_argument('-o', '--out', default=os.path.join(ROOT, 'out', 'solutions'))
    sm = sub.add_parser('sample'); sm.add_argument('spec'); sm.add_argument('-o', '--out')
    sub.add_parser('prompt'); sub.add_parser('catalog')
    a = ap.parse_args(); reg = load_registry()
    if a.cmd == 'validate':
        spec = json.load(open(a.spec, encoding='utf-8')); errs, warns = validate(spec, reg)
        for w in warns: print('warn:', w)
        for x in errs: print('ERROR:', x)
        print('valid' if not errs else 'INVALID'); sys.exit(1 if errs else 0)
    if a.cmd == 'render':
        spec = json.load(open(a.spec, encoding='utf-8')); errs, _ = validate(spec, reg)
        if errs: print('\n'.join(errs), file=sys.stderr); sys.exit(1)
        out = render_page(spec, a.view, reg)
        (open(a.out, 'w', encoding='utf-8').write(out) if a.out else sys.stdout.write(out))
    if a.cmd == 'sample':
        spec = json.load(open(a.spec, encoding='utf-8')); errs, warns = validate(spec, reg)
        for x in errs + warns: print('   ', x, file=sys.stderr)
        if errs: sys.exit(1)
        out = review_page.page('%s · Solutions' % spec['turn']['id'], 'Solutions · ' + spec['turn']['id'], 'Discharge Process · generated by %s' % GEN, [review_turn(spec, reg)], book=False)
        (open(a.out, 'w', encoding='utf-8').write(out) if a.out else sys.stdout.write(out))
    if a.cmd == 'build':
        man = json.load(open(os.path.join(a.dir, 'turns.json'), encoding='utf-8'))
        tdir = os.path.join(a.out, 'turns'); os.makedirs(tdir, exist_ok=True); bad = 0; turns = []
        for t in man['turns']:
            spec = json.load(open(os.path.join(a.dir, t['file']), encoding='utf-8')); errs, warns = validate(spec, reg)
            name = t['file'][:-5]
            print('%-34s %s%s' % (name, 'valid' if not errs else 'INVALID', (' · %d warnings' % len(warns)) if warns else ''))
            for x in errs + warns: print('   ', x)
            if errs: bad += 1; continue
            rt = review_turn(spec, reg, t.get('note', ''))
            turns.append(rt)
            open(os.path.join(tdir, name + '.html'), 'w', encoding='utf-8').write(
                review_page.page('%s · Solutions' % spec['turn']['id'], 'Solutions · ' + spec['turn']['id'], 'Discharge Process · generated by %s' % GEN, [rt], book=False))
        args = ('Tojo Solutions Turns', 'Solutions · every turn', 'Discharge Process, 250-bed hospital, Bhubaneswar · generated by %s · %d turns' % (GEN, len(turns)), turns)
        open(os.path.join(a.out, 'solutions-tab.html'), 'w', encoding='utf-8').write(review_page.page(*args))
        open(os.path.join(a.out, 'solutions-tab.artifact.html'), 'w', encoding='utf-8').write(review_page.page(*args, fragment=True))
        print('wrote %d turn files to %s and the tab book solutions-tab.html' % (len(turns), tdir))
        sys.exit(1 if bad else 0)
    if a.cmd == 'prompt': print(prompt(reg))
    if a.cmd == 'catalog': print(catalog(reg))

if __name__ == '__main__':
    main()
