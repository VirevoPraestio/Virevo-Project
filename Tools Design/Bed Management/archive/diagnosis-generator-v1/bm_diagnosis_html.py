#!/usr/bin/env python3
"""
bm_diagnosis_html — the Bed Management Diagnosis generator.

Claude (through the API) writes a response spec: JSON with the turn (and the user's message), the chat parts
(text, Tojo's note, @points, one question, the three prompts) and the canvas blocks with their slots. This
generator validates the spec against registry.json and draws it offline in the Bed Management Diagnosis look
(the morning count). No model writes HTML.

Rules baked in here, not left to the spec:
  * Background theme from the turn number, in sets of four (turns 1-4 base, 5-8 the second theme, ...).
    A fill-in-the-blank redraw keeps the theme of the turn it redraws.
  * Every turn looks different: a main block is used by one turn only, and no block but heading and effect
    appears in two turns in a row (the redraw pair excepted, and it must add a block of its own).
    The effect box changes its look with the turn number.
  * First pickable element raised on load with its box open; on a phone each box opens right under its
    element, on desktop one shared box.
  * Phone order: the user's message, Tojo's text, the drawing, then the note, question, points and prompts.

  python3 bm_diagnosis_html.py validate SPEC.json
  python3 bm_diagnosis_html.py render SPEC.json --view desktop|mobile -o OUT.html
  python3 bm_diagnosis_html.py build [SPEC_DIR] [-o OUT_DIR]   # every turn in turns.json, stacked in one file
  python3 bm_diagnosis_html.py prompt                          # the Bed Management Diagnosis part of the API system prompt
  python3 bm_diagnosis_html.py catalog
Standard library only.
"""
import argparse, copy, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BM = os.path.dirname(HERE)                     # tojo-html/bed-management
ROOT = os.path.dirname(BM)                     # tojo-html
sys.path[:0] = [BM, os.path.join(ROOT, 'diagnosis-html-generator'), os.path.join(ROOT, 'landing-common')]
import bm_common as C                          # noqa: E402  shared Bed Management shell, bed mark, selection
import diagnosis_html as dh                    # noqa: E402  shared slot checks and plain-English list (Discharge)
from preview import chat_parts                 # noqa: E402  the chat panel is the same in every place
from landing_common import embedded_fonts      # noqa: E402

REG_PATH = os.path.join(HERE, 'registry.json')
CSS_PATH = os.path.join(HERE, 'assets', 'bm-diagnosis.css')
GEN = 'bm_diagnosis_html 1.0'
TOOL, PLACE = 'Bed Management', 'Diagnosis'
e = C.e
ACC = '#2F5E9E'
DEFAULT_SPECS = os.path.join(BM, 'examples', 'diagnosis')
DEFAULT_OUT = os.path.join(ROOT, 'out', 'bed-management', 'diagnosis')
RAIL = ['#D6DDE8', '#E1E7EF', '#D8DEE9', '#DDE2EC', '#D6DCE6']

def load_registry():
    reg = json.load(open(REG_PATH, encoding='utf-8'))
    reg['plain_english'] = dh.load_registry()['plain_english']     # one plain-English list for every tool
    return reg

# ============================================================================================ theme
def turn_no(spec):
    m = re.search(r'(\d+)$', spec['turn'].get('id', '1'))
    return int(m.group(1)) if m else 1

