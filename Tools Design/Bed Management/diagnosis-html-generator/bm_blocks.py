"""
bm_blocks — Bed Management's own drawings for Diagnosis turns (drafts, 30 Sep 2026).

Why they exist: turns built only from the library's box blocks (cards, figures, chains) looked alike. Each of these
is a drawing, in the Diagnosis look (morning count palette, the small bed from the home page, gold = now), and each
turn uses a different one. They follow 07: drawn structures, the five states, both layouts from one markup,
nothing sideways on a phone, and on a phone every pickable item is stacked one above the other, never side by side.

  lens            areas to examine, on the rim of a magnifying glass           (bm-dg-02)
  day-strips      two ways a day can run, bed by bed, hour by hour             (bm-dg-03)
  admission-route the patient's way from the door to the bed, with clock times (bm-dg-04, 05)
  stopwatch       where an admission's hours go: work and waiting             (bm-dg-05)
  bed-bills       the leaving bill and the next bill, tied to one bed          (bm-dg-06, 07)
  receipt         the figures that turn hours into rupees, typed on a bill     (bm-dg-08)
  bed-count       the beds that change patient each day, and what they earn    (bm-dg-09)
  evidence-board  the findings pinned in the order given, on one thread        (bm-dg-10)
  rule-loop       one rule and the loop it starts                              (bm-dg-11)
  scale           demand against supply, on a balance                          (bm-dg-12)
  corridor        the five parts as closed doors, none opened yet             (bm-dg-12)

register(G) is called by bm_diagnosis_html with its helpers (sheet, bedmark, pick_attrs, L, dh, C).
"""
import math

G = {}
def e(s): return G['dh'].e(s)
def pt(o): return G['dh'].pt(o)

def register(helpers):
    G.update(helpers)
    return {'lens': r_lens, 'day-strips': r_day_strips, 'admission-route': r_route, 'stopwatch': r_stopwatch, 'bed-bills': r_bed_bills,
            'receipt': r_receipt, 'bed-count': r_bed_count, 'evidence-board': r_board, 'rule-loop': r_loop, 'scale': r_scale, 'corridor': r_corridor}

def sheet(sh, grp, first, where): return G['sheet'](sh, grp, first, where)
def pick(grp, key, first, cls=''): return G['pick_attrs'](grp, key, first, cls)
def desk(boxes): return '<div class="bx-desk-wrap">%s</div>' % ''.join(boxes)
def hint(t): return G['L'].hint(t)

def arc(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0); x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    return 'M%.1f %.1fA%d %d 0 %d 1 %.1f %.1f' % (x0, y0, r, r, 1 if (a1 - a0) > math.pi else 0, x1, y1)

