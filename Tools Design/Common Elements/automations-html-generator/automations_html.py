#!/usr/bin/env python3
"""
automations_html — the Automations tab generator.

Claude (through the API) writes a response spec: JSON with the turn, the chat parts and the canvas blocks
with their slots. This generator validates it against the Automations registry and draws the canvas offline
in the Automations look (the switch room), inside the app shell. No model writes HTML.

  python3 automations_html.py validate SPEC.json
  python3 automations_html.py render SPEC.json --view desktop|mobile -o OUT.html
  python3 automations_html.py sample SPEC.json -o OUT.html        # one turn: desktop and phone side by side, both live
  python3 automations_html.py build [SPEC_DIR] [-o OUT_DIR]      # every turn in SPEC_DIR/turns.json + the tab book
  python3 automations_html.py prompt                             # the Automations part of the API system prompt
  python3 automations_html.py catalog
Standard library only.
"""
import argparse, copy, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIAG = os.path.join(ROOT, 'diagnosis-html-generator')
COMMON = os.path.join(ROOT, 'landing-common')
SOL = os.path.join(ROOT, 'solutions-html-generator')
sys.path[:0] = [DIAG, COMMON]
import diagnosis_html as dh          # noqa: E402  shared slot checks, plain English, chat rules
import landing_common as lc          # noqa: E402  shared shell, stamp and buttons
from preview import chat_parts, user_msg   # noqa: E402  the chat panel is the same in every tab
import review_page                       # noqa: E402  desktop + phone review pages, shared by every tab

REG_PATH = os.path.join(HERE, 'registry.json')
CSS_PATH = os.path.join(HERE, 'assets', 'automations.css')
GEN = 'automations_html 1.0'
e = lc.e
TAB = 'Automations'
THEME = {'ground': '#E4E7EA', 'rail_bg': '#1C2A33', 'rail_fg': '#8FD3CD'}
SRC = {'yours': 'Your number', 'derived': 'Worked out from yours', 'estimate': 'Tojo’s guess', 'illustrative': 'Example only', 'target': 'Goal', 'needed': 'Need from you'}
STATUS = {'idea': 'Idea', 'designed': 'Designed', 'linked': 'Linked', 'testing': 'Testing', 'live': 'Switched on'}
TAB_KEY = {'Automations': 'au', 'Processes': 'pr', 'Solutions': 'so', 'Diagnosis': 'di'}


