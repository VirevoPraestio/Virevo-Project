#!/usr/bin/env python3
"""
processes_html — the Processes generator.

Claude (through the API) writes a response spec: JSON with the turn, the chat parts and the canvas blocks
with their slots. This generator validates it against the Processes registry and draws the canvas offline
in the Processes look (the ward board), inside the app shell. No model writes HTML.

  python3 processes_html.py validate SPEC.json
  python3 processes_html.py render SPEC.json --view desktop|mobile -o OUT.html
  python3 processes_html.py sample SPEC.json -o OUT.html        # one turn: desktop and phone side by side, both live
  python3 processes_html.py build [SPEC_DIR] [-o OUT_DIR]      # every turn in SPEC_DIR/turns.json + the book
  python3 processes_html.py prompt                             # the Processes part of the API system prompt
  python3 processes_html.py catalog
Standard library only.
"""
import argparse, copy, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIAG = os.path.join(ROOT, 'diagnosis-html-generator')
COMMON = os.path.join(ROOT, 'landing-common')
sys.path[:0] = [DIAG, COMMON]
import diagnosis_html as dh          # noqa: E402  shared slot checks, plain English, chat rules
import landing_common as lc          # noqa: E402  shared shell, stamp and buttons
from preview import chat_parts, user_msg   # noqa: E402  the chat panel is the same everywhere
import review_page                       # noqa: E402  desktop + phone review pages

REG_PATH = os.path.join(HERE, 'registry.json')
CSS_PATH = os.path.join(HERE, 'assets', 'processes.css')
GEN = 'processes_html 1.0'
e = lc.e
TAB = 'Processes'
THEME = {'ground': '#ECE8EE', 'rail_bg': '#2A1E30', 'rail_fg': '#E9C8F0'}
SRC = {'yours': 'Your number', 'derived': 'Worked out from yours', 'estimate': 'Tojo’s guess', 'illustrative': 'Example only', 'target': 'Goal', 'needed': 'Need from you', 'new': 'New, no starting number'}
TAB_KEY = {'Automations': 'au', 'Processes': 'pr', 'Solutions': 'so', 'Diagnosis': 'di'}
STATUS = {'agreed': 'Agreed', 'to_ask': 'Still to ask', 'worried': 'Has a worry'}


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
    return '<span class="px-src px-src-%s">%s</span>' % (s, SRC[s])

def lakh(lo, hi):
    f = lambda v: ('%g' % v)
    return '₹%s lakh' % f(lo) if lo == hi else '₹%s to %s lakh' % (f(lo), f(hi))

# ---------------------------------------------------------------------------------------------- drawn marks
MAGNET = '<svg class="px-mag" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8"/><circle class="px-mag-s" cx="7.5" cy="7.5" r="2.4"/></svg>'
def SEAT(on, cls=''):
    return ('<svg viewBox="0 0 40 44" class="px-seat %s%s" aria-hidden="true"><path class="px-seat-b" d="M10 4h20a3 3 0 013 3v15H7V7a3 3 0 013-3z"/>'
            '<path class="px-seat-c" d="M4 22h32v7H4z"/><path class="px-seat-l" d="M9 29v12M31 29v12"/></svg>') % ('on ' if on else '', cls)
CLIP = '<svg class="pp-clip" viewBox="0 0 30 16" aria-hidden="true"><path d="M8 0v6h14V0"/><rect x="5" y="5" width="20" height="9" rx="3"/></svg>'
TICK = '<svg class="px-tick" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7"/></svg>'

def initials(name):
    w = [x for x in re.split(r'[\s/]+', name) if x and x[0].isalpha() and x.lower() not in ('and', 'the', 'of')]
    return ''.join(x[0].upper() for x in w[:2]) or name[:1].upper()

# ---------------------------------------------------------------------------------------------- blocks
def r_heading(b):
    return '<header class="px-hd"><div class="px-eyebrow">%s%s</div><h2 class="px-title">%s</h2>%s</header>' % (
        MAGNET, e(b['eyebrow']), e(b['title']), '<p class="px-deck">%s</p>' % e(b['deck']) if b.get('deck') else '')

def r_landing(b, state):
    """The approved landing template (Processes A, the ward board), drawn from the spec's data."""
    mod = _load_module('pr_landing', os.path.join(HERE, 'landing.py'))
    P = lambda x: dict(x, pt=x.get('point'))
    data = {'stamp': b['stamp'], 'standing': b['standing'], 'deck': b['deck'], 'loop_at': b.get('loop_at', 0),
            'trial': P(b['trial']),
            'changes': [dict(P(c), t=c['title'], s=c['status']) for c in b['changes']],
            'measures': [dict(P(m), t=m['title'], v=m.get('value') or '—', s=m['status']) for m in b['measures']],
            'roles': [dict(P(r), t=r['title']) for r in b['roles']],
            'roles_note': b.get('roles_note', ''), 'roles_cost': b.get('roles_cost', ''),
            'pending': [P(p) for p in b['pending']], 'actions': b['actions']}
    return mod.sample_a(lc.Mode('html', state, {state: data}))

