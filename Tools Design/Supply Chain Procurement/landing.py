"""
Supply Chain and Procurement: the tool's home page, in three candidate looks for the Financial
domain (8 Oct 2026, for review).

Same five zones as every landing page, in the same order (06 §11.2): masthead with stamp and
Refresh now, where this stands, the drawing, what Tojo still has to do, the three buttons.
Same behaviour as Bed Management v3 and OPD: chat one screen tall with its own scroll, the first
element raised with its box open, on a phone each box opens right under its element, pickable
items stacked. The words are the same in all three; only the identity changes.

  A  The ledger         the month's account (a statement with a double-ruled total) and the
                        accounts book: one ruled line per part of the work, ticks as entries.
  B  The till roll      the month's till receipt, and four slips clipped to a rail, one per part,
                        each stamped with where it stands.
  C  The annual report  where the money goes (one bar split four ways), and the work register:
                        one bar of every step, cut into the four parts, with big figures under it.

Example figures are made up for an example 250-bed hospital and marked Example only or Tojo's
guess: about ₹3 crore of supplies bought a month, about ₹20 lakh of it lost.

Run:  python3 landing.py   ->  out/landing/
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sc_common as C
from sc_common import e, ico, ICONS, CHEV, sel, sel_cls, box, pt, tag, say_btn, standing, section, pending, actions, STAMP, MARK
from skins import SKINS

OUT = os.path.join(HERE, 'out', 'landing')
KICK = 'Virevo · ' + C.HOSPITAL

# ==========================================================================================
# The words (one set for all three looks)
STEP = {'done': 'Done', 'now': 'Now', 'later': 'Still to do', 'none': 'Not started'}
STATUS = {'now': 'In use now', 'started': 'Taking shape', 'none': 'Not started', 'empty': 'Nothing yet'}
DATA = {
 'filled': {
  'claim': 'We pay more than we need to, and some of what we buy is never billed',
  'deck': 'Diagnosis is two steps in. Three fixes are on the table. Nothing is switched on or changed yet.',
  'money': {'lost': '₹20 lakh', 'lost_l': 'lost each month', 'tag': 'example',
            'share': 'About 7 rupees of every 100 rupees spent on supplies',
            'spend': 'About ₹3 crore of supplies bought each month',
            'lines': [('Paid above the best price', '₹8 lakh', 40), ('Rushed buys from local shops', '₹5 lakh', 25),
                      ('Used on wards, never billed to the patient', '₹4 lakh', 20), ('Expired on the shelf', '₹3 lakh', 15)],
            'saved': 'None yet'},
  'places': [
   {'name': 'Diagnosis', 'status': 'now', 'pt': 1, 'head': 'About 7 of every 100 rupees spent on supplies is lost.',
    'fig': ('₹20 lakh', 'lost each month', 'example'), 'unit': 'steps done',
    'steps': [['Put a number on the loss', 'done'], ['Follow one item from the ward’s request to the patient’s bill', 'done'],
              ['Compare what we paid for our top 50 items', 'now'], ['Count what expires on the shelf', 'later'], ['Name the main cause', 'later']]},
   {'name': 'Solutions', 'status': 'started', 'pt': 3, 'head': 'Three fixes on the table. One is taking shape.',
    'fig': ('About half', 'of the loss could come back', 'guess'), 'unit': 'fixes agreed',
    'steps': [['One agreed price per item, from fewer suppliers', 'now'], ['A lowest level for each item, so rushed buys stop', 'later'],
              ['Bill each item at the bedside when it is used', 'later']]},
   {'name': 'Automations', 'status': 'none', 'head': 'Three helpers wait for the fixes to be agreed.', 'fig': None, 'unit': 'switched on',
    'steps': [['Warns when a bill is above the agreed price', 'none'], ['Orders again when stock falls to its lowest level', 'none'],
              ['Matches what wards used with what patients were billed', 'none']]},
   {'name': 'Processes', 'status': 'none', 'head': 'Three changes and one new role wait for a trial.', 'fig': None, 'unit': 'tried',
    'steps': [['One buying meeting each week', 'none'], ['Ward shelves checked every Monday', 'none'],
              ['A Stores Lead who signs off every rushed buy', 'none'], ['A ten-minute look at the numbers each morning', 'none']]},
  ],
  'pending': [
   {'text': 'List the 50 items we spend most on, with what we paid each time.', 'need': 'Needs last quarter’s supplier bills', 'pt': 2},
   {'text': 'Find out who can approve a rushed buy, and how often it happens.', 'pt': 4},
   {'text': 'Check what is thrown away each month because it expired.'},
   {'text': 'Match what the operating theatre used last week with what patients were billed.', 'need': 'Needs last week’s theatre list'},
  ],
  'actions': {'go': {'detail': 'Compare what we paid for our top 50 items', 'say': 'Let’s compare what we paid for our top 50 items'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about how we buy supplies: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Pick up where you left off', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Here is where the Supply Chain and Procurement work stands, across all four parts.',
                    'Diagnosis is two steps in. We buy the same items at different prices, and some of what wards use never reaches the patient’s bill.',
                    'Two things would sharpen this: the bills for our top 50 items, and who approves rushed buys.'],
           'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
           'note': 'No single big leak. Small gaps at every step.',
           'points': [{'n': 1, 'label': 'Money lost each month'}, {'n': 2, 'label': 'Prices of our top 50 items'},
                      {'n': 3, 'label': 'The three fixes'}, {'n': 4, 'label': 'Who approves rushed buys'}],
           'prompts': ['Let’s compare what we paid for our top 50 items', 'Why do we pay different prices?', 'Show me the three fixes']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Start with Diagnosis. Tojo follows one item with you, from the ward asking for it to the patient’s bill, and fills this page as you go.',
  'money': None,
  'places': [
   {'name': 'Diagnosis', 'status': 'empty', 'head': 'Fills in as you follow one item with Tojo.', 'fig': None, 'steps': []},
   {'name': 'Solutions', 'status': 'empty', 'head': 'Fills in once the main cause is named.', 'fig': None, 'steps': []},
   {'name': 'Automations', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': []},
   {'name': 'Processes', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': []},
  ],
  'pending': [
   {'text': 'Follow one item, from the ward asking for it to the patient’s bill.'},
   {'text': 'Put a number on what is lost each month.', 'need': 'Needs a month of supplier bills'},
   {'text': 'Find out who decides what to buy, and from whom.'},
  ],
  'actions': {'go': {'detail': 'Follow one item with Tojo', 'say': 'Let’s follow one item'},
              'add': {'detail': 'Share a bill list or a stock report', 'say': 'Here is what I already know about how we buy supplies: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Every conversation starts here', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Welcome to Supply Chain and Procurement. This page fills in as we talk.',
                    'We start by following one item: a ward asks for it, someone buys it, and we see whether it reaches the patient’s bill.'],
           'note': 'Follow one item. The money follows.', 'points': [],
           'prompts': ['Let’s follow one item', 'What should I bring?', 'How does this work?']},
 },
}

def counts(p):
    done = sum(1 for _, s in p['steps'] if s == 'done')
    return done, len(p['steps'])

def prog(p):
    d, n = counts(p)
    return '%d of %d %s' % (d, n, p['unit']) if n else ''

def place_detail(p, cls):
    """The box for one part of the work: its words are the same in every look; the skin dresses it."""
    fig = ''
    if p['fig']:
        v, l, t = p['fig']
        fig = '<div class="%s-fig"><span class="%s-fv">%s</span><span>%s</span>%s</div>' % (cls, cls, e(v), e(l), tag(t))
    steps = '<ol class="%s-steps">%s</ol>' % (cls, ''.join(
        '<li class="s-%s"><i class="mk mk-%s" aria-hidden="true"></i><span class="%s-sn">%s</span><span class="%s-ss">%s</span></li>' % (
            s, s, cls, e(t), cls, e(STEP[s])) for t, s in p['steps']))
    return ('<div class="%s-box"><div class="%s-bh"><h4>%s</h4><span class="%s-st s-%s">%s</span></div><p>%s</p>%s%s%s</div>') % (
        cls, cls, e(p['name']), cls, p['status'], e(STATUS[p['status']]), e(p['head']), fig, steps,
        say_btn('Open ' + p['name'], 'Take me to ' + p['name']))

# marks for a step: done, now, still to do, not started (each look draws them its own way)
def mark(s):
    return '<i class="mk mk-%s"><span class="sr">%s</span></i>' % (s, e(STEP[s]))

# ==========================================================================================
# A · THE LEDGER
def a_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    m = d['money']
    if m:
        lines = ''.join('<div class="la-l"><span>%s</span><i aria-hidden="true"></i><b>%s</b></div>' % (e(a), e(v)) for a, v, _ in m['lines'])
        acct = ('<aside class="la-acct"%s><div class="la-ah"><span class="la-at">The month’s account</span>%s</div>'
                '<p class="la-spend">%s</p><div class="la-lines">%s</div>'
                '<div class="la-tot"><span>Lost in all</span><b>%s</b></div><p class="la-share">%s</p>'
                '<div class="la-saved"><span>Saved so far</span><b>%s</b></div></aside>') % (
            pt(1), tag(m['tag']), e(m['spend']), lines, e(m['lost']), e(m['share']), e(m['saved']))
    else:
        acct = '<aside class="la-acct is-empty"><span class="la-at">The month’s account</span><p>Fills in once a month of supplier bills is in.</p></aside>'
    top = '<div class="la-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), acct)

    rows, desk = [], []
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        marks = ''.join(mark(s) for _, s in p['steps'])
        inner = ('<span class="la-no">%d</span>'
                 '<span class="la-part"><span class="la-pn">%s%s</span><span class="la-hl">%s</span></span>'
                 '<span class="la-ent"><span class="la-marks">%s</span><span class="la-prog">%s</span></span>'
                 '<span class="la-sat"><span class="la-st s-%s">%s</span></span>%s') % (
            i + 1, ico(ICONS[p['name']], 'currentColor', 18), e(p['name']), e(p['head']), marks or '<span class="la-blank"></span>', e(prog(p)),
            p['status'], e(STATUS[p['status']]), '' if empty else CHEV)
        if empty:
            rows.append('<div class="la-row is-empty">%s</div>' % inner); continue
        rows.append('<button class="la-row %s" type="button" data-s="%s"%s%s>%s</button>' % (sel_cls(first), p['status'], sel('la', k, first), pt(p.get('pt')), inner))
        det = place_detail(p, 'la')
        rows.append(box('la', k, det, first, 'mob'))
        desk.append(box('la', k, det, first, 'desk'))
    head = '<div class="la-head" aria-hidden="true"><span>No.</span><span>Part of the work</span><span>Entries</span><span>Stands at</span></div>'
    foot = ('<div class="la-foot"><span>Parts finished so far</span><b>%s</b></div>') % ('None of 4' if not empty else '—')
    book = '<div class="la-book%s">%s<div class="la-rows">%s</div>%s</div>' % (' is-empty' if empty else '', head, ''.join(rows), foot)
    key = ('<div class="la-key" aria-hidden="true"><span>%s Done</span><span>%s Now</span><span>%s Still to do</span><span>%s Not started</span></div>' % (
        mark('done'), mark('now'), mark('later'), mark('none'))) if not empty else ''
    sub = 'One line in the book for each part of the work. Tap a line to read its entries.' if not empty else 'One line in the book for each part of the work'
    emb = '<span class="bm-emb">%s</span>' % ico(MARK, 'var(--hi)', 28)
    return (C.masthead(KICK, emb, STAMP[state]) + top
            + section('Where each part of the work stands', book + key + ('<div class="la-desk">%s</div>' % ''.join(desk) if desk else ''), 'la-sec', sub)
            + pending(d['pending']) + actions(d['actions']))

A_PAGE_CSS = r'''
.la-top{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:36px;align-items:start;margin:26px 0 4px}
.la-top .bm-stand{margin:4px 0 0}
.la-acct{background:var(--card);border:1px solid var(--ink);padding:14px 20px 16px;display:flex;flex-direction:column;gap:5px;position:relative;
 background-image:repeating-linear-gradient(transparent 0 25px,var(--rule) 25px 26px);box-shadow:5px 5px 0 -1px var(--card),5px 5px 0 0 var(--line)}
.la-ah{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;border-bottom:3px double var(--ink);padding-bottom:6px}
.la-at{font:700 19px/1.2 var(--f-d)}
.la-spend{font-size:13.5px;font-style:italic;color:var(--mut)}
.la-lines{display:flex;flex-direction:column}
.la-l{display:flex;align-items:baseline;gap:8px;font-size:14.5px;line-height:26px}
.la-l span{min-width:0}
.la-l i{flex:1 1 20px;border-bottom:1.5px dotted var(--grey);transform:translateY(-5px);min-width:14px}
.la-l b{font:600 15px var(--f-b);white-space:nowrap;padding-left:10px;border-left:1px solid var(--hi);min-width:84px;text-align:right}
.la-tot{display:flex;justify-content:space-between;align-items:baseline;gap:10px;border-top:1px solid var(--ink);margin-top:4px;padding-top:6px}
.la-tot span{font-size:14.5px;font-weight:600}
.la-tot b{font:700 30px/1.05 var(--f-d);color:var(--hi-text);border-bottom:4px double var(--hi-text);padding-bottom:1px}
.la-share{font-size:13.5px;color:var(--mut);font-style:italic}
.la-saved{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--rule);padding-top:6px;font-size:14px}
.la-saved b{font-style:italic;font-weight:600}
.la-acct.is-empty{background:transparent;background-image:none;border:1px dashed var(--grey);box-shadow:none;color:var(--mut)}
.la-acct.is-empty p{font-size:14.5px;font-style:italic}
/* the book */
.la-book{position:relative;background:var(--card);border:1px solid var(--ink);border-left:14px solid var(--ink);box-shadow:4px 4px 0 -1px var(--card),4px 4px 0 0 var(--line),8px 8px 0 -1px var(--card),8px 8px 0 0 var(--line)}
.la-book::before{content:"";position:absolute;left:-9px;top:10px;bottom:10px;border-left:2px dashed rgba(255,255,255,.45)}
.la-head,.la-row{display:grid;grid-template-columns:52px minmax(0,1fr) 210px 150px;align-items:stretch}
.la-head{border-bottom:3px double var(--ink)}
.la-head span{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);padding:10px 12px}
.la-head span:nth-child(3),.la-head span:nth-child(4){border-left:1px solid var(--hi)}
.la-row{width:100%;border:0;border-bottom:1px solid var(--rule);background:transparent;text-align:left;padding:0;color:var(--ink)}
.lp .la-row.is-up{background:var(--soft)}
.la-no{font:italic 400 22px var(--f-d);color:var(--mut);padding:11px 12px;text-align:center}
.la-part{display:flex;flex-direction:column;gap:3px;padding:11px 12px;min-width:0}
.la-pn{display:inline-flex;align-items:center;gap:8px;font:700 22px/1.1 var(--f-d)}
.la-pn svg{flex-shrink:0;color:var(--mut)}
.la-hl{font-size:14.5px;line-height:1.45}
.la-ent{display:flex;flex-direction:column;justify-content:center;gap:5px;padding:10px 14px;border-left:1px solid var(--hi)}
.la-marks{display:flex;gap:6px;flex-wrap:wrap}
.la-prog{font-size:13px;font-style:italic;color:var(--mut)}
.la-sat{display:flex;align-items:center;padding:10px 12px;border-left:1px solid var(--hi);gap:8px}
.la-st{font-size:13px;font-weight:600;font-style:italic;padding:3px 10px;border:1px solid var(--ink);white-space:nowrap}
.la-st.s-now{background:var(--hi);border-color:var(--hi);color:#fff;font-style:normal}
.la-st.s-started{border-style:solid}
.la-st.s-none,.la-st.s-empty{border:1px dashed var(--grey);color:var(--mut)}
.la-row .sel-chev{display:none}
.la-row.is-empty .la-pn,.la-row.is-empty .la-hl,.la-row[data-s=none] .la-pn,.la-row[data-s=none] .la-hl{color:var(--mut)}
.la-blank{display:block;height:2px;width:70%;border-bottom:1px dashed var(--grey)}
.la-foot{display:flex;justify-content:space-between;align-items:baseline;padding:10px 14px 10px 64px;border-top:3px double var(--ink);font-size:14px}
.la-foot b{font:italic 600 15px var(--f-b)}
/* marks */
.mk{display:inline-block;width:18px;height:18px;position:relative;flex-shrink:0}
.mk-done::before{content:"";position:absolute;left:5px;top:1px;width:6px;height:11px;border-right:2.5px solid var(--ink);border-bottom:2.5px solid var(--ink);transform:rotate(40deg)}
.mk-now{border-radius:50%;background:var(--hi);box-shadow:0 0 0 2px var(--card),0 0 0 3px var(--hi)}
.mk-later::before{content:"";position:absolute;left:3px;right:3px;top:8px;border-top:2px solid var(--ink)}
.mk-none::before{content:"";position:absolute;left:2px;right:2px;top:8px;border-top:2px dotted var(--grey)}
.la-key{display:flex;flex-wrap:wrap;gap:8px 24px;margin-top:16px;font-size:13px;color:var(--mut);font-style:italic}
.la-key span{display:inline-flex;align-items:center;gap:8px}
/* the box */
.la-desk{margin-top:18px}
.la-box{display:flex;flex-direction:column;gap:10px;padding:16px 22px 18px;background:var(--card);border:1px solid var(--ink);border-top:3px double var(--ink)}
.la-bh{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.la-box h4{font:700 24px/1.1 var(--f-d)}
.la-box>p{font-size:15px;line-height:1.55}
.la-fig{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;font-size:14px;color:var(--mut);font-style:italic}
.la-fv{font:700 26px/1 var(--f-d);color:var(--hi-text);font-style:normal}
.la-steps{display:flex;flex-direction:column;counter-reset:st}
.la-steps li{display:flex;align-items:baseline;gap:10px;font-size:14.5px;line-height:1.45;padding:5px 0;border-bottom:1px solid var(--rule)}
.la-steps li .mk{transform:translateY(3px)}
.la-sn{flex:0 1 auto;min-width:0}
.la-ss{margin-left:auto;padding-left:14px;font-style:italic;font-size:13.5px;color:var(--mut);white-space:nowrap}
.la-steps li.s-now .la-ss{color:var(--hi-text);font-weight:600}
.la-steps li.s-now .la-sn{font-weight:600}
.la-box .bm-open{align-self:flex-start}
.skin-a .bx-mob{background:transparent;border:0}
.skin-a .bx-mob::before{background:var(--card);border-left:1px solid var(--ink);border-top:1px solid var(--ink);z-index:1;top:-7px}
.skin-a .bx-mob .la-box{padding:14px 16px 16px}
.skin-a p,.skin-a li,.skin-a b,.skin-a span{overflow-wrap:anywhere}
@container lp (max-width:699px){
 .la-top{grid-template-columns:1fr;gap:20px;margin:22px 0 4px}
 .la-acct{padding:14px 14px 16px}
 .la-l{font-size:14px;line-height:1.4;padding:5px 0}
 .la-l b{min-width:70px;font-size:14.5px}
 .la-book{border-left-width:10px}
 .la-book::before{left:-7px}
 .la-head{display:none}
 .la-row{grid-template-columns:34px minmax(0,1fr) 22px;grid-template-areas:"no part chev" "no ent ent" "no sat sat";padding:4px 0 10px}
 .la-no{grid-area:no;padding:12px 4px 0;font-size:19px}
 .la-part{grid-area:part;padding:12px 6px 4px 6px}
 .la-ent{grid-area:ent;border-left:0;padding:4px 6px;flex-direction:row;align-items:center;flex-wrap:wrap;gap:10px}
 .la-sat{grid-area:sat;border-left:0;padding:4px 6px}
 .la-row .sel-chev{display:inline-block;grid-area:chev;margin:20px 0 0}
 .la-pn{font-size:21px}
 .la-hl{font-size:14px}
 .la-rows .bx-mob{margin:2px 8px 12px}
 .la-foot{padding:10px 12px;font-size:14px}
 .la-box h4{font-size:21px}
 .la-steps li{display:grid;grid-template-columns:18px minmax(0,1fr);column-gap:10px;font-size:14px}
 .la-ss{grid-column:2;margin:2px 0 0;padding:0;justify-self:start}
 .la-ent{justify-content:flex-start}
}
'''

# ==========================================================================================
# B · THE TILL ROLL
def b_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    m = d['money']
    if m:
        lines = ''.join('<div class="tb-l"><span>%s</span><i aria-hidden="true"></i><b>%s</b></div>' % (e(a), e(v)) for a, v, _ in m['lines'])
        rc = ('<aside class="tb-rcpt"%s><div class="tb-rh"><b>This month</b>%s</div><p class="tb-spend">%s</p><div class="tb-dash" aria-hidden="true"></div>'
              '<div class="tb-lines">%s</div><div class="tb-dash" aria-hidden="true"></div>'
              '<div class="tb-tot"><span>Total lost</span><b>%s</b></div><p class="tb-share">%s</p><div class="tb-dash" aria-hidden="true"></div>'
              '<div class="tb-saved"><span>Saved so far</span><b>%s</b></div><div class="tb-bar" aria-hidden="true"></div></aside>') % (
            pt(1), tag(m['tag']), e(m['spend']), lines, e(m['lost']), e(m['share']), e(m['saved']))
    else:
        rc = '<aside class="tb-rcpt is-empty"><div class="tb-rh"><b>This month</b></div><p>Prints once a month of supplier bills is in.</p></aside>'
    top = '<div class="tb-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), rc)

    slips, desk = [], []
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        marks = ''.join(mark(s) for _, s in p['steps'])
        dn, n = counts(p)
        inner = ('<span class="tb-clip" aria-hidden="true"></span><span class="tb-sh"><span class="tb-no">%02d</span>%s<span class="tb-pn">%s</span></span>'
                 '<span class="tb-cut" aria-hidden="true"></span><span class="tb-hl">%s</span>'
                 '<span class="tb-marks">%s</span><span class="tb-prog">%s</span>'
                 '<span class="tb-stamp s-%s">%s</span>%s') % (
            i + 1, ico(ICONS[p['name']], 'currentColor', 17), e(p['name']), e(p['head']), marks, e(prog(p)) or '&nbsp;',
            p['status'], e(STATUS[p['status']]), '' if empty else CHEV)
        if empty:
            slips.append('<div class="tb-slip is-empty" data-s="empty">%s</div>' % inner); continue
        slips.append('<button class="tb-slip %s" type="button" data-s="%s"%s%s>%s</button>' % (sel_cls(first), p['status'], sel('tb', k, first), pt(p.get('pt')), inner))
        det = place_detail(p, 'tb')
        slips.append(box('tb', k, det, first, 'mob'))
        desk.append(box('tb', k, det, first, 'desk'))
    rail = '<div class="tb-rail%s"><div class="tb-bar2" aria-hidden="true"></div><div class="tb-slips">%s</div></div>' % (' is-empty' if empty else '', ''.join(slips))
    key = ('<div class="tb-key" aria-hidden="true"><span>%s Done</span><span>%s Now</span><span>%s Still to do</span><span>%s Not started</span></div>' % (
        mark('done'), mark('now'), mark('later'), mark('none'))) if not empty else ''
    sub = 'One slip for each part of the work. Tap a slip to read it.' if not empty else 'One slip for each part of the work'
    emb = '<span class="bm-emb">%s</span>' % ico(MARK, 'var(--card)', 28)
    return (C.masthead(KICK, emb, STAMP[state]) + top
            + section('Where each part of the work stands', rail + key + ('<div class="tb-desk">%s</div>' % ''.join(desk) if desk else ''), 'tb-sec', sub)
            + pending(d['pending']) + actions(d['actions']))

B_PAGE_CSS = r'''
.tb-top{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:36px;align-items:start;margin:26px 0 4px}
.tb-top .bm-stand{margin:4px 0 0}
.tb-rcpt{position:relative;background:var(--card);padding:22px 20px 26px;display:flex;flex-direction:column;gap:8px;-webkit-mask:var(--zig);mask:var(--zig);
 font-family:var(--f-d);transform:rotate(1deg);filter:drop-shadow(0 8px 10px rgba(0,0,0,.18))}
.tb-rh{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.tb-rh b{font:700 15px var(--f-d);text-transform:uppercase;letter-spacing:.06em}
.tb-spend,.tb-share{font:400 12.5px/1.5 var(--f-d);color:var(--mut)}
.tb-dash{border-top:2px dashed var(--ink);opacity:.5}
.tb-lines{display:flex;flex-direction:column;gap:5px}
.tb-l{display:flex;align-items:baseline;gap:6px;font:400 13px/1.4 var(--f-d)}
.tb-l span{min-width:0}
.tb-l i{flex:1 1 16px;min-width:12px;border-bottom:2px dotted var(--grey);transform:translateY(-4px)}
.tb-l b{font-weight:700;white-space:nowrap}
.tb-tot{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.tb-tot span{font:700 13px var(--f-d);text-transform:uppercase}
.tb-tot b{font:700 30px/1 var(--f-d);color:var(--hi-text);letter-spacing:-.03em}
.tb-saved{display:flex;justify-content:space-between;font:700 13px var(--f-d);text-transform:uppercase}
.tb-saved b{color:var(--mut)}
.tb-bar{height:34px;margin-top:6px;background:repeating-linear-gradient(90deg,var(--ink) 0 2px,transparent 2px 4px,var(--ink) 4px 7px,transparent 7px 9px,var(--ink) 9px 10px,transparent 10px 13px);opacity:.85}
.tb-rcpt.is-empty{background:transparent;-webkit-mask:none;mask:none;filter:none;transform:none;border:2px dashed var(--grey);color:var(--mut)}
.tb-rcpt.is-empty p{font:400 13px/1.5 var(--f-d)}
/* the rail and the slips */
.tb-rail{position:relative;padding-top:10px}
.tb-bar2{position:absolute;left:-8px;right:-8px;top:0;height:16px;background:linear-gradient(var(--ink),#4a4655);border-radius:3px;box-shadow:0 3px 0 rgba(0,0,0,.15)}
.tb-slips{position:relative;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;align-items:start}
.tb-slip{position:relative;display:flex;flex-direction:column;gap:9px;align-items:stretch;text-align:left;border:0;background:var(--card);color:var(--ink);
 padding:22px 16px 22px;-webkit-mask:var(--zigb);mask:var(--zigb);min-width:0;filter:drop-shadow(0 6px 6px rgba(0,0,0,.14))}
.tb-clip{position:absolute;left:50%;top:-2px;width:40px;height:16px;margin-left:-20px;background:#8f8a99;border-radius:0 0 6px 6px;box-shadow:inset 0 -3px 0 rgba(0,0,0,.25)}
.tb-sh{display:flex;align-items:center;gap:7px;min-width:0}
.tb-no{font:400 12px var(--f-d);color:var(--mut)}
.tb-sh svg{flex-shrink:0}
.tb-pn{font:700 16px/1.1 var(--f-d);text-transform:uppercase;letter-spacing:-.02em;overflow-wrap:normal !important;white-space:nowrap}
.tb-cut{border-top:2px dashed var(--ink);opacity:.45}
.tb-hl{font-size:14px;line-height:1.45}
.tb-marks{display:flex;gap:5px;flex-wrap:wrap;min-height:18px}
.tb-prog{font:700 12px var(--f-d);text-transform:uppercase;color:var(--mut)}
.tb-stamp{align-self:flex-start;font:700 12px var(--f-d);text-transform:uppercase;padding:4px 8px;border:3px double var(--ink);transform:rotate(-4deg);margin-top:4px;white-space:nowrap}
.tb-stamp.s-now{color:var(--hi-text);border-color:var(--hi-text)}
.tb-stamp.s-started{color:var(--ink)}
.tb-stamp.s-none,.tb-stamp.s-empty{color:var(--mut);border:2px dashed var(--grey);transform:none}
.tb-slip[data-s=none] .tb-hl,.tb-slip[data-s=none] .tb-pn,.tb-slip.is-empty .tb-hl,.tb-slip.is-empty .tb-pn{color:var(--mut)}
.tb-slip .sel-chev{position:absolute;right:16px;top:28px;margin:0}
.lp .tb-slip.is-up{background:#fff}
.tb-rail.is-empty .tb-slip{background:transparent;-webkit-mask:none;mask:none;filter:none;border:2px dashed var(--grey)}
.tb-rail.is-empty .tb-bar2{background:transparent;border:2px dashed var(--grey);box-shadow:none}
.tb-rail.is-empty .tb-clip{display:none}
/* marks: printed boxes */
.mk{display:inline-block;width:18px;height:18px;border:2px solid var(--ink);position:relative;flex-shrink:0}
.mk-done{background:var(--ink)}
.mk-done::before{content:"";position:absolute;left:4px;top:0;width:5px;height:9px;border-right:2px solid var(--card);border-bottom:2px solid var(--card);transform:rotate(40deg)}
.mk-now{background:var(--hi);border-color:var(--hi)}
.mk-now::before{content:"";position:absolute;left:4px;top:3px;border-left:7px solid #fff;border-top:4px solid transparent;border-bottom:4px solid transparent}
.mk-later{background:var(--card)}
.mk-none{border:2px dashed var(--grey)}
.tb-key{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:16px;font:400 12px var(--f-d);text-transform:uppercase;color:var(--mut)}
.tb-key span{display:inline-flex;align-items:center;gap:7px}
/* the docket */
.tb-desk{margin-top:20px}
.tb-box{display:flex;flex-direction:column;gap:10px;padding:22px 24px 26px;background:var(--card);-webkit-mask:var(--zig);mask:var(--zig)}
.tb-bh{display:flex;align-items:center;gap:14px;flex-wrap:wrap;border-bottom:2px dashed rgba(38,35,46,.4);padding-bottom:10px}
.tb-box h4{font:700 20px var(--f-d);text-transform:uppercase;letter-spacing:-.02em}
.tb-st{font:700 12px var(--f-d);text-transform:uppercase;padding:3px 8px;border:2px solid var(--ink)}
.tb-st.s-now{background:var(--hi);border-color:var(--hi);color:#fff}
.tb-st.s-none{border-style:dashed;border-color:var(--grey);color:var(--mut)}
.tb-box>p{font-size:15px;line-height:1.55}
.tb-fig{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;font-size:14px;color:var(--mut)}
.tb-fv{font:700 24px/1 var(--f-d);color:var(--hi-text);letter-spacing:-.03em}
.tb-steps{display:flex;flex-direction:column;gap:2px}
.tb-steps li{display:flex;align-items:center;gap:10px;font-size:14.5px;line-height:1.45;padding:4px 0}
.tb-sn{min-width:0}
.tb-ss{margin-left:auto;padding-left:14px;font:700 12px var(--f-d);text-transform:uppercase;color:var(--mut);white-space:nowrap}
.tb-steps li.s-now .tb-ss{color:var(--hi-text)}
.tb-box .bm-open{align-self:flex-start}
.skin-b .bx-mob{background:transparent;border:0}
.skin-b .bx-mob::before{display:none}
.skin-b .bx-mob .tb-box{padding:22px 16px 26px}
.skin-b p,.skin-b li,.skin-b b,.skin-b span{overflow-wrap:anywhere}
@container lp (max-width:699px){
 .tb-top{grid-template-columns:1fr;gap:22px;margin:22px 0 4px}
 .tb-rcpt{transform:none}
 .tb-bar2{display:none}
 .tb-rail{padding-top:0}
 .tb-slips{grid-template-columns:1fr;gap:14px}
 .tb-slip{padding:22px 16px 24px}
 .tb-slip .sel-chev{display:inline-block}
 .skin-b .js-sel.is-up{transform:translateY(-3px) rotate(-.6deg)}
 .tb-slips .bx-mob{margin:-6px 0 6px}
 .tb-steps li{display:grid;grid-template-columns:18px minmax(0,1fr);column-gap:10px;align-items:start}
 .tb-steps li .mk{margin-top:2px}
 .tb-ss{grid-column:2;margin:2px 0 0;padding:0;justify-self:start}
}
'''

# ==========================================================================================
# C · THE ANNUAL REPORT
def c_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    m = d['money']
    if m:
        shades = ['var(--ink)', '#4A4B50', '#8A8B84', '#BDBEB6']
        bar = ''.join('<i style="flex:%d;background:%s"></i>' % (w, c) for (_, _, w), c in zip(m['lines'], shades))
        leg = ''.join('<li><i style="background:%s"></i><span>%s</span><b>%s</b></li>' % (c, e(a), e(v)) for (a, v, _), c in zip(m['lines'], shades))
        fig = ('<aside class="cr-fig"%s><div class="cr-fh"><span class="cr-kick">Where the money goes</span>%s</div>'
               '<div class="cr-big"><b>%s</b><span>%s</span></div><p class="cr-share">%s. %s.</p>'
               '<div class="cr-bar" role="img" aria-label="₹20 lakh lost each month, split four ways">%s</div><ul class="cr-leg">%s</ul>'
               '<div class="cr-saved"><span>Saved so far</span><span class="cr-track" aria-hidden="true"></span><b>%s</b></div></aside>') % (
            pt(1), tag(m['tag']), e(m['lost']), e(m['lost_l']), e(m['spend']), e(m['share']), bar, leg, e(m['saved']))
    else:
        fig = '<aside class="cr-fig is-empty"><span class="cr-kick">Where the money goes</span><p>Fills in once a month of supplier bills is in.</p></aside>'
    top = '<div class="cr-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), fig)

    cols, desk = [], []
    total = sum(len(p['steps']) for p in d['places'])
    alldone = sum(counts(p)[0] for p in d['places'])
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        dn, n = counts(p)
        seg = ''.join('<i class="sg s-%s"></i>' % s for _, s in p['steps']) or '<i class="sg s-empty"></i>'
        inner = ('<span class="cr-seg" aria-hidden="true">%s</span><span class="cr-no">%02d</span><span class="cr-pn">%s</span>'
                 '<span class="cr-num"><b>%s</b><span>%s</span></span><span class="cr-st s-%s">%s</span><span class="cr-hl">%s</span>%s') % (
            seg, i + 1, e(p['name']), ('%d/%d' % (dn, n)) if n else '—', e(p['unit']) if n else 'no steps yet',
            p['status'], e(STATUS[p['status']]), e(p['head']), '' if empty else CHEV)
        if empty:
            cols.append('<div class="cr-col is-empty" data-s="empty">%s</div>' % inner); continue
        cols.append('<button class="cr-col %s" type="button" data-s="%s"%s%s>%s</button>' % (sel_cls(first), p['status'], sel('cr', k, first), pt(p.get('pt')), inner))
        det = place_detail(p, 'cr')
        cols.append(box('cr', k, det, first, 'mob'))
        desk.append(box('cr', k, det, first, 'desk'))
    head = ('<div class="cr-rh"><span><b>%s</b> of %s steps done</span><span class="cr-key" aria-hidden="true"><span><i class="sg s-done"></i>Done</span>'
            '<span><i class="sg s-now"></i>Now</span><span><i class="sg s-later"></i>Still to do</span><span><i class="sg s-none"></i>Not started</span></span></div>') % (
        alldone, total) if not empty else '<div class="cr-rh"><span>No steps yet</span></div>'
    reg = '<div class="cr-reg%s">%s<div class="cr-cols">%s</div></div>' % (' is-empty' if empty else '', head, ''.join(cols))
    sub = 'Every step of the work in one bar, cut into its four parts. Tap a part to read it.' if not empty else 'Every step of the work in one bar, cut into its four parts'
    emb = '<span class="bm-emb">%s</span>' % ico(MARK, 'var(--hi)', 28)
    return (C.masthead(KICK, emb, STAMP[state]) + top
            + section('Where each part of the work stands', reg + ('<div class="cr-desk">%s</div>' % ''.join(desk) if desk else ''), 'cr-sec', sub)
            + pending(d['pending']) + actions(d['actions']))

C_PAGE_CSS = r'''
.cr-top{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:40px;align-items:start;margin:26px 0 4px}
.cr-top .bm-stand{margin:4px 0 0}
.cr-fig{display:flex;flex-direction:column;gap:10px;background:var(--card);padding:18px 20px 20px;border-top:6px solid var(--ink)}
.cr-fh{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.cr-kick{font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.cr-big{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.cr-big b{font:800 44px/1 var(--f-d);letter-spacing:-.04em}
.cr-big span{font-size:15px;font-weight:600}
.cr-share{font-size:13.5px;line-height:1.5;color:var(--mut)}
.cr-bar{display:flex;height:26px;gap:2px}
.cr-bar i{display:block;min-width:4px}
.cr-leg{display:flex;flex-direction:column}
.cr-leg li{display:flex;align-items:baseline;gap:10px;font-size:14px;line-height:1.4;padding:6px 0;border-top:1px solid var(--line)}
.cr-leg li i{width:10px;height:10px;flex-shrink:0;transform:translateY(1px)}
.cr-leg li span{min-width:0}
.cr-leg li b{margin-left:auto;padding-left:10px;font-weight:800;white-space:nowrap}
.cr-saved{display:flex;align-items:center;gap:12px;font-size:13.5px;font-weight:600;border-top:1px solid var(--ink);padding-top:10px}
.cr-track{flex:1 1 60px;height:8px;background:repeating-linear-gradient(90deg,var(--line) 0 6px,transparent 6px 9px)}
.cr-saved b{font-weight:800}
.cr-fig.is-empty{background:transparent;border:1px dashed var(--grey);border-top:6px solid var(--grey);color:var(--mut)}
.cr-fig.is-empty p{font-size:14.5px}
/* the register */
.cr-rh{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;font-size:14px;margin-bottom:12px}
.cr-rh b{font:800 22px var(--f-d);letter-spacing:-.02em}
.cr-key{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:12.5px;color:var(--mut)}
.cr-key span{display:inline-flex;align-items:center;gap:7px}
.cr-key .sg{width:16px;height:10px;flex:none}
.cr-cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}
.cr-col{display:flex;flex-direction:column;align-items:flex-start;gap:8px;text-align:left;border:0;background:transparent;padding:12px 14px 18px;color:var(--ink);min-width:0;position:relative}
.lp .cr-col.is-up{background:var(--card)}
.cr-seg{display:flex;gap:3px;width:100%;height:30px;margin-bottom:6px}
.sg{display:block;flex:1;height:100%}
.sg.s-done{background:var(--ink)}
.sg.s-now{background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.sg.s-later{background:var(--soft);box-shadow:inset 0 0 0 1px var(--grey)}
.sg.s-none,.sg.s-empty{background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey);background-image:repeating-linear-gradient(135deg,transparent 0 5px,rgba(0,0,0,.08) 5px 6px)}
.cr-no{font:800 13px var(--f-d);color:var(--mut)}
.cr-pn{font:800 22px/1 var(--f-d);letter-spacing:-.025em}
.cr-num{display:flex;align-items:baseline;gap:8px}
.cr-num b{font:800 30px/1 var(--f-d);letter-spacing:-.04em}
.cr-num span{font-size:13px;color:var(--mut)}
.cr-st{font-size:12px;font-weight:600;padding:3px 9px;background:var(--soft)}
.cr-st.s-now{background:var(--hi);color:var(--ink)}
.cr-st.s-started{background:var(--ink);color:var(--card)}
.cr-st.s-none,.cr-st.s-empty{background:transparent;box-shadow:inset 0 0 0 1px var(--grey);color:var(--mut)}
.cr-hl{font-size:14px;line-height:1.45}
.cr-col[data-s=none] .cr-pn,.cr-col[data-s=none] .cr-hl,.cr-col[data-s=none] .cr-num b,.cr-col.is-empty .cr-pn,.cr-col.is-empty .cr-hl,.cr-col.is-empty .cr-num b{color:var(--mut)}
.cr-col .sel-chev{position:absolute;right:14px;top:58px;margin:0}
/* the box */
.cr-desk{margin-top:24px}
.cr-box{display:flex;flex-direction:column;gap:12px;padding:20px 22px 22px;background:var(--card);border-top:6px solid var(--ink)}
.cr-bh{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.cr-box h4{font:800 26px/1 var(--f-d);letter-spacing:-.03em}
.cr-box>p{font-size:15px;line-height:1.55}
.cr-fig2,.cr-fig{}
.cr-box .cr-fig{display:flex;flex-direction:row;align-items:baseline;gap:10px;flex-wrap:wrap;background:transparent;padding:0;border:0;font-size:14px;color:var(--mut)}
.cr-fv{font:800 28px/1 var(--f-d);letter-spacing:-.04em;color:var(--ink)}
.cr-steps{display:flex;flex-direction:column;counter-reset:st}
.cr-steps li{display:flex;align-items:baseline;gap:12px;font-size:14.5px;line-height:1.45;padding:8px 0;border-top:1px solid var(--line);counter-increment:st}
.cr-steps li::before{content:counter(st);font:800 14px var(--f-d);color:var(--mut);min-width:16px}
.cr-steps .mk{display:none}
.cr-sn{min-width:0}
.cr-ss{margin-left:auto;padding-left:14px;font-size:12.5px;font-weight:600;color:var(--mut);white-space:nowrap}
.cr-steps li.s-done .cr-ss{color:var(--ink)}
.cr-steps li.s-now .cr-ss{background:var(--hi);color:var(--ink);padding:1px 8px}
.cr-steps li.s-now .cr-sn{font-weight:600}
.cr-box .bm-open{align-self:flex-start}
.skin-c .bx-mob{background:transparent;border:0}
.skin-c .bx-mob::before{display:none}
.skin-c .bx-mob .cr-box{padding:16px 16px 18px}
.skin-c p,.skin-c li,.skin-c b,.skin-c span{overflow-wrap:anywhere}
@container lp (max-width:699px){
 .cr-top{grid-template-columns:1fr;gap:22px;margin:22px 0 4px}
 .cr-big b{font-size:38px}
 .cr-cols{grid-template-columns:1fr;gap:10px}
 .cr-col{padding:12px 40px 14px 12px}
 .cr-col .sel-chev{display:inline-block;top:62px;right:16px}
 .cr-cols .bx-mob{margin:0 0 8px}
 .cr-steps li{display:grid;grid-template-columns:16px minmax(0,1fr);column-gap:12px}
 .cr-ss{grid-column:2;margin:2px 0 0;padding:0;justify-self:start}
 .cr-steps li.s-now .cr-ss{padding:1px 8px}
}
'''

# ==========================================================================================
# The tool's colours in each look (colour is the only thing a second tool in this domain changes)
T = C.theme
THEMES = {
 # ledger buff, navy ink, red ink
 'a': T('#ECE5CF', '#FBF8EE', '#1E2B45', '#4A556D', '#C6BB98', '#F3EDD9', '#9F977E', '#B4321F', '#F2B8A6', '#9A2A19',
        ['#E3DAC0', '#D9E0E6', '#EAD6CC', '#E1DFC8', '#D6DED3'], '#1E2B45'),
 # counter grey, till ink, stamp violet
 'b': T('#DAD6CC', '#FFFEF8', '#26232E', '#504C58', '#BCB6A9', '#F1EEE5', '#98938A', '#6A3DBA', '#CDB8F7', '#5A31A3',
        ['#FFFEF8', '#EDE6FA', '#FFF1C9', '#DCEFE6', '#F9DDD5'], '#26232E'),
 # report white, black, lime
 'c': T('#EEEEE9', '#FFFFFF', '#0F1012', '#505257', '#CFCFC8', '#E2E3DB', '#A3A49C', '#C6E43F', '#C6E43F', '#4A5A00',
        ['#E2E3DB', '#D6D7CF', '#E2E3DB', '#D6D7CF', '#E2E3DB'], '#0F1012'),
}
PAGES = {
 'a': (a_canvas, A_PAGE_CSS, 'A', 'The ledger'),
 'b': (b_canvas, B_PAGE_CSS, 'B', 'The till roll'),
 'c': (c_canvas, C_PAGE_CSS, 'C', 'The annual report'),
}
ABOUT = {
 'a': ('<b>A · The ledger.</b> The domain reads like an accounts book. Playfair Display for names and figures, Source Serif for reading. '
       'Square corners, hairlines and double rules, a red double margin, ruled paper, ticks for entries. The rail is the book’s thumb index, the chat a cloth-bound cover with a gilt line, '
       'Tojo’s Note set in italic. Raised means a printed offset shadow. The drawing: the month’s account, then one ruled line in the book per part of the work.'
       '<em>Tool colours here: ledger buff, navy ink, red ink. Another Financial tool keeps all of this and changes only these colours.</em>'),
 'b': ('<b>B · The till roll.</b> The domain reads like the counter where money changes hands. Space Mono for names, figures and labels, Space Grotesk for reading. '
       'Paper slips with torn zigzag edges on a dotted counter, dashed tear lines, printed tick boxes, double-ringed stamps. The rail is tear-off tickets, the chat is the till printing slips, '
       'Tojo’s Note a rubber stamp. Raised means a slip lifted and tilted. The drawing: the month’s till receipt, then four slips clipped to a rail.'
       '<em>Tool colours here: counter grey, till ink, stamp violet. Another Financial tool keeps all of this and changes only these colours.</em>'),
 'c': ('<b>C · The annual report.</b> The domain reads like a company’s yearly report. Inter Tight for everything, set tight and heavy, with Instrument Serif italic for Tojo’s Note. '
       'Flat planes, no rounded corners, heavy rules, numbered sections, big figures. The rail is flat numbered bars, the chat flat black with an editorial note. '
       'Raised means a hard block shadow. The drawing: where the money goes in one bar, then every step of the work in one bar, cut into its four parts.'
       '<em>Tool colours here: report white, black, lime. Another Financial tool keeps all of this and changes only these colours.</em>'),
}

def build():
    os.makedirs(OUT, exist_ok=True)
    pages, words = {}, []
    for k, (fn, css, letter, label) in PAGES.items():
        sk, t = SKINS[k], THEMES[k]
        for st in ('filled', 'empty'):
            canvas = fn(st)
            for v in ('desktop', 'mobile'):
                h = C.page(sk, t, None, canvas, css, DATA[st]['chat'], v, 'Supply Chain and Procurement · %s' % label, 'sc sc-home')
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(OUT, 'scp-home-%s.%s.%s.html' % (k, v, st)), 'w', encoding='utf-8').write(h)
            words += [(k, st, w) for w in C.plain_check(_text(canvas) + ' ' + json.dumps(DATA[st]['chat'], ensure_ascii=False))]
    return pages, words

def _text(h):
    return re.sub(r'<[^>]+>', ' ', h)

def review(pages):
    tpl = open(os.path.join(HERE, 'review_template.html'), encoding='utf-8').read()
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>Sample %s</b><span>%s</span><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 4px %s"></i></button>' % (
        k, 'true' if k == 'a' else 'false', v[2], e(v[3]), THEMES[k]['ground'], THEMES[k]['ink'], THEMES[k]['hi']) for k, v in PAGES.items())
    return (tpl.replace('@@PICKS@@', picks).replace('@@ABOUT@@', json.dumps(ABOUT, ensure_ascii=False))
               .replace('@@DATA@@', json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')))

if __name__ == '__main__':
    pages, words = build()
    if words:
        print('PLAIN ENGLISH:', words)
    rv = os.path.join(OUT, 'supply-chain-home-samples.html')
    open(rv, 'w', encoding='utf-8').write(review(pages))
    print('built', rv, os.path.getsize(rv))
