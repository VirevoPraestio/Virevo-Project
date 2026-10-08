"""
Revenue & EBITDA: the tool's home page in three looks (8 Oct 2026, for review).

The second Financial tool. It uses the Financial identity approved for Supply Chain and Procurement
(the V skin: Virevo type unchanged, flat frame, the three papers of money) and changes only its
colours, which no other tool uses. There is no reference file yet; every figure is made up for an
example 250-bed hospital and marked Example only or Tojo's guess.

Same five zones as every landing page, in the same order (06 §11.2): masthead with stamp and
Refresh now, where this stands, the drawing, what Tojo still has to do, the three buttons.
Same behaviour: first element raised with its box open, on a phone each box under its element,
pickable items stacked, the chat one screen tall.

  A  The cheque book      the month's profit and loss on ledger paper; each part of the work a
                          cheque made out for what it should bring back, with a counterfoil of steps.
  B  The results board    twelve months of what is left from every 100 rupees, against the goal;
                          each part of the work a results card with a ring of steps done.
  C  The coin stacks      the month's money as a bridge from money in to what is left; each part of
                          the work a stack of coins, one coin per step.

Run:  python3 landing.py   ->  out/landing/
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
SCP = os.path.join(TOOLS, 'Supply Chain Procurement')       # the Financial look lives with the first Financial tool
sys.path[:0] = [HERE, SCP]
import sc_common as C
C.TOOL = 'Revenue & EBITDA'
C.HOSPITAL = 'Example hospital · 250 beds'
C.B.TOOL = C.TOOL
C.B.HOSPITAL[:] = [C.HOSPITAL]
from sc_common import e, ico, ICONS, CHEV, sel, sel_cls, box, pt, tag, say_btn, standing, section, pending, actions, STAMP
from skins import SKINS
import landing2 as L2          # Financial shared parts: segments, receipt, account, boxes
import landing3 as L3          # place-page shared parts (fx-*)

SK = SKINS['f']
OUT = os.path.join(HERE, 'out', 'landing')
KICK = 'Virevo · ' + C.HOSPITAL
# The tool's mark: a coin with an arrow rising out of it.
MARK = '<circle cx="9" cy="14" r="6"/><path d="M9 11v6"/><path d="M7 12.5h3"/><path d="M15 9l5-5"/><path d="M15.5 4H20v4.5"/>'

STEP = {'done': 'Done', 'now': 'Now', 'later': 'Still to do', 'none': 'Not started'}
STATUS = {'now': 'In use now', 'started': 'Taking shape', 'none': 'Not started', 'empty': 'Nothing yet'}

# ==========================================================================================
# The words (one set for all three looks)
MONEY = {
 'in': ('Money in', '₹18 crore'),
 'costs': [('Staff', '₹7.6 crore', 7.6), ('Medicines and supplies', '₹4.9 crore', 4.9), ('Doctors’ fees', '₹2.2 crore', 2.2), ('Rent, power and upkeep', '₹1 crore', 1.0)],
 'left': ('Left from running the hospital', '₹2.3 crore'),
 'share': 'About 13 of every 100 rupees', 'goal': 'Goal: 18 of every 100 rupees', 'gap': 'About ₹90 lakh a month short of the goal',
 'trend': [15.1, 14.6, 14.0, 14.4, 13.8, 13.1, 13.5, 12.9, 12.4, 13.0, 12.6, 12.8],
 'months': ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
}
DATA = {
 'filled': {
  'claim': 'We earn enough. We keep too little of it.',
  'deck': 'EBITDA is what is left from running the hospital, before loans, tax and wear on equipment. Ours is about 13 of every 100 rupees; the goal is 18. Diagnosis is two steps in. Nothing is changed yet.',
  'money': MONEY,
  'places': [
   {'name': 'Diagnosis', 'status': 'now', 'pt': 1, 'head': 'About ₹90 lakh a month short of the goal. Most of it is money earned but not collected.',
    'fig': ('About ₹90 lakh', 'a month short of the goal', 'example'), 'unit': 'steps done', 'pay': 'Finds where the ₹90 lakh goes', 'amt': '₹90 lakh',
    'steps': [['Put a number on the gap to the goal', 'done'], ['Split money in by department and by who pays', 'done'],
              ['Check the insurance claims turned down', 'now'], ['Check package prices against their cost', 'later'], ['Name the main cause', 'later']]},
   {'name': 'Solutions', 'status': 'started', 'pt': 3, 'head': 'Three fixes on the table. One is taking shape.',
    'fig': ('About ₹55 lakh', 'a month could come back', 'guess'), 'unit': 'fixes agreed', 'pay': 'Brings back about ₹55 lakh a month', 'amt': '₹55 lakh',
    'steps': [['Bill every patient on the day they go home', 'now'], ['Reprice the 20 packages that lose money', 'later'],
              ['Fill the quiet days with planned surgery', 'later']]},
   {'name': 'Automations', 'status': 'none', 'head': 'Three helpers wait for the fixes to be agreed.', 'fig': None, 'unit': 'switched on',
    'pay': 'Keeps the money from slipping again', 'amt': '—',
    'steps': [['Checks each claim before it goes to the insurer', 'none'], ['Sends yesterday’s money note at 8 AM', 'none'],
              ['Warns when a package costs more than its price', 'none']]},
   {'name': 'Processes', 'status': 'none', 'head': 'Three changes and one new role wait for a trial.', 'fig': None, 'unit': 'tried',
    'pay': 'Makes the fixes a habit', 'amt': '—',
    'steps': [['A ten-minute look at the money each morning', 'none'], ['The insurance desk owns every turned-down claim', 'none'],
              ['A price review every month', 'none'], ['A Revenue Lead who owns the gap', 'none']]},
  ],
  'pending': [
   {'text': 'Get the list of insurance claims turned down in the last three months.', 'need': 'Needs the insurance desk’s records', 'pt': 2},
   {'text': 'Find what each of the top 20 packages really costs.', 'pt': 4},
   {'text': 'Check how many days a bill waits after the patient goes home.'},
   {'text': 'Split money in by doctor and by department.', 'need': 'Needs last quarter’s bills'},
  ],
  'actions': {'go': {'detail': 'Check the insurance claims turned down', 'say': 'Let’s check the insurance claims turned down'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about our money: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Pick up where you left off', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Here is where the Revenue & EBITDA work stands, across all four parts.',
                    'Diagnosis is two steps in. About 13 of every 100 rupees is left after costs; the goal is 18. Most of the gap is money we earn but do not collect.',
                    'Two things would sharpen this: the claims turned down, and what our top 20 packages really cost.'],
           'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
           'note': 'We earn it. We do not always collect it.',
           'points': [{'n': 1, 'label': 'The gap to the goal'}, {'n': 2, 'label': 'Claims turned down'},
                      {'n': 3, 'label': 'The three fixes'}, {'n': 4, 'label': 'Package prices'}],
           'prompts': ['Let’s check the claims turned down', 'Why is so much money not collected?', 'Show me the three fixes']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Start with Diagnosis. Tojo puts a number on what is left from every 100 rupees, then follows the money from the bill to the bank with you, and fills this page as you go.',
  'money': None,
  'places': [
   {'name': 'Diagnosis', 'status': 'empty', 'head': 'Fills in as you put a number on the gap.', 'fig': None, 'steps': [], 'pay': 'Fills in as we go', 'amt': '—'},
   {'name': 'Solutions', 'status': 'empty', 'head': 'Fills in once the main cause is named.', 'fig': None, 'steps': [], 'pay': 'Fills in later', 'amt': '—'},
   {'name': 'Automations', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': [], 'pay': 'Fills in later', 'amt': '—'},
   {'name': 'Processes', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': [], 'pay': 'Fills in later', 'amt': '—'},
  ],
  'pending': [
   {'text': 'Put a number on what is left from every 100 rupees.', 'need': 'Needs last year’s profit and loss statement'},
   {'text': 'Split money in by department and by who pays.'},
   {'text': 'Find out how long a bill takes to be paid.'},
  ],
  'actions': {'go': {'detail': 'Put a number on the gap with Tojo', 'say': 'Let’s put a number on the gap'},
              'add': {'detail': 'Share a profit and loss statement', 'say': 'Here is what I already know about our money: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Every conversation starts here', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Welcome to Revenue & EBITDA. This page fills in as we talk.',
                    'We start by putting a number on what is left from every 100 rupees the hospital earns.'],
           'note': 'Count what is left. Then find where it goes.', 'points': [],
           'prompts': ['Let’s put a number on the gap', 'What should I bring?', 'What is EBITDA?']},
 },
}

def counts(p):
    return sum(1 for _, s in p['steps'] if s == 'done'), len(p['steps'])

def prog(p):
    d, n = counts(p)
    return '%d of %d %s' % (d, n, p['unit']) if n else 'No steps yet'

def mark(s):
    return '<i class="mk mk-%s"><span class="sr">%s</span></i>' % (s, e(STEP[s]))

def masthead(state):
    emb = '<span class="bm-emb">%s</span>' % ico(MARK, 'var(--hi)', 28)
    return C.masthead(KICK, emb, STAMP[state])

def detail(p):
    """The box for one part of the work (same words in every look)."""
    return L2.place_detail(p, 'vx')

def money_ledger(m):
    """The month's profit and loss, on ledger paper (A)."""
    if not m:
        return '<aside class="v-ac is-empty"><b class="v-ach">The month’s profit and loss</b><p>Fills in once last year’s statement is in.</p></aside>'
    costs = ''.join('<div class="v-al ra-cost"><span>%s</span><b>− %s</b></div>' % (e(a), e(v)) for a, v, _ in m['costs'])
    return ('<aside class="v-ac ra-pl"%s><div class="v-ah"><b class="v-ach">The month’s profit and loss</b>%s</div>'
            '<div class="v-al ra-in"><span>%s</span><b>%s</b></div><div class="v-alines">%s</div>'
            '<div class="v-atot"><span>%s</span><b>%s</b></div><p class="v-sm">%s · %s</p>'
            '<div class="v-asaved"><span>Short of the goal</span><b>About ₹90 lakh a month</b></div></aside>') % (
        pt(1), tag('example'), e(m['in'][0]), e(m['in'][1]), costs, e(m['left'][0]), e(m['left'][1]), e(m['share']), e(m['goal']))

