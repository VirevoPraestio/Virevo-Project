"""
Supply Chain and Procurement: the four place pages (8 Oct 2026, for review), beside the approved home page F.

Avishek approved F (the notebook) as the tool's home page, and asked for the four place pages to
borrow the other samples' ideas, each place looking different in colour and in the elements it uses.
All five use the Financial identity: the Virevo type exactly as in 07 §2 (Bebas Neue, Poppins,
Caveat), the flat frame, and the three papers of money (report sheet, ledger paper, receipt).

  Home         F · the notebook (approved): parts on the left page, the open part on the right.
  Diagnosis    the item's receipt: one item followed from the ward's request to the bill, every
               loss printed as a line; then the four causes weighed as report bars.
  Solutions    the ledger of fixes: one ruled entry per fix, its four stops, what it brings back,
               and a double-ruled total; by hand and automatic side by side in its box.
  Automations  the helpers' day: a flat 24-hour bar with each helper at the hour it runs, and
               under it each helper with the slip it would print.
  Processes    the week planner: a ruled notebook week with the changes pinned on their days,
               a signature register for who signs for what, and the numbers we watch.

Colours: each place has its own ground, ink and highlight, and none repeats another's.
Run:  python3 landing3.py   ->  out/landing/
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sc_common as C
from sc_common import e, ico, ICONS, CHEV, sel, sel_cls, box, pt, tag, say_btn, standing, section, pending, actions, STAMP, MARK
from skins import SKINS
import landing2 as L2
from landing import DATA as HOME_DATA, OUT, KICK

SK = SKINS['f']

# ==========================================================================================
# Colours: home keeps C's report white, black and lime. Each place gets its own.
RAIL = ['#E2E3DB', '#E3E9F0', '#ECE7F7', '#E0EFE8', '#F2EBDC']   # Resources, then the four places in their own grounds
def T(ground, card, ink, mut, line, soft, grey, hi, hi_dark, hi_text, panel):
    return C.theme(ground, card, ink, mut, line, soft, grey, hi, hi_dark, hi_text, RAIL, panel)
THEMES = {
 # home: report white, black, lime (as approved)
 'home': T('#EEEEE9', '#FFFFFF', '#0F1012', '#505257', '#CFCFC8', '#E2E3DB', '#A3A49C', '#C6E43F', '#C6E43F', '#4A5A00', '#0F1012'),
 # Diagnosis: steel, navy black, signal orange
 'diagnosis': T('#E3E9F0', '#FFFFFF', '#0E1A2B', '#4A5668', '#C3CDD9', '#EEF2F7', '#9AA6B4', '#FF8A3D', '#FF9A55', '#9A3E00', '#0E1A2B'),
 # Solutions: lilac, deep violet, violet
 'solutions': T('#ECE7F7', '#FFFFFF', '#1D1736', '#544C6E', '#D0C7E6', '#F4F0FB', '#A79FBE', '#A48EFF', '#B9A8FF', '#4F35C2', '#1D1736'),
 # Automations: mint, deep green, coral pink
 'automations': T('#E0EFE8', '#FFFFFF', '#08271D', '#3E5A50', '#BFD9CD', '#EEF7F3', '#93AEA3', '#FF6F91', '#FF8CA8', '#A3173E', '#08271D'),
 # Processes: sand, deep brown, sky blue
 'processes': T('#F2EBDC', '#FFFFFF', '#23190A', '#5C4E38', '#DCCFB4', '#F8F3E8', '#ADA083', '#4FA3F0', '#6FB5F5', '#145A9C', '#23190A'),
}

def masthead(place, state):
    emb = '<span class="bm-emb">%s</span>' % ico(ICONS[place] if place else MARK, 'var(--hi)', 28)
    return ('<header class="bm-mast"><div class="bm-id">%s<div><div class="bm-kick">%s</div><h1 class="bm-name">%s</h1></div></div>%s</header>') % (
        emb, e('Virevo · %s' % C.TOOL), e(place), C.B.stamp(STAMP[state]))

def two(a_lab, a, b_lab, b, cls=''):
    return '<div class="fx-two %s"><div><span class="fx-lab">%s</span><p>%s</p></div><div><span class="fx-lab">%s</span><p>%s</p></div></div>' % (
        cls, e(a_lab), e(a), e(b_lab), e(b))

# shared parts for the place pages
PLACE_CSS = r'''
.fx-box{display:flex;flex-direction:column;gap:12px;padding:18px 22px 20px;background:var(--card);border-top:6px solid var(--ink)}
.fx-bh{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.fx-box h4{font:400 30px/1 var(--f-d)}
.fx-box>p{font-size:14.5px;line-height:1.55}
.fx-lab{display:block;font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut);margin-bottom:4px}
.fx-two{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.fx-two>div{min-width:0}
.fx-two p{font-size:14px;line-height:1.55}
.fx-bul{display:flex;flex-direction:column;gap:5px}
.fx-bul li{position:relative;padding-left:16px;font-size:14px;line-height:1.5}
.fx-bul li::before{content:"";position:absolute;left:1px;top:.55em;width:7px;height:7px;background:var(--hi)}
.fx-box .bm-open{align-self:flex-start}
.fx-chip{display:inline-block;font-size:12px;font-weight:600;padding:3px 9px;background:var(--soft);white-space:nowrap}
.fx-chip.c-now{background:var(--hi);color:var(--ink)}.fx-chip.c-done{background:var(--ink);color:var(--card)}
.fx-chip.c-none{background:transparent;box-shadow:inset 0 0 0 1px var(--grey);color:var(--mut)}
.fx-hint{font-size:13px;color:var(--mut);margin-top:10px}
.fx-empty{border:2px dashed var(--grey);padding:18px 20px;color:var(--mut);font-size:14px;line-height:1.5}
@container lp (max-width:699px){
 .fx-two{grid-template-columns:1fr;gap:12px}
 .fx-box{padding:14px 16px 16px}
 .fx-box h4{font-size:26px}
}
'''

# ==========================================================================================
# DIAGNOSIS · the item's receipt
DG = {
 'filled': {
  'claim': 'We lose money at four points, and most of it before the box arrives',
  'deck': 'Two of five steps done. We followed one item from the ward’s request to the patient’s bill. The biggest loss is the price we pay.',
  'item': {'head': 'One item, followed', 'what': '100 IV cannulas for Ward 3', 'when': 'September', 'spent': '₹5,600 spent',
           'total': '₹1,776', 'total_l': 'lost on this one item', 'tag': 'example'},
  'lines': [
   {'label': 'Ward 3 asks for 100 cannulas', 'amt': '—', 'note': 'The start',
    'found': 'The ward sister writes the request on Monday. The store has 30 in stock, so the buyer orders 100.',
    'points': 'Requests are fine. The loss starts after this.'},
   {'label': 'Bought at ₹48 each. The best price we found is ₹40.', 'amt': '₹800', 'pt': 2,
    'found': 'The buyer orders from the usual supplier without checking the price. Two other suppliers sell the same cannula for ₹40 to ₹42.',
    'points': 'No agreed price for the item. This is the biggest loss.'},
   {'label': '20 more bought in a rush at a local shop, at ₹60 each', 'amt': '₹400', 'pt': 4,
    'found': 'The ward ran out on a Thursday night. A staff member bought 20 from a shop near the gate, at a higher price, with no one signing for it.',
    'points': 'No lowest stock level on the shelf, and no one who signs off a rushed buy.'},
   {'label': '8 used on patients, but never put on their bill', 'amt': '₹384',
    'found': 'Nurses used the cannulas during the night but did not note them on the patient’s chart, so billing never saw them.',
    'points': 'Items are not recorded at the bedside when they are used.'},
   {'label': '4 expired on the shelf and were thrown away', 'amt': '₹192',
    'found': 'Older boxes sat behind newer ones. Four cannulas passed their date before anyone reached them.',
    'points': 'Stock is not used oldest first. Small for this item, larger for medicines.'},
  ],
  'causes': [
   {'name': 'Prices never agreed with suppliers', 'amt': '₹8 lakh', 'w': 4, 'state': 'Leading so far', 'lead': True, 'pt': 2},
   {'name': 'No lowest level, so wards rush-buy', 'amt': '₹5 lakh', 'w': 3, 'state': 'Being checked', 'pt': 4},
   {'name': 'Use not recorded, so not billed', 'amt': '₹4 lakh', 'w': 2, 'state': 'Some signs'},
   {'name': 'Old stock not used first', 'amt': '₹3 lakh', 'w': 1, 'state': 'Not checked yet'},
  ],
  'pending': [
   {'text': 'Compare what we paid for our top 50 items with the best price.', 'need': 'Needs last quarter’s supplier bills', 'pt': 2},
   {'text': 'Find out who can approve a rushed buy, and how often it happens.', 'pt': 4},
   {'text': 'Count what expires on the shelf each month.'},
   {'text': 'Name the main cause, so the fixes start in the right place.'},
  ],
  'actions': {'go': {'detail': 'Compare what we paid for our top 50 items', 'say': 'Let’s compare what we paid for our top 50 items'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about how we lose money on supplies: '},
              'jump': {'tab': 'Solutions', 'detail': 'See the three fixes so far', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['Diagnosis is two of five steps in.', 'We followed 100 cannulas for Ward 3. Of ₹5,600 spent, about ₹1,776 was lost, and almost half of it on the price we paid.'],
           'pointer': 'Pick a point to add to it, or tap a line of the receipt.',
           'note': 'The loss starts at the price, not on the ward.',
           'points': [{'n': 1, 'label': 'Money lost each month'}, {'n': 2, 'label': 'The price we pay'},
                      {'n': 3, 'label': 'The four causes'}, {'n': 4, 'label': 'Rushed buys'}],
           'prompts': ['Our buyer has a price list', 'How sure are these numbers?', 'Let’s compare our top 50 items']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Tojo follows one item with you, from the ward asking for it to the patient’s bill, and prints every loss on the way.',
  'item': None, 'lines': [{'label': l} for l in ['The ward asks for it', 'Someone buys it', 'It reaches the shelf', 'It is used on a patient', 'It reaches the patient’s bill']],
  'causes': [{'name': n} for n in ['Prices never agreed', 'Rushed buys', 'Use not recorded', 'Old stock not used first']],
  'pending': [
   {'text': 'Pick one item the hospital buys often, and follow it with Tojo.'},
   {'text': 'Put a number on what is lost each month.', 'need': 'Needs a month of supplier bills'},
   {'text': 'Find out who decides what to buy, and from whom.'},
  ],
  'actions': {'go': {'detail': 'Follow one item with Tojo', 'say': 'Let’s follow one item'},
              'add': {'detail': 'Share a bill list or a stock report', 'say': 'Here is what I already know about how we buy supplies: '},
              'jump': {'tab': 'Solutions', 'detail': 'Fills in once the cause is named', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['This is Diagnosis. We find out where money is lost on supplies.', 'We start by following one item the hospital buys often.'],
           'note': 'Pick one item. Follow it.', 'points': [],
           'prompts': ['Let’s follow one item', 'Which item should we pick?', 'What should I bring?']},
 },
}

def dg_canvas(state):
    d = DG[state]; empty = state == 'empty'
    lines, desk = [], []
    for i, r in enumerate(d['lines']):
        k = str(i); first = i == 0 and not empty
        if empty:
            lines.append('<div class="dg-l is-empty"><span class="dg-n">%d</span><span class="dg-lt">%s</span><i aria-hidden="true"></i><b>?</b></div>' % (i + 1, e(r['label'])))
            continue
        lost = r['amt'] != '—'
        lines.append(('<button class="dg-l %s%s" type="button"%s%s><span class="dg-n">%d</span><span class="dg-lt">%s</span><i aria-hidden="true"></i>'
                      '<b>%s</b>%s</button>') % (sel_cls(first), ' is-loss' if lost else '', sel('dg', k, first), pt(r.get('pt')), i + 1, e(r['label']),
                                                 e(r['amt'] if lost else r['note']), CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>Line %d</h4>%s%s</div><p>%s</p>%s</div>') % (
            i + 1, '<span class="fx-chip c-now">%s lost</span>' % e(r['amt']) if lost else '<span class="fx-chip">The start</span>', tag('example'),
            e(r['label']), two('What we found', r['found'], 'What it points to', r['points']))
        lines.append(box('dg', k, det, first, 'mob'))
        desk.append(box('dg', k, det, first, 'desk'))
    it = d['item']
    if it:
        head = ('<div class="dg-rh"><span class="dg-rk">%s</span>%s</div><b class="dg-rw">%s</b><span class="dg-rs">%s · %s</span>') % (
            e(it['head']), tag(it['tag']), e(it['what']), e(it['when']), e(it['spent']))
        foot = '<div class="dg-tot"%s><span>%s</span><b>%s</b></div><div class="v-code dg-code" aria-hidden="true"></div>' % (pt(1), e(it['total_l']), e(it['total']))
    else:
        head = '<div class="dg-rh"><span class="dg-rk">One item, followed</span></div><span class="dg-rs">Prints as you follow an item with Tojo</span>'
        foot = ''
    rc = '<div class="dg-rc%s">%s<div class="v-cut" aria-hidden="true"></div><div class="dg-lines">%s</div><div class="v-cut" aria-hidden="true"></div>%s</div>' % (
        ' is-empty' if empty else '', head, ''.join(lines), foot)
    side = '<div class="dg-side">%s</div>' % ''.join(desk) if desk else '<div class="dg-side"><p class="fx-empty">Each line opens here once it is printed.</p></div>'
    body = '<div class="dg-wrap">%s%s</div>' % (rc, side)
    sub = 'Every loss on the way is printed as a line. Tap a line to read it.' if not empty else 'Prints as we follow one item'
    # causes, weighed as report bars
    rows = []
    mx = 8.0
    for c in d['causes']:
        if empty:
            rows.append('<div class="dc-r is-empty"><span class="dc-n">%s</span><span class="dc-bar"><i></i></span><b>—</b><span class="dc-s">Not weighed yet</span></div>' % e(c['name']))
            continue
        v = float(c['amt'].replace('₹', '').split()[0])
        dots = ''.join('<i class="%s"></i>' % ('on' if j < c['w'] else '') for j in range(5))
        rows.append(('<div class="dc-r%s"%s><span class="dc-n">%s</span><span class="dc-bar"><i style="width:%d%%"></i></span><b>%s</b>'
                     '<span class="dc-s"><span class="dc-dots" aria-label="%d of 5 pieces of evidence">%s</span>%s</span></div>') % (
            ' is-lead' if c.get('lead') else '', pt(c.get('pt')), e(c['name']), round(v / mx * 100), e(c['amt']), c['w'], dots, e(c['state'])))
    causes = '<div class="dc-rows"%s>%s</div><p class="fx-hint">%s</p>' % (
        pt(3) if not empty else '', ''.join(rows),
        'Bars show the money each cause loses a month (Example only). Dots show the evidence so far.' if not empty else 'Tojo weighs each cause as the evidence comes in.')
    return (masthead('Diagnosis', state) + standing(d['claim'], d['deck'], empty)
            + section('The item’s receipt', body, 'dg-sec', sub)
            + section('Which cause leads so far', causes, 'dc-sec', 'Four possible main causes')
            + pending(d['pending']) + actions(d['actions']))

DG_CSS = r'''
.dg-wrap{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:26px;align-items:start}
.dg-rc{background:var(--card);padding:24px 20px 28px;display:flex;flex-direction:column;gap:10px;-webkit-mask:var(--zig);mask:var(--zig);filter:drop-shadow(0 6px 8px rgba(0,0,0,.12))}
.dg-rh{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.dg-rk{font-size:12.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.dg-rw{font:400 28px/1 var(--f-d)}
.dg-rs{font-size:13px;color:var(--mut)}
.dg-lines{display:flex;flex-direction:column;gap:2px}
.dg-l{display:grid;grid-template-columns:22px minmax(0,1fr) minmax(14px,40px) auto 12px;align-items:baseline;gap:8px;width:100%;border:0;background:transparent;text-align:left;padding:8px 6px;color:var(--ink);font-size:14px;line-height:1.45}
.dg-l .dg-n{font:400 20px/1 var(--f-d);color:var(--mut)}
.dg-l>i{border-bottom:2px dotted var(--grey);transform:translateY(-4px)}
.dg-l>b{font-weight:600;white-space:nowrap}
.dg-l.is-loss>b{font:400 24px/1 var(--f-d);color:var(--hi-text)}
.dg-l:not(.is-loss)>b{font-size:12.5px;color:var(--mut)}
.lp .dg-l.is-up{background:var(--soft)}
.dg-l .sel-chev{display:none}
.dg-tot{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.dg-tot span{font-size:12.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.dg-tot b{font:400 30px/1 var(--f-d);background:linear-gradient(transparent 52%,var(--hi) 52% 92%,transparent 92%);padding:0 4px}
.dg-code{height:22px;margin-top:2px}
.dg-rc.is-empty{background:transparent;-webkit-mask:none;mask:none;filter:none;border:2px dashed var(--grey);color:var(--mut)}
.dg-l.is-empty{color:var(--mut);cursor:default}
.dg-side{position:sticky;top:190px}
.dg-side .fx-two{grid-template-columns:1fr}
/* causes */
.dc-rows{display:flex;flex-direction:column;border-top:1px solid var(--line)}
.dc-r{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr) 90px 180px;align-items:center;gap:14px;padding:11px 12px;border-bottom:1px solid var(--line)}
.dc-n{font-size:14.5px;font-weight:600;line-height:1.35}
.dc-bar{display:block;height:14px;background:var(--soft)}
.dc-bar i{display:block;height:100%;background:var(--ink)}
.dc-r>b{font:400 26px/1 var(--f-d);text-align:right}
.dc-s{display:flex;align-items:center;gap:10px;font-size:12.5px;font-weight:600;color:var(--mut)}
.dc-dots{display:flex;gap:4px}.dc-dots i{width:10px;height:10px;box-shadow:inset 0 0 0 1.5px var(--ink)}.dc-dots i.on{background:var(--ink)}
.dc-r.is-lead{background:var(--ink);color:var(--card)}
.dc-r.is-lead .dc-bar{background:rgba(255,255,255,.15)}.dc-r.is-lead .dc-bar i{background:var(--hi)}
.dc-r.is-lead .dc-s{color:var(--hi-dark)}.dc-r.is-lead .dc-dots i{box-shadow:inset 0 0 0 1.5px var(--hi)}.dc-r.is-lead .dc-dots i.on{background:var(--hi)}
.dc-r.is-empty{color:var(--mut)}.dc-r.is-empty .dc-bar{background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey)}.dc-r.is-empty .dc-bar i{display:none}
@container lp (max-width:699px){
 .dg-wrap{grid-template-columns:1fr}
 .dg-side{display:none}
 .dg-rc{padding:22px 14px 26px}
 .dg-l{grid-template-columns:20px minmax(0,1fr) auto 14px;padding:10px 4px}
 .dg-l>i{display:none}
 .dg-l .sel-chev{display:inline-block;margin-top:4px}
 .dg-lines .bx-mob{margin:2px 0 10px}
 .dg-lines .bx-mob .fx-box{border-top:3px solid var(--ink);background:var(--soft)}
 .dc-r{grid-template-columns:minmax(0,1fr) auto;gap:8px 12px}
 .dc-bar{grid-column:1/-1;grid-row:2}
 .dc-s{grid-column:1/-1}
}
'''

# ==========================================================================================
# SOLUTIONS · the ledger of fixes
STOPS = ['Idea', 'Shaped', 'Tested with you', 'Agreed']
SO = {
 'filled': {
  'claim': 'Three fixes could bring back about half of what we lose',
  'deck': 'One fix is being tested with you. None is agreed yet. Each fix works by hand first, so you can start without new software.',
  'fixes': [
   {'name': 'One agreed price per item, from fewer suppliers', 'stage': 2, 'back': '₹4 lakh', 'pt': 1,
    'what': 'The buyer agrees one price a year for each of the top 50 items with two or three suppliers. Every bill is checked against that price.',
    'hand': 'The buyer keeps one price list for the top 50 items and checks each bill against it before it is paid.',
    'auto': 'A helper checks every new bill against the agreed price each night and flags any bill above it.',
    'needs': ['Last quarter’s supplier bills', 'Management agreeing to fewer suppliers']},
   {'name': 'A lowest level for each item, so rushed buys stop', 'stage': 1, 'back': '₹3 lakh', 'pt': 2,
    'what': 'Every shelf gets a lowest level for each item. When stock reaches it, an order goes out, long before the ward runs out.',
    'hand': 'A card on each shelf shows the lowest level. The store checks the cards every Monday and orders.',
    'auto': 'A helper reads the stock count each morning and orders by itself when an item reaches its lowest level.',
    'needs': ['How much each ward uses in a week', 'A Stores Lead who signs off any rushed buy']},
   {'name': 'Bill each item at the bedside when it is used', 'stage': 0, 'back': '₹2.5 lakh',
    'what': 'Every item used on a patient is noted on the patient’s chart at the bedside, so it always reaches the bill.',
    'hand': 'Nurses tick each item on a printed list on the chart. Billing counts the ticks each evening.',
    'auto': 'A helper matches what each ward used with what its patients were billed, every evening.',
    'needs': ['Nursing heads agreeing to the list on the chart']},
  ],
  'total': '₹9.5 lakh',
  'pending': [
   {'text': 'Test the agreed price with you: which 50 items, and which suppliers.', 'need': 'Needs last quarter’s supplier bills', 'pt': 1},
   {'text': 'Shape the lowest levels: how much each ward uses in a week.', 'pt': 2},
   {'text': 'Check that each fix also works with no new software.'},
  ],
  'actions': {'go': {'detail': 'Test the agreed price with you', 'say': 'Let’s test the first fix: one agreed price per item'},
              'add': {'detail': 'Suggest a fix of your own', 'say': 'I have an idea for a fix: '},
              'jump': {'tab': 'Automations', 'detail': 'See the helpers for these fixes', 'say': 'Take me to Automations'}},
  'chat': {'text': ['Three fixes are written up. The first, one agreed price per item, is being tested with you.', 'If all three are agreed, about ₹9.5 lakh a month could come back.'],
           'pointer': 'Pick a point to add to it, or tap a line in the ledger.',
           'note': 'Fix the price first. It is the biggest gap.',
           'points': [{'n': 1, 'label': 'One agreed price'}, {'n': 2, 'label': 'Lowest levels on the shelf'}, {'n': 3, 'label': 'What comes back'}],
           'prompts': ['We already have two main suppliers', 'How sure is the ₹9.5 lakh?', 'Let’s test the agreed price']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'The fixes are entered here once Diagnosis names the main cause. Each one comes with a by-hand and an automatic version.',
  'fixes': [], 'total': None,
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
    for i, f in enumerate(d['fixes']):
        k = str(i); first = i == 0
        stops = ''.join('<span class="so-t %s"><i aria-hidden="true"></i><span>%s</span></span>' % (
            'on' if j < f['stage'] else 'now' if j == f['stage'] else '', e(s)) for j, s in enumerate(STOPS))
        rows.append(('<button class="so-row %s" type="button"%s%s><span class="so-no">%d</span><span class="so-fix"><b>%s</b><span class="so-st">Now: %s</span></span>'
                     '<span class="so-stops">%s</span><span class="so-back"><b>%s</b><span>a month</span></span>%s</button>') % (
            sel_cls(first), sel('so', k, first), pt(f.get('pt')), i + 1, e(f['name']), e(STOPS[f['stage']]), stops, e(f['back']), CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>Fix %d</h4><span class="fx-chip c-now">Now: %s</span>%s</div><p>%s</p>'
               '<div class="so-ways"><div class="so-way"><span class="fx-lab">By hand</span><p>%s</p></div><div class="so-way so-auto"><span class="fx-lab">Automatic</span><p>%s</p></div></div>'
               '<div><span class="fx-lab">What it relies on</span><ul class="fx-bul">%s</ul></div></div>') % (
            i + 1, e(STOPS[f['stage']]), tag('guess'), e(f['what']), e(f['hand']), e(f['auto']), ''.join('<li>%s</li>' % e(x) for x in f['needs']))
        rows.append(box('so', k, det, first, 'mob'))
        desk.append(box('so', k, det, first, 'desk'))
    if empty:
        rows = ['<div class="so-row is-empty"><span class="so-no">%d</span><span class="so-fix"><b>Not entered yet</b></span><span class="so-stops">%s</span><span class="so-back"><b>—</b></span></div>' % (
            n, ''.join('<span class="so-t"><i></i><span>%s</span></span>' % e(s) for s in STOPS)) for n in (1, 2, 3)]
    head = ('<div class="so-head" aria-hidden="true"><span>No.</span><span>The fix</span><span>Its four stops</span><span>Brings back</span></div>')
    foot = '<div class="so-foot"%s><span>If all three are agreed</span>%s<span class="so-ft"><b>%s</b>%s</span></div>' % (
        pt(3) if not empty else '', tag('guess') if not empty else '', e(d['total'] or '—'), '<em class="so-pm">a month</em>' if d['total'] else '')
    book = '<div class="so-book%s">%s<div class="so-rows">%s</div>%s</div>' % (' is-empty' if empty else '', head, ''.join(rows), foot)
    body = book + ('<div class="so-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'One entry per fix. Its stops are ticked as it moves. Tap an entry.' if not empty else 'One entry per fix'
    return (masthead('Solutions', state) + standing(d['claim'], d['deck'], empty)
            + section('The ledger of fixes', body, 'so-sec', sub) + pending(d['pending']) + actions(d['actions']))

SO_CSS = r'''
.so-book{position:relative;background:var(--card);border-top:6px solid var(--ink);
 background-image:linear-gradient(90deg,transparent 18px,var(--hi) 18px 19px,transparent 19px 22px,var(--hi) 22px 23px,transparent 23px)}
.so-head,.so-row{display:grid;grid-template-columns:72px minmax(0,1fr) 290px 140px;align-items:stretch}
.so-head{border-bottom:3px double var(--ink)}
.so-head span{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut);padding:10px 12px}
.so-head span:first-child{padding-left:32px}
.so-head span:nth-child(3),.so-head span:nth-child(4){border-left:1px solid var(--line)}
.so-head span:nth-child(4){text-align:right}
.so-row{width:100%;border:0;border-bottom:1px solid var(--line);background:transparent;text-align:left;padding:0;color:var(--ink)}
.lp .so-row.is-up{background:var(--card)}
.so-no{font:400 26px/1 var(--f-d);color:var(--mut);padding:14px 8px 0 32px}
.so-fix{display:flex;flex-direction:column;gap:4px;padding:12px;min-width:0}
.so-fix b{font-size:15px;font-weight:600;line-height:1.35}
.so-st{font-size:12.5px;color:var(--mut)}
.so-stops{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));align-items:start;padding:12px 10px;border-left:1px solid var(--line);position:relative}
.so-t{position:relative;display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;font-size:11.5px;font-weight:600;color:var(--mut);line-height:1.25}
.so-t::before{content:"";position:absolute;top:10px;left:-50%;right:50%;border-top:2px solid var(--line);z-index:0}
.so-t:first-child::before{display:none}
.so-t i{position:relative;z-index:1;width:22px;height:22px;background:var(--card);box-shadow:inset 0 0 0 2px var(--grey)}
.so-t.on{color:var(--ink)}.so-t.on i{background:var(--ink);box-shadow:none}
.so-t.on i::after{content:"";position:absolute;left:7px;top:3px;width:6px;height:11px;border-right:2.5px solid var(--card);border-bottom:2.5px solid var(--card);transform:rotate(40deg)}
.so-t.on::before,.so-t.now::before{border-top-color:var(--ink)}
.so-t.now{color:var(--ink)}.so-t.now i{background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.so-back{display:flex;flex-direction:column;align-items:flex-end;justify-content:center;padding:12px 14px;border-left:1px solid var(--line)}
.so-back b{font:400 28px/1 var(--f-d);white-space:nowrap}
.so-back span{font-size:12px;color:var(--mut)}
.so-row .sel-chev{display:none}
.so-row.is-empty{color:var(--mut);cursor:default}.so-row.is-empty .so-t i{box-shadow:inset 0 0 0 1.5px var(--grey);background:transparent}
.so-foot{display:flex;align-items:baseline;gap:12px;padding:10px 14px 12px 94px;border-top:3px double var(--ink);font-size:14px;font-weight:600}
.so-ft{margin-left:auto;display:flex;align-items:baseline;gap:8px}
.so-foot b{font:400 30px/1 var(--f-d);border-bottom:5px double var(--ink);background:linear-gradient(transparent 50%,var(--hi) 50% 90%,transparent 90%);padding:0 3px 2px}
.so-pm{font-size:12.5px;font-weight:600;font-style:normal;color:var(--mut)}
.so-desk{margin-top:18px}
.so-ways{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.so-way{padding:12px 14px;background:var(--soft);border-left:4px solid var(--ink)}
.so-way.so-auto{border-left-color:var(--hi)}
.so-way p{font-size:14px;line-height:1.55}
@container lp (max-width:699px){
 .so-book{background-image:linear-gradient(90deg,transparent 8px,var(--hi) 8px 9px,transparent 9px 12px,var(--hi) 12px 13px,transparent 13px)}
 .so-head{display:none}
 .so-row{grid-template-columns:40px minmax(0,1fr) 26px;grid-template-areas:"no fix chev" "no stops stops" "no back back";padding:2px 0 12px}
 .so-no{grid-area:no;padding:14px 0 0 20px;font-size:22px}
 .so-fix{grid-area:fix;padding:12px 6px 4px}
 .so-stops{grid-area:stops;border-left:0;padding:8px 10px 4px 0}
 .so-back{grid-area:back;border-left:0;flex-direction:row;align-items:baseline;justify-content:flex-start;gap:8px;padding:4px 6px}
 .so-row .sel-chev{display:inline-block;grid-area:chev;margin:20px 0 0}
 .so-rows .bx-mob{margin:2px 10px 12px 20px}
 .so-foot{padding:10px 12px 12px 24px;flex-wrap:wrap}
 .so-ways{grid-template-columns:1fr}
}
'''

# ==========================================================================================
# AUTOMATIONS · the helpers' day
LAMPS = ['Idea', 'Built', 'Tested', 'Switched on']
AU = {
 'filled': {
  'claim': 'Three helpers, each doing one small job at the same hour every day',
  'deck': 'None is built yet. Each waits for its fix to be agreed. Each one does by itself what a person can also do by hand.',
  'helpers': [
   {'name': 'Price watch', 'hour': 1, 'when': 'Every night at 1 AM', 'fix': 'One agreed price per item', 'pt': 1,
    'does': 'Checks every new supplier bill against the agreed price, and flags each bill that is higher.',
    'reads': 'New supplier bills, and the agreed price list', 'to': 'The buyer and the Stores Lead, at 8 AM',
    'slip': [('Bill 4471 · IV cannulas', ''), ('Paid', '₹48 each'), ('Agreed price', '₹40 each'), ('Above the agreed price', '₹800')]},
   {'name': 'Reorder helper', 'hour': 6, 'when': 'Every morning at 6 AM', 'fix': 'A lowest level for each item', 'pt': 2,
    'does': 'Reads the stock count, and orders by itself when an item reaches its lowest level.',
    'reads': 'This morning’s stock count, and each item’s lowest level', 'to': 'The supplier, with a copy to the Stores Lead',
    'slip': [('Ward 3 · Gloves', ''), ('In stock', '40 boxes'), ('Lowest level', '60 boxes'), ('Ordered', '200 boxes')]},
   {'name': 'Bill matcher', 'hour': 21, 'when': 'Every evening at 9 PM', 'fix': 'Bill each item at the bedside',
    'does': 'Matches what each ward used today with what its patients were billed, and lists what is missing.',
    'reads': 'The ward’s use for the day, and the day’s patient bills', 'to': 'The billing desk, before the night shift',
    'slip': [('Ward 5 · IV cannulas', ''), ('Used today', '12'), ('Billed', '8'), ('Still to bill', '4')]},
  ],
  'pending': [
   {'text': 'Agree the first fix, so its helper can be built.', 'pt': 1},
   {'text': 'Find out where supplier bills are kept today.', 'need': 'Needs a word with your accounts team'},
   {'text': 'Check whether the stock count can be read each morning.'},
  ],
  'actions': {'go': {'detail': 'Agree the first fix in Solutions', 'say': 'Let’s agree the first fix so its helper can be built'},
              'add': {'detail': 'Tell Tojo about your systems', 'say': 'Here is how our bills and stock are kept today: '},
              'jump': {'tab': 'Processes', 'detail': 'See the changes for people', 'say': 'Take me to Processes'}},
  'chat': {'text': ['Three helpers are planned, one for each fix. None is built yet.', 'Each runs at a set hour and sends one short slip to one person.'],
           'pointer': 'Pick a point to add to it, or tap a helper.',
           'note': 'One job, one hour, one slip.',
           'points': [{'n': 1, 'label': 'Price watch'}, {'n': 2, 'label': 'Reorder helper'}],
           'prompts': ['Where are our bills kept?', 'Can these work with our software?', 'Show me the people changes']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Helpers are placed on the day here once a fix is agreed. Each one does one job at a set hour.',
  'helpers': [],
  'pending': [{'text': 'Agree a fix in Solutions first.'}, {'text': 'Find out where bills and stock counts are kept today.'}],
  'actions': {'go': {'detail': 'Agree a fix first', 'say': 'Take me to Solutions to agree a fix'},
              'add': {'detail': 'Tell Tojo about your systems', 'say': 'Here is how our bills and stock are kept today: '},
              'jump': {'tab': 'Processes', 'detail': 'Fills in once a fix is agreed', 'say': 'Take me to Processes'}},
  'chat': {'text': ['This is Automations. Helpers are planned here once a fix is agreed.'],
           'note': 'A helper follows a fix.', 'points': [],
           'prompts': ['Take me to Solutions', 'What does a helper do?', 'Do we need new software?']},
 },
}

def au_canvas(state):
    d = AU[state]; empty = state == 'empty'
    marks = ''.join('<span class="au-mk" style="left:%.2f%%"%s><b>%d</b></span>' % (
        h['hour'] / 24 * 100, pt(h.get('pt')), i + 1) for i, h in enumerate(d['helpers']))
    marks += '<span class="au-lbls" aria-hidden="true">%s</span>' % ''.join('<span style="left:%.2f%%">%s</span>' % (
        h['hour'] / 24 * 100, e(h['when'].split(' at ')[1])) for h in d['helpers'])
    ticks = ''.join('<span style="left:%.2f%%">%s</span>' % (h / 24 * 100, l) for h, l in [(0, '12 AM'), (6, '6 AM'), (12, '12 PM'), (18, '6 PM'), (24, '12 AM')])
    day = ('<div class="au-day%s" role="img" aria-label="%s"><div class="au-bar"><i class="au-night1"></i><i class="au-light"></i><i class="au-night2"></i>%s</div>'
           '<div class="au-ticks" aria-hidden="true">%s</div></div>') % (
        ' is-empty' if empty else '', e('; '.join('%s runs %s' % (h['name'], h['when'].lower()) for h in d['helpers']) or 'No helpers placed yet'), marks, ticks)
    cards, desk = [], []
    for i, h in enumerate(d['helpers']):
        k = str(i); first = i == 0
        lamps = ''.join('<span class="au-lp"><i aria-hidden="true"></i>%s</span>' % e(l) for l in LAMPS)
        slip = ''.join('<div class="au-sl%s"><span>%s</span><b>%s</b></div>' % (' au-sl-h' if not v else '', e(a), e(v)) for a, v in h['slip'])
        cards.append(('<button class="au-card %s" type="button"%s%s><span class="au-ch"><span class="au-no">%d</span><span class="au-nm">%s</span></span>'
                      '<span class="au-when">%s</span><span class="au-does">%s</span><span class="au-lamps">%s</span>'
                      '<span class="au-slip" aria-label="The slip it would send"><span class="au-slk">The slip it would send</span>%s</span>%s</button>') % (
            sel_cls(first), sel('au', k, first), pt(h.get('pt')), i + 1, e(h['name']), e(h['when']), e(h['does']), lamps, slip, CHEV))
        det = ('<div class="fx-box"><div class="fx-bh"><h4>%s</h4><span class="fx-chip c-none">Not built yet</span></div><p>%s</p>'
               '<div class="fx-two"><div><span class="fx-lab">What it reads</span><p>%s</p></div><div><span class="fx-lab">Who gets the slip</span><p>%s</p></div></div>'
               '<div class="fx-two"><div><span class="fx-lab">When it runs</span><p>%s</p></div><div><span class="fx-lab">What it waits for</span><p>The fix: %s</p></div></div></div>') % (
            e(h['name']), e(h['does']), e(h['reads']), e(h['to']), e(h['when']), e(h['fix']))
        cards.append(box('au', k, det, first, 'mob'))
        desk.append(box('au', k, det, first, 'desk'))
    if empty:
        cards = ['<div class="au-card is-empty"><span class="au-no">%d</span><span class="au-does">Placed here once a fix is agreed</span></div>' % n for n in (1, 2, 3)]
    body = day + ('<div class="au-key" aria-hidden="true"><span><i class="k-n"></i>Night</span><span><i class="k-d"></i>Day</span><span><i class="k-l"></i>Not switched on yet</span></div>' if not empty else '') + \
        '<div class="au-cards%s">%s</div>' % (' is-empty' if empty else '', ''.join(cards)) + ('<div class="au-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'Each helper sits at the hour it runs. Tap a helper to read it.' if not empty else 'Each helper will sit at the hour it runs'
    return (masthead('Automations', state) + standing(d['claim'], d['deck'], empty)
            + section('The helpers’ day', body, 'au-sec', sub) + pending(d['pending']) + actions(d['actions']))

AU_CSS = r'''
.au-day{padding:6px 0 0}
.au-bar{position:relative;display:flex;height:46px;margin:34px 0 0}
.au-bar>i{display:block;height:100%}
.au-night1{flex:6;background:var(--ink)}.au-light{flex:13;background:var(--card);box-shadow:inset 0 0 0 1px var(--line)}.au-night2{flex:5;background:var(--ink)}
.au-mk{position:absolute;top:-34px;bottom:0;width:34px;display:flex;flex-direction:column;align-items:center;transform:translateX(-50%)}
.au-mk b{font:400 22px/1 var(--f-d);width:30px;height:30px;display:flex;align-items:center;justify-content:center;background:var(--hi);color:var(--ink);box-shadow:0 0 0 2px var(--ink)}
.au-mk::after{content:"";flex:1;border-left:3px solid var(--hi);margin-top:2px}
.au-lbls{position:absolute;left:0;right:0;top:0;bottom:0;pointer-events:none}
.au-lbls span{position:absolute;top:14px;transform:translateX(6px);font-size:12px;font-weight:600;white-space:nowrap;color:var(--card);background:var(--ink);padding:1px 6px}
.au-ticks{position:relative;height:22px;margin-top:6px}
.au-ticks span{position:absolute;transform:translateX(-50%);font-size:12px;color:var(--mut);white-space:nowrap}
.au-ticks span:first-child{transform:none}.au-ticks span:last-child{transform:translateX(-100%)}
.au-day.is-empty .au-bar>i{background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey)}
.au-key{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:12.5px;color:var(--mut);margin-top:4px}
.au-key span{display:inline-flex;align-items:center;gap:7px}.au-key i{width:18px;height:10px}
.au-key .k-n{background:var(--ink)}.au-key .k-d{background:var(--card);box-shadow:inset 0 0 0 1px var(--line)}.au-key .k-l{box-shadow:inset 0 0 0 1.5px var(--grey)}
.au-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:20px;align-items:start}
.au-card{display:flex;flex-direction:column;align-items:flex-start;gap:9px;text-align:left;border:0;background:var(--card);border-top:6px solid var(--ink);padding:14px 16px 16px;color:var(--ink);min-width:0;position:relative}
.au-ch{display:flex;align-items:center;gap:10px}
.au-no{font:400 22px/1 var(--f-d);width:28px;height:28px;display:flex;align-items:center;justify-content:center;background:var(--hi);color:var(--ink)}
.au-nm{font:400 28px/1 var(--f-d)}
.au-when{font-size:12.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.au-does{font-size:14px;line-height:1.5}
.au-lamps{display:flex;flex-wrap:wrap;gap:4px 12px}
.au-lp{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;font-weight:600;color:var(--mut)}
.au-lp i{width:10px;height:10px;border-radius:50%;box-shadow:inset 0 0 0 1.5px var(--grey)}
.au-slip{align-self:stretch;display:flex;flex-direction:column;gap:3px;background:var(--soft);padding:12px 12px 16px;-webkit-mask:var(--zigb);mask:var(--zigb);margin-top:2px}
.au-slk{font-size:11px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut);padding-bottom:4px;border-bottom:2px dashed var(--grey);margin-bottom:3px}
.au-sl{display:flex;justify-content:space-between;gap:8px;font-size:12.5px;line-height:1.4}
.au-sl b{font-weight:600;white-space:nowrap}
.au-sl-h span{font-weight:600}
.au-sl:last-child{border-top:1px solid var(--line);padding-top:3px;margin-top:2px}.au-sl:last-child b{color:var(--hi-text)}
.au-card .sel-chev{position:absolute;right:16px;top:20px;margin:0}
.au-card.is-empty{background:transparent;border:2px dashed var(--grey);border-top:6px solid var(--grey);color:var(--mut)}
.au-desk{margin-top:18px}
@container lp (max-width:699px){
 .au-lbls{display:none}
 .au-cards{grid-template-columns:1fr;gap:12px}
 .au-card{padding:14px 44px 16px 16px}
 .au-card .sel-chev{display:inline-block}
 .au-cards .bx-mob{margin:-4px 0 6px}
 .au-ticks span:nth-child(2),.au-ticks span:nth-child(4){font-size:11px}
}
'''

# ==========================================================================================
# PROCESSES · the week planner
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
PR = {
 'filled': {
  'claim': 'Four small changes to the week, and one new role',
  'deck': 'Nothing is tried yet. Each change waits for its fix to be agreed. We start with a four-week trial on two wards.',
  'changes': [
   {'name': 'Ward shelves checked', 'days': [0], 'time': '10 AM, 30 minutes', 'who': 'Each ward sister', 'pt': 1,
    'what': 'Every Monday, each ward counts its shelves against the lowest levels and sends the count to the store.',
    'why': 'Stops the Thursday-night rush buys: the store orders on Monday, long before a ward runs out.'},
   {'name': 'Buying meeting', 'days': [2], 'time': '3 PM, 45 minutes', 'who': 'Buyer, Stores Lead, one doctor', 'pt': 2,
    'what': 'Once a week, the buyer brings every bill above the agreed price and every rushed buy. Each one gets a reason or a fix.',
    'why': 'Keeps the agreed prices alive. A price that no one checks drifts back up within months.'},
   {'name': 'Ten-minute look at the numbers', 'days': list(range(7)), 'time': '9 AM, 10 minutes', 'who': 'Stores Lead, with the buyer',
    'what': 'Every morning, the Stores Lead reads yesterday’s slips from the helpers: bills above the price, orders sent, items not billed.',
    'why': 'Small gaps are caught the next morning, not at the month’s end.'},
   {'name': 'Every rushed buy signed', 'days': None, 'time': 'Any time, 2 minutes', 'who': 'The Stores Lead (new role)', 'pt': 3,
    'what': 'No one buys from a local shop unless the Stores Lead signs for it, and says why the shelf ran out.',
    'why': 'Each rushed buy becomes a lesson for the lowest levels, and the habit stops.'},
  ],
  'roles': [
   {'role': 'Stores Lead', 'new': True, 'signs': 'Every rushed buy, and the morning numbers'},
   {'role': 'Buyer', 'signs': 'Agreed prices, and every bill above them'},
   {'role': 'Ward sister', 'signs': 'The Monday shelf count'},
   {'role': 'Billing desk', 'signs': 'Items used but not yet billed, each evening'},
  ],
  'numbers': [
   {'name': 'Rushed buys a month', 'now': 'About 60', 'goal': 'Under 15', 'pt': 3},
   {'name': 'Bills above the agreed price', 'now': '1 in 3', 'goal': 'None'},
   {'name': 'Items used but not billed', 'now': '1 in 10', 'goal': '1 in 50'},
   {'name': 'Expired each month', 'now': '₹3 lakh', 'goal': 'Under ₹1 lakh'},
  ],
  'pending': [
   {'text': 'Name the Stores Lead, and who stands in for them.', 'need': 'Needs your choice of person', 'pt': 3},
   {'text': 'Pick the two wards for the four-week trial.'},
   {'text': 'Agree the time of the weekly buying meeting.', 'pt': 2},
  ],
  'actions': {'go': {'detail': 'Name the Stores Lead', 'say': 'Let’s name the Stores Lead'},
              'add': {'detail': 'Tell Tojo about your team', 'say': 'Here is who handles buying and stores today: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Back to where the work stands', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Four changes to the week are planned, and one new role: a Stores Lead.', 'Nothing is tried yet. A four-week trial on two wards comes first.'],
           'pointer': 'Pick a point to add to it, or tap a change on the week.',
           'note': 'One person signs. The habit changes.',
           'points': [{'n': 1, 'label': 'Monday shelf count'}, {'n': 2, 'label': 'The buying meeting'}, {'n': 3, 'label': 'The Stores Lead'}],
           'prompts': ['Our store keeper could be the Stores Lead', 'Which wards should trial it?', 'How long does this take each week?']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Changes are pinned on the week here once a fix is agreed: who does what, on which day, and the numbers we watch.',
  'changes': [], 'roles': [], 'numbers': [],
  'pending': [{'text': 'Agree a fix in Solutions first.'}, {'text': 'Tell Tojo who handles buying and stores today.'}],
  'actions': {'go': {'detail': 'Agree a fix first', 'say': 'Take me to Solutions to agree a fix'},
              'add': {'detail': 'Tell Tojo about your team', 'say': 'Here is who handles buying and stores today: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Every conversation starts here', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['This is Processes. Changes for people are planned here once a fix is agreed.'],
           'note': 'People first. Then the habit.', 'points': [],
           'prompts': ['Take me to Solutions', 'Who usually does what?', 'What is a Stores Lead?']},
 },
}

def pr_canvas(state):
    d = PR[state]; empty = state == 'empty'
    # the week: one column per day, changes pinned on their days; daily and any-day changes run as strips
    cols = ''.join('<div class="pw-d"><span class="pw-dn">%s</span></div>' % dd for dd in DAYS)
    items, desk, mob = [], [], []
    for i, c in enumerate(d['changes']):
        k = str(i); first = i == 0
        if c['days'] is None:
            span, where, cls = 'grid-column:1/-1', 'Any day', 'pw-any'
        elif len(c['days']) == 7:
            span, where, cls = 'grid-column:1/-1', 'Every day', 'pw-daily'
        else:
            span, where, cls = 'grid-column:%d' % (c['days'][0] + 1), DAYS[c['days'][0]], 'pw-one'
        inner = '<span class="pw-when">%s · %s</span><b class="pw-nm">%s</b><span class="pw-who">%s</span>%s' % (
            e(where), e(c['time']), e(c['name']), e(c['who']), CHEV)
        btn = '<button class="pw-c %s %s" type="button" style="%s"%s%s>%s</button>' % (cls, sel_cls(first), span, sel('pw', k, first), pt(c.get('pt')), inner)
        det = ('<div class="fx-box"><div class="fx-bh"><h4>%s</h4><span class="fx-chip c-none">Not tried yet</span></div><p>%s</p>%s</div>') % (
            e(c['name']), e(c['what']), two('Who and when', '%s · %s · %s' % (c['who'], where, c['time']), 'Why it helps', c['why']))
        items.append((btn, box('pw', k, det, first, 'mob')))
        desk.append(box('pw', k, det, first, 'desk'))
    if empty:
        week = '<div class="pw-week is-empty"><div class="pw-days">%s</div><p class="pw-wait">Changes are pinned on their days once a fix is agreed.</p></div>' % cols
    else:
        pins = ''.join('%s%s' % (b, m) for b, m in items)
        week = ('<div class="pw-week"><div class="vf-rings pw-rings" aria-hidden="true">%s</div><div class="pw-days">%s</div><div class="pw-grid">%s</div>'
                '<div class="pw-trial"><b>Trial</b><span>Four weeks on two wards</span><span class="pw-wk">%s</span></div></div>') % (
            '<i></i>' * 7, cols, pins, ''.join('<i>Week %d</i>' % n for n in range(1, 5)))
    body = week + ('<div class="pw-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'The changes, pinned on the days they happen. Tap a change.' if not empty else 'The changes, pinned on their days'
    # signature register
    if d['roles']:
        regs = ''.join('<div class="pr-sig"><span class="pr-role"><b>%s</b>%s</span><span class="pr-signs">Signs for: %s</span><span class="pr-line" aria-hidden="true"></span></div>' % (
            e(r['role']), '<span class="fx-chip c-now">New role</span>' if r.get('new') else '', e(r['signs'])) for r in d['roles'])
        reg = '<div class="pr-reg">%s</div>' % regs
        nums = ''.join('<div class="pr-num"%s><span class="pr-nn">%s</span><span class="pr-nv"><b>%s</b><span>now</span></span><span class="pr-ng"><b>%s</b><span>goal</span></span></div>' % (
            pt(n.get('pt')), e(n['name']), e(n['now']), e(n['goal'])) for n in d['numbers'])
        numsec = '<div class="pr-nums">%s</div><p class="fx-hint">Now: Example only. Goals: Tojo’s guess, to agree with you.</p>' % nums
        extra = (section('Who signs for what', reg, 'pr-sec-reg', 'One line per role. The new role is marked.')
                 + section('The numbers we watch', numsec, 'pr-sec-num', 'Read every morning in the ten-minute look'))
    else:
        extra = section('Who signs for what', '<p class="fx-empty">Roles are written here once a change is agreed.</p>', 'pr-sec-reg')
    return (masthead('Processes', state) + standing(d['claim'], d['deck'], empty)
            + section('The week, once the changes are in', body, 'pw-sec', sub) + extra + pending(d['pending']) + actions(d['actions']))

PR_CSS = r'''
.pw-week{position:relative;background:var(--card);border-top:6px solid var(--ink);padding:26px 16px 16px;
 background-image:repeating-linear-gradient(transparent 0 31px,var(--line) 31px 32px);background-position:0 62px}
.pw-rings{position:absolute;left:24px;right:24px;top:-12px;bottom:auto;width:auto;height:18px;margin:0;flex-direction:row}
.pw-rings i{width:9px;height:18px}
.pw-days,.pw-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:6px}
.pw-days{border-bottom:3px double var(--ink);padding-bottom:6px}
.pw-dn{font:400 22px/1 var(--f-d);color:var(--mut)}
.pw-grid{margin-top:12px;row-gap:10px;grid-auto-flow:row dense}
.pw-c{display:flex;flex-direction:column;align-items:flex-start;gap:3px;text-align:left;border:0;background:var(--soft);border-left:5px solid var(--ink);padding:9px 12px;color:var(--ink);min-width:0;position:relative}
.pw-one{grid-row:1}
.lp .pw-daily{color:var(--card)}
.pw-daily{background:var(--ink);border-left-color:var(--hi);flex-direction:row;align-items:baseline;flex-wrap:wrap;column-gap:14px}
.pw-daily .pw-when,.pw-daily .pw-who{color:var(--line)}
.pw-any{background:transparent;box-shadow:inset 0 0 0 2px var(--ink);border-left-color:var(--hi);flex-direction:row;align-items:baseline;flex-wrap:wrap;column-gap:14px}
.pw-when{font-size:11.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.pw-nm{font:400 24px/1 var(--f-d)}
.pw-who{font-size:13px;color:var(--mut)}
.pw-c .sel-chev{position:absolute;right:12px;top:14px;margin:0}
.pw-trial{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:14px;padding-top:10px;border-top:3px double var(--ink);font-size:13.5px}
.pw-trial b{font:400 22px/1 var(--f-d)}
.pw-wk{display:flex;gap:4px;margin-left:auto}
.pw-wk i{font-style:normal;font-size:12px;font-weight:600;padding:3px 10px;box-shadow:inset 0 0 0 1.5px var(--grey);color:var(--mut)}
.pw-week.is-empty{background:transparent;background-image:none;border:2px dashed var(--grey);border-top:6px solid var(--grey)}
.pw-wait{font-size:14px;color:var(--mut);padding:18px 0 4px}
.pw-desk{margin-top:18px}
/* signature register */
.pr-reg{display:flex;flex-direction:column;background:var(--card);border-top:6px solid var(--ink)}
.pr-sig{display:grid;grid-template-columns:220px minmax(0,1fr) 180px;align-items:end;gap:16px;padding:12px 16px;border-bottom:1px solid var(--line)}
.pr-role{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.pr-role b{font:400 24px/1 var(--f-d)}
.pr-signs{font-size:14px;line-height:1.45}
.pr-line{height:24px;border-bottom:2px dashed var(--ink);position:relative}
.pr-line::after{content:"Signature";position:absolute;left:0;bottom:-18px;font-size:10.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--mut)}
.pr-sig{padding-top:8px;padding-bottom:18px}
/* numbers */
.pr-nums{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.pr-num{display:flex;flex-direction:column;gap:8px;background:var(--card);padding:14px 16px;border-top:6px solid var(--hi);min-width:0}
.pr-nn{font-size:14px;font-weight:600;line-height:1.35}
.pr-nv,.pr-ng{display:flex;align-items:baseline;flex-wrap:wrap;gap:2px 8px}
.pr-nv b,.pr-ng b{font:400 26px/1 var(--f-d)}
.pr-nv span,.pr-ng span{font-size:12px;font-weight:600;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
.pr-ng b{color:var(--hi-text)}
.pr-ng{border-top:1px solid var(--line);padding-top:8px}
@container lp (max-width:699px){
 .pw-week{padding:22px 12px 14px;background-position:0 0}
 .pw-days{display:none}
 .pw-grid{grid-template-columns:1fr;row-gap:10px}
 .pw-c{grid-column:1 !important;grid-row:auto !important;min-height:0;padding-right:40px}
 .pw-daily,.pw-any{flex-direction:column;align-items:flex-start}
 .pw-c .sel-chev{display:inline-block}
 .pw-grid .bx-mob{margin:-4px 0 4px}
 .pw-wk{margin-left:0}
 .pr-sig{grid-template-columns:1fr;gap:6px}
 .pr-nums{grid-template-columns:1fr 1fr}
 .pr-nv b,.pr-ng b{font-size:26px}
}
'''

# ==========================================================================================
PAGES = {
 'home': (None, None, 'Home', 'The notebook (approved)'),
 'diagnosis': ('Diagnosis', (dg_canvas, DG_CSS, DG), 'Diagnosis', 'The item’s receipt'),
 'solutions': ('Solutions', (so_canvas, SO_CSS, SO), 'Solutions', 'The ledger of fixes'),
 'automations': ('Automations', (au_canvas, AU_CSS, AU), 'Automations', 'The helpers’ day'),
 'processes': ('Processes', (pr_canvas, PR_CSS, PR), 'Processes', 'The week planner'),
}
ABOUT = {
 'home': ('<b>Home · The notebook.</b> Approved as sample F. The month’s receipt stapled on; the parts on the left page of an open notebook, the open part on the right. '
          '<em>Colours: report white, black, lime. The rail now carries each place’s own colour.</em>'),
 'diagnosis': ('<b>Diagnosis · The item’s receipt.</b> One item followed from the ward’s request to the patient’s bill, every loss printed as a line on a till receipt, '
               'its line opening beside it. Under it, the four causes weighed as report bars, the leading one in ink. <em>Elements from B (receipt) and C (report bars). '
               'Colours: steel, navy ink, signal orange.</em>'),
 'solutions': ('<b>Solutions · The ledger of fixes.</b> One ruled entry per fix with a double margin, its four stops ticked across, what it brings back in the money column, '
               'and a double-ruled total. Each entry opens to its by-hand and automatic versions side by side. <em>Elements from A (ledger) and C (figures). '
               'Colours: lilac, deep violet ink, violet.</em>'),
 'automations': ('<b>Automations · The helpers’ day.</b> A flat 24-hour bar, night in ink, each helper pinned at the hour it runs; under it, one card per helper with its lamps '
                 'and the slip it would print. <em>Elements from C (flat bar) and B (printed slips). Colours: mint, deep green ink, coral.</em>'),
 'processes': ('<b>Processes · The week planner.</b> A ruled notebook week with the changes pinned on their days, the daily look as a strip across the week, the trial at the foot; '
               'then a signature register for who signs for what, and the numbers we watch, now against goal. <em>Elements from A and F (notebook), and C (figures). '
               'Colours: sand, deep brown ink, sky blue.</em>'),
}

def build():
    os.makedirs(OUT, exist_ok=True)
    pages, words = {}, []
    for k, (place, spec, label, title) in PAGES.items():
        t = THEMES[k]
        for st in ('filled', 'empty'):
            if spec is None:
                canvas, css, chat, cls = L2.f_canvas(st), L2.V_SHARED_CSS + L2.F_CSS, HOME_DATA[st]['chat'], 'sc sc-home vf'
            else:
                fn, pcss, data = spec
                canvas, css, chat, cls = fn(st), L2.V_SHARED_CSS + L2.F_CSS + PLACE_CSS + pcss, data[st]['chat'], 'sc sc-%s' % k
            for v in ('desktop', 'mobile'):
                h = C.page(SK, t, place, canvas, css, chat, v, 'Supply Chain and Procurement · %s' % label, cls)
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(OUT, 'scp-%s.%s.%s.html' % (k, v, st)), 'w', encoding='utf-8').write(h)
            words += [(k, st, w) for w in C.plain_check(re.sub(r'<[^>]+>', ' ', canvas) + ' ' + json.dumps(chat, ensure_ascii=False))]
    return pages, words

def review(pages):
    tpl = open(os.path.join(HERE, 'review_template.html'), encoding='utf-8').read()
    tpl = tpl.replace('the home page in three looks', 'the five landing pages')
    tpl = re.sub(r'<p class="rv-intro">.*?</p>', '<p class="rv-intro">The tool’s home page (the notebook, approved) and its four place pages, all in the Financial look: '
                 'the Virevo type unchanged, the flat frame, and the three papers of money (report sheet, ledger paper, receipt). Each place has its own colours and its own drawing. '
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
    rv = os.path.join(OUT, 'supply-chain-landing-pages.html')
    open(rv, 'w', encoding='utf-8').write(review(pages))
    print('built', rv, os.path.getsize(rv))