# --- trial: the two weeks on one ward, as a strip of day magnets ------------------------------------------------
def r_trial(b):
    days = b.get('days', 14); ph = b['phases']
    def phase_of(d):
        for j, p in enumerate(ph):
            if p['from'] <= d <= p['to']: return j
        return 0
    sel = b.get('default', 1)
    bands = ''.join('<div class="tr-band tr-p%d" style="grid-column:%d / %d"><b>Days %s</b><span>%s</span></div>' % (
        j % 5, p['from'], p['to'] + 1, ('%d to %d' % (p['from'], p['to'])) if p['to'] > p['from'] else str(p['from']), e(p['title'])) for j, p in enumerate(ph))
    boxes = ''.join('<button type="button" class="tr-day tr-p%d%s" data-d="%d" data-ph="%d" aria-pressed="false" aria-label="Day %d, %s"><i>%d</i></button>' % (
        phase_of(d) % 5, ' tr-wk2' if d == 8 else '', d, phase_of(d), d, e(ph[phase_of(d)]['title']), d) for d in range(1, days + 1))
    det = ''.join('<div class="tr-d tr-p%d" data-ph="%d"%s%s><div class="tr-dh"><span class="tr-dn">Days %s</span><h4>%s</h4></div><p>%s</p>'
                  '<div class="tr-who"><span class="px-label">Who acts</span><b>%s</b></div><div class="tr-rec"><span class="px-label">Recorded</span><ul>%s</ul></div></div>' % (
        j % 5, j, '' if j == phase_of(sel) else ' hidden', pt(p), ('%d to %d' % (p['from'], p['to'])) if p['to'] > p['from'] else str(p['from']), e(p['title']), e(p['what']), e(p['who']),
        ''.join('<li>%s%s</li>' % (MAGNET, e(r)) for r in p['records'])) for j, p in enumerate(ph))
    w = b['ward']
    needs = ''.join('<li>%s<span>%s</span></li>' % (TICK, e(n)) for n in b['needs'])
    return ('<section class="px-tr" data-day="%d" data-days="%d">'
            '<div class="tr-top"><div class="tr-ward tr-ward-%s"%s><span class="px-label">%s</span><b>%s</b><span class="tr-wn">%s</span>%s</div>'
            '<ul class="tr-needs" aria-label="What the trial needs">%s</ul></div>'
            '<div class="tr-board"><div class="tr-bar"><button type="button" class="px-play tr-play"><svg viewBox="0 0 14 14" aria-hidden="true"><path class="pl" d="M3 2l9 5-9 5z"/><path class="pa" d="M4 2v10M10 2v10"/></svg><span>Play the two weeks</span></button>'
            '<span class="tr-now" aria-live="polite">Day <b>%d</b> of %d</span></div>'
            '<div class="tr-weeks"><span>Week 1</span><span>Week 2</span></div>'
            '<div class="tr-grid" style="--n:%d">%s</div><div class="tr-grid tr-days" style="--n:%d">%s</div></div>'
            '<div class="tr-sheet" aria-live="polite">%s</div>%s</section>') % (
        sel, days, w['status'], pt(w), e(w.get('label_head', 'The trial ward')), e(w['label']), e(w['note']),
        '<span class="px-tag px-tag-needed">Needs your choice</span>' if w['status'] == 'needed' else '<span class="px-tag px-tag-ok">Chosen</span>',
        needs, sel, days, days, bands, days, boxes, det, '<p class="px-cond">%s</p>' % e(b['condition']) if b.get('condition') else '')

# --- people: name badges on the board, grouped by what they do -------------------------------------------------
def r_people(b):
    badges = []; sheets = []; k = 0
    for g in b['groups']:
        items = []
        for p in g['people']:
            k += 1
            items.append('<li><button type="button" class="pp-b pp-%s" data-i="%d" data-trial="%s" data-st="%s" aria-pressed="false"%s>%s<span class="pp-av">%s</span>'
                         '<span class="pp-n">%s</span><span class="pp-st">%s</span></button></li>' % (
                p['status'], k, 'y' if p.get('trial') else 'n', p['status'], pt(p), CLIP, e(initials(p['name'])), e(p['name']), STATUS[p['status']]))
            sheets.append('<div class="pp-d" data-i="%d" hidden><div class="pp-dh"><b>%s</b><span class="px-tag pp-t-%s">%s</span>%s</div>'
                          '<dl><div><dt>What changes</dt><dd>%s</dd></div><div><dt>What they gain</dt><dd>%s</dd></div>%s</dl>'
                          '<button type="button" class="px-ask" data-text="%s">Ask Tojo about this</button></div>' % (
                k, e(p['name']), p['status'], STATUS[p['status']], '<span class="px-tag px-tag-trial">In the trial</span>' if p.get('trial') else '<span class="px-tag">After the trial</span>',
                e(p['change']), e(p['gain']), ('<div class="pp-said"><dt>What you told us</dt><dd>%s</dd></div>' % e(p['said'])) if p.get('said') else '',
                e('About %s: ' % p['name'])))
        badges.append('<section class="pp-g"><h4>%s</h4><ul>%s</ul></section>' % (e(g['name']), ''.join(items)))
    n = k; trial = sum(1 for g in b['groups'] for p in g['people'] if p.get('trial')); ask = sum(1 for g in b['groups'] for p in g['people'] if p['status'] != 'agreed')
    dflt = next((i + 1 for i, p in enumerate([p for g in b['groups'] for p in g['people']]) if p['name'] == b.get('default')), 0)
    return ('<section class="px-pp" data-filter="all" data-default="%d">' % dflt + '<div class="px-seg" role="group" aria-label="Show">'
            '<button type="button" data-f="all" aria-pressed="true">Everyone <b>%d</b></button><button type="button" data-f="trial" aria-pressed="false">In the trial <b>%d</b></button>'
            '<button type="button" data-f="ask" aria-pressed="false">Still to ask <b>%d</b></button></div>'
            '<div class="pp-board" style="grid-template-columns:%s">%s</div><div class="pp-sheet" aria-live="polite"><p class="pp-hint">Pick a name badge to see what changes for that person.</p>%s</div>'
            '<p class="pp-rule">%s</p></section>') % (n, trial, ask, ' '.join('minmax(0,%dfr)' % max(1, len(g['people'])) for g in b['groups']), ''.join(badges), ''.join(sheets), e(b['rule']))