# ==========================================================================================
# A · THE CHEQUE BOOK
def a_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    top = '<div class="v-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), money_ledger(d['money']))
    rows, desk = [], []
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        marks = ''.join(mark(s) for _, s in p['steps'])
        inner = ('<span class="ra-stub"><span class="ra-sno">No. %02d</span><span class="ra-marks">%s</span><span class="ra-sp">%s</span><span class="v-st s-%s">%s</span></span>'
                 '<span class="ra-body"><span class="ra-pay"><span class="ra-k">Pay</span><b class="ra-pn">%s%s</b></span>'
                 '<span class="ra-amt"><span class="ra-k">₹</span><b>%s</b></span>'
                 '<span class="ra-words"><span class="ra-k">For</span><span class="ra-w">%s</span></span>'
                 '<span class="ra-sign"><span class="ra-line">%s</span></span>'
                 '<span class="ra-micr" aria-hidden="true">VIREVO · %s · PART %d OF 4</span></span>%s') % (
            i + 1, marks or '<span class="ra-none">No steps yet</span>', e(prog(p)), p['status'], e(STATUS[p['status']]),
            ico(ICONS[p['name']], 'currentColor', 20), e(p['name']), e(p['amt'].replace('₹', '')), e(p['pay']),
            'Signed when agreed with you' if p['status'] != 'empty' else 'Not written yet',
            e(C.TOOL.upper()), i + 1, '' if empty else CHEV)
        if empty:
            rows.append('<div class="ra-chq is-empty" data-s="empty">%s</div>' % inner); continue
        rows.append('<button class="ra-chq %s" type="button" data-s="%s"%s%s>%s</button>' % (sel_cls(first), p['status'], sel('ra', k, first), pt(p.get('pt')), inner))
        det = detail(p); rows.append(box('ra', k, det, first, 'mob')); desk.append(box('ra', k, det, first, 'desk'))
    book = '<div class="ra-book%s">%s</div>' % (' is-empty' if empty else '', ''.join(rows))
    key = ('<div class="ra-key" aria-hidden="true"><span>%s Done</span><span>%s Now</span><span>%s Still to do</span><span>%s Not started</span></div>' % (
        mark('done'), mark('now'), mark('later'), mark('none'))) if not empty else ''
    sub = 'One cheque per part, made out for what it brings back. Tap a cheque.' if not empty else 'One cheque for each part of the work'
    return (masthead(state) + top + section('Where each part of the work stands', book + key + ('<div class="ra-desk">%s</div>' % ''.join(desk) if desk else ''), 'ra-sec', sub)
            + pending(d['pending']) + actions(d['actions']))