# ------------------------------------------------------------------------------------------ lens
def r_lens(b, ctx):
    grp = ctx.uid('bmln'); areas, sheets = b['areas'], b['sheets']; n = len(areas)
    cx = cy = 150; R = 116; gap = 0.07
    segs, nums = [], []
    for i, a in enumerate(areas):
        a0 = -math.pi / 2 + i * 2 * math.pi / n + gap / 2; a1 = a0 + 2 * math.pi / n - gap
        cur = ' is-cur' if i == 0 else ''
        segs.append('<path d="%s" class="ln-seg ln-%s%s" data-cur-for="%s:%s"/>' % (arc(cx, cy, R, a0, a1), e(a.get('state', 'later')), cur, grp, e(sheets[i]['key'])))
        am = (a0 + a1) / 2
        nums.append('<g class="ln-num%s" data-cur-for="%s:%s"><circle cx="%.1f" cy="%.1f" r="15"/><text x="%.1f" y="%.1f">%d</text></g>' % (
            cur, grp, e(sheets[i]['key']), cx + R * math.cos(am), cy + R * math.sin(am), cx + R * math.cos(am), cy + R * math.sin(am) + 5, i + 1))
    c = b['centre']
    svg = ('<svg class="ln-svg" viewBox="0 0 330 330" aria-hidden="true"><line x1="236" y1="236" x2="312" y2="312" class="ln-handle"/>'
           '<circle cx="150" cy="150" r="%d" class="ln-glass"/>%s%s</svg>') % (R - 16, ''.join(segs), ''.join(nums))
    glass = '<div class="ln-lens" role="img" aria-label="%s">%s<div class="ln-c"><span class="tj-label">%s</span><b class="tj-big">%s</b><span>%s</span></div></div>' % (
        e('%s: %s' % (c['title'], ', '.join(a['name'] for a in areas))), svg, e(c['kicker']), e(c['title']), e(c['sub']))
    items, boxes = [], []
    for i, a in enumerate(areas):
        sh = sheets[i]; first = i == 0
        items.append('<button type="button"%s%s><span class="ln-n">%d</span><span class="ln-t"><b>%s</b><small>%s</small></span></button>%s' % (
            pick(grp, sh['key'], first, 'ln-a ln-a-%s' % e(a.get('state', 'later'))), pt(a), i + 1, e(a['name']), e(a['status']), sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    return ('<section class="tj-block bm-ln"><div class="ln-grid">%s<div class="ln-list">%s</div></div>%s%s%s</section>') % (
        glass, ''.join(items), hint(b.get('hint', 'Tap an area to see the question I’ll ask there.')), desk(boxes), G['dh'].divider(b.get('caption')))

# ------------------------------------------------------------------------------------------ day-strips
DS_WORD = {'out': 'Patients leaving', 'in': 'Patients arriving', 'both': 'Both at once', 'none': 'Quiet'}
def ds_cell(state, label):
    bed = {'out': 'leaving', 'in': 'next', 'both': 'in', 'none': 'empty'}[state]
    arrow = {'out': '<i class="ds-ar ds-out" aria-hidden="true">↑</i>', 'in': '<i class="ds-ar ds-in" aria-hidden="true">↓</i>',
             'both': '<i class="ds-ar ds-both" aria-hidden="true">↕</i>', 'none': ''}[state]
    return '<span class="ds-cell ds-%s" title="%s">%s%s<em>%s</em><span class="sr">%s</span></span>' % (state, e(DS_WORD[state]), G['bedmark'](bed, 26), arrow, e(label), e(DS_WORD[state]))

def r_day_strips(b, ctx):
    grp = ctx.uid('bmds'); slots = b['slots']; n = len(slots); sheets = b['sheets']
    head = '<div class="ds-head" style="--n:%d"><span></span>%s</div>' % (n, ''.join('<span>%s</span>' % e(s) for s in slots))
    rows, boxes = [], []
    for i, p in enumerate(b['patterns']):
        sh = sheets[i]; first = i == 0
        cells = ''.join(ds_cell(c, slots[j]) for j, c in enumerate(p['cells']))
        rows.append('<button type="button"%s style="--n:%d"><span class="ds-name"><b class="tj-big">%s</b><small>%s</small></span><span class="ds-cells">%s</span></button>%s' % (
            pick(grp, sh['key'], first, 'ds-row'), n, e(p['name']), e(p['tag']), cells, sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    key = '<div class="ds-key">%s</div>' % ''.join('<span>%s%s</span>' % (ds_cell(k, '')[:-7] if False else G['bedmark']({'out': 'leaving', 'in': 'next', 'both': 'in', 'none': 'empty'}[k], 18), e(DS_WORD[k])) for k in ('out', 'in', 'both', 'none'))
    return '<section class="tj-block bm-ds">%s<div class="ds-rows">%s</div>%s%s%s%s</section>' % (
        head, ''.join(rows), key, hint(b.get('hint', 'Tap a pattern to read it.')), desk(boxes), G['dh'].divider(b.get('caption')))

# ------------------------------------------------------------------------------------------ admission-route
DOOR = '<svg viewBox="0 0 40 52" width="34" height="44" aria-hidden="true"><rect x="3" y="3" width="34" height="46" rx="2" class="dr-f"/><rect x="9" y="9" width="22" height="38" class="dr-d"/><circle cx="26" cy="29" r="2.2" class="dr-h"/></svg>'
def r_route(b, ctx):
    grp = ctx.uid('bmrt'); stops, sheets = b['stops'], b['sheets']; blank = b['mode'] == 'blank'
    items, boxes = [], []
    for i, s in enumerate(stops):
        sh = sheets[i]; first = i == 0
        if blank:
            chip = G['L'].slot('%s:%s' % (grp, sh['key']), 'hh : mm', 'rt-chip')
        else:
            chip = '<span class="rt-chip rt-val">%s</span>' % e(s['typical'])
        gap = '<span class="rt-gap">%s</span>' % e(s['gap']) if s.get('gap') else ''
        items.append('<div class="rt-cell"><button type="button"%s data-state="%s">%s<span class="rt-dot">%d</span><b class="rt-name">%s</b></button>%s%s</div>' % (
            pick(grp, sh['key'], first, 'rt-stop'), 'outcome' if s.get('outcome') else 'plain', chip, i + 1, e(s['name']), gap, sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    ends = ('<div class="rt-end rt-start">%s<span>%s</span></div>' % (DOOR, e(b['start_label'])),
            '<div class="rt-end rt-fin">%s<span>%s</span></div>' % (G['bedmark']('next', 30), e(b['end_label'])))
    return ('<section class="tj-block bm-rt bm-rt-%s"><div class="rt-line">%s<div class="rt-stops" style="--n:%d">%s</div>%s</div>%s%s%s</section>') % (
        e(b['mode']), ends[0], len(stops), ''.join(items), ends[1], hint(b.get('hint', 'Tap a step to open it.')), desk(boxes), G['dh'].divider(b.get('caption')))

# ------------------------------------------------------------------------------------------ stopwatch
def r_stopwatch(b, ctx):
    cx, cy, R = 110, 124, 86
    total = sum(p['hours'] for p in b['parts']); span = float(b['dial_hours'])
    a = -math.pi / 2; arcs = []
    for p in b['parts']:
        a1 = a + 2 * math.pi * p['hours'] / span
        arcs.append('<path d="%s" class="sw-%s"/>' % (arc(cx, cy, R, a, a1), e(p['kind']))); a = a1
    ticks = ''.join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="sw-tick"/>' % (
        cx + (R + 14) * math.cos(-math.pi / 2 + k * 2 * math.pi / span), cy + (R + 14) * math.sin(-math.pi / 2 + k * 2 * math.pi / span),
        cx + (R + 22) * math.cos(-math.pi / 2 + k * 2 * math.pi / span), cy + (R + 22) * math.sin(-math.pi / 2 + k * 2 * math.pi / span)) for k in range(int(span)))
    svg = ('<svg class="sw-svg" viewBox="0 0 220 240" role="img" aria-label="%s"><rect x="96" y="4" width="28" height="14" rx="3" class="sw-crown"/>'
           '<line x1="110" y1="18" x2="110" y2="30" class="sw-stem"/><circle cx="%d" cy="%d" r="%d" class="sw-face"/>%s%s'
           '<text x="%d" y="%d" class="sw-v">%s</text><text x="%d" y="%d" class="sw-l">%s</text></svg>') % (
        e('%s: %s' % (b['label'], b['value'])), cx, cy, R + 24, ticks, ''.join(arcs), cx, cy + 6, e(b['value']), cx, cy + 30, e(b['value_sub']))
    legend = ''.join('<li class="sw-li sw-li-%s"><i></i><b>%s</b><span>%s</span></li>' % (e(p['kind']), e(p['label']), e(p['text'])) for p in b['parts'])
    return ('<section class="tj-block bm-sw"><div class="sw-grid">%s<div class="sw-side"><div class="tj-label">%s</div><ul>%s</ul><p class="sw-worst">%s</p></div></div></section>') % (
        svg, e(b['label']), legend, e(b['worst']))

# ------------------------------------------------------------------------------------------ bed-bills
def r_bed_bills(b, ctx):
    grp = ctx.uid('bmbb'); tags, sheets = b['tags'], b['sheets']; blank = b['mode'] == 'blank'
    parts, boxes = [], []
    for i, t in enumerate(tags):
        sh = sheets[i]; first = i == 0
        fill = '%s:%s' % (grp, sh['key'])
        val = G['L'].slot(fill, 'hh : mm', 'bb-val') if blank else '<span class="bb-val">%s</span>%s' % (e(t['value']), '<span class="bb-worst">%s</span>' % e(t['worst']) if t.get('worst') else '')
        parts.append('<div class="bb-cell"><button type="button"%s data-state="%s"><span class="bb-hole" aria-hidden="true"></span><span class="bb-who">%s</span><b class="bb-lab">%s</b>%s</button>%s</div>' % (
            pick(grp, sh['key'], first, 'bb-tag bb-tag-%d' % i), 'outcome' if t.get('outcome') else 'plain', e(t['who']), e(t['label']), val, sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    bed = G['bedmark']
    mid = ('<div class="bb-mid" aria-hidden="true"><div class="bb-gap"><span>%s</span></div><div class="bb-beds">%s<i>→</i>%s<i>→</i>%s</div>'
           '<div class="bb-bedlab"><span>Leaving</span><span>Empty</span><span>Next patient</span></div></div>') % (e(b['gap_label']), bed('leaving', 34), bed('empty', 34), bed('next', 34))
    return ('<section class="tj-block bm-bb"><div class="bb-row">%s%s%s</div>%s%s%s</section>') % (
        parts[0], mid, parts[1], hint(b.get('hint', 'Tap a bill to open it.')), desk(boxes), G['dh'].divider(b.get('caption')))

# ------------------------------------------------------------------------------------------ receipt
def r_receipt(b, ctx):
    grp = ctx.uid('bmrc'); lines, sheets = b['lines'], b['sheets']
    rows, boxes = [], []
    for i, ln in enumerate(lines):
        sh = sheets[i]; first = i == 0
        rows.append('<div role="button" tabindex="0"%s%s><span class="rc-no">%d</span><span class="rc-lab"><b>%s</b><small>%s</small></span><span class="rc-lead" aria-hidden="true"></span>'
                    '<span class="rc-in">%s</span></div>%s' % (
                        pick(grp, sh['key'], first, 'rc-line'), pt(ln), i + 1, e(ln['label']), e(ln['unit']), G['L'].inline(ln['label'], ln['placeholder'], grp), sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    total = '<div class="rc-total"><span>%s</span><b data-count-for="%s" data-waiting="%s" data-done="%s">%s</b></div>' % (
        e(b['total_label']), grp, e(b['waiting']), e(b['done']), e(b['waiting']))
    return ('<section class="tj-block bm-rc"><div class="rc-paper"><div class="rc-head"><span class="tj-label">%s</span><span class="rc-sub">%s</span></div>'
            '<div class="rc-lines">%s</div>%s</div>%s%s%s</section>') % (
        e(b['title']), e(b['subtitle']), ''.join(rows), total, hint(b.get('hint', 'Type each figure on its line.')), desk(boxes), G['dh'].divider(b.get('caption')))

# ------------------------------------------------------------------------------------------ bed-count
def r_bed_count(b, ctx):
    grp = ctx.uid('bmbc'); occ, stay, rate = b['occupied'], b['stay'], b['rate']; h = b['hours']
    per_day = int(round(occ / stay))
    beds = ''.join('<span class="bc-bed">%s<i></i></span>' % G['bedmark']('leaving', 16) for _ in range(per_day))
    reads, boxes = [], []
    for i, r in enumerate(b['readouts']):
        sh = b['sheets'][i]; first = i == 0
        reads.append('<div class="bc-cell"><button type="button"%s data-state="%s"%s><span class="tj-label">%s</span><b class="bc-v" data-bc="%s">—</b><small>%s</small></button>%s</div>' % (
            pick(grp, sh['key'], first, 'bc-read'), e(r.get('state', 'plain')), pt(r), e(r['label']), e(r['calc']), e(r['note']), sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    slider = ('<div class="bc-slider"><label for="%s-h"><span class="tj-label">%s</span><b class="bc-h">%s hours</b></label>'
              '<input id="%s-h" type="range" min="%s" max="%s" step="%s" value="%s"><div class="bc-scale"><span>%s hours</span><span>%s hours</span></div></div>') % (
        grp, e(h['label']), h['value'], grp, h['min'], h['max'], h['step'], h['value'], h['min'], h['max'])
    return ('<section class="tj-block bm-bc" data-occ="%s" data-stay="%s" data-rate="%s"><div class="bc-top"><div class="bc-from"><b class="tj-big">%d</b><span>%s</span></div>'
            '<div class="bc-arrow" aria-hidden="true">→</div><div class="bc-from"><b class="tj-big">%d</b><span>%s</span></div></div>'
            '<div class="bc-beds" role="img" aria-label="%d beds change patient every day">%s</div><p class="bc-cap">%s</p>%s<div class="bc-reads">%s</div>%s%s%s</section>') % (
        occ, stay, rate, occ, e(b['occupied_label']), per_day, e(b['per_day_label']), per_day, beds, e(b['beds_caption']), slider, ''.join(reads),
        hint(b.get('hint', 'Tap a figure to see the working.')), desk(boxes), G['dh'].divider(b.get('caption')))

BC_JS = r'''
(function(){
  function indian(n){n=Math.round(n);var s=String(n),l=s.slice(-3),r=s.slice(0,-3);return (r?r.replace(/\B(?=(\d{2})+(?!\d))/g,',')+',':'')+l;}
  [].slice.call(document.querySelectorAll('.bm-bc')).forEach(function(b){
    var occ=+b.getAttribute('data-occ'),stay=+b.getAttribute('data-stay'),rate=+b.getAttribute('data-rate'),r=b.querySelector('input[type=range]');
    function upd(){var h=+r.value,t=occ/stay,hy=t*h*365,d=hy/24,v=d*rate;
      b.querySelector('.bc-h').textContent=h+' hours';
      var out={hy:indian(hy),d:indian(d),v:'₹'+(Math.round(v/1e6)/10)+' crore'};
      [].slice.call(b.querySelectorAll('[data-bc]')).forEach(function(x){x.textContent=out[x.getAttribute('data-bc')];});}
    r.addEventListener('input',upd);upd();});
})();
'''

# ------------------------------------------------------------------------------------------ evidence-board
def r_board(b, ctx):
    grp = ctx.uid('bmeb'); cards, sheets = b['cards'], b['sheets']
    items, boxes = [], []
    for i, c in enumerate(cards):
        sh = sheets[i]; first = i == 0
        items.append('<div class="eb-cell" style="--r:%s"><button type="button"%s%s><span class="eb-pin" aria-hidden="true"></span><span class="eb-no">%d</span>'
                     '<b class="eb-f">%s</b><span class="eb-q">%s</span><small>%s</small></button>%s</div>' % (
                         ['-1.4deg', '1deg', '-0.6deg', '1.3deg', '-1deg', '0.7deg'][i % 6], pick(grp, sh['key'], first, 'eb-card'), pt(c), i + 1,
                         e(c['finding']), e(c['quote']), e(c['from']), sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    return ('<section class="tj-block bm-eb"><div class="eb-board"><div class="eb-banner">%s</div><div class="eb-row" style="--n:%d"><span class="eb-thread" aria-hidden="true"></span>%s</div></div>%s%s</section>') % (
        e(b['banner']), len(cards), ''.join(items), hint(b.get('hint', 'Tap a card to see where it came from.')), desk(boxes))

# ------------------------------------------------------------------------------------------ rule-loop
def r_loop(b, ctx):
    grp = ctx.uid('bmrl'); steps, sheets = b['steps'], b['sheets']
    nodes, boxes = [], []
    for i, s in enumerate(steps):
        sh = sheets[i]; first = i == 0
        nodes.append('<div class="rl-node rl-p%d"><button type="button"%s data-state="%s"%s><span class="rl-no">%d</span><b>%s</b>%s</button>%s%s</div>' % (
            i + 1, pick(grp, sh['key'], first, 'rl-card'), 'outcome' if s.get('outcome') else 'plain', pt(s), i + 1, e(s['text']),
            '<span class="rl-clock">%s</span>' % e(s['clock']) if s.get('clock') else '', '<span class="rl-then" aria-hidden="true">↓</span>' if i < len(steps) - 1 else '',
            sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    ring = ('<svg class="rl-ring" viewBox="0 0 800 450" aria-hidden="true"><defs><marker id="%s-ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0 0L10 5L0 10z"/></marker></defs>'
            '<path d="M470 40 A330 190 0 0 1 740 190"/><path d="M740 260 A330 190 0 0 1 470 410"/><path d="M330 410 A330 190 0 0 1 60 260"/><path d="M60 190 A330 190 0 0 1 330 40"/></svg>') % grp
    ring = ring.replace('<path d="M', '<path marker-end="url(#%s-ah)" d="M' % grp)
    feeds = '<div class="rl-feeds"><span class="tj-label">%s</span><div>%s</div></div>' % (e(b['feeds_label']), ''.join('<span class="rl-chip">%s</span>' % e(f) for f in b['feeds']))
    rule = '<div class="rl-rule"><span class="rl-rk">The rule</span><b>%s</b><span class="rl-from">%s</span></div>' % (e(b['rule']), e(b['rule_from']))
    back = '<p class="rl-back"><span aria-hidden="true">↻</span>%s</p>' % e(b['back'])
    return '<section class="tj-block bm-rl">%s<div class="rl-wrap">%s%s%s</div>%s%s%s</section>' % (
        feeds, ring, rule, ''.join(nodes), back, hint(b.get('hint', 'Tap a step to follow the loop.')), desk(boxes))

# ------------------------------------------------------------------------------------------ scale
def r_scale(b, ctx):
    l, r = b['left'], b['right']
    tilt = max(-9, min(9, (float(r['value']) - float(l['value'])) * 1.2))
    svg = ('<svg class="sc-svg" viewBox="0 0 520 262" role="img" aria-label="%s">'
           '<path d="M260 150 L230 236 H290 Z" class="sc-post"/><g transform="rotate(%.1f 260 150)"><line x1="70" y1="150" x2="450" y2="150" class="sc-beam"/>'
           '<line x1="100" y1="150" x2="100" y2="186" class="sc-cord"/><line x1="420" y1="150" x2="420" y2="186" class="sc-cord"/>'
           '<g transform="rotate(%.1f 100 186)"><path d="M36 186 H164 Q156 232 100 232 Q44 232 36 186Z" class="sc-pan sc-heavy"/><text x="100" y="220" class="sc-n">%s</text></g>'
           '<g transform="rotate(%.1f 420 186)"><path d="M356 186 H484 Q476 232 420 232 Q364 232 356 186Z" class="sc-pan"/><text x="420" y="220" class="sc-n">%s</text></g>'
           '</g><circle cx="260" cy="150" r="7" class="sc-pin"/></svg>') % (
        e('%s %s against %s %s' % (l['value'], l['label'], r['value'], r['label'])), tilt, -tilt, e(l['value']), -tilt, e(r['value']))
    labs = '<div class="sc-labs"><span><b>%s</b>%s</span><span><b>%s</b>%s</span></div>' % (e(l['label']), e(l['note']), e(r['label']), e(r['note']))
    return '<section class="tj-block bm-sc"><div class="sc-grid"><div>%s%s</div><div class="sc-verdict"><span class="tj-label">%s</span><b class="tj-big">%s</b><p class="tj-text">%s</p></div></div></section>' % (
        svg, labs, e(b['verdict_label']), e(b['verdict']), e(b['text']))

# ------------------------------------------------------------------------------------------ corridor
def door_svg():
    return ('<svg class="cd-door" viewBox="0 0 60 90" aria-hidden="true"><rect x="2" y="2" width="56" height="86" class="cd-frame"/>'
            '<g class="cd-leaf"><rect x="8" y="8" width="44" height="80" class="cd-panel"/><rect x="15" y="16" width="30" height="24" class="cd-inset"/>'
            '<rect x="15" y="48" width="30" height="30" class="cd-inset"/><circle cx="44" cy="52" r="2.6" class="cd-knob"/></g></svg>')

def r_corridor(b, ctx):
    grp = ctx.uid('bmcd'); doors, sheets = b['doors'], b['sheets']
    items, boxes = [], []
    for i, d in enumerate(doors):
        sh = sheets[i]; first = i == 0
        items.append('<div class="cd-cell"><button type="button"%s%s><span class="cd-plate">Part %d</span>%s<b class="cd-name">%s</b><small>%s</small></button>%s</div>' % (
            pick(grp, sh['key'], first, 'cd-d'), pt(d), i + 1, door_svg(), e(d['name']), e(d['text']), sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    return ('<section class="tj-block bm-cd"><div class="tj-label">%s</div><div class="cd-hall" style="--n:%d">%s</div><div class="cd-floor" aria-hidden="true"></div>%s%s</section>') % (
        e(b['label']), len(doors), ''.join(items), hint(b.get('hint', 'Tap a door to look in.')), desk(boxes))

# ==========================================================================================
CSS = r'''
/* ---- shared for Bed Management drawings: every sheet wraps its words, nothing sticks out */
.bm-sheet,.bm-sheet *{overflow-wrap:anywhere;min-width:0}
.bm-sheet h3.tj-big{overflow-wrap:normal;word-break:normal}
/* lens */
.ln-grid{display:grid;grid-template-columns:330px minmax(0,1fr);gap:30px;align-items:center}
.ln-lens{position:relative;width:330px;max-width:100%;aspect-ratio:1}
.ln-svg{position:absolute;inset:0;width:100%;height:100%}
.ln-handle{stroke:var(--ink);stroke-width:24;stroke-linecap:round}
.ln-glass{fill:var(--card);stroke:var(--ink);stroke-width:3}
.ln-seg{fill:none;stroke:var(--line,#B2BED0);stroke-width:22;transition:stroke .2s}
.ln-seg.ln-now{stroke:var(--ink)}
.ln-seg.is-cur{stroke:var(--gold)}
.ln-num circle{fill:var(--card);stroke:var(--ink);stroke-width:2.5}.ln-num text{font-size:14px;font-weight:700;fill:var(--ink);text-anchor:middle}
.ln-num.is-cur circle{fill:var(--gold)}
.ln-c{position:absolute;left:50%;top:45.5%;transform:translate(-50%,-50%);width:52%;text-align:center;display:flex;flex-direction:column;gap:4px;align-items:center}
.ln-c b{font-size:30px;line-height:.95}.ln-c span:last-child{font-size:12.5px;color:var(--muted)}
.ln-list{display:flex;flex-direction:column;gap:10px}
.ln-a{display:grid;grid-template-columns:36px minmax(0,1fr) auto;align-items:center;gap:12px;text-align:left;background:var(--card);border:2px solid var(--ink);border-radius:8px;padding:10px 14px;font:inherit;color:inherit}
.ln-n{width:30px;height:30px;border-radius:50%;border:2.5px solid var(--ink);display:flex;align-items:center;justify-content:center;font-weight:700}
.ln-a-now .ln-n{background:var(--gold);border-color:var(--gold)}
.ln-t{display:flex;flex-direction:column;gap:1px}.ln-t b{font-size:15px;line-height:1.3}.ln-t small{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.ln-a-now .ln-t small{color:var(--green)}
/* day-strips */
.ds-head,.ds-row{display:grid;grid-template-columns:200px repeat(var(--n),minmax(0,1fr));gap:6px;align-items:center}
.ds-head span{font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);text-align:center}
.ds-rows{display:flex;flex-direction:column;gap:12px}
.ds-row{text-align:left;background:var(--card);border:2px solid var(--ink);border-radius:10px;padding:12px 12px;font:inherit;color:inherit}
.ds-cells{display:contents}
.ds-name{display:flex;flex-direction:column;gap:2px;padding-left:4px}.ds-name b{font-size:28px;line-height:1}.ds-name small{font-size:13px;color:var(--muted)}
.ds-cell{position:relative;display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 2px;border-radius:6px}
.ds-cell em{display:none;font-style:normal;font-size:11px;color:var(--muted)}
.ds-out{background:rgba(138,86,8,.1)}.ds-in{background:rgba(47,107,79,.12)}.ds-both{background:linear-gradient(90deg,rgba(138,86,8,.1) 50%,rgba(47,107,79,.12) 50%)}
.ds-ar{position:absolute;right:6px;top:4px;font-style:normal;font-weight:700;font-size:14px}.ds-out.ds-cell .ds-ar{color:var(--st-target)}.ds-in .ds-ar{color:var(--green)}.ds-both .ds-ar{color:var(--ink)}
.ds-key{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:12.5px;color:var(--muted)}.ds-key span{display:inline-flex;align-items:center;gap:6px}
/* admission-route */
.rt-line{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:10px;position:relative}
.rt-end{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11.5px;font-weight:600;text-align:center;max-width:90px}
.dr-f{fill:var(--card);stroke:var(--ink);stroke-width:2.5}.dr-d{fill:var(--ground);stroke:var(--ink);stroke-width:2}.dr-h{fill:var(--gold)}
.rt-stops{position:relative;display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr))}
.rt-stops::before{content:"";position:absolute;left:0;right:0;top:66px;border-top:5px dotted var(--ink)}
.rt-cell{position:relative;display:flex;flex-direction:column;min-width:0}
.rt-stop{position:relative;display:flex;flex-direction:column;align-items:center;gap:8px;padding:8px 6px 10px;background:transparent;border:0;border-radius:10px;font:inherit;color:inherit;text-align:center}
.rt-chip{display:inline-flex;align-items:center;justify-content:center;min-height:38px;min-width:96px;padding:0 10px;border-radius:6px;font-family:var(--f-display);font-size:24px;line-height:1;background:var(--card)}
.rt-chip.tl-slot{font-family:var(--f-body);font-size:14px;font-weight:600;letter-spacing:.08em}
.rt-val{border:2px solid var(--ink)}
.rt-dot{position:relative;z-index:1;width:34px;height:34px;border-radius:50%;background:var(--card);border:4px solid var(--ink);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.rt-name{font-size:13.5px;line-height:1.3;max-width:150px}
.rt-stop[data-state="outcome"] .rt-dot,.rt-stop[data-state="outcome"] .rt-val{border-color:var(--red);color:var(--red)}
.rt-gap{position:absolute;left:100%;top:57px;transform:translateX(-50%);z-index:2;font-size:11px;font-weight:700;color:var(--st-target);background:var(--ground);padding:1px 5px;border-radius:8px;white-space:nowrap}
/* stopwatch */
.sw-grid{display:grid;grid-template-columns:240px minmax(0,1fr);gap:28px;align-items:center;background:var(--card);border:2px solid var(--ink);padding:18px 24px}
.sw-svg{width:100%;max-width:240px;height:auto}
.sw-face{fill:var(--ground);stroke:var(--ink);stroke-width:3}.sw-crown{fill:var(--ink)}.sw-stem{stroke:var(--ink);stroke-width:5}
.sw-tick{stroke:var(--ink);stroke-width:2}
.sw-work{fill:none;stroke:var(--ink);stroke-width:26}
.sw-wait{fill:none;stroke:var(--st-target);stroke-width:26;stroke-dasharray:6 3}
.sw-v{font-family:var(--f-display);font-size:34px;fill:var(--ink);text-anchor:middle}.sw-l{font-size:11px;fill:var(--muted);text-anchor:middle}
.sw-side{display:flex;flex-direction:column;gap:10px}.sw-side ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.sw-li{display:grid;grid-template-columns:22px minmax(0,1fr);gap:2px 10px;font-size:14px}.sw-li i{grid-row:span 2;width:18px;height:18px;border-radius:4px;margin-top:2px}
.sw-li-work i{background:var(--ink)}.sw-li-wait i{background:repeating-linear-gradient(135deg,var(--st-target) 0 4px,transparent 4px 7px);border:2px solid var(--st-target)}
.sw-li span{color:var(--muted);font-size:13px}.sw-worst{margin:0;font-weight:600;color:var(--red);font-size:14px}
/* bed-bills */
.bb-row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr) minmax(0,1fr);gap:14px;align-items:center}
.bb-cell{display:flex;flex-direction:column;min-width:0}
.bb-tag{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:8px;text-align:left;background:var(--card);border:2px solid var(--ink);border-radius:6px 22px 22px 6px;padding:18px 20px 18px 34px;font:inherit;color:inherit}
.bb-hole{position:absolute;left:12px;top:50%;width:11px;height:11px;margin-top:-5px;border-radius:50%;border:2px solid var(--ink);background:var(--ground)}
.bb-who{font-size:12px;font-weight:600;color:var(--acc)}.bb-lab{font-size:16px;line-height:1.3}
.bb-val{font-family:var(--f-display);font-size:34px;line-height:1}.bb-val.tl-slot{font-family:var(--f-body);font-size:15px;font-weight:600;letter-spacing:.08em;padding:6px 12px}
.bb-worst{font-size:13px;font-weight:600;color:var(--red)}
.bb-tag[data-state="outcome"]{border-color:var(--red)}.bb-tag[data-state="outcome"] .bb-val{color:var(--red)}
.bb-mid{display:flex;flex-direction:column;align-items:center;gap:8px}
.bb-gap{width:100%;border:2px dashed var(--red);border-bottom:0;height:18px;position:relative}
.bb-gap span{position:absolute;left:50%;top:-12px;transform:translateX(-50%);background:var(--ground);padding:0 8px;font-size:12px;font-weight:700;color:var(--red);white-space:nowrap}
.bb-beds{display:flex;align-items:center;gap:10px}.bb-beds i{font-style:normal;color:var(--muted)}
.bb-bedlab{display:flex;justify-content:space-between;width:100%;font-size:11px;color:var(--muted)}
/* receipt */
.rc-paper{background:var(--card);border:2px solid var(--ink);padding:18px 22px 20px;max-width:760px;position:relative;
 -webkit-mask:conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) bottom/18px 9px repeat-x,linear-gradient(#000 0 0) top/100% calc(100% - 9px) no-repeat;
 mask:conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) bottom/18px 9px repeat-x,linear-gradient(#000 0 0) top/100% calc(100% - 9px) no-repeat;padding-bottom:30px}
.rc-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;border-bottom:2px dashed var(--muted);padding-bottom:10px;margin-bottom:6px}
.rc-sub{font-size:12.5px;color:var(--muted)}
.rc-lines{display:flex;flex-direction:column}
.rc-line{display:grid;grid-template-columns:26px minmax(0,1.3fr) minmax(20px,.4fr) minmax(150px,1fr);align-items:center;gap:10px;padding:10px 8px;border-bottom:1px solid var(--faint);border-radius:6px;cursor:pointer}
.rc-no{font-weight:700;color:var(--acc)}.rc-lab{display:flex;flex-direction:column}.rc-lab b{font-size:15px;line-height:1.3}.rc-lab small{font-size:12px;color:var(--muted)}
.rc-lead{border-bottom:2px dotted var(--muted);height:0;align-self:end;margin-bottom:12px}
.rc-total{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-top:12px;padding-top:12px;border-top:3px double var(--ink)}
.rc-total span{font-weight:600}.rc-total b{font-family:var(--f-display);font-size:26px;color:var(--red)}.rc-total b.is-done{color:var(--green)}
/* bed-count */
.bc-top{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.bc-from{display:flex;align-items:baseline;gap:10px}.bc-from b{font-size:54px;line-height:1}.bc-from span{font-size:14px;color:var(--muted);max-width:180px}
.bc-arrow{font-size:26px;color:var(--muted)}
.bc-beds{display:grid;grid-template-columns:repeat(21,minmax(0,1fr));gap:6px;padding:14px;background:var(--card);border:2px solid var(--ink)}
.bc-bed{position:relative;display:flex;justify-content:center}.bc-bed i{position:absolute;left:50%;bottom:-4px;width:70%;height:3px;transform:translateX(-50%);background:var(--red)}
.bc-cap{margin:-4px 0 0;font-size:13px;color:var(--muted)}
.bc-slider{display:flex;flex-direction:column;gap:6px;max-width:520px}
.bc-slider label{display:flex;justify-content:space-between;align-items:baseline;gap:10px}.bc-h{font-family:var(--f-display);font-size:28px}
.bc-slider input{width:100%;accent-color:var(--ink);min-height:32px}
.bc-scale{display:flex;justify-content:space-between;font-size:12px;color:var(--muted)}
.bc-reads{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.bc-cell{display:flex;flex-direction:column;min-width:0}
.bc-read{display:flex;flex-direction:column;align-items:flex-start;gap:6px;text-align:left;background:#16222F;color:#E8EEF6;border:2px solid var(--ink);border-radius:8px;padding:14px 16px;font:inherit;height:100%}
.bc-read .tj-label{color:#AFC0D6}.bc-read small{font-size:12.5px;color:#AFC0D6}
.bc-v{font-family:var(--f-display);font-size:38px;line-height:1;color:#F1D493}
.bc-read[data-state="outcome"]{box-shadow:inset 0 -5px 0 var(--red)}
.lp .bc-read.is-up,.tj .bc-read.is-up{background:#16222F!important}
/* evidence-board */
.eb-board{background:#E9DCC4;background-image:radial-gradient(rgba(90,60,30,.16) 1px,transparent 1.4px);background-size:9px 9px;border:9px solid #7B5B3E;border-radius:8px;padding:16px 18px 24px}
.eb-banner{display:inline-block;background:var(--ink);color:#F3F1EA;font-weight:600;font-size:13.5px;padding:7px 14px;border-radius:3px;margin-bottom:18px}
.eb-row{position:relative;display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:14px;align-items:start}
.eb-thread{position:absolute;left:8%;right:8%;top:6px;border-top:2px solid #A33A2A;z-index:1}
.eb-cell{position:relative;z-index:2;display:flex;flex-direction:column;min-width:0}
.eb-card{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:6px;text-align:left;background:#FFFDF7;border:0;border-radius:2px;padding:22px 14px 14px;transform:rotate(var(--r));box-shadow:0 6px 12px -6px rgba(60,40,20,.5);font:inherit;color:#1A2B45}
.eb-card.is-up{transform:rotate(0) translateY(-5px)}
.eb-pin{position:absolute;left:50%;top:-4px;width:16px;height:16px;margin-left:-8px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#E7635A,#8E2F1C);box-shadow:0 2px 3px rgba(0,0,0,.35)}
.eb-no{font-size:12px;font-weight:700;color:#2F5E9E}.eb-f{font-size:15px;line-height:1.3}
.eb-q{font-family:var(--f-hand);font-weight:700;font-size:21px;line-height:1.1;color:#6B4F16}.eb-card small{font-size:11.5px;color:#475672}
/* rule-loop */
.rl-feeds{display:flex;flex-direction:column;gap:8px}.rl-feeds>div{display:flex;flex-wrap:wrap;gap:6px}
.rl-chip{font-size:12.5px;font-weight:600;padding:4px 10px;border-radius:14px;border:1.5px solid var(--ink);background:var(--card)}
.rl-wrap{position:relative;aspect-ratio:16/9;max-width:860px;width:100%;margin:6px auto 0}
.rl-ring{position:absolute;inset:0;width:100%;height:100%}
.rl-ring path{fill:none;stroke:var(--acc);stroke-width:3.5;stroke-dasharray:10 7}.rl-ring marker path{fill:var(--acc);stroke:none}
.rl-rule{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:36%;display:flex;flex-direction:column;gap:6px;text-align:center;background:var(--ink);color:#F3F1EA;border-radius:12px;padding:16px 18px;box-shadow:0 0 0 5px var(--ground),0 0 0 7px var(--gold)}
.rl-rk{font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold)}.rl-rule b{font-size:16px;line-height:1.4}.rl-from{font-size:12px;opacity:.85}
.rl-node{position:absolute;width:26%;display:flex;flex-direction:column}
.rl-p1{left:50%;top:0;transform:translateX(-50%)}.rl-p2{right:0;top:50%;transform:translateY(-50%)}.rl-p3{left:50%;bottom:0;transform:translateX(-50%)}.rl-p4{left:0;top:50%;transform:translateY(-50%)}
.rl-card{display:flex;flex-direction:column;align-items:flex-start;gap:6px;text-align:left;background:var(--card);border:2px solid var(--ink);border-radius:10px;padding:12px 14px;font:inherit;color:inherit}
.rl-no{width:26px;height:26px;border-radius:50%;background:var(--acc);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.rl-card b{font-size:14.5px;line-height:1.35}.rl-clock{font-family:var(--f-display);font-size:22px;color:var(--acc)}
.rl-card[data-state="outcome"]{border-color:var(--red)}.rl-card[data-state="outcome"] .rl-no{background:var(--red)}.rl-card[data-state="outcome"] b{color:var(--red)}
.rl-then{display:none}
.rl-back{margin:0;display:flex;align-items:center;justify-content:center;gap:8px;font-size:13px;font-weight:600;color:var(--acc)}.rl-back span{font-size:20px}
/* scale */
.sc-grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:24px;align-items:center;background:var(--card);border:2px solid var(--ink);padding:16px 22px}
.sc-svg{width:100%;height:auto}
.sc-post{fill:var(--ink)}.sc-beam{stroke:var(--ink);stroke-width:8;stroke-linecap:round}.sc-cord{stroke:var(--ink);stroke-width:2}
.sc-pan{fill:var(--ground);stroke:var(--ink);stroke-width:3}.sc-heavy{fill:#F4E2C6;stroke:var(--st-target)}
.sc-n{font-family:var(--f-display);font-size:34px;text-anchor:middle;fill:var(--ink)}.sc-pin{fill:var(--gold);stroke:var(--ink);stroke-width:2}
.sc-labs{display:flex;justify-content:space-between;gap:16px;font-size:12.5px;color:var(--muted)}.sc-labs span{display:flex;flex-direction:column;max-width:48%}.sc-labs b{font-size:14px;color:var(--ink)}
.sc-labs span:last-child{text-align:right}
.sc-verdict{display:flex;flex-direction:column;gap:6px}.sc-verdict b{font-size:40px;line-height:1}
/* corridor */
.cd-hall{display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:14px;padding:18px 16px 0;background:var(--card);border:2px solid var(--ink);border-bottom:0}
.cd-cell{display:flex;flex-direction:column;min-width:0}
.cd-d{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;background:transparent;border:0;border-radius:10px;padding:8px 6px 12px;font:inherit;color:inherit}
.cd-plate{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:2px 8px;background:var(--ink);color:#F1D493;border-radius:3px}
.cd-door{width:64px;height:96px;perspective:200px}
.cd-frame{fill:#E9EEF5;stroke:var(--ink);stroke-width:3}.cd-panel{fill:#FDFDFE;stroke:var(--ink);stroke-width:2.5}.cd-inset{fill:none;stroke:var(--ink);stroke-width:1.5;opacity:.6}.cd-knob{fill:var(--gold)}
.cd-leaf{transform-origin:8px 48px;transition:transform .25s}
.cd-d.is-up .cd-leaf{transform:skewY(-6deg) scaleX(.72)}
.cd-d.is-up .cd-frame{fill:#FFF3D6}
.cd-name{font-size:14px;line-height:1.3}.cd-d small{font-size:12.5px;color:var(--muted);line-height:1.4}
.cd-floor{height:10px;background:repeating-linear-gradient(90deg,var(--ink) 0 22px,transparent 22px 30px);opacity:.25;margin-top:-2px}

/* ================= phone: every pickable item stacked, one above the other, never side by side ================= */
@container tj (max-width:699px){
 .ln-grid{grid-template-columns:1fr;gap:16px;justify-items:center}
 .ln-lens{width:270px}.ln-c b{font-size:24px}
 .ln-list{width:100%}
 .ds-head{display:none}
 .ds-row{grid-template-columns:1fr;gap:8px}
 .ds-cells{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
 .ds-cell em{display:block}
 .rt-line{grid-template-columns:1fr;gap:6px}
 .rt-end{flex-direction:row;max-width:none;gap:10px;justify-content:flex-start}
 .rt-stops{grid-template-columns:1fr}
 .rt-stops::before{left:17px;right:auto;top:0;bottom:0;border-top:0;border-left:5px dotted var(--ink)}
 .rt-stop{display:grid;grid-template-columns:34px minmax(0,1fr) auto;align-items:center;gap:12px;text-align:left;padding:10px 8px 10px 0}
 .rt-stop .rt-dot{grid-column:1;grid-row:1}.rt-stop .rt-name{grid-column:2;grid-row:1;max-width:none}.rt-stop .rt-chip{grid-column:3;grid-row:1;min-width:84px;font-size:20px}
 .rt-gap{position:static;transform:none;align-self:flex-start;margin:0 0 4px 46px;background:transparent}
 .sw-grid{grid-template-columns:1fr;justify-items:center;padding:14px}
 .sw-svg{max-width:210px}
 .bb-row{grid-template-columns:1fr;gap:10px}
 .bb-mid{padding:6px 0}
 .rc-paper{padding:14px 12px 28px}
 .rc-line{grid-template-columns:22px minmax(0,1fr);gap:6px 8px}
 .rc-lead{display:none}.rc-in{grid-column:1/-1}
 .bc-beds{grid-template-columns:repeat(9,minmax(0,1fr));padding:10px}
 .bc-from b{font-size:44px}
 .bc-reads{grid-template-columns:1fr;gap:10px}
 .eb-board{padding:12px 10px 18px;border-width:7px}
 .eb-row{grid-template-columns:1fr;gap:16px;padding-left:18px}
 .eb-thread{left:6px;right:auto;top:0;bottom:0;border-top:0;border-left:2px solid #A33A2A}
 .eb-card{transform:none}.eb-pin{left:-15px;top:14px;margin-left:0}
 .rl-wrap{aspect-ratio:auto;display:flex;flex-direction:column;gap:12px}
 .rl-ring{display:none}
 .rl-rule,.rl-node{position:static;transform:none;width:100%}
 .rl-then{display:block;text-align:center;font-size:20px;color:var(--acc);line-height:1;margin-top:8px}
 .sc-grid{grid-template-columns:1fr;padding:12px}
 .sc-verdict b{font-size:32px}
 .cd-hall{grid-template-columns:1fr;gap:10px;padding:12px;background:var(--card)}
 .cd-d{display:grid;grid-template-columns:48px minmax(0,1fr);grid-template-rows:auto auto auto;gap:2px 12px;text-align:left;align-items:start;padding:8px}
 .cd-door{grid-row:1/span 3;width:44px;height:66px}
 .cd-plate{justify-self:start}
}
'''