# --- swap: each step of the day, moved from today to with the changes -------------------------------------------
def r_swap(b):
    rows = ''.join('<li class="sw-row%s"%s><div class="sw-name"><b>%s</b><span>%s</span></div>'
                   '<button type="button" class="sw-mag" aria-pressed="false" aria-label="%s: move to %s">%s<span class="sw-t sw-today">%s%s</span><span class="sw-t sw-with">%s%s</span>%s</button></li>' % (
        ' sw-flag' if r.get('flag') else '', pt(r), e(r['name']), e(r['who']), e(r['name']), e(b['with_label']), MAGNET,
        e(r['today']), ' <em>%s</em>' % e(r['today_at']) if r.get('today_at') else '', e(r['with']), ' <em>%s</em>' % e(r['with_at']) if r.get('with_at') else '',
        '<b class="px-flag">%s</b>' % e(r['flag']) if r.get('flag') else '') for r in b['rows'])
    return ('<section class="px-sw" data-state="today"><div class="sw-bar"><div class="px-seg" role="group" aria-label="Show">'
            '<button type="button" data-s="today" aria-pressed="true">Today</button><button type="button" data-s="with" aria-pressed="false">%s</button></div>'
            '<span class="sw-count" aria-live="polite"><b>0</b> of %d moved</span></div>'
            '<div class="sw-heads"><span></span><span>Today</span><span>%s</span></div><ol class="sw-rows">%s</ol>'
            '<p class="sw-keep">%s</p>%s</section>') % (
        e(b['with_label']), len(b['rows']), e(b['with_label']), rows, e(b['keeps']), '<p class="px-cond">%s</p>' % e(b['condition']) if b.get('condition') else '')

# --- seats: the roles as chairs, their triggers as lamps, the sizing check as a day strip --------------------------
LAMP = {'met': 'Met', 'not': 'Not met', 'unknown': 'Not known yet'}
def r_seats(b):
    roles = []
    for i, r in enumerate(b['roles']):
        trig = ''.join('<li class="st-lamp st-%s"%s%s%s><i></i><span>%s</span><span class="st-lv"><b>%s</b>%s</span></li>' % (
            t['state'], ' data-above="%g"' % t['above'] if t.get('above') is not None else '', ' data-src="%s"' % t['source'], pt(t), e(t['label']),
            e(t.get('value') or LAMP[t['state']]), src(t['source'])) for t in r.get('triggers', []))
        cost = lakh(r['cost_low'], r['cost_high']) + (' a year each' if r.get('each') else ' a year')
        roles.append('<section class="st-role st-%s%s" data-i="%d" data-seats="%d" data-lo="%g" data-hi="%g" data-each="%s"%s%s>'
                     '<div class="st-chairs">%s</div><div class="st-body"><div class="st-h"><h4>%s</h4><span class="st-state">%s</span></div><p>%s</p>'
                     '<span class="st-cost">%s</span>%s%s</div></section>' % (
            r['state'], ' st-sized' if r.get('sized') else '', i, r['seats'], r['cost_low'], r['cost_high'], 'y' if r.get('each') else 'n', pt(r),
            ' data-rule="any"' if r.get('triggers') else '',
            ''.join(SEAT(False) for _ in range(r['seats'])), e(r['name']), {'needed': 'Needed now', 'optional': 'Optional for now', 'check': 'Needs your numbers'}[r['state']], e(r['does']), e(cost),
            ('<ul class="st-lamps"><li class="st-rule">%s</li>%s</ul>' % (e(r.get('rule', 'Any one is enough')), trig)) if trig else '',
            '<p class="st-note">%s</p>' % e(r['note']) if r.get('note') else ''))
    top = ''
    if b.get('reports_to'):
        top = '<div class="st-top"><div class="st-boss"%s>%s<b>%s</b><span>%s</span></div></div>' % (pt(b['reports_to']), SEAT(True, 'st-boss-s'), e(b['reports_to']['name']), e(b['reports_to']['does']))
    between = ''
    if b.get('between'):
        between = ('<section class="st-btw"><div class="px-label">%s</div><ol>%s</ol><div class="st-bd" aria-live="polite">%s</div></section>') % (
            e(b['between_label']), ''.join('<li><button type="button" class="st-link st-l-%s" data-k="%d" aria-pressed="%s"%s><span>%d</span>%s</button></li>' % (
                x['status'], k, 'true' if k == 0 else 'false', pt(x), k + 1, e(x['title'])) for k, x in enumerate(b['between'])),
            ''.join('<p data-k="%d"%s>%s <span class="px-tag px-tag-%s">%s</span></p>' % (k, '' if k == 0 else ' hidden', e(x['detail']),
                    'needed' if x['status'] == 'needed' else 'ok', {'agreed': 'Agreed', 'new': 'New', 'needed': 'Needs your answer'}[x['status']]) for k, x in enumerate(b['between'])))
    size = ''
    z = b.get('sizing')
    if z:
        wins = ''.join('<div class="sz-win" style="--a:%.2f%%;--b:%.2f%%"><b>%s</b><span>%s</span></div>' % (
            100.0 * (w['from'] - z['start']) / (z['end'] - z['start']), 100.0 * (w['to'] - z['start']) / (z['end'] - z['start']), e(w['label']), e(w['clock'])) for w in z['windows'])
        ticks = ''.join('<span style="left:%.2f%%">%s</span>' % (100.0 * (h - z['start']) / (z['end'] - z['start']), e(lc_clock(h))) for h in range(z['start'], z['end'] + 1, 3))
        size = ('<section class="px-sz"%s data-mode="busy" data-per="%g" data-lo="%d" data-hi="%d" data-wins=\'%s\' data-start="%d" data-end="%d">'
                '<div class="sz-bar"><div class="px-seg" role="group" aria-label="Size by"><button type="button" data-m="flat" aria-pressed="false">%s</button><button type="button" data-m="busy" aria-pressed="true">%s</button></div>'
                '<label class="sz-sl"><span>%s <b class="sz-n">%d</b></span><input type="range" class="sz-range" min="%d" max="%d" step="1" value="%d" aria-label="%s"></label></div>'
                '<div class="sz-day"><div class="sz-ticks">%s</div><div class="sz-wins">%s</div><div class="sz-people"></div></div>'
                '<div class="sz-read"><div><span class="px-label">%s</span><b class="sz-count"></b></div><p class="sz-why" aria-live="polite"></p></div>'
                '<div class="sz-total"><span class="px-label">%s</span><b class="sz-cost"></b></div></section>') % (
            pt(z), z['per_person'], z['yours_low'], z['yours_high'], json.dumps([[w['from'], w['to'], w['label']] for w in z['windows']]), z['start'], z['end'],
            e(z['flat_label']), e(z['busy_label']), e(z['slider_label']), z['default'], z['min'], z['max'], z['default'], e(z['slider_label']), ticks, wins,
            e(z['count_label']), e(z['total_label']))
    return ('<section class="px-st"%s data-flat="%s" data-busy="%s" data-recheck="%s">%s<div class="st-roles" style="--r:%d">%s</div>%s%s%s</section>') % (
        ' data-sized="y"' if z else '', e(z['flat_text']) if z else '', e(z['busy_text']) if z else '', e(z['recheck_text']) if z else '',
        top, len(b['roles']), ''.join(roles), between, size, '<p class="st-others">%s</p>' % e(b['others']) if b.get('others') else '')