A_CSS = r'''
.ra-pl{background-image:linear-gradient(90deg,transparent 16px,var(--ink) 16px 17px,transparent 17px 20px,var(--ink) 20px 21px,transparent 21px),repeating-linear-gradient(transparent 0 23px,var(--rule) 23px 24px);gap:4px}
.ra-pl .v-al{line-height:24px;grid-template-columns:minmax(0,1fr) 104px}.ra-pl .v-al b{white-space:nowrap}.ra-pl .v-al span,.ra-pl .v-al b{padding-top:2px;padding-bottom:2px}
.ra-pl .ra-in{border-bottom:1px solid var(--ink);font-weight:600}
.ra-pl .ra-in b{border-left:1px solid var(--ink)}
.ra-pl .ra-cost span{color:var(--mut)}
.ra-book{display:flex;flex-direction:column;gap:8px}
.ra-chq{position:relative;display:grid;grid-template-columns:150px minmax(0,1fr);width:100%;border:0;padding:0;text-align:left;color:var(--ink);background:transparent;min-width:0}
.ra-stub{display:flex;flex-direction:column;align-items:flex-start;gap:6px;padding:10px 14px;background:var(--soft);border-right:2px dashed var(--grey);position:relative}
.ra-sno{font:400 20px/1 var(--f-d);color:var(--mut)}
.ra-marks{display:flex;gap:4px;flex-wrap:wrap}
.ra-sp{font-size:12px;font-weight:600;color:var(--mut);line-height:1.35}
.ra-none{font-size:12px;color:var(--mut)}
.ra-body{display:grid;grid-template-columns:minmax(0,1fr) 150px;grid-template-areas:"pay amt" "words words" "sign micr";gap:4px 16px;padding:9px 18px 8px;background:var(--card);
 background-image:repeating-radial-gradient(circle at 100% 0,transparent 0 9px,var(--hi-soft) 9px 10px),linear-gradient(var(--card),var(--card));background-size:100% 100%;border-top:6px solid var(--ink);min-width:0}
.ra-bank{grid-area:bank;display:flex;justify-content:space-between;align-items:center;gap:10px;padding-right:28px;font-size:11.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.ra-pay{grid-area:pay;align-self:end;display:flex;align-items:baseline;gap:10px;border-bottom:1px solid var(--ink);padding:4px 0;min-width:0}
.ra-k{font-size:11.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut);flex-shrink:0}
.ra-pn{display:inline-flex;align-items:center;gap:8px;font:400 26px/1 var(--f-d)}
.ra-pn svg{color:var(--mut);flex-shrink:0}
.ra-words{grid-area:words;display:flex;align-items:baseline;gap:10px;border-bottom:1px dotted var(--grey);padding-bottom:4px;font-size:14px;line-height:1.45;min-width:0}
.ra-amt{grid-area:amt;align-self:end;display:flex;align-items:baseline;gap:6px;padding:4px 10px;box-shadow:inset 0 0 0 2px var(--ink);background:var(--card)}
.ra-amt b{font:400 26px/1 var(--f-d);white-space:nowrap}
.ra-sign{grid-area:sign;display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap}
.ra-line{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);border-top:1.5px dashed var(--ink);padding-top:3px;min-width:180px;margin-top:8px}
.ra-micr{grid-area:micr;align-self:end;justify-self:end;font:400 13px/1 var(--f-d);letter-spacing:.14em;color:var(--mut);white-space:nowrap}
.ra-bank .v-st{letter-spacing:0;text-transform:none}
.ra-chq .sel-chev{position:absolute;right:16px;top:18px;margin:0}
.ra-amt{margin-right:4px}
.lp .ra-chq.is-up .ra-body{background-color:#fff}
.ra-chq[data-s=none] .ra-pn,.ra-chq[data-s=none] .ra-w,.ra-chq.is-empty .ra-pn,.ra-chq.is-empty .ra-w{color:var(--mut)}
.ra-book.is-empty .ra-body{border-top-color:var(--grey);background-image:none;background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey)}
.ra-book.is-empty .ra-stub{background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey)}
.mk{display:inline-block;width:16px;height:16px;position:relative;flex-shrink:0}
.mk-done{background:var(--ink)}
.mk-done::before{content:"";position:absolute;left:5px;top:2px;width:5px;height:9px;border-right:2px solid var(--card);border-bottom:2px solid var(--card);transform:rotate(40deg)}
.mk-now{background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.mk-later{box-shadow:inset 0 0 0 1.5px var(--ink)}
.mk-none{box-shadow:inset 0 0 0 1.5px var(--grey);background-image:repeating-linear-gradient(135deg,transparent 0 4px,rgba(0,0,0,.1) 4px 5px)}
.ra-key{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:12.5px;color:var(--mut);margin-top:10px}
.ra-key span{display:inline-flex;align-items:center;gap:7px}
.ra-desk{margin-top:12px}
.ra-desk .vx-steps li{padding:3px 0}
.ra-desk .vx-box{gap:8px;padding:14px 20px 16px}
@container lp (max-width:699px){
 .ra-chq{grid-template-columns:1fr}
 .ra-stub{flex-direction:row;flex-wrap:wrap;align-items:center;border-right:0;border-bottom:2px dashed var(--grey);padding:10px 44px 10px 12px}
 .ra-body{grid-template-columns:1fr;grid-template-areas:"pay" "words" "amt" "sign";padding:10px 12px 12px}
 .ra-micr{display:none}
 .ra-amt{justify-self:start}
 .ra-chq .sel-chev{top:14px}
 .ra-book .bx-mob{margin:-4px 0 4px}
}
'''

