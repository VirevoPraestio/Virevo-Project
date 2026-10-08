"""
bm_so_blocks2 — Bed Management Solutions drawings for turns bm-so-02 to bm-so-12 (drafts, 1 Oct 2026).

Same rules as bm_so_blocks: the library's Solutions motifs (lightbulb, jigsaw, maze, knots, route, drafting sheet,
door plates from the landing page) in the fit-out look, every drawing interactive, the common tool layer on every
pickable item (first raised with its sheet open; on a phone each sheet under its item, every item stacked).

  hub         what you provide -> one engine -> what comes out                  (bm-so-02)
  pair        two boxes read side by side, stacked on a phone                  (bm-so-02, 08, 11)
  foundation  what we bring above the ground line, what must be there below it (bm-so-03)
  doors       the five parts as doors off one corridor, the covered one ajar   (bm-so-04)
  day-switch  the day now against the day as it would run, on one clock       (bm-so-05)
  notes       a few drafting cards, each opening its sheet                     (bm-so-05, 07, 12)
  owners      two owners, peers, joined by a two-way arrow                     (bm-so-05)
  maze        the library maze, with the layer                                 (bm-so-06)
  rerun       try a change: the plan re-runs and the change is recorded        (bm-so-06)
  gap-knots   a chain whose waiting is in the gaps; an owner undoes the knots  (bm-so-07)
  people      six teams on a plan, and who signs it off                        (bm-so-08)
  sizing      the four roles and the two sizing chains, with a live slider     (bm-so-09)
  costing     what can be costed, and the numbers still needed                 (bm-so-09)
  gauges      eight measures as dials, six nobody reads today                  (bm-so-10)
  findings    the hospital's own facts, muted                                  (bm-so-11)
"""
import math, re
import bm_so_blocks as B
G = B.G
e, pt, pick, hint, desk, sheet = B.e, B.pt, B.pick, B.hint, B.desk, B.sheet

def register():
    return {'hub': r_hub, 'pair': r_pair, 'foundation': r_foundation, 'doors': r_doors, 'day-switch': r_day, 'notes': r_notes,
            'owners': r_owners, 'maze': r_maze, 'rerun': r_rerun, 'gap-knots': r_gapknots, 'people': r_people, 'sizing': r_sizing,
            'costing': r_costing, 'gauges': r_gauges, 'findings': r_findings}

def lab(t, cls=''): return '<div class="sx-label%s">%s</div>' % (' ' + cls if cls else '', e(t)) if t else ''
def cond(t): return '<p class="sx-cond so-cap">%s</p>' % e(t) if t else ''
def tagspan(t, cls='so-tg'): return '<span class="%s">%s</span>' % (cls, e(t)) if t else ''

