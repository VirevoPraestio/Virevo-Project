"""
v3 redraw of the five approved Bed Management pages (30 Sep 2026 feedback), HTML only for review:
  Home B (ward plan) · Diagnosis B (morning count) · Solutions B (corridor of fixes) ·
  Automations C (station panel) · Processes B (trial ward)
Chat one screen tall with its own scroll; first element raised with its box open;
on a phone each box opens right under its element.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for sub in ('home', 'diagnosis', 'solutions', 'automations', 'processes'):
    sys.path.insert(0, os.path.join(HERE, sub))
import bm_common as C
from bm_common import e, ico, ICONS, BED_ICO, STAMP, bed_svg, bed_key, BED_CSS, masthead, emblem, standing, section, pending, actions, tag, pt, sel, sel_cls, box, CHEV, say_btn
import home as H, diagnosis as D, solutions as S, automations as A, processes as P

OUT = os.path.join(C.ROOT, 'out', 'landing', 'approved')

# ------------------------------------------------------------------------------------------
# HOME · the ward plan
NOTES = {
 'Diagnosis': ['Seven stops walked, from the patient leaving to the next patient in bed.', 'One week of morning counts, ward by ward.',
               'Needs admission times from your admissions desk.', 'Uses your own figures once the match is done.', 'Named in plain words once the evidence is in.'],
 'Solutions': ['On its second drawing: one list on a screen for the wards, housekeeping and admissions.', 'An idea for now. It gets shaped once the cause is named.',
               'An idea for now. It joins up with the Discharge Process work.'],
 'Automations': ['Marks the bed free the moment the discharge is closed. Waits for the bed list.', 'Sends housekeeping the ward and bed number within 2 minutes.',
                 'Sends admissions a list of tomorrow’s likely free beds at 9 PM.'],
 'Processes': ['One named person on each shift keeps the bed list right.', 'Tried on one ward first, for two weeks.', 'Ward, housekeeping and admissions, ten minutes, standing.'],
}
def home_canvas(state):
    d = H.DATA[state]; empty = state == 'empty'
    rooms, desk = [], []
    for i, p in enumerate(d['places']):
        mob = ''
        if p['steps']:
            beds = []
            for j, (t, s) in enumerate(p['steps']):
                k = '%d-%d' % (i, j); first = (i, j) == (0, 0)
                beds.append('<button class="bmb s-%s %s" type="button"%s aria-label="%s: %s">%s</button>' % (s, sel_cls(first), sel('hb', k, first), e(t), H.STEP[s], bed_svg(44)))
                inner = ('<div class="hb-box"><span class="hb-bk">%s · step %d of %d</span><div class="hb-bt"><b>%s</b><span class="hb-st s-%s">%s</span></div><p>%s</p>%s</div>') % (
                    e(p['name']), j + 1, len(p['steps']), e(t), s, H.STEP[s], e(NOTES[p['name']][j]), say_btn('Open ' + p['name'], 'Take me to ' + p['name']))
                desk.append(box('hb', k, inner, first, 'desk'))
                mob += box('hb', k, inner, first, 'mob')
            done = sum(1 for _, s in p['steps'] if s == 'done')
            prog = '%d of %d %s' % (done, len(p['steps']), p['unit'])
            beds = ''.join(beds)
        else:
            beds = ''.join('<span class="bmb s-empty">%s</span>' % bed_svg(44) for _ in range(3)); prog = 'Nothing yet'
        fig = ''
        if p['fig']:
            v, l, t = p['fig']
            fig = '<div class="h-fig"><span class="h-fv">%s</span><span class="h-fl">%s</span>%s</div>' % (e(v), e(l), tag(t))
        rooms.append(('<div class="h-room h-r%d" data-s="%s"%s><span class="h-door" aria-hidden="true"></span>'
                      '<div class="h-plate"><span class="h-pn">%s %s</span><span class="h-ps">%s</span></div><p class="h-hl">%s</p>%s'
                      '<div class="h-beds">%s</div>%s<div class="h-cap"><b>%s</b></div></div>') % (
            i + 1, p['status'], pt(p.get('pt')), ico(ICONS[p['name']], 'currentColor', 20), e(p['name']), e(H.STATUS[p['status']]), e(p['head']), fig, beds, mob, e(prog)))
    total = sum(len(p['steps']) for p in d['places']); made = sum(1 for p in d['places'] for _, s in p['steps'] if s == 'done')
    station = ('<div class="h-corr"><span class="h-cl">Corridor</span><div class="h-stn"><span class="h-sk">Nurses’ station</span><span class="h-sv">%s</span>'
               '<span class="h-bar"><i style="width:%d%%"></i></span></div><span class="h-cl">Corridor</span></div>') % (
        ('%d of %d beds made up' % (made, total)) if total else 'No beds set up yet', int(100 * made / total) if total else 0)
    plan = '<div class="h-plan bm-paper">%s%s%s</div>%s%s' % (''.join(rooms[:2]), station, ''.join(rooms[2:]),
            bed_key(('Made up: done', 'In use now', 'Still to do', 'Not started')), '<div class="hb-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'One room for each part. Tap a small bed to read its step.' if not empty else 'One room for each part'
    return (masthead('Virevo · 250-bed hospital, Bhubaneswar', 'Bed Management', emblem(BED_ICO), STAMP[state]) + standing(d['claim'], d['deck'], empty)
            + section('Where each part of the work stands', plan, 'h-sec', sub) + pending(d['pending']) + actions(d['actions']))

HOME_CSS = H.CSS + '''
.h-cap{justify-content:flex-end}
.h-beds{gap:10px}
.h-beds .bmb.js-sel{border-radius:8px;background:transparent}
.h-beds .bmb.js-sel.is-up{background:var(--card)}
.hb-desk{margin-top:18px}
.hb-box{display:flex;flex-direction:column;gap:8px;padding:18px 22px;background:var(--card);border:2px solid var(--ink);border-radius:6px;border-left:6px solid #d4a94f}
.bx-mob .hb-box{padding:14px 16px}
.hb-bk{font-size:12px;font-weight:600;color:var(--mut)}
.hb-bt{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.hb-bt b{font-size:17px}
.hb-st{font-size:12px;font-weight:600;padding:2px 10px;border-radius:10px;border:1.5px solid var(--ink)}
.hb-st.s-done{background:var(--ink);color:var(--card)}.hb-st.s-now{background:#d4a94f;border-color:#d4a94f}.hb-st.s-none{border-style:dashed;border-color:var(--grey);color:var(--mut)}
.hb-box p{font-size:14.5px;line-height:1.5}
.hb-box .bm-open{align-self:flex-start;margin-top:4px}
.bx-mob{background:var(--card);border-left:2px solid var(--ink);border-top:2px solid var(--ink)}
'''

# ------------------------------------------------------------------------------------------
# DIAGNOSIS · the morning count
def dg_canvas(state):
    d = D.DATA[state]; empty = state == 'empty'
    if not d['ward']:
        return D.canvas_b(d, empty)
    times = list(d['ward'])
    def view(t, w):
        beds = D.ward_beds(w)
        return ('<div class="db-ward bm-paper"><div class="db-bay">%s</div><div class="db-corr"><span>Corridor</span></div><div class="db-bay">%s</div>'
                '<div class="db-stn"><span class="db-sk">Nurses’ station</span><span class="db-sv">%d</span><span class="db-sl">patients waiting for a bed</span></div></div>'
                '<p class="db-line"><b>%s.</b> %s</p>') % (''.join(beds[:10]), ''.join(beds[10:]), w['wait'], e(t), e(w['line']))
    btns, desk = [], []
    for i, (t, w) in enumerate(d['ward'].items()):
        first = i == 0
        btns.append('<button class="db-t %s" type="button"%s><span class="db-tt">%s</span><span class="db-tw">%d waiting · %d ready</span>%s</button>' % (
            sel_cls(first), sel('db', str(i), first), e(t), w['wait'], w['ready'], CHEV))
        btns.append(box('db', str(i), view(t, w), first, 'mob'))
        desk.append(box('db', str(i), view(t, w), first, 'desk'))
    key = ('<div class="db-key" aria-hidden="true"><span><i class="bmb db-use">%s</i>Patient in bed</span><span><i class="bmb db-dirty">%s</i>Empty, waiting to be cleaned</span>'
           '<span><i class="bmb db-ready">%s</i>Ready for a patient</span></div>') % (bed_svg(20), bed_svg(20), bed_svg(20))
    hours = ['8 AM', '9', '10', '11', '12 PM', '1', '2', '3', '4', '5 PM']
    mx = max(d['arrive'] + d['free'])
    bars = lambda xs, c: ''.join('<span class="db-b %s" style="height:%d%%"></span>' % (c, 100 * x / mx if x else 3) for x in xs)
    clock = ('<div class="db-clock" aria-label="New patients arrive mostly 9 to 11 AM. Beds come free mostly 1 to 3 PM.">'
             '<div class="db-lane"><span class="db-ll">New patients arriving</span><div class="db-bars">%s</div></div>'
             '<div class="db-lane"><span class="db-ll">Beds coming free</span><div class="db-bars">%s</div></div>'
             '<div class="db-lane db-hrs"><span class="db-ll"></span><div class="db-bars">%s</div></div></div>') % (
        bars(d['arrive'], 'arr'), bars(d['free'], 'fre'), ''.join('<span>%s</span>' % h for h in hours))
    body = ('<div class="db-top">%s</div><div class="db-ts" role="group" aria-label="Time of day">%s</div><div class="db-desk">%s</div>%s'
            '<div class="db-sub"><h4>Across the day</h4>%s</div>') % (tag('derived'), ''.join(btns), ''.join(desk), key, clock)
    return D.top(d, empty) + section('The morning count', body, 'db-sec', 'One example ward of 20 beds, worked out from your week of counts. Tap a time.') + D.stages_strip(d) + D.evidence(d) + D.tail(d)

DG_CSS = D.COMMON + D.CSS_B + '''
.db-top{display:flex;justify-content:flex-end;margin:-6px 0 10px}
.db-ts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:16px;border:0;border-radius:0;overflow:visible}
.lp .db-t{display:flex;flex-direction:column;align-items:flex-start;gap:2px;min-height:64px;padding:10px 16px;border:2px solid var(--ink);border-radius:8px;background:var(--card);text-align:left;min-width:0}
.db-tt{font-family:'Bebas Neue',sans-serif;font-size:30px;line-height:1}
.db-tw{font-size:12.5px;color:var(--mut);font-weight:500}
.lp .db-t.is-up{background:#d4a94f;border-color:var(--ink)}
.db-t.is-up .db-tw{color:var(--ink)}
.bx-mob .db-line{margin-top:10px}
@container lp (max-width:699px){
 .db-ts{grid-template-columns:1fr;gap:10px}
 .lp .db-t{flex-direction:row;align-items:center;gap:12px;min-height:56px;padding:8px 16px}
 .db-tw{flex:1 1 auto}
 .db-top{justify-content:flex-start;margin:0 0 10px}
 .db-ts .bx-mob{margin:2px 0 8px}
 .db-ts .bx-mob::before{display:none}
}
'''

# ------------------------------------------------------------------------------------------
# SOLUTIONS · the corridor of fixes
def so_detail(f):
    return ('<div class="sb-det"><div><div class="so-lab">What it is</div><p class="sb-what">%s</p>%s</div>'
            '<div><div class="so-lab">What it depends on</div>%s</div><div><div class="so-lab">How it was drawn</div><ol class="sb-revs">%s</ol></div></div>') % (
        e(f['what']), S.saves(f), S.deps(f), ''.join('<li><span class="so-rev"><span>%s</span></span>%s</li>' % (r, e(t)) for r, t in f['revs']))
def so_canvas(state):
    d = S.DATA[state]; empty = state == 'empty'
    if not d['fixes']:
        return S.canvas_b(d, empty)
    rooms, desk = [], []
    for f in d['fixes']:
        first = f['n'] == 1; k = str(f['n'])
        rooms.append('<button class="sb-room %s s%d" type="button"%s%s><span class="sb-plate"><span>Fix %d</span>%s</span><b class="sb-name">%s</b>%s<span class="sb-more">%s%s</span><span class="sb-door" aria-hidden="true"></span></button>' % (
            sel_cls(first), f['stage'], sel('sb', k, first), pt(f.get('pt')), f['n'], S.rev_badge(f), e(f['name']), S.track(f, 'so-track sb-track', True),
            'What it is, what it depends on, how it was drawn', CHEV))
        rooms.append(box('sb', k, so_detail(f), first, 'mob'))
        desk.append(box('sb', k, so_detail(f), first, 'desk'))
    agreed = sum(1 for f in d['fixes'] if f['stage'] == 3)
    plan = ('<div class="sb-plan bm-paper"><div class="sb-rooms">%s</div><div class="sb-corr"><span>Corridor</span><span class="sb-stn">Nurses’ station · <b>%d of %d fixes agreed</b></span></div></div>'
            '<div class="sb-desk">%s</div>') % (''.join(rooms), agreed, len(d['fixes']), ''.join(desk))
    return S.top(d, empty) + section('The corridor of fixes', plan, 'sb-sec', 'One room for each fix. Each door plate carries its four stops. Tap a room to open it.') + S.tail(d)

SO_CSS = S.COMMON + S.CSS_B + '''
.sb-room.js-sel{background:transparent}
.sb-room.js-sel.is-up{background:var(--card);box-shadow:0 0 0 2.5px #d4a94f,0 7px 0 -1px rgba(0,0,0,.2),0 18px 28px -6px rgba(0,0,0,.32) !important}
.sb-more{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--mut);margin-top:auto}
.sb-desk .sb-det{margin-top:22px}
.bx-mob .sb-det{margin-top:0;padding:16px;border-width:0}
.bx-mob{background:var(--card);border:2px solid var(--ink);border-radius:4px;margin:0 12px 14px !important}
.bx-mob::before{border-left:2px solid var(--ink);border-top:2px solid var(--ink)}
@container lp (max-width:699px){
 .sb-rooms .bx-mob{border-left-width:2px}
}
'''

# ------------------------------------------------------------------------------------------
# AUTOMATIONS · the station panel
def au_canvas(state):
    d = A.DATA[state]; empty = state == 'empty'
    if not d['autos']:
        return A.canvas_c(d, empty)
    head = '<div class="ac-row ac-hd"><span>Automation</span>%s</div>' % ''.join('<span class="ac-sh">%s</span>' % e(s) for s in A.STAGES)
    rows, desk = [], []
    for a in d['autos']:
        first = a['n'] == 1; k = str(a['n'])
        cells = ''.join('<span class="ac-cell%s"><i aria-hidden="true"></i><span class="sr">%s: %s</span></span>' % (
            ' lit' if i <= a['stage'] else '', e(s), 'yes' if i <= a['stage'] else 'not yet') for i, s in enumerate(A.STAGES))
        rows.append('<button class="ac-row ac-btn %s" type="button"%s%s><span class="ac-name"><span class="ac-no">%d</span><span><b>%s</b><em>%s</em></span>%s</span>%s</button>' % (
            sel_cls(first), sel('ac', k, first), pt(a.get('pt')), a['n'], e(a['name']), e(a['when']), CHEV, cells))
        rows.append(box('ac', k, A.detail(a, False, 'acx'), first, 'mob'))
        desk.append(box('ac', k, A.detail(a, False, 'acx'), first, 'desk'))
    panel = ('<div class="ac-panel">%s<div class="ac-grid">%s%s</div><div class="ac-foot"><span>Nurses’ station · status panel</span><span>%d of %d switched on</span></div></div>') % (
        A.main_switch(d, 'ac-main'), head, ''.join(rows), sum(1 for a in d['autos'] if a['stage'] == 3), len(d['autos']))
    return A.top(d, empty) + section('The station panel', panel + '<div class="ac-desk">%s</div>' % ''.join(desk), 'ac-sec',
                                     'One row for each automation. A lamp lights as it moves from idea to switched on. Tap a row.') + A.tail(d)

AU_CSS = A.COMMON + A.CSS_C + '''
.ac-row{grid-template-columns:minmax(0,1.8fr) repeat(4,minmax(0,.55fr))}
.lp .ac-btn{width:100%;background:transparent;border:0;border-top:1.5px solid rgba(201,194,245,.22);color:var(--card);text-align:left;padding:0 6px;border-radius:10px;margin:2px 0}
.ac-btn .ac-name{padding:14px 6px}
.lp .ac-btn.is-up{background:#37345A;border-top-color:transparent;box-shadow:0 0 0 2.5px #d4a94f,0 7px 0 -1px rgba(0,0,0,.45),0 18px 28px -6px rgba(0,0,0,.6) !important}
.ac-desk{margin-top:20px}
.ac-desk .au-det{border-left:6px solid #d4a94f}
.bx-mob .au-det{border:0;border-radius:10px;color:var(--ink)}
.ac-grid .bx-mob{background:var(--card);border-radius:10px;margin:12px 0 10px !important}
.ac-grid .bx-mob::before{background:var(--card)}
@container lp (max-width:699px){
 .ac-row{grid-template-columns:repeat(4,minmax(0,1fr))}
 .ac-btn .ac-name{grid-column:1/-1;padding:12px 4px 6px;min-height:0}
 .ac-btn .sel-chev{color:var(--accl);margin-left:auto}
}
'''

# ------------------------------------------------------------------------------------------
# PROCESSES · the trial ward
def pr_canvas(state):
    d = P.DATA[state]; empty = state == 'empty'
    if not d['changes']:
        return P.canvas_b(d, empty)
    pin = lambda c: '<button class="pb-pin %s" type="button"%s aria-label="Change %d: %s">%d</button>' % (
        sel_cls(c['n'] == 1), sel('pb', str(c['n']), c['n'] == 1), c['n'], e(c['name']), c['n'])
    at = lambda w: ''.join(pin(c) for c in d['changes'] if c['where'] == w)
    beds = ''.join('<span class="bmb s-%s">%s</span>' % ('done' if i not in (2, 5) else 'later', bed_svg(30)) for i in range(8))
    seats = ''.join('<span class="pb-seat"%s>%s<em>%s</em></span>' % (pt(r.get('pt')), ''.join(P.chair(s, 30) for s in r['seats']), e(r['name'])) for r in d['roles'])
    reads = ''.join('<div class="pb-read"%s><span class="pb-rl">%s</span>%s</div>' % (pt(m.get('pt')), e(m['name']), P.mreading(m)) for m in d['measures'])
    plan = ('<div class="pb-wrap"><div class="pb-plan bm-paper">'
            '<div class="pb-bay"><span class="pb-rn">Beds bay</span><div class="pb-beds">%s</div><div class="pb-pins">%s</div></div>'
            '<div class="pb-stn"><span class="pb-rn">Nurses’ station</span><div class="pb-pins">%s</div><div class="pb-seats">%s</div></div>'
            '<div class="pb-hk"><span class="pb-rn">Housekeeping room</span><div class="pb-pins">%s</div></div>'
            '<div class="pb-wall"><span class="pb-rn">On the station wall: the measures we watch</span><div class="pb-reads">%s</div></div></div>%s</div>') % (
        beds, at('bay'), at('stn'), seats, at('hk'), reads, P.trial(d))
    def det(c):
        return '<div class="pb-det"><p>%s</p><h5>How it will work</h5><ul>%s</ul></div>' % (e(c['what']), ''.join('<li>%s</li>' % e(x) for x in c['how']))
    legend, desk = [], []
    for c in d['changes']:
        first = c['n'] == 1; k = str(c['n'])
        legend.append('<button class="pb-lg %s" type="button"%s%s><span class="pb-ln">%d</span><span><b>%s</b><em>%s</em></span>%s</button>' % (
            sel_cls(first), sel('pb', k, first), pt(c.get('pt')), c['n'], e(c['name']), e(c['state']), CHEV))
        legend.append(box('pb', k, det(c), first, 'mob'))
        desk.append(box('pb', k, det(c), first, 'desk'))
    body = '<div class="pb-grid">%s<div class="pb-side"><h4>The changes</h4>%s%s</div></div>' % (plan, ''.join(legend), ''.join(desk))
    return P.top(d, empty) + section('The trial ward', body, 'pb-sec', 'One ward seen from above. Each change is pinned where it happens. Tap a pin or a change.') + P.tail(d)

PR_CSS = P.COMMON + P.CSS_B + '''
.pb-lg.js-sel{margin-bottom:10px}
.lp .pb-lg.is-up{background:var(--soft)}
.pb-lg.is-up .pb-ln{background:#d4a94f;color:var(--ink)}
.lp .pb-pin.is-up{background:#d4a94f;color:var(--ink);outline:0}
.pb-det{font-size:14px;line-height:1.55;padding:14px 16px;border-left:5px solid #d4a94f;background:var(--card);border-radius:0 10px 10px 0;box-shadow:inset 0 0 0 1.5px var(--line)}
.pb-det h5{font-size:12.5px;font-weight:600;margin:10px 0 6px;color:var(--acc)}
.pb-det ul{display:flex;flex-direction:column;gap:5px}
.pb-det li{padding-left:14px;position:relative;font-size:13.5px}.pb-det li::before{content:"";position:absolute;left:0;top:.6em;width:6px;height:6px;border-radius:50%;background:var(--ink)}
.pb-desk-wrap{margin-top:4px}
.pb-side .bx-mob{margin:-2px 0 14px !important;background:var(--card)}
.pb-side .bx-mob::before{display:none}
.pb-side .bx-desk{margin-top:4px}
'''

PAGES = {
 'home': (None, H.THEME, home_canvas, HOME_CSS, H.DATA, 'bm-home', 'Home', 'The ward plan (Sample B)'),
 'diagnosis': ('Diagnosis', D.THEME, dg_canvas, DG_CSS, D.DATA, 'bm-diagnosis bm-d-b', 'Diagnosis', 'The morning count (Sample B)'),
 'solutions': ('Solutions', S.THEME, so_canvas, SO_CSS, S.DATA, 'bm-solutions bm-s-b', 'Solutions', 'The corridor of fixes (Sample B)'),
 'automations': ('Automations', A.THEME, au_canvas, AU_CSS, A.DATA, 'bm-automations bm-a-c', 'Automations', 'The station panel (Sample C)'),
 'processes': ('Processes', P.THEME, pr_canvas, PR_CSS, P.DATA, 'bm-processes bm-p-b', 'Processes', 'The trial ward (Sample B)'),
}

def build():
    os.makedirs(OUT, exist_ok=True)
    pages = {}
    for k, (place, t, fn, css, data, cls, label, _) in PAGES.items():
        for st in ('filled', 'empty'):
            for v in ('desktop', 'mobile'):
                h = C.page_v3(t, place, fn(st), BED_CSS + css, data[st]['chat'], v, 'Bed Management %s' % label, cls)
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(OUT, 'v3-%s.%s.%s.html' % (k, v, st)), 'w').write(h)
    return pages

def review(pages):
    tpl = open(os.path.join(HERE, 'review_template_v3.html')).read()
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>%s</b><span>%s</span><i style="background:%s;border-color:%s"></i></button>' % (
        k, 'true' if k == 'home' else 'false', e(v[6]), e(v[7]), v[1]['ground'], v[1]['ink']) for k, v in PAGES.items())
    return tpl.replace('@@PICKS@@', picks).replace('@@DATA@@', json.dumps(pages, ensure_ascii=False).replace('</', '<\\/'))

if __name__ == '__main__':
    pages = build()
    rv = os.path.join(OUT, 'bed-management-approved-pages-v3.html')
    open(rv, 'w').write(review(pages))
    print('built', rv, os.path.getsize(rv))