# ==========================================================================================
# B · THE RESULTS BOARD
def trend_svg(m):
    vals, w, h, pl, pr, pt_, pb = m['trend'], 380, 150, 26, 8, 14, 22
    lo, hi = 10.0, 20.0
    X = lambda i: pl + i * (w - pl - pr) / (len(vals) - 1)
    Y = lambda v: pt_ + (hi - v) * (h - pt_ - pb) / (hi - lo)
    grid = ''.join('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="tg"/><text x="%d" y="%.1f" class="tl">%d</text>' % (
        pl, w - pr, Y(v), Y(v), pl - 8, Y(v) + 4, v) for v in (10, 14, 18))
    goal = '<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="tgoal"/><text x="%d" y="%.1f" class="tlg">Goal 18</text>' % (pl, w - pr, Y(18), Y(18), w - pr - 54, Y(18) - 6)
    path = 'M' + ' L'.join('%.1f %.1f' % (X(i), Y(v)) for i, v in enumerate(vals))
    area = path + ' L%.1f %.1f L%.1f %.1f Z' % (X(len(vals) - 1), Y(lo), X(0), Y(lo))
    months = ''.join('<text x="%.1f" y="%d" class="tm">%s</text>' % (X(i), h - 6, mo) for i, mo in enumerate(m['months']) if i % 3 == 0 or i == len(vals) - 1)
    last = '<circle cx="%.1f" cy="%.1f" r="6" class="tdot"/>' % (X(len(vals) - 1), Y(vals[-1]))
    return ('<svg class="rb-svg" viewBox="0 0 %d %d" role="img" aria-label="Left from every 100 rupees, last 12 months: from 15.1 in October down to 12.8 in September. Goal 18.">'
            '%s<path d="%s" class="tarea"/><path d="%s" class="tline"/>%s%s%s</svg>') % (w, h, grid, area, path, goal, last, months)