def tone_of(spec, reg):
    """The background theme is a rule, not content: sets of four by turn number. canvas.tone only for a redraw."""
    if spec.get('canvas', {}).get('tone'):
        return spec['canvas']['tone']
    t = reg['tones']
    return t['rotation'][((max(turn_no(spec), 1) - 1) // t['set_size']) % len(t['rotation'])]

def theme(reg, tone):
    s = reg['tones']['list'][tone]
    return C.theme(s['ground'], s['card'], s['ink'], s['muted'], s['line'], s['soft'], s['grey'], RAIL, '6px', '--acc:%s' % ACC)

# ============================================================================================ pieces
SEL, BOX, CHEV = C.sel, C.box, C.CHEV

def face(grp, key, first, inner, cls='', tag='button', extra=''):
    return '<%s class="%s %s" type="button"%s>%s%s</%s>' % (tag, C.sel_cls(first), cls, SEL(grp, key, first, extra), inner, CHEV, tag)

def pt_attr(o):
    return ' data-pt="%d"' % o['point'] if o.get('point') else ''

def hint(t):
    return '<p class="bd-hint">%s</p>' % e(t)

def dbox(inner):
    return '<div class="bd-card">%s</div>' % inner

def desk(boxes):
    return '<div class="bd-desk">%s</div>' % ''.join(boxes)

def src_tag(s):
    return '<span class="bm-tag %s">%s</span>' % ({'yours': 'yours', 'derived': 'yours', 'estimate': 'guess'}[s],
                                                    {'yours': 'Your number', 'derived': 'Worked out from yours', 'estimate': 'Tojo’s guess'}[s])

def arc(cx, cy, r, h0, h1):
    a0, a1 = (h0 / 24.0) * 2 * math.pi - math.pi / 2, (h1 / 24.0) * 2 * math.pi - math.pi / 2
    x0, y0, x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0), cx + r * math.cos(a1), cy + r * math.sin(a1)
    return 'M%.1f %.1fA%d %d 0 %d 1 %.1f %.1f' % (x0, y0, r, r, 1 if (h1 - h0) > 12 else 0, x1, y1)

def at(cx, cy, r, h):
    a = (h / 24.0) * 2 * math.pi - math.pi / 2
    return cx + r * math.cos(a), cy + r * math.sin(a)

def hr(h):
    h = h % 24
    return '%d %s' % (12 if h % 12 == 0 else h % 12, 'AM' if h < 12 else 'PM') if h not in (0, 12) else ('Midnight' if h == 0 else 'Noon')

# ============================================================================================ blocks
def r_heading(b, n):
    return '<header class="bd-head"><div class="bd-eye">%s</div><h2 class="bd-title">%s</h2>%s</header>' % (
        e(b['eyebrow']), e(b['title']), '<p class="bd-deck">%s</p>' % e(b['deck']) if b.get('deck') else '')

def r_revenue_dial(b, n):
    cx = cy = 150; R = 118
    s0, s1 = b['stops_billing_at'], b['starts_billing_at']
    svg = ['<svg class="rd-svg" viewBox="0 0 300 300" role="img" aria-label="A day on one bed. %s until %s, %s until %s.">' % (
        e(b['labels']['billing']), hr(s0), e(b['labels']['dead']), hr(s1))]
    svg.append('<circle cx="150" cy="150" r="%d" class="rd-ring"/>' % R)
    for h in range(24):
        x0, y0 = at(cx, cy, R + 14, h); x1, y1 = at(cx, cy, R + (22 if h % 6 == 0 else 18), h)
        svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="rd-tick%s"/>' % (x0, y0, x1, y1, ' big' if h % 6 == 0 else ''))
    svg.append('<path d="%s" class="rd-on"/>' % arc(cx, cy, R, 6, s0))
    svg.append('<path d="%s" class="rd-off"/>' % arc(cx, cy, R, s0, s1))
    svg.append('<path d="%s" class="rd-on"/>' % arc(cx, cy, R, s1, 24))
    for h, lab in ((0, 'Midnight'), (6, '6 AM'), (12, 'Noon'), (18, '6 PM')):
        x, y = at(cx, cy, R - 42, h)
        svg.append('<text x="%.1f" y="%.1f" class="rd-hr">%s</text>' % (x, y + 4, lab))
    for i, s in enumerate(b['stops']):
        x, y = at(cx, cy, R, s['at'])
        svg.append('<g class="rd-m m-%s%s"><circle cx="%.1f" cy="%.1f" r="15"/><text x="%.1f" y="%.1f">%d</text></g>' % (
            e(s['key']), ' is-out' if s.get('outcome') else '', x, y, x, y + 5, i + 1))
    svg.append('<text x="150" y="140" class="rd-c1">One bed</text><text x="150" y="164" class="rd-c2">one day</text></svg>')
    stops, boxes = [], []
    for i, s in enumerate(b['stops']):
        first = i == 0
        inner = dbox('<span class="bd-k">%s · %s</span><b>%s</b><p>%s</p><p class="rd-bill">%s</p>' % (
            e(s['when']), hr(s['at']), e(s['title']), e(s['detail']), e(s['bill'])))
        bed = {'in': 'rd-bed-in', 'empty': 'rd-bed-empty', 'next': 'rd-bed-next'}[s['bed']]
        stops.append(face('rd', s['key'], first, '<span class="rd-n">%d</span><span class="rd-tx"><span class="rd-w">%s</span><b>%s</b><span>%s</span></span><span class="bmb %s">%s</span>' % (
            i + 1, e(s['when']), e(s['title']), e(s['line']), bed, C.bed_svg(34)), 'rd-stop%s' % (' is-out' if s.get('outcome') else ''), extra=pt_attr(s)) + BOX('rd', s['key'], inner, first, 'mob'))
        boxes.append(BOX('rd', s['key'], inner, first, 'desk'))
    legend = ('<div class="rd-key"><span><i class="k-on"></i>%s</span><span><i class="k-off"></i>%s</span><span><i class="k-on"></i>%s</span></div>' % (
        e(b['labels']['billing']), e(b['labels']['dead']), e(b['labels']['again'])))
    return ('<section class="bd-blk rd" data-selroot="rd" data-cur="%s"><div class="rd-grid"><div class="rd-dial">%s%s</div><div class="rd-stops">%s</div></div>%s%s'
            '<p class="bd-rule">%s</p></section>') % (e(b['stops'][0]['key']), ''.join(svg), legend, ''.join(stops), hint('Tap a numbered step to see what happens on the bed.'), desk(boxes), e(b['caption']))

CLIP_SVG = '<svg class="cb-clip" viewBox="0 0 120 44" aria-hidden="true"><rect x="22" y="10" width="76" height="30" rx="6"/><rect x="44" y="2" width="32" height="16" rx="8" class="h"/></svg>'
def r_clipboard(b, n):
    rows, boxes = [], []
    first_key = next((i['key'] for i in b['items'] if i.get('now')), b['items'][0]['key'])
    for i, it in enumerate(b['items']):
        first = it['key'] == first_key
        inner = dbox('<span class="bd-k">%s</span><p class="cb-q">%s</p><span class="cb-when">%s</span>' % (
            e(it['name']), e(it['ask']), 'I’m asking this one now.' if it.get('now') else 'I’ll ask this one later, one at a time.'))
        rows.append(face('cb', it['key'], first, '<span class="cb-box%s" aria-hidden="true"></span><span class="cb-no">%d</span><b>%s</b><span class="cb-st">%s</span>' % (
            ' is-now' if it.get('now') else '', i + 1, e(it['name']), 'Asking now' if it.get('now') else 'Later'), 'cb-row%s' % (' is-now' if it.get('now') else ''), extra=pt_attr(it))
            + BOX('cb', it['key'], inner, first, 'mob'))
        boxes.append(BOX('cb', it['key'], inner, first, 'desk'))
    board = '<div class="cb-board">%s<div class="cb-paper"><div class="cb-title">%s</div><div class="cb-rows">%s</div><p class="cb-foot">%s</p></div></div>' % (
        CLIP_SVG, e(b['title']), ''.join(rows), e(b['footer']))
    return '<section class="bd-blk cb"><div class="cb-grid">%s<div class="cb-side">%s%s</div></div></section>' % (board, hint('Tap a line to see the question I’ll ask there.'), desk(boxes))

SUNS = ['<circle cx="12" cy="17" r="4"/><path d="M3 20h18M12 9v2M5.5 12l1.4 1.4M18.5 12l-1.4 1.4"/>',
        '<circle cx="12" cy="10" r="4"/><path d="M12 2v2M12 16v2M4 10H2M22 10h-2M6.3 4.3l1.4 1.4M17.7 4.3l-1.4 1.4M3 21h18"/>',
        '<path d="M7 18a5 5 0 0110 0"/><path d="M3 20h18M12 9v2M5 13l1.4 1.4M19 13l-1.4 1.4"/>']
def r_pattern_pair(b, n):
    labels = ''.join('<div class="pp-rl">%s<span>%s</span></div>' % (C.ico(SUNS[i], 'currentColor', 22), e(r)) for i, r in enumerate(b['rows']))
    cols, boxes = [], []
    for i, p in enumerate(b['patterns']):
        first = i == 0
        steps = ''.join('<span class="pp-step"><i class="pp-when">%s</i>%s</span>' % (e(b['rows'][j]), e(s)) for j, s in enumerate(p['steps']))
        inner = dbox('<span class="bd-k">%s · %s</span><p>%s</p>' % (e(p['name']), e(p['tag']), e(p['detail'])))
        cols.append(face('pp', p['key'], first, '<span class="pp-top"><b>%s</b><span>%s</span></span><span class="pp-steps">%s</span>' % (
            e(p['name']), e(p['tag']), steps), 'pp-col pp-%s' % e(p['key'])) + BOX('pp', p['key'], inner, first, 'mob'))
        boxes.append(BOX('pp', p['key'], inner, first, 'desk'))
    return '<section class="bd-blk pp"><div class="pp-grid"><div class="pp-labels"><div class="pp-rl0"></div>%s</div>%s</div>%s%s</section>' % (
        labels, ''.join(cols), hint('Tap a pattern. Read across each row to compare the same moment of the day.'), desk(boxes))

def r_admission_line(b, n):
    blank = b['mode'] == 'blank'
    pos = [('r', 1, 1), ('lr', 2, 1), ('l dn', 3, 1), ('l', 3, 2), ('r', 2, 2)]
    items, boxes = [], []
    for i, s in enumerate(b['stages']):
        first = i == 0
        lines, col, row = pos[i]
        if blank:
            tm = '<span class="al-blank" aria-label="time to fill in">hh : mm</span>'
            more = '<button type="button" class="al-say" data-say data-text="Step %d, %s: ">Add my time for this step</button>' % (i + 1, e(s['name'].lower()))
        else:
            tm = '<span class="al-typ">%s</span>%s' % (e(s.get('typical', '')), '<span class="al-worst">Worst: %s</span>' % e(s['worst']) if s.get('worst') else '')
            more = ''
        inner = dbox('<span class="bd-k">Step %d</span><b>%s</b><p>%s</p>%s%s' % (
            i + 1, e(s['name']), e(s['what']), '' if blank else '<p class="al-bt">Typical: %s%s</p>' % (e(s.get('typical', '')), ' · Worst: %s' % e(s['worst']) if s.get('worst') else ''), more))
        items.append(face('al', s['key'], first, '<span class="al-dot">%d</span><b class="al-nm">%s</b>%s' % (i + 1, e(s['name']), tm),
                          'al-s %s%s' % (lines, ' is-out' if s.get('outcome') else ''), extra=' style="grid-column:%d;grid-row:%d"' % (col, row))
                     + BOX('al', s['key'], inner, first, 'mob'))
        boxes.append(BOX('al', s['key'], inner, first, 'desk'))
    key = ('<div class="al-key" style="grid-column:1;grid-row:2"><span class="al-blank sm">hh : mm</span> is your time to fill in.%s</div>' % (
        ' Tap a step, then add your time.' if blank else '')) if blank else (
        '<div class="al-key" style="grid-column:1;grid-row:2"><span class="al-typ sm">Top</span> is a typical day. <span class="al-worst sm">Worst</span> is beneath it.</div>')
    return '<section class="bd-blk al al-m-%s"><div class="al-grid">%s%s</div>%s%s%s</section>' % (
        e(b['mode']), ''.join(items), key, hint('Tap a step to see what it covers.'), desk(boxes), '<p class="bd-rule">%s</p>' % e(b['caption']) if b.get('caption') else '')

def fmt_h(h):
    w, f = int(h), h - int(h)
    return ('%d' % w if w else '') + ('½' if abs(f - .5) < .01 else '') + (' hour' if h == 1 else ' hours')

def r_time_split(b, n):
    tot = sum(p['hours'] for p in b['parts'])
    segs, boxes = [], []
    for i, p in enumerate(b['parts']):
        first = i == 0
        inner = dbox('<span class="bd-k">%s · %s</span><p>%s</p>' % (e(p['label']), fmt_h(p['hours']), e(p['detail'])))
        segs.append(face('ts', str(i), first, '<b>%s</b><span>%s</span>' % (fmt_h(p['hours']), e(p['label'])), 'ts-seg ts-%s' % p['kind'],
                         extra=' style="flex-grow:%s"' % p['hours']) + BOX('ts', str(i), inner, first, 'mob'))
        boxes.append(BOX('ts', str(i), inner, first, 'desk'))
    return '<section class="bd-blk ts"><div class="ts-top"><b>%s</b><span>%s in all</span></div><div class="ts-bar">%s</div>%s<p class="bd-rule">%s</p></section>' % (
        e(b['title']), fmt_h(tot), ''.join(segs), desk(boxes), e(b['caption']))

def r_bill_slips(b, n):
    blank = b['mode'] == 'blank'
    out, boxes = [], []
    for i, s in enumerate(b['slips']):
        first = i == 0
        if blank:
            val = '<span class="bs-blank">hh : mm</span>'
            more = '<button type="button" class="al-say" data-say data-text="%s: ">Add this time</button>' % e(s['label'])
        else:
            val = '<span class="bs-val">%s</span>%s' % (e(s['value']), '<span class="bs-worst">%s</span>' % e(s['worst']) if s.get('worst') else '')
            more = ''
        inner = dbox('<span class="bd-k">%s</span><b>%s</b><p>%s</p>%s' % (e(s['who']), e(s['label']), e(s['detail']), more))
        out.append(face('bs', s['key'], first, '<span class="bs-head"><span class="bs-who">%s</span><span class="bs-no">Bill %d</span></span><b class="bs-lab">%s</b><span class="bs-line"></span><span class="bs-line short"></span>%s' % (
            e(s['who']), i + 1, e(s['label']), val), 'bs-slip%s' % (' is-out' if s.get('outcome') else '')) + BOX('bs', s['key'], inner, first, 'mob'))
        boxes.append(BOX('bs', s['key'], inner, first, 'desk'))
    arrow = '<div class="bs-arrow" aria-hidden="true"><span>%s</span><svg viewBox="0 0 120 24"><path d="M2 12h108"/><path d="M100 4l12 8-12 8"/></svg></div>' % e(b['arrow'])
    caps = ''.join('<p>%s</p>' % e(c) for c in b.get('captions', []))
    return '<section class="bd-blk bs bs-m-%s"><div class="bs-row">%s%s%s</div>%s%s%s</section>' % (
        e(b['mode']), out[0], arrow, out[1], hint('Tap a bill to see which time it asks for.' if blank else 'Tap a bill to see its time.'), desk(boxes),
        '<div class="bs-caps">%s</div>' % caps if caps else '')

def mins(t):
    h, m = t.split(':'); return int(h) * 60 + int(m)

def r_gap_ruler(b, n):
    lo, hi = 10 * 60, 21 * 60
    x = lambda t: 100.0 * (mins(t) - lo) / (hi - lo)
    ticks = ''.join('<span class="gr-t%s" style="left:%.2f%%"><i>%s</i></span>' % (' big' if h % 3 == 0 else '', 100.0 * (h * 60 - lo) / (hi - lo), hr(h) if h % 2 == 0 else '') for h in range(10, 22))
    a, u, w = x(b['from']), x(b['to']), x(b['worst_to'])
    bar = ('<div class="gr-track">%s<span class="gr-gap" style="left:%.2f%%;width:%.2f%%"></span><span class="gr-more" style="left:%.2f%%;width:%.2f%%"></span>'
           '<span class="gr-pin gr-a" style="left:%.2f%%"><b>%s</b></span><span class="gr-pin gr-u" style="left:%.2f%%"><b>%s</b></span><span class="gr-pin gr-w" style="left:%.2f%%"><b>%s</b></span></div>') % (
        ticks, a, u - a, u, w - u, a, e(b['from_label']), u, e(b['to_label']), w, e('Worst day'))
    sw = ('<div class="gr-sw" role="group" aria-label="Which day"><button type="button" class="gr-b" data-gr="usual" aria-pressed="true">Usual day</button>'
          '<button type="button" class="gr-b" data-gr="worst" aria-pressed="false">Worst day</button></div>')
    read = '<p class="gr-read"><span class="gr-r-usual">%s</span><span class="gr-r-worst">%s</span></p>' % (e(b['usual']), e(b['worst']))
    return '<section class="bd-blk gr" data-gr-state="usual"><div class="gr-top"><b>The gap, on your clock</b>%s</div>%s%s</section>' % (sw, bar, read)

def r_figure_cards(b, n):
    cards, boxes = [], []
    for i, it in enumerate(b['items']):
        first = i == 0
        inner = dbox('<span class="bd-k">Figure %d</span><b>%s</b><p>%s</p><button type="button" class="al-say" data-say data-text="%s: ">Add this figure</button>' % (
            i + 1, e(it['name']), e(it['turns_into']), e(it['name'])))
        cards.append('<div class="fc-cell">%s%s</div>' % (face('fc', it['key'], first, '<span class="fc-no">%d</span><b>%s</b><span class="fc-field"><span>%s</span></span><span class="bm-tag need">Need from you</span>' % (
            i + 1, e(it['name']), e(it['unit'])), 'fc-card', extra=pt_attr(it)), BOX('fc', it['key'], inner, first, 'mob')))
        boxes.append(BOX('fc', it['key'], inner, first, 'desk'))
    return '<section class="bd-blk fc"><div class="fc-grid">%s</div>%s%s</section>' % (''.join(cards), hint('Tap a card to see what that figure turns into.'), desk(boxes))

def r_step_ledger(b, n):
    steps, boxes = [], []
    for i, s in enumerate(b['steps']):
        first = i == 0
        inner = dbox('<span class="bd-k">Step %d · %s</span><b>%s</b><p>%s</p>%s' % (i + 1, e(s['label']), e(s['value']), e(s['how']), src_tag(s['source'])))
        steps.append('<div class="sl-step" style="--i:%d">%s%s</div>' % (i, face('sl', s['key'], first, '<span class="sl-no">%d</span><span class="sl-tx"><span class="sl-lab">%s</span><b class="sl-val">%s</b></span>' % (
            i + 1, e(s['label']), e(s['value'])), 'sl-card%s' % (' is-out' if s.get('outcome') else '')), BOX('sl', s['key'], inner, first, 'mob')))
        boxes.append(BOX('sl', s['key'], inner, first, 'desk'))
    return '<section class="bd-blk sl"><div class="sl-stair">%s</div>%s%s<p class="bd-rule">%s</p></section>' % (
        ''.join(steps), hint('Tap a step to see the working.'), desk(boxes), e(b['condition']))

def r_pin_board(b, n):
    cards, boxes = [], []
    for i, c in enumerate(b['cards']):
        first = i == 0
        inner = dbox('<span class="bd-k">Finding %d · from you</span><b>%s</b><p class="pb-from">%s</p><p>%s</p>' % (i + 1, e(c['text']), e(c['from']), e(c['detail'])))
        cards.append('<div class="pb-cell" style="--r:%s">%s%s</div>' % (['-1.6deg', '1.1deg', '-0.6deg', '1.5deg', '-1.2deg', '0.8deg'][i % 6], face('pb', c['key'], first,
            '<span class="pb-pin" aria-hidden="true"></span><span class="pb-no">%d</span><b>%s</b><span class="pb-src">%s</span>' % (i + 1, e(c['text']), e(c['from'])), 'pb-card', extra=pt_attr(c)),
            BOX('pb', c['key'], inner, first, 'mob')))
        boxes.append(BOX('pb', c['key'], inner, first, 'desk'))
    return '<section class="bd-blk pb"><div class="pb-board"><div class="pb-banner">%s</div><div class="pb-grid">%s</div></div>%s%s</section>' % (
        e(b['banner']), ''.join(cards), hint('Tap a card to see which of your answers it came from.'), desk(boxes))

def r_rule_loop(b, n):
    nodes, boxes = [], []
    for i, s in enumerate(b['steps']):
        first = i == 0
        inner = dbox('<span class="bd-k">Then %d</span><b>%s</b><p>%s</p>%s' % (i + 1, e(s['text']), e(s['detail']), '<p class="rl-clk">%s</p>' % e(s['clock']) if s.get('clock') else ''))
        nodes.append('<div class="rl-node rl-n%d">%s%s</div>' % (i + 1, face('rl', s['key'], first, '<span class="rl-no">%d</span><b>%s</b>%s' % (
            i + 1, e(s['text']), '<span class="rl-clock">%s</span>' % e(s['clock']) if s.get('clock') else ''), 'rl-card%s' % (' is-out' if s.get('outcome') else ''), extra=pt_attr(s)),
            BOX('rl', s['key'], inner, first, 'mob')))
        boxes.append(BOX('rl', s['key'], inner, first, 'desk'))
    ring = ('<svg class="rl-ring" viewBox="0 0 400 300" preserveAspectRatio="none" aria-hidden="true"><ellipse cx="200" cy="150" rx="160" ry="112"/>'
            '')
    rule = '<div class="rl-rule"><span class="rl-rk">The rule</span><b>%s</b><span class="rl-from">%s</span></div>' % (e(b['rule']), e(b['rule_from']))
    back = '<div class="rl-back"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M4 12a8 8 0 1 0 3-6.2"/><path d="M3 3v5h5"/></svg>%s</div>' % e(b['back'])
    return '<section class="bd-blk rl"><div class="rl-wrap">%s%s%s</div>%s%s%s</section>' % (ring, rule, ''.join(nodes), back, hint('Tap a step to follow the loop.'), desk(boxes))

def r_effect(b, n, reg=None):
    styles = (reg or load_registry())['variety']['effect_styles']
    st = styles[(n // 2) % len(styles)]
    return '<section class="bd-blk ef ef-%s%s"><span class="ef-l">%s</span><b class="ef-v">%s</b><span class="ef-s">%s</span></section>' % (
        st, ' is-out' if b.get('outcome') else '', e(b['label']), e(b['value']), e(b['sub']))

RENDER = {'heading': r_heading, 'revenue-dial': r_revenue_dial, 'clipboard': r_clipboard, 'pattern-pair': r_pattern_pair,
          'admission-line': r_admission_line, 'time-split': r_time_split, 'bill-slips': r_bill_slips, 'gap-ruler': r_gap_ruler,
          'figure-cards': r_figure_cards, 'step-ledger': r_step_ledger, 'pin-board': r_pin_board, 'rule-loop': r_rule_loop, 'effect': r_effect}

# ============================================================================================ validation
SIMPLE = {'via': 'through', 'ensure': 'make sure', 'prior to': 'before', 'additional': 'more', 'approximately': 'about', 'utilise': 'use',
          'numerous': 'many', 'obtain': 'get', 'require': 'need', 'requires': 'needs', 'regarding': 'about', 'assist': 'help', 'initiate': 'start',
          'component': 'part', 'components': 'parts', 'implement': 'put in place', 'optimal': 'best', 'visibility': 'a clear view',
          'enable': 'let', 'enables': 'lets', 'allocate': 'give', 'allocated': 'given', 'allocation': 'giving a bed', 'isolated': 'measured on its own',
          'documentation': 'paperwork', 'billable': 'charged', 'adequate': 'enough', 'diagnostics': 'tests and scans'}
SKIP_KEYS = {'id', 'type', 'register', 'tool', 'tab', 'context', 'source', 'status', 'mode', 'kind', 'key', 'user_tag', 'user_message', 'user_words',
             'transcript', 'redraw_of', 'tone', 'note_for_review', 'bed'}
MAX_SENTENCE = 20
DIRECTION = re.compile(r'\b(left|right|above|below|sidebar)\b', re.I)

def simple_check(spec):
    out = []
    allowed = {w.lower() for w in spec.get('turn', {}).get('user_words', [])}
    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k not in SKIP_KEYS: walk(v, '%s.%s' % (path, k) if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o): walk(v, '%s[%d]' % (path, i))
        elif isinstance(o, str) and o.strip():
            for sent in re.split(r'(?<=[.?!])\s+', o):
                if len(sent.split()) > MAX_SENTENCE: out.append('%s: a sentence of %d words; keep each under %d' % (path, len(sent.split()), MAX_SENTENCE + 1))
            if re.search(r'\s[—–]\s|;', o): out.append('%s: a dash or semicolon joins two thoughts; make two sentences' % path)
            if re.search(r'\btabs?\b', o, re.I): out.append('%s: never say “tab”; name the place' % path)
            if re.search(r'\bgraphic\b', o, re.I): out.append('%s: “graphic” → name the drawing (the clipboard, the two bills)' % path)
            low = ' %s ' % re.sub(r'[^a-z ]', ' ', o.lower())
            for w, rep in SIMPLE.items():
                if w not in allowed and ' %s ' % w in low: out.append('%s: “%s” → write “%s”' % (path, w, rep))
    walk({'chat': spec.get('chat', {}), 'canvas': spec.get('canvas', {})}, '')
    return out

def canvas_points(blocks):
    s = set()
    def walk(o):
        if isinstance(o, dict):
            if o.get('point'): s.add(int(o['point']))
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(blocks); return s

def validate(spec, reg=None):
    reg = reg or load_registry()
    by = {b['id']: b for b in reg['blocks']}
    errs, warns = [], []
    turn, chat, canvas = spec.get('turn', {}), spec.get('chat', {}), spec.get('canvas', {})
    for k in ('id', 'type', 'user_message'):
        if not turn.get(k): errs.append('turn.%s: required (the user’s message is recorded with every turn)' % k)
    if turn.get('tab', PLACE) != PLACE or turn.get('tool', TOOL) != TOOL:
        errs.append('turn: this generator draws %s · %s turns only' % (TOOL, PLACE))
    blocks = canvas.get('blocks', [])
    if not blocks or blocks[0].get('type') != 'heading': errs.append('canvas: first block must be "heading"')
    if sum(1 for b in blocks if b.get('type') == 'heading') > 1: errs.append('canvas: only one heading')
    if len(blocks) - 1 > reg['budget']['max_blocks']: errs.append('canvas: %d blocks after the heading, limit %d' % (len(blocks) - 1, reg['budget']['max_blocks']))
    if sum(1 for b in blocks if b.get('type') == 'effect') > 2: errs.append('canvas: at most two effect boxes')
    for i, b in enumerate(blocks):
        t = b.get('type'); path = 'canvas.blocks[%d](%s)' % (i, t)
        if t not in by: errs.append('%s: unknown block' % path); continue
        if by[t]['status'] in ('retired', 'changes_requested'): errs.append('%s: block is %s' % (path, by[t]['status']))
        dh.check_fields(path, by[t]['slots'], b, errs, warns)
        if turn.get('type') in ('question', 'data-ask') and t in reg['withheld_in_fact_turns']:
            errs.append('%s: not in a %s turn; money worked out is held back until the figures are in' % (path, turn.get('type')))
        if t in ('admission-line', 'bill-slips'):
            items = b.get('stages') or b.get('slips') or []
            for j, s in enumerate(items):
                has = s.get('typical') or s.get('value')
                if b.get('mode') == 'blank' and has: errs.append('%s[%d]: a blank field carries no time; leave it for the user' % (path, j))
                if b.get('mode') == 'filled' and not has: errs.append('%s[%d]: filled mode needs the user’s time' % (path, j))
        if t == 'gap-ruler':
            for f in ('from', 'to', 'worst_to'):
                if not re.match(r'^\d{1,2}:\d{2}$', str(b.get(f, ''))): errs.append('%s.%s: a time like 12:30' % (path, f))
        if t == 'revenue-dial' and not b.get('stops_billing_at', 0) < b.get('starts_billing_at', 0):
            errs.append('%s: billing must stop before it starts again' % path)
        rec = reg['turn_recipes'].get(turn.get('type'))
        if rec and t not in ('heading',) and t not in rec:
            warns.append('%s: not in the %s recipe %s' % (path, turn.get('type'), rec))
    tones = reg['tones']
    if canvas.get('tone'):
        if canvas['tone'] not in tones['list']: errs.append('canvas.tone: unknown %r' % canvas['tone'])
        if not turn.get('redraw_of'): errs.append('canvas.tone: only a redraw (turn.redraw_of) may set its theme by hand')
    s2 = copy.deepcopy(spec); s2['turn'].pop('user_message', None)
    errs += ['plain English: ' + p for p in dh.plain_check(s2, reg)]
    errs += ['simple English: ' + x for x in simple_check(spec)]
    prompts = chat.get('prompts', [])
    if len(prompts) != 3: errs.append('chat.prompts: exactly 3 predictive prompts, got %d' % len(prompts))
    text = chat.get('text', [])
    if isinstance(text, list) and len(text) > 3: errs.append('chat.text: at most 3 paragraphs')
    pts = chat.get('points', [])
    if pts and not 2 <= len(pts) <= 6: errs.append('chat.points: 2–6 points')
    cps = canvas_points(blocks)
    for i, p in enumerate(pts):
        if p.get('n') != i + 1: errs.append('chat.points[%d].n must be %d' % (i, i + 1))
        if p.get('canvas') and p['n'] not in cps: errs.append('chat.points[%d]: links to the canvas but no canvas item has point %d' % (i, p['n']))
    if chat.get('note') and dh.words(chat['note']) > 16: warns.append('chat.note: keep Tojo’s Note to one line (16 words)')
    for k in ('pointer', 'invite'):
        if chat.get(k) and DIRECTION.search(chat[k]): errs.append('chat.%s: never say where the drawing is; name it instead' % k)
    q = chat.get('question')
    if q and not 2 <= len(q.get('options', [])) <= 5: errs.append('chat.question.options: 2–5 options')
    return errs, warns

def book_check(specs, reg):
    """The rules that span turns: every turn looks different, and the theme follows the turn number."""
    errs = []
    rep = set(reg['variety']['repeatable'])
    main_of, types_of, ids = {}, {}, [s['turn']['id'] for s in specs]
    for s in specs:
        bl = [b['type'] for b in s['canvas']['blocks']]
        main_of[s['turn']['id']] = bl[1] if len(bl) > 1 else 'heading'
        types_of[s['turn']['id']] = set(bl)
    seen = {}
    for i, s in enumerate(specs):
        tid, rd = s['turn']['id'], s['turn'].get('redraw_of')
        m = main_of[tid]
        if rd:
            if rd not in main_of: errs.append('%s: redraw_of %s is not an earlier turn' % (tid, rd)); continue
            if m != main_of[rd]: errs.append('%s: a redraw reuses the main block of %s (%s), not %s' % (tid, rd, main_of[rd], m))
            if not (types_of[tid] - types_of[rd] - {'heading'}): errs.append('%s: a redraw must add at least one block %s did not have' % (tid, rd))
            want = tone_of(next(x for x in specs if x['turn']['id'] == rd), reg)
            if tone_of(s, reg) != want: errs.append('%s: a redraw keeps the theme of %s (%s); set canvas.tone to it' % (tid, rd, want))
        elif m in seen:
            errs.append('%s: main block %s is already used by %s; every turn must look different' % (tid, m, seen[m]))
        seen.setdefault(m, tid)
        if i:
            prev = specs[i - 1]['turn']['id']
            shared = (types_of[tid] & types_of[prev]) - rep
            if rd == prev: shared -= {m}
            if shared: errs.append('%s: shares %s with the turn before (%s); two turns in a row must not look alike' % (tid, ', '.join(sorted(shared)), prev))
    return errs

# ============================================================================================ pages
SEL_JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  function pick(g,k,scroll){
    $$('.js-sel[data-grp="'+g+'"]').forEach(function(o){var on=o.getAttribute('data-key')===k;o.classList.toggle('is-up',on);o.setAttribute('aria-expanded',on?'true':'false');});
    $$('[data-box^="'+g+':"]').forEach(function(b){b.hidden=b.getAttribute('data-box')!==g+':'+k;});
    $$('[data-selroot="'+g+'"]').forEach(function(r){r.setAttribute('data-cur',k);});
    if(scroll){var m=$$('.bx-mob[data-box="'+g+':'+k+'"]').filter(function(b){return b.offsetParent;})[0];if(m&&m.scrollIntoView)m.scrollIntoView({block:'nearest',behavior:'smooth'});}
  }
  $$('.js-sel').forEach(function(b){b.addEventListener('click',function(){pick(b.getAttribute('data-grp'),b.getAttribute('data-key'),true);});});
  $$('.gr').forEach(function(g){$$('.gr-b',g).forEach(function(b){b.addEventListener('click',function(){
    g.setAttribute('data-gr-state',b.getAttribute('data-gr'));$$('.gr-b',g).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});});});});
  function tell(){try{parent.postMessage({tojoH:document.documentElement.scrollHeight},'*');}catch(e){}}
  window.addEventListener('load',tell);
})();
'''

def css():
    return C.BED_CSS + open(CSS_PATH, encoding='utf-8').read()

def split_chat(chat):
    """Tojo's text on its own, then everything else (note, question, points, prompts)."""
    whole = chat_parts(chat)
    cut = whole.index('</div>') + len('</div>')
    return whole[:cut], whole[cut:]

def user_bubble(spec):
    t = spec['turn']
    tag = '<b>%s</b>' % e(t['user_tag']) if t.get('user_tag') else ''
    return '<div class="sh-um">%s%s</div>' % (tag, e(t['user_message']))

def render_canvas(spec, reg):
    n = turn_no(spec)
    inner = ''.join(r_effect(b, n, reg) if b['type'] == 'effect' else RENDER[b['type']](b, n) for b in spec['canvas']['blocks'])
    tone = tone_of(spec, reg); th = theme(reg, tone)
    paper = reg['tones']['list'][tone]['paper']
    return th, '<div class="lp-host"><div class="lp bd bd-paper-%s" data-tone="%s" data-turn="%s" data-generator="%s" style="%s">%s</div></div>' % (
        paper, tone, e(spec['turn']['id']), GEN, th['vars'], inner)

def render_page(spec, view, reg, fonts=True):
    th, canvas = render_canvas(spec, reg)
    text, rest = split_chat(spec['chat'])
    if view == 'desktop':
        body = C.desktop(th, PLACE, canvas, user_bubble(spec) + text + rest)
    else:
        body = C.mobile(th, PLACE, '@@CANVAS@@', '@@CHAT@@')
        body = body.replace('<div class="sh-mc">', '<div class="sh-mc">' + user_bubble(spec), 1)
        body = body.replace('@@CANVAS@@<div class="sh-mpanel">@@CHAT@@</div>',
                            '<div class="sh-mpanel bd-mt">%s</div>%s<div class="sh-mpanel bd-mr">%s</div>' % (text, canvas, rest))
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s · %s %s</title>%s<style>%s%s%s.bm-app .sh-bar{background:%s}%s%s%s</style></head><body>%s<script>%s%s</script></body></html>') % (
        e(spec['turn']['id']), TOOL, PLACE, embedded_fonts() if fonts else '', C.SHELL_CSS, C.shell_css(th), C.SHELL_V3_CSS, th['ground'],
        C.BASE_CSS, C.SEL_CSS, css(), body, C.JS, SEL_JS)

# ============================================================================================ the stacked book
BOOK_CSS = r'''
:root{--bg:#EEF1F5;--panel:#FFFFFF;--ink:#1A2B45;--muted:#56637C;--line:#CBD3DF;--accent:#2F5E9E;--gold:#B8862B}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151D;--panel:#19212C;--ink:#E6EBF2;--muted:#9BA8BA;--line:#2B3645;--accent:#8DB2E6;--gold:#E0B25A;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#10151D;--panel:#19212C;--ink:#E6EBF2;--muted:#9BA8BA;--line:#2B3645;--accent:#8DB2E6;--gold:#E0B25A;color-scheme:dark}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Poppins','Segoe UI',system-ui,sans-serif}
.bk{box-sizing:border-box;max-width:1880px;margin:0 auto;padding:22px 16px 80px}
.bk *,.bk *::before,.bk *::after{box-sizing:border-box}
.bk-top{border-bottom:1.5px solid var(--line);padding-bottom:14px;margin-bottom:8px}
.bk-top h1{margin:0;font-family:'Bebas Neue','Arial Narrow',sans-serif;font-weight:400;font-size:44px;line-height:.95}
.bk-top p{margin:6px 0 0;font-size:13.5px;line-height:1.55;color:var(--muted);max-width:980px}
.bk-jump{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.bk-jump a{font-size:12.5px;font-weight:600;color:var(--ink);text-decoration:none;border:1.5px solid var(--line);background:var(--panel);border-radius:16px;padding:5px 11px}
.bk-jump a:hover{border-color:var(--accent)}
.bk-turn{padding:34px 0 30px;border-bottom:1.5px dashed var(--line)}
.bk-head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px 24px;align-items:start;margin-bottom:14px}
.bk-id{font-family:'Bebas Neue','Arial Narrow',sans-serif;font-size:34px;line-height:1;margin:0}
.bk-id small{font-family:'Poppins',sans-serif;font-size:13px;font-weight:600;color:var(--accent);margin-left:10px;letter-spacing:.02em}
.bk-meta{display:flex;flex-wrap:wrap;gap:6px;justify-content:flex-end}
.bk-chip{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:12px;background:var(--panel);border:1.5px solid var(--line);white-space:nowrap}
.bk-chip i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:-1px;border:1px solid rgba(0,0,0,.25)}
.bk-rec{grid-column:1/-1;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.bk-box{background:var(--panel);border:1.5px solid var(--line);border-radius:8px;padding:10px 12px;font-size:13px;line-height:1.5}
.bk-box b{display:block;font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin-bottom:3px}
.bk-box ol{margin:0;padding-left:18px}
.bk-note{grid-column:1/-1;font-size:12.5px;color:var(--muted);margin:0}
.bk-views{display:grid;grid-template-columns:minmax(0,1fr) 410px;gap:20px;align-items:start}
.bk-lab{font-size:11.5px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.bk-screen{position:relative;width:100%;overflow:hidden;border-radius:10px;border:1.5px solid var(--line);background:#fff}
.bk-screen iframe{position:absolute;left:0;top:0;width:1440px;height:900px;border:0;transform-origin:0 0}
.bk-hand{width:410px;max-width:100%;border:10px solid #1b2129;border-radius:36px;overflow:hidden;background:#fff}
.bk-hand iframe{display:block;width:390px;height:844px;border:0}
@media (max-width:1180px){.bk-views{grid-template-columns:minmax(0,1fr)}.bk-rec{grid-template-columns:1fr}.bk-hand{justify-self:center}}
@media (max-width:640px){.bk-head{grid-template-columns:1fr}.bk-meta{justify-content:flex-start}.bk-hand{width:100%;border-width:6px;border-radius:24px}.bk-hand iframe{width:100%}}
'''
BOOK_JS = r'''
(function(){
  var T=JSON.parse(document.getElementById('bk-data').textContent),F=document.getElementById('bk-fonts').textContent;
  document.getElementById('bk-top-fonts').textContent=F;
  function doc(h){return h.replace('</head>','<style>'+F+'</style></head>');}
  function fit(){[].slice.call(document.querySelectorAll('.bk-screen')).forEach(function(s){var sc=Math.min(1,s.clientWidth/1440);var f=s.querySelector('iframe');f.style.transform='scale('+sc+')';s.style.height=Math.ceil(900*sc)+'px';});}
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){load(en.target);io.unobserve(en.target);}});},{rootMargin:'900px 0px'}):null;
  function load(sec){var t=T[sec.getAttribute('data-i')];[].slice.call(sec.querySelectorAll('iframe[data-v]')).forEach(function(f){if(!f.srcdoc)f.srcdoc=doc(t[f.getAttribute('data-v')]);});}
  [].slice.call(document.querySelectorAll('.bk-turn')).forEach(function(s){if(io)io.observe(s);else load(s);});
  fit();window.addEventListener('resize',fit);
})();
'''

def book(specs, reg, notes):
    from html import escape
    data, secs, jump = [], [], []
    for i, s in enumerate(specs):
        t = s['turn']; tone = tone_of(s, reg); tl = reg['tones']['list'][tone]
        blocks = [b['type'] for b in s['canvas']['blocks'][1:]]
        title = s['canvas']['blocks'][0]['title']
        data.append({'desktop': render_page(s, 'desktop', reg, fonts=False), 'mobile': render_page(s, 'mobile', reg, fonts=False)})
        q = s['chat'].get('question')
        rec = ('<div class="bk-rec"><div class="bk-box"><b>The user’s message</b>%s</div>'
               '<div class="bk-box"><b>The three prompts</b><ol>%s</ol></div>'
               '<div class="bk-box"><b>%s</b>%s</div></div>') % (
            e(t['user_message']), ''.join('<li>%s</li>' % e(p) for p in s['chat']['prompts']),
            'The question and its options' if q else 'Question', ('%s<ol>%s</ol>' % (e(q['text']), ''.join('<li>%s</li>' % e(o) for o in q['options']))) if q else 'None in this turn. The user answers in their own words.')
        src = t.get('transcript', {})
        chips = ['<span class="bk-chip">%s</span>' % e(src.get('label', '')), '<span class="bk-chip"><i style="background:%s"></i>%s</span>' % (tl['ground'], e(tl['name']))]
        chips += ['<span class="bk-chip">%s</span>' % e(b) for b in dict.fromkeys(blocks)]
        if t.get('redraw_of'): chips.append('<span class="bk-chip">Redraw of %s</span>' % e(t['redraw_of']))
        note = notes.get(t['id'], '')
        secs.append(('<section class="bk-turn" id="%s" data-i="%d"><div class="bk-head"><h2 class="bk-id">%s<small>%s</small></h2><div class="bk-meta">%s</div>%s%s</div>'
                     '<div class="bk-views"><div><div class="bk-lab">Desktop · 1440 × 900, scaled to fit · scroll inside it</div><div class="bk-screen"><iframe data-v="desktop" title="%s on desktop" loading="lazy"></iframe></div></div>'
                     '<div><div class="bk-lab">Phone · 390 × 844 · scroll inside it</div><div class="bk-hand"><iframe data-v="mobile" title="%s on a phone" loading="lazy"></iframe></div></div></div></section>') % (
            e(t['id']), i, e(t['id']), e(title), ''.join(chips), rec, '<p class="bk-note">%s</p>' % e(note) if note else '', e(t['id']), e(t['id'])))
        jump.append('<a href="#%s">%s</a>' % (e(t['id']), e(t['id'])))
    fonts = re.sub(r'</?style[^>]*>', '', embedded_fonts())
    intro = ('%d turns, stacked in conversation order. Each is drawn by %s from its spec, which records the user’s message, Tojo’s chat parts and the three prompts. '
             'The background theme changes every four turns. Every turn uses its own drawing, except a fill-in-the-blank and its answered redraw, which share one by rule.') % (len(specs), GEN)
    return ('<title>Bed Management Diagnosis Turns</title><style>%s</style><style id="bk-top-fonts"></style><script type="application/json" id="bk-data">%s</script><script type="text/plain" id="bk-fonts">%s</script>'
            '<div class="bk"><div class="bk-top"><h1>Bed Management · Diagnosis turns</h1><p>300-bed hospital, Nagpur. %s</p><nav class="bk-jump" aria-label="Turns">%s</nav></div>%s</div>'
            '<script>%s</script>') % (BOOK_CSS, json.dumps(data, ensure_ascii=False).replace('</', '<\\/'), fonts, e(intro), ''.join(jump), ''.join(secs), BOOK_JS)

# ============================================================================================ prompt
def slot_summary(slots):
    def one(s):
        t, opt = s['type'], '' if s.get('required', True) else '?'
        if t == 'text': return 'text≤%dw%s' % (s.get('max_words', 99), opt)
        if t == 'enum': return 'one of %s%s' % ('|'.join(s['values']), opt)
        if t in ('number', 'bool'): return t + opt
        if t == 'list': return ['%d–%d ×' % (s['min'], s['max']), one(s['item'])] + ([opt] if opt else [])
        if t == 'object': return {k + ('' if v.get('required', True) else '?'): one(v) for k, v in s['fields'].items()}
    return {k + ('' if v.get('required', True) else '?'): one(v) for k, v in slots.items()}

def catalog(reg):
    out = ['# Bed Management · Diagnosis canvas blocks (registry v%d, %s)\n' % (reg['registry_version'], reg['updated']),
           'First block is always `heading`. At most %d blocks after it.\n' % reg['budget']['max_blocks'],
           '**Themes.** %s\n' % reg['tones']['rule'], '**Every turn looks different.** %s\n' % reg['variety']['rule']]
    for b in reg['blocks']:
        out.append('## `%s` (%s · %s)\n%s\n- Use when: %s\n- Avoid when: %s\n- Slots: %s\n' % (
            b['id'], b['status'], b['scope'], b['purpose'], '; '.join(b['use_when']), '; '.join(b['avoid_when']), json.dumps(slot_summary(b['slots']), ensure_ascii=False)))
    out.append('## Recipes by turn type\n' + '\n'.join('- `%s`: %s' % (k, ', '.join(v)) for k, v in reg['turn_recipes'].items()))
    return '\n'.join(out)

def prompt(reg):
    tpl = open(os.path.join(ROOT, 'prompts', 'tojo-api-system-prompt.md'), encoding='utf-8').read()
    rules = open(os.path.join(ROOT, 'rules', '06-html-response-rules.md'), encoding='utf-8').read()
    extra = ('\n\n# This turn is in Bed Management · Diagnosis\nSet `turn.tool` to "Bed Management" and `turn.tab` to "Diagnosis". Record the user’s message in `turn.user_message`. '
             'Use the Bed Management Diagnosis catalogue below. Never repeat the main block of an earlier turn unless the turn redraws a fill-in-the-blank (set `turn.redraw_of`).\n\n')
    return tpl.replace('{{RULES_06}}', rules).replace('{{CATALOG}}', extra + catalog(reg))

# ============================================================================================ CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    v = sub.add_parser('validate'); v.add_argument('spec')
    r = sub.add_parser('render'); r.add_argument('spec'); r.add_argument('--view', default='desktop', choices=['desktop', 'mobile']); r.add_argument('-o', '--out')
    b = sub.add_parser('build'); b.add_argument('dir', nargs='?', default=DEFAULT_SPECS); b.add_argument('-o', '--out', default=DEFAULT_OUT)
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
    if a.cmd == 'build':
        man = json.load(open(os.path.join(a.dir, 'turns.json'), encoding='utf-8'))
        os.makedirs(a.out, exist_ok=True); specs, notes, bad = [], {}, 0
        for t in man['turns']:
            spec = json.load(open(os.path.join(a.dir, t['file']), encoding='utf-8')); errs, warns = validate(spec, reg)
            print('%-26s %s%s  theme: %s' % (t['file'][:-5], 'valid' if not errs else 'INVALID', (' · %d warnings' % len(warns)) if warns else '', tone_of(spec, reg)))
            for x in errs + warns: print('   ', x)
            if errs: bad += 1; continue
            specs.append(spec); notes[spec['turn']['id']] = t.get('note', '')
        berrs = book_check(specs, reg)
        for x in berrs: print('BOOK ERROR:', x)
        if bad or berrs: sys.exit(1)
        page = book(specs, reg, notes)
        open(os.path.join(a.out, 'diagnosis-turns.html'), 'w', encoding='utf-8').write(
            '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>%s</body></html>' % page)
        open(os.path.join(a.out, 'diagnosis-turns.artifact.html'), 'w', encoding='utf-8').write(page)
        open(os.path.join(a.out, 'system-section.md'), 'w', encoding='utf-8').write(prompt(reg))
        for s in specs:     # single pages, for tests
            for vw in ('desktop', 'mobile'):
                os.makedirs(os.path.join(a.out, 'pages'), exist_ok=True)
                open(os.path.join(a.out, 'pages', '%s.%s.html' % (s['turn']['id'], vw)), 'w', encoding='utf-8').write(render_page(s, vw, reg))
        print('wrote %s (%d turns) and system-section.md' % (os.path.join(a.out, 'diagnosis-turns.html'), len(specs)))
    if a.cmd == 'prompt': print(prompt(reg))
    if a.cmd == 'catalog': print(catalog(reg))

if __name__ == '__main__':
    main()