# ------------------------------------------------------------------------------------------ hub
def r_hub(b, ctx):
    grp = ctx.uid('sohb'); ins, boxes = [], []
    for i, x in enumerate(b['inputs']):
        sh = b['sheets'][i]; first = i == 0
        ins.append('<li class="hb-i"><button type="button"%s data-feeds="%s"%s><span class="hb-k">%s</span><b>%s</b><em>%s</em></button><span class="hb-w" aria-hidden="true"></span></li>%s' % (
            pick(grp, sh['key'], first, 'hb-node'), ','.join(str(f) for f in x.get('feeds', [])), pt(x), e(x['kind']), e(x['title']), e(x['line']), sheet(sh, grp, first, 'mob-li')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    eng = b['engine']
    outs = ''.join('<li class="hb-o" data-o="%d"><span class="hb-on">%d</span><span>%s</span></li>' % (i + 1, i + 1, e(o)) for i, o in enumerate(b['outputs']))
    return ('<section class="sx-block so-hub" data-block="hub">%s<div class="hb-grid"><div class="hb-col hb-in">%s<ol class="hb-list">%s</ol></div>'
            '<div class="hb-core"><div class="hb-engine">%s<small>%s</small><b>%s</b><em>%s</em></div></div>'
            '<div class="hb-col hb-out">%s<ol class="hb-outs">%s</ol></div></div>%s%s</section>') % (
        hint(b.get('hint') or 'Pick something you provide. Its wire lights, and so does what it feeds.'), lab(b['in_label'], 'hb-lab'), ''.join(ins),
        G['so'].BULB.replace('class="sx-bulb"', 'class="sx-bulb hb-bulb"'), e(eng['label']), e(eng['title']), e(eng['line']), lab(b['out_label'], 'hb-lab'), outs,
        cond(b.get('caption')), desk(boxes))

# ------------------------------------------------------------------------------------------ pair
def r_pair(b, ctx):
    L = G['L']; boxes = []
    for x in b['items']:
        ask = L.say(x['ask']['label'], x['ask']['say'], 'so-ask') if x.get('ask') else ''
        boxes.append('<div class="pr-box" data-state="%s"%s>%s<div class="pr-v">%s</div><p>%s</p>%s</div>' % (
            e(x.get('state', 'plain')), pt(x), lab(x['label']), e(x['value']), e(x['sub']), ask))
    vs = '<span class="pr-vs" aria-hidden="true">%s</span>' % e(b['between']) if b.get('between') else '<span class="pr-gap" aria-hidden="true"></span>'
    return '<section class="sx-block so-pair" data-block="pair">%s<div class="pr-row">%s</div>%s</section>' % (lab(b.get('label')), vs.join(boxes), cond(b.get('caption')))

# ------------------------------------------------------------------------------------------ foundation
def r_foundation(b, ctx):
    grp = ctx.uid('sofd'); boxes = []; sh = iter(b['sheets']); k = [0]
    def items(lst, cls):
        out = []
        for x in lst:
            s = next(sh); first = k[0] == 0; k[0] += 1
            out.append('<li><button type="button"%s%s><b>%s</b><em>%s</em></button></li>%s' % (pick(grp, s['key'], first, 'fd-box ' + cls), pt(x), e(x['title']), e(x['line']), sheet(s, grp, first, 'mob-li')))
            boxes.append(sheet(s, grp, first, 'desk'))
        return ''.join(out)
    up, down = items(b['bring'], 'fd-up'), items(b['there'], 'fd-dn')
    sw = b['switch']
    return ('<section class="sx-block so-fd" data-block="foundation" data-dig="yes"><div class="fd-bar"><div class="ut-switch fd-switch" role="group" aria-label="%s">'
            '<button type="button" data-dig="yes" aria-pressed="true">%s</button><button type="button" data-dig="no" aria-pressed="false">%s</button></div>%s</div>'
            '<div class="fd-build"><svg class="fd-roof" viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true"><path d="M0 10 L50 0.6 L100 10"/></svg>%s<ol class="fd-floors">%s<li class="fd-extra" aria-hidden="true"><span>%s</span></li></ol>'
            '<div class="fd-ground"><span>%s</span></div>%s<ol class="fd-found">%s</ol></div>'
            '<p class="fd-read" aria-live="polite"><span class="fd-yes">%s</span><span class="fd-no">%s</span></p>%s</section>') % (
        e(sw['label']), e(sw['yes']), e(sw['no']), hint(b.get('hint') or 'Pick a box to open it. Then switch to see a hospital still on paper.'),
        lab(b['bring_label'], 'fd-lab'), up, e(sw['extra']), e(b['ground']), lab(b['there_label'], 'fd-lab fd-lab-dn'), down, e(sw['read_yes']), e(sw['read_no']), desk(boxes))

# ------------------------------------------------------------------------------------------ doors
def r_doors(b, ctx):
    grp = ctx.uid('sodr'); items, boxes = [], []
    for i, d in enumerate(b['doors']):
        s = b['sheets'][i]; first = i == (b.get('default', 1) - 1)
        st = d.get('state', 'closed')
        items.append(('<li class="dr-li"><button type="button"%s data-state="%s"%s><span class="dr-leaf" aria-hidden="true"></span><span class="dr-plate"><small>Part %d</small><b>%s</b></span>'
                      '<span class="dr-q">%s</span>%s<span class="dr-knob" aria-hidden="true"></span></button>%s</li>') % (
            pick(grp, s['key'], first, 'dr-door'), e(st), pt(d), d['n'], e(d['title']), e(d['question']), tagspan(d.get('tag'), 'dr-tag'), sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    return ('<section class="sx-block so-doors" data-block="doors">%s<ol class="dr-row" style="--n:%d">%s</ol><div class="dr-corr" aria-hidden="true"><span>%s</span></div>%s</section>') % (
        hint(b.get('hint') or 'Pick a door to see the question that part answers.'), len(b['doors']), ''.join(items), e(b['corridor']), desk(boxes))

# ------------------------------------------------------------------------------------------ day-switch
def _h(t):
    h, m = [int(x) for x in t.split(':')]; return h + m / 60.0

def _clk(t):
    h, m = [int(x) for x in t.split(':')]
    return 'noon' if (h, m) == (12, 0) else '%d%s %s' % (h % 12 or 12, (':%02d' % m) if m else '', 'AM' if h < 12 else 'PM')

def r_day(b, ctx):
    t0, t1 = _h(b['from']), _h(b['to']); span = t1 - t0
    X = lambda t: 100.0 * (_h(t) - t0) / span
    ticks = ''.join('<span class="dy-tick" style="left:%.2f%%">%s</span>' % (X('%d:00' % h), e(_clk('%d:00' % h))) for h in range(int(math.ceil(t0)), int(t1) + 1, 2))
    lanes = []
    for ln in b['lanes']:
        bars = ''
        for state in ('now', 'with'):
            for x in ln.get(state, []):
                bars += '<span class="dy-bar dy-%s" data-state="%s" style="left:%.2f%%;width:%.2f%%"><b>%s</b></span>' % (
                    state, e(x.get('state', 'plain')), X(x['from']), X(x['to']) - X(x['from']), e(x['label']))
        lanes.append('<div class="dy-lane"><div class="dy-name">%s</div><div class="dy-track">%s</div></div>' % (e(ln['name']), bars))
    sw = b['switch']
    return ('<section class="sx-block so-day" data-block="day-switch" data-state="now"><div class="dy-top"><div class="ut-switch dy-switch" role="group" aria-label="Which day">'
            '<button type="button" data-state="now" aria-pressed="true">%s</button><button type="button" data-state="with" aria-pressed="false">%s</button></div>'
            '<p class="dy-cap" aria-live="polite"><span class="dy-now">%s</span><span class="dy-with">%s</span></p></div>'
            '<div class="dy-board"><div class="dy-axis">%s</div>%s</div>%s</section>') % (
        e(sw['now']), e(sw['with']), e(sw['cap_now']), e(sw['cap_with']), ticks, ''.join(lanes), cond(b.get('caption')))

# ------------------------------------------------------------------------------------------ notes
def r_notes(b, ctx):
    grp = ctx.uid('sont'); items, boxes = [], []
    for i, x in enumerate(b['items']):
        s = b['sheets'][i]; first = i == 0
        items.append('<li class="nt-li"><button type="button"%s data-state="%s"%s><span class="nt-pin" aria-hidden="true"></span>%s<b>%s</b><em>%s</em></button>%s</li>' % (
            pick(grp, s['key'], first, 'nt-card'), e(x.get('state', 'plain')), pt(x), tagspan(x.get('tag')), e(x['title']), e(x['text']), sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    n = len(b['items'])
    return '<section class="sx-block so-notes" data-block="notes">%s<ol class="nt-row" style="--c:%d">%s</ol>%s%s</section>' % (
        lab(b.get('label')), 4 if n == 4 else min(n, 3), ''.join(items), cond(b.get('caption')), desk(boxes))

# ------------------------------------------------------------------------------------------ owners
def r_owners(b, ctx):
    grp = ctx.uid('soow'); items, boxes = [], []
    for i, x in enumerate(b['owners']):
        s = b['sheets'][i]; first = i == 0
        items.append('<div class="ow-li"><button type="button"%s%s>%s<b>%s</b><em>%s</em></button>%s</div>' % (
            pick(grp, s['key'], first, 'ow-card'), pt(x), tagspan(x.get('tag'), 'so-tg so-tg-new'), e(x['title']), e(x['line']), sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    arrow = '<div class="ow-arrow" aria-hidden="true"><span></span><small>%s</small></div>' % e(b['link'])
    return '<section class="sx-block so-own" data-block="owners">%s<div class="ow-row">%s</div><p class="ow-say">%s</p>%s</section>' % (
        lab(b.get('label')), arrow.join(items), e(b['line']), desk(boxes))

# ------------------------------------------------------------------------------------------ maze (library, layered)
def r_maze(b, ctx):
    grp = ctx.uid('somz'); so = G['so']
    lib = so.r_maze({'routes': [dict(r) for r in b['routes']], 'start': b['start'], 'goal': b['goal']})
    board = lib[lib.index('<div class="mz-board">'):lib.index('<div class="mz-side">')]
    dead = [r for r in b['routes'] if r['kind'] == 'dead']; order = dead + [r for r in b['routes'] if r['kind'] == 'way']
    items, boxes = [], []
    first_i = len(order) - 1
    for k, r in enumerate(order):
        s = b['sheets'][b['routes'].index(r)]; n = k + 1; way = r['kind'] == 'way'; first = k == first_i
        items.append('<li><button type="button"%s data-route="%d"%s><span class="mz-n">%s</span><span><small>%s</small><b>%s</b></span></button></li>%s' % (
            pick(grp, s['key'], first, 'mz-r' + (' mz-r-way' if way else '')), n, pt(r), '' if way else str(n), 'The way through' if way else 'Ruled out', e(r['name']), sheet(s, grp, first, 'mob-li')))
        boxes.append(sheet(s, grp, first, 'desk'))
    return ('<section class="sx-block sx-maze so-maze" data-block="maze" data-sel="%d" data-way="on"><div class="mz-top">%s<div class="mz-side">%s<ol class="mz-list">%s</ol></div></div>%s</section>') % (
        first_i + 1, board, hint(b.get('hint') or 'Pick a route to follow it through the maze.'), ''.join(items), desk(boxes))

# ------------------------------------------------------------------------------------------ rerun
def r_rerun(b, ctx):
    grp = ctx.uid('sorr'); tries, boxes = [], []
    for i, x in enumerate(b['tries']):
        s = b['sheets'][i]; first = i == 0
        tries.append('<li><button type="button"%s%s><span class="rr-bolt" aria-hidden="true"></span><b>%s</b></button>%s</li>' % (
            pick(grp, s['key'], first, 'rr-try'), pt(x), e(x['title']), sheet(s, grp, first, 'mob-li')))
        boxes.append(sheet(s, grp, first, 'desk'))
    n = len(b['loop'])
    loop = ''.join('<li class="rr-s" data-state="%s" style="--i:%d"><span class="rr-n">%d</span><b>%s</b><em>%s</em></li>' % (
        e(x.get('state', 'outcome' if i == n - 1 else 'plain')), i, i + 1, e(x['title']), e(x.get('line', ''))) for i, x in enumerate(b['loop']))
    return ('<section class="sx-block so-rr" data-block="rerun" data-run="0"><div class="rr-grid"><div class="rr-side">%s<ol class="rr-tries">%s</ol></div>'
            '<div class="rr-main">%s<ol class="rr-loop" style="--n:%d">%s</ol></div></div>%s</section>') % (
        lab(b['tries_label']), ''.join(tries), lab(b['loop_label']), n, loop, desk(boxes))

# ------------------------------------------------------------------------------------------ gap-knots
def r_gapknots(b, ctx):
    grp = ctx.uid('sogk'); so = G['so']; parts, boxes = [], []
    steps = b['steps']; n = len(steps)
    for i, s_ in enumerate(steps):
        last = i == n - 1
        parts.append('<li class="gk-step" data-state="%s"><span class="gk-sn">%d</span><b>%s</b><em>%s</em></li>' % ('outcome' if last else 'plain', i + 1, e(s_['title']), e(s_.get('line', ''))))
        if not last:
            s = b['sheets'][i]; first = i == 0; g = b['gaps'][i]
            parts.append('<li class="gk-gap"><button type="button"%s%s><span class="gk-rope">%s</span><span class="gk-gl"><small>Gap %d</small><b>%s</b></span></button></li>%s' % (
                pick(grp, s['key'], first, 'gk-g'), pt(g), so.KNOT_SVG, i + 1, e(g['title']), sheet(s, grp, first, 'mob-li')))
            boxes.append(sheet(s, grp, first, 'desk'))
    sw = b['switch']
    return ('<section class="sx-block so-gk" data-block="gap-knots" data-state="today"><div class="dy-top"><div class="ut-switch gk-switch" role="group" aria-label="Which picture">'
            '<button type="button" data-state="today" aria-pressed="true">%s</button><button type="button" data-state="owner" aria-pressed="false">%s</button></div>'
            '<p class="dy-cap" aria-live="polite"><span class="gk-today">%s</span><span class="gk-owner">%s</span></p></div>%s<ol class="gk-chain">%s</ol>%s%s</section>') % (
        e(sw['today']), e(sw['owner']), e(sw['cap_today']), e(sw['cap_owner']), hint(b.get('hint') or 'Pick a gap to see who waits there.'), ''.join(parts), cond(b.get('caption')), desk(boxes))

# ------------------------------------------------------------------------------------------ people
def r_people(b, ctx):
    grp = ctx.uid('sopp'); rooms, boxes = [], []
    C = G['C']
    for i, x in enumerate(b['teams']):
        s = b['sheets'][i]; first = i == 0
        rooms.append('<li class="pp-li"><button type="button"%s data-state="%s"%s><span class="pp-door" aria-hidden="true"></span><b>%s</b><em>%s</em>%s</button>%s</li>' % (
            pick(grp, s['key'], first, 'pp-room'), 'target' if x.get('resist') else 'plain', pt(x), e(x['title']), e(x['gets']),
            tagspan(b['resist_tag'], 'so-tg so-tg-amber') if x.get('resist') else '', sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    a = b['approver']
    mg = ''.join('<div class="pp-mg">%s<b>%s</b><em>%s</em></div>' % (tagspan(m.get('tag'), 'so-tg so-tg-new'), e(m['title']), e(m['line'])) for m in b['managers'])
    return ('<section class="sx-block so-ppl" data-block="people">%s%s<ol class="pp-plan">%s</ol><div class="pp-tree"><div class="pp-top"><span class="so-tg pp-sign">%s</span><b>%s</b><em>%s</em></div>'
            '<div class="pp-lines" aria-hidden="true"></div><div class="pp-split">%s</div><p class="pp-note">%s</p></div>%s</section>') % (
        hint(b.get('hint') or 'Pick a team to see what changes for them.'), lab(b['teams_label']), ''.join(rooms), e(a['tag']), e(a['title']), e(a['line']), mg, e(b['tree_note']), desk(boxes))

# ------------------------------------------------------------------------------------------ sizing
def r_sizing(b, ctx):
    grp = ctx.uid('sosz'); L = G['L']; roles, boxes = [], []
    for i, x in enumerate(b['roles']):
        s = b['sheets'][i]; first = i == 0
        roles.append('<li><button type="button"%s data-state="%s"%s>%s<b>%s</b><em>%s</em></button>%s</li>' % (
            pick(grp, s['key'], first, 'sz-role'), 'target' if x.get('new') else 'plain', pt(x), tagspan(b['new_tag'], 'so-tg so-tg-new') if x.get('new') else tagspan(x.get('tag'), 'so-tg'),
            e(x['title']), e(x['line']), sheet(s, grp, first, 'mob-li')))
        boxes.append(sheet(s, grp, first, 'desk'))
    chains = []
    for c in b['chains']:
        steps = []
        for j, st in enumerate(c['steps']):
            inner = '<b>%s</b><em>%s</em>' % (e(st['title']), e(st.get('line', '')))
            if st.get('slider'):
                sl = st['slider']; cid = ctx.uid('szr')
                inner += ('<label class="sz-sl" for="%s">%s</label><input id="%s" class="sz-range" type="range" min="%d" max="%d" step="1" value="%d" data-per="%d">'
                          '<span class="sz-out" aria-live="polite"><span class="sz-a">%d</span> arrivals, so <b class="sz-v">%d</b> %s <i class="sx-src sx-src-estimate">%s</i></span>') % (
                    cid, e(sl['label']), cid, sl['min'], sl['max'], sl['value'], sl['per'], sl['value'], -(-sl['value'] // sl['per']), e(sl['unit']), e(sl['source']))
            if st.get('ask'):
                inner += L.inline(st['ask']['label'], st['ask']['hint'], grp + '-in')
            if st.get('result'):
                inner += '<span class="sz-res">%s</span>' % e(st['result'])
            steps.append('<li class="sz-st" data-state="%s">%s</li>' % (e(st.get('state', 'plain')), inner))
        chains.append('<div class="sz-chain" data-state="%s"><div class="sz-ch-h">%s<span class="so-tg sz-verdict">%s</span></div><ol>%s</ol></div>' % (
            e(c['state']), lab(c['title']), e(c['verdict']), '<li class="sz-ar" aria-hidden="true"></li>'.join(steps)))
    return ('<section class="sx-block so-sz" data-block="sizing">%s%s<ol class="sz-roles">%s</ol>%s<div class="sz-chains">%s</div>%s%s</section>') % (
        hint(b.get('hint') or 'Pick a role to open it. Move the slider to see the number of staff change.'), lab(b['roles_label']), ''.join(roles), desk(boxes),
        ''.join(chains), cond(b.get('caption')), '')

# ------------------------------------------------------------------------------------------ costing
def r_costing(b, ctx):
    L = G['L']; grp = ctx.uid('soco') + '-in'
    lines = ''.join('<li><span>%s</span><b>%s</b></li>' % (e(x['label']), e(x['value'])) for x in b['lines'])
    needs = ''.join('<li><span class="co-q">%s</span>%s</li>' % (e(x['label']), L.inline(x['label'], x['hint'], grp)) for x in b['needed'])
    return ('<section class="sx-block so-co" data-block="costing"><div class="co-grid"><div class="co-cost">%s<div class="co-v">%s</div><ul class="co-lines">%s</ul><p class="co-note">%s</p></div>'
            '<div class="co-need"><div class="co-nh">%s<span class="co-count" data-count-for="%s" data-done="All in. I can redo the cost as a difference." data-waiting="None in yet">None in yet</span></div>'
            '<ol class="co-list">%s</ol></div></div></section>') % (
        lab(b['cost_label']), e(b['cost']), lines, e(b['note']), lab(b['needed_label']), grp, needs)

# ------------------------------------------------------------------------------------------ gauges
def _dial(v):
    R = 34; cx, cy = 42, 42
    arc = 'M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (cx - R, cy, R, R, cx + R, cy)
    needle = ''
    if v is not None:
        a = math.pi * (1 - v); x, y = cx + (R - 8) * math.cos(a), cy - (R - 8) * math.sin(a)
        needle = '<path class="gg-nd" d="M%d %d L%.1f %.1f"/><circle class="gg-hub" cx="%d" cy="%d" r="4"/>' % (cx, cy, x, y, cx, cy)
    else:
        needle = '<text class="gg-qm" x="%d" y="%d">?</text>' % (cx, cy - 4)
    ticks = ''.join('<path class="gg-tk" d="M%.1f %.1f L%.1f %.1f"/>' % (cx + R * math.cos(math.pi * k / 4), cy - R * math.sin(math.pi * k / 4), cx + (R - 6) * math.cos(math.pi * k / 4), cy - (R - 6) * math.sin(math.pi * k / 4)) for k in range(5))
    return '<svg class="gg-dial" viewBox="0 0 84 50" aria-hidden="true"><path class="gg-arc" d="%s"/>%s%s</svg>' % (arc, ticks, needle)

def r_gauges(b, ctx):
    grp = ctx.uid('sogg'); dials, boxes = [], []
    for i, x in enumerate(b['measures']):
        s = b['sheets'][i]; first = i == 0
        new = x.get('new', False)
        dials.append('<li class="gg-li" data-kind="%s"><button type="button"%s data-new="%s"%s>%s<span class="gg-tx">%s<b>%s</b><em>%s</em></span></button>%s</li>' % (
            e(x['kind']), pick(grp, s['key'], first, 'gg-card'), 'yes' if new else 'no', pt(x), _dial(x.get('needle')),
            tagspan(b['new_tag'] if new else b['tracked_tag'], 'so-tg so-tg-amber' if new else 'so-tg'), e(x['title']), e(x['reading']), sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    f = b['filters']
    btns = ''.join('<button type="button" data-f="%s" aria-pressed="%s">%s</button>' % (k, 'true' if k == 'all' else 'false', e(v)) for k, v in (('all', f['all']), ('lead', f['lead']), ('result', f['result'])))
    return ('<section class="sx-block so-gg" data-block="gauges" data-f="all"><div class="dy-top"><div class="ut-switch gg-switch" role="group" aria-label="Which measures">%s</div><p class="dy-cap">%s</p></div>'
            '<ol class="gg-grid">%s</ol>%s%s</section>') % (btns, e(b['key_line']), ''.join(dials), cond(b.get('caption')), desk(boxes))

# ------------------------------------------------------------------------------------------ findings
def r_findings(b, ctx):
    grp = ctx.uid('sofi'); items, boxes = [], []
    for i, x in enumerate(b['items']):
        s = b['sheets'][i]; first = i == 0
        items.append('<li><button type="button"%s%s><small>%s</small><b>%s</b><em>%s</em></button>%s</li>' % (
            pick(grp, s['key'], first, 'fi-card'), pt(x), e(x['tag']), e(x['value']), e(x['line']), sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    return '<section class="sx-block so-fi" data-block="findings">%s<ol class="fi-row">%s</ol>%s%s</section>' % (lab(b['label']), ''.join(items), cond(b.get('caption')), desk(boxes))

# ------------------------------------------------------------------------------------------ the three buttons, on every turn (06 §11.2 point 5)
def actions(a):
    btn = lambda k, head, d: '<button type="button" class="so-act so-act-%s" data-say-lead data-text="%s"><span class="so-act-k">%s</span><span class="so-act-d">%s</span></button>' % (
        k, e(d['say']), e(head), e(d['detail']))
    return '<nav class="so-acts" aria-label="What to do next">%s%s%s</nav>' % (
        btn('go', 'Proceed with next step', a['go']), btn('add', 'Add more', a['add']), btn('jump', 'Jump to ' + a['jump']['tab'], a['jump']))

JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  function sw(root,attr,sel){$$(sel+' button',root).forEach(function(b){b.addEventListener('click',function(){root.setAttribute(attr,b.getAttribute(attr));
    $$(sel+' button',root).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});});});}
  /* hub: the picked input lights its wire, the engine and what it feeds */
  $$('.so-hub').forEach(function(h){function on(b){var f=(b.getAttribute('data-feeds')||'').split(',');
      $$('.hb-o',h).forEach(function(o){o.classList.toggle('is-fed',f.indexOf(o.getAttribute('data-o'))>=0);});}
    $$('.hb-node',h).forEach(function(b){b.addEventListener('click',function(){on(b);});});var up=h.querySelector('.hb-node.is-up');if(up)on(up);});
  $$('.so-fd').forEach(function(f){sw(f,'data-dig','.fd-switch');});
  $$('.so-day').forEach(function(d){sw(d,'data-state','.dy-switch');});
  $$('.so-gk').forEach(function(d){sw(d,'data-state','.gk-switch');});
  $$('.so-gg').forEach(function(d){sw(d,'data-f','.gg-switch');});
  /* maze: the picked route walks its trail; the bulb lights on the way through */
  $$('.so-maze').forEach(function(m){function go(b){var n=b.getAttribute('data-route');m.setAttribute('data-sel',n);m.setAttribute('data-way',b.classList.contains('mz-r-way')?'on':'off');
      $$('.mz-trail,.mz-pin',m).forEach(function(t){t.classList.toggle('is-sel',t.getAttribute('data-route')===n);});}
    $$('.mz-r',m).forEach(function(b){b.addEventListener('click',function(){go(b);});});var up=m.querySelector('.mz-r.is-up');if(up)go(up);});
  /* rerun: each change runs the loop again */
  $$('.so-rr').forEach(function(r){$$('.rr-try',r).forEach(function(b){b.addEventListener('click',function(){r.classList.remove('is-run');void r.offsetWidth;r.classList.add('is-run');});});
    setTimeout(function(){r.classList.add('is-run');},400);});
  /* sizing: the busiest hour sets the headcount */
  $$('.so-sz .sz-range').forEach(function(s){var out=s.parentNode.querySelector('.sz-v'),per=+s.getAttribute('data-per');
    var a=s.parentNode.querySelector('.sz-a');function upd(){out.textContent=Math.ceil(+s.value/per);if(a)a.textContent=s.value;}s.addEventListener('input',upd);upd();});
})();
'''

CSS = r'''
/* switches keep the library look */
.sx .ut-switch button[aria-pressed="true"]{color:var(--sheet)!important}
/* tags */
.so-tg{display:inline-flex;align-self:flex-start;font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:2px 8px;border:1.5px solid var(--ink);border-radius:10px;line-height:1.3}
.so-tg-new,.so-tg-amber{border-color:var(--amber);color:var(--amber);background:#FBF1D2}
.so-cap{border-top:1.5px dashed var(--faint);padding-top:10px;font-style:italic;color:var(--muted);font-size:13px}
.sx .so-hub ol,.sx .so-fd ol,.sx .so-doors ol,.sx .so-notes ol,.sx .so-rr ol,.sx .so-gk ol,.sx .so-ppl ol,.sx .so-sz ol,.sx .so-co ol,.sx .so-gg ol,.sx .so-fi ol{list-style:none;margin:0;padding:0}
.so-hub,.so-fd,.so-doors,.so-day,.so-notes,.so-own,.so-rr,.so-gk,.so-ppl,.so-sz,.so-co,.so-gg,.so-fi,.so-pair{display:flex;flex-direction:column;gap:14px}
.sx .so-hub button,.sx .so-fd button,.sx .so-doors button,.sx .so-notes button,.sx .so-own button,.sx .so-rr button,.sx .so-gk button,.sx .so-ppl button,.sx .so-sz button,.sx .so-gg button,.sx .so-fi button{font:inherit;color:var(--ink);text-align:left}
/* ---- the three buttons ---- */
.so-acts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:6px;padding-top:16px;border-top:1.5px solid var(--ink)}
.sx .so-act{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:3px;min-height:64px;padding:10px 16px;text-align:left;font:inherit;color:var(--ink);background:var(--sheet);border:1.5px solid var(--ink);border-radius:4px;cursor:pointer}
.so-act-k{font-weight:600;font-size:15px}.so-act-d{font-size:12.5px;color:var(--muted);line-height:1.35}
.sx .so-act-go{background:var(--ink);color:var(--sheet);box-shadow:inset 6px 0 0 var(--gold);padding-left:22px}.sx .so-act-go .so-act-d{color:inherit;opacity:.85}
.so-act:hover{transform:translate(-1px,-1px);box-shadow:3px 3px 0 rgba(23,59,56,.18)}.so-act-go:hover{box-shadow:inset 6px 0 0 var(--gold),3px 3px 0 rgba(23,59,56,.25)}
.so-act.is-said{outline:3px solid var(--gold);outline-offset:2px}
/* ---- hub ---- */
.hb-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.8fr) minmax(0,1fr);column-gap:52px;align-items:center}
.hb-lab{margin-bottom:8px;letter-spacing:.04em;text-transform:uppercase;font-size:11.5px!important}
.hb-list{display:flex;flex-direction:column;gap:10px;position:relative}
.hb-in .hb-list::after{content:"";position:absolute;right:-27px;top:30px;bottom:30px;border-right:3px dashed var(--wire)}
.hb-i{position:relative}
.hb-node{width:100%;display:flex;flex-direction:column;gap:2px;padding:9px 12px;background:var(--sheet);border:2px solid var(--ink);border-radius:3px}
.hb-k{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--line)}
.hb-node b{font-size:14px;font-weight:600;line-height:1.3}.hb-node em{font-style:normal;font-size:12px;color:var(--muted);line-height:1.35}
.hb-w{position:absolute;left:100%;top:50%;width:27px;border-top:3px dashed var(--wire)}
.hb-i:has(.is-up) .hb-w{border-top-style:solid;border-color:var(--gold);filter:drop-shadow(0 0 3px rgba(212,169,79,.8))}
.hb-core{position:relative;display:flex;align-items:center}
.hb-core::before,.hb-core::after{content:"";position:absolute;top:50%;width:52px;border-top:3px solid var(--gold)}
.hb-core::before{right:100%}.hb-core::after{left:100%}
.hb-engine{width:100%;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;padding:18px 12px;background:#FBF1D2;border:2.5px solid var(--ink);box-shadow:0 0 0 6px rgba(212,169,79,.22),6px 6px 0 rgba(23,59,56,.12)}
.hb-engine small{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--gold-t)}
.hb-engine b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:28px;line-height:.95}.hb-engine em{font-style:normal;font-size:12.5px;line-height:1.4;color:var(--ink)}
.hb-bulb{width:42px;height:52px}
.hb-outs{display:flex;flex-direction:column;gap:7px;position:relative}
.hb-out .hb-outs::before{content:"";position:absolute;left:-26px;top:16px;bottom:16px;border-left:3px solid var(--gold)}
.hb-o{position:relative;display:flex;align-items:center;gap:8px;padding:6px 10px;border:2px solid var(--red);background:var(--sheet);font-size:13px;font-weight:600;line-height:1.3;transition:background .2s,box-shadow .2s}
.hb-o::before{content:"";position:absolute;right:100%;top:50%;width:24px;border-top:2px solid var(--gold)}
.hb-on{width:20px;height:20px;border-radius:50%;border:1.5px solid var(--red);color:var(--red);display:inline-flex;align-items:center;justify-content:center;font-size:11px;flex-shrink:0}
.hb-o.is-fed{background:#FBF1D2;box-shadow:0 0 0 3px rgba(212,169,79,.45)}
/* ---- pair ---- */
.pr-row{display:flex;align-items:stretch;gap:0}
.pr-box{flex:1 1 0;min-width:0;display:flex;flex-direction:column;gap:6px;padding:16px 18px;background:var(--sheet);border:2px solid var(--ink)}
.pr-box[data-state="target"]{border-color:var(--amber);background:#FDF8EA}.pr-box[data-state="outcome"]{border-color:var(--red)}.pr-box[data-state="start"]{border-color:var(--green)}
.pr-v{font-family:'Bebas Neue',sans-serif;font-size:36px;line-height:.95}
.pr-box[data-state="outcome"] .pr-v{color:var(--red)}.pr-box[data-state="target"] .pr-v{color:var(--amber)}.pr-box[data-state="start"] .pr-v{color:var(--green)}
.pr-box p{font-size:13.5px;line-height:1.45}.pr-box .tl-say{margin-top:auto;align-self:flex-start}
.pr-gap{width:16px;flex-shrink:0}
.pr-vs{align-self:center;flex-shrink:0;padding:0 12px;font-family:'Bebas Neue',sans-serif;font-size:22px;color:var(--muted)}
/* ---- foundation ---- */
.fd-bar,.dy-top{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.fd-build{position:relative;display:flex;flex-direction:column;gap:10px;padding:0 34px 0}
.fd-roof{display:block;width:calc(100% + 20px);height:38px;margin:0 -10px;overflow:visible}.fd-roof path{fill:var(--soft);stroke:var(--ink);stroke-width:2.5;vector-effect:non-scaling-stroke}
.fd-floors,.fd-found{display:grid;grid-template-columns:repeat(var(--c,3),minmax(0,1fr));gap:10px}
.fd-found{--c:2}
.fd-box{width:100%;height:100%;display:flex;flex-direction:column;gap:3px;padding:12px 14px;background:var(--sheet);border:2px solid var(--ink)}
.fd-box b{font-size:14.5px;font-weight:600;line-height:1.3}.fd-box em{font-style:normal;font-size:12.5px;line-height:1.4;color:var(--muted)}
.fd-dn{border-color:var(--amber);background:#FDF8EA}
.fd-extra{display:none;grid-column:1/-1;border:2px dashed var(--red);padding:10px 14px;font-size:13px;font-weight:600;color:var(--red);background:repeating-linear-gradient(135deg,rgba(142,47,28,.07) 0 6px,transparent 6px 12px)}
.fd-ground{position:relative;border-top:4px solid var(--ink);margin:6px -34px 0;padding-top:6px;text-align:center}
.fd-ground::after{content:"";position:absolute;left:0;right:0;top:4px;height:10px;background:repeating-linear-gradient(135deg,var(--ink) 0 2px,transparent 2px 9px);opacity:.35}
.fd-ground span{position:relative;z-index:1;background:var(--ground);padding:0 10px;font-size:11.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.fd-lab-dn{color:var(--amber)!important}
.fd-read{font-size:14px;line-height:1.45;padding:10px 14px;border-left:4px solid var(--gold);background:rgba(250,252,251,.7)}
.fd-no{display:none}
.so-fd[data-dig="no"] .fd-yes{display:none}.so-fd[data-dig="no"] .fd-no{display:inline;color:var(--red);font-weight:600}
.so-fd[data-dig="no"] .fd-extra{display:block}
.so-fd[data-dig="no"] .fd-dn{border-style:dashed;background:transparent}
.so-fd[data-dig="no"] .fd-read{border-left-color:var(--red)}
/* ---- doors ---- */
.dr-row{display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:16px;align-items:end}
.dr-li{display:flex;flex-direction:column;min-width:0}
.dr-door{position:relative;width:100%;min-height:250px;display:flex;flex-direction:column;gap:10px;padding:16px 14px 18px;background:var(--sheet);border:2.5px solid var(--ink);border-bottom-width:5px;border-radius:70px 70px 2px 2px}
.dr-leaf{position:absolute;inset:8px 8px 8px;border:1.5px solid var(--faint);border-radius:62px 62px 0 0;pointer-events:none}
.dr-plate{position:relative;margin:26px auto 0;display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 10px;border:1.5px solid var(--ink);background:var(--soft);text-align:center;width:88%}
.dr-plate small{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--line)}
.dr-plate b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:21px;line-height:.95}
.dr-q{position:relative;font-size:12.5px;line-height:1.4;color:var(--ink);padding:0 2px}
.dr-knob{position:relative;margin-top:auto;align-self:flex-end;margin-right:4px;width:10px;height:10px;border-radius:50%;background:var(--ink)}
.dr-tag{position:absolute;left:50%;transform:translateX(-50%);top:-12px;font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:var(--ink);color:var(--sheet);padding:2px 9px}
.dr-door[data-state="covered"]{background:#ECEFEC;border-color:var(--wire);color:var(--muted);transform:perspective(600px) rotateY(-9deg);transform-origin:left center}
.dr-door[data-state="covered"] .dr-plate{background:transparent;border-color:var(--wire)}
.dr-door[data-state="covered"].is-up{transform:perspective(600px) rotateY(-9deg) translateY(-5px)}
.dr-corr{position:relative;border-top:2px dashed var(--faint);margin-top:-2px;padding-top:8px}
.dr-corr span{font-size:11.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.so-doors .bx-mob{margin-top:10px}
/* ---- day-switch ---- */
.dy-cap{font-size:13px;font-weight:600;line-height:1.4;flex:1;min-width:200px}
.dy-with,.gk-owner{display:none}
.so-day[data-state="with"] .dy-now{display:none}.so-day[data-state="with"] .dy-with{display:inline}
.dy-board{position:relative;background:var(--sheet);border:1.5px solid var(--ink);padding:30px 18px 14px 150px}
.dy-axis{position:absolute;left:150px;right:18px;top:8px;height:16px}
.dy-tick{position:absolute;transform:translateX(-50%);font-size:11px;font-weight:600;color:var(--muted);white-space:nowrap}.dy-tick:first-child{transform:none}.dy-tick:last-child{transform:translateX(-100%)}
.dy-lane{position:relative;height:52px;border-top:1px dashed var(--faint)}
.dy-name{position:absolute;left:-136px;width:126px;top:50%;transform:translateY(-50%);font-size:13px;font-weight:600;line-height:1.25}
.dy-track{position:absolute;inset:0;background:repeating-linear-gradient(90deg,var(--grid) 0 1px,transparent 1px 8.333%)}
.dy-bar{position:absolute;top:10px;height:32px;display:flex;align-items:center;padding:0 8px;overflow:hidden;border:2px solid var(--ink);background:#E3E9E6;border-radius:3px;transition:opacity .35s}
.dy-bar b{font-size:11.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dy-bar[data-state="outcome"]{border-color:var(--red);background:repeating-linear-gradient(135deg,rgba(142,47,28,.14) 0 6px,transparent 6px 12px);color:var(--red)}
.dy-bar[data-state="start"]{border-color:var(--green);background:#E2EFE8;color:var(--green)}
.dy-bar[data-state="target"]{border-color:var(--amber);background:#FBF1D2}
.dy-now{opacity:1}.dy-with{opacity:0;pointer-events:none}
.dy-bar.dy-with{display:flex}
.so-day[data-state="with"] .dy-bar.dy-now{opacity:0}.so-day[data-state="with"] .dy-bar.dy-with{opacity:1}
.so-day[data-state="now"] .dy-bar.dy-now:not([data-state="outcome"]){filter:grayscale(.4)}
/* ---- notes ---- */
.nt-row{display:grid;grid-template-columns:repeat(var(--c),minmax(0,1fr));gap:12px}
.nt-li{display:flex;flex-direction:column;min-width:0}
.nt-card{position:relative;width:100%;height:100%;display:flex;flex-direction:column;gap:5px;padding:16px 14px 14px;background:var(--sheet);border:1.5px solid var(--ink);box-shadow:4px 4px 0 rgba(23,59,56,.10)}
.nt-pin{position:absolute;top:-7px;left:50%;width:13px;height:13px;margin-left:-6px;border-radius:50%;background:var(--gold);border:2px solid var(--ink)}
.nt-card b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:23px;line-height:.95}.nt-card em{font-style:normal;font-size:12.5px;line-height:1.4;color:var(--muted)}
.nt-card[data-state="target"]{border-color:var(--amber)}.nt-card[data-state="muted"]{background:#ECEFEC;border-color:var(--wire)}.nt-card[data-state="muted"] b{color:var(--muted)}
.so-notes .bx-mob{margin-top:10px}
/* ---- owners ---- */
.ow-row{display:flex;align-items:stretch}
.ow-li{flex:1 1 0;min-width:0;display:flex;flex-direction:column}
.ow-card{width:100%;height:100%;display:flex;flex-direction:column;gap:5px;padding:16px 16px;background:#FDF8EA;border:2.5px solid var(--amber)}
.ow-card b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:28px;line-height:.95}.ow-card em{font-style:normal;font-size:13px;line-height:1.4}
.ow-arrow{flex:0 0 120px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px}
.ow-arrow span{position:relative;width:100%;border-top:3px solid var(--amber)}
.ow-arrow span::before,.ow-arrow span::after{content:"";position:absolute;top:-8px;width:11px;height:11px;border-top:3px solid var(--amber);border-left:3px solid var(--amber)}
.ow-arrow span::before{left:0;transform:rotate(-45deg)}.ow-arrow span::after{right:0;transform:rotate(135deg)}
.ow-arrow small{font-size:11.5px;font-weight:600;color:var(--amber);text-align:center;line-height:1.3}
.ow-say{font-family:'Bebas Neue',sans-serif;font-size:24px;line-height:1.05;text-align:center;padding:8px 10px;border-top:1.5px dashed var(--faint);border-bottom:1.5px dashed var(--faint)}
/* ---- maze, layered ---- */
.so-maze .mz-r.tl-pick,.so-maze .mz-r.tl-pick.is-up{transform:none}
.so-maze .mz-list li.bx{margin:6px 0 10px}
/* ---- rerun ---- */
.rr-grid{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,2fr);gap:22px;align-items:start}
.rr-tries{display:flex;flex-direction:column;gap:10px;margin-top:14px}
.rr-try{width:100%;display:flex;align-items:center;gap:10px;padding:10px 12px;background:var(--sheet);border:2px solid var(--ink);border-radius:22px}
.rr-try b{font-size:13.5px;font-weight:600;line-height:1.3}
.rr-bolt{width:14px;height:18px;flex-shrink:0;background:linear-gradient(var(--gold),var(--gold));clip-path:polygon(60% 0,0 58%,45% 58%,30% 100%,100% 38%,55% 38%)}
.rr-loop{position:relative;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:30px 46px;margin-top:6px;padding:4px}
.rr-loop::before{content:"";position:absolute;inset:34px 22% 34px 22%;border:3px dashed var(--wire);border-radius:30px}
.rr-s{position:relative;z-index:1;display:flex;flex-direction:column;gap:4px;padding:12px 14px;background:var(--sheet);border:2px solid var(--ink)}
.rr-s:nth-child(3){grid-column:2;grid-row:2}.rr-s:nth-child(4){grid-column:1;grid-row:2}
.rr-n{width:24px;height:24px;border-radius:50%;border:2px solid var(--ink);display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:700}
.rr-s b{font-size:14.5px;font-weight:600}.rr-s em{font-style:normal;font-size:12.5px;color:var(--muted);line-height:1.4}
.rr-s[data-state="outcome"]{border-color:var(--red)}.rr-s[data-state="outcome"] b{color:var(--red)}
.so-rr.is-run .rr-s{animation:rr-lit 2.4s ease both;animation-delay:calc(var(--i) * .45s)}
@keyframes rr-lit{0%{box-shadow:none}25%{box-shadow:0 0 0 4px rgba(212,169,79,.7);background:#FBF1D2}100%{box-shadow:none}}
/* ---- gap-knots ---- */
.gk-today{display:inline}
.so-gk[data-state="owner"] .gk-today{display:none}.so-gk[data-state="owner"] .gk-owner{display:inline}
.gk-chain{display:flex;flex-wrap:wrap;align-items:stretch;row-gap:14px}
.gk-step{flex:0 0 172px;display:flex;flex-direction:column;gap:4px;padding:12px;background:#ECEFEC;border:2px solid var(--wire)}
.gk-step b{font-size:14px;font-weight:600;line-height:1.3;color:var(--muted)}.gk-step em{font-style:normal;font-size:12px;color:var(--muted);line-height:1.35}
.gk-step[data-state="outcome"]{border-color:var(--red);background:var(--sheet)}.gk-step[data-state="outcome"] b{color:var(--red)}
.gk-sn{font-size:10.5px;font-weight:700;color:var(--muted)}
.gk-gap{flex:0 0 112px;display:flex}
.gk-g{width:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:4px;background:transparent;border:0;border-radius:6px}
.gk-rope{width:84px;height:44px}.gk-rope svg{width:100%;height:100%;overflow:visible}
.gk-rope .kn-rope,.gk-rope .kn-tie,.gk-rope .kn-flat{fill:none;stroke-width:3;stroke-linecap:round}
.gk-rope .kn-rope,.gk-rope .kn-tie{stroke:var(--red)}.gk-rope .kn-flat{stroke:var(--green);opacity:0}
.so-gk[data-state="owner"] .gk-rope .kn-tie,.so-gk[data-state="owner"] .gk-rope .kn-rope{opacity:0}.so-gk[data-state="owner"] .gk-rope .kn-flat{opacity:1}
.gk-gl{display:flex;flex-direction:column;align-items:center;text-align:center}
.gk-gl small{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--red)}.gk-gl b{font-size:11.5px;font-weight:600;line-height:1.25}
.so-gk[data-state="owner"] .gk-gl small{color:var(--green)}
.gk-g.tl-pick.is-up{background:#FFF8E6!important}
.so-gk .bx-mob{flex:0 0 100%}
/* ---- people ---- */
.pp-plan{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border:2.5px solid var(--ink);background:var(--sheet)}
.pp-li{display:flex;flex-direction:column;min-width:0;border-right:1.5px solid var(--ink);border-bottom:1.5px solid var(--ink)}
.pp-li:nth-child(3n){border-right:0}
.pp-room{position:relative;width:100%;height:100%;display:flex;flex-direction:column;gap:5px;padding:16px 16px 14px 16px;background:transparent;border:0}
.pp-door{position:absolute;left:16px;bottom:-2px;width:34px;height:8px;background:var(--ground);border-left:1.5px solid var(--ink);border-right:1.5px solid var(--ink)}
.pp-room b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:24px;line-height:.95}.pp-room em{font-style:normal;font-size:12.5px;line-height:1.4;color:var(--ink)}
.pp-room[data-state="target"]{background:#FDF8EA;box-shadow:inset 0 0 0 2.5px var(--amber)}
.pp-tree{display:flex;flex-direction:column;align-items:center;gap:0;margin-top:6px}
.pp-top{width:100%;display:flex;flex-direction:column;align-items:center;gap:3px;padding:12px 16px;background:var(--sheet);border:2.5px solid var(--amber);text-align:center}
.pp-top b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:28px;line-height:.95}.pp-top em{font-style:normal;font-size:12.5px;color:var(--muted)}
.pp-sign{align-self:center;border-color:var(--amber);color:var(--amber)}
.pp-lines{width:50%;height:26px;border:3px solid var(--ink);border-bottom:0;position:relative}
.pp-lines::before{content:"";position:absolute;left:50%;top:-26px;height:26px;border-left:3px solid var(--ink)}
.pp-lines{margin-top:26px}
.pp-split{width:100%;display:grid;grid-template-columns:1fr 1fr;gap:16%}
.pp-mg{display:flex;flex-direction:column;gap:3px;padding:12px 14px;background:#FDF8EA;border:2.5px solid var(--amber)}
.pp-mg b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:24px;line-height:.95}.pp-mg em{font-style:normal;font-size:12.5px;line-height:1.4}
.pp-note{margin-top:10px;font-size:13px;color:var(--muted);text-align:center}
/* ---- sizing ---- */
.sz-roles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.sz-roles>li{min-width:0}.sz-roles>li.bx{grid-column:1/-1}
.sz-role{width:100%;height:100%;display:flex;flex-direction:column;gap:4px;padding:12px 14px;background:var(--sheet);border:2px solid var(--ink)}
.sz-role[data-state="target"]{border-color:var(--amber);background:#FDF8EA}
.sz-role b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:24px;line-height:.95}.sz-role em{font-style:normal;font-size:12.5px;color:var(--muted);line-height:1.4}
.sz-chains{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-top:4px}
.sz-chain{display:flex;flex-direction:column;gap:8px;padding:12px;border:1.5px dashed var(--faint);background:rgba(250,252,251,.6)}
.sz-ch-h{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}
.sz-chain ol{display:flex;flex-direction:column;gap:0}
.sz-st{display:flex;flex-direction:column;gap:4px;padding:10px 12px;background:var(--sheet);border:2px solid var(--ink)}
.sz-st b{font-size:14px;font-weight:600;line-height:1.3}.sz-st em{font-style:normal;font-size:12.5px;color:var(--muted);line-height:1.4}
.sz-st[data-state="outcome"]{border-color:var(--red)}.sz-st[data-state="outcome"] b{color:var(--red)}
.sz-st[data-state="target"]{border-color:var(--amber);background:#FDF8EA}.sz-st[data-state="target"] b{color:var(--amber)}
.sz-ar{height:18px;position:relative}.sz-ar::before{content:"";position:absolute;left:24px;top:0;bottom:0;border-left:2.5px solid var(--ink)}
.sz-ar::after{content:"";position:absolute;left:20px;bottom:1px;width:7px;height:7px;border-right:2.5px solid var(--ink);border-bottom:2.5px solid var(--ink);transform:rotate(45deg)}
.sz-chain[data-state="outcome"] .sz-verdict{border-color:var(--red);color:var(--red)}.sz-chain[data-state="target"] .sz-verdict{border-color:var(--amber);color:var(--amber);background:#FBF1D2}
.sz-sl{font-size:12px;font-weight:600;margin-top:4px}.sz-range{width:100%;accent-color:var(--line)}
.sz-out{font-size:13px}.sz-a{font-weight:700}.sz-out b{font-family:'Bebas Neue',sans-serif;font-size:26px;font-weight:400;color:var(--red)}
.sz-res{font-size:12.5px;font-weight:600;color:var(--amber)}
.sz-st .tl-inline{margin-top:4px}
.sx-src{font-style:normal;font-size:10.5px;font-weight:700;padding:1px 6px;border:1px dashed var(--amber);color:var(--amber);border-radius:8px;white-space:nowrap}
/* ---- costing ---- */
.co-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:18px}
.co-cost,.co-need{display:flex;flex-direction:column;gap:8px;padding:16px 18px;background:var(--sheet);border:2px solid var(--ink)}
.co-need{border-style:dashed;border-color:var(--amber)}
.co-v{font-family:'Bebas Neue',sans-serif;font-size:42px;line-height:.95}
.co-lines{display:flex;flex-direction:column;gap:5px;margin:0;padding:0;list-style:none}.co-lines li{display:flex;justify-content:space-between;gap:10px;font-size:13px;border-bottom:1px dashed var(--faint);padding-bottom:4px}
.co-lines b{white-space:nowrap}
.co-note{font-size:12.5px;color:var(--muted);line-height:1.4}
.co-nh{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
.co-count{font-size:11.5px;font-weight:700;color:var(--amber)}.co-count.is-done{color:var(--green)}
.co-list{display:flex;flex-direction:column;gap:10px}.co-list li{display:flex;flex-direction:column;gap:4px}
.co-q{font-size:13px;font-weight:600}
/* ---- gauges ---- */
.gg-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.gg-li{display:flex;flex-direction:column;min-width:0;transition:opacity .25s}
.gg-li>.bx{grid-column:1/-1}
.so-gg[data-f="lead"] .gg-li:not([data-kind="lead"]),.so-gg[data-f="result"] .gg-li:not([data-kind="result"]){opacity:.35}
.gg-card{width:100%;height:100%;display:flex;flex-direction:column;align-items:flex-start;gap:6px;padding:12px;background:var(--sheet);border:2px solid var(--ink)}
.gg-card[data-new="yes"]{border-style:dashed;border-color:var(--amber)}
.gg-dial{width:84px;height:50px}
.gg-arc{fill:none;stroke:var(--ink);stroke-width:5;stroke-linecap:round}.gg-tk{stroke:var(--ink);stroke-width:1.6}
.gg-card[data-new="yes"] .gg-arc{stroke:var(--amber);stroke-dasharray:6 6}
.gg-nd{stroke:var(--red);stroke-width:3;stroke-linecap:round}.gg-hub{fill:var(--ink)}
.gg-qm{font-family:'Bebas Neue',sans-serif;font-size:24px;fill:var(--amber);text-anchor:middle}
.gg-tx{display:flex;flex-direction:column;gap:3px;min-width:0}
.gg-tx b{font-size:13.5px;font-weight:600;line-height:1.3}.gg-tx em{font-style:normal;font-size:12px;color:var(--muted);line-height:1.35}
/* ---- findings ---- */
.fi-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.fi-row>li{display:flex;flex-direction:column;min-width:0}
.fi-card{width:100%;height:100%;display:flex;flex-direction:column;gap:4px;padding:14px;background:#ECEFEC;border:2px solid var(--wire)}
.fi-card small{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.fi-card b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:28px;line-height:.95;color:var(--ink)}.fi-card em{font-style:normal;font-size:12.5px;color:var(--muted);line-height:1.4}
.so-fi .bx-mob{margin-top:10px}
/* ---- phone ---- */
@container sx (max-width:699px){
 .so-acts{grid-template-columns:minmax(0,1fr);gap:10px}
 .hb-grid{grid-template-columns:minmax(0,1fr);row-gap:26px}
 .hb-in .hb-list::after,.hb-w,.hb-o::before,.hb-out .hb-outs::before{display:none}
 .hb-core::before{right:auto;left:50%;top:-26px;width:0;height:26px;border-top:0;border-left:3px solid var(--gold)}
 .hb-core::after{left:50%;top:100%;width:0;height:26px;border-top:0;border-left:3px solid var(--gold)}
 .pr-row{flex-direction:column}.pr-gap{height:12px;width:auto}.pr-vs{padding:6px 0}
 .fd-build{padding:0}.fd-floors,.fd-found{grid-template-columns:minmax(0,1fr)}.fd-ground{margin:6px 0 0}.fd-roof{margin:0;width:100%}
 .dr-row{grid-template-columns:minmax(0,1fr);gap:12px}
 .dr-door{min-height:0;border-radius:40px 40px 2px 2px;padding:14px 16px 16px}
 .dr-plate{margin:6px auto 0}
 .dr-door[data-state="covered"],.dr-door[data-state="covered"].is-up{transform:none}
 .dy-board{padding:30px 10px 10px 10px}
 .dy-axis{left:10px;right:10px}
 .dy-lane{height:auto;padding:4px 0 6px}
 .dy-name{position:static;transform:none;width:auto;margin:2px 0 4px}
 .dy-track{position:relative;height:36px}
 .dy-track{height:auto;min-height:44px}
 .dy-bar{top:2px;height:auto;min-height:38px;padding:3px 6px}.dy-bar b{white-space:normal;line-height:1.2;font-size:11px}
 .dy-tick:nth-child(even){display:none}
 .nt-row{grid-template-columns:minmax(0,1fr)}
 .ow-row{flex-direction:column}.ow-arrow{flex:0 0 auto;padding:10px 0}.ow-arrow span{width:0;height:46px;border-top:0;border-left:3px solid var(--amber)}
 .ow-arrow span::before{left:-7px;top:0;transform:rotate(45deg)}.ow-arrow span::after{left:-7px;right:auto;top:auto;bottom:0;transform:rotate(225deg)}
 .ow-say{font-size:21px}
 .rr-grid{grid-template-columns:minmax(0,1fr)}
 .rr-loop{grid-template-columns:minmax(0,1fr);gap:12px}.rr-loop::before{inset:20px auto 20px 14px;border-radius:0;border-width:0 0 0 3px}
 .rr-s:nth-child(3),.rr-s:nth-child(4){grid-column:auto;grid-row:auto}
 .gk-chain{flex-direction:column;flex-wrap:nowrap}
 .gk-step{flex:0 0 auto}.gk-gap{flex:0 0 auto}
 .gk-g{flex-direction:row;justify-content:flex-start;gap:12px;padding:6px 10px}
 .gk-gl{align-items:flex-start;text-align:left}
 .pp-plan{grid-template-columns:minmax(0,1fr)}.pp-li{border-right:0}
 .pp-split{grid-template-columns:minmax(0,1fr);gap:10px}.pp-lines{width:0;border-width:0 0 0 3px;margin-top:0}.pp-lines::before{display:none}
 .sz-roles,.sz-chains,.co-grid,.fi-row{grid-template-columns:minmax(0,1fr)}
 .gg-grid{grid-template-columns:minmax(0,1fr)}
 .gg-card{flex-direction:row;align-items:center;gap:12px}
}
'''