def ring(p, size=86):
    d, n = counts(p)
    r = 34; c = 2 * math.pi * r
    f = d / n if n else 0
    now = sum(1 for _, s in p['steps'] if s == 'now') / n if n else 0
    return ('<svg viewBox="0 0 86 86" width="%d" height="%d" aria-hidden="true"><circle cx="43" cy="43" r="%d" class="rg-bg"/>'
            '<circle cx="43" cy="43" r="%d" class="rg-now" stroke-dasharray="%.1f %.1f" stroke-dashoffset="%.1f" transform="rotate(-90 43 43)"/>'
            '<circle cx="43" cy="43" r="%d" class="rg-done" stroke-dasharray="%.1f %.1f" transform="rotate(-90 43 43)"/>'
            '<text x="43" y="50" class="rg-t">%s</text></svg>') % (
        size, size, r, r, c * now, c, -c * f, r, c * f, c, ('%d/%d' % (d, n)) if n else '—')

def b_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    m = d['money']
    if m:
        panel = ('<aside class="rb-tr"%s><div class="v-ah"><b class="v-ach">Left from every 100 rupees</b>%s</div>'
                 '<div class="rb-big"><b>12.8</b><span>this month · goal 18</span></div>%s'
                 '<div class="rb-row"><div><span>Money in</span><b>%s</b></div><div><span>Left after costs</span><b>%s</b></div><div><span>Short of goal</span><b>₹90 lakh</b></div></div></aside>') % (
            pt(1), tag('example'), trend_svg(m), e(m['in'][1]), e(m['left'][1]))
    else:
        panel = '<aside class="rb-tr is-empty"><b class="v-ach">Left from every 100 rupees</b><p>Draws twelve months once last year’s statement is in.</p></aside>'
    top = '<div class="v-top rb-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), panel)
    cards, desk = [], []
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        lab = 'Gap found' if p['name'] == 'Diagnosis' else 'Could bring back'
        back = ('<span class="rb-back"><span>%s</span><b>%s</b></span>' % (lab, e(p['amt'] + (' a month' if p['amt'] != '—' else '')))) if not empty else ''
        inner = ('<span class="rb-band"><span class="rb-no">%02d</span><span class="rb-pn">%s</span></span><span class="rb-mid">%s<span class="rb-sg" aria-hidden="true">%s</span></span>'
                 '<span class="v-st s-%s">%s</span><span class="rb-hl">%s</span><span class="rb-pr">%s</span>%s%s') % (
            i + 1, e(p['name']), ring(p), L2.segs(p), p['status'], e(STATUS[p['status']]), e(p['head']), e(prog(p)), back, '' if empty else CHEV)
        if empty:
            cards.append('<div class="rb-card is-empty" data-s="empty">%s</div>' % inner); continue
        cards.append('<button class="rb-card %s" type="button" data-s="%s"%s%s>%s</button>' % (sel_cls(first), p['status'], sel('rb', k, first), pt(p.get('pt')), inner))
        det = detail(p); cards.append(box('rb', k, det, first, 'mob')); desk.append(box('rb', k, det, first, 'desk'))
    board = '<div class="rb-cards%s">%s</div>' % (' is-empty' if empty else '', ''.join(cards))
    key = L2.key_html('rb-key') if not empty else ''
    sub = 'One results card for each part of the work. The ring shows steps done. Tap a card.' if not empty else 'One results card for each part of the work'
    return (masthead(state) + top + section('Where each part of the work stands', board + key + ('<div class="rb-desk">%s</div>' % ''.join(desk) if desk else ''), 'rb-sec', sub)
            + pending(d['pending']) + actions(d['actions']))

