"""
Bed Management · Diagnosis turns, drawn in the Diagnosis look (the night round: pale blue-grey,
deep navy, plan paper, door plates, the small bed). Source: the approved Nagpur transcript,
`bed-management-sample-chat-transcript.md`, turns 7 to 16, plus the diagnosis turn the practice
run left out (playbook §2). Chat text is the approved text, word for word.

Each turn: one review file with the desktop screen and the phone screen, both live.
Run:  python3 dg_turns.py [turn ids...]  -> out/bed-management/turns/diagnosis/
"""
import html, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BM = os.path.dirname(HERE)
sys.path.insert(0, BM); sys.path.insert(0, os.path.join(BM, 'diagnosis'))
import bm_common as C
from bm_common import e, ico, SEND, bed_svg, BED_CSS, tag, sel, sel_cls, box, CHEV, desktop, mobile, embedded_fonts, SHELL_CSS, shell_css, SHELL_V3_CSS, BASE_CSS, SEL_CSS, JS, SEL_JS
from preview import chat_parts
import diagnosis as D

T = D.THEME
OUT = os.path.join(C.ROOT, 'out', 'bed-management', 'turns', 'diagnosis')

# ------------------------------------------------------------------------------------------
# Shared turn parts
def heading(eyebrow, title, deck):
    return '<header class="tn-head"><div class="tn-eye">%s</div><h2 class="tn-title">%s</h2><p class="tn-deck">%s</p></header>' % (e(eyebrow), e(title), e(deck))

def divider(text):
    return '<p class="tn-div">%s</p>' % e(text)

def effect(label, value, sub, state=''):
    return '<div class="tn-eff %s"><span class="tn-el">%s</span><span class="tn-ev">%s</span><span class="tn-es">%s</span></div>' % (state, e(label), e(value), e(sub))

TURN_CSS = BED_CSS + '''
.tn{padding:26px 40px 48px;color:var(--ink);display:flex;flex-direction:column;gap:26px;--gold:#d4a94f;--dgold:#6B4F16;--amber:#8A5608;--green:#2F6B4F;--red:#8E2F1C}
.tn-head{display:flex;flex-direction:column;gap:8px;max-width:760px}
.tn-eye{font-size:12.5px;font-weight:600;color:var(--acc)}
.tn-title{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:52px;line-height:.98;margin:0;text-wrap:balance}
.tn-deck{font-size:15.5px;line-height:1.55;color:var(--mut);margin:0}
.tn-div{margin:0;border-top:1.5px dashed var(--mut);padding-top:10px;font-size:14.5px;font-style:italic;line-height:1.5;color:var(--mut)}
.tn-eff{display:flex;flex-direction:column;gap:4px;padding:18px 22px;background:var(--soft);border:2px solid var(--ink);border-radius:6px}
.tn-eff.outcome{border-color:var(--red)}.tn-eff.outcome .tn-ev{color:var(--red)}
.tn-el{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.tn-ev{font-family:'Bebas Neue',sans-serif;font-size:36px;line-height:1}
.tn-es{font-size:14px;line-height:1.5;color:var(--ink)}
.tn-hint{font-size:12.5px;color:var(--mut);font-style:italic;margin:-14px 0 0}
.sh-um{max-width:330px}
@container lp (max-width:699px){
 .tn{padding:20px 16px 32px;gap:22px}
 .tn-title{font-size:40px}
 .tn-deck{font-size:14.5px}
 .tn-ev{font-size:30px}
}
'''

def chat_block(turn):
    um = '<div class="sh-um">%s</div>' % e(turn['user'])
    return um + chat_parts(turn['chat'])

FONTS = []
def page(turn, view):
    if not FONTS: FONTS.append(embedded_fonts())
    canvas = '<div class="lp-host"><div class="lp tn" style="%s">%s</div></div>' % (T['vars'], turn['canvas']())
    body = desktop(T, 'Diagnosis', canvas, chat_block(turn)) if view == 'desktop' else mobile(T, 'Diagnosis', canvas, chat_block(turn))
    css = TURN_CSS + turn.get('css', '')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title>%s<style>%s%s%s%s%s%s .bm-app .sh-bar{background:%s}</style></head><body>%s<script>%s%s</script></body></html>') % (
        e(turn['id']), FONTS[0], SHELL_CSS, shell_css(T), SHELL_V3_CSS, BASE_CSS, SEL_CSS, css, T['ground'], body, JS, SEL_JS)

