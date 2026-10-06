"""
dp_pr_blocks — the Processes drawings for Discharge Process (drafts, 5 Oct 2026).

The Processes motifs of the block library (Common Elements/processes-html-generator: the ward board, the magnets, the
name badges, the chairs, the instrument windows, the trial strip and the loop, 07 §1.5) redrawn with the common tool layer:
the first item raised with its sheet open, on a phone each sheet right under its item and every pickable item stacked,
entries typed in the drawing added to the chat message. Two new ones join them: the timesheet (a day's clock times,
typed straight into the drawing, then redrawn filled) and the night lanes (each job on one clock from 6 PM to the next
afternoon, today against with the changes).

  heading       the library heading, with a small ward board: which column of the board this turn is about
  swap          each step of the day, its magnet moved from today to with the changes            (dp-pr-10)
  trial         the two weeks on one ward: the day strip you can play, the phases as pickable bands (dp-pr-08)
  badges        name badges on the board, grouped by what each person does, filtered             (dp-pr-09)
  seats         the roles as chairs, their triggers as lamps, the busy-hours check as a day strip   (dp-pr-11)
  readouts      the measures as instrument windows, starting number or after the trial         (dp-pr-13)
  loop          plan, try, measure, adjust, spread: a wheel with a yes-or-no gate              (dp-pr-14)
  timesheet     one normal day's times: blank to type in, or filled with the gaps between       (dp-pr-06, 07)
  night-lanes   each job on one clock from the evening round to the next afternoon             (dp-pr-01)

All classes carry their own prefix (xh, xs, xt, xb, xc, xr, xl, xm, xn) so they never meet the Solutions drawings that
also draw in this place. Colours come from the canvas variables (the ward board: heather, aubergine, plum).
register(G) is called by dp_processes_html with the generator's helpers (e, L, B = bm_so_blocks).
"""
import json, math

G = {}
def e(s): return G['e'](s)
def pt(o): return ' data-tj-point="%d"' % int(o['point']) if isinstance(o, dict) and o.get('point') is not None else ''
def pick(grp, key, first, cls=''): return G['L'].pick_attrs(grp, key, first, cls)
def sheet(s, grp, first, where): return G['B'].sheet(s, grp, first, where)
def desk(boxes): return '<div class="bx-desk-wrap">%s</div>' % ''.join(boxes)
def hint(t): return '<p class="tl-hint so-hint"><span class="xh-mag-s" aria-hidden="true">%s</span>%s</p>' % (MAGNET, e(t))
def cond(t): return '<p class="sx-cond so-cap">%s</p>' % e(t) if t else ''
def lab(t): return '<div class="sx-label">%s</div>' % e(t) if t else ''

SRC = {'yours': 'Your number', 'derived': 'Worked out from yours', 'estimate': 'Tojo’s guess', 'illustrative': 'Example only', 'target': 'Goal', 'needed': 'Need from you', 'new': 'New, no starting number'}
def src(s): return '<span class="xh-src xh-src-%s">%s</span>' % (e(s), e(SRC[s]))

MAGNET = '<svg class="xh-mag" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8"/><circle class="xh-mag-s" cx="7.5" cy="7.5" r="2.4"/></svg>'
def SEAT(on, cls=''):
    return ('<svg viewBox="0 0 40 44" class="xh-seat %s%s" aria-hidden="true"><path class="xh-seat-b" d="M10 4h20a3 3 0 013 3v15H7V7a3 3 0 013-3z"/>'
            '<path class="xh-seat-c" d="M4 22h32v7H4z"/><path class="xh-seat-l" d="M9 29v12M31 29v12"/></svg>') % ('on ' if on else '', cls)
CLIP = '<svg class="xb-clip" viewBox="0 0 30 16" aria-hidden="true"><path d="M8 0v6h14V0"/><rect x="5" y="5" width="20" height="9" rx="3"/></svg>'
TICK = '<svg class="xh-tick" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7"/></svg>'
PLAY = '<svg viewBox="0 0 14 14" aria-hidden="true"><path class="pl" d="M3 2l9 5-9 5z"/><path class="pa" d="M4 2v10M10 2v10"/></svg>'

def register(helpers):
    G.update(helpers)
    return {'heading': r_heading, 'swap': r_swap, 'trial': r_trial, 'badges': r_badges, 'seats': r_seats, 'readouts': r_readouts,
            'loop': r_loop, 'timesheet': r_timesheet, 'night-lanes': r_lanes}

def initials(name):
    w = [x for x in name.replace('/', ' ').split() if x and x[0].isalpha() and x.lower() not in ('and', 'the', 'of')]
    return ''.join(x[0].upper() for x in w[:2]) or name[:1].upper()

# ------------------------------------------------------------------------------------------ heading, with the ward board
COLS = ['Changes', 'People', 'Roles', 'Measures', 'The trial']
def r_heading(b, ctx):
    h = ('<header class="xh-hd"><div class="xh-eyebrow">%s%s</div><h2 class="xh-title">%s</h2>%s</header>') % (
        MAGNET, e(b['eyebrow']), e(b['title']), '<p class="xh-deck">%s</p>' % e(b['deck']) if b.get('deck') else '')
    p = b.get('plate')
    if not p: return '<div class="xh-wrap">%s</div>' % h
    at = COLS.index(p['column'])
    cols = ''.join('<li class="%s"><i>%s</i><span>%s</span></li>' % ('is-at' if i == at else '', MAGNET, e(c)) for i, c in enumerate(COLS))
    plate = ('<div class="xh-board" aria-label="Ward board: %s"><div class="xh-bt"><span class="xh-bn">Ward board</span><b>%s</b></div><ol>%s</ol></div>') % (e(p['column']), e(p['name']), cols)
    return '<div class="xh-wrap xh-with">%s%s</div>' % (h, plate)

