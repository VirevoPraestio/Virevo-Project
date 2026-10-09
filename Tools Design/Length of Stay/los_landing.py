"""
Length of Stay: the tool's home page in three looks (8 Oct 2026, for review).

The third Financial tool. Every kind of stay: the wait in Emergency for a bed, days in the ICU, in the
step-down unit, on the wards, and the hospital as a whole. Each extra day is a bed someone else waits
for, and a day the hospital pays for but is often not paid for (fixed-price packages), so the tool sits
in the Financial domain.

It uses the Financial identity approved for Supply Chain and Procurement (the V skin: Virevo type
unchanged, flat frame, report sheet, ledger paper, receipt) and changes only its colours, which no
other tool uses. No reference file yet; every figure is made up for an example 250-bed hospital and
marked Example only or Tojo's guess.

Same five zones as every landing page, in the same order: masthead with stamp and Refresh now, where
this stands, the drawing, what Tojo still has to do, the three buttons. Same behaviour: first element
raised with its box open, on a phone each box under its element, pickable items stacked.

  A  The patient's path   the stay drawn as a route through the hospital (Emergency, ICU, step-down,
                          ward, home), each stop with its days against the goal; each part of the
                          work a patient wristband, one day box per step.
  B  The bed board        today's 250 beds as a census grid, area by area, the beds held by patients
                          ready to go home marked; each part of the work a row on the ward's bed board.
  C  The stay chart       one average stay as a chart of days, needed and extra, area by area; each
                          part of the work a bedside monitor, its trace climbing one step per step done.

Run:  python3 los_landing.py   ->  out/landing/
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
SCP = os.path.join(TOOLS, 'Supply Chain Procurement')       # the Financial look lives with the first Financial tool
sys.path[:0] = [HERE, SCP]
import sc_common as C
C.TOOL = 'Length of Stay'
C.HOSPITAL = 'Example hospital · 250 beds'
C.B.TOOL = C.TOOL
C.B.HOSPITAL[:] = [C.HOSPITAL]
from sc_common import e, ico, ICONS, CHEV, sel, sel_cls, box, pt, tag, say_btn, standing, section, pending, actions, STAMP
from skins import SKINS
import landing2 as L2
import landing3 as L3

SK = SKINS['f']
OUT = os.path.join(HERE, 'out', 'landing')
KICK = 'Virevo · ' + C.HOSPITAL
# The tool's mark: a hospital bed with a clock over it.
MARK = ('<path d="M2 20V8"/><path d="M2 15h20v5"/><path d="M22 15v-2a2 2 0 0 0-2-2h-9v4"/><circle cx="6.5" cy="12.5" r="1.8"/>'
        '<circle cx="17" cy="5" r="3.2"/><path d="M17 3.4V5l1.2 1"/>')

STEP = {'done': 'Done', 'now': 'Now', 'later': 'Still to do', 'none': 'Not started'}
STATUS = {'now': 'In use now', 'started': 'Taking shape', 'none': 'Not started', 'empty': 'Nothing yet'}

# ==========================================================================================
# The words (one set for all three looks)
AREAS = [
 # key, name, what, now, goal, unit, extra a month, cost of one extra day, cost a month
 {'k': 'er', 'name': 'Emergency', 'what': 'Wait for a bed', 'now': 5.2, 'goal': 4.0, 'unit': 'hours', 'nowt': '5 hours 10 minutes', 'goalt': '4 hours',
  'extra': 'About 14 patients a day wait longer', 'cost': None},
 {'k': 'icu', 'name': 'ICU', 'what': 'Intensive care', 'now': 4.8, 'goal': 3.5, 'unit': 'days', 'nowt': '4.8 days', 'goalt': '3.5 days',
  'extra': 'About 180 extra days a month', 'day': '₹45,000 a day', 'cost': '₹81 lakh'},
 {'k': 'sd', 'name': 'Step-down', 'what': 'Between ICU and ward', 'now': 2.9, 'goal': 2.0, 'unit': 'days', 'nowt': '2.9 days', 'goalt': '2 days',
  'extra': 'About 220 extra days a month', 'day': '₹22,000 a day', 'cost': '₹48 lakh'},
 {'k': 'wd', 'name': 'Wards', 'what': 'On the ward', 'now': 4.1, 'goal': 3.5, 'unit': 'days', 'nowt': '4.1 days', 'goalt': '3.5 days',
  'extra': 'About 900 extra days a month', 'day': '₹9,000 a day', 'cost': '₹81 lakh'},
]
STAY = {
 'areas': AREAS,
 'avg': ('Average stay, whole hospital', '4.6 days'), 'goal': 'Goal: 3.9 days',
 'extra': ('Extra days a month', 'About 1,300'), 'cost': ('What the extra days cost', 'About ₹2.1 crore a month'),
 'held': 'About 43 beds a day held by patients ready to go',
}
DATA = {
 'filled': {
  'claim': 'Patients stay longer than they need to.',
  'deck': 'A patient stays 4.6 days on average; the goal is 3.9. The extra days cost about ₹2.1 crore a month and keep Emergency waiting for beds. Diagnosis is two steps in. Nothing is changed yet.',
  'stay': STAY,
  'places': [
   {'name': 'Diagnosis', 'status': 'now', 'pt': 1, 'head': 'About 1,300 extra days a month, mostly patients ready to go home but still waiting.',
    'fig': ('About 1,300', 'extra days a month', 'example'), 'unit': 'steps done', 'short': 'Finds where the extra days come from',
    'steps': [['Put a number on the extra days', 'done'], ['Split the days by area: Emergency, ICU, step-down, wards', 'done'],
              ['Count the days patients wait while ready to go home', 'now'], ['Find what one extra day costs in each area', 'later'], ['Name the main cause', 'later']]},
   {'name': 'Solutions', 'status': 'started', 'pt': 3, 'head': 'Three fixes on the table. One is taking shape.',
    'fig': ('About 600', 'days a month could come back', 'guess'), 'unit': 'fixes agreed', 'short': 'Could free about 600 days a month',
    'steps': [['Set each patient’s going-home day on the first day', 'now'], ['Move ICU patients to step-down the day they are ready', 'later'],
              ['Run scans and tests on weekends too', 'later']]},
   {'name': 'Automations', 'status': 'none', 'head': 'Three helpers wait for the fixes to be agreed.', 'fig': None, 'unit': 'switched on',
    'short': 'Keeps the days from creeping back',
    'steps': [['Sends the list of patients ready to move at 8 AM', 'none'], ['Warns when a patient passes their expected days', 'none'],
              ['Shows Emergency the free beds every hour', 'none']]},
   {'name': 'Processes', 'status': 'none', 'head': 'Three changes and one new role wait for a trial.', 'fig': None, 'unit': 'tried',
    'short': 'Makes the fixes a habit',
    'steps': [['A fifteen-minute bed round every morning', 'none'], ['The going-home day written on the first day', 'none'],
              ['A senior doctor’s round on weekends', 'none'], ['A Patient Flow Lead who owns the extra days', 'none']]},
  ],
  'pending': [
   {'text': 'Get three months of admission and going-home times, by area.', 'need': 'Needs the records desk’s list', 'pt': 2},
   {'text': 'Find which tests most often hold a patient back.', 'pt': 4},
   {'text': 'Check how many patients go home on Saturday and Sunday.'},
   {'text': 'Find what one extra day in the ICU really costs.', 'need': 'Needs last quarter’s ICU costs'},
  ],
  'actions': {'go': {'detail': 'Count the days patients wait while ready to go', 'say': 'Let’s count the days patients wait while ready to go home'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about how long patients stay: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Pick up where you left off', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Here is where the Length of Stay work stands, across all four parts.',
                    'Diagnosis is two steps in. Patients stay 4.6 days on average against a goal of 3.9, and the ICU runs furthest over.',
                    'Two things would sharpen this: the admission and going-home times, and which tests hold patients back.'],
           'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
           'note': 'Every extra day is a bed someone else is waiting for.',
           'points': [{'n': 1, 'label': 'The stay, area by area'}, {'n': 2, 'label': 'Admission and going-home times'},
                      {'n': 3, 'label': 'The three fixes'}, {'n': 4, 'label': 'Tests that hold patients back'}],
           'prompts': ['Let’s count the days patients wait', 'Why is the ICU so far over?', 'Show me the three fixes']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Start with Diagnosis. Tojo puts a number on how long patients stay in each area, then follows a stay from Emergency to home with you, and fills this page as you go.',
  'stay': None,
  'places': [
   {'name': 'Diagnosis', 'status': 'empty', 'head': 'Fills in as you put a number on the stay.', 'fig': None, 'steps': [], 'short': 'Fills in as we go'},
   {'name': 'Solutions', 'status': 'empty', 'head': 'Fills in once the main cause is named.', 'fig': None, 'steps': [], 'short': 'Fills in later'},
   {'name': 'Automations', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': [], 'short': 'Fills in later'},
   {'name': 'Processes', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': [], 'short': 'Fills in later'},
  ],
  'pending': [
   {'text': 'Put a number on the average stay in each area.', 'need': 'Needs three months of admission and going-home times'},
   {'text': 'Find how long Emergency patients wait for a bed.'},
   {'text': 'Find what one day costs in the ICU, step-down and the wards.'},
  ],
  'actions': {'go': {'detail': 'Put a number on the stay with Tojo', 'say': 'Let’s put a number on how long patients stay'},
              'add': {'detail': 'Share admission and going-home times', 'say': 'Here is what I already know about how long patients stay: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Every conversation starts here', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Welcome to Length of Stay. This page fills in as we talk.',
                    'We start by putting a number on how long patients stay: in Emergency, the ICU, step-down and on the wards.'],
           'note': 'Count the days. Then find the ones nobody needed.', 'points': [],
           'prompts': ['Let’s put a number on the stay', 'What should I bring?', 'Why is this a money question?']},
 },
}

def counts(p):
    return sum(1 for _, s in p['steps'] if s == 'done'), len(p['steps'])

def prog(p):
    d, n = counts(p)
    return '%d of %d %s' % (d, n, p['unit']) if n else 'No steps yet'

def masthead(state):
    return C.masthead(KICK, '<span class="bm-emb">%s</span>' % ico(MARK, 'var(--hi)', 28), STAMP[state])

def detail(p):
    return L2.place_detail(p, 'vx')

def wrap(d, inner, cls, sub, desk, empty):
    return (inner + ('<div class="%s-desk">%s</div>' % (cls, ''.join(desk)) if desk else ''))

def page(state, top, body, cls, sub):
    d = DATA[state]
    return masthead(state) + top + section('Where each part of the work stands', body, cls + '-sec', sub) + pending(d['pending']) + actions(d['actions'])

def pick(cls, grp, i, p, inner, empty, rows, desk, tagname='button'):
    k = str(i); first = i == 0 and not empty
    if empty:
        rows.append('<div class="%s is-empty" data-s="empty">%s</div>' % (cls, inner)); return
    rows.append('<button class="%s %s" type="button" data-s="%s"%s%s>%s</button>' % (cls, sel_cls(first), p['status'], sel(grp, k, first), pt(p.get('pt')), inner + CHEV))
    det = detail(p); rows.append(box(grp, k, det, first, 'mob')); desk.append(box(grp, k, det, first, 'desk'))

# ==========================================================================================
# A · THE PATIENT'S PATH
def path_panel(s):
    if not s:
        return '<aside class="la-path is-empty"><b class="v-ach">The stay, area by area</b><p>Draws the route from Emergency to home once three months of times are in.</p></aside>'
    stops = []
    for a in s['areas']:
        pct = min(a['now'], a['goal'] * 1.6) / (a['goal'] * 1.6) * 100
        gl = a['goal'] / (a['goal'] * 1.6) * 100
        stops.append(('<div class="la-stop la-%s"><i class="la-dot" aria-hidden="true"></i><div class="la-sh"><b>%s</b><span>%s</span>'
                      '<span class="la-nums"><b>%s</b> · goal %s</span></div>'
                      '<div class="la-bar" aria-hidden="true"><i style="width:%.1f%%"></i><em style="left:%.1f%%"></em></div><div class="la-x">%s%s</div></div>') % (
            a['k'], e(a['name']), e(a['what']), e(a['nowt']), e(a['goalt']), pct, gl, e(a['extra']), (' · ' + e(a['cost'])) if a.get('cost') else ''))
    stops.append('<div class="la-stop la-home"><i class="la-dot" aria-hidden="true"></i><div class="la-sh"><b>Home</b><span>%s</span></div></div>' % e(s['held']))
    return ('<aside class="la-path"%s><div class="v-ah"><b class="v-ach">The stay, area by area</b>%s</div><div class="la-route">%s</div>'
            '<div class="v-atot"><span>%s<br><small>%s · %s</small></span><b>%s</b></div>'
            '<div class="v-asaved"><span>%s</span><b>%s</b></div></aside>') % (
        pt(1), tag('example'), ''.join(stops), e(s['avg'][0]), e(s['goal']), e(s['extra'][1] + ' extra days a month'), e(s['avg'][1]), e(s['cost'][0]), e(s['cost'][1]))

def a_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    top = '<div class="v-top la-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), path_panel(d['stay']))
    rows, desk = [], []
    for i, p in enumerate(d['places']):
        days = ''.join('<span class="lw-d s-%s"><small>Day</small>%d<span class="sr"> %s</span></span>' % (s, j + 1, e(STEP[s])) for j, (_, s) in enumerate(p['steps'])) \
            or '<span class="lw-none">No days yet</span>'
        d_, n = counts(p)
        inner = ('<span class="lw-snap" aria-hidden="true"></span><span class="lw-lab"><span class="lw-k">Tojo · %s · part %d of 4</span>'
                 '<b class="lw-n">%s%s</b><span class="lw-s">%s</span></span>'
                 '<span class="lw-days">%s</span><span class="lw-meta"><span class="v-st s-%s">%s</span><span class="lw-p">%s</span></span>'
                 '<span class="lw-code" aria-hidden="true"></span>') % (
            e(C.TOOL), i + 1, ico(ICONS[p['name']], 'currentColor', 20), e(p['name']), e(p['short']), days, p['status'], e(STATUS[p['status']]), e(prog(p)))
        pick('lw-band', 'lw', i, p, inner, empty, rows, desk)
    body = '<div class="lw-tray%s">%s</div>' % (' is-empty' if empty else '', ''.join(rows))
    key = ('<div class="v-key lw-key" aria-hidden="true"><span><i class="lw-d s-done"></i>Done</span><span><i class="lw-d s-now"></i>Now</span>'
           '<span><i class="lw-d s-later"></i>Still to do</span><span><i class="lw-d s-none"></i>Not started</span></div>') if not empty else ''
    sub = 'One wristband per part, one day box per step. Tap a band.' if not empty else 'One wristband for each part of the work'
    return page(state, top, body + key + ('<div class="la-desk">%s</div>' % ''.join(desk) if desk else ''), 'la', sub)

A_CSS = r'''
.la-top{grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:32px}
.la-path{background:var(--card);border-top:6px solid var(--ink);padding:16px 18px 16px;display:flex;flex-direction:column;gap:6px}
.la-route{position:relative;display:flex;flex-direction:column;gap:0;margin:4px 0 6px}
.la-route::before{content:"";position:absolute;left:8px;top:10px;bottom:14px;width:4px;background:var(--ink)}
.la-stop{position:relative;padding:0 0 9px 30px;display:flex;flex-direction:column;gap:3px}
.la-dot{position:absolute;left:0;top:2px;width:20px;height:20px;background:var(--card);box-shadow:inset 0 0 0 4px var(--ink)}
.la-er .la-dot{background:var(--hi)}
.la-icu .la-dot{background:var(--ink)}
.la-home .la-dot{background:var(--ink);box-shadow:none}
.la-home .la-dot::after{content:"";position:absolute;left:6px;top:3px;width:5px;height:9px;border-right:2.5px solid var(--card);border-bottom:2.5px solid var(--card);transform:rotate(40deg)}
.la-home{padding-bottom:0}
.la-sh{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.la-sh b{font:400 22px/1 var(--f-d)}
.la-sh span{font-size:12.5px;color:var(--mut);line-height:1.35}
.la-sh .la-nums{margin-left:auto;color:var(--mut)}
.la-sh .la-nums b{font:600 13px/1.35 var(--f-b);color:var(--ink)}
.la-bar{position:relative;height:8px;background:var(--soft);box-shadow:inset 0 0 0 1px var(--line)}
.la-bar i{position:absolute;left:0;top:0;bottom:0;background:var(--ink)}
.la-bar em{position:absolute;top:-4px;bottom:-4px;width:3px;margin-left:-1px;background:var(--hi)}
.la-nums{font-size:12.5px;white-space:nowrap}
.la-nums b{color:var(--ink);font-weight:600}
.la-x{font-size:12.5px;font-weight:600;line-height:1.35}
.la-path .v-atot span{line-height:1.3}
.la-path .v-atot small{font-size:12px;font-weight:500;color:var(--mut)}
.la-path.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey);color:var(--mut)}
.la-path.is-empty p{font-size:14px}
.lw-tray{display:flex;flex-direction:column;gap:8px;background:var(--soft);padding:10px;box-shadow:inset 0 0 0 1px var(--line)}
.lw-band{position:relative;display:grid;grid-template-columns:34px minmax(0,1.25fr) minmax(0,1fr) 150px 54px;align-items:center;gap:0 16px;width:100%;min-height:72px;
 border:0;padding:0 40px 0 0;text-align:left;color:var(--ink);background:var(--card);box-shadow:inset 0 0 0 2px var(--ink)}
.lw-band[data-s=now]{background:linear-gradient(90deg,var(--hi) 0 34px,var(--card) 34px)}
.lw-band[data-s=started]{background:linear-gradient(90deg,var(--ink) 0 34px,var(--card) 34px)}
.lw-snap{align-self:stretch;position:relative;border-right:2px solid var(--ink)}
.lw-snap::after{content:"";position:absolute;left:8px;top:50%;width:14px;height:14px;margin-top:-7px;border-radius:50%;background:var(--card);box-shadow:inset 0 0 0 2px var(--ink)}
.lw-lab{display:flex;flex-direction:column;gap:2px;padding:8px 0;min-width:0}
.lw-k{font-size:11px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.lw-n{display:inline-flex;align-items:center;gap:8px;font:400 26px/1 var(--f-d)}
.lw-n svg{color:var(--mut);flex-shrink:0}
.lw-s{font-size:13px;line-height:1.4}
.lw-days{display:flex;gap:4px;flex-wrap:wrap}
.lw-d{display:inline-flex;flex-direction:column;align-items:center;justify-content:center;width:34px;height:38px;font:400 18px/1 var(--f-d);box-shadow:inset 0 0 0 1.5px var(--ink);background:var(--card)}
.lw-d small{font:600 8.5px/1 var(--f-b);letter-spacing:.08em;text-transform:uppercase;margin-bottom:2px}
.lw-d.s-done{background:var(--ink);color:var(--card)}
.lw-d.s-now{background:var(--hi);color:var(--ink);box-shadow:inset 0 0 0 2px var(--ink)}
.lw-d.s-later{color:var(--ink)}
.lw-d.s-none{color:var(--mut);box-shadow:inset 0 0 0 1.5px var(--grey);background-image:repeating-linear-gradient(135deg,transparent 0 5px,rgba(0,0,0,.07) 5px 6px)}
.lw-none{font-size:12.5px;color:var(--mut)}
.lw-meta{display:flex;flex-direction:column;align-items:flex-start;gap:5px}
.lw-p{font-size:12px;font-weight:600;color:var(--mut)}
.lw-code{align-self:stretch;margin:12px 0;background:repeating-linear-gradient(90deg,var(--ink) 0 2px,transparent 2px 4px,var(--ink) 4px 7px,transparent 7px 9px,var(--ink) 9px 10px,transparent 10px 13px)}
.lw-band .sel-chev{position:absolute;right:12px;top:50%;margin:-8px 0 0}
.lp .lw-band.is-up{background-color:var(--card)}
.lw-band[data-s=none] .lw-n,.lw-band[data-s=none] .lw-s,.lw-band.is-empty .lw-n,.lw-band.is-empty .lw-s{color:var(--mut)}
.lw-band[data-s=none],.lw-band.is-empty{box-shadow:inset 0 0 0 1.5px var(--grey)}
.lw-band[data-s=none] .lw-snap,.lw-band.is-empty .lw-snap{border-color:var(--grey)}
.lw-band[data-s=none] .lw-code,.lw-band.is-empty .lw-code{opacity:.3}
.lw-tray.is-empty{background:transparent;box-shadow:inset 0 0 0 2px var(--grey)}
.lw-key{margin-top:12px}
.lw-key .lw-d{width:16px;height:16px}
.la-desk{margin-top:14px}
.la-desk .vx-steps li{padding:3px 0}
@container lp (max-width:699px){
 .lw-tray{padding:10px}
 .lw-band{grid-template-columns:26px minmax(0,1fr);grid-template-areas:"snap lab" "snap days" "snap meta";gap:6px 12px;padding:0 40px 12px 0}
 .lw-band[data-s=now]{background:linear-gradient(90deg,var(--hi) 0 26px,var(--card) 26px)}
 .lw-band[data-s=started]{background:linear-gradient(90deg,var(--ink) 0 26px,var(--card) 26px)}
 .lw-snap{grid-area:snap}.lw-snap::after{left:4px}
 .lw-lab{grid-area:lab;padding-bottom:0}.lw-days{grid-area:days}.lw-meta{grid-area:meta;flex-direction:row;flex-wrap:wrap;align-items:center;gap:6px 10px}
 .lw-code{display:none}
 .lw-band .sel-chev{right:12px;top:22px;margin:0}
 .la-sh .la-nums{margin-left:0;width:100%}
 .la-top{grid-template-columns:1fr}
 .lw-tray .bx-mob{margin:-4px 0 4px}
}
'''

# ==========================================================================================
# B · THE BED BOARD
CENSUS = [  # area, beds, in use, ready to go home but still here, waiting (Emergency only)
 ('Emergency', 20, 6, 0, 14, 'beds and trolleys'),
 ('ICU', 20, 15, 4, 0, 'beds'),
 ('Step-down', 30, 22, 6, 0, 'beds'),
 ('Wards', 180, 138, 33, 0, 'beds'),
]
def census_panel(s):
    if not s:
        return '<aside class="lb-cen is-empty"><b class="v-ach">Today’s beds</b><p>Draws every bed once the bed list is in.</p></aside>'
    blocks = []
    for name, n, use, ready, wait, what in CENSUS:
        free = n - use - ready - wait
        cells = ['w'] * wait + ['u'] * use + ['r'] * ready + ['f'] * free
        note = ('%d waiting for a bed' % wait) if wait else ('%d ready to go home' % ready)
        blocks.append('<div class="lb-area"><div class="lb-ah"><b>%s</b><span>%d %s · %s</span></div><div class="lb-grid" aria-hidden="true">%s</div></div>' % (
            e(name), n, e(what), e(note), ''.join('<i class="c-%s"></i>' % c for c in cells)))
    return ('<aside class="lb-cen"%s role="img" aria-label="Today’s 250 beds by area. 43 are held by patients ready to go home; 14 Emergency patients are waiting for a bed.">'
            '<div class="v-ah"><b class="v-ach">Today’s beds, area by area</b>%s</div>%s'
            '<div class="lb-legend"><span><i class="c-u"></i>In use</span><span><i class="c-r"></i>Ready to go home, still here</span><span><i class="c-w"></i>Waiting in Emergency</span><span><i class="c-f"></i>Free</span></div>'
            '<div class="lb-tot"><div><span>Average stay</span><b>4.6 days</b></div><div><span>Goal</span><b>3.9 days</b></div><div><span>Extra days cost</span><b>₹2.1 crore</b></div></div></aside>') % (
        pt(1), tag('example'), ''.join(blocks))

def b_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    top = '<div class="v-top lb-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), census_panel(d['stay']))
    rows, desk = [], []
    for i, p in enumerate(d['places']):
        d_, n = counts(p)
        ticks = L2.segs(p, 'lb-t')
        inner = ('<span class="lb-bed"><small>Bed</small>%02d</span><span class="lb-who"><b>%s%s</b><span>%s</span></span>'
                 '<span class="lb-day"><span class="lb-dl">%s</span><span class="lb-ts" aria-hidden="true">%s</span></span>'
                 '<span class="lb-plan"><span class="v-st s-%s">%s</span><span>%s</span></span>') % (
            i + 1, ico(ICONS[p['name']], 'currentColor', 18), e(p['name']), e(p['head']), e(('Day %d of %d' % (d_, n)) if n else 'No days yet'), ticks,
            p['status'], e(STATUS[p['status']]), e(p['short']))
        pick('lb-row', 'lb', i, p, inner, empty, rows, desk)
    head = '<div class="lb-hd" aria-hidden="true"><span>Bed</span><span>Part of the work</span><span>Day of stay</span><span>Plan</span></div>'
    body = '<div class="lb-board%s"><div class="lb-bt">Bed board · %s</div>%s%s</div>' % (' is-empty' if empty else '', e(C.TOOL), head, ''.join(rows))
    key = L2.key_html('lb-key').replace('class="sg ', 'class="lb-t ') if not empty else ''
    sub = 'One bed per part of the work, its day of stay as steps done. Tap a bed.' if not empty else 'One bed for each part of the work'
    return page(state, top, body + key + ('<div class="lb-desk">%s</div>' % ''.join(desk) if desk else ''), 'lb', sub)

B_CSS = r'''
.lb-top{grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:32px}
.lb-cen{background:var(--card);border-top:6px solid var(--ink);padding:16px 18px;display:flex;flex-direction:column;gap:9px}
.lb-area{display:flex;flex-direction:column;gap:5px}
.lb-ah{display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}
.lb-ah b{font:400 20px/1 var(--f-d)}
.lb-ah span{font-size:12px;color:var(--mut);font-weight:600}
.lb-grid{display:grid;grid-template-columns:repeat(30,minmax(0,1fr));gap:3px}
.lb-grid i{display:block;aspect-ratio:1;min-width:0}
.c-u{background:var(--ink)}
.c-r{background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.c-w{background:repeating-linear-gradient(135deg,var(--hi) 0 2px,var(--card) 2px 4px);box-shadow:inset 0 0 0 1.5px var(--ink)}
.c-f{background:var(--card);box-shadow:inset 0 0 0 1px var(--grey)}
.lb-legend{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:11.5px;color:var(--mut)}
.lb-legend span{display:inline-flex;align-items:center;gap:6px}
.lb-legend i{display:inline-block;width:12px;height:12px}
.lb-tot{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;border-top:3px double var(--ink);padding-top:8px}
.lb-tot div{display:flex;flex-direction:column;gap:2px;min-width:0}
.lb-tot span{font-size:11.5px;font-weight:600;color:var(--mut)}
.lb-tot b{font:400 24px/1 var(--f-d);white-space:nowrap}
.lb-tot div:last-child b{background:linear-gradient(transparent 50%,var(--hi) 50% 92%,transparent 92%);align-self:flex-start;padding:0 3px}
.lb-cen.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey);color:var(--mut)}
.lb-cen.is-empty p{font-size:14px}
.lb-board{background:var(--card);padding:0 0 6px;box-shadow:inset 0 0 0 3px var(--ink),0 0 0 6px var(--soft),0 0 0 7px var(--line)}
.lb-bt{background:var(--ink);color:var(--card);font:400 22px/1 var(--f-d);letter-spacing:.04em;padding:10px 16px}
.lb-hd{display:grid;grid-template-columns:64px minmax(0,1.6fr) 170px 190px;gap:14px;padding:8px 16px 6px;font-size:11.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut);border-bottom:2px solid var(--ink)}
.lb-row{position:relative;display:grid;grid-template-columns:64px minmax(0,1.6fr) 170px 190px;gap:14px;align-items:center;width:100%;border:0;border-bottom:1px solid var(--line);
 padding:8px 40px 8px 16px;background:transparent;text-align:left;color:var(--ink)}
.lp .lb-row.is-up{background:var(--hi-soft)}
.lb-bed{display:flex;flex-direction:column;align-items:center;justify-content:center;width:50px;height:48px;background:var(--ink);color:var(--card);font:400 26px/1 var(--f-d)}
.lb-bed small{font:600 9px/1 var(--f-b);letter-spacing:.1em;text-transform:uppercase;margin-bottom:2px}
.lb-row[data-s=none] .lb-bed,.lb-row.is-empty .lb-bed{background:transparent;color:var(--mut);box-shadow:inset 0 0 0 1.5px var(--grey)}
.lb-who{display:flex;flex-direction:column;gap:3px;min-width:0}
.lb-who b{display:inline-flex;align-items:center;gap:8px;font:400 24px/1 var(--f-d)}
.lb-who b svg{color:var(--mut);flex-shrink:0}
.lb-who span{font-size:13px;line-height:1.4}
.lb-day{display:flex;flex-direction:column;gap:6px}
.lb-dl{font-size:13px;font-weight:600}
.lb-ts{display:flex;gap:3px;height:14px}
.lb-t{display:block;flex:1;height:100%}
.lb-t.s-done{background:var(--ink)}.lb-t.s-now{background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.lb-t.s-later{background:var(--soft);box-shadow:inset 0 0 0 1px var(--grey)}
.lb-t.s-none,.lb-t.s-empty{box-shadow:inset 0 0 0 1.5px var(--grey);background-image:repeating-linear-gradient(135deg,transparent 0 5px,rgba(0,0,0,.08) 5px 6px)}
.lb-plan{display:flex;flex-direction:column;align-items:flex-start;gap:5px;font-size:12.5px;line-height:1.35;color:var(--mut)}
.lb-row[data-s=none] .lb-who,.lb-row.is-empty .lb-who{color:var(--mut)}
.lb-row .sel-chev{position:absolute;right:14px;top:50%;margin:-8px 0 0}
.lb-board.is-empty{box-shadow:inset 0 0 0 2px var(--grey)}
.lb-board.is-empty .lb-bt{background:var(--soft);color:var(--mut)}
.lb-key{margin-top:16px}
.lb-key .lb-t{width:18px;height:10px;flex:none}
.lb-desk{margin-top:14px}
@container lp (max-width:699px){
 .lb-top{grid-template-columns:1fr}
 .lb-hd{display:none}
 .lb-row{grid-template-columns:52px minmax(0,1fr);grid-template-areas:"bed who" "day day" "plan plan";gap:8px 12px;padding:12px 40px 12px 12px}
 .lb-bed{grid-area:bed}.lb-who{grid-area:who}.lb-day{grid-area:day}.lb-plan{grid-area:plan;flex-direction:row;flex-wrap:wrap;align-items:center;gap:6px 10px}
 .lb-row .sel-chev{top:22px;margin:0}
 .lb-board .bx-mob{margin:0 8px 8px}
 .lb-tot b{font-size:20px}
 .lb-grid{grid-template-columns:repeat(20,minmax(0,1fr))}
}
'''

# ==========================================================================================
# C · THE STAY CHART
def chart_panel(s):
    if not s:
        return '<aside class="lc-ch is-empty"><b class="v-ach">One average stay, area by area</b><p>Draws the days, needed and extra, once three months of times are in.</p></aside>'
    span = 5.0
    ticks = ''.join('<span style="left:%.1f%%">%d</span>' % (x / span * 100, x) for x in range(0, 6))
    rows = []
    for a in s['areas'][1:]:
        rows.append('<div class="lc-r"><span class="lc-l"><b>%s</b><small>%s · goal %s</small></span><span class="lc-t"><i class="lc-need" style="width:%.1f%%"></i>'
                    '<i class="lc-extra" style="width:%.1f%%"></i></span><b class="lc-x">+%.1f</b></div>' % (
            e(a['name']), e(a['nowt']), e(a['goalt']), a['goal'] / span * 100, (a['now'] - a['goal']) / span * 100, a['now'] - a['goal']))
    er = s['areas'][0]
    return ('<aside class="lc-ch"%s role="img" aria-label="Days in each area, needed and extra: ICU 4.8 against 3.5, step-down 2.9 against 2, wards 4.1 against 3.5. Emergency wait 5 hours 10 minutes against 4 hours.">'
            '<div class="v-ah"><b class="v-ach">One average stay, area by area</b>%s</div>'
            '<div class="lc-axis" aria-hidden="true"><span class="lc-l">Days</span><span class="lc-ticks">%s</span><span></span></div>%s'
            '<div class="lc-er"><b>Emergency</b><span>Wait for a bed: <b>%s</b>, goal %s. %s.</span></div>'
            '<div class="lc-leg"><span><i class="lc-need"></i>Needed</span><span><i class="lc-extra"></i>Extra</span></div>'
            '<div class="v-atot"><span>%s<br><small>%s · %s</small></span><b>%s</b></div></aside>') % (
        pt(1), tag('example'), ticks, ''.join(rows), e(er['nowt']), e(er['goalt']), e(er['extra']), e(s['avg'][0]), e(s['goal']), e(s['cost'][1]), e(s['avg'][1]))

def trace(p):
    """A stepped trace: climbs one step for each step done, a dot where the work is now."""
    n = len(p['steps'])
    if not n:
        return ''
    w, h, x0 = 160, 56, 4
    dx = (w - 2 * x0) / n
    pts, y, now = [(x0, h - 6)], h - 6, None
    for j, (_, s) in enumerate(p['steps']):
        x = x0 + j * dx
        if s == 'done':
            y -= (h - 14) / n
            pts += [(x, pts[-1][1]), (x, y)]
        if s == 'now' and now is None:
            now = (x + dx / 2, y)
    pts.append((w - x0 if now is None else now[0], y))
    path = 'M' + ' L'.join('%.1f %.1f' % q for q in pts)
    dot = ('<circle cx="%.1f" cy="%.1f" r="5" class="lm-dot"/>' % now) if now else ''
    grid = ''.join('<line x1="%.1f" x2="%.1f" y1="4" y2="%d" class="lm-g"/>' % (x0 + j * dx, x0 + j * dx, h - 4) for j in range(1, n))
    return '<svg class="lm-svg" viewBox="0 0 %d %d" aria-hidden="true">%s<path d="%s" class="lm-tr"/>%s</svg>' % (w, h, grid, path, dot)

def c_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    top = '<div class="v-top lc-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), chart_panel(d['stay']))
    rows, desk = [], []
    for i, p in enumerate(d['places']):
        d_, n = counts(p)
        live = p['status'] in ('now', 'started')
        screen = ('<span class="lm-top"><span class="lm-n">%s</span><span class="lm-led" aria-hidden="true"></span></span>'
                  '<span class="lm-read"><b>%s</b><span>%s</span></span>%s') % (
            e(p['name']), ('%d/%d' % (d_, n)) if n else '—', e(p['unit'].upper() if n else 'NO STEPS YET'), trace(p) if live else '<span class="lm-off">%s</span>' % e('Waits for a fix' if p['status'] == 'none' else 'Fills in later'))
        inner = ('<span class="lm-scr">%s</span><span class="lm-foot"><span class="v-st s-%s">%s</span><span class="lm-hl">%s</span></span>') % (
            screen, p['status'], e(STATUS[p['status']]), e(p['short']))
        pick('lm-mon', 'lm', i, p, inner, empty, rows, desk)
    body = '<div class="lm-rack%s">%s</div>' % (' is-empty' if empty else '', ''.join(rows))
    key = ('<div class="v-key lm-key" aria-hidden="true"><span><i class="lm-k1"></i>The trace climbs one step for each step done</span><span><i class="lm-k2"></i>Where the work is now</span>'
           '<span><i class="lm-k3"></i>Screen off: not started</span></div>') if not empty else ''
    sub = 'One bedside monitor for each part of the work. Tap a monitor.' if not empty else 'One bedside monitor for each part of the work'
    return page(state, top, body + key + ('<div class="lc-desk">%s</div>' % ''.join(desk) if desk else ''), 'lc', sub)

C_CSS = r'''
.lc-top{grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:32px}
.lc-ch{background:var(--card);border-top:6px solid var(--ink);padding:16px 18px;display:flex;flex-direction:column;gap:8px}
.lc-axis,.lc-r{display:grid;grid-template-columns:150px minmax(0,1fr) 40px;gap:10px;align-items:center}
.lc-ticks{position:relative;height:16px;border-bottom:1.5px solid var(--ink)}
.lc-ticks span{position:absolute;top:0;transform:translateX(-50%);font-size:11.5px;font-weight:600;color:var(--mut)}
.lc-ticks span:first-child{transform:none}.lc-ticks span:last-child{transform:translateX(-100%)}
.lc-axis .lc-l{font-size:11.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.lc-l{display:flex;flex-direction:column;gap:1px;min-width:0}
.lc-l b{font:400 20px/1 var(--f-d)}
.lc-l small{font-size:11.5px;color:var(--mut);line-height:1.3}
.lc-t{display:flex;height:22px;background:repeating-linear-gradient(90deg,var(--line) 0 1px,transparent 1px 20%)}
.lc-need{display:block;background:var(--ink)}
.lc-extra{display:block;background:repeating-linear-gradient(135deg,var(--hi) 0 4px,var(--hi-dark) 4px 6px);box-shadow:inset 0 0 0 2px var(--ink)}
.lc-x{font:400 22px/1 var(--f-d);text-align:right}
.lc-er{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:8px;font-size:13px;line-height:1.45}
.lc-er>b{font:400 20px/1 var(--f-d)}
.lc-er span b{font-weight:600}
.lc-leg{display:flex;gap:16px;font-size:12px;color:var(--mut)}
.lc-leg span{display:inline-flex;align-items:center;gap:6px}
.lc-leg i{display:inline-block;width:18px;height:10px}
.lc-ch .v-atot span{line-height:1.3}
.lc-ch .v-atot small{font-size:12px;font-weight:500;color:var(--mut)}
.lc-ch.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey);color:var(--mut)}
.lc-ch.is-empty p{font-size:14px}
.lm-rack{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;align-items:start;padding:14px;background:var(--soft);box-shadow:inset 0 -6px 0 var(--ink)}
.lm-mon{position:relative;display:flex;flex-direction:column;gap:0;width:100%;border:0;padding:8px 8px 0;background:var(--card);box-shadow:inset 0 0 0 2px var(--ink);text-align:left;color:var(--ink);min-width:0}
.lm-scr{display:flex;flex-direction:column;gap:6px;background:var(--panel);color:#fff;padding:10px 12px 10px;min-height:150px}
.lm-top{display:flex;justify-content:space-between;align-items:center;gap:8px;padding-right:22px}
.lm-n{font:400 22px/1 var(--f-d);letter-spacing:.03em}
.lm-led{width:9px;height:9px;border-radius:50%;background:var(--hi-dark);flex-shrink:0}
.lm-read{display:flex;align-items:baseline;gap:8px}
.lm-read b{font:400 40px/1 var(--f-d);color:var(--hi-dark)}
.lm-read span{font-size:11px;font-weight:600;letter-spacing:.09em;color:#fff}
.lm-svg{display:block;width:100%;height:auto;margin-top:auto}
.lm-g{stroke:rgba(255,255,255,.22);stroke-width:1;stroke-dasharray:2 3}
.lm-tr{fill:none;stroke:var(--hi-dark);stroke-width:2.5;stroke-linejoin:round}
.lm-dot{fill:var(--hi);stroke:#fff;stroke-width:2}
.lm-off{margin-top:auto;font-size:12.5px;font-weight:600;color:#fff;border-top:1px dashed rgba(255,255,255,.4);padding-top:8px}
.lm-mon[data-s=none] .lm-scr,.lm-mon.is-empty .lm-scr{background:var(--soft);color:var(--mut)}
.lm-mon[data-s=none] .lm-read b,.lm-mon.is-empty .lm-read b,.lm-mon[data-s=none] .lm-read span,.lm-mon.is-empty .lm-read span,.lm-mon[data-s=none] .lm-off,.lm-mon.is-empty .lm-off{color:var(--mut)}
.lm-mon[data-s=none] .lm-off,.lm-mon.is-empty .lm-off{border-top-color:var(--grey)}
.lm-mon[data-s=none] .lm-led,.lm-mon.is-empty .lm-led{background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey)}
.lm-foot{display:flex;flex-direction:column;align-items:flex-start;gap:6px;padding:10px 4px 12px}
.lm-hl{font-size:13px;line-height:1.4}
.lm-mon .sel-chev{position:absolute;right:16px;top:17px;margin:0;color:#fff}
.lm-mon[data-s=none] .sel-chev{color:var(--mut)}
.lm-rack.is-empty{background:transparent;box-shadow:inset 0 0 0 2px var(--grey)}
.lm-mon.is-empty{box-shadow:inset 0 0 0 1.5px var(--grey)}
.lm-key{margin-top:14px}
.lm-key i{display:inline-block;width:18px;height:10px}
.lm-k1{border-left:2.5px solid var(--ink);border-top:2.5px solid var(--ink);height:10px}
.lm-k2{width:10px!important;border-radius:50%;background:var(--hi);box-shadow:inset 0 0 0 1.5px var(--ink)}
.lm-k3{background:var(--soft);box-shadow:inset 0 0 0 1px var(--grey)}
.lc-desk{margin-top:16px}
@container lp (max-width:699px){
 .lc-top{grid-template-columns:1fr}
 .lc-axis,.lc-r{grid-template-columns:100px minmax(0,1fr) 34px;gap:8px}
 .lm-rack{grid-template-columns:1fr;padding:10px}
 .lm-scr{min-height:0}
 .lm-svg{max-width:220px}
 .lm-rack .bx-mob{margin:-6px 0 4px}
}
'''

# ==========================================================================================
T = C.theme
THEMES = {
 # A: aqua, petrol ink, coral red (the emergency colour)
 'a': T('#DFEFEE', '#FFFFFF', '#0B2F3A', '#3D5A62', '#BBD6D5', '#EDF6F5', '#8EA9AC', '#FF6F61', '#FF8A80', '#B3261E',
        ['#D6E9E8', '#E6F2F1', '#FBE3DF', '#E1ECEE', '#EEF0E4'], '#0B2F3A'),
 # B: whiteboard, indigo ink, marker cyan
 'b': T('#EFEDE6', '#FFFFFF', '#1C1E4F', '#4B4D72', '#D6D3C6', '#F6F5F0', '#A09FAE', '#39C6EC', '#6FD6F2', '#0A6683',
        ['#E7E4DA', '#F2F0EA', '#DDF2F8', '#E8E8F0', '#F1EDE0'], '#1C1E4F'),
 # C: pale butter, ox-blood ink, monitor yellow
 'c': T('#F4EFD9', '#FFFFFF', '#3A1016', '#664A4D', '#DDD4B6', '#FAF7EA', '#AFA393', '#FFD43B', '#FFDF6E', '#7A5A00',
        ['#EEE7CB', '#F7F3E2', '#FFF0B8', '#F1E6E2', '#ECE9DC'], '#3A1016'),
}
PAGES = {
 'a': (a_canvas, A_CSS, 'A', 'The patient’s path'),
 'b': (b_canvas, B_CSS, 'B', 'The bed board'),
 'c': (c_canvas, C_CSS, 'C', 'The stay chart'),
}
NOTE = ('<em>All three: the Financial look approved for Supply Chain and Procurement (Virevo type unchanged, flat frame, ledger and report paper) '
        'in colours no other tool uses. Every figure is made up for an example 250-bed hospital and marked Example only or Tojo’s guess.</em>')
ABOUT = {
 'a': ('<b>A · The patient’s path.</b> The stay drawn as a route through the hospital: Emergency, ICU, step-down, wards, home. Each stop shows its days now against the goal, '
       'the extra days a month and what they cost; a double-ruled total for the whole hospital. Each part of the work is a patient wristband with one day box per step. '
       'Colours: aqua, petrol ink, coral red.' + NOTE),
 'b': ('<b>B · The bed board.</b> Today’s 250 beds as a grid, area by area: in use, held by patients ready to go home, Emergency patients waiting, free. '
       'Each part of the work is a bed on the ward’s bed board: its day of stay as steps done, and its plan. Colours: whiteboard, indigo ink, marker cyan.' + NOTE),
 'c': ('<b>C · The stay chart.</b> One average stay as a chart of days, area by area, needed in ink and extra in the highlight, with the Emergency wait beneath. '
       'Each part of the work is a bedside monitor: its reading is the steps done, its trace climbs one step for each, a dot where the work is now; '
       'parts not started have their screen off. Colours: pale butter, ox-blood ink, monitor yellow.' + NOTE),
}

def build():
    os.makedirs(OUT, exist_ok=True)
    pages, words = {}, []
    base = L2.V_SHARED_CSS + L3.PLACE_CSS
    for k, (fn, css, letter, label) in PAGES.items():
        t = THEMES[k]
        for st in ('filled', 'empty'):
            canvas = fn(st)
            for v in ('desktop', 'mobile'):
                h = C.page(SK, t, None, canvas, base + css, DATA[st]['chat'], v, 'Length of Stay · %s' % label, 'ls ls-home ls-%s' % k)
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(OUT, 'los-home-%s.%s.%s.html' % (k, v, st)), 'w', encoding='utf-8').write(h)
            text = re.sub(r'<[^>]+>', ' ', canvas) + ' ' + json.dumps(DATA[st]['chat'], ensure_ascii=False)
            words += [(k, st, w) for w in C.plain_check(text)]
    return pages, words

def review(pages):
    tpl = open(os.path.join(SCP, 'review_template.html'), encoding='utf-8').read()
    for old in ('Supply Chain and Procurement · three looks for the Financial domain', 'Supply Chain and Procurement · the home page in three looks'):
        tpl = tpl.replace(old, 'Length of Stay · the home page in three looks')
    tpl = re.sub(r'<p class="rv-intro">.*?</p>', '<p class="rv-intro">The third Financial tool: every kind of stay, from the wait in Emergency to days in the ICU, '
                 'step-down and the wards. All three looks keep the Financial identity approved for Supply Chain and Procurement (the Virevo type unchanged, the flat frame, '
                 'ledger and report paper) and the same five zones, and each brings its own drawing of a hospital stay in colours no other tool uses. '
                 'Pick a look below. Scroll inside each view; every page opens with its first part raised and its box open. On the phone, each box opens right under the part you tap.</p>', tpl, flags=re.S)
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>Sample %s</b><span>%s</span><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 4px %s"></i></button>' % (
        k, 'true' if k == 'a' else 'false', v[2], e(v[3]), THEMES[k]['ground'], THEMES[k]['ink'], THEMES[k]['hi']) for k, v in PAGES.items())
    return (tpl.replace('@@PICKS@@', picks).replace('@@ABOUT@@', json.dumps(ABOUT, ensure_ascii=False))
               .replace('@@DATA@@', json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')))

if __name__ == '__main__':
    pages, words = build()
    if words:
        print('PLAIN ENGLISH:', words)
    rv = os.path.join(OUT, 'length-of-stay-home-samples.html')
    open(rv, 'w', encoding='utf-8').write(review(pages))
    print('built', rv, os.path.getsize(rv))