B_CSS = r'''
.rb-top{grid-template-columns:minmax(0,1fr) minmax(0,1.15fr)}
.rb-tr{display:flex;flex-direction:column;gap:8px;background:var(--card);padding:16px 18px 16px;border-top:6px solid var(--ink)}
.rb-big{display:flex;align-items:baseline;gap:10px}
.rb-big b{font:400 30px/1 var(--f-d)}
.rb-big span{font-size:13px;color:var(--mut);font-weight:600}
.rb-svg{width:100%;height:auto;display:block}
.rb-svg .tg{stroke:var(--line);stroke-width:1}
.rb-svg .tl,.rb-svg .tm{font:500 11.5px var(--f-b);fill:var(--mut);text-anchor:end}
.rb-svg .tm{text-anchor:middle}
.rb-svg .tgoal{stroke:var(--ink);stroke-width:1.5;stroke-dasharray:6 4}
.rb-svg .tlg{font:600 11.5px var(--f-b);fill:var(--ink)}
.rb-svg .tline{fill:none;stroke:var(--ink);stroke-width:2.5;stroke-linejoin:round}
.rb-svg .tarea{fill:var(--hi-soft)}
.rb-svg .tdot{fill:var(--hi);stroke:var(--ink);stroke-width:2}
.rb-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;border-top:1px solid var(--line);padding-top:8px}
.rb-row div{display:flex;flex-direction:column;gap:2px;min-width:0}
.rb-row span{font-size:11.5px;font-weight:600;color:var(--mut)}
.rb-row b{font:400 24px/1 var(--f-d)}
.rb-tr.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey);color:var(--mut)}
.rb-tr.is-empty p{font-size:14px}
.rb-cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;align-items:start}
.rb-card{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:8px;text-align:left;border:0;background:var(--card);padding:0 14px 14px;color:var(--ink);min-width:0}
.rb-band{align-self:stretch;display:flex;align-items:baseline;gap:8px;margin:0 -14px;padding:10px 14px;background:var(--ink);color:var(--card)}
.rb-no{font:400 18px/1 var(--f-d);color:var(--hi)}
.rb-pn{font:400 24px/1 var(--f-d)}
.rb-mid{display:flex;align-items:center;gap:10px;align-self:stretch;margin-top:4px}
.rb-sg{display:flex;flex-direction:column;gap:3px;flex:1;height:60px}
.rb-sg .sg{flex:1;height:auto}
.rg-bg{fill:none;stroke:var(--soft);stroke-width:10}
.rg-done{fill:none;stroke:var(--ink);stroke-width:10}
.rg-now{fill:none;stroke:var(--hi);stroke-width:10}
.rg-t{font:400 22px var(--f-d);fill:var(--ink);text-anchor:middle}
.rb-hl{font-size:13.5px;line-height:1.45}
.rb-pr{font-size:12px;font-weight:600;color:var(--mut)}
.rb-back{align-self:stretch;display:flex;flex-direction:column;gap:3px;border-top:1px solid var(--line);padding-top:6px}
.rb-back span{font-size:11.5px;font-weight:600;color:var(--mut)}
.rb-back b{font:400 22px/1 var(--f-d);white-space:nowrap}
.rb-card[data-s=none] .rb-hl,.rb-card.is-empty .rb-hl{color:var(--mut)}
.rb-card[data-s=none] .rb-band,.rb-card.is-empty .rb-band{background:var(--soft);color:var(--mut)}
.rb-card .sel-chev{position:absolute;right:14px;top:12px;margin:0;color:var(--card)}
.rb-cards.is-empty .rb-card{background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey)}
.rb-key{margin-top:14px}
.rb-desk{margin-top:16px}
@container lp (max-width:699px){
 .rb-top{grid-template-columns:1fr}
 .rb-cards{grid-template-columns:1fr}
 .rb-card .sel-chev{display:inline-block}
 .rb-cards .bx-mob{margin:-4px 0 4px}
 .rb-sg{height:auto;flex-direction:row;height:14px}
}
'''

# ==========================================================================================
# C · THE COIN STACKS
def bridge(m):
    """Money in, each cost taken away, what is left: a flat bridge, one row per line."""
    total = 18.0
    rows, run = [], total
    rows.append(('Money in', m['in'][1], 0, total, 'in'))
    for a, v, x in m['costs']:
        rows.append((a, '− ' + v, run - x, x, 'cost')); run -= x
    rows.append(('Left', m['left'][1], 0, run, 'left'))
    out = ''.join('<div class="rc-r rc-%s"><span class="rc-l">%s</span><span class="rc-t"><i style="margin-left:%.2f%%;width:%.2f%%"></i></span><b>%s</b></div>' % (
        k, e(a), s / total * 100, w / total * 100, e(v)) for a, v, s, w, k in rows)
    return out

def c_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    m = d['money']
    if m:
        panel = ('<aside class="rc-br"%s><div class="v-ah"><b class="v-ach">This month, from money in to what is left</b>%s</div>'
                 '<div class="rc-rows" role="img" aria-label="Money in ₹18 crore; less staff, medicines and supplies, doctors’ fees, rent, power and upkeep; ₹2.3 crore left.">%s</div>'
                 '<div class="rc-foot"><span>%s</span><b>%s</b></div></aside>') % (pt(1), tag('example'), bridge(m), e(m['share']), e(m['goal']))
    else:
        panel = '<aside class="rc-br is-empty"><b class="v-ach">This month, from money in to what is left</b><p>Fills in once last year’s statement is in.</p></aside>'
    top = '<div class="v-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), panel)
    stacks, desk = [], []
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        coins = ''.join('<i class="cn s-%s"></i>' % s for _, s in reversed(p['steps'])) or '<i class="cn s-empty"></i><i class="cn s-empty"></i>'
        inner = ('<span class="rc-stack" aria-hidden="true">%s</span><span class="rc-base"></span><span class="rc-no">%02d</span><span class="rc-pn">%s</span>'
                 '<span class="v-st s-%s">%s</span><span class="rc-pr">%s</span><span class="rc-hl">%s</span>%s') % (
            coins, i + 1, e(p['name']), p['status'], e(STATUS[p['status']]), e(prog(p)), e(p['head']), '' if empty else CHEV)
        if empty:
            stacks.append('<div class="rc-st is-empty" data-s="empty">%s</div>' % inner); continue
        stacks.append('<button class="rc-st %s" type="button" data-s="%s"%s%s>%s</button>' % (sel_cls(first), p['status'], sel('rc', k, first), pt(p.get('pt')), inner))
        det = detail(p); stacks.append(box('rc', k, det, first, 'mob')); desk.append(box('rc', k, det, first, 'desk'))
    counter = '<div class="rc-counter%s"><div class="rc-stacks">%s</div></div>' % (' is-empty' if empty else '', ''.join(stacks))
    key = ('<div class="rc-key" aria-hidden="true"><span><i class="cn s-done"></i>Done</span><span><i class="cn s-now"></i>Now</span>'
           '<span><i class="cn s-later"></i>Still to do</span><span><i class="cn s-none"></i>Not started</span></div>') if not empty else ''
    sub = 'One stack of coins for each part of the work, one coin per step. Tap a stack.' if not empty else 'One stack of coins for each part of the work'
    return (masthead(state) + top + section('Where each part of the work stands', counter + key + ('<div class="rc-desk">%s</div>' % ''.join(desk) if desk else ''), 'rc-sec', sub)
            + pending(d['pending']) + actions(d['actions']))