def lc_clock(h):
    h = h % 24
    if h == 0: return 'midnight'
    if h == 12: return 'noon'
    return '%d %s' % (h % 12 or 12, 'AM' if h < 12 else 'PM')

# --- readouts: the measures as instrument windows ------------------------------------------------------------------
def r_readouts(b):
    cells = ''.join('<li><button type="button" class="rd rd-%s" data-i="%d" data-when="%s" aria-pressed="%s"%s><span class="rd-n">%s</span>'
                    '<span class="rd-w"><span class="rd-v rd-now">%s</span><span class="rd-v rd-end">%s</span></span>%s</button></li>' % (
        m['state'], i, m['when'], 'true' if i == b.get('default', 0) else 'false', pt(m), e(m['name']),
        e(m['value']) if m['state'] == 'confirmed' else 'No number yet', 'Read on day 14' if m['when'] == 'trial' else 'Read after', src(m['source'])) for i, m in enumerate(b['measures']))
    det = ''.join('<div class="rd-d" data-i="%d"%s><b>%s</b><dl><div><dt>How it is measured</dt><dd>%s</dd></div><div><dt>Who records it</dt><dd>%s</dd></div><div><dt>Goal</dt><dd>%s</dd></div></dl></div>' % (
        i, '' if i == b.get('default', 0) else ' hidden', e(m['name']), e(m['how']), e(m['who']), e(m['goal'])) for i, m in enumerate(b['measures']))
    ms = b['measures']
    return ('<section class="px-rd" data-filter="all" data-view="now"><div class="rd-bar"><div class="px-seg" role="group" aria-label="Show">'
            '<button type="button" data-f="all" aria-pressed="true">All <b>%d</b></button><button type="button" data-f="trial" aria-pressed="false">In the trial <b>%d</b></button>'
            '<button type="button" data-f="later" aria-pressed="false">After the trial <b>%d</b></button></div>'
            '<div class="px-seg" role="group" aria-label="Read"><button type="button" data-v="now" aria-pressed="true">Starting number</button><button type="button" data-v="end" aria-pressed="false">After the trial</button></div></div>'
            '<div class="rd-key"><span><i class="k-c"></i>%d with your starting number</span><span><i class="k-n"></i>%d new, no number made up</span></div>'
            '<ol class="rd-grid">%s</ol><div class="rd-sheet" aria-live="polite">%s</div>%s</section>') % (
        len(ms), sum(1 for m in ms if m['when'] == 'trial'), sum(1 for m in ms if m['when'] == 'later'),
        sum(1 for m in ms if m['state'] == 'confirmed'), sum(1 for m in ms if m['state'] != 'confirmed'), cells, det,
        '<p class="px-cond">%s</p>' % e(b['condition']) if b.get('condition') else '')

# --- loop: plan, try on one ward, measure, adjust, spread -------------------------------------------------------------
def r_loop(b):
    st = b['steps']; n = len(st); cx, cy, r = 160, 160, 118
    arcs = []; nodes = []
    for i in range(n):
        a1 = math.radians(-90 + i * 360.0 / n + 13); a2 = math.radians(-90 + (i + 1) * 360.0 / n - 13)
        arcs.append('<path class="lp-arc" data-a="%d" d="M%.1f %.1f A%d %d 0 0 1 %.1f %.1f" marker-end="url(#px-ah)"/>' % (
            i, cx + r * math.cos(a1), cy + r * math.sin(a1), r, r, cx + r * math.cos(a2), cy + r * math.sin(a2)))
        a = math.radians(-90 + i * 360.0 / n)
        nodes.append('<button type="button" class="lp-node" data-k="%d" style="left:%.2f%%;top:%.2f%%" aria-pressed="false"%s><b>%d</b><span>%s</span></button>' % (
            i, 100 * (cx + r * math.cos(a)) / 320, 100 * (cy + r * math.sin(a)) / 320, pt(st[i]), i + 1, e(st[i]['name'])))
    g = b['gate']
    sheets = ''.join('<div class="lp-d" data-k="%d" hidden><div class="lp-dh"><span>Step %d</span><h4>%s</h4></div><p>%s</p><div class="lp-who"><span class="px-label">Who</span><b>%s</b></div>%s</div>' % (
        i, i + 1, e(s['name']), e(s['what']), e(s['who']),
        ('<div class="lp-gate"><b>%s</b><div><button type="button" class="px-pill lp-yes">%s</button><button type="button" class="px-pill lp-no">%s</button></div></div>' % (e(g['question']), e(g['yes']), e(g['no']))) if i == g['at'] else '') for i, s in enumerate(st))
    return ('<section class="px-lp" data-at="%d" data-gate="%d" data-yes="%d" data-no="%d" data-retry="%d"><div class="lp-wheel"><svg viewBox="0 0 320 320" aria-hidden="true"><defs>'
            '<marker id="px-ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="lp-ahp"/></marker></defs>'
            '<circle class="lp-ring" cx="160" cy="160" r="118"/>%s</svg>%s<div class="lp-mid"><span class="lp-round">Round <b>1</b></span><b class="lp-now"></b><span class="lp-sub">%s</span></div></div>'
            '<div class="lp-side"><div class="lp-bar"><button type="button" class="px-pill lp-prev">← Back</button><button type="button" class="px-pill px-pill-on lp-next">Next step →</button></div>'
            '<div class="lp-sheet" aria-live="polite">%s</div></div></section>') % (
        b.get('at', 0), g['at'], g['yes_to'], g['no_to'], g['retry_to'], ''.join(arcs), ''.join(nodes), e(b['sub']), sheets)