# ------------------------------------------------------------------------------------------
# bm-dg-01 · transcript turn 7 · the case reveal: a comparable hospital's day as a revenue clock
T7_STOPS = [
 {'k': 'a', 'when': 'Late morning', 'title': 'Final bill closed', 'bed': 'in', 'state': 'plain',
  'line': 'Sent for insurance approval.', 'bill': 'The bill stops here. Nothing more is charged to this bed.',
  'detail': 'The outgoing patient’s final bill is closed and sent for insurance approval. From this moment nothing new is charged against this bed.'},
 {'k': 'b', 'when': 'Afternoon', 'title': 'Approval, payment, family briefing', 'bed': 'in', 'state': 'plain',
  'line': 'The patient is still in the bed.', 'bill': 'Still nothing billing, with the bed still in use.',
  'detail': 'Approval comes through, the family pays and is briefed. All this time the patient is still in the bed, and the bed earns nothing.'},
 {'k': 'c', 'when': 'Evening', 'title': 'Patient leaves, bed turned around', 'bed': 'empty', 'state': 'plain',
  'line': 'Housekeeping cleans and readies it.', 'bill': 'The bed is empty now. Still nothing billing.',
  'detail': 'The patient finally leaves. Housekeeping cleans the bed and readies it for the next patient.'},
 {'k': 'd', 'when': 'Later still', 'title': 'Next patient admitted', 'bed': 'next', 'state': 'outcome',
  'line': 'Only now does a new bill open.', 'bill': 'The bed starts earning again.',
  'detail': 'The next patient is admitted. Only now does a new bill open, and the bed starts earning again.'},
]
def t7_canvas():
    stops, desk = [], []
    for i, s in enumerate(T7_STOPS):
        first = i == 0
        bedcls = {'in': 's-done', 'empty': 'db-dirty', 'next': 's-done'}[s['bed']]
        inner = '<div class="rc-box"><span class="rc-bw">%s</span><b>%s</b><p>%s</p><p class="rc-bill">%s</p></div>' % (e(s['when']), e(s['title']), e(s['detail']), e(s['bill']))
        stops.append('<button class="rc-stop %s is-%s" type="button"%s><span class="rc-when">%s</span><span class="bmb %s">%s</span><b class="rc-t">%s</b><span class="rc-l">%s</span>%s</button>%s' % (
            sel_cls(first), s['state'], sel('rc', s['k'], first), e(s['when']), bedcls, bed_svg(40), e(s['title']), e(s['line']), CHEV, box('rc', s['k'], inner, first, 'mob')))
        desk.append(box('rc', s['k'], inner, first, 'desk'))
    clock = ('<div class="rc-clock" aria-label="Billing on this bed: running before late morning, nothing from late morning until the next patient is admitted">'
             '<span class="rc-on">Billing</span><span class="rc-off">Nothing bills on this bed</span><span class="rc-on rc-on2">Billing again</span></div>')
    plan = '<div class="rc-plan bm-paper"><div class="rc-row">%s</div>%s</div>' % (''.join(stops), clock)
    return (heading('A hospital much like yours', 'The bed that stopped earning', 'One bed through one day. Watch where the bill stops, and how long it stays stopped.')
            + plan + '<p class="tn-hint">Tap a step to see what happens there.</p>' + '<div class="rc-desk">%s</div>' % ''.join(desk)
            + divider('Nothing bills on this bed across this whole stretch — pharmacy, diagnostics and procedures included.')
            + effect('Dead bed time', 'Last bill closed to next bill opened', 'Often half a day or more on one bed — and a number most hospitals have never isolated.', 'outcome'))