C_CSS = r'''
.rc-br{display:flex;flex-direction:column;gap:10px;background:var(--card);padding:16px 18px;border-top:6px solid var(--ink)}
.rc-rows{display:flex;flex-direction:column;gap:6px}
.rc-r{display:grid;grid-template-columns:112px minmax(0,1fr) 100px;align-items:center;gap:10px;font-size:13px;line-height:1.3}
.rc-l{min-width:0}
.rc-t{display:block;height:18px;background:repeating-linear-gradient(90deg,var(--line) 0 1px,transparent 1px 20%)}
.rc-t i{display:block;height:100%}
.rc-in .rc-t i{background:var(--ink)}
.rc-cost .rc-t i{background:var(--soft);box-shadow:inset 0 0 0 1.5px var(--ink)}
.rc-left .rc-t i{background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.rc-r b{font-weight:600;text-align:right;white-space:nowrap}
.rc-left b{font:400 24px/1 var(--f-d)}
.rc-left .rc-l{font-weight:600}
.rc-foot{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;border-top:3px double var(--ink);padding-top:8px;font-size:13px}
.rc-foot b{font-weight:600}
.rc-br.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey);color:var(--mut)}
.rc-br.is-empty p{font-size:14px}
.rc-counter{background:var(--card);border-top:6px solid var(--ink);padding:18px 14px 16px;background-image:linear-gradient(transparent 155px,var(--soft) 155px)}
.rc-stacks{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;align-items:start}
.rc-st{position:relative;display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;border:0;background:transparent;padding:6px 10px 14px;color:var(--ink);min-width:0}
.lp .rc-st.is-up{background:var(--card)}
.rc-stack{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:118px;gap:0}
.cn{display:block;width:84px;height:16px;border-radius:50%;margin-top:-3px;box-shadow:inset 0 0 0 2px var(--ink);position:relative}
.cn::after{content:"";position:absolute;left:12%;right:12%;top:4px;height:2px;border-radius:2px;background:rgba(255,255,255,.35)}
.cn.s-done{background:var(--ink)}
.cn.s-now{background:var(--hi)}
.cn.s-later{background:var(--card)}
.cn.s-later::after,.cn.s-none::after,.cn.s-empty::after{display:none}
.cn.s-none,.cn.s-empty{background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey);background-image:repeating-linear-gradient(135deg,transparent 0 4px,rgba(0,0,0,.08) 4px 5px)}
.rc-base{width:110px;height:6px;background:var(--ink);margin-bottom:6px}
.rc-no{font:400 18px/1 var(--f-d);color:var(--mut)}
.rc-pn{font:400 26px/1 var(--f-d)}
.rc-pr{font-size:12px;font-weight:600;color:var(--mut)}
.rc-hl{font-size:13.5px;line-height:1.45}
.rc-st[data-s=none] .rc-pn,.rc-st[data-s=none] .rc-hl,.rc-st.is-empty .rc-pn,.rc-st.is-empty .rc-hl{color:var(--mut)}
.rc-st .sel-chev{position:absolute;right:12px;top:12px;margin:0}
.rc-counter.is-empty{background:transparent;background-image:none;border:2px dashed var(--grey);border-top:6px solid var(--grey)}
.rc-key{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:12.5px;color:var(--mut);margin-top:14px}
.rc-key span{display:inline-flex;align-items:center;gap:8px}
.rc-key .cn{width:26px;height:10px;margin:0}
.rc-desk{margin-top:16px}
@container lp (max-width:699px){
 .rc-r{grid-template-columns:96px minmax(0,1fr) 92px;gap:8px;font-size:12.5px}
 .rc-counter{background-image:none;padding:12px 10px}
 .rc-stacks{grid-template-columns:1fr;gap:10px}
 .rc-st{display:grid;grid-template-columns:auto minmax(0,1fr);grid-template-areas:"stack no" "stack pn" "stack st" "stack pr" "hl hl";column-gap:14px;row-gap:4px;text-align:left;align-items:start;justify-items:start;padding:10px 40px 12px 8px;border-bottom:1px solid var(--line)}
 .rc-stack{grid-area:stack;height:auto;min-height:70px;width:72px}
 .rc-stack .cn{width:64px;height:13px;margin-top:-2px}
 .rc-base{display:none}
 .rc-no{grid-area:no}.rc-pn{grid-area:pn}.rc-st .v-st{grid-area:st}.rc-pr{grid-area:pr}.rc-hl{grid-area:hl}
 .rc-st .sel-chev{display:inline-block}
 .rc-stacks .bx-mob{margin:-4px 0 4px}
}
'''

