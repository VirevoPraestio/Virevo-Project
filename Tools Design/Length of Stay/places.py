"""
Length of Stay: the four place pages, beside the approved home page A (the patient's path). 8 Oct 2026, for review.

All five use the Financial look (V skin, Virevo type unchanged). Each place has its own colours and
its own drawing of a hospital stay, using ideas from the samples not chosen (B the bed board,
C the stay chart and the bedside monitors):

  Home         A · the patient's path (approved): the stay as a route from Emergency to home;
               one patient wristband per part of the work.
  Diagnosis    one patient's chart: a real-shaped stay followed day by day, Emergency to home,
               each event a line with the time it should have taken and the extra; then the
               1,300 extra days split by cause, one square per 13 days.
  Solutions    the beds we get back: one entry per fix, its four stops, the days it frees a month,
               and the beds that frees every day drawn as beds; double-ruled total.
  Automations  the hospital's day: a 24-hour clock face with each helper at its hour; one
               bedside monitor per helper showing the alert it would put up.
  Processes    the week on the bed board: a whiteboard week with the changes as magnets on their
               days; who owns the flow in each area; the numbers we watch, now and plan.

Every figure is made up for an example 250-bed hospital and marked Example only or Tojo's guess.
Run:  python3 places.py   ->  out/landing/
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import los_landing as H              # sets the tool name, loads the Financial look
C, L2, L3 = H.C, H.L2, H.L3
from sc_common import e, ico, ICONS, CHEV, sel, sel_cls, box, pt, tag, say_btn, standing, section, pending, actions, STAMP

SK = H.SK
OUT = H.OUT
masthead, two = L3.masthead, L3.two

# ==========================================================================================
RAIL = ['#D6E9E8', '#F7E4E1', '#F6F3D4', '#F4EFD9', '#EFEDE6']   # home, then the four places in their own grounds
def T(ground, card, ink, mut, line, soft, grey, hi, hi_dark, hi_text, panel):
    return C.theme(ground, card, ink, mut, line, soft, grey, hi, hi_dark, hi_text, RAIL, panel)
THEMES = {
 # home (approved A): aqua, petrol, coral red
 'home': T('#DFEFEE', '#FFFFFF', '#0B2F3A', '#3D5A62', '#BBD6D5', '#EDF6F5', '#8EA9AC', '#FF6F61', '#FF8A80', '#B3261E', '#0B2F3A'),
 # Diagnosis: pale rose, deep cobalt, spring green
 'diagnosis': T('#F7E4E1', '#FFFFFF', '#14246B', '#4E5785', '#E6CCC7', '#FCF2F0', '#A9A3BC', '#5EE08A', '#8BEAAB', '#0F6B36', '#14246B'),
 # Solutions: pale lemon, graphite, magenta
 'solutions': T('#F6F3D4', '#FFFFFF', '#20242B', '#53575F', '#DCD8B4', '#FAF9EA', '#A3A396', '#F06BD0', '#F59ADF', '#A0177F', '#20242B'),
 # Automations: pale butter, ox-blood, monitor yellow
 'automations': T('#F4EFD9', '#FFFFFF', '#3A1016', '#664A4D', '#DDD4B6', '#FAF7EA', '#AFA393', '#FFD43B', '#FFDF6E', '#7A5A00', '#3A1016'),
 # Processes: whiteboard, indigo, marker cyan
 'processes': T('#EFEDE6', '#FFFFFF', '#1C1E4F', '#4B4D72', '#D6D3C6', '#F6F5F0', '#A09FAE', '#39C6EC', '#6FD6F2', '#0A6683', '#1C1E4F'),
}

def chip(cls, text):
    return '<span class="fx-chip %s">%s</span>' % (cls, e(text))

# ==========================================================================================
# DIAGNOSIS · one patient's chart
AREA_CLS = {'Emergency': 'a-er', 'ICU': 'a-icu', 'Step-down': 'a-sd', 'Ward': 'a-wd'}
DG = {
 'filled': {
  'claim': 'One patient stayed 9 days. The care needed 7.',
  'deck': 'Two of five steps done. We followed one typical stay from Emergency to home, and counted the days patients wait across the hospital. Most extra days come after the patient is ready to go.',
  'stay': [  # area, start day, needed days, extra days
   ('Emergency', 0.0, 0.17, 0.13), ('ICU', 0.3, 3.0, 1.0), ('Step-down', 4.3, 2.0, 0.0), ('Ward', 6.3, 2.0, 1.0)],
  'lines': [
   {'when': 'Day 0 · 9 PM', 'area': 'Emergency', 'what': 'Seen and admitted; waited 7 hours for an ICU bed', 'extra': '3 hours', 'pt': 3,
    'found': 'The ICU was full. Two patients there had been ready to move to step-down since the morning.',
    'points': 'The wait in Emergency starts in the ICU.'},
   {'when': 'Day 1 to 4', 'area': 'ICU', 'what': 'Ready to leave the ICU on day 3; moved on day 4', 'extra': '1 day', 'pt': 3,
    'found': 'No step-down bed was free until a step-down patient went to the ward the next afternoon.',
    'points': 'Each area waits for the one after it.'},
   {'when': 'Day 4 to 6', 'area': 'Step-down', 'what': 'Two days, as planned', 'extra': None, 'note': 'On plan',
    'found': 'The step-down stay went as the doctor expected.', 'points': 'Step-down is not where this stay lost time.'},
   {'when': 'Day 6 to 8', 'area': 'Ward', 'what': 'Recovered on the ward; ready to go home on the morning of day 8', 'extra': None, 'note': 'On plan',
    'found': 'The going-home day was first written down on day 7, a day before.', 'points': 'Set the day earlier and the rest can be ready in time.'},
   {'when': 'Day 8 to 9', 'area': 'Ward', 'what': 'Ready to go home; waited for a scan report and the going-home papers', 'extra': '1 day', 'pt': 2,
    'found': 'The scan was done on Saturday and reported on Monday. The papers were signed at 4 PM; the family came at 6 PM.',
    'points': 'Weekend reports and late papers. The biggest cause across the hospital.'},
  ],
  'causes': [('Waiting while ready to go home: reports, papers, a ride', 45, 'Leading so far', 2),
             ('Waiting for a bed in the next area', 25, 'Being checked', 3),
             ('Tests and doctors’ rounds paused at weekends', 20, 'Being checked', None),
             ('Planned surgery admitted a day early', 10, 'Not checked yet', None)],
  'pending': [
   {'text': 'Get three months of admission, move and going-home times, by area.', 'need': 'Needs the records desk’s list', 'pt': 2},
   {'text': 'Count the days patients wait while ready to go home, and what for.', 'pt': 2},
   {'text': 'Find what one extra day costs in each area.'},
   {'text': 'Name the main cause, so the fixes start in the right place.'},
  ],
  'actions': {'go': {'detail': 'Count the days patients wait while ready', 'say': 'Let’s count the days patients wait while ready to go home'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about how long patients stay: '},
              'jump': {'tab': 'Solutions', 'detail': 'See the three fixes so far', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['Diagnosis is two of five steps in.', 'We followed one stay: 9 days, where the care needed 7. Across the hospital, almost half of the extra days are patients who are ready to go home but still waiting.'],
           'pointer': 'Pick a point to add to it, or tap a line of the chart.',
           'note': 'Ready to go is not the same as gone.',
           'points': [{'n': 1, 'label': 'The extra days, by cause'}, {'n': 2, 'label': 'Waiting while ready to go'},
                      {'n': 3, 'label': 'Waiting for the next bed'}],
           'prompts': ['Our records desk has the times', 'Why do reports wait for Monday?', 'Let’s count the waiting days']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Tojo follows one typical stay with you, from Emergency to home, and writes each step on the chart: the time it should have taken, and the extra.',
  'stay': [],
  'lines': [{'when': '', 'area': a, 'what': w} for a, w in [('Emergency', 'Seen and admitted'), ('ICU', 'Days in intensive care'), ('Step-down', 'Days in step-down'),
                                                           ('Ward', 'Days on the ward'), ('Ward', 'Ready to go home, until gone')]],
  'causes': [('Waiting while ready to go home', 0, '', None), ('Waiting for a bed in the next area', 0, '', None),
             ('Weekends', 0, '', None), ('Admitted early', 0, '', None)],
  'pending': [
   {'text': 'Put a number on the average stay in each area.', 'need': 'Needs three months of admission and going-home times'},
   {'text': 'Pick one typical stay to follow with Tojo.'},
   {'text': 'Find how long Emergency patients wait for a bed.'},
  ],
  'actions': {'go': {'detail': 'Put a number on the stay with Tojo', 'say': 'Let’s put a number on how long patients stay'},
              'add': {'detail': 'Share admission and going-home times', 'say': 'Here is what I already know about how long patients stay: '},
              'jump': {'tab': 'Solutions', 'detail': 'Fills in once the cause is named', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['This is Diagnosis. We find out where the extra days come from.', 'We start with one typical stay, followed from Emergency to home.'],
           'note': 'Follow one patient home.', 'points': [],
           'prompts': ['Let’s put a number on the stay', 'What should I bring?', 'Why is this a money question?']},
 },
}

def stay_strip(stay):
    span = 10.0
    segs = []
    for a, s, need, extra in stay:
        segs.append('<i class="pc-seg %s" style="left:%.2f%%;width:%.2f%%"><span>%s</span></i>' % (AREA_CLS[a], s / span * 100, need / span * 100, e(a if need > 0.5 else '')))
        if extra:
            segs.append('<i class="pc-seg pc-x" style="left:%.2f%%;width:%.2f%%"></i>' % ((s + need) / span * 100, extra / span * 100))
    ticks = ''.join('<span style="left:%.1f%%">%d</span>' % (d / span * 100, d) for d in range(0, 11))
    return ('<div class="pc-strip" role="img" aria-label="One stay: Emergency 7 hours, ICU 4 days, step-down 2 days, ward 3 days. Extra: 3 hours in Emergency, 1 day in the ICU, 1 day on the ward.">'
            '<div class="pc-track">%s</div><div class="pc-ticks" aria-hidden="true">%s</div><div class="pc-leg" aria-hidden="true">'
            '<span><i class="a-er"></i>Emergency</span><span><i class="a-icu"></i>ICU</span><span><i class="a-sd"></i>Step-down</span><span><i class="a-wd"></i>Ward</span>'
            '<span><i class="pc-x"></i>Extra</span></div></div>') % (''.join(segs), ticks)

def waffle(causes, empty):
    cells = []
    for j, (name, v, *_ ) in enumerate(causes):
        cells += ['<i class="wf-%d"></i>' % j] * v
    if empty:
        cells = ['<i class="wf-e"></i>'] * 100
    return '<div class="wf-grid" role="img" aria-label="%s">%s</div>' % (
        e('The 1,300 extra days a month, one square for every 13 days: ' + ', '.join('%s %d of 100' % (c[0], c[1]) for c in causes)) if not empty else 'Not split yet', ''.join(cells))

def dg_canvas(state):
    d = DG[state]; empty = state == 'empty'
    rows, desk = [], []
    for i, r in enumerate(d['lines']):
        k = str(i); first = i == 0 and not empty
        area = '<span class="pc-a %s">%s</span>' % (AREA_CLS[r['area']], e(r['area']))
        if empty:
            rows.append('<div class="pc-l is-empty"><span class="pc-wh"><span class="pc-d">—</span>%s</span><span class="pc-w">%s</span><span class="pc-xt">—</span></div>' % (area, e(r['what'])))
            continue
        x = r.get('extra')
        rows.append(('<button class="pc-l %s%s" type="button"%s%s><span class="pc-wh"><span class="pc-d">%s</span>%s</span><span class="pc-w">%s%s</span><span class="pc-xt">%s</span>%s</button>') % (
            sel_cls(first), ' is-extra' if x else '', sel('pc', k, first), pt(r.get('pt')), e(r['when']), area, e(r['what']),
            '<span class="pc-n">%s</span>' % e(r['note']) if r.get('note') else '', ('+ ' + e(x)) if x else '—', CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>%s</h4>%s%s</div><p>%s</p>%s</div>') % (
            e(r['when']), chip('c-now', x + ' extra') if x else chip('', r.get('note', '')), tag('example'), e(r['what']),
            two('What we found', r['found'], 'What it points to', r['points']))
        rows.append(box('pc', k, det, first, 'mob')); desk.append(box('pc', k, det, first, 'desk'))
    head = ('<div class="pc-top"><div><span class="pc-k">Patient chart</span><b>%s</b></div>%s</div>%s'
            '<div class="pc-h" aria-hidden="true"><span>When, where</span><span>What happened</span><span>Extra</span></div>') % (
        'One typical stay, chest pain, age 62' if not empty else 'One typical stay', tag('example') if not empty else '', stay_strip(d['stay']) if not empty else '')
    foot = ('<div class="pc-f"%s><span>Stayed 9 days. The care needed 7.</span><b>+ 2 days</b><span class="pc-fl">and 3 hours more in Emergency</span></div>' % pt(1)) if not empty else ''
    chart = '<div class="pc-ch%s">%s<div class="pc-rows">%s</div>%s</div>' % (' is-empty' if empty else '', head, ''.join(rows), foot)
    body = '<div class="pc-wrap">%s<div class="pc-side">%s</div></div>' % (chart, ''.join(desk) if desk else '<p class="fx-empty">Each line opens here once it is written.</p>')
    sub = 'Each step of the stay is a line: when, where, and the time it took beyond what the care needed. Tap a line.' if not empty else 'Writes itself as we follow a stay'
    leg = ''.join('<li%s><i class="wf-%d"></i><span>%s</span><b>%s</b><em>%s</em></li>' % (
        pt(c[3]), j, e(c[0]), ('%d days' % round(c[1] * 13, -1)) if not empty else '—', e(c[2] or 'Not weighed yet')) for j, c in enumerate(d['causes']))
    gap = '<div class="wf"%s>%s<ul class="wf-leg">%s</ul></div><p class="fx-hint">%s</p>' % (
        pt(1) if not empty else '', waffle(d['causes'], empty), leg,
        'Example only. One square for every 13 extra days. The two top causes come from the chart above; the other two are still being checked.' if not empty else 'Tojo splits the extra days as the evidence comes in.')
    return (masthead('Diagnosis', state) + standing(d['claim'], d['deck'], empty)
            + section('One patient’s chart', body, 'pc-sec', sub)
            + section('Where the 1,300 extra days come from', gap, 'wf-sec', 'Four possible causes, a month')
            + pending(d['pending']) + actions(d['actions']))

DG_CSS = r'''
.a-er{--a:var(--hi)}.a-icu{--a:var(--ink)}.a-sd{--a:var(--mut)}.a-wd{--a:var(--grey)}
.pc-wrap{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:22px;align-items:start}
.pc-ch{background:var(--card);border-top:6px solid var(--ink);padding:14px 16px 12px}
.pc-top{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;padding-bottom:10px}
.pc-top div{display:flex;flex-direction:column;gap:2px}
.pc-k{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.pc-top b{font:400 24px/1 var(--f-d)}
.pc-strip{display:flex;flex-direction:column;gap:4px;padding:4px 0 12px}
.pc-track{position:relative;height:30px;background:repeating-linear-gradient(90deg,var(--line) 0 1px,transparent 1px 10%);box-shadow:inset 0 0 0 1px var(--line)}
.pc-seg{position:absolute;top:0;bottom:0;background:var(--a);display:flex;align-items:center;padding-left:6px;overflow:hidden}
.pc-seg span{font-size:11.5px;font-weight:600;color:#fff;white-space:nowrap}
.pc-seg.a-wd span{color:var(--ink)}.pc-seg.a-er span{color:var(--ink)}
.pc-seg.pc-x,.pc-leg i.pc-x{background:repeating-linear-gradient(135deg,var(--hi) 0 4px,var(--card) 4px 7px);box-shadow:inset 0 0 0 2px var(--ink)}
.pc-ticks{position:relative;height:14px}
.pc-ticks span{position:absolute;white-space:nowrap;transform:translateX(-50%);font-size:11px;font-weight:600;color:var(--mut)}
.pc-ticks span:first-child{transform:none}.pc-ticks span:last-child{transform:translateX(-100%)}
.pc-leg{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:12px;color:var(--mut)}
.pc-leg span{display:inline-flex;align-items:center;gap:5px}
.pc-leg i{display:inline-block;width:14px;height:10px;background:var(--a)}
.pc-days{margin-left:auto}
.pc-h,.pc-l{display:grid;grid-template-columns:100px minmax(0,1fr) 66px 0;align-items:baseline;gap:8px}
.pc-h{border-top:3px double var(--ink);border-bottom:1px solid var(--ink);padding:6px 4px}
.pc-h span{font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.pc-h span:nth-child(3){text-align:right}
.pc-wh{display:flex;flex-direction:column;align-items:flex-start;gap:5px}
.pc-l{width:100%;border:0;border-bottom:1px solid var(--line);background:transparent;text-align:left;padding:9px 4px;color:var(--ink);font-size:14px;line-height:1.4}
.lp .pc-l.is-up{background:var(--soft)}
.pc-d{font:400 17px/1.1 var(--f-d);color:var(--mut)}
.pc-a{justify-self:start;font-size:11.5px;font-weight:600;padding:2px 7px;box-shadow:inset 4px 0 0 var(--a);background:var(--soft)}
.pc-w{display:flex;flex-direction:column;gap:2px;min-width:0}
.pc-n{font-size:12px;font-weight:600;color:var(--mut)}
.pc-xt{text-align:right;font-weight:600;color:var(--mut);white-space:nowrap}
.pc-l.is-extra .pc-xt{font:400 20px/1 var(--f-d);color:var(--hi-text)}
.pc-l .sel-chev{display:none}
.pc-f{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:baseline;gap:4px 10px;padding:10px 4px 2px;border-top:1px solid var(--ink)}
.pc-f>span:first-child{font-size:14px;font-weight:600}
.pc-f b{font:400 30px/1 var(--f-d);border-bottom:5px double var(--ink);background:linear-gradient(transparent 50%,var(--hi) 50% 90%,transparent 90%);padding:0 3px 2px}
.pc-fl{grid-column:1/-1;font-size:13px;color:var(--mut)}
.pc-ch.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey)}
.pc-l.is-empty{color:var(--mut);cursor:default}
.pc-side{position:sticky;top:190px}
.pc-side .fx-two{grid-template-columns:1fr}
.wf{display:flex;align-items:center;gap:26px;background:var(--card);padding:16px 20px;border-top:6px solid var(--ink)}
.wf-grid{display:grid;grid-template-columns:repeat(10,16px);gap:3px;flex-shrink:0}
.wf-grid i,.wf-leg li i{display:block;width:16px;height:16px}
.wf-0{background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.wf-1{background:var(--ink)}
.wf-2{background:var(--mut)}
.wf-3{background:var(--card);box-shadow:inset 0 0 0 2px var(--grey)}
.wf-e{box-shadow:inset 0 0 0 1px var(--grey)}
.wf-leg{flex:1;display:flex;flex-direction:column;min-width:0}
.wf-leg li{display:grid;grid-template-columns:16px minmax(0,1fr) 92px 120px;align-items:baseline;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.wf-leg li i{width:14px;height:14px}
.wf-leg b{font:400 22px/1 var(--f-d);text-align:right;white-space:nowrap}
.wf-leg em{font-style:normal;font-size:12.5px;font-weight:600;color:var(--mut)}
@container lp (max-width:699px){
 .pc-wrap{grid-template-columns:1fr}
 .pc-side{display:none}
 .pc-ch{padding:12px 10px 10px}
 .pc-h{display:none}
 .pc-l{grid-template-columns:minmax(0,1fr) 16px;grid-template-areas:"d c" "w w" "x x";row-gap:5px;padding:10px 2px}
 .pc-wh{grid-area:d;flex-direction:row;align-items:baseline;gap:10px}.pc-w{grid-area:w}.pc-l .sel-chev{display:inline-block;grid-area:c}
 .pc-xt{grid-area:x;text-align:left}
 .pc-rows .bx-mob{margin:2px 0 10px}
 .pc-rows .bx-mob .fx-box{border-top:3px solid var(--ink);background:var(--soft)}
 .pc-days{margin-left:0}
 .wf{flex-direction:column;align-items:flex-start;gap:12px;padding:14px}
 .wf-grid{grid-template-columns:repeat(10,minmax(0,1fr));align-self:stretch;max-width:260px}
 .wf-grid i{width:auto;aspect-ratio:1;height:auto}
 .wf-leg{align-self:stretch}
 .wf-leg li{grid-template-columns:16px minmax(0,1fr) auto;row-gap:2px}
 .wf-leg em{grid-column:2/-1}
}
'''

# ==========================================================================================
# SOLUTIONS · the beds we get back
STOPS = ['Idea', 'Shaped', 'Tested with you', 'Agreed']
SO = {
 'filled': {
  'claim': 'Three fixes could give back about 20 beds every day',
  'deck': 'One fix is being tested with you. None is agreed yet. Each one says how many days it frees a month, and how many beds that gives back every day.',
  'fixes': [
   {'name': 'Set each patient’s going-home day on the first day, and plan to it', 'stage': 2, 'days': 400, 'beds': 13, 'cost': '₹3 lakh', 'pt': 1,
    'what': 'The doctor writes the expected going-home day on the first day. Reports, papers, medicines and the ride are planned to that day, not started on it.',
    'hand': 'The ward sister writes the day on the bed board and checks the list of what is still needed each morning.',
    'auto': 'A helper lists, every morning, the patients due home tomorrow and what each is still waiting for.',
    'needs': ['Doctors agreeing to write the day on the first day', 'Reports ready by noon on the going-home day']},
   {'name': 'Move ICU patients to step-down the day they are ready', 'stage': 1, 'days': 120, 'beds': 4, 'cost': '₹1 lakh', 'pt': 2,
    'what': 'A short move round at 10 AM in the ICU and step-down agrees who moves today, so the bed below is freed before noon.',
    'hand': 'The ICU and step-down nurses in charge meet at 10 AM and agree the moves on paper.',
    'auto': 'A helper shows which ICU patients are ready to move and which step-down beds free up today.',
    'needs': ['A step-down bed freed by noon each day', 'ICU doctors agreeing the move the evening before']},
   {'name': 'Run scans and their reports on weekends too', 'stage': 0, 'days': 80, 'beds': 3, 'cost': '₹8 lakh a month',
    'what': 'Scans and their reports run on Saturday and Sunday as on weekdays, so patients are not kept in for a Monday report.',
    'hand': 'One extra scan technician and one reporting doctor on each weekend day, on a rota.',
    'auto': 'A helper lists on Friday the patients who will need a scan or report over the weekend.',
    'needs': ['A weekend rota for the scan room', 'Reporting doctors agreeing to weekend cover']},
  ],
  'pending': [
   {'text': 'Test the first fix with you on one ward: who writes the day, and who checks it.', 'need': 'Needs one ward to try it', 'pt': 1},
   {'text': 'Shape the second fix: when the move round meets, and who decides.', 'pt': 2},
   {'text': 'Check that each fix also works with no new software.'},
  ],
  'actions': {'go': {'detail': 'Test the first fix on one ward', 'say': 'Let’s test the first fix: the going-home day on the first day'},
              'add': {'detail': 'Suggest a fix of your own', 'say': 'I have an idea for a fix: '},
              'jump': {'tab': 'Automations', 'detail': 'See the helpers for these fixes', 'say': 'Take me to Automations'}},
  'chat': {'text': ['Three fixes are written up. The first, setting the going-home day on the first day, is being tested with you.',
                    'Together they could free about 600 days a month: about 20 beds back every day.'],
           'pointer': 'Pick a point to add to it, or tap a fix.',
           'note': 'Plan the going home on the day they come in.',
           'points': [{'n': 1, 'label': 'The going-home day'}, {'n': 2, 'label': 'The ICU move round'}, {'n': 3, 'label': 'The beds we get back'}],
           'prompts': ['Our doctors will not commit to a day', 'How sure are the 20 beds?', 'Let’s test the first fix']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'The fixes are entered here once Diagnosis names the main cause, each with the days it frees and the beds that gives back every day.',
  'fixes': [],
  'pending': [{'text': 'Name the main cause in Diagnosis first.'}, {'text': 'Write the first fix, with its by-hand version.'}],
  'actions': {'go': {'detail': 'Name the main cause first', 'say': 'Let’s name the main cause'},
              'add': {'detail': 'Suggest a fix of your own', 'say': 'I have an idea for a fix: '},
              'jump': {'tab': 'Automations', 'detail': 'Fills in once a fix is agreed', 'say': 'Take me to Automations'}},
  'chat': {'text': ['This is Solutions. The fixes are entered here once the main cause is named.'],
           'note': 'A fix waits for its cause.', 'points': [],
           'prompts': ['Take me back to Diagnosis', 'What kind of fixes come up?', 'Can I suggest a fix?']},
 },
}
BED = '<svg viewBox="0 0 24 16" aria-hidden="true"><path d="M1 15V2"/><path d="M1 11h22v4"/><path d="M23 11V9a2 2 0 0 0-2-2H9v4"/><circle cx="5" cy="8" r="1.8"/></svg>'

def so_canvas(state):
    d = SO[state]; empty = state == 'empty'
    rows, desk = [], []
    for i, f in enumerate(d['fixes']):
        k = str(i); first = i == 0
        beds = ''.join('<i class="br-b">%s</i>' % BED for _ in range(f['beds']))
        stops = ''.join('<span class="pb-t %s" title="%s"></span>' % ('on' if j < f['stage'] else 'now' if j == f['stage'] else '', e(s)) for j, s in enumerate(STOPS))
        rows.append(('<button class="br-row %s" type="button"%s%s><span class="br-no">%d</span><span class="br-fix"><b>%s</b>'
                     '<span class="br-st"><span class="pb-ts" aria-hidden="true">%s</span>Now: %s · to start %s</span></span>'
                     '<span class="br-n"><span>Days freed a month</span><b>%d</b></span>'
                     '<span class="br-beds"><span class="br-bl">%d beds back every day</span><span class="br-bs" aria-hidden="true">%s</span></span>%s</button>') % (
            sel_cls(first), sel('br', k, first), pt(f.get('pt')), i + 1, e(f['name']), stops, e(STOPS[f['stage']]), e(f['cost']),
            f['days'], f['beds'], beds, CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>Fix %d</h4>%s%s</div><p>%s</p>'
               '<div class="so-ways"><div class="so-way"><span class="fx-lab">By hand</span><p>%s</p></div><div class="so-way so-auto"><span class="fx-lab">Automatic</span><p>%s</p></div></div>'
               '<div><span class="fx-lab">What it relies on</span><ul class="fx-bul">%s</ul></div></div>') % (
            i + 1, chip('c-now', 'Now: ' + STOPS[f['stage']]), tag('guess'), e(f['what']), e(f['hand']), e(f['auto']), ''.join('<li>%s</li>' % e(x) for x in f['needs']))
        rows.append(box('br', k, det, first, 'mob')); desk.append(box('br', k, det, first, 'desk'))
    if empty:
        rows = ['<div class="br-row is-empty"><span class="br-no">%d</span><span class="br-fix"><b>Not entered yet</b></span><span class="br-n"><span>Days freed a month</span><b>—</b></span>'
                '<span class="br-beds"><span class="br-bl">Beds back every day: —</span></span></div>' % n for n in (1, 2, 3)]
    head = '<div class="br-head" aria-hidden="true"><span>No.</span><span>The fix</span><span>Days freed</span><span>Beds back every day</span></div>'
    foot = ('<div class="br-foot"%s><span>If all three are agreed</span>%s<span class="br-tot"><span>Days freed a month <b>about 600</b></span>'
            '<span>Beds back every day <b class="br-big">about 20</b></span><span>Worth <b>about ₹1 crore a month</b></span></span></div>' % (pt(3), tag('guess'))) if not empty else ''
    sheet = '<div class="br-sheet%s">%s<div class="br-rows">%s</div>%s</div>' % (' is-empty' if empty else '', head, ''.join(rows), foot)
    body = sheet + ('<div class="br-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'One entry per fix: the days it frees, and the beds that gives back every day. Tap an entry.' if not empty else 'One entry per fix'
    return (masthead('Solutions', state) + standing(d['claim'], d['deck'], empty)
            + section('The beds we get back', body, 'br-sec', sub) + pending(d['pending']) + actions(d['actions']))

SO_CSS = r'''
.br-sheet{background:var(--card);border-top:6px solid var(--ink);background-image:linear-gradient(90deg,transparent 18px,var(--ink) 18px 19px,transparent 19px 22px,var(--ink) 22px 23px,transparent 23px)}
.br-head,.br-row{display:grid;grid-template-columns:62px minmax(0,1fr) 80px 290px;align-items:center;gap:0 14px}
.br-head{border-bottom:3px double var(--ink);padding:8px 40px 8px 0}
.br-head>span{font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.br-head>span:first-child{padding-left:30px}
.br-head>span:nth-child(3){text-align:right}
.br-row{position:relative;width:100%;border:0;border-bottom:1px solid var(--line);background:transparent;text-align:left;padding:12px 40px 12px 0;color:var(--ink);min-width:0}
.lp .br-row.is-up{background:var(--card)}
.br-no{font:400 26px/1 var(--f-d);color:var(--mut);padding-left:30px}
.br-fix{display:flex;flex-direction:column;gap:6px;min-width:0}
.br-fix b{font-size:14.5px;font-weight:600;line-height:1.35}
.br-st{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--mut);flex-wrap:wrap}
.pb-ts{display:flex;gap:3px}
.pb-t{width:14px;height:8px;box-shadow:inset 0 0 0 1.5px var(--grey)}
.pb-t.on{background:var(--ink);box-shadow:none}.pb-t.now{background:var(--hi);box-shadow:inset 0 0 0 1.5px var(--ink)}
.br-n{display:flex;flex-direction:column;gap:2px;text-align:right}
.br-n span{display:none;font-size:11px;font-weight:600;color:var(--mut)}
.br-n b{font:400 28px/1 var(--f-d)}
.br-beds{display:flex;flex-direction:column;gap:5px;min-width:0}
.br-bl{font-size:12.5px;font-weight:600;color:var(--hi-text)}
.br-bs{display:flex;flex-wrap:wrap;gap:3px}
.br-b{display:inline-flex;width:28px;height:20px;padding:1px;background:var(--hi);box-shadow:inset 0 0 0 1.5px var(--ink)}
.br-b svg{width:26px;height:18px;fill:none;stroke:var(--ink);stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.br-row .sel-chev{position:absolute;right:14px;top:50%;margin:-8px 0 0}
.br-row.is-empty{color:var(--mut);cursor:default}
.br-row.is-empty .br-bl{color:var(--mut)}
.br-foot{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding:10px 14px 12px 92px;border-top:3px double var(--ink);font-size:14px;font-weight:600}
.br-tot{margin-left:auto;display:flex;align-items:baseline;gap:20px;flex-wrap:wrap}
.br-tot span{font-size:12.5px;color:var(--mut)}
.br-tot b{font:400 24px/1 var(--f-d);color:var(--ink);margin-left:6px}
.br-tot b.br-big{font-size:30px;border-bottom:5px double var(--ink);background:linear-gradient(transparent 50%,var(--hi) 50% 90%,transparent 90%);padding:0 3px 2px}
.br-sheet.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey)}
.br-desk{margin-top:16px}
.so-ways{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.so-way{padding:12px 14px;background:var(--soft);border-left:4px solid var(--ink)}
.so-way.so-auto{border-left-color:var(--hi)}
.so-way p{font-size:14px;line-height:1.55}
@container lp (max-width:699px){
 .br-sheet{background-image:linear-gradient(90deg,transparent 8px,var(--ink) 8px 9px,transparent 9px 12px,var(--ink) 12px 13px,transparent 13px)}
 .br-head{display:none}
 .br-row{grid-template-columns:40px minmax(0,1fr);grid-template-areas:"no fix" "no n" "no beds";row-gap:10px;padding:12px 40px 14px 0}
 .br-no{grid-area:no;padding-left:20px;font-size:22px;align-self:start}
 .br-n span{display:inline}
 .br-fix{grid-area:fix}.br-n{grid-area:n;text-align:left;flex-direction:row;align-items:baseline;gap:8px}.br-beds{grid-area:beds}
 .br-row .sel-chev{top:16px;margin:0}
 .br-rows .bx-mob{margin:2px 10px 12px 20px}
 .br-foot{padding:10px 12px 12px 24px}
 .br-tot{margin-left:0}
 .so-ways{grid-template-columns:1fr}
}
'''

# ==========================================================================================
# AUTOMATIONS · the hospital's day
LAMPS = ['Idea', 'Built', 'Tested', 'Switched on']
AU = {
 'filled': {
  'claim': 'Three helpers, each at the hour a bed can be freed',
  'deck': 'None is built yet. Each waits for its fix to be agreed. Each one does by itself what a person can also do by hand.',
  'helpers': [
   {'name': 'Ready to move', 'hour': 8, 'when': 'Every morning at 8 AM', 'fix': 'Set each patient’s going-home day on the first day', 'pt': 1,
    'does': 'Lists the patients ready to move today: ICU to step-down, step-down to ward, ward to home, and what each is still waiting for.',
    'reads': 'Doctors’ notes, test results and each patient’s going-home day', 'to': 'The bed manager and the nurse in charge of each area',
    'screen': [('ICU to step-down', '3'), ('Step-down to ward', '4'), ('Ward to home', '21'), ('Still waiting for a report', '6')]},
   {'name': 'Over the expected days', 'hour': 14, 'when': 'Every afternoon at 2 PM', 'fix': 'Set each patient’s going-home day on the first day', 'pt': 2,
    'does': 'Warns when a patient has stayed past their expected going-home day, and says what they are waiting for.',
    'reads': 'Each patient’s going-home day and what is still open', 'to': 'The doctor on duty and the Patient Flow Lead',
    'screen': [('Ward 3 · bed 12', 'Day 6 of 4'), ('Waiting for', 'Scan report'), ('Ward 5 · bed 4', 'Day 9 of 7'), ('Waiting for', 'A ride home')]},
   {'name': 'Free beds for Emergency', 'hour': None, 'when': 'Every hour, day and night', 'fix': 'Move ICU patients to step-down the day they are ready',
    'does': 'Shows Emergency the free and soon-free beds in each area, so patients are sent up as soon as a bed is clean.',
    'reads': 'The bed list and the moves agreed this morning', 'to': 'The Emergency doctor in charge',
    'screen': [('ICU', '1 free'), ('Step-down', '2 free'), ('Wards', '9 free'), ('Free by 2 PM', '11 more')]},
  ],
  'pending': [
   {'text': 'Agree the first fix, so its helpers can be built.', 'pt': 1},
   {'text': 'Find out where the bed list and test results are kept today.', 'need': 'Needs a word with your hospital software team'},
   {'text': 'Agree who answers the 2 PM warning on each ward.', 'pt': 2},
  ],
  'actions': {'go': {'detail': 'Agree the first fix in Solutions', 'say': 'Let’s agree the first fix so its helpers can be built'},
              'add': {'detail': 'Tell Tojo about your systems', 'say': 'Here is how our bed list is kept today: '},
              'jump': {'tab': 'Processes', 'detail': 'See the changes for people', 'say': 'Take me to Processes'}},
  'chat': {'text': ['Three helpers are planned, each at the hour a bed can be freed. None is built yet.', 'Each puts one short list in front of one person.'],
           'pointer': 'Pick a point to add to it, or tap a monitor.',
           'note': 'A bed freed at 10 AM is worth two freed at 6 PM.',
           'points': [{'n': 1, 'label': 'The 8 AM list'}, {'n': 2, 'label': 'The 2 PM warning'}],
           'prompts': ['Where is our bed list kept?', 'Can these work with our software?', 'Show me the people changes']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Helpers are set on the hospital’s day here once a fix is agreed. Each one does one job at one hour.',
  'helpers': [],
  'pending': [{'text': 'Agree a fix in Solutions first.'}, {'text': 'Find out where the bed list and test results are kept today.'}],
  'actions': {'go': {'detail': 'Agree a fix first', 'say': 'Take me to Solutions to agree a fix'},
              'add': {'detail': 'Tell Tojo about your systems', 'say': 'Here is how our bed list is kept today: '},
              'jump': {'tab': 'Processes', 'detail': 'Fills in once a fix is agreed', 'say': 'Take me to Processes'}},
  'chat': {'text': ['This is Automations. Helpers are planned here once a fix is agreed.'],
           'note': 'A helper follows a fix.', 'points': [],
           'prompts': ['Take me to Solutions', 'What does a helper do?', 'Do we need new software?']},
 },
}

def clock(helpers, empty):
    cx = cy = 100; R = 84
    def at(h, r):
        a = (h / 24.0) * 2 * math.pi - math.pi / 2
        return cx + r * math.cos(a), cy + r * math.sin(a)
    # night (8 PM to 6 AM) shaded as an arc band
    x1, y1 = at(20, R - 9); x2, y2 = at(6, R - 9)
    night = '<path d="M%.1f %.1f A%d %d 0 0 1 %.1f %.1f" class="ck-night"/>' % (x1, y1, R - 9, R - 9, x2, y2)
    ticks = ''.join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="ck-t%s"/>' % (at(h, R)[0], at(h, R)[1], at(h, R - (10 if h % 6 == 0 else 5))[0], at(h, R - (10 if h % 6 == 0 else 5))[1], ' ck-tb' if h % 6 == 0 else '') for h in range(24))
    nums = ''.join('<text x="%.1f" y="%.1f" class="ck-n">%s</text>' % (at(h, R - 26)[0], at(h, R - 26)[1] + 5, lab) for h, lab in ((0, 'Midnight'), (6, '6 AM'), (12, 'Noon'), (18, '6 PM')))
    marks = ''
    if not empty:
        hourly = ''.join('<circle cx="%.1f" cy="%.1f" r="2.6" class="ck-hr"/>' % at(h, R + 7) for h in range(24))
        marks = hourly
        for i, h in enumerate(helpers):
            if h['hour'] is None: continue
            x, y = at(h['hour'], R - 9); tx, ty = at(h['hour'], R + 2)
            marks += '<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" class="ck-hand"/><rect x="%.1f" y="%.1f" width="22" height="22" class="ck-tag"/><text x="%.1f" y="%.1f" class="ck-tn">%d</text>' % (
                cx, cy, x, y, tx - 11, ty - 11, tx, ty + 6, i + 1)
    face = '<circle cx="%d" cy="%d" r="%d" class="ck-face"/>' % (cx, cy, R)
    return ('<svg viewBox="-12 -12 224 224" class="ck-svg" role="img" aria-label="%s">%s%s%s%s%s<circle cx="100" cy="100" r="5" class="ck-pin"/></svg>') % (
        e('The hospital’s 24 hours. ' + '; '.join('%s: %s' % (h['name'], h['when']) for h in helpers)) if not empty else 'The hospital’s 24 hours',
        face, night, ticks, nums, marks)

def au_canvas(state):
    d = AU[state]; empty = state == 'empty'
    key = ''.join('<li%s><span class="ck-k">%s</span><span><b>%s</b><em>%s</em></span></li>' % (
        pt(h.get('pt')), str(i + 1) if h['hour'] is not None else '•', e(h['name']), e(h['when'])) for i, h in enumerate(d['helpers']))
    face = '<div class="ck%s">%s<div class="ck-side"><span class="ck-h">The hospital’s day</span><p>%s</p>%s</div></div>' % (
        ' is-empty' if empty else '', clock(d['helpers'], empty),
        'Each helper is set at the hour it runs; the dots round the edge are the hourly one. Night is shaded.' if not empty else 'Helpers are set at their hours once a fix is agreed.',
        '<ul class="ck-key">%s</ul>' % key if key else '')
    mons, desk = [], []
    for i, h in enumerate(d['helpers']):
        k = str(i); first = i == 0
        lamps = ''.join('<span class="au-lp"><i aria-hidden="true"></i>%s</span>' % e(l) for l in LAMPS)
        scr = ''.join('<span class="mn-l"><span>%s</span><b>%s</b></span>' % (e(a), e(v)) for a, v in h['screen'])
        mons.append(('<button class="mn %s" type="button"%s%s><span class="mn-scr"><span class="mn-top"><span class="mn-nm">%s</span><span class="mn-at">%s</span></span>'
                     '<span class="mn-k">What it would show</span>%s</span><span class="mn-foot"><span class="mn-does">%s</span><span class="au-lamps">%s</span></span>%s</button>') % (
            sel_cls(first), sel('mn', k, first), pt(h.get('pt')), e(h['name']), e(h['when']), scr, e(h['does']), lamps, CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>%s</h4>%s</div><p>%s</p>%s%s</div>') % (
            e(h['name']), chip('c-none', 'Not built yet'), e(h['does']), two('What it reads', h['reads'], 'Who sees it', h['to']),
            two('When it runs', h['when'], 'What it waits for', 'The fix: ' + h['fix']))
        mons.append(box('mn', k, det, first, 'mob')); desk.append(box('mn', k, det, first, 'desk'))
    if empty:
        mons = ['<div class="mn is-empty"><span class="mn-scr"><span class="mn-nm">Helper %d</span><span class="mn-off">Screen off until a fix is agreed</span></span></div>' % n for n in (1, 2, 3)]
    body = face + '<div class="mn-rack%s">%s</div>' % (' is-empty' if empty else '', ''.join(mons)) + ('<div class="mn-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'Each helper at the hour it runs, and the monitor it would put up. Tap a monitor.' if not empty else 'Each helper will sit at the hour it runs'
    return (masthead('Automations', state) + standing(d['claim'], d['deck'], empty)
            + section('The hospital’s day', body, 'ck-sec', sub) + pending(d['pending']) + actions(d['actions']))

AU_CSS = r'''
.ck{display:grid;grid-template-columns:230px minmax(0,1fr);gap:26px;align-items:center;background:var(--card);border-top:6px solid var(--ink);padding:14px 20px}
.ck-svg{display:block;width:230px;height:230px}
.ck-face{fill:var(--soft);stroke:var(--ink);stroke-width:4}
.ck-night{fill:none;stroke:var(--ink);stroke-width:14;opacity:.16}
.ck-t{stroke:var(--ink);stroke-width:1.5}.ck-tb{stroke-width:3}
.ck-n{font:600 10.5px var(--f-b);fill:var(--mut);text-anchor:middle}
.ck-hr{fill:var(--hi);stroke:var(--ink);stroke-width:1}
.ck-hand{stroke:var(--ink);stroke-width:3}
.ck-tag{fill:var(--hi);stroke:var(--ink);stroke-width:2}
.ck-tn{font:400 17px var(--f-d);fill:var(--ink);text-anchor:middle}
.ck-pin{fill:var(--ink)}
.ck-side{display:flex;flex-direction:column;gap:8px;min-width:0}
.ck-h{font:400 24px/1 var(--f-d)}
.ck-side p{font-size:13.5px;line-height:1.5;color:var(--mut)}
.ck-key{display:flex;flex-direction:column}
.ck-key li{display:flex;align-items:center;gap:12px;padding:7px 0;border-bottom:1px solid var(--line)}
.ck-k{flex-shrink:0;width:26px;height:26px;display:flex;align-items:center;justify-content:center;font:400 18px/1 var(--f-d);background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.ck-key li span:last-child{display:flex;flex-direction:column;gap:1px;min-width:0}
.ck-key b{font-size:14px;font-weight:600}
.ck-key em{font-style:normal;font-size:12.5px;color:var(--mut)}
.ck.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey)}
.ck.is-empty .ck-face{fill:transparent;stroke:var(--grey);stroke-width:2;stroke-dasharray:5 4}
.ck.is-empty .ck-night{display:none}
.mn-rack{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;align-items:start;margin-top:16px;padding:14px;background:var(--soft);box-shadow:inset 0 -6px 0 var(--ink)}
.mn{position:relative;display:flex;flex-direction:column;width:100%;border:0;padding:8px 8px 0;background:var(--card);box-shadow:inset 0 0 0 2px var(--ink);text-align:left;color:var(--ink);min-width:0}
.mn-scr{display:flex;flex-direction:column;gap:4px;background:var(--panel);color:#fff;padding:10px 12px 12px}
.mn-top{display:flex;flex-direction:column;gap:2px;padding-right:22px;padding-bottom:6px;border-bottom:1px dashed rgba(255,255,255,.4);margin-bottom:2px}
.mn-nm{font:400 22px/1 var(--f-d);letter-spacing:.02em;color:var(--hi-dark)}
.mn-at{font-size:12px;font-weight:600;color:#fff}
.mn-k{font-size:10.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:#fff;opacity:.85}
.mn-l{display:flex;justify-content:space-between;gap:8px;font-size:12.5px;line-height:1.4}
.mn-l b{font-weight:600;color:var(--hi-dark);white-space:nowrap}
.mn-foot{display:flex;flex-direction:column;gap:8px;padding:10px 4px 12px}
.mn-does{font-size:13px;line-height:1.45}
.au-lamps{display:flex;flex-wrap:wrap;gap:4px 12px}
.au-lp{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:600;color:var(--mut)}
.au-lp i{width:10px;height:10px;border-radius:50%;box-shadow:inset 0 0 0 1.5px var(--grey)}
.mn .sel-chev{position:absolute;right:16px;top:18px;margin:0;color:#fff}
.mn-off{margin-top:8px;font-size:12.5px;font-weight:600;color:var(--mut)}
.mn.is-empty{box-shadow:inset 0 0 0 1.5px var(--grey);padding-bottom:8px}
.mn.is-empty .mn-scr{background:var(--soft)}
.mn.is-empty .mn-nm{color:var(--mut)}
.mn-rack.is-empty{background:transparent;box-shadow:inset 0 0 0 2px var(--grey)}
.mn-desk{margin-top:16px}
@container lp (max-width:699px){
 .ck{grid-template-columns:1fr;justify-items:center;padding:14px}
 .ck-side{align-self:stretch}
 .mn-rack{grid-template-columns:1fr;padding:10px}
 .mn-rack .bx-mob{margin:-6px 0 4px}
}
'''

# ==========================================================================================
# PROCESSES · the week on the bed board
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
PR = {
 'filled': {
  'claim': 'A bed round every morning, and one owner for the flow',
  'deck': 'Nothing is tried yet. Each change waits for its fix to be agreed. We start with a two-month trial on two wards.',
  'changes': [
   {'name': 'Fifteen-minute bed round', 'days': [0, 1, 2, 3, 4, 5, 6], 'when': 'Every day, 9:30 AM', 'who': 'Patient Flow Lead, nurses in charge of each area', 'pt': 1,
    'what': 'Standing at the bed board, the group agrees every move today: who goes home, who moves up or down, and what each is waiting for.',
    'why': 'Moves agreed at 9:30 AM free beds before noon, when Emergency needs them most.'},
   {'name': 'Long-stay review', 'days': [2], 'when': 'Wednesday, 3 PM, 45 minutes', 'who': 'Medical director, Patient Flow Lead, two senior doctors', 'pt': 2,
    'what': 'Every patient past seven days is reviewed: what holds them, who unblocks it, and by when.',
    'why': 'A few long stays take many beds. They need a senior eye once a week.'},
   {'name': 'Senior doctor’s weekend round', 'days': [5, 6], 'when': 'Saturday and Sunday, 10 AM', 'who': 'One senior doctor on a rota',
    'what': 'A senior doctor sees every patient due home and signs off those who are ready, as on a weekday.',
    'why': 'Today weekend patients wait for Monday’s round.'},
   {'name': 'A Patient Flow Lead', 'days': [], 'when': 'Full time, new role', 'who': 'Reports to the medical director', 'pt': 3,
    'what': 'One person owns the extra days: runs the bed round, answers the 2 PM warning, and brings the weekly review.',
    'why': 'Today the extra days belong to everyone, so no one closes them.'},
  ],
  'owners': [('Emergency', 'Emergency head', False), ('ICU', 'ICU head', False), ('Step-down', 'Step-down nurse in charge', False),
             ('Wards', 'Ward nurses in charge', False), ('Going home', 'Patient Flow Lead', True)],
  'numbers': [
   {'name': 'Average stay, in days', 'now': '4.6', 'plan': '3.9', 'dir': 'Lower is better'},
   {'name': 'Emergency wait for a bed, in minutes', 'now': '310', 'plan': '240', 'dir': 'Lower is better'},
   {'name': 'Patients home by noon, of every 100', 'now': '18', 'plan': '50', 'dir': 'Higher is better'},
   {'name': 'Patients past their going-home day, today', 'now': '43', 'plan': '15', 'dir': 'Lower is better'},
  ],
  'pending': [
   {'text': 'Name the Patient Flow Lead, and who stands in for them.', 'need': 'Needs your choice of person', 'pt': 3},
   {'text': 'Agree the time of the daily bed round.', 'pt': 1},
   {'text': 'Pick the two wards for the trial.'},
  ],
  'actions': {'go': {'detail': 'Name the Patient Flow Lead', 'say': 'Let’s name the Patient Flow Lead'},
              'add': {'detail': 'Tell Tojo about your team', 'say': 'Here is who manages beds today: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Back to where the work stands', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Three changes set the week: a bed round every day, a long-stay review on Wednesday and a senior round at weekends. One new role owns the flow.',
                    'Nothing is tried yet. A two-month trial on two wards comes first.'],
           'pointer': 'Pick a point to add to it, or tap a change on the board.',
           'note': 'Every bed has a plan. Every plan has an owner.',
           'points': [{'n': 1, 'label': 'The daily bed round'}, {'n': 2, 'label': 'The long-stay review'}, {'n': 3, 'label': 'The Patient Flow Lead'}],
           'prompts': ['Our nursing head could lead the round', 'Who should join the bed round?', 'How long does this take each week?']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Changes are pinned on the week here once a fix is agreed: what happens each day, who owns the flow in each area, and the numbers we watch.',
  'changes': [], 'owners': [], 'numbers': [],
  'pending': [{'text': 'Agree a fix in Solutions first.'}, {'text': 'Tell Tojo who manages beds today.'}],
  'actions': {'go': {'detail': 'Agree a fix first', 'say': 'Take me to Solutions to agree a fix'},
              'add': {'detail': 'Tell Tojo about your team', 'say': 'Here is who manages beds today: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Every conversation starts here', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['This is Processes. Changes for people are planned here once a fix is agreed.'],
           'note': 'Give the flow an owner.', 'points': [],
           'prompts': ['Take me to Solutions', 'Who usually owns the beds?', 'What is a Patient Flow Lead?']},
 },
}

def pr_canvas(state):
    d = PR[state]; empty = state == 'empty'
    rows, desk = [], []
    for i, c in enumerate(d['changes']):
        k = str(i); first = i == 0
        if c['days']:
            cells = ''.join('<span class="wk-c%s">%s</span>' % (' on' if j in c['days'] else '', '<i class="wk-mag" aria-hidden="true"></i>' if j in c['days'] else '') for j in range(7))
        else:
            cells = '<span class="wk-role">New role · %s</span>' % e(c['who'])
        rows.append(('<button class="wk-r %s" type="button"%s%s><span class="wk-nm"><b>%s</b><span>%s</span></span><span class="wk-days">%s</span>%s</button>') % (
            sel_cls(first), sel('wk', k, first), pt(c.get('pt')), e(c['name']), e(c['when']), cells, CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>%s</h4>%s</div><p>%s</p>%s</div>') % (
            e(c['name']), chip('c-none', 'Not tried yet'), e(c['what']), two('Who and when', '%s · %s' % (c['who'], c['when']), 'Why it helps', c['why']))
        rows.append(box('wk', k, det, first, 'mob')); desk.append(box('wk', k, det, first, 'desk'))
    head = '<div class="wk-h" aria-hidden="true"><span>The change</span><span class="wk-days">%s</span></div>' % ''.join('<span>%s</span>' % dd for dd in DAYS)
    trial = ('<div class="wk-trial"><b>Trial</b><span>Two months, two wards</span><span class="wk-m"><i>Month 1</i><i>Month 2</i></span></div>') if not empty else ''
    if empty:
        rows = ['<div class="wk-r is-empty"><span class="wk-nm"><b>Not pinned yet</b><span>Fills in once a fix is agreed</span></span><span class="wk-days">%s</span></div>' % (
            '<span class="wk-c"></span>' * 7)]
    board = '<div class="wk%s"><div class="wk-bt">Bed board · the week</div>%s<div class="wk-rows">%s</div>%s</div>' % (' is-empty' if empty else '', head, ''.join(rows), trial)
    body = board + ('<div class="wk-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'The changes pinned on the days they happen. Tap a change.' if not empty else 'The changes, pinned on their days'
    if d['owners']:
        own = ''.join('<div class="fo-c%s"><span class="fo-a">%s</span><b>%s</b>%s</div>' % (' fo-new' if new else '', e(a), e(o), chip('c-now', 'New role') if new else '')
                      for a, o, new in d['owners'])
        owners = '<div class="fo">%s</div>' % own
        nums = ''.join(('<div class="pv"><span class="pv-n">%s<em>%s</em></span>'
                        '<span class="pv-v"><span>Now <b>%s</b></span><i class="pv-ar" aria-hidden="true"></i><span>Plan <b class="pv-p">%s</b></span></span></div>') % (
            e(n['name']), e(n['dir']), e(n['now']), e(n['plan'])) for n in d['numbers'])
        numsec = '<div class="pvs">%s</div><p class="fx-hint">Now: Example only. Plan: Tojo’s guess, to agree with you.</p>' % nums
        extra = (section('Who owns the flow in each area', owners, 'fo-sec', 'From Emergency to home, every area has one owner')
                 + section('The numbers we watch: now and plan', numsec, 'pv-sec', 'Read every morning at the bed round'))
    else:
        extra = section('Who owns the flow in each area', '<p class="fx-empty">Owners are written here once a change is agreed.</p>', 'fo-sec')
    return (masthead('Processes', state) + standing(d['claim'], d['deck'], empty)
            + section('The week on the bed board', body, 'wk-sec', sub) + extra + pending(d['pending']) + actions(d['actions']))

PR_CSS = r'''
.wk{background:var(--card);box-shadow:inset 0 0 0 3px var(--ink),0 0 0 6px var(--soft),0 0 0 7px var(--line)}
.wk-bt{background:var(--ink);color:var(--card);font:400 22px/1 var(--f-d);letter-spacing:.04em;padding:10px 16px}
.wk-h,.wk-r{display:grid;grid-template-columns:minmax(0,1fr) 392px;gap:14px;align-items:center}
.wk-h{padding:8px 40px 6px 16px;border-bottom:2px solid var(--ink)}
.wk-h>span:first-child{font-size:11.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.wk-days{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:4px}
.wk-h .wk-days span{text-align:center;font:400 18px/1 var(--f-d);color:var(--mut)}
.wk-r{position:relative;width:100%;border:0;border-bottom:1px solid var(--line);padding:9px 40px 9px 16px;background:transparent;text-align:left;color:var(--ink)}
.lp .wk-r.is-up{background:var(--hi-soft)}
.wk-nm{display:flex;flex-direction:column;gap:2px;min-width:0}
.wk-nm b{font:400 22px/1 var(--f-d)}
.wk-nm span{font-size:12.5px;color:var(--mut)}
.wk-c{position:relative;height:34px;background:repeating-linear-gradient(transparent 0 8px,var(--soft) 8px 9px);box-shadow:inset 0 0 0 1px var(--line)}
.wk-c.on{background:var(--card);box-shadow:inset 0 0 0 1.5px var(--ink)}
.wk-mag{position:absolute;left:50%;top:50%;width:18px;height:18px;margin:-9px 0 0 -9px;border-radius:50%;background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink),0 2px 0 var(--ink)}
.wk-role{grid-column:1/-1;font-size:12.5px;font-weight:600;padding:9px 12px;background:var(--hi-soft);box-shadow:inset 4px 0 0 var(--hi)}
.wk-r .sel-chev{position:absolute;right:14px;top:50%;margin:-8px 0 0}
.wk-trial{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:8px 16px;border-top:3px double var(--ink);font-size:13.5px}
.wk-trial b{font:400 22px/1 var(--f-d)}
.wk-m{display:flex;gap:4px;margin-left:auto}
.wk-m i{font-style:normal;font-size:12px;font-weight:600;padding:3px 10px;box-shadow:inset 0 0 0 1.5px var(--grey);color:var(--mut)}
.wk.is-empty{box-shadow:inset 0 0 0 2px var(--grey)}
.wk.is-empty .wk-bt{background:var(--soft);color:var(--mut)}
.wk-r.is-empty{color:var(--mut);cursor:default}.wk-r.is-empty .wk-nm b{color:var(--mut)}
.wk-desk{margin-top:16px}
.fo{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));background:var(--card);border-top:6px solid var(--ink)}
.fo-c{display:flex;flex-direction:column;align-items:flex-start;gap:5px;padding:12px 14px 14px;border-right:1px solid var(--line);position:relative}
.fo-c:last-child{border-right:0}
.fo-c:not(:last-child)::after{content:"";position:absolute;right:-7px;top:16px;width:12px;height:12px;background:var(--card);border-top:2px solid var(--ink);border-right:2px solid var(--ink);transform:rotate(45deg);z-index:1}
.fo-a{font:400 20px/1 var(--f-d)}
.fo-c b{font-size:13.5px;font-weight:600;line-height:1.35}
.fo-new{background:var(--hi-soft)}
.pvs{display:grid;grid-template-columns:1fr 1fr;column-gap:28px;background:var(--card);border-top:6px solid var(--ink);padding:4px 16px 8px}
.pv{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid var(--line)}
.pv-n{font-size:14px;font-weight:600;line-height:1.35}
.pv-n em{display:block;font-style:normal;font-size:12px;font-weight:600;color:var(--mut);margin-top:2px}
.pv-v{display:flex;justify-content:flex-end;align-items:baseline;gap:10px;flex-wrap:wrap;max-width:200px}
.pv-v span{font-size:12px;font-weight:600;color:var(--mut)}
.pv-v b{font:400 22px/1 var(--f-d);color:var(--ink);margin-left:4px}
.pv-v b.pv-p{color:var(--hi-text)}
.pv-ar{width:22px;height:2px;background:var(--ink);position:relative;align-self:center}
.pv-ar::after{content:"";position:absolute;right:-1px;top:-4px;border-left:7px solid var(--ink);border-top:5px solid transparent;border-bottom:5px solid transparent}
@container lp (max-width:699px){
 .wk-h{grid-template-columns:1fr;padding:8px 40px 6px 12px}
 .wk-h>span:first-child{display:none}
 .wk-r{grid-template-columns:1fr;gap:8px;padding:10px 40px 12px 12px}
 .wk-days{grid-template-columns:repeat(7,minmax(0,1fr))}
 .wk-r .sel-chev{top:14px;margin:0}
 .wk-rows .bx-mob{margin:2px 10px 10px}
 .wk-m{margin-left:0}
 .fo{grid-template-columns:1fr}
 .fo-c{border-right:0;border-bottom:1px solid var(--line);flex-direction:row;flex-wrap:wrap;align-items:baseline;gap:4px 10px}
 .fo-c:not(:last-child)::after{right:auto;left:22px;top:auto;bottom:-7px;transform:rotate(135deg)}
 .pvs{padding:4px 12px 8px;grid-template-columns:1fr}
 .pv{grid-template-columns:1fr;gap:6px}
 .pv-v{justify-content:flex-start;max-width:none}
}
'''

# ==========================================================================================
PAGES = {
 'home': (None, None, 'Home', 'The patient’s path (approved)'),
 'diagnosis': ('Diagnosis', (dg_canvas, DG_CSS, DG), 'Diagnosis', 'One patient’s chart'),
 'solutions': ('Solutions', (so_canvas, SO_CSS, SO), 'Solutions', 'The beds we get back'),
 'automations': ('Automations', (au_canvas, AU_CSS, AU), 'Automations', 'The hospital’s day'),
 'processes': ('Processes', (pr_canvas, PR_CSS, PR), 'Processes', 'The week on the bed board'),
}
ABOUT = {
 'home': ('<b>Home · The patient’s path.</b> Approved as sample A. The stay as a route from Emergency through the ICU, step-down and the wards to home, each stop against its goal; '
          'each part of the work a patient wristband. <em>Colours: aqua, petrol, coral red. The rail now carries each place’s own colour.</em>'),
 'diagnosis': ('<b>Diagnosis · One patient’s chart.</b> One typical stay followed day by day: a strip of the days in each area with the extra hatched, then each step as a line of the chart '
               '(when, where, what happened, the extra), its line opening beside the chart. Below it, the 1,300 extra days split by cause, one square for every 13 days. '
               '<em>From sample C (the stay chart). Colours: pale rose, deep cobalt, spring green.</em>'),
 'solutions': ('<b>Solutions · The beds we get back.</b> One ruled entry per fix: its four stops, the days it frees a month, and the beds that gives back every day, drawn as beds. '
               'A double-ruled total. Each entry opens to its by-hand and automatic versions. <em>From sample B (beds as the unit). Colours: pale lemon, graphite, magenta.</em>'),
 'automations': ('<b>Automations · The hospital’s day.</b> A 24-hour clock face with night shaded and each helper set at its hour; one bedside monitor per helper showing what it would put up, '
                 'with its four lamps. <em>From sample C (the monitors). Colours: pale butter, ox-blood, monitor yellow.</em>'),
 'processes': ('<b>Processes · The week on the bed board.</b> A whiteboard week with each change as a magnet on its days, the new role and a two-month trial; who owns the flow in each area, '
               'Emergency to home; the numbers we watch, now and plan. <em>From sample B (the bed board). Colours: whiteboard, indigo, marker cyan.</em>'),
}

def build():
    os.makedirs(OUT, exist_ok=True)
    pages, words = {}, []
    base = L2.V_SHARED_CSS + L3.PLACE_CSS
    for k, (place, spec, label, title) in PAGES.items():
        t = THEMES[k]
        for st in ('filled', 'empty'):
            if spec is None:
                canvas, css, chat, cls = H.a_canvas(st), base + H.A_CSS, H.DATA[st]['chat'], 'ls ls-home ls-a'
            else:
                fn, pcss, data = spec
                canvas, css, chat, cls = fn(st), base + pcss, data[st]['chat'], 'ls ls-%s' % k
            for v in ('desktop', 'mobile'):
                h = C.page(SK, t, place, canvas, css, chat, v, 'Length of Stay · %s' % label, cls)
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(OUT, 'los-%s.%s.%s.html' % (k, v, st)), 'w', encoding='utf-8').write(h)
            text = re.sub(r'<[^>]+>', ' ', canvas) + ' ' + json.dumps(chat, ensure_ascii=False)
            words += [(k, st, w) for w in C.plain_check(text)]
    return pages, words

def review(pages):
    tpl = open(os.path.join(H.SCP, 'review_template.html'), encoding='utf-8').read()
    for old in ('Supply Chain and Procurement · the home page in three looks', 'Supply Chain and Procurement · three looks for the Financial domain'):
        tpl = tpl.replace(old, 'Length of Stay · the five landing pages')
    tpl = re.sub(r'<p class="rv-intro">.*?</p>', '<p class="rv-intro">The tool’s home page (the patient’s path, approved) and its four place pages, in the Financial look: '
                 'Virevo type unchanged, flat frame, ledger and report paper. Each place has its own colours and its own drawing of a hospital stay, using ideas from the two samples not chosen '
                 '(the bed board and the stay chart). Pick a page below. Every page opens with its first item raised and its box open; on the phone, each box opens right under the item you tap.</p>', tpl, flags=re.S)
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>%s</b><span>%s</span><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 4px %s"></i></button>' % (
        k, 'true' if k == 'home' else 'false', v[2], e(v[3]), THEMES[k]['ground'], THEMES[k]['ink'], THEMES[k]['hi']) for k, v in PAGES.items())
    return (tpl.replace('@@PICKS@@', picks).replace('@@ABOUT@@', json.dumps(ABOUT, ensure_ascii=False))
               .replace('@@DATA@@', json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')))

if __name__ == '__main__':
    pages, words = build()
    if words:
        print('PLAIN ENGLISH:', words)
    rv = os.path.join(OUT, 'length-of-stay-landing-pages.html')
    open(rv, 'w', encoding='utf-8').write(review(pages))
    print('built', rv, os.path.getsize(rv))