def _load_module(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def load_registry():
    reg = json.load(open(REG_PATH, encoding='utf-8'))
    reg['plain_english'] = dh.load_registry()['plain_english']
    return reg

def pt(o):
    return ' data-pt="%d"' % o['point'] if isinstance(o, dict) and o.get('point') is not None else ''

def src(s):
    return '<span class="ax-src ax-src-%s">%s</span>' % (s, SRC[s])

def _x(t, t0=18.0, t1=40.0):
    h, m = [int(v) for v in t.split(':')]; v = h + m / 60.0
    if v < t0: v += 24
    return max(0.0, min(100.0, 100.0 * (v - t0) / (t1 - t0)))

def _clock(t):
    h, m = [int(v) for v in t.split(':')]
    if h == 0 and m == 0: return 'midnight'
    if h == 12 and m == 0: return 'noon'
    return '%d%s %s' % (h % 12 or 12, (':%02d' % m) if m else '', 'AM' if h < 12 else 'PM')

def _hours(t):
    h, m = [int(v) for v in t.split(':')]; v = h + m / 60.0
    return v + 24 if v < 18 else v

# ---------------------------------------------------------------------------------------------- drawn marks
HAND = ('<svg class="ax-hand" viewBox="0 0 64 40" aria-hidden="true"><path class="ax-hand-m" d="M2 24 H14 L22 17 H33 C36 17 36 22 33 22 H25"/>'
        '<path class="ax-hand-m" d="M14 24 L14 31 H22"/><circle class="ax-hand-j" cx="14" cy="24" r="2.4"/><circle class="ax-hand-j" cx="22" cy="17" r="2.4"/>'
        '<path class="ax-hand-p" d="M62 22 H50 C46 22 44 19 40 19 H31 C28 19 28 24 31 24 H38 M50 22 C48 29 44 31 38 31 H30"/></svg>')
GEAR = ('<svg class="ax-gear" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 8.5a3.5 3.5 0 1 1 0 7a3.5 3.5 0 0 1 0-7z M12 2.5v3 M12 18.5v3 M2.5 12h3 M18.5 12h3 '
        'M5.3 5.3l2.1 2.1 M16.6 16.6l2.1 2.1 M5.3 18.7l2.1-2.1 M16.6 7.4l2.1-2.1"/></svg>')
BOT = ('<svg class="ax-bot" viewBox="0 0 120 120" aria-hidden="true"><rect class="ax-bot-s" x="18" y="16" width="84" height="64" rx="16"/>'
       '<rect class="ax-bot-scr" x="28" y="26" width="64" height="44" rx="10"/><circle class="ax-bot-e" cx="46" cy="46" r="5"/><circle class="ax-bot-e" cx="74" cy="46" r="5"/>'
       '<path class="ax-bot-m" d="M48 58 Q60 66 72 58"/><path class="ax-bot-s2" d="M52 80 L48 96 H72 L68 80"/><rect class="ax-bot-s" x="36" y="96" width="48" height="8" rx="4"/>'
       '<path class="ax-bot-a" d="M60 16 V6"/><circle class="ax-bot-t" cx="60" cy="5" r="4"/></svg>')
SILHOUETTE = ('<svg class="ax-holo" viewBox="0 0 200 200" aria-hidden="true"><defs>'
              '<linearGradient id="axh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3CD" stop-opacity=".55"/><stop offset="1" stop-color="#8FD3CD" stop-opacity=".04"/></linearGradient>'
              '<pattern id="axs" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.3" fill="#8FD3CD" fill-opacity=".35"/></pattern></defs>'
              '<g class="ax-holo-fig"><ellipse class="ax-holo-b" cx="100" cy="64" rx="25" ry="31"/><path class="ax-holo-b" d="M90 92 H110 V112 H90 Z"/>'
              '<path class="ax-holo-b" d="M36 176 C40 136 66 118 100 116 C134 118 160 136 164 176 Z"/>'
              '<ellipse class="ax-holo-s" cx="100" cy="64" rx="25" ry="31"/><path class="ax-holo-s" d="M36 176 C40 136 66 118 100 116 C134 118 160 136 164 176 Z"/>'
              '<g class="ax-holo-net"><path d="M88 52 L100 46 L112 54 L106 68 L94 70 Z M100 46 L106 68 M88 52 L106 68"/>'
              '<circle cx="88" cy="52" r="2.2"/><circle cx="100" cy="46" r="2.2"/><circle cx="112" cy="54" r="2.2"/><circle cx="106" cy="68" r="2.2"/><circle cx="94" cy="70" r="2.2"/></g></g>'
              '<ellipse class="ax-holo-base" cx="100" cy="182" rx="70" ry="9"/><ellipse class="ax-holo-base ax-holo-base2" cx="100" cy="182" rx="48" ry="5"/>'
              '<path class="ax-holo-beam" d="M30 182 L64 40 H136 L170 182 Z"/></svg>')

def _brain_svg(n_in=7, n_out=6, seed=7):
    """A digital brain on a wide screen: a wavy two-lobed outline, a mesh of glowing nodes, input wires on the left, output wires on the right."""
    import random
    rnd = random.Random(seed)
    W, H = 320, 210; cx, cy = W / 2.0, H / 2.0; rx, ry = 92, 78
    def outline(side):
        pts = []
        for i in range(0, 181, 6):
            t = math.radians(i) if side > 0 else math.radians(180 + i)
            r = 1 + 0.055 * math.sin(11 * t) + 0.03 * math.sin(5 * t + 1)
            x = cx + side * 3 + math.sin(t) * rx * r * (1 if side > 0 else -1) * (1 if side > 0 else -1)
            x = cx + side * (3 + abs(math.sin(t)) * rx * r)
            y = cy - math.cos(t) * ry * r
            pts.append((x, y))
        return 'M' + ' L'.join('%.1f %.1f' % p for p in pts)
    gyri = []
    for side in (-1, 1):
        for k in range(4):
            y0 = cy - ry * .62 + k * ry * .42
            d = 'M%.1f %.1f' % (cx + side * 12, y0)
            for j in range(1, 7):
                d += ' Q%.1f %.1f %.1f %.1f' % (cx + side * (12 + j * 11 - 5), y0 + (8 if j % 2 else -8), cx + side * (12 + j * 11), y0)
            gyri.append('<path class="ax-brain-g" d="%s"/>' % d)
    nodes = []
    while len(nodes) < 62:
        x = cx + (rnd.random() * 2 - 1) * rx * .92; y = cy + (rnd.random() * 2 - 1) * ry * .9
        if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < .82 and abs(x - cx) > 6: nodes.append((x, y))
    links = set()
    for i, (x, y) in enumerate(nodes):
        for j in sorted(range(len(nodes)), key=lambda j: (nodes[j][0] - x) ** 2 + (nodes[j][1] - y) ** 2)[1:3]:
            if (nodes[j][0] - cx) * (x - cx) > 0 or rnd.random() < .2: links.add(tuple(sorted((i, j))))
    ins = ''.join('<path class="ax-brain-w ax-brain-in" style="--d:%d" d="M0 %.1f C40 %.1f 50 %.1f %.1f %.1f"/>' % (
        k, 18 + k * (H - 36) / max(n_in - 1, 1), 18 + k * (H - 36) / max(n_in - 1, 1), cy + (k - n_in / 2.0) * 9, cx - rx * .96, cy + (k - n_in / 2.0) * 9) for k in range(n_in))
    outs = ''.join('<path class="ax-brain-w ax-brain-out" style="--d:%d" d="M%.1f %.1f C%.1f %.1f %.1f %.1f %d %.1f"/>' % (
        k, cx + rx * .96, cy + (k - n_out / 2.0) * 10, W - 50, cy + (k - n_out / 2.0) * 10, W - 40, 20 + k * (H - 40) / max(n_out - 1, 1), W, 20 + k * (H - 40) / max(n_out - 1, 1)) for k in range(n_out))
    return ('<svg class="ax-brain" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" aria-hidden="true">%s%s<path class="ax-brain-o" d="%s"/><path class="ax-brain-o" d="%s"/>%s%s%s</svg>' % (
        W, H, ins, outs, outline(-1), outline(1), ''.join(gyri),
        ''.join('<line class="ax-brain-l" style="--d:%d" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (k % 9, nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1]) for k, (i, j) in enumerate(sorted(links))),
        ''.join('<circle class="ax-brain-n" style="--d:%d" cx="%.1f" cy="%.1f" r="%.1f"/>' % (k % 7, x, y, 1.6 + (k % 3) * .7) for k, (x, y) in enumerate(nodes))))

# ---------------------------------------------------------------------------------------------- blocks
def r_heading(b):
    return '<header class="ax-hd"><div class="ax-eyebrow">%s</div><h2 class="ax-title">%s</h2>%s</header>' % (
        e(b['eyebrow']), e(b['title']), '<p class="ax-deck">%s</p>' % e(b['deck']) if b.get('deck') else '')

def r_landing(b, state):
    """The approved landing template (Automations B, the overnight arc), drawn from the spec's data."""
    mod = _load_module('au_landing', os.path.join(HERE, 'landing.py'))
    data = {'stamp': b['stamp'], 'standing': b['standing'], 'deck': b['deck'],
            'main': dict(b['main'], pt=b['main'].get('point')),
            'autos': [dict(a, hour=_hours(a['at']), pt=a.get('point')) for a in b['autos']],
            'evidence': b.get('evidence', ''), 'pending': [dict(p, pt=p.get('point')) for p in b['pending']], 'actions': b['actions']}
    return mod.sample_b(lc.Mode('html', state, {state: data}))

# --- nightshift: the automations as one production line through the night --------------------------------
def _line_map(st, t0, t1, long_gap=6.0):
    """Stations sit evenly along the line; a long gap (the night) gets more room. Returns time (hours) -> percent."""
    hs = [_hours(t0)] + [_hours(s['at']) for s in st] + [_hours(t1) + (24 if _hours(t1) < _hours(t0) else 0)]
    pos = [0.0]
    for a, b in zip(hs, hs[1:]): pos.append(pos[-1] + (2.4 if b - a >= long_gap else (0.6 if pos[-1] == 0 and len(pos) == 1 else 1.0)))
    top = pos[-1] or 1
    pos = [4 + 92 * p / top for p in pos]
    def f(h):
        if h <= hs[0]: return pos[0]
        for (a, pa), (b, pb) in zip(zip(hs, pos), zip(hs[1:], pos[1:])):
            if h <= b: return pa + (pb - pa) * ((h - a) / (b - a) if b > a else 1)
        return pos[-1]
    return f, list(zip(hs, pos))

def r_nightshift(b):
    st = sorted(b['stations'], key=lambda s: _hours(s['at']))
    t0, t1 = b.get('from', '18:00'), b.get('to', '16:00')
    fmap, anchors = _line_map(st, t0, t1)
    x = lambda t: fmap(_hours(t))
    now = b.get('start_at', '09:00'); sel = b.get('default', st[0]['n'])
    ticks = ''
    night = b['night']
    band = '<span class="ns-night" style="left:%.2f%%;width:%.2f%%"><em>%s</em></span>' % (x(night['from']), x(night['to']) - x(night['from']), e(night['label']))
    wide, rows, tray, det = [], [], [], []
    for k, s in enumerate(st):
        h = _hours(s['at']); human = s.get('hand')
        icon = HAND if human else GEAR
        wide.append('<button type="button" class="ns-st%s%s" data-st="%d" data-h="%.2f"%s style="left:%.2f%%" aria-pressed="%s"><span class="ns-box">%s<b>%d</b></span>'
                    '<span class="ns-lab"><small>%s</small>%s</span></button>' % (
                        ' ns-up' if k % 2 == 0 else ' ns-down', ' ns-human' if human else '', s['n'], h, pt(s), x(s['at']), 'true' if s['n'] == sel else 'false',
                        icon, s['n'], e(_clock(s['at'])), e(s['title'])))
        rows.append('<li><button type="button" class="ns-row%s" data-st="%d" data-h="%.2f"%s aria-pressed="%s"><span class="ns-rt">%s</span><span class="ns-box">%s<b>%d</b></span><span class="ns-rl">%s</span></button></li>' % (
            ' ns-human' if human else '', s['n'], h, pt(s), 'true' if s['n'] == sel else 'false', e(_clock(s['at'])), icon, s['n'], e(s['title'])))
        tray.append('<li class="ns-out" data-h="%.2f"><span class="ns-chk" aria-hidden="true"></span><span>%s</span></li>' % (h, e(s['makes'])))
        hand = ('<div class="ns-hd">%s<span><b>A person’s hand here: %s</b>%s</span></div>' % (HAND, e(human['who']), e(human['does']))) if human else \
               '<div class="ns-hd ns-hd-none">%s<span><b>No one needs to do anything</b>A person checks it later.</span></div>' % GEAR
        det.append('<div class="ns-d" data-st="%d"%s><div class="ns-dh"><small>%s · %s</small><b>%s</b><p>%s</p></div><dl><dt>It reads</dt><dd>%s</dd><dt>It makes</dt><dd>%s</dd>'
                   '<dt>Stage</dt><dd><span class="ax-tag ax-tag-%s">%s</span></dd></dl>%s</div>' % (
                       s['n'], '' if s['n'] == sel else ' hidden', e(_clock(s['at'])), 'Station %d' % s['n'], e(s['title']), e(s['does']), e(s['reads']), e(s['makes']),
                       s['status'], STATUS[s['status']], hand))
    leave = b['leaves']
    goal = '<span class="ns-leave" style="left:%.2f%%"><span>%s <b>%s</b> %s</span></span>' % (x(leave['at']), e(leave['label']), e(_clock(leave['at'])), src(leave['source']))
    opts = ''.join('<option value="%.2f"%s>%s</option>' % (_hours(t), ' selected' if t == now else '', e(_clock(t))) for t in b['clock'])
    return ('<section class="ax-block ax-ns" data-block="nightshift" data-now="%.2f" data-sel="%d" data-map="%s">'
            '<div class="ns-bar"><button type="button" class="ns-play" aria-label="Play the night">%s<span>Play the night</span></button>'
            '<label class="ns-clock"><span>Show the line at</span><input type="range" class="ns-range" min="%.2f" max="%.2f" step="0.25" value="%.2f" aria-label="Time of day"><output class="ns-now"></output></label>'
            '<select class="ns-pick" aria-label="Jump to a time">%s</select></div>'
            '<div class="ns-wide"><div class="ns-ticks">%s</div><div class="ns-floor">%s<div class="ns-belt"><span class="ns-flow" aria-hidden="true"></span></div>'
            '<span class="ns-hand" aria-hidden="true"></span>%s%s</div></div>'
            '<ol class="ns-narrow">%s</ol>'
            '<div class="ns-low"><div class="ns-tray"><div class="ax-label">Ready by <b class="ns-now2"></b></div><ul>%s</ul></div><div class="ns-sheet" aria-live="polite">%s</div></div>'
            '%s</section>') % (
        _hours(now), sel, json.dumps(anchors), '<svg viewBox="0 0 16 16" aria-hidden="true"><path class="ns-pl" d="M4 2.5 L13 8 L4 13.5 Z"/><path class="ns-pa" d="M4 3 V13 M11 3 V13"/></svg>',
        _hours(t0), _hours(t1) + (24 if _hours(t1) < _hours(t0) else 0), _hours(now), opts, ticks, band, ''.join(wide), goal,
        ''.join(rows), ''.join(tray), ''.join(det), '<p class="ax-cond">%s</p>' % e(b['condition']) if b.get('condition') else '')

# --- brain: the record that writes itself over the stay --------------------------------------------------
def r_brain(b):
    kinds = b['kinds']; secs = b['sections']; days = b['days']; sel = b.get('default_day', len(days))
    kin = ''.join('<li class="br-k" data-k="%s"%s><span class="br-dot" aria-hidden="true"></span><span><b>%s</b><em>%s</em></span><span class="br-c">0</span></li>' % (
        k['k'], pt(k), e(k['name']), e(k['example']), ) for k in kinds)
    sec = ''.join('<li class="br-s" data-kinds="%s"><span><b>%s</b></span><span class="br-bar" aria-hidden="true"><i></i></span><span class="br-p">0%%</span></li>' % (
        ','.join(s['from']), e(s['name'])) for s in secs)
    dayb = ''.join('<button type="button" class="br-day" data-day="%d" aria-pressed="%s"><b>%s</b><span>%s</span></button>' % (
        i + 1, 'true' if i + 1 == sel else 'false', e(d['label']), e(d['what'])) for i, d in enumerate(days))
    evs = json.dumps([[ev['k'] for ev in d['events']] for d in days])
    log = ''.join('<li class="br-ev" data-day="%d" data-k="%s"><span class="br-evk">%s</span>%s</li>' % (i + 1, ev['k'], e({k['k']: k['name'] for k in kinds}[ev['k']]), e(ev['text']))
                  for i, d in enumerate(days) for ev in d['events'])
    return ('<section class="ax-block ax-br" data-block="brain" data-day="%d" data-evs=\'%s\'>'
            '<div class="br-days" role="group" aria-label="Day of the stay">%s<button type="button" class="br-play">Play the stay</button></div>'
            '<div class="br-screen"><div class="br-col"><div class="br-h">What happens to the patient</div><ul class="br-kinds">%s</ul></div>'
            '<div class="br-mid">%s<div class="br-count"><b class="br-n">0</b> facts recorded, <span class="br-t">none typed twice</span></div></div>'
            '<div class="br-col"><div class="br-h">The discharge summary, filling in</div><ul class="br-secs">%s</ul></div></div>'
            '<details class="br-log"><summary>See what was recorded, day by day</summary><ul>%s</ul></details>%s</section>') % (
        sel, evs.replace("'", '&#39;'), dayb, kin, _brain_svg(len(kinds), len(secs)), sec, log, '<p class="ax-cond">%s</p>' % e(b['condition']) if b.get('condition') else '')

# --- agent: the thinker's loop, step by step, with the hand-offs to people -------------------------------
def r_agent(b):
    loop = b['loop']; steps = b['steps']; n = len(loop)
    R, C = 118, 150
    nodes = []
    for i, l in enumerate(loop):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x, y = C + R * math.cos(a), C + R * math.sin(a)
        nodes.append('<g class="ag-node" data-stage="%s"><circle cx="%.1f" cy="%.1f" r="26"/><text x="%.1f" y="%.1f">%s</text></g>' % (l['id'], x, y, x, y + 4, e(l['name'])))
    ring = '<circle class="ag-ring" cx="%d" cy="%d" r="%d"/><circle class="ag-run" cx="%d" cy="%d" r="%d"/>' % (C, C, R, C, C, R)
    cards = []
    for i, s in enumerate(steps):
        chk = ''.join('<li>%s</li>' % e(c) for c in s['checks'])
        hand = ('<div class="ag-hand">%s<span><b>Hands to %s</b>%s</span></div>' % (HAND, e(s['hand']['who']), e(s['hand']['does']))) if s.get('hand') else ''
        cards.append('<div class="ag-card" data-step="%d" data-stages="%s"%s%s><small>Step %d of %d · %s</small><b>%s</b><p>%s</p>'
                     '<div class="ax-label">What it checks first</div><ul>%s</ul>%s</div>' % (
                         i + 1, ','.join(s['stages']), pt(s), '' if i == 0 else ' hidden', i + 1, len(steps), e(s['when']), e(s['title']), e(s['does']), chk, hand))
    dots = ''.join('<button type="button" class="ag-dot" data-step="%d" aria-pressed="%s" aria-label="Step %d">%d</button>' % (i + 1, 'true' if i == 0 else 'false', i + 1, i + 1) for i in range(len(steps)))
    never = ''.join('<li>%s</li>' % e(x) for x in b['never'])
    return ('<section class="ax-block ax-ag" data-block="agent" data-step="1"><div class="ag-grid"><div class="ag-stage"><svg class="ag-loop" viewBox="0 0 300 300" aria-hidden="true">%s%s</svg>'
            '<div class="ag-person">%s</div><div class="ag-cap">%s</div></div>'
            '<div class="ag-side"><div class="ag-nav"><button type="button" class="ag-prev" aria-label="Back">&larr;</button>%s<button type="button" class="ag-next">Next step &rarr;</button></div>%s</div></div>'
            '<div class="ag-never"><span class="ax-label">Tojo never</span><ul>%s</ul></div></section>') % (
        ring, ''.join(nodes), SILHOUETTE, e(b['caption']), dots, ''.join(cards), never)

# --- sources: the switchboard of records and where they come from ----------------------------------------
def r_sources(b):
    srcs = b['sources']; autos = b['automations']; on = b.get('default_on', [s['id'] for s in srcs if s.get('no_it')])
    sw = []
    for s in srcs:
        recs = ''.join('<li><b>%s</b><span>%s</span></li>' % (e(r['name']), e(r['when'])) for r in s['records'])
        tag = '<span class="ax-tag ax-tag-none">No IT work</span>' if s.get('no_it') else '<span class="ax-tag ax-tag-%s">%s</span>' % (s['link'], {'waiting': 'Waiting on your IT team', 'linked': 'Linked', 'needed': 'Need from you'}[s['link']])
        sw.append('<li class="so-src%s" data-id="%s"%s><button type="button" class="so-sw" role="switch" aria-checked="%s" aria-label="%s"><span class="so-track"><span class="so-knob"></span></span></button>'
                  '<div class="so-b"><b>%s</b><span>%s</span>%s<details><summary>%d records it holds</summary><ul>%s</ul></details></div><span class="so-wire" aria-hidden="true"></span></li>' % (
                      ' so-noit' if s.get('no_it') else '', s['id'], pt(s), 'true' if s['id'] in on else 'false', e(s['name']), e(s['name']), e(s['holds']), tag, len(s['records']), recs))
    lamps = ''.join('<li class="so-auto" data-needs="%s"%s><span class="so-lamp" aria-hidden="true"></span><span><b>%s</b><em class="so-why"></em></span></li>' % (
        ','.join(a['needs']), pt(a), e(a['name'])) for a in autos)
    names = json.dumps({s['id']: s['short'] for s in srcs})
    pres = ''.join('<button type="button" class="so-pre" data-on="%s">%s</button>' % (','.join(p['on']), e(p['label'])) for p in b.get('presets', []))
    return ('<section class="ax-block ax-so" data-block="sources" data-names=\'%s\'><div class="so-bar"><span class="ax-label">Try it:</span>%s</div>'
            '<div class="so-board"><div class="so-col"><div class="ax-label">Where the records come from</div><ul class="so-srcs">%s</ul></div>'
            '<div class="so-bus" aria-hidden="true"><span></span></div>'
            '<div class="so-col"><div class="ax-label">Automations that can switch on</div><ul class="so-autos">%s</ul><p class="so-read" aria-live="polite"></p></div></div>%s</section>') % (
        names.replace("'", '&#39;'), pres, ''.join(sw), lamps, '<p class="ax-cond">%s</p>' % e(b['condition']) if b.get('condition') else '')

# --- helper: the desk helper who asks the IT team, in plain words or with the detail ---------------------
def r_helper(b):
    say = b['says']
    plain = ''.join('<li class="hp-i"><span class="hp-n">%d</span><span>%s</span></li>' % (i + 1, e(x)) for i, x in enumerate(b['plain']))
    detail = ''.join('<li class="hp-i"><span class="hp-n">%d</span><span><b>%s</b>%s</span></li>' % (i + 1, e(x['ask']), e(x['why'])) for i, x in enumerate(b['detail']))
    return ('<section class="ax-block ax-hp" data-block="helper" data-view="plain"><div class="hp-grid"><div class="hp-bot">%s<div class="hp-bubble"><span class="hp-say hp-v-plain">%s</span><span class="hp-say hp-v-detail">%s</span></div></div>'
            '<div class="hp-main"><div class="hp-sw" role="group" aria-label="How much detail"><button type="button" data-view="plain" aria-pressed="true">In plain words</button>'
            '<button type="button" data-view="detail" aria-pressed="false">With the detail (optional)</button></div>'
            '<ol class="hp-list hp-v-plain">%s</ol><ol class="hp-list hp-v-detail">%s</ol><p class="hp-park">%s</p></div></div></section>') % (
        BOT, e(say['plain']), e(say['detail']), plain, detail, e(b['park']))

# --- relay: the hand-over from discharge to the bed, each side checking the other ------------------------
def r_relay(b):
    legs = b['legs']; sel = b.get('default', 1)
    tr = []; n = len(legs)
    for i, l in enumerate(legs):
        tr.append('<li class="rl-leg rl-side-%s" data-leg="%d"%s style="grid-column:%d;grid-row:%d"><button type="button" class="rl-b" aria-pressed="%s"><span class="rl-who"><i class="rl-%s"></i>%s</span><b>%s</b>'
                  '<span class="rl-t"><span class="rl-today">%s</span><span class="rl-with">%s</span></span></button>%s</li>' % (
                      l['side'], i + 1, pt(l), i + 1, 1 if l['side'] == 'dis' else 2, 'true' if i + 1 == sel else 'false', l['side'], e(l['who']), e(l['name']), e(l['today']), e(l['with']),
                      '<span class="rl-check" title="Checked by the other side" aria-hidden="true"></span>' if l.get('checked_by') else ''))
    pts = ' '.join('%.2f,%d' % ((i + .5) * 100.0 / n, 25 if l['side'] == 'dis' else 75) for i, l in enumerate(legs))
    path = '<svg class="rl-path" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline points="%s"/></svg>' % pts
    det = ''.join('<div class="rl-d" data-leg="%d"%s><div><small>%s</small><b>%s</b><p>%s</p></div><dl><dt>Today</dt><dd>%s</dd><dt>With both linked</dt><dd>%s</dd><dt>Checked by</dt><dd>%s</dd></dl></div>' % (
        i + 1, '' if i + 1 == sel else ' hidden', e(l['who']), e(l['name']), e(l['how']), e(l['today']), e(l['with']), e(l.get('checked_by') or 'No one')) for i, l in enumerate(legs))
    g = b['gap']
    return ('<section class="ax-block ax-rl" data-block="relay" data-state="today"><div class="rl-bar"><div class="rl-switch" role="group" aria-label="Which picture">'
            '<button type="button" data-state="today" aria-pressed="true">Today</button><button type="button" data-state="with" aria-pressed="false">%s</button></div>'
            '<div class="rl-gap"><span class="ax-label">%s</span><span class="rl-gbar"><i class="rl-gt" style="width:%.1f%%"></i><i class="rl-gw" style="width:%.1f%%"></i><em style="left:%.1f%%">%s</em></span>'
            '<b class="rl-today">%s %s</b><b class="rl-with">%s %s</b></div></div>'
            '<div class="rl-lanes" style="--n:%d"><span class="rl-lane rl-lane-dis">Discharge side</span><span class="rl-lane rl-lane-bed">Bed side</span><div class="rl-track">%s</div><ol>%s</ol></div>'
            '<div class="rl-sheet" aria-live="polite">%s</div>%s</section>') % (
        e(b['with_label']), e(g['label']), 100.0 * g['today'] / g['scale'], 100.0 * g['with'] / g['scale'], 100.0 * g['line'] / g['scale'], e(g['line_label']),
        e(g['today_text']), src(g['today_source']), e(g['with_text']), src(g['with_source']), n, path, ''.join(tr), det, '<p class="ax-cond">%s</p>' % e(b['condition']) if b.get('condition') else '')

RENDER = {'heading': r_heading, 'nightshift': r_nightshift, 'brain': r_brain, 'agent': r_agent, 'sources': r_sources, 'helper': r_helper, 'relay': r_relay}

# ---------------------------------------------------------------------------------------------- simple English (same rules as Solutions)
SIMPLE = {'via': 'through', 'ensure': 'make sure', 'prior to': 'before', 'additional': 'more', 'approximately': 'about', 'utilise': 'use',
          'numerous': 'many', 'obtain': 'get', 'require': 'need', 'requires': 'needs', 'regarding': 'about', 'assist': 'help', 'initiate': 'start',
          'component': 'part', 'components': 'parts', 'implement': 'put in place', 'implementation': 'putting it in place', 'optimal': 'best',
          'streamline': 'simplify', 'visibility': 'a clear view', 'alignment': 'agreement', 'enable': 'let', 'enables': 'lets', 'key stakeholders': 'people involved',
          'api': 'link', 'database': 'records', 'server': 'computer', 'interface': 'screen', 'algorithm': 'rules', 'data': 'records', 'sync': 'keep in step',
          'real-time': 'as it happens', 'realtime': 'as it happens', 'pipeline': 'line'}
SKIP_KEYS = {'id', 'type', 'register', 'tool', 'tab', 'context', 'source', 'status', 'state', 'kind', 'user_tag', 'k', 'from', 'needs', 'on', 'side', 'link', 'stages',
             'today_source', 'with_source', 'short', 'at', 'clock', 'ticks', 'to', 'start_at'}
MAX_SENTENCE = 20

def simple_check(spec):
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
            low = ' %s ' % re.sub(r'[^a-z\- ]', ' ', o.lower())
            for w, rep in SIMPLE.items():
                if ' %s ' % w in low: out.append('%s: “%s” → write “%s”' % (path, w, rep))
    walk(spec, '')
    return out

def moves_check(spec):
    out = []
    ch = spec.get('chat', {}); prompts = ch.get('prompts', [])
    for j, m in enumerate(ch.get('moves', [])):
        if m.get('prompt') not in prompts: out.append('chat.moves[%d]: "%s" is not one of the prompts' % (j, m.get('prompt')))
        if m.get('tab') not in ('Solutions', 'Processes', 'Diagnosis'): out.append('chat.moves[%d].tab: Solutions, Processes or Diagnosis' % j)
    return out

def block_checks(blocks):
    errs = []
    t = re.compile(r'^\d{1,2}:\d{2}$')
    for i, b in enumerate(blocks):
        typ = b.get('type')
        if typ == 'nightshift':
            for f in ['start_at', 'clock']:
                vals = b.get(f) if isinstance(b.get(f), list) else [b.get(f)]
                for v in vals:
                    if v is not None and not t.match(str(v)): errs.append('canvas.blocks[%d](nightshift).%s: a time like 21:30' % (i, f))
            if b.get('start_at') not in b.get('clock', []): errs.append('canvas.blocks[%d](nightshift).start_at must be one of the clock times' % i)
            ns = [s.get('n') for s in b.get('stations', [])]
            if b.get('default') is not None and b['default'] not in ns: errs.append('canvas.blocks[%d](nightshift).default: a station number' % i)
        if typ == 'brain':
            ks = {k.get('k') for k in b.get('kinds', [])}
            for j, s in enumerate(b.get('sections', [])):
                for k in s.get('from', []):
                    if k not in ks: errs.append('canvas.blocks[%d](brain).sections[%d].from: "%s" is not a kind' % (i, j, k))
            for j, d in enumerate(b.get('days', [])):
                for ev in d.get('events', []):
                    if ev.get('k') not in ks: errs.append('canvas.blocks[%d](brain).days[%d]: event kind "%s" is not a kind' % (i, j, ev.get('k')))
        if typ == 'agent':
            ids = {l.get('id') for l in b.get('loop', [])}
            for j, s in enumerate(b.get('steps', [])):
                for st in s.get('stages', []):
                    if st not in ids: errs.append('canvas.blocks[%d](agent).steps[%d].stages: "%s" is not in the loop' % (i, j, st))
        if typ == 'sources':
            ids = {s.get('id') for s in b.get('sources', [])}
            for j, a in enumerate(b.get('automations', [])):
                for x in a.get('needs', []):
                    if x not in ids: errs.append('canvas.blocks[%d](sources).automations[%d].needs: "%s" is not a source' % (i, j, x))
            for j, p in enumerate(b.get('presets', [])):
                for x in p.get('on', []):
                    if x not in ids: errs.append('canvas.blocks[%d](sources).presets[%d].on: "%s" is not a source' % (i, j, x))
            for j, s in enumerate(b.get('sources', [])):
                if not s.get('no_it') and s.get('link') not in ('waiting', 'linked', 'needed'): errs.append('canvas.blocks[%d](sources).sources[%d].link: waiting, linked or needed' % (i, j))
    return errs

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
        errs += ['simple English: ' + x for x in simple_check(spec)] + moves_check(spec)
        return errs, warns
    errs, warns = dh.validate(spec, reg)
    errs = [x for x in errs if 'only “sage” exists' not in x]
    for i, b in enumerate(blocks):
        if b.get('type') == 'landing': errs.append('canvas.blocks[%d]: "landing" is only for landing turns' % i)
    rec = reg['turn_recipes'].get(ttype)
    if rec:
        for i, b in enumerate(blocks):
            if b.get('type') != 'heading' and b.get('type') not in rec:
                warns.append('canvas.blocks[%d](%s): not in the %s recipe %s — check it is the right block' % (i, b.get('type'), ttype, rec))
    errs += block_checks(blocks)
    if spec.get('turn', {}).get('tab', TAB) != TAB: errs.append('turn.tab: this generator only draws Automations turns')
    errs += ['simple English: ' + x for x in simple_check(spec)] + moves_check(spec)
    return errs, warns

# ---------------------------------------------------------------------------------------------- pages
def render_canvas(spec, reg=None):
    blocks = spec['canvas']['blocks']
    if spec['turn']['type'] == 'landing':
        return r_landing(blocks[0], spec['canvas'].get('state', 'filled'))
    inner = ''.join(RENDER[b['type']](b) for b in blocks)
    return '<div class="ax-host"><div class="ax" data-turn="%s" data-generator="%s"><div class="ax-stack">%s</div></div></div>' % (e(spec['turn']['id']), GEN, inner)

PAGE_JS = r'''
(function(){
  var input=document.getElementById('tojo-input');
  var pts=[].slice.call(document.querySelectorAll('.sh-pt'));
  function Q(r,s){return [].slice.call(r.querySelectorAll(s));}
  function sel(){return pts.filter(function(p){return p.getAttribute('aria-pressed')==='true';}).map(function(p){return p.getAttribute('data-n');});}
  function tags(){return sel().map(function(n){return '@Point'+n;}).join(' ');}
  function say(t){var g=tags();input.value=(g?g+' ':'')+t;input.focus();}
  pts.forEach(function(p){p.addEventListener('click',function(){
    p.setAttribute('aria-pressed',p.getAttribute('aria-pressed')==='true'?'false':'true');
    var s=sel();Q(document,'[data-pt]').forEach(function(el){el.classList.toggle('is-lit',s.indexOf(el.getAttribute('data-pt'))>=0);});
    var g=tags();input.value=(g?g+' ':'')+input.value.replace(/@Point\d+\s*/g,'');});});
  Q(document,'.sh-pr,.sh-opt,.lp-act').forEach(function(b){b.addEventListener('click',function(){say(b.getAttribute('data-text'));});});
  Q(document,'.lp-refresh').forEach(function(b){b.addEventListener('click',function(){
    var s=b.closest('.lp-stamp');s.querySelector('.lp-stamp-at').textContent=b.getAttribute('data-fresh');
    s.querySelector('.lp-stamp-since').textContent=b.getAttribute('data-fresh-since');b.classList.add('is-done');});});
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  function clock(h){var v=h%24,hh=Math.floor(v),mm=Math.round((v-hh)*60);if(mm===60){hh++;mm=0;}
    if(hh===0&&mm===0)return 'midnight';if(hh===12&&mm===0)return 'noon';return ((hh%12)||12)+(mm?':'+(mm<10?'0':'')+mm:'')+' '+(hh<12?'AM':'PM');}
  // nightshift: the clock moves along the line; stations light as their time passes; pick one for its sheet
  Q(document,'.ax-ns').forEach(function(n){
    var r=n.querySelector('.ns-range'),min=+r.min,max=+r.max,timer=null,play=n.querySelector('.ns-play'),pick=n.querySelector('.ns-pick');
    var mp=JSON.parse(n.getAttribute('data-map'));
    function px(h){if(h<=mp[0][0])return mp[0][1];for(var i=1;i<mp.length;i++){if(h<=mp[i][0]){var a=mp[i-1],b=mp[i];return a[1]+(b[1]-a[1])*((h-a[0])/((b[0]-a[0])||1));}}return mp[mp.length-1][1];}
    function at(h){r.value=h;n.querySelector('.ns-hand').style.left=px(h)+'%';
      n.querySelector('.ns-now').textContent=clock(h);n.querySelector('.ns-now2').textContent=clock(h);
      Q(n,'[data-h]').forEach(function(x){x.classList.toggle('is-done',+x.getAttribute('data-h')<=h+0.001);});}
    function st(k){k=String(k);Q(n,'.ns-st,.ns-row').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-st')===k?'true':'false');});
      Q(n,'.ns-d').forEach(function(d){d.hidden=d.getAttribute('data-st')!==k;});}
    function stop(){if(timer){clearInterval(timer);timer=null;}play.classList.remove('is-on');play.querySelector('span').textContent='Play the night';}
    r.addEventListener('input',function(){stop();at(+r.value);});
    pick.addEventListener('change',function(){stop();at(+pick.value);});
    play.addEventListener('click',function(){if(timer){stop();return;}var h=+r.value>=max-0.01?min:+r.value;play.classList.add('is-on');play.querySelector('span').textContent='Pause';
      if(reduce){at(max);stop();return;}timer=setInterval(function(){h+=0.25;if(h>=max){h=max;at(h);stop();return;}at(h);},120);});
    Q(n,'.ns-st,.ns-row').forEach(function(b){b.addEventListener('click',function(){st(b.getAttribute('data-st'));});});
    at(+n.getAttribute('data-now'));st(n.getAttribute('data-sel'));});
  // brain: pick a day of the stay; facts flow in and the summary fills
  Q(document,'.ax-br').forEach(function(br){
    var ev=JSON.parse(br.getAttribute('data-evs')),timer=null;
    function day(d){br.setAttribute('data-day',d);var c={},tot=0;
      for(var i=0;i<d;i++){ev[i].forEach(function(k){c[k]=(c[k]||0)+1;tot++;});}
      var all={};ev.forEach(function(x){x.forEach(function(k){all[k]=(all[k]||0)+1;});});
      Q(br,'.br-k').forEach(function(k){var v=c[k.getAttribute('data-k')]||0;k.querySelector('.br-c').textContent=v;k.classList.toggle('is-on',v>0);
        k.classList.toggle('is-new',(ev[d-1]||[]).indexOf(k.getAttribute('data-k'))>=0);});
      Q(br,'.br-s').forEach(function(s){var ks=s.getAttribute('data-kinds').split(','),a=0,b=0;ks.forEach(function(k){a+=c[k]||0;b+=all[k]||0;});
        var p=b?Math.round(100*a/b):0;s.querySelector('.br-bar i').style.width=p+'%';s.querySelector('.br-p').textContent=p+'%';s.classList.toggle('is-full',p===100);});
      br.querySelector('.br-n').textContent=tot;
      Q(br,'.br-day').forEach(function(b){b.setAttribute('aria-pressed',+b.getAttribute('data-day')===d?'true':'false');});
      Q(br,'.br-ev').forEach(function(x){x.hidden=+x.getAttribute('data-day')>d;});
      br.classList.remove('is-pulse');void br.offsetWidth;br.classList.add('is-pulse');}
    Q(br,'.br-day').forEach(function(b){b.addEventListener('click',function(){if(timer){clearInterval(timer);timer=null;}day(+b.getAttribute('data-day'));});});
    br.querySelector('.br-play').addEventListener('click',function(){if(timer)clearInterval(timer);var d=1;day(d);if(reduce){day(ev.length);return;}
      timer=setInterval(function(){d++;if(d>ev.length){clearInterval(timer);timer=null;return;}day(d);},1100);});
    day(+br.getAttribute('data-day'));});
  // agent: step through the loop
  Q(document,'.ax-ag').forEach(function(ag){
    var cards=Q(ag,'.ag-card'),n=cards.length;
    function go(k){k=Math.max(1,Math.min(n,k));ag.setAttribute('data-step',k);var st=cards[k-1].getAttribute('data-stages').split(',');
      cards.forEach(function(c,i){c.hidden=i!==k-1;});Q(ag,'.ag-dot').forEach(function(d){d.setAttribute('aria-pressed',+d.getAttribute('data-step')===k?'true':'false');});
      Q(ag,'.ag-node').forEach(function(x){x.classList.toggle('is-on',st.indexOf(x.getAttribute('data-stage'))>=0);});
      ag.querySelector('.ag-next').textContent=k===n?'Start again':'Next step →';ag.querySelector('.ag-prev').disabled=k===1;}
    ag.querySelector('.ag-next').addEventListener('click',function(){var k=+ag.getAttribute('data-step');go(k===n?1:k+1);});
    ag.querySelector('.ag-prev').addEventListener('click',function(){go(+ag.getAttribute('data-step')-1);});
    Q(ag,'.ag-dot').forEach(function(d){d.addEventListener('click',function(){go(+d.getAttribute('data-step'));});});
    go(1);});
  // sources: flip the switches; automations light when every source they need is on
  Q(document,'.ax-so').forEach(function(so){
    var names=JSON.parse(so.getAttribute('data-names'));
    function on(){return Q(so,'.so-src').filter(function(s){return s.querySelector('.so-sw').getAttribute('aria-checked')==='true';}).map(function(s){return s.getAttribute('data-id');});}
    function upd(){var o=on(),k=0,autos=Q(so,'.so-auto');
      Q(so,'.so-src').forEach(function(s){s.classList.toggle('is-on',o.indexOf(s.getAttribute('data-id'))>=0);});
      autos.forEach(function(a){var need=a.getAttribute('data-needs').split(','),miss=need.filter(function(x){return o.indexOf(x)<0;});
        a.classList.toggle('is-on',!miss.length);if(!miss.length)k++;
        a.querySelector('.so-why').textContent=miss.length?('Waits on '+miss.map(function(x){return names[x];}).join(' and ')):'Can switch on';});
      so.querySelector('.so-read').textContent=k+' of '+autos.length+' can switch on with these links.';
      Q(so,'.so-pre').forEach(function(p){var want=p.getAttribute('data-on').split(',').filter(Boolean).sort().join(',');p.setAttribute('aria-pressed',want===o.slice().sort().join(',')?'true':'false');});}
    Q(so,'.so-sw').forEach(function(b){b.addEventListener('click',function(){b.setAttribute('aria-checked',b.getAttribute('aria-checked')==='true'?'false':'true');upd();});});
    Q(so,'.so-pre').forEach(function(p){p.addEventListener('click',function(){var want=p.getAttribute('data-on').split(',');
      Q(so,'.so-src').forEach(function(s){s.querySelector('.so-sw').setAttribute('aria-checked',want.indexOf(s.getAttribute('data-id'))>=0?'true':'false');});upd();});});
    upd();});
  // helper: plain words or the detail
  Q(document,'.ax-hp').forEach(function(h){Q(h,'.hp-sw button').forEach(function(b){b.addEventListener('click',function(){
    h.setAttribute('data-view',b.getAttribute('data-view'));Q(h,'.hp-sw button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});});});});
  // relay: today or with both linked; pick a leg
  Q(document,'.ax-rl').forEach(function(rl){
    Q(rl,'.rl-switch button').forEach(function(b){b.addEventListener('click',function(){rl.setAttribute('data-state',b.getAttribute('data-state'));
      Q(rl,'.rl-switch button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});});});
    Q(rl,'.rl-leg').forEach(function(l){l.querySelector('.rl-b').addEventListener('click',function(){var k=l.getAttribute('data-leg');
      Q(rl,'.rl-leg .rl-b').forEach(function(x){x.setAttribute('aria-pressed',x.closest('.rl-leg')===l?'true':'false');});
      Q(rl,'.rl-d').forEach(function(d){d.hidden=d.getAttribute('data-leg')!==k;});});});});
  function tell(){try{parent.postMessage({tojoHeight:document.documentElement.scrollHeight,tojoId:document.documentElement.getAttribute('data-frame')},'*');}catch(e){}}
  window.addEventListener('load',tell);setTimeout(tell,900);
})();
'''

def css_all():
    mod = _load_module('au_landing', os.path.join(HERE, 'landing.py'))
    return lc.LP_BASE_CSS + mod.CSS + open(CSS_PATH, encoding='utf-8').read()

def render_page(spec, view='desktop', reg=None, fonts=True):
    reg = reg or load_registry()
    canvas = render_canvas(spec, reg)
    chat = user_msg(spec) + chat_parts(spec['chat'])
    for m in spec['chat'].get('moves', []):
        key = 'data-text="%s">' % e(m['prompt'])
        chat = chat.replace(key, key + '<span class="sh-move sh-move-%s">Opens %s</span>' % (TAB_KEY.get(m['tab'], 'x'), e(m['tab'])), 1)
    body = lc.desktop(TAB, THEME, canvas, chat, False, 0) if view == 'desktop' else lc.mobile(TAB, THEME, canvas, chat, False, 0)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<title>%s · %s</title>%s<style>%s%s%s</style></head><body>%s<script>%s</script></body></html>') % (
        e(spec['turn']['id']), e(TAB), lc.embedded_fonts() if fonts else '', lc.SHELL_CSS, lc.LP_SHELL_CSS, css_all(), body, PAGE_JS)

TYPE_NAMES = {'landing': 'Landing page', 'overview': 'Overview', 'part': 'One part', 'question': 'Question', 'data-ask': 'Asking for figures',
              'data-back': 'Your answer in', 'findings': 'Findings', 'elaboration': 'Going deeper', 'progress': 'Progress',
              'challenge': 'A challenge', 'recommendation': 'Recommendation', 'scripted': 'Scripted'}

def review_turn(spec, reg, note=''):
    blocks = spec['canvas']['blocks']
    title = next((b.get('title') for b in blocks if b.get('type') == 'heading'), None) or (blocks[0].get('standing') if blocks else '')
    return {'id': spec['turn']['id'], 'type': TYPE_NAMES.get(spec['turn']['type'], spec['turn']['type']), 'user': spec['turn'].get('user_message', ''),
            'title': title, 'note': note, 'desktop': render_page(spec, 'desktop', reg, fonts=False), 'mobile': render_page(spec, 'mobile', reg, fonts=False)}

# ---------------------------------------------------------------------------------------------- prompt
def slot_summary(slots):
    def one(s):
        t = s['type']; opt = '' if s.get('required', True) else '?'
        if t == 'text': return 'text≤%dw%s' % (s.get('max_words', 99), opt)
        if t == 'enum': return 'one of %s%s' % ('|'.join(s['values']), opt)
        if t in ('number', 'bool'): return t + opt
        if t == 'list': return ['%d–%d ×' % (s['min'], s['max']), one(s['item'])] + ([opt] if opt else [])
        if t == 'object': return {k + ('' if v.get('required', True) else '?'): one(v) for k, v in s['fields'].items()}
    return {k + ('' if v.get('required', True) else '?'): one(v) for k, v in slots.items()}

def catalog(reg):
    out = ['# Automations canvas blocks — catalogue (registry v%d, %s)\n' % (reg['registry_version'], reg['updated']),
           'Use only these blocks in an Automations turn. First block is always `heading` (except a `landing` turn, whose only block is `landing`). At most %d blocks after the heading.\n' % reg['budget']['max_blocks']]
    for b in reg['blocks']:
        out.append('## `%s` (%s · scope %s)\n%s\n- Use when: %s\n- Avoid when: %s\n- Slots: %s\n%s' % (
            b['id'], b['status'], b.get('scope', 'all'), b['purpose'], '; '.join(b['use_when']), '; '.join(b['avoid_when']),
            json.dumps(slot_summary(b['slots']), ensure_ascii=False), ('- Interaction: %s\n' % b['interaction']) if b.get('interaction') else ''))
    out.append('## Recipes by turn type\n' + '\n'.join('- `%s`: %s' % (k, ', '.join(v)) for k, v in reg['turn_recipes'].items()))
    return '\n'.join(out)

def prompt(reg):
    tpl = open(os.path.join(ROOT, 'prompts', 'tojo-api-system-prompt.md'), encoding='utf-8').read()
    rules = open(os.path.join(ROOT, 'rules', '06-html-response-rules.md'), encoding='utf-8').read()
    extra = ('\n\n# This turn is in the Automations tab\nSet `turn.tab` to "Automations". Use the Automations catalogue below. '
             'This tab takes the working detail of how things run by themselves: how each automation works, which records are tracked as they happen, '
             'what is read from which system, and what the IT team sets up. A `landing` turn has one block, `landing`.\n\n')
    return tpl.replace('{{RULES_06}}', rules).replace('{{CATALOG}}', extra + catalog(reg))

# ---------------------------------------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate'); v.add_argument('spec')
    r = sub.add_parser('render'); r.add_argument('spec'); r.add_argument('--view', default='desktop', choices=['desktop', 'mobile']); r.add_argument('-o', '--out')
    sm = sub.add_parser('sample'); sm.add_argument('spec'); sm.add_argument('-o', '--out')
    b = sub.add_parser('build'); b.add_argument('dir', nargs='?', default=os.path.join(ROOT, 'examples', 'automations')); b.add_argument('-o', '--out', default=os.path.join(ROOT, 'out', 'automations'))
    sub.add_parser('prompt'); sub.add_parser('catalog')
    a = ap.parse_args(); reg = load_registry()
    if a.cmd == 'validate':
        spec = json.load(open(a.spec, encoding='utf-8')); errs, warns = validate(spec, reg)
        for w in warns: print('warn:', w)
        for x in errs: print('ERROR:', x)
        print('valid' if not errs else 'INVALID'); sys.exit(1 if errs else 0)
    if a.cmd in ('render', 'sample'):
        spec = json.load(open(a.spec, encoding='utf-8')); errs, _ = validate(spec, reg)
        if errs: print('\n'.join(errs), file=sys.stderr); sys.exit(1)
        out = render_page(spec, a.view, reg) if a.cmd == 'render' else review_page.page('%s · Automations' % spec['turn']['id'], 'Automations · ' + spec['turn']['id'],
                                                                                          'Discharge Process · generated by %s' % GEN, [review_turn(spec, reg)], book=False)
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
            rt = review_turn(spec, reg, t.get('note', '')); turns.append(rt)
            open(os.path.join(tdir, name + '.html'), 'w', encoding='utf-8').write(review_page.page(
                '%s · Automations' % spec['turn']['id'], 'Automations · ' + spec['turn']['id'], 'Discharge Process · generated by %s' % GEN, [rt], book=False))
        args = ('Tojo Automations Turns', 'Automations · every turn', 'Discharge Process, 250-bed hospital, Bhubaneswar · generated by %s · %d turns' % (GEN, len(turns)), turns)
        open(os.path.join(a.out, 'automations-tab.html'), 'w', encoding='utf-8').write(review_page.page(*args))
        open(os.path.join(a.out, 'automations-tab.artifact.html'), 'w', encoding='utf-8').write(review_page.page(*args, fragment=True))
        print('wrote %d turn files to %s and the tab book automations-tab.html' % (len(turns), tdir))
        sys.exit(1 if bad else 0)
    if a.cmd == 'prompt': print(prompt(reg))
    if a.cmd == 'catalog': print(catalog(reg))

if __name__ == '__main__':
    main()