# ==========================================================================================
T = C.theme
RAIL = ['#E6E2EE', '#E3ECE6', '#F4E9D8', '#E2E8F3', '#F1E2E8']
THEMES = {
 # A: banknote green paper, bottle green ink, marigold
 'a': T('#E4ECE3', '#FFFFFF', '#0C2E26', '#3E584F', '#C3D3C6', '#F0F5EF', '#93A79A', '#F2B233', '#F5C25C', '#7A5200',
        ['#DCE6DC', '#E8EFE6', '#F6EBD3', '#E3EBE6', '#EEE7D8'], '#0C2E26'),
 # B: pale periwinkle, midnight, growth green
 'b': T('#E8EBF6', '#FFFFFF', '#121A3A', '#4A5170', '#C9CEE3', '#F1F3FA', '#9BA1BD', '#35D088', '#5EDC9F', '#0E6B42',
        ['#E0E4F2', '#E9ECF7', '#E4F3EC', '#ECE8F6', '#F2EEE4'], '#121A3A'),
 # C: blush cream, aubergine, teal
 'c': T('#F4ECE6', '#FFFFFF', '#2A1B37', '#5C4C68', '#E2D1C6', '#FAF4EF', '#AE9DA6', '#22C1B0', '#4FD4C5', '#0B6A60',
        ['#EEE3DB', '#F6EDE6', '#E0F2EF', '#EFE6EE', '#F3EADF'], '#2A1B37'),
}
PAGES = {
 'a': (a_canvas, A_CSS, 'A', 'The cheque book'),
 'b': (b_canvas, B_CSS, 'B', 'The results board'),
 'c': (c_canvas, C_CSS, 'C', 'The coin stacks'),
}
NOTE = ('<em>All three: the Financial look approved for Supply Chain and Procurement (Virevo type unchanged, flat frame, ledger and receipt paper) '
        'in colours no other tool uses. Every figure is made up for an example 250-bed hospital and marked Example only or Tojo’s guess.</em>')
ABOUT = {
 'a': ('<b>A · The cheque book.</b> The month’s profit and loss on ledger paper: money in, each cost taken away, and a double-ruled line for what is left. '
       'Each part of the work is a cheque made out for what it should bring back, with a counterfoil that ticks its steps and a signature line for when it is agreed. '
       'Colours: banknote green, bottle green ink, marigold.' + NOTE),
 'b': ('<b>B · The results board.</b> Twelve months of what is left from every 100 rupees, against a dashed goal line, with this month marked. '
       'Each part of the work is a results card: a ring of steps done, a step bar, and what it could bring back. Colours: periwinkle, midnight ink, growth green.' + NOTE),
 'c': ('<b>C · The coin stacks.</b> The month’s money as a bridge, from money in, cost by cost, to what is left. '
       'Each part of the work is a stack of coins on a counter, one coin per step: inked when done, highlighted when now. Colours: blush cream, aubergine ink, teal.' + NOTE),
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
                h = C.page(SK, t, None, canvas, base + css, DATA[st]['chat'], v, 'Revenue & EBITDA · %s' % label, 'rv rv-home rv-%s' % k)
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(OUT, 'rev-home-%s.%s.%s.html' % (k, v, st)), 'w', encoding='utf-8').write(h)
            text = re.sub(r'<[^>]+>', ' ', canvas) + ' ' + json.dumps(DATA[st]['chat'], ensure_ascii=False)
            words += [(k, st, w) for w in C.plain_check(text.replace('EBITDA', ''))]
    return pages, words

def review(pages):
    tpl = open(os.path.join(SCP, 'review_template.html'), encoding='utf-8').read()
    tpl = tpl.replace('Supply Chain and Procurement · three looks for the Financial domain', 'Revenue & EBITDA · the home page in three looks')
    tpl = tpl.replace('Supply Chain and Procurement · the home page in three looks', 'Revenue & EBITDA · the home page in three looks')
    tpl = re.sub(r'<p class="rv-intro">.*?</p>', '<p class="rv-intro">The second Financial tool. All three looks keep the Financial identity approved for Supply Chain and Procurement '
                 '(the Virevo type unchanged, the flat frame, ledger and receipt paper) and the same five zones, and each brings its own money drawing in colours no other tool uses. '
                 'Pick a look below. Scroll inside each view; every page opens with its first part raised and its box open. On the phone, each box opens right under the part you tap.</p>', tpl, flags=re.S)
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>Sample %s</b><span>%s</span><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 4px %s"></i></button>' % (
        k, 'true' if k == 'a' else 'false', v[2], e(v[3]), THEMES[k]['ground'], THEMES[k]['ink'], THEMES[k]['hi']) for k, v in PAGES.items())
    return (tpl.replace('@@PICKS@@', picks).replace('@@ABOUT@@', json.dumps(ABOUT, ensure_ascii=False))
               .replace('@@DATA@@', json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')))

if __name__ == '__main__':
    pages, words = build()
    if words:
        print('PLAIN ENGLISH:', words)
    rv = os.path.join(OUT, 'revenue-ebitda-home-samples.html')
    open(rv, 'w', encoding='utf-8').write(review(pages))
    print('built', rv, os.path.getsize(rv))