T7_CSS = '''
.rc-plan{border:3px solid var(--ink);border-radius:4px;padding:0 0 18px}
.rc-row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))}
.rc-stop{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:8px;text-align:left;background:var(--card);border:0;border-right:2px solid var(--ink);border-bottom:2.5px solid var(--ink);padding:16px 16px 20px;min-width:0}
.rc-stop:last-child{border-right:0}
.rc-when{font-size:12.5px;font-weight:600;color:var(--acc)}
.rc-t{font-size:15px;line-height:1.35}
.rc-l{font-size:13px;line-height:1.45;color:var(--mut)}
.rc-stop.is-outcome{box-shadow:inset 0 0 0 2.5px var(--red)}
.rc-stop.is-outcome .rc-t{color:var(--red)}
.lp .rc-stop.is-up{background:#FFF8E6}
.bmb.db-dirty svg .f{stroke:var(--amber);stroke-dasharray:4 3}.bmb.db-dirty svg .h{fill:var(--amber)}.bmb.db-dirty svg .p{stroke:var(--amber)}
.rc-clock{display:grid;grid-template-columns:.5fr 3fr .5fr;margin:18px 14px 0;font-size:12.5px;font-weight:600}
.rc-on{padding:8px 10px;background:var(--ink);color:var(--card);border-radius:4px 0 0 4px}
.rc-on2{border-radius:0 4px 4px 0;text-align:right}
.rc-off{padding:8px 12px;text-align:center;color:var(--red);border:2px dashed var(--red);border-left:0;border-right:0;background:repeating-linear-gradient(135deg,rgba(142,47,28,.08) 0 6px,transparent 6px 12px)}
.rc-desk .rc-box{padding:18px 22px;background:var(--card);border:2px solid var(--ink);border-left:6px solid #d4a94f;border-radius:6px}
.rc-box{display:flex;flex-direction:column;gap:6px}
.rc-bw{font-size:12px;font-weight:600;color:var(--acc)}.rc-box b{font-size:16px}.rc-box p{margin:0;font-size:14.5px;line-height:1.5}
.rc-bill{font-weight:600;color:var(--red)}
.rc-desk{margin-top:-10px}
.rc-row .bx-mob{background:var(--card);border-left:2px solid var(--ink);border-top:2px solid var(--ink);border-radius:4px;margin:0 12px 12px !important;padding:14px 16px}
@container lp (max-width:699px){
 .rc-row{grid-template-columns:1fr}
 .rc-stop{display:grid;grid-template-columns:48px 1fr auto;column-gap:12px;row-gap:4px;border-right:0;padding:14px}
 .rc-stop .bmb{grid-row:1/span 3;grid-column:1}
 .rc-when,.rc-t,.rc-l{grid-column:2}
 .rc-stop .sel-chev{grid-column:3;grid-row:1}
 .rc-clock{grid-template-columns:1fr;margin:14px 12px 0;gap:0}
 .rc-on,.rc-on2{border-radius:4px;text-align:left}
 .rc-off{border:2px dashed var(--red);margin:4px 0}
}
'''

# ------------------------------------------------------------------------------------------
# bm-dg-02 · transcript turn 8 · the agenda: five areas, one question at a time
T8_AREAS = [
 {'k': 'who', 'name': 'Who runs what', 'q': 'Does the same team handle both your discharges and your admissions, or two separate teams?', 'first': True},
 {'k': 'tat', 'name': 'How long an admission takes', 'q': 'The five steps of an admission, and a typical day’s clock time for each.'},
 {'k': 'map', 'name': 'Tomorrow’s bed picture', 'q': 'Is there a mechanism that maps tomorrow’s planned admissions against the beds you expect to free up?'},
 {'k': 'bill', 'name': 'When billing stops and restarts', 'q': 'What time the outgoing patient’s final bill closes, and when the next patient’s first bill opens.'},
 {'k': 'turn', 'name': 'Who turns the bed around', 'q': 'Has anyone worked out how many bed turnovers housekeeping and transport can handle at peak?'},
]
ROOM_ICO = {'who': '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0112 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15 20a5 5 0 016-4.5"/>',
            'tat': '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>',
            'map': '<rect x="4" y="5" width="16" height="15" rx="1"/><path d="M4 10h16M9 5V3M15 5V3"/>',
            'bill': '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
            'turn': '<path d="M4 12a8 8 0 0114-5"/><path d="M18 3v4h-4"/><path d="M20 12a8 8 0 01-14 5"/><path d="M6 21v-4h4"/>'}
