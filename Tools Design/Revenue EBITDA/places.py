"""
Revenue & EBITDA: the four place pages, beside the approved home page A (the cheque book). 8 Oct 2026, for review.

All five use the Financial look (V skin, Virevo type unchanged). Each place has its own colours,
none used by another tool, and its own money drawing:

  Home         A · the cheque book (approved): profit and loss on ledger paper; one cheque per part.
  Diagnosis    the bank statement: ₹1,000 of bills followed to the bank, each step a statement line
               with what was lost and the balance left; the gap split four ways on a ring.
  Solutions    the payback sheet: one entry per fix, what it costs to start, what it brings back each
               month, and a twelve-month strip showing the month it pays for itself.
  Automations  the bill's road: the money's journey from the patient leaving to the bank, each helper
               hung at the stop where it acts, and the note it would send.
  Processes    the money rhythm: daily, weekly and monthly lanes with the changes pinned in them;
               who owns each line of the profit and loss; the numbers we watch, plan against now.

Every figure is made up for an example 250-bed hospital and marked Example only or Tojo's guess.
Run:  python3 places.py   ->  out/landing/
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rev_landing as H              # sets the tool name, loads the Financial look
C, L2, L3 = H.C, H.L2, H.L3
from sc_common import e, ico, ICONS, CHEV, sel, sel_cls, box, pt, tag, say_btn, standing, section, pending, actions, STAMP

SK = H.SK
OUT = H.OUT
masthead, two = L3.masthead, L3.two

# ==========================================================================================
RAIL = ['#E3E8E2', '#F7E6DC', '#ECEED9', '#E1ECF7', '#F2E6F0']   # Resources, then the four places in their own grounds
def T(ground, card, ink, mut, line, soft, grey, hi, hi_dark, hi_text, panel):
    return C.theme(ground, card, ink, mut, line, soft, grey, hi, hi_dark, hi_text, RAIL, panel)
THEMES = {
 # home (approved A): banknote green, bottle green, marigold
 'home': T('#E4ECE3', '#FFFFFF', '#0C2E26', '#3E584F', '#C3D3C6', '#F0F5EF', '#93A79A', '#F2B233', '#F5C25C', '#7A5200', '#0C2E26'),
 # Diagnosis: peach, deep plum, electric blue
 'diagnosis': T('#F7E6DC', '#FFFFFF', '#3A1430', '#6A4A5E', '#E4C9BA', '#FBF1EB', '#B59AA6', '#5B8CFF', '#86A9FF', '#2347B8', '#3A1430'),
 # Solutions: pale olive, deep teal, tangerine
 'solutions': T('#ECEED9', '#FFFFFF', '#0E3B3A', '#46605E', '#D2D6B4', '#F5F6EA', '#9DA88F', '#FF9A2E', '#FFAE57', '#8A4300', '#0E3B3A'),
 # Automations: ice blue, navy, hot pink
 'automations': T('#E1ECF7', '#FFFFFF', '#0D2240', '#45556E', '#C2D3E6', '#EFF5FB', '#95A6BB', '#FF5C93', '#FF85AE', '#B3124D', '#0D2240'),
 # Processes: orchid pink, aubergine brown, sea green
 'processes': T('#F2E6F0', '#FFFFFF', '#2E1A2C', '#5E4A5B', '#DECBDA', '#F9F2F7', '#AD98AA', '#2EC4A6', '#5ED6BE', '#0B6E5B', '#2E1A2C'),
}

def chip(cls, text):
    return '<span class="fx-chip %s">%s</span>' % (cls, e(text))

# ==========================================================================================
# DIAGNOSIS · the bank statement
DG = {
 'filled': {
  'claim': 'Of every ₹1,000 we bill, ₹967 reaches the bank, 41 days later',
  'deck': 'Two of five steps done. We followed ₹1,000 of September bills from the patient leaving to the money in the bank. The biggest loss is claims the insurer turns down or cuts.',
  'lines': [
   {'when': 'Day 0', 'what': 'Bill raised when the patient goes home', 'lost': None, 'bal': '₹1,000', 'note': 'The start',
    'found': 'We took September’s bills for patients who stayed at least one night: about ₹1,000 of every ₹1,000 billed is our starting point.',
    'points': 'Billing works. The losses come after this line.'},
   {'when': 'Day 0', 'what': 'Items used on the ward but missed on the bill', 'lost': '₹11', 'bal': '₹989',
    'found': 'Dressings, cannulas and some medicines used at night were not written on the chart, so billing never saw them.',
    'points': 'Bedside recording. The Supply Chain and Procurement work found the same gap.'},
   {'when': 'Day 9', 'what': 'Bill sent to the insurer, 9 days on average', 'lost': None, 'bal': '₹989', 'note': 'Time lost', 'pt': 3,
    'found': 'Bills wait for the doctor’s notes and the discharge papers. Most insurers set a time limit; late bills are cut more often.',
    'points': 'Bills should go the day the patient leaves.'},
   {'when': 'Day 30', 'what': 'Claims turned down or cut by the insurer', 'lost': '₹22', 'bal': '₹967', 'pt': 2,
    'found': 'About 7 of every 100 claims come back turned down or cut, mostly for missing papers or codes that do not match.',
    'points': 'Check each claim before it goes. The biggest loss.'},
   {'when': 'Day 41', 'what': 'Money reaches the bank', 'lost': None, 'bal': '₹967', 'note': 'The end',
    'found': 'The money that is paid arrives about 41 days after the patient left. Some small bills are written off after 90 days.',
    'points': 'Time to cash matters too, but less than what is lost.'},
  ],
  'gap': [('Claims turned down or cut', 40, 'Leading so far', True, 2), ('Items missed on the bill', 20, 'Being checked', False, None),
          ('Packages priced below cost', 20, 'Being checked', False, 4), ('Quiet days and empty beds', 10, 'Not checked yet', False, None)],
  'pending': [
   {'text': 'Get the list of claims turned down in the last three months, with the reason.', 'need': 'Needs the insurance desk’s records', 'pt': 2},
   {'text': 'Find what each of the top 20 packages really costs.', 'pt': 4},
   {'text': 'Count the days each bill waits after the patient leaves.', 'pt': 3},
   {'text': 'Name the main cause, so the fixes start in the right place.'},
  ],
  'actions': {'go': {'detail': 'Check the claims turned down', 'say': 'Let’s check the claims turned down'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about how our money comes in: '},
              'jump': {'tab': 'Solutions', 'detail': 'See the three fixes so far', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['Diagnosis is two of five steps in.', 'Of every ₹1,000 we bill, ₹967 reaches the bank, about 41 days later. Two thirds of the loss is claims the insurer turns down or cuts.'],
           'pointer': 'Pick a point to add to it, or tap a line of the statement.',
           'note': 'The bill is right. The claim is not.',
           'points': [{'n': 1, 'label': 'The gap, split four ways'}, {'n': 2, 'label': 'Claims turned down'},
                      {'n': 3, 'label': 'Bills sent late'}, {'n': 4, 'label': 'Package prices'}],
           'prompts': ['Our insurance desk has the list', 'Why are claims turned down?', 'Let’s check the claims']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Tojo follows ₹1,000 of bills with you, from the patient leaving to the money in the bank, and writes each step as a line of a statement.',
  'lines': [{'when': '', 'what': w} for w in ['Bill raised when the patient goes home', 'Items used but missed on the bill', 'Bill sent to the insurer',
                                               'Claims turned down or cut', 'Money reaches the bank']],
  'gap': [('Claims turned down', 0, '', False, None), ('Items missed', 0, '', False, None), ('Package prices', 0, '', False, None), ('Quiet days', 0, '', False, None)],
  'pending': [
   {'text': 'Put a number on what is left from every 100 rupees.', 'need': 'Needs last year’s profit and loss statement'},
   {'text': 'Follow one month of bills to the bank with Tojo.'},
   {'text': 'Find out who sends claims to insurers, and when.'},
  ],
  'actions': {'go': {'detail': 'Put a number on the gap with Tojo', 'say': 'Let’s put a number on the gap'},
              'add': {'detail': 'Share a profit and loss statement', 'say': 'Here is what I already know about our money: '},
              'jump': {'tab': 'Solutions', 'detail': 'Fills in once the cause is named', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['This is Diagnosis. We find out where money is lost between the bill and the bank.', 'We start with one month of bills.'],
           'note': 'Follow the money to the bank.', 'points': [],
           'prompts': ['Let’s put a number on the gap', 'What should I bring?', 'What is EBITDA?']},
 },
}

def donut(gap, empty):
    tot = sum(g[1] for g in gap) or 1
    r, cx, cy, sw = 54, 70, 70, 22
    import math
    c = 2 * math.pi * r
    cols = ['var(--hi)', 'var(--ink)', 'var(--mut)', 'var(--grey)']
    segs, off = [], 0.0
    for (name, v, *_), col in zip(gap, cols):
        L = c * v / tot
        segs.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="%d" stroke-dasharray="%.1f %.1f" stroke-dashoffset="%.1f" transform="rotate(-90 %d %d)"/>' % (
            cx, cy, r, col, sw, max(L - 2, 0), c, -off, cx, cy))
        off += L
    if empty:
        segs = ['<circle cx="70" cy="70" r="54" fill="none" stroke="var(--grey)" stroke-width="2" stroke-dasharray="5 4"/>']
    mid = ('<text x="70" y="68" class="dn-b">₹90 lakh</text><text x="70" y="88" class="dn-s">a month</text>' if not empty else
           '<text x="70" y="76" class="dn-s">Not split yet</text>')
    return '<svg viewBox="0 0 140 140" width="150" height="150" role="img" aria-label="%s">%s%s</svg>' % (
        e('The ₹90 lakh gap: ' + ', '.join('%s ₹%d lakh' % (g[0], g[1]) for g in gap) if not empty else 'Not split yet'), ''.join(segs), mid)

def dg_canvas(state):
    d = DG[state]; empty = state == 'empty'
    rows, desk = [], []
    for i, r in enumerate(d['lines']):
        k = str(i); first = i == 0 and not empty
        if empty:
            rows.append('<div class="ds-l is-empty"><span class="ds-d">—</span><span class="ds-w">%s</span><span class="ds-x">—</span><span class="ds-b">—</span></div>' % e(r['what']))
            continue
        lost = r['lost']
        rows.append(('<button class="ds-l %s%s" type="button"%s%s><span class="ds-d">%s</span><span class="ds-w">%s%s</span><span class="ds-x">%s</span>'
                     '<span class="ds-b">%s</span>%s</button>') % (
            sel_cls(first), ' is-loss' if lost else '', sel('ds', k, first), pt(r.get('pt')), e(r['when']), e(r['what']),
            '<span class="ds-n">%s</span>' % e(r['note']) if r.get('note') else '', ('− ' + e(lost)) if lost else '—', e(r['bal']), CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>%s</h4>%s%s</div><p>%s</p>%s</div>') % (
            e(r['when']), chip('c-now', lost + ' lost') if lost else chip('', r.get('note', '')), tag('example'), e(r['what']),
            two('What we found', r['found'], 'What it points to', r['points']))
        rows.append(box('ds', k, det, first, 'mob'))
        desk.append(box('ds', k, det, first, 'desk'))
    head = ('<div class="ds-top"><div><span class="ds-k">Statement</span><b>₹1,000 of September bills</b></div>%s</div>'
            '<div class="ds-h" aria-hidden="true"><span>Day</span><span>What happened</span><span>Lost</span><span>Left</span></div>') % (tag('example') if not empty else '')
    foot = ('<div class="ds-f"%s><span>Reached the bank</span><b>₹967</b><span class="ds-fl">Lost on the way: ₹33 of every ₹1,000</span></div>' % pt(1)) if not empty else ''
    stmt = '<div class="ds-st%s">%s<div class="ds-rows">%s</div>%s</div>' % (' is-empty' if empty else '', head, ''.join(rows), foot)
    body = '<div class="ds-wrap">%s<div class="ds-side">%s</div></div>' % (stmt, ''.join(desk) if desk else '<p class="fx-empty">Each line opens here once it is written.</p>')
    sub = 'Each step from the bill to the bank is a line: what was lost, and what is left. Tap a line.' if not empty else 'Writes itself as we follow the bills'
    leg = ''.join('<li%s><i style="background:%s"></i><span>%s</span><b>%s</b><em>%s</em></li>' % (
        pt(g[4]), col, e(g[0]), ('₹%d lakh' % g[1]) if not empty else '—', e(g[2] or 'Not weighed yet')) for g, col in zip(d['gap'], ['var(--hi)', 'var(--ink)', 'var(--mut)', 'var(--grey)']))
    gap = '<div class="dn"%s>%s<ul class="dn-leg">%s</ul></div><p class="fx-hint">%s</p>' % (
        pt(1) if not empty else '', donut(d['gap'], empty), leg,
        'Example only. The two top causes come from the statement above; the other two are still being checked.' if not empty else 'Tojo splits the gap as the evidence comes in.')
    return (masthead('Diagnosis', state) + standing(d['claim'], d['deck'], empty)
            + section('The bank statement', body, 'ds-sec', sub)
            + section('Where the ₹90 lakh gap comes from', gap, 'dn-sec', 'Four possible causes, a month')
            + pending(d['pending']) + actions(d['actions']))

DG_CSS = r'''
.ds-wrap{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:22px;align-items:start}
.ds-st{background:var(--card);border-top:6px solid var(--ink);padding:14px 16px 12px}
.ds-top{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;padding-bottom:10px}
.ds-top div{display:flex;flex-direction:column;gap:2px}
.ds-k{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.ds-top b{font:400 24px/1 var(--f-d)}
.ds-h,.ds-l{display:grid;grid-template-columns:52px minmax(0,1fr) 62px 66px 12px;align-items:baseline;gap:8px}
.ds-h{border-top:3px double var(--ink);border-bottom:1px solid var(--ink);padding:6px 4px}
.ds-h span{font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.ds-h span:nth-child(3),.ds-h span:nth-child(4){text-align:right}
.ds-l{width:100%;border:0;border-bottom:1px solid var(--line);background:transparent;text-align:left;padding:9px 4px;color:var(--ink);font-size:14px;line-height:1.4}
.lp .ds-l.is-up{background:var(--soft)}
.ds-d{font:400 18px/1 var(--f-d);color:var(--mut)}
.ds-w{display:flex;flex-direction:column;gap:2px;min-width:0}
.ds-n{font-size:12px;font-weight:600;color:var(--mut)}
.ds-x{text-align:right;font-weight:600;color:var(--mut);white-space:nowrap}
.ds-l.is-loss .ds-x{font:400 22px/1 var(--f-d);color:var(--hi-text)}
.ds-b{text-align:right;font:400 22px/1 var(--f-d);white-space:nowrap}
.ds-l .sel-chev{display:none}
.ds-f{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:baseline;gap:4px 10px;padding:10px 4px 2px;border-top:1px solid var(--ink)}
.ds-f>span:first-child{font-size:14px;font-weight:600}
.ds-f b{font:400 30px/1 var(--f-d);border-bottom:5px double var(--ink);background:linear-gradient(transparent 50%,var(--hi-soft) 50% 90%,transparent 90%);padding:0 3px 2px}
.ds-fl{grid-column:1/-1;font-size:13px;color:var(--mut)}
.ds-st.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey)}
.ds-l.is-empty{color:var(--mut);cursor:default}
.ds-side{position:sticky;top:190px}
.ds-side .fx-two{grid-template-columns:1fr}
.dn{display:flex;align-items:center;gap:28px;background:var(--card);padding:16px 20px;border-top:6px solid var(--ink)}
.dn svg{flex-shrink:0}
.dn-b{font:400 22px var(--f-d);fill:var(--ink);text-anchor:middle}
.dn-s{font:600 12px var(--f-b);fill:var(--mut);text-anchor:middle}
.dn-leg{flex:1;display:flex;flex-direction:column;min-width:0}
.dn-leg li{display:grid;grid-template-columns:14px minmax(0,1fr) 90px 120px;align-items:baseline;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.dn-leg li i{width:12px;height:12px}
.dn-leg b{font:400 22px/1 var(--f-d);text-align:right}
.dn-leg em{font-style:normal;font-size:12.5px;font-weight:600;color:var(--mut)}
@container lp (max-width:699px){
 .ds-wrap{grid-template-columns:1fr}
 .ds-side{display:none}
 .ds-st{padding:12px 10px 10px}
 .ds-h{display:none}
 .ds-l{grid-template-columns:44px minmax(0,1fr) 16px;grid-template-areas:"d w c" "d x x";row-gap:4px;padding:10px 2px}
 .ds-d{grid-area:d}.ds-w{grid-area:w}.ds-l .sel-chev{display:inline-block;grid-area:c}
 .ds-x{grid-area:x;text-align:left}
 .ds-b{display:none}
 .ds-rows .bx-mob{margin:2px 0 10px}
 .ds-rows .bx-mob .fx-box{border-top:3px solid var(--ink);background:var(--soft)}
 .dn{flex-direction:column;align-items:flex-start;gap:12px;padding:14px}
 .dn-leg{align-self:stretch}
 .dn-leg li{grid-template-columns:14px minmax(0,1fr) auto;row-gap:2px}
 .dn-leg em{grid-column:2/-1}
}
'''

# ==========================================================================================
# SOLUTIONS · the payback sheet
STOPS = ['Idea', 'Shaped', 'Tested with you', 'Agreed']
SO = {
 'filled': {
  'claim': 'Three fixes could bring back about ₹55 lakh a month',
  'deck': 'One fix is being tested with you. None is agreed yet. Each one says what it costs to start, what it brings back, and the month it pays for itself.',
  'fixes': [
   {'name': 'Bill every patient on the day they go home, with the claim checked first', 'stage': 2, 'cost': '₹6 lakh', 'back': '₹25 lakh', 'pay': 1, 'ramp': 0, 'pt': 1,
    'what': 'The bill and the claim are closed on the day the patient leaves. Each claim is checked for missing papers and codes before it goes to the insurer.',
    'hand': 'Two billing staff on the evening shift close each bill and tick a one-page claim checklist before sending.',
    'auto': 'A helper checks each claim against the insurer’s rules and lists what is missing before it is sent.',
    'needs': ['The insurance desk’s list of claims turned down', 'Doctors finishing their notes before the patient leaves']},
   {'name': 'Reprice the 20 packages that lose money', 'stage': 1, 'cost': '₹2 lakh', 'back': '₹15 lakh', 'pay': 1, 'ramp': 0, 'pt': 2,
    'what': 'We find what each of the top 20 packages really costs, and reprice or rework the ones that lose money on every patient.',
    'hand': 'The accounts team costs each package from last quarter’s bills and supplies, once a month.',
    'auto': 'A helper compares each package’s price with its cost every month and flags the ones that lose money.',
    'needs': ['Last quarter’s bills and supplies by package', 'Management agreeing to new prices']},
   {'name': 'Fill the quiet days with planned surgery', 'stage': 0, 'cost': '₹20 lakh', 'back': '₹15 lakh', 'pay': 3, 'ramp': 1,
    'what': 'Tuesdays and Saturdays run half empty. Planned surgery is moved to those days, with doctors and patients told well ahead.',
    'hand': 'The operating theatre manager keeps a two-week plan and offers the quiet days first.',
    'auto': 'A helper shows the empty slots for the next two weeks to every surgeon each Monday.',
    'needs': ['Surgeons agreeing to the new days', 'Theatre staff on the quiet days']},
  ],
  'pending': [
   {'text': 'Test the first fix with you: who closes the bill, and who checks the claim.', 'need': 'Needs the billing team’s shifts', 'pt': 1},
   {'text': 'Shape the second fix: which 20 packages, and what each costs.', 'pt': 2},
   {'text': 'Check that each fix also works with no new software.'},
  ],
  'actions': {'go': {'detail': 'Test the first fix with you', 'say': 'Let’s test the first fix: billing on the day the patient leaves'},
              'add': {'detail': 'Suggest a fix of your own', 'say': 'I have an idea for a fix: '},
              'jump': {'tab': 'Automations', 'detail': 'See the helpers for these fixes', 'say': 'Take me to Automations'}},
  'chat': {'text': ['Three fixes are written up. The first, billing on the day the patient leaves, is being tested with you.', 'Together they could bring back about ₹55 lakh a month, after about ₹28 lakh to start.'],
           'pointer': 'Pick a point to add to it, or tap a line of the payback sheet.',
           'note': 'Collect first. Then price. Then fill the beds.',
           'points': [{'n': 1, 'label': 'Billing on the day they leave'}, {'n': 2, 'label': 'The 20 packages'}, {'n': 3, 'label': 'What comes back'}],
           'prompts': ['Our billing team leaves at 6 PM', 'How sure is the ₹55 lakh?', 'Let’s test the first fix']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'The fixes are entered here once Diagnosis names the main cause, each with what it costs to start and the month it pays for itself.',
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

def so_canvas(state):
    d = SO[state]; empty = state == 'empty'
    rows, desk = [], []
    months = ''.join('<span>%d</span>' % m for m in range(1, 13))
    for i, f in enumerate(d['fixes']):
        k = str(i); first = i == 0
        cells = ''.join('<i class="pb-c %s"></i>' % ('c-ramp' if m <= f['ramp'] else 'c-pay' if m == f['pay'] else 'c-back' if m > f['pay'] else 'c-cost')
                        for m in range(1, 13))
        stops = ''.join('<span class="pb-t %s" title="%s"></span>' % ('on' if j < f['stage'] else 'now' if j == f['stage'] else '', e(s)) for j, s in enumerate(STOPS))
        rows.append(('<button class="pb-row %s" type="button"%s%s><span class="pb-no">%d</span><span class="pb-fix"><b>%s</b>'
                     '<span class="pb-st"><span class="pb-ts" aria-hidden="true">%s</span>Now: %s</span></span>'
                     '<span class="pb-n"><span>To start</span><b>%s</b></span><span class="pb-n pb-nb"><span>Back a month</span><b>%s</b></span>'
                     '<span class="pb-strip" aria-label="Pays for itself in month %d">%s</span>%s</button>') % (
            sel_cls(first), sel('pb', k, first), pt(f.get('pt')), i + 1, e(f['name']), stops, e(STOPS[f['stage']]),
            e(f['cost']), e(f['back']), f['pay'], cells, CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>Fix %d</h4>%s%s</div><p>%s</p>'
               '<div class="so-ways"><div class="so-way"><span class="fx-lab">By hand</span><p>%s</p></div><div class="so-way so-auto"><span class="fx-lab">Automatic</span><p>%s</p></div></div>'
               '<div><span class="fx-lab">What it relies on</span><ul class="fx-bul">%s</ul></div></div>') % (
            i + 1, chip('c-now', 'Now: ' + STOPS[f['stage']]), tag('guess'), e(f['what']), e(f['hand']), e(f['auto']), ''.join('<li>%s</li>' % e(x) for x in f['needs']))
        rows.append(box('pb', k, det, first, 'mob'))
        desk.append(box('pb', k, det, first, 'desk'))
    if empty:
        rows = ['<div class="pb-row is-empty"><span class="pb-no">%d</span><span class="pb-fix"><b>Not entered yet</b></span><span class="pb-n"><span>To start</span><b>—</b></span>'
                '<span class="pb-n pb-nb"><span>Back a month</span><b>—</b></span><span class="pb-strip">%s</span></div>' % (n, '<i class="pb-c"></i>' * 12) for n in (1, 2, 3)]
    head = '<div class="pb-head" aria-hidden="true"><span>No.</span><span>The fix</span><span>To start</span><span>Back a month</span><span class="pb-mo">Months 1 to 12 %s</span></div>' % (
        '<span class="pb-ms">%s</span>' % months)
    foot = ('<div class="pb-foot"%s><span>If all three are agreed</span>%s<span class="pb-tot"><span>To start <b>₹28 lakh</b></span><span>Back a month <b class="pb-big">₹55 lakh</b></span></span></div>' % (
        pt(3), tag('guess'))) if not empty else ''
    sheet = '<div class="pb-sheet%s">%s<div class="pb-rows">%s</div>%s</div>' % (' is-empty' if empty else '', head, ''.join(rows), foot)
    key = ('<div class="pb-key" aria-hidden="true"><span><i class="pb-c c-cost"></i>Paying back what it cost</span><span><i class="pb-c c-pay"></i>The month it pays for itself</span>'
           '<span><i class="pb-c c-back"></i>Money back</span><span><i class="pb-c c-ramp"></i>Getting started</span></div>') if not empty else ''
    body = sheet + key + ('<div class="pb-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'One entry per fix: what it costs, what it brings back, and when it pays for itself. Tap an entry.' if not empty else 'One entry per fix'
    return (masthead('Solutions', state) + standing(d['claim'], d['deck'], empty)
            + section('The payback sheet', body, 'pb-sec', sub) + pending(d['pending']) + actions(d['actions']))

SO_CSS = r'''
.pb-sheet{background:var(--card);border-top:6px solid var(--ink);background-image:linear-gradient(90deg,transparent 18px,var(--ink) 18px 19px,transparent 19px 22px,var(--ink) 22px 23px,transparent 23px)}
.pb-head,.pb-row{display:grid;grid-template-columns:64px minmax(0,1fr) 84px 96px 220px;align-items:center;gap:0 10px}
.pb-head{border-bottom:3px double var(--ink);padding:8px 12px 8px 0}
.pb-head>span{font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.pb-head>span:first-child{padding-left:30px}
.pb-mo{display:flex;flex-direction:column;gap:3px}
.pb-ms{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:2px;letter-spacing:0}
.pb-ms span{text-align:center;font-size:11px}
.pb-row{width:100%;border:0;border-bottom:1px solid var(--line);background:transparent;text-align:left;padding:12px 12px 12px 0;color:var(--ink);min-width:0}
.lp .pb-row.is-up{background:var(--card)}
.pb-no{font:400 26px/1 var(--f-d);color:var(--mut);padding-left:30px}
.pb-fix{display:flex;flex-direction:column;gap:6px;min-width:0}
.pb-fix b{font-size:14.5px;font-weight:600;line-height:1.35}
.pb-st{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--mut)}
.pb-ts{display:flex;gap:3px}
.pb-t{width:14px;height:8px;box-shadow:inset 0 0 0 1.5px var(--grey)}
.pb-t.on{background:var(--ink);box-shadow:none}.pb-t.now{background:var(--hi);box-shadow:inset 0 0 0 1.5px var(--ink)}
.pb-n{display:flex;flex-direction:column;gap:2px;text-align:right}
.pb-n span{font-size:11px;font-weight:600;color:var(--mut)}
.pb-n b{font:400 24px/1 var(--f-d);white-space:nowrap}
.pb-nb b{color:var(--hi-text)}
.pb-strip{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:2px;height:22px}
.pb-c{display:block;height:100%;box-shadow:inset 0 0 0 1px var(--line)}
.pb-c.c-cost{background:repeating-linear-gradient(135deg,var(--soft) 0 3px,var(--line) 3px 5px)}
.pb-c.c-pay{background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.pb-c.c-back{background:var(--ink)}
.pb-c.c-ramp{background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey);background-image:repeating-linear-gradient(90deg,transparent 0 3px,var(--line) 3px 4px)}
.pb-row .sel-chev{display:none}
.pb-row.is-empty{color:var(--mut);cursor:default}
.pb-foot{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding:10px 14px 12px 92px;border-top:3px double var(--ink);font-size:14px;font-weight:600}
.pb-tot{margin-left:auto;display:flex;align-items:baseline;gap:22px;flex-wrap:wrap}
.pb-tot span{font-size:12.5px;color:var(--mut)}
.pb-tot b{font:400 24px/1 var(--f-d);color:var(--ink);margin-left:6px}
.pb-tot b.pb-big{font-size:30px;border-bottom:5px double var(--ink);background:linear-gradient(transparent 50%,var(--hi) 50% 90%,transparent 90%);padding:0 3px 2px}
.pb-key{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:12.5px;color:var(--mut);margin-top:12px}
.pb-key span{display:inline-flex;align-items:center;gap:7px}.pb-key .pb-c{width:18px;height:12px}
.pb-desk{margin-top:16px}
.so-ways{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.so-way{padding:12px 14px;background:var(--soft);border-left:4px solid var(--ink)}
.so-way.so-auto{border-left-color:var(--hi)}
.so-way p{font-size:14px;line-height:1.55}
@container lp (max-width:699px){
 .pb-sheet{background-image:linear-gradient(90deg,transparent 8px,var(--ink) 8px 9px,transparent 9px 12px,var(--ink) 12px 13px,transparent 13px)}
 .pb-head{display:none}
 .pb-row{grid-template-columns:40px minmax(0,1fr) minmax(0,1fr) 22px;grid-template-areas:"no fix fix chev" "no n1 n2 n2" "no strip strip strip";row-gap:10px;padding:12px 8px 14px 0}
 .pb-no{grid-area:no;padding-left:20px;font-size:22px;align-self:start}
 .pb-fix{grid-area:fix}.pb-n{grid-area:n1;text-align:left}.pb-nb{grid-area:n2}.pb-strip{grid-area:strip}
 .pb-row .sel-chev{display:inline-block;grid-area:chev;align-self:start;margin-top:4px}
 .pb-rows .bx-mob{margin:2px 10px 12px 20px}
 .pb-foot{padding:10px 12px 12px 24px}
 .pb-tot{margin-left:0}
 .so-ways{grid-template-columns:1fr}
}
'''

# ==========================================================================================
# AUTOMATIONS · the bill's road
STOPS_ROAD = ['Patient leaves', 'Bill closed', 'Claim sent', 'Insurer pays', 'Money in the bank', 'Next morning', 'Month end']
LAMPS = ['Idea', 'Built', 'Tested', 'Switched on']
AU = {
 'filled': {
  'claim': 'Three helpers, each placed where the money slips',
  'deck': 'None is built yet. Each waits for its fix to be agreed. Each one does by itself what a person can also do by hand.',
  'helpers': [
   {'name': 'Claim checker', 'at': 2, 'when': 'Every claim, before it is sent', 'fix': 'Bill every patient on the day they go home', 'pt': 1,
    'does': 'Checks each claim against the insurer’s rules: papers, codes and limits. Lists what is missing before it goes.',
    'reads': 'The closed bill, the doctor’s notes and the insurer’s rules', 'to': 'The billing staff member who closed the bill',
    'note': [('Claim 2291 · Ward 4', ''), ('Discharge summary', 'Missing'), ('Code for the surgery', 'Does not match'), ('Hold until fixed', '2 items')]},
   {'name': 'Morning money note', 'at': 5, 'when': 'Every morning at 8 AM', 'fix': 'A ten-minute look at the money each morning', 'pt': 2,
    'does': 'Sends one short note: yesterday’s bills, money in, claims turned down, and what is left from every 100 rupees this month.',
    'reads': 'Yesterday’s bills, payments and claims', 'to': 'The Revenue Lead, the billing head and the insurance desk',
    'note': [('Yesterday · 7 October', ''), ('Billed', '₹61 lakh'), ('Money in', '₹54 lakh'), ('Claims turned down', '3')]},
   {'name': 'Package cost watch', 'at': 6, 'when': 'On the 1st of every month', 'fix': 'Reprice the 20 packages that lose money',
    'does': 'Works out what each package cost last month, and flags each one that cost more than its price.',
    'reads': 'Last month’s bills and supplies, by package', 'to': 'The Revenue Lead and the accounts team',
    'note': [('September · 20 packages', ''), ('Cost more than their price', '6'), ('Biggest loss', 'Knee replacement'), ('Lost on each', '₹14,000')]},
  ],
  'pending': [
   {'text': 'Agree the first fix, so its helper can be built.', 'pt': 1},
   {'text': 'Find out where claims and payments are kept today.', 'need': 'Needs a word with your accounts team'},
   {'text': 'Get each insurer’s rules for claims.'},
  ],
  'actions': {'go': {'detail': 'Agree the first fix in Solutions', 'say': 'Let’s agree the first fix so its helper can be built'},
              'add': {'detail': 'Tell Tojo about your systems', 'say': 'Here is how our bills and claims are kept today: '},
              'jump': {'tab': 'Processes', 'detail': 'See the changes for people', 'say': 'Take me to Processes'}},
  'chat': {'text': ['Three helpers are planned, one at each place the money slips. None is built yet.', 'Each sends one short note to one person.'],
           'pointer': 'Pick a point to add to it, or tap a helper on the road.',
           'note': 'Catch it before it leaves the building.',
           'points': [{'n': 1, 'label': 'Claim checker'}, {'n': 2, 'label': 'Morning money note'}],
           'prompts': ['Where are our claims kept?', 'Can these work with our software?', 'Show me the people changes']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Helpers are placed on the bill’s road here once a fix is agreed. Each one does one job at one stop.',
  'helpers': [],
  'pending': [{'text': 'Agree a fix in Solutions first.'}, {'text': 'Find out where bills, claims and payments are kept today.'}],
  'actions': {'go': {'detail': 'Agree a fix first', 'say': 'Take me to Solutions to agree a fix'},
              'add': {'detail': 'Tell Tojo about your systems', 'say': 'Here is how our bills and claims are kept today: '},
              'jump': {'tab': 'Processes', 'detail': 'Fills in once a fix is agreed', 'say': 'Take me to Processes'}},
  'chat': {'text': ['This is Automations. Helpers are planned here once a fix is agreed.'],
           'note': 'A helper follows a fix.', 'points': [],
           'prompts': ['Take me to Solutions', 'What does a helper do?', 'Do we need new software?']},
 },
}

def au_canvas(state):
    d = AU[state]; empty = state == 'empty'
    n = len(STOPS_ROAD)
    stops = ''.join('<span class="rd-s" style="left:%.2f%%"><i></i><b>%s</b></span>' % (j / (n - 1) * 100, e(s)) for j, s in enumerate(STOPS_ROAD))
    tags = ''.join('<span class="rd-tag" style="left:%.2f%%"%s>%d</span>' % (h['at'] / (n - 1) * 100, pt(h.get('pt')), i + 1) for i, h in enumerate(d['helpers']))
    road = '<div class="rd%s" role="img" aria-label="%s"><div class="rd-line"></div>%s%s</div>' % (
        ' is-empty' if empty else '', e('The bill’s road: ' + ', '.join(STOPS_ROAD) + '. ' + '; '.join('%s at %s' % (h['name'], STOPS_ROAD[h['at']]) for h in d['helpers'])), tags, stops)
    cards, desk = [], []
    for i, h in enumerate(d['helpers']):
        k = str(i); first = i == 0
        lamps = ''.join('<span class="au-lp"><i aria-hidden="true"></i>%s</span>' % e(l) for l in LAMPS)
        note = ''.join('<span class="rn-l%s"><span>%s</span><b>%s</b></span>' % (' rn-h' if not v else '', e(a), e(v)) for a, v in h['note'])
        cards.append(('<button class="rd-card %s" type="button"%s%s><span class="rd-ch"><span class="rd-no">%d</span><span class="rd-nm">%s</span></span>'
                      '<span class="rd-at">At: %s · %s</span><span class="rd-does">%s</span><span class="au-lamps">%s</span>'
                      '<span class="rn" aria-label="The note it would send"><span class="rn-k">The note it would send</span>%s</span>%s</button>') % (
            sel_cls(first), sel('rd', k, first), pt(h.get('pt')), i + 1, e(h['name']), e(STOPS_ROAD[h['at']]), e(h['when']), e(h['does']), lamps, note, CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>%s</h4>%s</div><p>%s</p>%s%s</div>') % (
            e(h['name']), chip('c-none', 'Not built yet'), e(h['does']), two('What it reads', h['reads'], 'Who gets the note', h['to']),
            two('When it runs', h['when'], 'What it waits for', 'The fix: ' + h['fix']))
        cards.append(box('rd', k, det, first, 'mob'))
        desk.append(box('rd', k, det, first, 'desk'))
    if empty:
        cards = ['<div class="rd-card is-empty"><span class="rd-no">%d</span><span class="rd-does">Placed on the road once a fix is agreed</span></div>' % n for n in (1, 2, 3)]
    body = road + '<div class="rd-cards%s">%s</div>' % (' is-empty' if empty else '', ''.join(cards)) + ('<div class="rd-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'Each helper hangs at the stop where it acts. Tap a helper to read it.' if not empty else 'Each helper will hang at the stop where it acts'
    return (masthead('Automations', state) + standing(d['claim'], d['deck'], empty)
            + section('The bill’s road', body, 'rd-sec', sub) + pending(d['pending']) + actions(d['actions']))

AU_CSS = r'''
.rd{position:relative;height:118px;margin:0 46px}
.rd-line{position:absolute;left:0;right:0;top:56px;height:10px;background:var(--ink)}
.rd-line::after{content:"";position:absolute;right:-14px;top:-7px;border-left:16px solid var(--ink);border-top:12px solid transparent;border-bottom:12px solid transparent}
.rd-s{position:absolute;top:50px;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:8px;width:84px;text-align:center}
.rd-s i{width:22px;height:22px;background:var(--card);box-shadow:inset 0 0 0 3px var(--ink)}
.rd-s b{font-size:12px;font-weight:600;line-height:1.25}
.rd-tag{position:absolute;top:0;transform:translateX(-50%);width:34px;height:34px;display:flex;align-items:center;justify-content:center;font:400 22px/1 var(--f-d);background:var(--hi);color:var(--ink);box-shadow:0 0 0 2px var(--ink)}
.rd-tag::after{content:"";position:absolute;left:50%;top:34px;height:16px;border-left:3px solid var(--ink)}
.rd.is-empty .rd-line{background:transparent;border-top:2px dashed var(--grey);border-bottom:2px dashed var(--grey)}
.rd.is-empty .rd-line::after{display:none}
.rd.is-empty .rd-s i{box-shadow:inset 0 0 0 2px var(--grey)}
.rd.is-empty .rd-s b{color:var(--mut)}
.rd-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:18px;align-items:start}
.rd-card{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:9px;text-align:left;border:0;background:var(--card);border-top:6px solid var(--ink);padding:14px 16px 16px;color:var(--ink);min-width:0}
.rd-ch{display:flex;align-items:center;gap:10px}
.rd-no{font:400 22px/1 var(--f-d);width:28px;height:28px;display:flex;align-items:center;justify-content:center;background:var(--hi);color:var(--ink)}
.rd-nm{font:400 26px/1 var(--f-d)}
.rd-at{font-size:12px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--mut);line-height:1.4}
.rd-does{font-size:14px;line-height:1.5}
.au-lamps{display:flex;flex-wrap:wrap;gap:4px 12px}
.au-lp{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:600;color:var(--mut)}
.au-lp i{width:10px;height:10px;border-radius:50%;box-shadow:inset 0 0 0 1.5px var(--grey)}
.rn{align-self:stretch;display:flex;flex-direction:column;gap:3px;background:var(--soft);padding:12px 12px 16px;-webkit-mask:var(--zigb);mask:var(--zigb)}
.rn-k{font-size:11px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut);padding-bottom:4px;border-bottom:2px dashed var(--grey);margin-bottom:3px}
.rn-l{display:flex;justify-content:space-between;gap:8px;font-size:12.5px;line-height:1.4}
.rn-l b{font-weight:600;white-space:nowrap;text-align:right}
.rn-h span{font-weight:600}
.rn-l:last-child{border-top:1px solid var(--line);padding-top:3px;margin-top:2px}.rn-l:last-child b{color:var(--hi-text)}
.rd-card .sel-chev{position:absolute;right:16px;top:20px;margin:0}
.rd-card.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey);color:var(--mut)}
.rd-desk{margin-top:16px}
@container lp (max-width:699px){
 .rd{height:auto;margin:0;padding:6px 0 4px 54px}
 .rd-line{left:20px;right:auto;top:4px;bottom:4px;width:8px;height:auto}
 .rd-line::after{display:none}
 .rd-s{position:relative;left:auto !important;top:auto;transform:none;flex-direction:row;width:auto;gap:12px;text-align:left;margin:0 0 18px -44px}
 .rd-s i{flex-shrink:0}
 .rd-s b{font-size:13px}
 .rd-tag{display:none}
 .rd-cards{grid-template-columns:1fr;gap:12px}
 .rd-card{padding:14px 44px 16px 16px}
 .rd-card .sel-chev{display:inline-block}
 .rd-cards .bx-mob{margin:-4px 0 6px}
}
'''

# ==========================================================================================
# PROCESSES · the money rhythm
PR = {
 'filled': {
  'claim': 'A rhythm for the money, and one owner for the gap',
  'deck': 'Nothing is tried yet. Each change waits for its fix to be agreed. We start with a two-month trial.',
  'changes': [
   {'lane': 'Daily', 'name': 'Ten-minute look at the money', 'when': '9 AM, 10 minutes', 'who': 'Revenue Lead, billing head, insurance desk', 'pt': 1,
    'what': 'Every morning the three read the money note: yesterday’s bills, money in and claims turned down, and agree who fixes what today.',
    'why': 'Small slips are caught the next morning, not at the month’s end.'},
   {'lane': 'Weekly', 'name': 'Every turned-down claim reviewed', 'when': 'Friday 3 PM, 45 minutes', 'who': 'Insurance desk, with one doctor', 'pt': 2,
    'what': 'Each claim turned down that week gets a reason and an owner. The same reason twice becomes a change to the checklist.',
    'why': 'Most claims are turned down for the same few reasons. Fixing the reason stops the next one.'},
   {'lane': 'Monthly', 'name': 'Package price review', 'when': 'First Monday, 1 hour', 'who': 'Revenue Lead, accounts, two heads of department',
    'what': 'The packages that cost more than their price last month are repriced, reworked or kept on purpose.',
    'why': 'Costs change every month. Prices set once a year drift into losses.'},
   {'lane': 'Role', 'name': 'A Revenue Lead who owns the gap', 'when': 'Full time, new role', 'who': 'Reports to the chief executive', 'pt': 3,
    'what': 'One person owns the ₹90 lakh gap: runs the daily look, chases the claims, and brings the monthly review.',
    'why': 'Today the gap belongs to everyone, so no one closes it.'},
  ],
  'owners': [
   ('Money in from insurers', 'Insurance desk head', False), ('Money from patients paying themselves', 'Billing head', False),
   ('Package prices', 'Revenue Lead', True), ('Staff', 'HR head', False), ('Medicines and supplies', 'Stores Lead (Supply Chain work)', False),
  ],
  'numbers': [
   {'name': 'Days from leaving to bill sent', 'now': '9', 'plan': '1', 'w': 10},
   {'name': 'Claims turned down, of every 100', 'now': '7', 'plan': '2', 'w': 29},
   {'name': 'Money in the bank within 30 days, of every 100', 'now': '45', 'plan': '80', 'w': 56},
   {'name': 'Left from every 100 rupees', 'now': '13', 'plan': '18', 'w': 72},
  ],
  'pending': [
   {'text': 'Name the Revenue Lead, and who stands in for them.', 'need': 'Needs your choice of person', 'pt': 3},
   {'text': 'Agree the time of the daily look at the money.', 'pt': 1},
   {'text': 'Check that the insurance desk can meet every Friday.', 'pt': 2},
  ],
  'actions': {'go': {'detail': 'Name the Revenue Lead', 'say': 'Let’s name the Revenue Lead'},
              'add': {'detail': 'Tell Tojo about your team', 'say': 'Here is who handles billing and claims today: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Back to where the work stands', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Three changes set a rhythm for the money: daily, weekly and monthly. One new role owns the gap.', 'Nothing is tried yet. A two-month trial comes first.'],
           'pointer': 'Pick a point to add to it, or tap a change in the rhythm.',
           'note': 'A gap with an owner closes.',
           'points': [{'n': 1, 'label': 'The daily look'}, {'n': 2, 'label': 'The Friday claim review'}, {'n': 3, 'label': 'The Revenue Lead'}],
           'prompts': ['Our finance manager could be the Revenue Lead', 'Who should join the daily look?', 'How long does this take each week?']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Changes are pinned on the money rhythm here once a fix is agreed: what happens daily, weekly and monthly, who owns each line, and the numbers we watch.',
  'changes': [], 'owners': [], 'numbers': [],
  'pending': [{'text': 'Agree a fix in Solutions first.'}, {'text': 'Tell Tojo who handles billing and claims today.'}],
  'actions': {'go': {'detail': 'Agree a fix first', 'say': 'Take me to Solutions to agree a fix'},
              'add': {'detail': 'Tell Tojo about your team', 'say': 'Here is who handles billing and claims today: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Every conversation starts here', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['This is Processes. Changes for people are planned here once a fix is agreed.'],
           'note': 'Give the gap an owner.', 'points': [],
           'prompts': ['Take me to Solutions', 'Who usually owns the money?', 'What is a Revenue Lead?']},
 },
}
LANES = ['Daily', 'Weekly', 'Monthly', 'Role']

def pr_canvas(state):
    d = PR[state]; empty = state == 'empty'
    lanes, desk = [], []
    for ln in LANES:
        items = []
        for i, c in enumerate(d['changes']):
            if c['lane'] != ln: continue
            k = str(i); first = i == 0
            items.append('<button class="mr-c %s" type="button"%s%s><span class="mr-when">%s</span><b class="mr-nm">%s</b><span class="mr-who">%s</span>%s</button>' % (
                sel_cls(first), sel('mr', k, first), pt(c.get('pt')), e(c['when']), e(c['name']), e(c['who']), CHEV))
            det = ('<div class="fx-box"><div class="fx-bh"><h4>%s</h4>%s</div><p>%s</p>%s</div>') % (
                e(c['name']), chip('c-none', 'Not tried yet'), e(c['what']), two('Who and when', '%s · %s' % (c['who'], c['when']), 'Why it helps', c['why']))
            items.append(box('mr', k, det, first, 'mob'))
            desk.append(box('mr', k, det, first, 'desk'))
        body = ''.join(items) or '<span class="mr-wait">%s</span>' % ('Fills in once a fix is agreed' if empty else '—')
        lanes.append('<div class="mr-lane"><span class="mr-ln">%s</span><div class="mr-items">%s</div></div>' % (e('New role' if ln == 'Role' else ln), body))
    trial = ('<div class="mr-trial"><b>Trial</b><span>Two months, all wards</span><span class="mr-wk">%s</span></div>' % ''.join('<i>%s</i>' % m for m in ('Month 1', 'Month 2'))) if not empty else ''
    board = '<div class="mr%s">%s%s</div>' % (' is-empty' if empty else '', ''.join(lanes), trial)
    body = board + ('<div class="mr-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'The changes, set in the rhythm they happen. Tap a change.' if not empty else 'The changes, set in their rhythm'
    if d['owners']:
        own = ''.join('<div class="ow-r"><span class="ow-l">%s</span><i aria-hidden="true"></i><span class="ow-o"><b>%s</b>%s</span></div>' % (
            e(l), e(o), chip('c-now', 'New role') if new else '') for l, o, new in d['owners'])
        owners = '<div class="ow"><div class="ow-h" aria-hidden="true"><span>Line of the profit and loss, and who owns it</span></div>%s</div>' % own
        nums = ''.join(('<div class="pv"%s><span class="pv-n">%s<em>%s</em></span>'
                        '<span class="pv-v"><span>Now <b>%s</b></span><i class="pv-ar" aria-hidden="true"></i><span>Plan <b class="pv-p">%s</b></span></span></div>') % (
            pt(n.get('pt')), e(n['name']), 'Lower is better' if float(n['plan']) < float(n['now']) else 'Higher is better', e(n['now']), e(n['plan'])) for n in d['numbers'])
        numsec = '<div class="pvs">%s</div><p class="fx-hint">Now: Example only. Plan: Tojo’s guess, to agree with you. </p>' % nums
        extra = (section('Who owns each line', owners, 'ow-sec', 'Every line of the profit and loss has one owner')
                 + section('The numbers we watch: plan against now', numsec, 'pv-sec', 'Read every morning in the ten-minute look'))
    else:
        extra = section('Who owns each line', '<p class="fx-empty">Owners are written here once a change is agreed.</p>', 'ow-sec')
    return (masthead('Processes', state) + standing(d['claim'], d['deck'], empty)
            + section('The money rhythm', body, 'mr-sec', sub) + extra + pending(d['pending']) + actions(d['actions']))

PR_CSS = r'''
.mr{background:var(--card);border-top:6px solid var(--ink)}
.mr-lane{display:grid;grid-template-columns:120px minmax(0,1fr);border-bottom:1px solid var(--line)}
.mr-ln{font:400 24px/1 var(--f-d);padding:12px 14px;background:var(--soft);color:var(--ink)}
.mr-items{display:flex;flex-wrap:wrap;gap:8px;padding:7px 12px;align-items:flex-start}
.mr-c{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:3px;text-align:left;border:0;border-left:5px solid var(--ink);background:var(--soft);padding:7px 40px 8px 12px;color:var(--ink);min-width:0;flex:1 1 100%}
.mr-when{font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.mr-nm{font:400 24px/1 var(--f-d)}
.mr-who{font-size:13px;color:var(--mut)}
.mr-c .sel-chev{position:absolute;right:14px;top:14px;margin:0}
.mr-wait{font-size:13.5px;color:var(--mut);padding:8px 2px}
.mr-trial{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:7px 14px;border-top:3px double var(--ink);font-size:13.5px}
.mr-trial b{font:400 22px/1 var(--f-d)}
.mr-wk{display:flex;gap:4px;margin-left:auto}
.mr-wk i{font-style:normal;font-size:12px;font-weight:600;padding:3px 10px;box-shadow:inset 0 0 0 1.5px var(--grey);color:var(--mut)}
.mr.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey)}
.mr.is-empty .mr-ln{background:transparent;color:var(--mut)}
.mr-desk{margin-top:14px}
.ow{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));column-gap:16px;align-items:start;background:var(--card);border-top:6px solid var(--ink);padding:4px 16px 6px}
.ow-h{grid-column:1/-1}
.ow-h{display:flex;justify-content:space-between;padding:8px 0;border-bottom:3px double var(--ink)}
.ow-h span{font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.ow-r{display:flex;flex-direction:column;align-items:flex-start;gap:4px;padding:9px 0;border-bottom:1px solid var(--line);font-size:13px;color:var(--mut)}
.ow-r i{display:none}
.ow-o{justify-content:flex-start !important;text-align:left !important;color:var(--ink);font-size:14px}
.ow-l{min-width:0}
.ow-r i{flex:1 1 20px;min-width:14px;border-bottom:2px dotted var(--grey);transform:translateY(-4px)}
.ow-o{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end;text-align:right}
.ow-o b{font-weight:600}
.pvs{display:grid;grid-template-columns:1fr 1fr;column-gap:28px;background:var(--card);border-top:6px solid var(--ink);padding:4px 16px 8px}
.pv{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:12px;padding:7px 0;border-bottom:1px solid var(--line)}
.pv-n em{display:block;font-style:normal;font-size:12px;font-weight:600;color:var(--mut);margin-top:2px}
.pv-v{align-items:baseline}
.pv-ar{width:22px;height:2px;background:var(--ink);position:relative;align-self:center}
.pv-ar::after{content:"";position:absolute;right:-1px;top:-4px;border-left:7px solid var(--ink);border-top:5px solid transparent;border-bottom:5px solid transparent}
.pv-n{font-size:14px;font-weight:600;line-height:1.35}
.pv-bar{position:relative;display:block;height:12px;background:var(--soft)}
.pv-bar i{display:block;height:100%;background:var(--hi)}
.pv-bar em{position:absolute;top:-4px;bottom:-4px;border-left:3px solid var(--ink)}
.pv-v{display:flex;justify-content:flex-end;gap:12px}
.pv-v span{font-size:12px;font-weight:600;color:var(--mut)}
.pv-v b{font:400 24px/1 var(--f-d);color:var(--ink);margin-left:4px}
.pv-v b.pv-p{color:var(--hi-text)}
@container lp (max-width:699px){
 .mr-lane{grid-template-columns:1fr}
 .mr-ln{padding:10px 12px;font-size:22px}
 .mr-items{flex-direction:column;align-items:stretch;flex-wrap:nowrap;padding:10px}
 .mr-c{flex:0 0 auto;width:100%}
 .mr-items .bx-mob{width:100%}
 .mr-c .sel-chev{display:inline-block}
 .mr-items .bx-mob{margin:-4px 0 4px}
 .mr-wk{margin-left:0}
 .ow{padding:4px 12px 6px;grid-template-columns:1fr}
 .ow-r{flex-direction:column;align-items:flex-start;gap:2px}
 .ow-r i{display:none}
 .ow-o{justify-content:flex-start;text-align:left}
 .pvs{padding:4px 12px 8px;grid-template-columns:1fr}
 .pv{grid-template-columns:1fr;gap:6px}
 .pv-v{justify-content:flex-start}
}
'''

# ==========================================================================================
PAGES = {
 'home': (None, None, 'Home', 'The cheque book (approved)'),
 'diagnosis': ('Diagnosis', (dg_canvas, DG_CSS, DG), 'Diagnosis', 'The bank statement'),
 'solutions': ('Solutions', (so_canvas, SO_CSS, SO), 'Solutions', 'The payback sheet'),
 'automations': ('Automations', (au_canvas, AU_CSS, AU), 'Automations', 'The bill’s road'),
 'processes': ('Processes', (pr_canvas, PR_CSS, PR), 'Processes', 'The money rhythm'),
}
ABOUT = {
 'home': ('<b>Home · The cheque book.</b> Approved as sample A. The month’s profit and loss on ledger paper; each part of the work a cheque made out for what it brings back. '
          '<em>Colours: banknote green, bottle green, marigold. The rail now carries each place’s own colour.</em>'),
 'diagnosis': ('<b>Diagnosis · The bank statement.</b> ₹1,000 of bills followed to the bank: each step a statement line with the day, what was lost and the balance left, '
               'its line opening beside the statement. Below it, the ₹90 lakh gap split four ways on a ring. <em>Colours: peach, deep plum, electric blue.</em>'),
 'solutions': ('<b>Solutions · The payback sheet.</b> One ruled entry per fix: its four stops, what it costs to start, what it brings back each month, and a twelve-month strip '
               'that marks the month it pays for itself. A double-ruled total. Each entry opens to its by-hand and automatic versions. <em>Colours: pale olive, deep teal, tangerine.</em>'),
 'automations': ('<b>Automations · The bill’s road.</b> The money’s journey from the patient leaving to the next morning, each helper hung at the stop where it acts; '
                 'one card per helper with its lamps and the note it would send. <em>Colours: ice blue, navy, hot pink.</em>'),
 'processes': ('<b>Processes · The money rhythm.</b> Daily, weekly and monthly lanes with the changes set in them, the new role, and a two-month trial; who owns each line '
               'of the profit and loss; the numbers we watch, plan against now. <em>Colours: orchid pink, aubergine, sea green.</em>'),
}

def build():
    os.makedirs(OUT, exist_ok=True)
    pages, words = {}, []
    base = L2.V_SHARED_CSS + L3.PLACE_CSS
    for k, (place, spec, label, title) in PAGES.items():
        t = THEMES[k]
        for st in ('filled', 'empty'):
            if spec is None:
                canvas, css, chat, cls = H.a_canvas(st), base + H.A_CSS, H.DATA[st]['chat'], 'rv rv-home rv-a'
            else:
                fn, pcss, data = spec
                canvas, css, chat, cls = fn(st), base + pcss, data[st]['chat'], 'rv rv-%s' % k
            for v in ('desktop', 'mobile'):
                h = C.page(SK, t, place, canvas, css, chat, v, 'Revenue & EBITDA · %s' % label, cls)
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(OUT, 'rev-%s.%s.%s.html' % (k, v, st)), 'w', encoding='utf-8').write(h)
            text = re.sub(r'<[^>]+>', ' ', canvas) + ' ' + json.dumps(chat, ensure_ascii=False)
            words += [(k, st, w) for w in C.plain_check(text.replace('EBITDA', ''))]
    return pages, words

def review(pages):
    tpl = open(os.path.join(H.SCP, 'review_template.html'), encoding='utf-8').read()
    tpl = tpl.replace('Supply Chain and Procurement · the home page in three looks', 'Revenue & EBITDA · the five landing pages')
    tpl = tpl.replace('Supply Chain and Procurement · three looks for the Financial domain', 'Revenue & EBITDA · the five landing pages')
    tpl = re.sub(r'<p class="rv-intro">.*?</p>', '<p class="rv-intro">The tool’s home page (the cheque book, approved) and its four place pages, in the Financial look: '
                 'the Virevo type unchanged, the flat frame, ledger and receipt paper. Each place has its own colours and its own money drawing. '
                 'Scroll inside each view; every page opens with its first element raised and its box open. On the phone, each box opens right under the element you tap.</p>', tpl, flags=re.S)
    tpl = tpl.replace("cur={s:'a',st:'filled'}", "cur={s:'home',st:'filled'}")
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>%s</b><span>%s</span><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 4px %s"></i></button>' % (
        k, 'true' if k == 'home' else 'false', e(v[2]), e(v[3]), THEMES[k]['ground'], THEMES[k]['ink'], THEMES[k]['hi']) for k, v in PAGES.items())
    return (tpl.replace('@@PICKS@@', picks).replace('@@ABOUT@@', json.dumps(ABOUT, ensure_ascii=False))
               .replace('@@DATA@@', json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')))

if __name__ == '__main__':
    pages, words = build()
    if words:
        print('PLAIN ENGLISH:', words)
    rv = os.path.join(OUT, 'revenue-ebitda-landing-pages.html')
    open(rv, 'w', encoding='utf-8').write(review(pages))
    print('built', rv, os.path.getsize(rv))