# ------------------------------------------------------------------------------------------ swap: magnets moved from today to with the changes
def r_swap(b, ctx):
    grp = ctx.uid('prsw'); rows, boxes = [], []
    for i, r in enumerate(b['rows']):
        s = b['sheets'][i]; first = i == 0
        rows.append(('<li class="xs-row%s"%s><button type="button"%s><b>%s</b><span>%s</span></button>'
                     '<button type="button" class="xs-mag" aria-pressed="false" aria-label="%s: move to %s">%s<span class="xs-t xs-today">%s%s</span><span class="xs-t xs-with">%s%s</span>%s</button>%s</li>') % (
            ' xs-flag' if r.get('flag') else '', pt(r), pick(grp, s['key'], first, 'xs-name'), e(r['name']), e(r['who']), e(r['name']), e(b['with_label']), MAGNET,
            e(r['today']), ' <em>%s</em>' % e(r['today_at']) if r.get('today_at') else '', e(r['with']), ' <em>%s</em>' % e(r['with_at']) if r.get('with_at') else '',
            '<b class="xh-flag">%s</b>' % e(r['flag']) if r.get('flag') else '', sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    return ('<section class="sx-block px-x xs" data-block="swap" data-state="today">%s<div class="xs-bar"><div class="xh-seg" role="group" aria-label="Show">'
            '<button type="button" data-s="today" aria-pressed="true">Today</button><button type="button" data-s="with" aria-pressed="false">%s</button></div>'
            '<span class="xs-count" aria-live="polite"><b>0</b> of %d moved</span></div>'
            '<div class="xs-heads"><span>Step, and who</span><span>Today</span><span>%s</span></div><ol class="xs-rows">%s</ol><p class="xh-rule">%s</p>%s%s</section>') % (
        hint(b.get('hint') or 'Pick a step to open it. Move its magnet, or move them all at once.'), e(b['with_label']), len(b['rows']), e(b['with_label']), ''.join(rows), e(b['keeps']),
        cond(b.get('condition')), desk(boxes))

# ------------------------------------------------------------------------------------------ trial: the two weeks on one ward
PH = ['#9C92A1', '#6D4A77', '#8A5608', '#2F6B4F', '#2A1E30']
def r_trial(b, ctx):
    grp = ctx.uid('prtr'); days = b.get('days', 14); ph = b['phases']
    def phase_of(d):
        for j, p in enumerate(ph):
            if p['from'] <= d <= p['to']: return j
        return 0
    bands, boxes = [], []
    for j, p in enumerate(ph):
        s = b['sheets'][j]; first = j == 0
        span = ('Days %d to %d' % (p['from'], p['to'])) if p['to'] > p['from'] else 'Day %d' % p['from']
        bands.append('<div class="xt-cell" style="grid-column:%d / %d;--c:%s"><button type="button"%s data-from="%d" data-to="%d"%s><small>%s</small><b>%s</b><em>%s</em></button>%s</div>' % (
            p['from'], p['to'] + 1, PH[j % 5], pick(grp, s['key'], first, 'xt-band'), p['from'], p['to'], pt(p), e(span), e(p['title']), e(p['who']), sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    dots = ''.join('<span class="xt-day%s" data-d="%d" style="--c:%s"><i>%d</i></span>' % (' xt-wk2' if d == 8 else '', d, PH[phase_of(d) % 5], d) for d in range(1, days + 1))
    w = b['ward']
    needs = ''.join('<li>%s<span>%s</span></li>' % (TICK, e(n)) for n in b['needs'])
    ward_entry = G['L'].entry('The trial ward', w['ask'], w.get('ask_hint', 'Type the ward’s name'), fill='%s:ward' % grp) if w.get('ask') else ''
    return ('<section class="sx-block px-x xt" data-block="trial" data-day="1" data-days="%d">%s'
            '<div class="xt-top"><div class="xt-ward xt-ward-%s"%s><span class="sx-label">The trial ward</span><b>%s</b><span class="xt-wn">%s</span>%s%s</div>'
            '<ul class="xt-needs" aria-label="What the trial needs">%s</ul></div>'
            '<div class="xt-board"><div class="xt-bar"><button type="button" class="xh-play xt-play">%s<span>Play the two weeks</span></button>'
            '<span class="xt-now" aria-live="polite">Day <b>1</b> of %d</span></div>'
            '<div class="xt-weeks"><span>Week 1</span><span>Week 2</span></div><div class="xt-dots" style="--n:%d">%s</div>'
            '<div class="xt-bands" style="--n:%d">%s</div></div>%s%s</section>') % (
        days, hint(b.get('hint') or 'Pick a part of the trial, or play the two weeks.'), e(w['status']), pt(w), e(w['label']), e(w['note']),
        '<span class="xh-tag xh-tag-needed">Needs your choice</span>' if w['status'] == 'needed' else '<span class="xh-tag xh-tag-ok">Chosen</span>', ward_entry,
        needs, PLAY, days, days, dots, days, ''.join(bands), cond(b.get('condition')), desk(boxes))

# ------------------------------------------------------------------------------------------ badges: who has to agree, on the board
STATUS = {'agreed': 'Agreed', 'to_ask': 'Still to ask', 'worried': 'Has a worry'}
def r_badges(b, ctx):
    grp = ctx.uid('prbg'); groups, order, boxes = {}, [], []
    for i, p in enumerate(b['people']):
        s = b['sheets'][i]; first = i == 0
        if p['group'] not in groups: groups[p['group']] = []; order.append(p['group'])
        groups[p['group']].append('<li><button type="button"%s data-trial="%s" data-st="%s"%s>%s<span class="xb-av">%s</span><span class="xb-n">%s</span><span class="xb-st">%s</span>%s</button>%s</li>' % (
            pick(grp, s['key'], first, 'xb-b xb-' + p['status']), 'y' if p.get('trial') else 'n', p['status'], pt(p), CLIP, e(initials(p['name'])), e(p['name']), STATUS[p['status']],
            '<span class="xb-in">In the trial</span>' if p.get('trial') else '', sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    ppl = b['people']
    n_t = sum(1 for p in ppl if p.get('trial')); n_a = sum(1 for p in ppl if p['status'] != 'agreed')
    cols = ' '.join('minmax(124px,%dfr)' % max(2, len(groups[g])) for g in order)
    board = ''.join('<section class="xb-g"><h4>%s</h4><ul>%s</ul></section>' % (e(g), ''.join(groups[g])) for g in order)
    return ('<section class="sx-block px-x xb" data-block="badges" data-filter="all">%s<div class="xh-seg" role="group" aria-label="Show">'
            '<button type="button" data-f="all" aria-pressed="true">Everyone <b>%d</b></button><button type="button" data-f="trial" aria-pressed="false">In the trial <b>%d</b></button>'
            '<button type="button" data-f="ask" aria-pressed="false">Still to ask <b>%d</b></button></div>'
            '<div class="xb-board" style="--cols:%s">%s</div><p class="xh-rule">%s</p>%s</section>') % (
        hint(b.get('hint') or 'Pick a name badge to see what changes for that person.'), len(ppl), n_t, n_a, cols, board, e(b['rule']), desk(boxes))

# ------------------------------------------------------------------------------------------ seats: chairs, lamps and the busy-hours check
LAMP = {'met': 'Met', 'not': 'Not met', 'unknown': 'Not known yet'}
def lakh(lo, hi):
    f = lambda v: ('%g' % v)
    return '₹%s lakh' % f(lo) if lo == hi else '₹%s to %s lakh' % (f(lo), f(hi))
def clock(h):
    h = h % 24
    return 'midnight' if h == 0 else ('noon' if h == 12 else '%d %s' % (h % 12 or 12, 'AM' if h < 12 else 'PM'))

def r_seats(b, ctx):
    grp = ctx.uid('prst'); roles, boxes = [], []
    for i, r in enumerate(b['roles']):
        s = b['sheets'][i]; first = i == 0
        trig = ''.join('<li class="xc-lamp xc-%s"%s%s><i></i><span>%s</span><span class="xc-lv"><b>%s</b>%s</span></li>' % (
            t['state'], ' data-above="%g"' % t['above'] if t.get('above') is not None else '', pt(t), e(t['label']), e(t.get('value') or LAMP[t['state']]), src(t['source'])) for t in r.get('triggers', []))
        cost = lakh(r['cost_low'], r['cost_high']) + (' a year each' if r.get('each') else ' a year')
        roles.append(('<li class="xc-li"><div class="xc-role xc-%s%s" data-seats="%d" data-lo="%g" data-hi="%g" data-each="%s">'
                      '<button type="button"%s%s><span class="xc-chairs">%s</span><span class="xc-h"><b>%s</b><span class="xc-state">%s</span></span><span class="xc-does">%s</span><span class="xc-cost">%s</span></button>'
                      '%s%s</div>%s</li>') % (
            r['state'], ' xc-sized' if r.get('sized') else '', r['seats'], r['cost_low'], r['cost_high'], 'y' if r.get('each') else 'n',
            pick(grp, s['key'], first, 'xc-pick'), pt(r), ''.join(SEAT(False) for _ in range(r['seats'])), e(r['name']),
            {'needed': 'Needed now', 'optional': 'Optional for now', 'check': 'Needs your numbers'}[r['state']], e(r['does']), e(cost),
            ('<ul class="xc-lamps"><li class="xc-rule">%s</li>%s</ul>' % (e(r.get('rule', 'Any one is enough')), trig)) if trig else '',
            '<p class="xc-note">%s</p>' % e(r['note']) if r.get('note') else '', sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    top = ''
    if b.get('reports_to'):
        top = '<div class="xc-top"><div class="xc-boss"%s>%s<b>%s</b><span>%s</span></div></div>' % (pt(b['reports_to']), SEAT(True, 'xc-boss-s'), e(b['reports_to']['name']), e(b['reports_to']['does']))
    size = ''
    z = b.get('sizing')
    if z:
        span = float(z['end'] - z['start'])
        wins = ''.join('<div class="xc-win" style="--a:%.2f%%;--b:%.2f%%"><b>%s</b><span>%s</span></div>' % (
            100.0 * (w['from'] - z['start']) / span, 100.0 * (w['to'] - z['start']) / span, e(w['label']), e(w['clock'])) for w in z['windows'])
        ticks = ''.join('<span style="left:%.2f%%">%s</span>' % (100.0 * (h - z['start']) / span, e(clock(h))) for h in range(z['start'], z['end'] + 1, 3))
        size = ('<section class="xc-sz"%s data-mode="busy" data-per="%g" data-lo="%d" data-hi="%d" data-wins=\'%s\' data-start="%d" data-end="%d">'
                '<div class="xc-szbar"><div class="xh-seg" role="group" aria-label="Size by"><button type="button" data-m="flat" aria-pressed="false">%s</button><button type="button" data-m="busy" aria-pressed="true">%s</button></div>'
                '<label class="xc-sl"><span>%s <b class="xc-n">%d</b></span><input type="range" class="xc-range" min="%d" max="%d" step="1" value="%d" aria-label="%s"></label></div>'
                '<div class="xc-day"><div class="xc-ticks">%s</div><div class="xc-wins">%s</div><div class="xc-people"></div></div>'
                '<div class="xc-read"><div><span class="sx-label">%s</span><b class="xc-count"></b></div><p class="xc-why" aria-live="polite"></p></div>'
                '<div class="xc-total"><span class="sx-label">%s</span><b class="xc-cost-t"></b></div></section>') % (
            pt(z), z['per_person'], z['yours_low'], z['yours_high'], json.dumps([[w['from'], w['to'], w['label']] for w in z['windows']]), z['start'], z['end'],
            e(z['flat_label']), e(z['busy_label']), e(z['slider_label']), z['default'], z['min'], z['max'], z['default'], e(z['slider_label']), ticks, wins,
            e(z['count_label']), e(z['total_label']))
    return ('<section class="sx-block px-x xc"%s data-block="seats" data-flat="%s" data-busy="%s" data-recheck="%s">%s%s<ol class="xc-roles" style="--r:%d">%s</ol>%s%s%s</section>') % (
        ' data-sized="y"' if z else '', e(z['flat_text']) if z else '', e(z['busy_text']) if z else '', e(z['recheck_text']) if z else '',
        hint(b.get('hint') or 'Pick a role to open it. Move the slider to size the team.'), top, len(b['roles']), ''.join(roles), size,
        '<p class="xc-others">%s</p>' % e(b['others']) if b.get('others') else '', desk(boxes))

# ------------------------------------------------------------------------------------------ readouts: the measures as instrument windows
def r_readouts(b, ctx):
    grp = ctx.uid('prrd'); cells, boxes = [], []
    for i, m in enumerate(b['measures']):
        s = b['sheets'][i]; first = i == 0
        cells.append('<li><button type="button"%s data-when="%s"%s><span class="xr-n">%s</span><span class="xr-w"><span class="xr-v xr-now">%s</span><span class="xr-v xr-end">%s</span></span>%s</button>%s</li>' % (
            pick(grp, s['key'], first, 'xr xr-' + m['state']), m['when'], pt(m), e(m['name']), e(m['value']) if m['state'] == 'confirmed' else 'No number yet',
            'Read on day 14' if m['when'] == 'trial' else 'Read after', src(m['source']), sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    ms = b['measures']
    return ('<section class="sx-block px-x xr-sec" data-block="readouts" data-filter="all" data-view="now">%s<div class="xr-bar"><div class="xh-seg" role="group" aria-label="Show">'
            '<button type="button" data-f="all" aria-pressed="true">All <b>%d</b></button><button type="button" data-f="trial" aria-pressed="false">In the trial <b>%d</b></button>'
            '<button type="button" data-f="later" aria-pressed="false">After the trial <b>%d</b></button></div>'
            '<div class="xh-seg" role="group" aria-label="Read"><button type="button" data-v="now" aria-pressed="true">Starting number</button><button type="button" data-v="end" aria-pressed="false">After the trial</button></div></div>'
            '<div class="xr-key"><span><i class="k-c"></i>%d with your starting number</span><span><i class="k-n"></i>%d new, no number made up</span></div>'
            '<ol class="xr-grid">%s</ol>%s%s</section>') % (
        hint(b.get('hint') or 'Pick a window to see how it is measured and who records it.'), len(ms), sum(1 for m in ms if m['when'] == 'trial'), sum(1 for m in ms if m['when'] == 'later'),
        sum(1 for m in ms if m['state'] == 'confirmed'), sum(1 for m in ms if m['state'] != 'confirmed'), ''.join(cells), cond(b.get('condition')), desk(boxes))

# ------------------------------------------------------------------------------------------ loop: plan, try, measure, adjust, spread
def r_loop(b, ctx):
    grp = ctx.uid('prlp'); st = b['steps']; n = len(st); cx, cy, r = 160, 160, 118
    arcs, nodes, rows, boxes = [], [], [], []
    g = b['gate']
    for i in range(n):
        a1 = math.radians(-90 + i * 360.0 / n + 13); a2 = math.radians(-90 + (i + 1) * 360.0 / n - 13)
        arcs.append('<path class="xl-arc" data-a="%d" d="M%.1f %.1f A%d %d 0 0 1 %.1f %.1f" marker-end="url(#%s-ah)"/>' % (
            i, cx + r * math.cos(a1), cy + r * math.sin(a1), r, r, cx + r * math.cos(a2), cy + r * math.sin(a2), grp))
        a = math.radians(-90 + i * 360.0 / n)
        s = dict(b['sheets'][i]); first = i == b.get('at', 0)
        nodes.append('<button type="button"%s data-k="%d" style="left:%.2f%%;top:%.2f%%"%s><b>%d</b><span>%s</span></button>' % (
            pick(grp, s['key'], first, 'xl-node'), i, 100 * (cx + r * math.cos(a)) / 320, 100 * (cy + r * math.sin(a)) / 320, pt(st[i]), i + 1, e(st[i]['name'])))
        gate = ('<div class="xl-gate"><b>%s</b><div><button type="button" class="xh-pill xl-yes" data-go="%d">%s</button><button type="button" class="xh-pill xl-no" data-go="%d">%s</button></div></div>' % (
            e(g['question']), g['yes_to'], e(g['yes']), g['no_to'], e(g['no']))) if i == g['at'] else ''
        sm, sd = sheet(s, grp, first, 'mob-li'), sheet(s, grp, first, 'desk')
        if gate:
            sm = sm.replace('</div><', '</div>%s<' % gate, 1); sd = sd.replace('</div><', '</div>%s<' % gate, 1)
        rows.append('<li><button type="button"%s data-k="%d"><b>%d</b><span>%s</span><em>%s</em></button></li>%s' % (
            pick(grp, s['key'], first, 'xl-row'), i, i + 1, e(st[i]['name']), e(st[i]['who']), sm))
        boxes.append(sd)
    return ('<section class="sx-block px-x xl" data-block="loop" data-at="%d" data-gate="%d" data-no="%d" data-retry="%d">%s<div class="xl-grid"><div class="xl-wheel"><svg viewBox="0 0 320 320" aria-hidden="true"><defs>'
            '<marker id="%s-ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" class="xl-ahp"/></marker></defs>'
            '<circle class="xl-ring" cx="160" cy="160" r="118"/>%s</svg>%s<div class="xl-mid"><span class="xl-round">Round <b>1</b></span><b class="xl-now"></b><span class="xl-sub">%s</span></div></div>'
            '<div class="xl-side"><div class="xl-bar"><button type="button" class="xh-pill xl-prev">Back</button><button type="button" class="xh-pill xh-pill-on xl-next">Next step</button></div>'
            '<ol class="xl-list">%s</ol>%s</div></div></section>') % (
        b.get('at', 0), g['at'], g['no_to'], g['retry_to'], hint(b.get('hint') or 'Step round the loop, or pick a step. At the check, the answer sends you on or back.'),
        grp, ''.join(arcs), ''.join(nodes), e(b['sub']), ''.join(rows), desk(boxes))

# ------------------------------------------------------------------------------------------ timesheet: one normal day, typed in, then filled
def r_timesheet(b, ctx):
    grp = ctx.uid('prts'); blank = b['mode'] == 'blank'; L = G['L']
    items, boxes = [], []
    for i, s0 in enumerate(b['steps']):
        s = b['sheets'][i]; first = i == 0
        if blank:
            chip = L.inline('%s (%s)' % (s0['title'], s0['field']), 'hh : mm', grp)
        else:
            chip = '<span class="xm-val">%s</span>' % e(s0['value'])
        gap = '<span class="xm-gap">%s</span>' % e(s0['gap']) if s0.get('gap') and not blank else ''
        items.append('<li class="xm-cell"><div role="button" tabindex="0"%s data-state="%s"%s><span class="xm-dot">%d</span><b class="xm-name">%s</b><small class="xm-f">%s</small>%s</div>%s%s</li>' % (
            pick(grp, s['key'], first, 'xm-stop'), e(s0.get('state', 'plain')), pt(s0), i + 1, e(s0['title']), e(s0['field']), chip, gap, sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    count = ('<p class="xm-count"><span class="sx-label">%s</span> <b data-count-for="%s" data-waiting="%s" data-done="%s">%s</b></p>' % (
        e(b.get('count_label', 'Times typed in')), grp, e(b.get('waiting', 'None typed yet')), e(b.get('done', 'All in. Send to Tojo.')), e(b.get('waiting', 'None typed yet')))) if blank else ''
    return ('<section class="sx-block px-x xm xm-%s" data-block="timesheet">%s<div class="xm-sheet"><div class="xm-head"><span class="xm-paper">%s</span><span class="xm-day">%s</span></div>'
            '<ol class="xm-line" style="--n:%d">%s</ol>%s</div>%s%s</section>') % (
        e(b['mode']), hint(b.get('hint') or ('Type a rough time on each step. Leave a step empty if nobody records it.' if blank else 'Pick a step to see what it shows.')),
        e(b['label']), e(b['day']), len(b['steps']), ''.join(items), count, cond(b.get('caption')), desk(boxes))

# ------------------------------------------------------------------------------------------ night lanes: each job on one clock, evening to afternoon
def _hr(t, t0):
    h, m = [int(x) for x in t.split(':')]; v = h + m / 60.0
    return v + 24 if v < t0 else v
def _clk(h):
    h = h % 24; hh = int(h); mm = int(round((h - hh) * 60))
    if (hh, mm) == (0, 0): return 'midnight'
    if (hh, mm) == (12, 0): return 'noon'
    return '%d%s %s' % (hh % 12 or 12, ':%02d' % mm if mm else '', 'AM' if hh < 12 else 'PM')

def r_lanes(b, ctx):
    grp = ctx.uid('prnl')
    t0 = int(b['from'].split(':')[0]); a, z = _hr(b['from'], t0), _hr(b['to'], t0)
    night = b.get('night')
    n0, n1 = (_hr(night['from'], t0), _hr(night['to'], t0)) if night else (z, z)
    squeeze = 1.5                                   # the night is drawn as if it were an hour and a half long
    total = (n0 - a) + (squeeze if night else 0) + (z - n1)
    def X(t):
        h = _hr(t, t0) if isinstance(t, str) else t
        if h <= n0: u = h - a
        elif h <= n1: u = (n0 - a) + squeeze * (h - n0) / ((n1 - n0) or 1)
        else: u = (n0 - a) + (squeeze if night else 0) + (h - n1)
        return 100.0 * u / total
    hours = [h for h in range(int(a), int(z) + 1, 3) if not (n0 < h < n1)] + ([int(n0), int(n1)] if night else [])
    ticks = ''.join('<span style="left:%.2f%%">%s</span>' % (X(float(h)), e(_clk(h))) for h in sorted(set(hours)))
    lines = ''.join('<i style="left:%.2f%%"></i>' % X(float(h)) for h in sorted(set(hours)))
    band = '<span class="xn-night" style="left:%.2f%%;width:%.2f%%"><em>%s</em></span>' % (X(n0), X(n1) - X(n0), e(night['label'])) if night else ''
    lanes, boxes = [], []
    for i, ln in enumerate(b['lanes']):
        s = b['sheets'][i]; first = i == 0
        bars = ''
        for k in ('today', 'with'):
            x = ln[k]; l0, l1 = X(x['from']), X(x['to'])
            right = l0 > 58
            bars += ('<span class="xn-bar xn-%s" data-state="%s" style="left:%.2f%%;width:%.2f%%"></span>'
                     '<span class="xn-lab xn-lab-%s%s" style="%s:%.2f%%"><b>%s</b> %s to %s</span>') % (
                k, e(x.get('state', 'plain')), l0, max(l1 - l0, 1.6), k, ' xn-r' if right else '', 'right' if right else 'left', (100 - l1) if right else l0,
                e(x['label']), e(_clk(_hr(x['from'], t0))), e(_clk(_hr(x['to'], t0))))
        txt = ''.join('<span class="xn-tx xn-tx-%s"><small>%s</small>%s · %s to %s</span>' % (k, e(b['switch'][k]), e(ln[k]['label']), e(_clk(_hr(ln[k]['from'], t0))), e(_clk(_hr(ln[k]['to'], t0)))) for k in ('today', 'with'))
        lanes.append('<li class="xn-lane%s"><button type="button"%s%s><b>%s</b><em>%s</em>%s</button><div class="xn-track">%s</div><div class="xn-txs">%s</div>%s</li>' % (
            ' xn-flag' if ln.get('flag') else '', pick(grp, s['key'], first, 'xn-name'), pt(ln), e(ln['name']), e(ln.get('who', '')),
            '<span class="xh-flag">%s</span>' % e(ln['flag']) if ln.get('flag') else '', bars, txt, sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    sw = b['switch']
    return ('<section class="sx-block px-x xn" data-block="night-lanes" data-state="today">%s<div class="xn-bar0"><div class="xh-seg" role="group" aria-label="Which day">'
            '<button type="button" data-s="today" aria-pressed="true">%s</button><button type="button" data-s="with" aria-pressed="false">%s</button></div>'
            '<p class="xn-cap" aria-live="polite"><span class="xn-c-today">%s</span><span class="xn-c-with">%s</span></p></div>'
            '<div class="xn-board"><div class="xn-axis"><span></span><div class="xn-ticks">%s</div></div><ol class="xn-lanes"><li class="xn-bands" aria-hidden="true"><span></span><div class="xn-track">%s%s</div></li>%s</ol></div>%s%s</section>') % (
        hint(b.get('hint') or 'Pick a job to open it. Switch to see the same work with the changes.'), e(sw['today']), e(sw['with']), e(sw['cap_today']), e(sw['cap_with']),
        ticks, lines, band, ''.join(lanes), cond(b.get('caption')), desk(boxes))

# ============================================================================================== behaviour beyond the layer
JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  function seg(root,attr,fn){$$('.xh-seg button['+attr+']',root).forEach(function(b){b.addEventListener('click',function(){
    $$('button',b.parentNode).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});fn(b.getAttribute(attr));});});}
  /* raise an item without scrolling (the layer's own picking, for play and step buttons) */
  function raise(p){if(!p)return;var g=p.getAttribute('data-grp'),k=p.getAttribute('data-key');
    $$('.tl-pick[data-grp="'+g+'"]').forEach(function(o){var on=o.getAttribute('data-key')===k;o.classList.toggle('is-up',on);o.setAttribute('aria-expanded',on?'true':'false');});
    $$('[data-box^="'+g+':"]').forEach(function(b){b.hidden=b.getAttribute('data-box')!==g+':'+k;});}
  /* swap: move each magnet across, one at a time or all together */
  $$('.xs').forEach(function(sw){var rows=$$('.xs-row',sw),n=rows.length;
    function upd(){var k=rows.filter(function(r){return r.classList.contains('is-moved');}).length;sw.querySelector('.xs-count b').textContent=k;
      var s=k===n?'with':(k===0?'today':'');$$('.xh-seg button',sw).forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-s')===s?'true':'false');});sw.setAttribute('data-state',s||'mixed');}
    rows.forEach(function(r){r.querySelector('.xs-mag').addEventListener('click',function(){r.classList.toggle('is-moved');r.querySelector('.xs-mag').setAttribute('aria-pressed',r.classList.contains('is-moved')?'true':'false');upd();});});
    seg(sw,'data-s',function(s){rows.forEach(function(r,i){var go=s==='with';setTimeout(function(){r.classList.toggle('is-moved',go);r.querySelector('.xs-mag').setAttribute('aria-pressed',go?'true':'false');upd();},reduce?0:i*90);});});
    upd();});
  /* trial: the day strip follows the picked part; play walks the two weeks */
  $$('.xt').forEach(function(tr){var days=+tr.getAttribute('data-days'),timer=null,play=tr.querySelector('.xt-play'),bands=$$('.xt-band',tr);
    function day(d,lift){tr.setAttribute('data-day',d);$$('.xt-day',tr).forEach(function(x){var k=+x.getAttribute('data-d');x.classList.toggle('is-past',k<d);x.classList.toggle('is-now',k===d);});
      tr.querySelector('.xt-now b').textContent=d;if(lift){var b=bands.filter(function(x){return +x.getAttribute('data-from')<=d&&d<=+x.getAttribute('data-to');})[0];raise(b);}}
    function stop(){if(timer){clearInterval(timer);timer=null;}play.classList.remove('is-on');play.querySelector('span').textContent='Play the two weeks';}
    bands.forEach(function(b){b.addEventListener('click',function(){stop();day(+b.getAttribute('data-from'),false);});});
    play.addEventListener('click',function(){if(timer){stop();return;}var d=+tr.getAttribute('data-day');if(d>=days)d=0;play.classList.add('is-on');play.querySelector('span').textContent='Pause';
      if(reduce){day(days,true);stop();return;}timer=setInterval(function(){d++;if(d>days){stop();return;}day(d,true);},650);});
    day(1,false);});
  /* badges: filter who is shown */
  $$('.xb').forEach(function(pp){seg(pp,'data-f',function(f){pp.setAttribute('data-filter',f);$$('.xb-b',pp).forEach(function(b){
      var on=f==='all'||(f==='trial'&&b.getAttribute('data-trial')==='y')||(f==='ask'&&b.getAttribute('data-st')!=='agreed');b.classList.toggle('is-dim',!on);});});});
  /* seats: the slider drives the lamps, the chairs and the busy-hours check */
  $$('.xc').forEach(function(st){var z=st.querySelector('.xc-sz');
    function fmt(v){return (Math.round(v*10)/10).toString();}
    function range(lo,hi){return lo===hi?'₹'+fmt(lo)+' lakh':'₹'+fmt(lo)+' to '+fmt(hi)+' lakh';}
    function upd(){var n=z?+z.querySelector('.xc-range').value:0,mode=z?z.getAttribute('data-mode'):'',lo=0,hi=0;
      $$('.xc-role',st).forEach(function(r){
        $$('.xc-lamp[data-above]',r).forEach(function(l){var met=n>+l.getAttribute('data-above');l.classList.toggle('xc-met',met);l.classList.toggle('xc-not',!met);l.querySelector('b').textContent=n+' a day';});
        var lamps=$$('.xc-lamp',r);
        if(lamps.length&&z){var any=lamps.some(function(l){return l.classList.contains('xc-met');}),unk=lamps.some(function(l){return l.classList.contains('xc-unknown');});
          r.classList.remove('xc-needed','xc-optional','xc-check');r.classList.add(any?'xc-needed':(unk?'xc-check':'xc-optional'));
          r.querySelector('.xc-state').textContent=any?'Needed now':(unk?'Needs your numbers':'Optional for now');}
        var seats=+r.getAttribute('data-seats');
        if(z&&r.classList.contains('xc-sized')){var per=+z.getAttribute('data-per'),wins=JSON.parse(z.getAttribute('data-wins'));seats=mode==='flat'?Math.max(1,Math.ceil(n/per)):wins.length;
          var ch=r.querySelector('.xc-chairs'),have=ch.children.length;while(have<seats){ch.insertAdjacentHTML('beforeend',ch.firstElementChild.outerHTML);have++;}while(have>seats){ch.removeChild(ch.lastElementChild);have--;}}
        var need=!r.classList.contains('xc-optional');
        $$('.xh-seat',r).forEach(function(s){s.classList.toggle('on',need);});
        if(need&&!r.classList.contains('xc-check')){var k=r.getAttribute('data-each')==='y'?seats:1;lo+=k*+r.getAttribute('data-lo');hi+=k*+r.getAttribute('data-hi');}});
      if(!z)return;
      var per=+z.getAttribute('data-per'),wins=JSON.parse(z.getAttribute('data-wins')),a=+z.getAttribute('data-start'),b=+z.getAttribute('data-end'),ylo=+z.getAttribute('data-lo'),yhi=+z.getAttribute('data-hi'),inr=n>=ylo&&n<=yhi;
      z.querySelector('.xc-n').textContent=n;var html='';
      if(mode==='flat'){var k=Math.max(1,Math.ceil(n/per));for(var i=0;i<k;i++)html+='<div class="xc-p xc-flat"><span style="--a:0%;--b:100%">Person '+(i+1)+', all day</span></div>';
        z.querySelector('.xc-count').textContent=k+(k===1?' person':' people');z.querySelector('.xc-why').textContent=st.getAttribute('data-flat').replace('{n}',n).replace('{k}',k);}
      else{html='<div class="xc-p">';wins.forEach(function(w,i){html+='<span style="--a:'+(100*(w[0]-a)/(b-a))+'%;--b:'+(100*(w[1]-a)/(b-a))+'%">Person '+(i+1)+'</span>';});html+='</div>';
        z.querySelector('.xc-count').textContent=wins.length+' people';z.querySelector('.xc-why').textContent=inr?st.getAttribute('data-busy'):st.getAttribute('data-recheck');}
      z.classList.toggle('is-recheck',mode==='busy'&&!inr);z.querySelector('.xc-people').innerHTML=html;z.querySelector('.xc-cost-t').textContent=range(lo,hi)+' a year';}
    if(z){z.querySelector('.xc-range').addEventListener('input',upd);seg(z,'data-m',function(m){z.setAttribute('data-mode',m);upd();});}
    upd();});
  /* readouts: filter, and flip between the starting number and after the trial */
  $$('.xr-sec').forEach(function(rd){
    seg(rd,'data-f',function(f){rd.setAttribute('data-filter',f);$$('.xr',rd).forEach(function(b){var on=f==='all'||b.getAttribute('data-when')===f;b.classList.toggle('is-dim',!on);});});
    seg(rd,'data-v',function(v){rd.setAttribute('data-view',v);});});
  /* loop: step round; at the check the answer sends the marker on or back */
  $$('.xl').forEach(function(lp){var nodes=$$('.xl-node',lp),rows=$$('.xl-row',lp),n=nodes.length,round=1,gate=+lp.getAttribute('data-gate');
    function go(k,back,lift){k=(k+n)%n;lp.setAttribute('data-at',k);
      nodes.forEach(function(x,i){x.classList.toggle('is-done',i<k);});rows.forEach(function(x,i){x.classList.toggle('is-done',i<k);});
      $$('.xl-arc',lp).forEach(function(a,i){a.classList.toggle('is-done',i<k);});
      lp.querySelector('.xl-now').textContent=nodes[k].querySelector('span').textContent;lp.querySelector('.xl-round b').textContent=round;
      lp.querySelector('.xl-prev').disabled=k===0&&round===1;lp.querySelector('.xl-next').hidden=k===gate;
      lp.querySelector('.xl-next').textContent=k===n-1?'Next ward':(k===+lp.getAttribute('data-no')?'Try again':'Next step');
      if(lift)raise(nodes[k]);lp.classList.remove('is-back');if(back){void lp.offsetWidth;lp.classList.add('is-back');}}
    nodes.concat(rows).forEach(function(x){x.addEventListener('click',function(){go(+x.getAttribute('data-k'));});});
    lp.querySelector('.xl-next').addEventListener('click',function(){var k=+lp.getAttribute('data-at');if(k===n-1){round=1;go(0,false,true);return;}
      if(k===+lp.getAttribute('data-no')){go(+lp.getAttribute('data-retry'),true,true);return;}go(k+1,false,true);});
    lp.querySelector('.xl-prev').addEventListener('click',function(){go(+lp.getAttribute('data-at')-1,false,true);});
    $$('.xl-yes',lp).forEach(function(b){b.addEventListener('click',function(ev){ev.stopPropagation();go(+b.getAttribute('data-go'),false,true);});});
    $$('.xl-no',lp).forEach(function(b){b.addEventListener('click',function(ev){ev.stopPropagation();round++;go(+b.getAttribute('data-go'),true,true);});});
    go(+lp.getAttribute('data-at'));});
  /* night lanes: today, or with the changes */
  $$('.xn').forEach(function(nl){seg(nl,'data-s',function(s){nl.setAttribute('data-state',s);});});
})();
'''

CSS = r'''
/* ---- shared marks of the ward board ---- */
.xh-mag{width:16px;height:16px;flex-shrink:0}.xh-mag circle{fill:var(--plum)}.xh-mag .xh-mag-s{fill:#fff;opacity:.45}
.xh-mag-s{display:inline-flex}.so-hint .xh-mag{width:14px;height:14px}
.xh-tick{width:16px;height:16px;flex-shrink:0}.xh-tick path{fill:none;stroke:var(--green);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.xh-seat{width:30px;height:33px;flex-shrink:0}.xh-seat path{fill:none;stroke:var(--plum);stroke-width:2.4;stroke-dasharray:3.5 2.5;stroke-linejoin:round;stroke-linecap:round;transition:fill .3s}
.xh-seat.on path{stroke-dasharray:none}.xh-seat.on .xh-seat-b,.xh-seat.on .xh-seat-c{fill:var(--plum)}
.xh-src{display:inline-block;font-size:10.5px;font-weight:600;padding:2px 7px;border-radius:10px;border:1.5px solid var(--green);color:var(--green);white-space:nowrap;font-style:normal}
.xh-src-derived,.xh-src-estimate,.xh-src-illustrative,.xh-src-target{border-style:dashed;border-color:var(--gold-t);color:var(--gold-t)}
.xh-src-needed{border-style:dashed;border-color:var(--red);color:var(--red)}.xh-src-new{border-style:dashed;border-color:var(--amber);color:var(--amber)}
.xh-tag{display:inline-block;font-size:11px;font-weight:600;padding:2px 9px;border-radius:11px;border:1.5px solid var(--off);color:var(--muted);white-space:nowrap}
.xh-tag-needed{border-style:dashed;border-color:var(--amber);color:var(--amber)}.xh-tag-ok{border-color:var(--green);color:var(--green)}
.xh-flag{display:inline-block;font-size:10.5px;font-weight:600;padding:1px 7px;border:1.5px solid var(--amber);color:var(--amber);border-radius:10px;white-space:nowrap;background:#fff}
.xh-seg{display:inline-flex;background:var(--board);border:1.5px solid var(--ink);border-radius:22px;padding:3px;gap:2px;flex-wrap:wrap;align-self:flex-start}
.sx .xh-seg button{border:0;background:transparent;border-radius:18px;font-size:13px;font-weight:500;padding:0 14px;min-height:36px;color:var(--ink);cursor:pointer}
.xh-seg button b{font-weight:600;color:var(--plum);margin-left:3px}
.sx .xh-seg button[aria-pressed=true]{background:var(--plum);color:#fff}.xh-seg button[aria-pressed=true] b{color:var(--plum-l)}
.sx .xh-pill{border:1.5px solid var(--ink);background:var(--board);border-radius:22px;font-size:13px;font-weight:500;padding:0 16px;min-height:40px;cursor:pointer;color:var(--ink)}
.sx .xh-pill-on{background:var(--plum);border-color:var(--plum);color:#fff;box-shadow:inset 5px 0 0 var(--gold)}
.xh-pill:disabled{opacity:.4;cursor:default}
.sx .xh-play{display:inline-flex;align-items:center;gap:8px;border:0;border-radius:22px;background:var(--ink);color:#fff;font-size:13px;font-weight:600;padding:0 16px;min-height:42px;cursor:pointer}
.xh-play svg{width:13px;height:13px}.xh-play .pl{fill:var(--plum-l)}.xh-play .pa{stroke:var(--plum-l);stroke-width:2.6;display:none}.xh-play.is-on .pl{display:none}.xh-play.is-on .pa{display:inline}
.xh-rule{font-size:13px;font-weight:500;background:var(--ink);color:#F3EEF5;border-radius:12px;padding:10px 14px;line-height:1.45;box-shadow:inset 6px 0 0 var(--gold)}
.px-x{display:flex;flex-direction:column;gap:12px}
.px-x li.bx{list-style:none}
/* ---- heading with the ward board ---- */
.xh-wrap{border-bottom:2px solid var(--ink);padding-bottom:12px}
.xh-with{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:22px;align-items:end}
.xh-hd{display:flex;flex-direction:column;gap:4px}
.xh-eyebrow{font-size:13px;font-weight:600;color:var(--muted);display:flex;align-items:center;gap:8px}.xh-eyebrow .xh-mag{width:18px;height:18px}
.xh-title{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:60px;line-height:.92;letter-spacing:.01em;color:var(--ink)}
.xh-deck{font-size:15px;color:var(--muted);max-width:74ch;line-height:1.45}
.xh-board{background:var(--board);border:2px solid var(--ink);border-radius:12px;padding:10px 12px;min-width:300px;box-shadow:0 5px 0 rgba(42,30,48,.14)}
.xh-bt{display:flex;align-items:baseline;gap:8px;margin-bottom:8px}.xh-bn{font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:var(--ink);color:var(--plum-l);padding:2px 7px;border-radius:4px}
.xh-bt b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:22px;line-height:1}
.xh-board ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px}
.xh-board li{display:flex;flex-direction:column;align-items:center;gap:3px;font-size:10.5px;color:var(--muted);text-align:center;line-height:1.15;padding:4px 2px;border-top:2px solid var(--pxline)}
.xh-board li .xh-mag circle{fill:var(--off)}.xh-board li.is-at{color:var(--ink);font-weight:700;border-top-color:var(--plum)}
.xh-board li.is-at .xh-mag circle{fill:var(--plum)}.xh-board li.is-at i{filter:drop-shadow(0 0 0 2px var(--gold))}
.xh-board li i{display:flex;font-style:normal}
/* ---- swap ---- */
.xs-bar{display:flex;align-items:center;gap:14px;flex-wrap:wrap}.xs-count{font-size:13px;color:var(--muted)}.xs-count b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:26px;color:var(--ink);vertical-align:-3px}
.xs-heads,.xs-row{display:grid;grid-template-columns:190px minmax(0,1fr) minmax(0,1fr);column-gap:14px}
.xs-heads{font-size:12.5px;font-weight:600;color:var(--muted);padding:0 14px}.xs-heads span:last-child{color:var(--plum)}
.sx .xs-rows{list-style:none;margin:0;position:relative;background:var(--board);border:1.5px solid var(--ink);border-radius:14px;padding:6px 14px;box-shadow:0 6px 0 rgba(42,30,48,.12)}
.xs-row{align-items:center;padding:6px 0;border-bottom:1px solid var(--pxline)}.xs-row:last-child{border-bottom:0}
.sx .xs-name{display:flex;flex-direction:column;align-items:flex-start;text-align:left;padding:6px 8px;border:0;border-radius:8px;background:transparent;font:inherit;color:var(--ink)}
.xs-name b{font-size:13.5px;line-height:1.2}.xs-name span{font-size:11.5px;color:var(--muted)}
.sx .xs-mag{grid-column:2;display:flex;align-items:center;gap:8px;text-align:left;min-height:44px;padding:5px 10px;border-radius:10px;border:1.5px solid var(--off);background:var(--wash);color:var(--ink);font:inherit;
  font-size:12.5px;line-height:1.3;transition:transform .45s cubic-bezier(.3,1.3,.5,1),background .3s,color .3s;position:relative;z-index:1;cursor:pointer}
.xs-mag .xh-mag circle{fill:var(--off)}.xs-t em{display:block;font-style:normal;font-weight:600;font-size:11.5px;white-space:nowrap;margin-top:1px}
.xs-with{display:none}.xs-row.is-moved .xs-today{display:none}.xs-row.is-moved .xs-with{display:inline}
.sx .xs-row.is-moved .xs-mag{transform:translateX(calc(100% + 14px));background:var(--plum);border-color:var(--plum);color:#fff}
.xs-row.is-moved .xs-mag .xh-mag circle{fill:var(--gold)}
.sx .xs-flag .xs-mag{border-color:var(--amber);border-width:2px}.xs-flag .xs-name b{color:var(--amber)}
.xs-mag .xh-flag{margin-left:auto}.xs-row.is-moved .xh-flag{display:none}
.xs-row > .bx{grid-column:1/-1}
/* ---- trial ---- */
.xt-top{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:14px;align-items:stretch}
.xt-ward{display:flex;flex-direction:column;gap:5px;background:var(--board);border:1.5px solid var(--ink);border-radius:14px;padding:12px 14px}
.xt-ward b{font-size:15px;line-height:1.3}.xt-wn{font-size:12.5px;color:var(--muted);line-height:1.4}.xt-ward .xh-tag{align-self:flex-start;margin-top:3px}
.xt-ward-needed{border-style:dashed;border-color:var(--amber)}
.xt-needs{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;align-content:center}
.xt-needs li{display:flex;gap:7px;align-items:center;font-size:12.5px;background:var(--board);border-radius:20px;padding:7px 10px;border:1px solid var(--pxline)}
.xt-board{background:var(--board);border:1.5px solid var(--ink);border-radius:14px;padding:12px 14px 14px;box-shadow:0 6px 0 rgba(42,30,48,.12);display:flex;flex-direction:column;gap:10px}
.xt-bar{display:flex;align-items:center;gap:14px}.xt-now{font-size:13px;color:var(--muted)}.xt-now b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:26px;color:var(--ink);vertical-align:-3px}
.xt-weeks{display:grid;grid-template-columns:1fr 1fr;font-size:12px;font-weight:600;color:var(--muted)}.xt-weeks span:last-child{padding-left:6px;border-left:2px solid var(--ink)}
.xt-dots,.xt-bands{display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:6px}
.xt-day{aspect-ratio:1;max-height:48px;border-radius:50%;border:2px solid var(--c);background:#fff;display:flex;align-items:center;justify-content:center;transition:transform .15s,background .2s}
.xt-day i{font-style:normal;font-weight:700;font-size:12.5px}
.xt-day.is-past,.xt-day.is-now{background:var(--c);color:#fff}.xt-day.is-now{transform:scale(1.14);box-shadow:0 3px 0 rgba(42,30,48,.3)}
.xt-dots .xt-day:nth-child(8){box-shadow:-5px 0 0 -3px var(--ink)}.xt-dots .xt-day.is-now:nth-child(8){box-shadow:0 3px 0 rgba(42,30,48,.3)}
.xt-cell{display:flex;flex-direction:column;min-width:0}
.sx .xt-band{display:flex;flex-direction:column;align-items:flex-start;gap:2px;width:100%;height:100%;padding:7px 9px;text-align:left;border:0;border-top:5px solid var(--c);border-radius:8px;background:var(--wash);font:inherit;color:var(--ink);line-height:1.25}
.xt-band small{font-size:10.5px;font-weight:700;color:var(--muted)}.xt-band b{font-size:12.5px}.xt-band em{font-style:normal;font-size:11px;color:var(--muted)}
/* ---- badges ---- */
.xb-board{display:grid;grid-template-columns:var(--cols);background:var(--board);border:1.5px solid var(--ink);border-radius:14px;box-shadow:0 6px 0 rgba(42,30,48,.12);overflow:hidden}
.xb-g{padding:10px 12px 14px;border-right:1.5px solid var(--pxline);min-width:0}.xb-g:last-child{border-right:0}
.xb-g h4{margin:0 0 12px;font-size:13.5px;font-weight:600;padding-bottom:6px;border-bottom:2px solid var(--ink)}
.xb-g ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:12px 8px}
.sx .xb-b{position:relative;width:100%;display:flex;flex-direction:column;align-items:center;gap:3px;padding:14px 6px 9px;background:#fff;border:1.5px solid var(--ink);border-radius:10px;font:inherit;color:var(--ink);transition:transform .15s,opacity .2s}
.xb-clip{position:absolute;top:-7px;left:50%;width:26px;height:14px;transform:translateX(-50%)}.xb-clip path{fill:none;stroke:var(--muted);stroke-width:1.6}.xb-clip rect{fill:var(--plum-l);stroke:var(--ink);stroke-width:1.4}
.xb-av{width:34px;height:34px;border-radius:50%;background:var(--plum);color:#fff;font-weight:700;font-size:13px;display:flex;align-items:center;justify-content:center}
.xb-n{font-size:12.5px;font-weight:600;line-height:1.2;text-align:center}.xb-st{font-size:10.5px;font-weight:600;color:var(--muted)}
.xb-in{font-size:9.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--plum)}
.sx .xb-to_ask{border-style:dashed}.xb-to_ask .xb-st{color:var(--amber)}
.sx .xb-worried{border-color:var(--amber);box-shadow:inset 0 -4px 0 var(--amber)}.xb-worried .xb-av{background:var(--amber)}.xb-worried .xb-st{color:var(--amber)}
.xb-agreed .xb-av{background:var(--green)}.xb-agreed .xb-st{color:var(--green)}
.xb-b.is-dim{opacity:.28}
.xb-g li{display:flex;flex-direction:column;min-width:0}.xb-g li.bx{grid-column:1/-1}
/* ---- seats ---- */
.xc-top{display:flex;justify-content:center;position:relative;padding-bottom:14px}
.xc-top::after{content:'';position:absolute;bottom:0;left:25%;right:25%;height:12px;border:2px solid var(--plum);border-bottom:0;border-radius:8px 8px 0 0}
.xc-top::before{content:'';position:absolute;bottom:12px;left:50%;height:8px;border-left:2px solid var(--plum)}
.xc-boss{display:flex;align-items:center;gap:10px;background:var(--ink);color:#F3EEF5;border-radius:26px;padding:6px 18px 6px 8px}
.xc-boss b{font-size:14px}.xc-boss span{font-size:12px;color:#CFC3D4}.xc-boss .xh-seat path{stroke:var(--plum-l)}.xc-boss .xh-seat.on .xh-seat-b,.xc-boss .xh-seat.on .xh-seat-c{fill:var(--plum-l)}
.xc-roles{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(var(--r),minmax(0,1fr));gap:12px}
.xc-li{display:flex;flex-direction:column;min-width:0}
.xc-role{display:flex;flex-direction:column;gap:8px;background:var(--board);border:1.5px solid var(--ink);border-radius:14px;padding:6px 6px 12px;box-shadow:0 6px 0 rgba(42,30,48,.12);height:100%}
.xc-optional{border-style:dashed}
.sx .xc-pick{display:flex;flex-direction:column;align-items:flex-start;gap:6px;width:100%;padding:8px 8px 6px;text-align:left;border:0;border-radius:10px;background:transparent;font:inherit;color:var(--ink)}
.xc-chairs{display:flex;gap:6px;min-height:36px}.xc-chairs .xh-seat{width:32px;height:36px}
.xc-h{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}.xc-h b{font-size:16px}
.xc-state{font-size:11px;font-weight:600;padding:2px 9px;border-radius:11px;border:1.5px solid var(--green);color:#fff;background:var(--green)}
.xc-optional .xc-state{background:transparent;color:var(--muted);border-color:var(--off)}.xc-check .xc-state{background:transparent;color:var(--amber);border-color:var(--amber);border-style:dashed}
.xc-does{font-size:13px;line-height:1.4;color:var(--muted)}.xc-cost{font-size:13px;font-weight:600}
.xc-lamps{list-style:none;margin:0 8px;padding:6px 0 0;display:flex;flex-direction:column;gap:5px;border-top:1px dashed var(--pxline)}
.xc-rule{font-size:11.5px;font-weight:600;color:var(--muted)}
.xc-lamp{display:grid;grid-template-columns:14px minmax(0,1fr) auto;column-gap:8px;align-items:center;font-size:12.5px;line-height:1.3}
.xc-lv{display:flex;flex-direction:column;align-items:flex-end;gap:2px}
.xc-lamp i{width:12px;height:12px;border-radius:50%;border:2px solid var(--off)}
.xc-lamp b{font-size:12px;text-align:right;white-space:nowrap}.xc-lamp.xc-unknown b{display:none}
.xc-lamp.xc-met i{background:var(--green);border-color:var(--green);box-shadow:0 0 0 3px rgba(47,107,79,.2)}
.xc-lamp.xc-unknown i{border-style:dashed;border-color:var(--amber)}.xc-lamp.xc-not b{color:var(--muted);font-weight:500}
.xc-note{font-size:12px;font-style:italic;color:var(--muted);margin:0 8px}
.xc-sz{background:var(--board);border:1.5px solid var(--ink);border-radius:14px;padding:12px 14px;display:flex;flex-direction:column;gap:10px}
.xc-szbar{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.xc-sl{display:flex;align-items:center;gap:10px;flex:1 1 260px;font-size:12.5px;font-weight:600;color:var(--muted)}.xc-sl b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:26px;color:var(--ink);vertical-align:-3px}
.xc-range{flex:1;accent-color:var(--plum);min-height:30px;min-width:120px}
.xc-day{position:relative;padding-top:18px}
.xc-ticks{position:relative;height:0}.xc-ticks span{position:absolute;top:-18px;transform:translateX(-50%);font-size:10.5px;color:var(--muted);white-space:nowrap}
.xc-ticks span:first-child{transform:none}.xc-ticks span:last-child{transform:translateX(-100%)}
.xc-wins{position:relative;height:38px;background:var(--wash);border-radius:6px}
.xc-win{position:absolute;top:0;bottom:0;left:var(--a);width:calc(var(--b) - var(--a));background:rgba(109,74,119,.18);border:1.5px solid var(--plum);border-radius:6px;padding:2px 6px;display:flex;flex-direction:column;justify-content:center;overflow:hidden}
.xc-win b{font-size:11px;line-height:1.1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.xc-win span{font-size:10.5px;color:var(--muted);white-space:nowrap}
.xc-people{display:flex;flex-direction:column;gap:4px;margin-top:6px}
.xc-p{position:relative;height:24px}.xc-p span{position:absolute;top:0;bottom:0;left:var(--a);width:calc(var(--b) - var(--a));background:var(--plum);color:#fff;border-radius:12px;font-size:11px;font-weight:600;padding:0 10px;display:flex;align-items:center;white-space:nowrap;overflow:hidden}
.xc-flat span{background:repeating-linear-gradient(90deg,#8E6A98 0 10px,#A688AE 10px 20px)}
.xc-read{display:grid;grid-template-columns:auto minmax(0,1fr);gap:16px;align-items:center}.xc-read > div{display:flex;flex-direction:column}
.xc-count{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:34px;line-height:1}.xc-why{font-size:13px;line-height:1.45}
.xc-sz.is-recheck .xc-why{color:var(--amber);font-weight:600}.xc-sz.is-recheck .xc-p span{background:transparent;border:1.5px dashed var(--amber);color:var(--amber)}
.xc-total{display:flex;align-items:baseline;gap:10px;border-top:1.5px solid var(--ink);padding-top:8px}.xc-cost-t{font-size:16px}
.xc-others{font-size:12.5px;font-style:italic;color:var(--muted)}
/* ---- readouts ---- */
.xr-bar{display:flex;gap:10px;flex-wrap:wrap;justify-content:space-between}
.xr-key{display:flex;gap:18px;font-size:12px;color:var(--muted);flex-wrap:wrap}.xr-key span{display:flex;align-items:center;gap:6px}
.xr-key i{width:22px;height:12px;border-radius:3px}.xr-key .k-c{background:var(--ink)}.xr-key .k-n{border:1.5px dashed var(--amber)}
.xr-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.xr-grid > li{display:flex;flex-direction:column;min-width:0}
.sx .xr{width:100%;height:100%;display:flex;flex-direction:column;gap:6px;text-align:left;padding:9px 10px;background:var(--board);border:1.5px solid var(--ink);border-radius:12px;font:inherit;color:var(--ink);transition:opacity .2s}
.xr-n{font-size:12.5px;font-weight:600;line-height:1.25;min-height:31px}
.xr-w{display:flex;align-items:center;min-height:42px;padding:6px 10px;background:var(--ink);border-radius:7px;box-shadow:inset 0 0 0 2px #4A3A52,inset 0 8px 14px rgba(0,0,0,.35)}
.xr-v{font-family:'Bebas Neue',sans-serif;font-size:25px;line-height:1;color:#F3EEF5;letter-spacing:.02em}
.xr-end{display:none;font-family:'Poppins',sans-serif;font-size:12.5px;font-weight:600;color:var(--plum-l)}
.xr-sec[data-view=end] .xr-now{display:none}.xr-sec[data-view=end] .xr-end{display:inline}
.xr-sec[data-view=end] .xr-w{background:transparent;box-shadow:none;border:1.5px dashed var(--plum)}.xr-sec[data-view=end] .xr-end{color:var(--plum)}
.xr-new .xr-w{background:transparent;box-shadow:none;border:1.5px dashed var(--amber)}.xr-new .xr-now{font-family:'Poppins',sans-serif;font-size:12.5px;font-weight:600;color:var(--amber)}
.xr .xh-src{align-self:flex-start}.xr.is-dim{opacity:.28}
.xr-grid > li.bx{grid-column:1/-1}
/* ---- loop ---- */
.xl-grid{display:grid;grid-template-columns:320px minmax(0,1fr);gap:24px;align-items:start}
.xl-wheel{position:relative;width:320px;height:320px}.xl-wheel svg{position:absolute;inset:0;width:100%;height:100%}
.xl-ring{fill:none;stroke:var(--pxline);stroke-width:14}
.xl-arc{fill:none;stroke:var(--off);stroke-width:3;transition:stroke .3s}.xl-arc.is-done{stroke:var(--plum)}.xl-ahp{fill:var(--plum)}
.sx .xl-node{position:absolute;transform:translate(-50%,-50%);width:92px;display:flex;flex-direction:column;align-items:center;gap:3px;background:none;border:0;padding:4px;font:inherit;color:var(--ink)}
.sx .xl-node.tl-pick.is-up{transform:translate(-50%,calc(-50% - 5px))}
.xl-node b{width:40px;height:40px;border-radius:50%;background:var(--board);border:2.5px solid var(--ink);display:flex;align-items:center;justify-content:center;font-size:15px;transition:background .3s}
.xl-node span{font-size:11.5px;font-weight:600;line-height:1.2;text-align:center;border-radius:6px;padding:0 3px}
.xl-node.is-done b{background:var(--ink);color:#fff}.xl-node.is-up b{background:var(--gold);color:var(--ink)}
.xl-mid{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:150px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:2px}
.xl-round{font-size:12px;font-weight:600;color:var(--plum)}.xl-now{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:28px;line-height:1}.xl-sub{font-size:12px;color:var(--muted)}
.xl.is-back .xl-mid{animation:xl-back .6s ease-out}
@keyframes xl-back{0%{transform:translate(-50%,-50%) rotate(0)}40%{transform:translate(-50%,-50%) rotate(-8deg)}100%{transform:translate(-50%,-50%) rotate(0)}}
.xl-side{display:flex;flex-direction:column;gap:10px;min-width:0}.xl-bar{display:flex;gap:8px}
.xl-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.sx .xl-row{width:100%;display:grid;grid-template-columns:28px minmax(0,1fr) auto;gap:10px;align-items:center;padding:8px 10px;text-align:left;border:1.5px solid var(--ink);border-radius:10px;background:var(--board);font:inherit;color:var(--ink)}
.xl-row b{width:26px;height:26px;border-radius:50%;border:2px solid var(--ink);display:flex;align-items:center;justify-content:center;font-size:12px}
.xl-row.is-done b{background:var(--ink);color:#fff}.xl-row span{font-size:13.5px;font-weight:600}.xl-row em{font-style:normal;font-size:11.5px;color:var(--muted);text-align:right}
.xl-gate{display:flex;flex-direction:column;gap:8px;border-top:1.5px dashed var(--amber);padding-top:10px;margin-top:6px}.xl-gate b{font-size:14px;color:var(--amber)}.xl-gate div{display:flex;gap:8px;flex-wrap:wrap}
.sx .xl-yes{background:var(--green);border-color:var(--green);color:#fff}
/* ---- timesheet ---- */
.xm-sheet{background:var(--board);border:1.5px solid var(--ink);border-radius:6px;padding:14px 16px 16px;box-shadow:6px 6px 0 rgba(42,30,48,.12);
  background-image:linear-gradient(var(--pxline) 1px,transparent 1px);background-size:100% 30px}
.xm-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;border-bottom:2px solid var(--ink);padding-bottom:6px;margin-bottom:24px}
.xm-paper{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--plum)}.xm-day{font-family:'Bebas Neue',sans-serif;font-size:24px;line-height:1}
.xm-line{list-style:none;margin:0;padding:20px 0 0;position:relative;display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr))}
.xm-line::before{content:"";position:absolute;left:4%;right:4%;top:43px;border-top:4px dotted var(--ink);opacity:.6}
.xm-cell{position:relative;display:flex;flex-direction:column;min-width:0}
.xm-stop{position:relative;display:flex;flex-direction:column;align-items:center;gap:6px;padding:4px 4px 10px;border-radius:10px;text-align:center;cursor:pointer}
.xm-dot{position:relative;z-index:1;width:34px;height:34px;border-radius:50%;background:var(--board);border:3.5px solid var(--ink);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.xm-name{font-size:12.5px;line-height:1.25}.xm-f{font-size:10.5px;color:var(--muted)}
.xm-stop[data-state="outcome"] .xm-dot{border-color:var(--red);color:var(--red)}
.sx .xm .tl-inline{width:100%;max-width:96px;min-height:38px;text-align:center;font:inherit;font-size:13px;font-weight:600;border:2px dashed var(--plum);border-radius:6px;background:#fff;color:var(--ink);padding:0 4px}
.sx .xm .tl-inline.is-filled{border-style:solid;border-color:var(--green)}
.xm-val{display:inline-flex;align-items:center;justify-content:center;min-height:38px;min-width:76px;padding:0 8px;border:2px solid var(--ink);border-radius:6px;background:#fff;font-family:'Bebas Neue',sans-serif;font-size:22px;line-height:1}
.xm-stop[data-state="target"] .xm-val{border-color:var(--amber);color:var(--amber)}.xm-stop[data-state="outcome"] .xm-val{border-color:var(--red);color:var(--red)}
.xm-gap{position:absolute;left:0;top:-18px;transform:translateX(-50%);z-index:2;font-size:10.5px;font-weight:700;color:var(--plum);background:var(--board);padding:1px 5px;border-radius:8px;white-space:nowrap}
.xm-count{margin:12px 0 0;display:flex;align-items:baseline;gap:8px}.xm-count b{font-size:14px;color:var(--amber)}.xm-count b.is-done{color:var(--green)}
/* ---- night lanes ---- */
.xn-bar0{display:flex;align-items:center;gap:16px;flex-wrap:wrap}.xn-cap{flex:1 1 280px;margin:0;font-size:13px;color:var(--muted);line-height:1.45}
.xn[data-state=today] .xn-c-with,.xn[data-state=with] .xn-c-today{display:none}
.xn-board{background:var(--board);border:1.5px solid var(--ink);border-radius:14px;padding:12px 14px 14px;box-shadow:0 6px 0 rgba(42,30,48,.12)}
.xn-axis,.xn-lane,.xn-bands{display:grid;grid-template-columns:180px minmax(0,1fr);column-gap:14px;align-items:center}
.xn-ticks{position:relative;height:20px}.xn-ticks span{position:absolute;transform:translateX(-50%);font-size:10.5px;color:var(--muted);white-space:nowrap}
.xn-ticks span:first-child{transform:none}.xn-ticks span:last-child{transform:translateX(-100%)}
.xn-lanes{list-style:none;margin:0;padding:0;position:relative;display:flex;flex-direction:column;gap:6px}
.xn-bands{position:absolute;inset:0;pointer-events:none}.xn-bands .xn-track{height:100%;background:none;border:0}
.xn-night{position:absolute;top:0;bottom:0;background:repeating-linear-gradient(135deg,rgba(42,30,48,.07) 0 6px,transparent 6px 12px);border-left:1.5px dashed var(--off);border-right:1.5px dashed var(--off)}
.xn-night em{position:absolute;top:2px;left:50%;transform:translateX(-50%);white-space:nowrap;font-style:normal;font-size:10.5px;font-weight:600;color:var(--muted)}
.xn-lane{padding:4px 0;border-bottom:1px solid var(--pxline)}.xn-lane:last-child{border-bottom:0}
.sx .xn-name{display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:6px 8px;text-align:left;border:0;border-radius:8px;background:transparent;font:inherit;color:var(--ink)}
.xn-name b{font-size:13.5px;line-height:1.2}.xn-name em{font-style:normal;font-size:11.5px;color:var(--muted)}.xn-flag .xn-name b{color:var(--amber)}
.xn-track{position:relative;height:50px}
.xn-bands .xn-track i{position:absolute;top:0;bottom:0;border-left:1px dashed var(--pxline)}
.xn-bar{position:absolute;top:8px;height:14px;border-radius:7px;transition:opacity .3s}
.xn-lab{position:absolute;top:25px;font-size:11.5px;line-height:1.2;white-space:nowrap;color:var(--muted);transition:opacity .3s;background:var(--board);padding:1px 4px;border-radius:4px;z-index:1}.xn-lab b{color:var(--ink);font-weight:600}
.xn-today{background:#fff;border:2px solid var(--ink)}.xn-today[data-state="outcome"]{border-color:var(--red);background:#FBEDEA}.xn-today[data-state="target"]{border-color:var(--amber);background:#FBF2E4}
.xn-with{background:var(--plum)}.xn-with[data-state="start"]{background:var(--green)}
.xn-bar.xn-with,.xn-lab-with{opacity:0}
.xn[data-state=with] .xn-bar.xn-with,.xn[data-state=with] .xn-lab-with{opacity:1}.xn[data-state=with] .xn-today{opacity:.35;border-style:dashed}.xn[data-state=with] .xn-lab-today{opacity:0}
.xn-txs{display:none}.xn-lane > .bx{grid-column:1/-1}
/* ---- phone: one column, every pickable item stacked, each sheet under its item ---- */
@container sx (max-width:699px){
 .xh-with{grid-template-columns:minmax(0,1fr);gap:12px}.xh-board{min-width:0}.xh-title{font-size:44px}
 .xs-heads{display:none}.xs-row{grid-template-columns:minmax(0,1fr);row-gap:6px;padding:8px 0}
 .sx .xs-mag{grid-column:1}.sx .xs-row.is-moved .xs-mag{transform:none}
 .xt-top{grid-template-columns:minmax(0,1fr)}.xt-needs{grid-template-columns:minmax(0,1fr)}
 .xt-dots{grid-template-columns:repeat(7,minmax(0,1fr))}.xt-weeks{display:none}.xt-dots .xt-day:nth-child(8){box-shadow:none}
 .xt-bands{grid-template-columns:minmax(0,1fr)!important;gap:8px}.xt-cell{grid-column:1!important}
 .xb-board{grid-template-columns:minmax(0,1fr)!important}.xb-g{border-right:0;border-bottom:1.5px solid var(--pxline)}.xb-g:last-child{border-bottom:0}
 .xb-g ul{grid-template-columns:minmax(0,1fr)!important;gap:12px}
 .sx .xb-b{flex-direction:row;justify-content:flex-start;gap:10px;padding:12px 12px 10px;text-align:left}.xb-b .xb-n{text-align:left}.xb-clip{left:30px}
 .xc-roles{grid-template-columns:minmax(0,1fr)!important}.xc-top::after{left:10%;right:10%}
 .xc-read{grid-template-columns:minmax(0,1fr);gap:4px}.xc-win span{display:none}.xc-ticks span:nth-child(even){display:none}
 .xr-grid{grid-template-columns:minmax(0,1fr)!important}
 .xl-grid{grid-template-columns:minmax(0,1fr);justify-items:center}.xl-side{width:100%}
 .xl-wheel{width:280px;height:280px}.xl-node{display:none!important}
 .xm-line{grid-template-columns:minmax(0,1fr)!important;gap:4px;padding-top:0}
 .xm-line::before{left:17px;right:auto;top:6px;bottom:6px;border-top:0;border-left:4px dotted var(--ink)}
 .xm-stop{display:grid;grid-template-columns:34px minmax(0,1fr) auto;grid-template-rows:auto auto;column-gap:12px;row-gap:0;text-align:left;align-items:center;padding:8px 6px 8px 0}
 .xm-dot{grid-row:1/3}.xm-name{grid-column:2}.xm-f{grid-column:2;grid-row:2}.xm-stop .tl-inline,.xm-val{grid-column:3;grid-row:1/3}
 .xm-gap{position:static;transform:none;margin:0 0 4px 46px;align-self:flex-start;background:transparent}
 .xn-axis,.xn-track,.xn-bands{display:none!important}.xn-lane{grid-template-columns:minmax(0,1fr)}
 .xn-txs{display:flex;flex-direction:column;gap:4px;padding:0 8px 6px}
 .xn-tx{font-size:12.5px;line-height:1.35;padding:6px 8px;border-radius:8px;border:1.5px solid var(--ink);background:#fff}.xn-tx small{display:block;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
 .xn-tx-with{display:none;border-color:var(--plum);background:var(--wash)}.xn[data-state=with] .xn-tx-with{display:block}.xn[data-state=with] .xn-tx-today{opacity:.5}
}
'''