RENDER = {'heading': r_heading, 'trial': r_trial, 'people': r_people, 'swap': r_swap, 'seats': r_seats, 'readouts': r_readouts, 'loop': r_loop}

# ---------------------------------------------------------------------------------------------- simple English
SIMPLE = {'via': 'through', 'ensure': 'make sure', 'prior to': 'before', 'additional': 'more', 'approximately': 'about', 'utilise': 'use',
          'numerous': 'many', 'obtain': 'get', 'require': 'need', 'requires': 'needs', 'regarding': 'about', 'assist': 'help', 'initiate': 'start',
          'component': 'part', 'components': 'parts', 'implement': 'put in place', 'implementation': 'putting it in place', 'optimal': 'best',
          'streamline': 'simplify', 'visibility': 'a clear view', 'alignment': 'agreement', 'enable': 'let', 'enables': 'lets', 'key stakeholders': 'people involved',
          'stakeholder': 'person involved', 'stakeholders': 'people involved', 'kpi': 'measure', 'kpis': 'measures', 'metric': 'measure', 'metrics': 'measures',
          'baseline': 'starting number', 'headcount': 'number of staff', 'tat': 'time taken', 'onboard': 'bring in', 'onboarding': 'bringing in',
          'serialised': 'one after the other', 'decouple': 'separate', 'decoupling': 'separating', 'workflow': 'order of work', 'pilot': 'trial',
          'utilisation': 'use', 'throughput': 'how many get through', 'fte': 'full-time person', 'sla': 'agreed time', 'escalate': 'pass up'}
SKIP_KEYS = {'id', 'type', 'register', 'tool', 'tab', 'context', 'source', 'status', 'state', 'kind', 'user_tag', 'when', 'from', 'to', 'at', 'yes_to', 'no_to'}
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
        if m.get('tab') not in ('Solutions', 'Automations', 'Diagnosis'): out.append('chat.moves[%d].tab: Solutions, Automations or Diagnosis' % j)
    return out

def block_checks(blocks):
    errs = []
    for i, b in enumerate(blocks):
        typ = b.get('type'); P = 'canvas.blocks[%d](%s)' % (i, typ)
        if typ == 'trial':
            days = b.get('days', 14); cover = []
            for j, p in enumerate(b.get('phases', [])):
                if not (1 <= p.get('from', 0) <= p.get('to', 0) <= days): errs.append('%s.phases[%d]: from and to must sit inside days 1 to %d' % (P, j, days))
                cover += list(range(p.get('from', 0), p.get('to', -1) + 1))
            if sorted(cover) != list(range(1, days + 1)): errs.append('%s.phases: every day from 1 to %d is in exactly one phase' % (P, days))
            if not (1 <= b.get('default', 1) <= days): errs.append('%s.default: a day from 1 to %d' % (P, days))
        if typ == 'seats':
            z = b.get('sizing')
            if z:
                if sum(1 for r in b.get('roles', []) if r.get('sized')) != 1: errs.append('%s: with sizing, exactly one role is "sized"' % P)
                if not (z.get('min', 0) <= z.get('default', 0) <= z.get('max', 0)): errs.append('%s.sizing.default: between min and max' % P)
                if not (z.get('min', 0) <= z.get('yours_low', 0) <= z.get('yours_high', 0) <= z.get('max', 0)): errs.append('%s.sizing.yours_low/high: your range sits inside min to max' % P)
                for j, w in enumerate(z.get('windows', [])):
                    if not (z['start'] <= w['from'] < w['to'] <= z['end']): errs.append('%s.sizing.windows[%d]: inside the day strip' % (P, j))
            for j, r in enumerate(b.get('roles', [])):
                if r.get('cost_low', 0) > r.get('cost_high', 0): errs.append('%s.roles[%d]: cost_low is above cost_high' % (P, j))
                ts = r.get('triggers', [])
                met = any(t.get('state') == 'met' for t in ts)
                if ts and met and r.get('state') != 'needed': errs.append('%s.roles[%d]: a trigger is met, so state is "needed"' % (P, j))
                if ts and not met and r.get('state') == 'needed': errs.append('%s.roles[%d]: no trigger is met, so state cannot be "needed"' % (P, j))
                for k, t in enumerate(ts):
                    if t.get('state') == 'unknown' and t.get('source') != 'needed': errs.append('%s.roles[%d].triggers[%d]: an unknown trigger has source "needed"' % (P, j, k))
                    if t.get('above') is not None and not z: errs.append('%s.roles[%d].triggers[%d].above: only with sizing (the slider drives it)' % (P, j, k))
            if b.get('between') and not b.get('between_label'): errs.append('%s.between_label: required with between' % P)
        if typ == 'readouts':
            for j, m in enumerate(b.get('measures', [])):
                if m.get('state') == 'confirmed' and not m.get('value'): errs.append('%s.measures[%d]: a confirmed measure has its value' % (P, j))
                if m.get('state') == 'new' and m.get('value'): errs.append('%s.measures[%d]: a new measure has no value yet. Never make one up.' % (P, j))
                if m.get('state') == 'new' and m.get('source') != 'new': errs.append('%s.measures[%d].source: "new" for a new measure' % (P, j))
                if m.get('state') == 'confirmed' and m.get('source') == 'new': errs.append('%s.measures[%d].source: say where the number came from' % (P, j))
        if typ == 'loop':
            n = len(b.get('steps', [])); g = b.get('gate', {})
            for k in ('at', 'yes_to', 'no_to', 'retry_to'):
                if not (0 <= g.get(k, -1) < n): errs.append('%s.gate.%s: a step index from 0 to %d' % (P, k, n - 1))
            if not (0 <= b.get('at', 0) < n): errs.append('%s.at: a step index' % P)
        if typ == 'people':
            names = [p.get('name') for g in b.get('groups', []) for p in g.get('people', [])]
            if len(names) != len(set(names)): errs.append('%s: each person or team appears once' % P)
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
            for j, m in enumerate(blocks[0].get('measures', [])):
                if m.get('status') == 'new' and m.get('value'): errs.append('canvas.blocks[0](landing).measures[%d]: a new measure has no value yet' % j)
                if m.get('status') == 'confirmed' and not m.get('value'): errs.append('canvas.blocks[0](landing).measures[%d]: a confirmed measure has its value' % j)
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
    if spec.get('turn', {}).get('tab', TAB) != TAB: errs.append('turn.tab: this generator only draws Processes turns')
    errs += ['simple English: ' + x for x in simple_check(spec)] + moves_check(spec)
    return errs, warns