def t8_canvas():
    rooms, desk = [], []
    for i, a in enumerate(T8_AREAS):
        first = i == 0
        inner = '<div class="ag-box"><span class="ag-bk">%s</span><p>%s</p><span class="ag-when">%s</span></div>' % (
            e(a['name']), e(a['q']), 'I’m asking this one now.' if first else 'I’ll ask this one later.')
        rooms.append('<button class="ag-room %s%s" type="button"%s><span class="ag-plate">%s</span>%s<b>%s</b>%s</button>%s' % (
            sel_cls(first), ' is-first' if first else '', sel('ag', a['k'], first), ico(ROOM_ICO[a['k']], 'currentColor', 22),
            '<span class="ag-tag">First up</span>' if first else '', e(a['name']), CHEV, box('ag', a['k'], inner, first, 'mob')))
        desk.append(box('ag', a['k'], inner, first, 'desk'))
    plan = '<div class="ag-plan bm-paper"><div class="ag-rooms">%s</div><div class="ag-corr"><span>Five areas, no fixed order between them. One question at a time.</span></div></div>' % ''.join(rooms)
    return (heading('What I need to know', 'Five areas, one question at a time', 'This is where the questions are going, so nothing comes as a surprise.')
            + plan + '<p class="tn-hint">Tap an area to see what I’ll ask there.</p>' + '<div class="ag-desk">%s</div>' % ''.join(desk))

T8_CSS = '''
.ag-plan{border:3px solid var(--ink);border-radius:4px}
.ag-rooms{display:grid;grid-template-columns:repeat(5,minmax(0,1fr))}
.ag-room{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:10px;text-align:left;background:var(--card);border:0;border-right:2px solid var(--ink);padding:18px 16px 22px;min-height:150px;min-width:0}
.ag-room:nth-last-child(2){border-right:0}
.ag-room:last-of-type{border-right:0}
.ag-plate{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:4px;background:var(--ink);color:var(--card)}
.ag-room b{font-size:15px;line-height:1.35}
.ag-tag{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;padding:2px 9px;border-radius:10px;border:1.5px solid var(--green);color:var(--green)}
.ag-room.is-first{box-shadow:inset 0 0 0 2.5px var(--green)}
.lp .ag-room.is-up{background:#FFF8E6}
.ag-corr{border-top:2.5px solid var(--ink);padding:12px 16px;font-size:12.5px;color:var(--mut);background:repeating-linear-gradient(90deg,var(--line) 0 14px,transparent 14px 26px) 0 100%/100% 1.5px no-repeat}
.ag-desk{margin-top:-10px}
.ag-desk .ag-box{padding:18px 22px;background:var(--card);border:2px solid var(--ink);border-left:6px solid #d4a94f;border-radius:6px}
.ag-box{display:flex;flex-direction:column;gap:6px}
.ag-bk{font-size:12px;font-weight:600;color:var(--acc)}.ag-box p{margin:0;font-size:15px;line-height:1.5}.ag-when{font-size:12.5px;color:var(--mut)}
.ag-rooms .bx-mob{background:var(--card);border-left:2px solid var(--ink);border-top:2px solid var(--ink);border-radius:4px;margin:0 12px 12px !important;padding:14px 16px}
@container lp (max-width:699px){
 .ag-rooms{grid-template-columns:1fr}
 .ag-room{display:grid;grid-template-columns:40px 1fr auto;column-gap:12px;align-items:center;min-height:0;border-right:0;border-bottom:2px solid var(--ink);padding:14px}
 .ag-tag{grid-column:2;grid-row:1;justify-self:start}
 .ag-room b{grid-column:2}
 .ag-room .ag-plate{grid-row:1/span 2}
 .ag-room .sel-chev{grid-column:3;grid-row:1/span 2}
}
'''

TURNS = {
 'bm-dg-01': {'id': 'bm-dg-01', 'src': 7, 'name': 'The case reveal',
   'user': 'Yes, beds. That’s the problem I want to work on.',
   'user_note': 'Paraphrased in the transcript: commits to the bed problem.',
   'chat': {'text': ['Beds it is — and what you’ve described lines up closely with a hospital we worked with. Let me show you their day rather than describe it.',
                     'One thing to watch as you read it: that bed stopped earning hours before it was empty.',
                     'Does that look like your day? And is there anything about your own setup you’d add to what’s there?'],
            'note': 'The bed stops earning long before it is empty.',
            'prompts': ['Yes, that is our day', 'Ours is sometimes longer', 'What happens next?']},
   'canvas': t7_canvas, 'css': T7_CSS},
 'bm-dg-02': {'id': 'bm-dg-02', 'src': 8, 'name': 'The questions, and the first one',
   'user': 'Yes, that matches. Ours is sometimes longer. What happens next?',
   'user_note': 'Paraphrased in the transcript: confirms the case matches, adds that their own dead bed time is sometimes longer, asks what happens next.',
   'chat': {'text': ['That’s worth holding on to — and most hospitals can’t say how much longer, because nobody measures that stretch end to end.',
                     'Now I need to pin down how your hospital actually runs it. The graphic has the whole list so you can see where this is going; I’ll take them one at a time rather than dump them on you.',
                     'First one: does the same team handle both your discharges and your admissions, or are those two separate teams?'],
            'note': 'One question at a time.',
            'question': {'text': 'Pick the closest', 'options': ['One team does both', 'Two separate teams', 'It varies by ward / I’d need to check']},
            'prompts': ['Why does that matter?', 'How long will this take?', 'Can I answer these later?']},
   'canvas': t8_canvas, 'css': T8_CSS},
}