# ---------------------------------------------------------------------------------------------- pages
def render_canvas(spec, reg=None):
    blocks = spec['canvas']['blocks']
    if spec['turn']['type'] == 'landing':
        return r_landing(blocks[0], spec['canvas'].get('state', 'filled'))
    inner = ''.join(RENDER[b['type']](b) for b in blocks)
    return '<div class="px-host"><div class="px" data-turn="%s" data-generator="%s"><div class="px-stack">%s</div></div></div>' % (e(spec['turn']['id']), GEN, inner)

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
  Q(document,'.sh-pr,.sh-opt,.lp-act,.px-ask').forEach(function(b){b.addEventListener('click',function(){say(b.getAttribute('data-text'));});});
  Q(document,'.lp-refresh').forEach(function(b){b.addEventListener('click',function(){
    var s=b.closest('.lp-stamp');s.querySelector('.lp-stamp-at').textContent=b.getAttribute('data-fresh');
    s.querySelector('.lp-stamp-since').textContent=b.getAttribute('data-fresh-since');b.classList.add('is-done');});});
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  function seg(root,attr,fn){Q(root,'.px-seg button['+attr+']').forEach(function(b){b.addEventListener('click',function(){
    Q(b.parentNode,'button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});fn(b.getAttribute(attr));});});}
  // trial: pick a day, or play the two weeks; the phase sheet follows the day
  Q(document,'.px-tr').forEach(function(tr){
    var days=+tr.getAttribute('data-days'),timer=null,play=tr.querySelector('.tr-play');
    function day(d){tr.setAttribute('data-day',d);var ph=null;
      Q(tr,'.tr-day').forEach(function(b){var k=+b.getAttribute('data-d');b.setAttribute('aria-pressed',k===d?'true':'false');b.classList.toggle('is-past',k<d);if(k===d)ph=b.getAttribute('data-ph');});
      Q(tr,'.tr-d').forEach(function(x){x.hidden=x.getAttribute('data-ph')!==ph;});
      Q(tr,'.tr-band').forEach(function(x,i){x.classList.toggle('is-on',String(i)===ph);});
      tr.querySelector('.tr-now b').textContent=d;}
    function stop(){if(timer){clearInterval(timer);timer=null;}play.classList.remove('is-on');play.querySelector('span').textContent='Play the two weeks';}
    Q(tr,'.tr-day').forEach(function(b){b.addEventListener('click',function(){stop();day(+b.getAttribute('data-d'));});});
    play.addEventListener('click',function(){if(timer){stop();return;}var d=+tr.getAttribute('data-day');if(d>=days)d=0;play.classList.add('is-on');play.querySelector('span').textContent='Pause';
      if(reduce){day(days);stop();return;}timer=setInterval(function(){d++;if(d>days){stop();return;}day(d);},650);});
    day(+tr.getAttribute('data-day'));});
  // people: filter the badges; pick one for its sheet
  Q(document,'.px-pp').forEach(function(pp){
    function pick(i){Q(pp,'.pp-b').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-i')===i?'true':'false');});
      Q(pp,'.pp-d').forEach(function(d){d.hidden=d.getAttribute('data-i')!==i;});pp.querySelector('.pp-hint').hidden=!!i;}
    seg(pp,'data-f',function(f){pp.setAttribute('data-filter',f);Q(pp,'.pp-b').forEach(function(b){
      var on=f==='all'||(f==='trial'&&b.getAttribute('data-trial')==='y')||(f==='ask'&&b.getAttribute('data-st')!=='agreed');
      b.classList.toggle('is-dim',!on);b.disabled=!on;});
      var cur=pp.querySelector('.pp-b[aria-pressed=true]');if(cur&&cur.disabled)pick('');});
    Q(pp,'.pp-b').forEach(function(b){b.addEventListener('click',function(){pick(b.getAttribute('aria-pressed')==='true'?'':b.getAttribute('data-i'));});});
    var d0=pp.getAttribute('data-default');if(d0&&d0!=='0')pick(d0);});
  // swap: move each step across, one at a time or all together
  Q(document,'.px-sw').forEach(function(sw){
    var rows=Q(sw,'.sw-row'),n=rows.length;
    function upd(){var k=rows.filter(function(r){return r.classList.contains('is-moved');}).length;sw.querySelector('.sw-count b').textContent=k;
      var s=k===n?'with':(k===0?'today':'');Q(sw,'.px-seg button').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-s')===s?'true':'false');});
      sw.setAttribute('data-state',s||'mixed');}
    rows.forEach(function(r){r.querySelector('.sw-mag').addEventListener('click',function(){r.classList.toggle('is-moved');
      r.querySelector('.sw-mag').setAttribute('aria-pressed',r.classList.contains('is-moved')?'true':'false');upd();});});
    seg(sw,'data-s',function(s){rows.forEach(function(r,i){var go=s==='with';
      setTimeout(function(){r.classList.toggle('is-moved',go);r.querySelector('.sw-mag').setAttribute('aria-pressed',go?'true':'false');upd();},reduce?0:i*90);});});
    upd();});
  // seats: the slider drives the lamps, the manager's seat and the sizing check
  Q(document,'.px-st').forEach(function(st){
    var z=st.querySelector('.px-sz');
    function fmt(v){return (Math.round(v*10)/10).toString();}
    function range(lo,hi){return lo===hi?'₹'+fmt(lo)+' lakh':'₹'+fmt(lo)+' to '+fmt(hi)+' lakh';}
    function upd(){
      var n=z?+z.querySelector('.sz-range').value:0,mode=z?z.getAttribute('data-mode'):'',lo=0,hi=0;
      Q(st,'.st-role').forEach(function(r){
        Q(r,'.st-lamp[data-above]').forEach(function(l){var met=n>+l.getAttribute('data-above');l.classList.toggle('st-met',met);l.classList.toggle('st-not',!met);
          l.querySelector('b').textContent=n+' a day';});
        var lamps=Q(r,'.st-lamp');
        if(lamps.length){var any=lamps.some(function(l){return l.classList.contains('st-met');}),unk=lamps.some(function(l){return l.classList.contains('st-unknown');});
          r.classList.remove('st-needed','st-optional','st-check');r.classList.add(any?'st-needed':(unk?'st-check':'st-optional'));
          r.querySelector('.st-state').textContent=any?'Needed now':(unk?'Needs your numbers':'Optional for now');}
        var seats=+r.getAttribute('data-seats');
        if(z&&r.classList.contains('st-sized')){var per=+z.getAttribute('data-per'),wins=JSON.parse(z.getAttribute('data-wins'));
          seats=mode==='flat'?Math.max(1,Math.ceil(n/per)):wins.length;
          var ch=r.querySelector('.st-chairs'),have=ch.children.length;
          while(have<seats){ch.insertAdjacentHTML('beforeend',ch.firstElementChild.outerHTML);have++;}while(have>seats){ch.removeChild(ch.lastElementChild);have--;}}
        var need=!r.classList.contains('st-optional')||!Q(r,'.st-lamp').length;
        Q(r,'.px-seat').forEach(function(s){s.classList.toggle('on',need);});
        if(need&&!r.classList.contains('st-check')){var k=r.getAttribute('data-each')==='y'?seats:1;lo+=k*+r.getAttribute('data-lo');hi+=k*+r.getAttribute('data-hi');}
        r.setAttribute('data-now',seats);});
      if(!z)return;
      var per=+z.getAttribute('data-per'),wins=JSON.parse(z.getAttribute('data-wins')),a=+z.getAttribute('data-start'),b=+z.getAttribute('data-end');
      var ylo=+z.getAttribute('data-lo'),yhi=+z.getAttribute('data-hi'),inr=n>=ylo&&n<=yhi;
      z.querySelector('.sz-n').textContent=n;
      var ppl=z.querySelector('.sz-people'),html='';
      if(mode==='flat'){var k=Math.max(1,Math.ceil(n/per));for(var i=0;i<k;i++)html+='<div class="sz-p sz-flat"><span style="--a:0%;--b:100%">Person '+(i+1)+', all day</span></div>';
        z.querySelector('.sz-count').textContent=k+(k===1?' person':' people');z.querySelector('.sz-why').textContent=st.getAttribute('data-flat').replace('{n}',n).replace('{k}',k);}
      else{html='<div class="sz-p">';wins.forEach(function(w,i){html+='<span style="--a:'+(100*(w[0]-a)/(b-a))+'%;--b:'+(100*(w[1]-a)/(b-a))+'%">Person '+(i+1)+'</span>';});html+='</div>';
        z.querySelector('.sz-count').textContent=wins.length+' people';z.querySelector('.sz-why').textContent=inr?st.getAttribute('data-busy'):st.getAttribute('data-recheck');}
      z.classList.toggle('is-recheck',mode==='busy'&&!inr);ppl.innerHTML=html;
      z.querySelector('.sz-cost').textContent=range(lo,hi)+' a year';}
    if(z){z.querySelector('.sz-range').addEventListener('input',upd);seg(z,'data-m',function(m){z.setAttribute('data-mode',m);upd();});}
    Q(st,'.st-link').forEach(function(l){l.addEventListener('click',function(){var k=l.getAttribute('data-k');
      Q(st,'.st-link').forEach(function(x){x.setAttribute('aria-pressed',x===l?'true':'false');});Q(st,'.st-bd p').forEach(function(p){p.hidden=p.getAttribute('data-k')!==k;});});});
    upd();});
  // readouts: filter, pick one, flip between the starting number and the end of the trial
  Q(document,'.px-rd').forEach(function(rd){
    function pick(i){Q(rd,'.rd').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-i')===i?'true':'false');});Q(rd,'.rd-d').forEach(function(d){d.hidden=d.getAttribute('data-i')!==i;});}
    seg(rd,'data-f',function(f){rd.setAttribute('data-filter',f);Q(rd,'.rd').forEach(function(b){var on=f==='all'||b.getAttribute('data-when')===f;b.classList.toggle('is-dim',!on);b.disabled=!on;});
      var cur=rd.querySelector('.rd[aria-pressed=true]');if(!cur||cur.disabled){var f1=rd.querySelector('.rd:not([disabled])');if(f1)pick(f1.getAttribute('data-i'));}});
    seg(rd,'data-v',function(v){rd.setAttribute('data-view',v);});
    Q(rd,'.rd').forEach(function(b){b.addEventListener('click',function(){pick(b.getAttribute('data-i'));});});});
  // loop: step round; at the gate the answer sends the marker on or back
  Q(document,'.px-lp').forEach(function(lp){
    var nodes=Q(lp,'.lp-node'),n=nodes.length,round=1,gate=+lp.getAttribute('data-gate');
    function go(k,back){k=(k+n)%n;lp.setAttribute('data-at',k);
      nodes.forEach(function(x,i){x.setAttribute('aria-pressed',i===k?'true':'false');x.classList.toggle('is-done',i<k);});
      Q(lp,'.lp-arc').forEach(function(a,i){a.classList.toggle('is-done',i<k);});
      Q(lp,'.lp-d').forEach(function(d){d.hidden=+d.getAttribute('data-k')!==k;});
      lp.querySelector('.lp-now').textContent=nodes[k].querySelector('span').textContent;lp.querySelector('.lp-round b').textContent=round;
      lp.querySelector('.lp-prev').disabled=k===0&&round===1;lp.querySelector('.lp-next').hidden=k===gate;
      lp.querySelector('.lp-next').textContent=k===n-1?'Next ward →':(k===+lp.getAttribute('data-no')?'Try again →':'Next step →');
      lp.classList.remove('is-back');if(back){void lp.offsetWidth;lp.classList.add('is-back');}}
    nodes.forEach(function(x,i){x.addEventListener('click',function(){go(i);});});
    lp.querySelector('.lp-next').addEventListener('click',function(){var k=+lp.getAttribute('data-at');if(k===n-1){round=1;go(0);return;}
      if(k===+lp.getAttribute('data-no')){go(+lp.getAttribute('data-retry'),true);return;}go(k+1);});
    lp.querySelector('.lp-prev').addEventListener('click',function(){go(+lp.getAttribute('data-at')-1);});
    Q(lp,'.lp-yes').forEach(function(b){b.addEventListener('click',function(){go(+lp.getAttribute('data-yes'));});});
    Q(lp,'.lp-no').forEach(function(b){b.addEventListener('click',function(){round++;go(+lp.getAttribute('data-no'),true);});});
    go(+lp.getAttribute('data-at'));});
  function tell(){try{parent.postMessage({tojoHeight:document.documentElement.scrollHeight,tojoId:document.documentElement.getAttribute('data-frame')},'*');}catch(e){}}
  window.addEventListener('load',tell);setTimeout(tell,900);
})();
'''

def css_all():
    mod = _load_module('pr_landing', os.path.join(HERE, 'landing.py'))
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
    out = ['# Processes canvas blocks — catalogue (registry v%d, %s)\n' % (reg['registry_version'], reg['updated']),
           'Use only these blocks in a Processes turn. First block is always `heading` (except a `landing` turn, whose only block is `landing`). At most %d blocks after the heading.\n' % reg['budget']['max_blocks']]
    for b in reg['blocks']:
        out.append('## `%s` (%s · scope %s)\n%s\n- Use when: %s\n- Avoid when: %s\n- Slots: %s\n%s' % (
            b['id'], b['status'], b.get('scope', 'all'), b['purpose'], '; '.join(b['use_when']), '; '.join(b['avoid_when']),
            json.dumps(slot_summary(b['slots']), ensure_ascii=False), ('- Interaction: %s\n' % b['interaction']) if b.get('interaction') else ''))
    out.append('## Recipes by turn type\n' + '\n'.join('- `%s`: %s' % (k, ', '.join(v)) for k, v in reg['turn_recipes'].items()))
    return '\n'.join(out)

def prompt(reg):
    tpl = open(os.path.join(ROOT, 'prompts', 'tojo-api-system-prompt.md'), encoding='utf-8').read()
    rules = open(os.path.join(ROOT, 'rules', '06-html-response-rules.md'), encoding='utf-8').read()
    extra = ('\n\n# This turn is in Processes\nSet `turn.tab` to "Processes". Use the Processes catalogue below. '
             'Processes takes the working detail of the people and the work: who must agree and what changes for each, the changes to the order of work, '
             'new roles and how they are sized, the measures we watch, and the trial on one ward. A `landing` turn has one block, `landing`. '
             'Never make up a starting number for a measure. A measure with no number yet is "new".\n\n')
    return tpl.replace('{{RULES_06}}', rules).replace('{{CATALOG}}', extra + catalog(reg))

# ---------------------------------------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate'); v.add_argument('spec')
    r = sub.add_parser('render'); r.add_argument('spec'); r.add_argument('--view', default='desktop', choices=['desktop', 'mobile']); r.add_argument('-o', '--out')
    sm = sub.add_parser('sample'); sm.add_argument('spec'); sm.add_argument('-o', '--out')
    b = sub.add_parser('build'); b.add_argument('dir', nargs='?', default=os.path.join(ROOT, 'examples', 'processes')); b.add_argument('-o', '--out', default=os.path.join(ROOT, 'out', 'processes'))
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
        out = render_page(spec, a.view, reg) if a.cmd == 'render' else review_page.page('%s · Processes' % spec['turn']['id'], 'Processes · ' + spec['turn']['id'],
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
                '%s · Processes' % spec['turn']['id'], 'Processes · ' + spec['turn']['id'], 'Discharge Process · generated by %s' % GEN, [rt], book=False))
        args = ('Tojo Processes Turns', 'Processes · every turn', 'Discharge Process, 250-bed hospital, Bhubaneswar · generated by %s · %d turns' % (GEN, len(turns)), turns)
        open(os.path.join(a.out, 'processes-tab.html'), 'w', encoding='utf-8').write(review_page.page(*args))
        open(os.path.join(a.out, 'processes-tab.artifact.html'), 'w', encoding='utf-8').write(review_page.page(*args, fragment=True))
        print('wrote %d turn files to %s and the book processes-tab.html' % (len(turns), tdir))
        sys.exit(1 if bad else 0)
    if a.cmd == 'prompt': print(prompt(reg))
    if a.cmd == 'catalog': print(catalog(reg))

if __name__ == '__main__':
    main()