# ------------------------------------------------------------------------------------------
REVIEW = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>@@ID@@ · @@NAME@@</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@400;500;600&display=swap">
<style>
body{margin:0;background:#EEF0F4;color:#1C2542;font-family:Poppins,system-ui,sans-serif}
.rv{max-width:1900px;margin:0 auto;padding:22px 20px 60px}
h1{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:40px;line-height:1;margin:0}
.rv-meta{font-size:13.5px;color:#4A536E;margin:6px 0 16px;line-height:1.55;max-width:900px}
.rv-views{display:flex;gap:24px;align-items:flex-start}
.rv-col{display:flex;flex-direction:column;gap:6px;min-width:0}
.rv-lab{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#4A536E}
.rv-desk{flex:1 1 auto}
.rv-dwrap{width:100%;overflow:hidden;border:1.5px solid #C9CEDB;border-radius:10px;background:#fff}
.rv-dwrap iframe{width:1440px;height:900px;border:0;transform-origin:0 0;display:block}
.rv-pwrap{width:390px;border:10px solid #1b1b1b;border-radius:34px;overflow:hidden;background:#fff}
.rv-pwrap iframe{width:390px;height:844px;border:0;display:block}
@media (max-width:1000px){.rv-views{flex-direction:column}}
</style></head><body><div class="rv">
<h1>@@ID@@ · @@NAME@@</h1>
<p class="rv-meta">Bed Management · Diagnosis · transcript turn @@SRC@@. The chat text is the approved transcript, word for word. @@NOTE@@ Each view is one real screen: scroll inside it.</p>
<div class="rv-views">
 <div class="rv-col rv-desk"><div class="rv-lab">Desktop · 1440 × 900, scaled to fit</div><div class="rv-dwrap" id="dwrap"><iframe id="fd" title="Desktop"></iframe></div></div>
 <div class="rv-col"><div class="rv-lab">Phone · 390 × 844</div><div class="rv-pwrap"><iframe id="fm" title="Phone"></iframe></div></div>
</div></div>
<script>
var P=@@DATA@@;var fd=document.getElementById('fd'),fm=document.getElementById('fm'),dw=document.getElementById('dwrap');
function fit(){var sc=Math.min(1,dw.clientWidth/1440);fd.style.transform='scale('+sc+')';dw.style.height=Math.ceil(900*sc)+'px';}
fd.srcdoc=P.desktop;fm.srcdoc=P.mobile;fit();window.addEventListener('resize',fit);
</script></body></html>'''

def build(ids=None):
    os.makedirs(OUT, exist_ok=True)
    made = []
    for k, t in TURNS.items():
        if ids and k not in ids: continue
        pages = {v: page(t, v) for v in ('desktop', 'mobile')}
        for v, h in pages.items(): open(os.path.join(OUT, '%s.%s.html' % (k, v)), 'w').write(h)
        note = 'The hospital’s message is shown as the user bubble. %s' % t['user_note'] if t.get('user_note') else ''
        rv = (REVIEW.replace('@@ID@@', e(k)).replace('@@NAME@@', e(t['name'])).replace('@@SRC@@', str(t['src'])).replace('@@NOTE@@', e(note))
                    .replace('@@DATA@@', json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')))
        f = os.path.join(OUT, '%s-review.html' % k); open(f, 'w').write(rv); made.append(f)
    return made

if __name__ == '__main__':
    for f in build(sys.argv[1:] or None): print('built', f)
