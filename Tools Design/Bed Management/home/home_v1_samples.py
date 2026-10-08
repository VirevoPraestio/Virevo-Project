"""
Bed Management - the tool's own home page (the summary of all four places).
Three samples for review, each with its own look and its own bed drawing:

  A  The ward bay     four beds side by side, one bed for each place (linen and teal)
  B  The ward plan    a ward seen from above: four rooms off one corridor, one small bed per step (slate)
  C  The quilt        one big bed, its quilt sewn from four patches, one patch per place (sand and brick)

Every sample keeps the same five zones as every landing page (masthead with the stamp,
where this stands, the drawing, what Tojo still has to do, the three buttons) and the same
chat panel. Two states: 'filled' (in progress) and 'empty' (first visit).
Standard library only. Run:  python3 home.py  -> out/bed-management/home/
"""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [os.path.join(os.path.dirname(ROOT), 'Common Elements', 'landing-common'), os.path.join(os.path.dirname(ROOT), 'Common Elements', 'diagnosis-html-generator')]
from landing_common import embedded_fonts, REFRESH_ICO, chat_html  # noqa: E402
from preview import SHELL_CSS, TABS, ico, CLIP, MIC, SEND, SHEET, HOME  # noqa: E402

e = lambda s: html.escape('' if s is None else str(s), quote=True)
TOOL = 'Bed Management'
ICONS = dict(TABS)
BED_ICO = '<path d="M3 19V6"/><path d="M3 15h18v4"/><path d="M21 15v-2.5A2.5 2.5 0 0018.5 10H11v5"/><circle cx="7" cy="12" r="2"/>'

# ------------------------------------------------------------------------------------------
# Words shared by all three samples
STATUS = {'now': 'In use now', 'started': 'Being made ready', 'none': 'Not made up yet', 'done': 'Made up', 'empty': 'Empty bed'}
STEP = {'done': 'Done', 'now': 'Now', 'later': 'Still to do', 'none': 'Not started'}
TAGS = {'yours': 'Your number', 'guess': 'Tojo’s guess', 'need': 'Need from you'}

DATA = {
 'filled': {
  'stamp': {'at': 'Brought up to date at midnight, 30 September', 'since': '3 conversations since then are not in yet',
            'fresh': 'Brought up to date just now, 11:40 AM', 'fresh_since': 'Everything you have said is in'},
  'claim': 'Beds come free too late for the patients who need them',
  'deck': 'Diagnosis is past halfway. Three fixes are on the table. Nothing is switched on or changed on the wards yet.',
  'places': [
   {'key': 'diagnosis', 'name': 'Diagnosis', 'status': 'now', 'pt': 1,
    'head': 'Beds come free after 2 PM. Most new patients arrive by 11 AM.',
    'fig': {'v': '75 minutes', 'l': 'Bed empty after the patient leaves', 'tag': 'yours'},
    'prog': [2, 5, 'stages done'],
    'steps': [['Walk a bed’s day', 'done'], ['Count beds free each morning', 'done'], ['Match arrivals to free beds', 'now'],
              ['Price the wait', 'later'], ['Name the cause', 'later']]},
   {'key': 'solutions', 'name': 'Solutions', 'status': 'started', 'pt': 3,
    'head': 'Three fixes on the table. One is taking shape.',
    'fig': {'v': 'About 1 hour', 'l': 'Could come off each bed’s wait', 'tag': 'guess'},
    'prog': [0, 3, 'fixes agreed'],
    'steps': [['One bed list everyone can see', 'now'], ['Housekeeping called the moment a patient leaves', 'later'],
              ['Tomorrow’s free beds planned tonight', 'later']]},
   {'key': 'automations', 'name': 'Automations', 'status': 'none', 'pt': None,
    'head': 'Starts once a fix is agreed. One idea is waiting.', 'fig': None,
    'prog': [0, 1, 'switched on'],
    'steps': [['Bed marked free on its own when the patient leaves', 'none']]},
   {'key': 'processes', 'name': 'Processes', 'status': 'none', 'pt': None,
    'head': 'Starts once a fix is agreed. Two ideas are waiting.', 'fig': None,
    'prog': [0, 2, 'tried on a ward'],
    'steps': [['One bed owner on every shift', 'none'], ['Watch the time from bed free to next patient in', 'none']]},
  ],
  'pending': [
   {'text': 'Match each morning’s new patients to the beds free the night before.'},
   {'text': 'Find how many beds are in use most nights.', 'need': 'Needs your bed count at midnight', 'pt': 2},
   {'text': 'Time each step of an admission, from the doctor’s call to the patient in bed.', 'need': 'Needs times from your admissions desk', 'pt': 4},
   {'text': 'Check whether one team runs both discharges and admissions.'},
  ],
  'actions': {'go': {'detail': 'Match arrivals to free beds', 'say': 'Let’s match each morning’s new patients to the beds free the night before'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about our beds: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Pick up where you left off', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Here is where Bed Management stands, across all four parts of the work.',
                    'Diagnosis is two stages in. Beds come free after 2 PM, but most new patients arrive by 11 AM.',
                    'Two numbers would sharpen this: beds in use most nights, and how long each step of an admission takes.'],
           'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
           'note': 'The beds do free up. Just too late.',
           'points': [{'n': 1, 'label': 'Beds that free up late'}, {'n': 2, 'label': 'Beds in use most nights'},
                      {'n': 3, 'label': 'The one bed list idea'}, {'n': 4, 'label': 'Admission times by step'}],
           'prompts': ['Let’s match arrivals to free beds', 'Why do beds free up so late?', 'Show me the three fixes']},
 },
 'empty': {
  'stamp': {'at': 'Nothing to bring up to date yet', 'since': 'This page fills in as you talk to Tojo',
            'fresh': 'Checked just now, 11:40 AM', 'fresh_since': 'No conversations yet'},
  'claim': 'Nothing here yet',
  'deck': 'Start with Diagnosis. Tojo walks one bed’s day with you and fills this page as you go.',
  'places': [
   {'key': 'diagnosis', 'name': 'Diagnosis', 'status': 'empty', 'head': 'Fills in as you walk a bed’s day with Tojo.', 'fig': None, 'prog': None, 'steps': []},
   {'key': 'solutions', 'name': 'Solutions', 'status': 'empty', 'head': 'Fills in once the cause is named.', 'fig': None, 'prog': None, 'steps': []},
   {'key': 'automations', 'name': 'Automations', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'prog': None, 'steps': []},
   {'key': 'processes', 'name': 'Processes', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'prog': None, 'steps': []},
  ],
  'pending': [
   {'text': 'Walk one bed’s day, from the patient leaving to the next patient in.'},
   {'text': 'Count the beds free each morning for one week.', 'need': 'Needs your bed list for last week'},
   {'text': 'Find how many beds are in use most nights.'},
  ],
  'actions': {'go': {'detail': 'Walk a bed’s day with Tojo', 'say': 'Let’s walk a bed’s day'},
              'add': {'detail': 'Share a bed list or a report', 'say': 'Here is what I already know about our beds: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Every conversation starts here', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Welcome to Bed Management. This page fills in as we talk.',
                    'We start by walking one bed’s day: when the patient leaves, when the bed is cleaned, and when the next patient gets in.'],
           'note': 'Start with one bed. The rest follows.', 'points': [],
           'prompts': ['Let’s walk a bed’s day', 'What should I bring?', 'How does this work?']},
 },
}

# ------------------------------------------------------------------------------------------
THEMES = {
 'a': {'name': 'The ward bay', 'ground': '#EAE3D6', 'ink': '#0E3A3B', 'rail_bg': '#0E3A3B', 'rail_fg': '#d4a94f',
       'rail': ['#E2DBCB', '#DCE5DF', '#E6DECF', '#D8E1DC', '#E4DCCC'],
       'vars': '--g:#EAE3D6;--card:#FBF8F2;--ink:#0E3A3B;--mut:#475B59;--line:#B7C3BD;--soft:#E1EAE6;--grey:#8C9A96;--btnr:10px'},
 'b': {'name': 'The ward plan', 'ground': '#E2E6EE', 'ink': '#1C2542', 'rail_bg': '#1C2542', 'rail_fg': '#d4a94f',
       'rail': ['#D8DDE8', '#E3E0EA', '#D5DCE6', '#DFE2EC', '#D9DEE6'],
       'vars': '--g:#E2E6EE;--card:#FAFBFD;--ink:#1C2542;--mut:#4A536E;--line:#B5BCCE;--soft:#EDF0F6;--grey:#8D94A8;--btnr:6px'},
 'c': {'name': 'The quilt', 'ground': '#F0E4D8', 'ink': '#3A1F16', 'rail_bg': '#3A1F16', 'rail_fg': '#d4a94f',
       'rail': ['#E8D9CA', '#EEDCCB', '#E6DACD', '#ECD8CC', '#E9DDCF'],
       'vars': '--g:#F0E4D8;--card:#FFF9F3;--ink:#3A1F16;--mut:#654A40;--line:#D2BBAB;--soft:#F7ECE2;--grey:#A08F87;--btnr:22px;'
               '--p1:#F7E1CF;--p2:#EDE5D0;--p3:#F2DAD4;--p4:#E6E2DA'},
}

# ------------------------------------------------------------------------------------------
# Parts every sample shares
def stamp(s):
    return ('<div class="lp-stamp"><div class="lp-stamp-txt"><span class="lp-stamp-at">%s</span><span class="lp-stamp-since">%s</span></div>'
            '<button class="lp-refresh" type="button" data-fresh="%s" data-fresh-since="%s">%s<span>Refresh now</span></button></div>') % (
        e(s['at']), e(s['since']), e(s['fresh']), e(s['fresh_since']), REFRESH_ICO)

def masthead(d, emblem):
    return ('<header class="bm-mast"><div class="bm-id">%s<div><div class="bm-kick">Virevo · 250-bed hospital, Bhubaneswar</div>'
            '<h1 class="bm-name">Bed Management</h1></div></div>%s</header>') % (emblem, stamp(d['stamp']))

def standing(d, empty):
    return '<div class="bm-stand%s"><h2 class="bm-claim">%s</h2><p class="bm-deck">%s</p></div>' % (' is-empty' if empty else '', e(d['claim']), e(d['deck']))

def pt(n):
    return '' if n is None else ' data-pt="%d"' % n

def pending(d):
    items = ''.join('<li class="bm-pi%s"%s><i class="bm-pm" aria-hidden="true"></i><span>%s%s</span></li>' % (
        ' wait' if p.get('need') else '', pt(p.get('pt')), e(p['text']),
        '<b class="bm-need">%s</b>' % e(p['need']) if p.get('need') else '') for p in d['pending'])
    return '<section class="bm-pend" aria-label="What Tojo still has to do"><h3 class="bm-lab">What Tojo still has to do</h3><ul>%s</ul></section>' % items

def actions(d):
    a = d['actions']
    b = lambda k, head, det: '<button class="lp-act lp-act-%s" type="button" data-text="%s"><span class="lp-act-k">%s</span><span class="lp-act-d">%s</span></button>' % (
        k, e(a[k]['say']), e(head), e(det))
    return '<nav class="lp-acts" aria-label="What to do next">%s%s%s</nav>' % (
        b('go', 'Proceed with next step', a['go']['detail']), b('add', 'Add more', a['add']['detail']),
        b('jump', 'Jump to ' + a['jump']['tab'], a['jump']['detail']))

def foot(d):
    return '<div class="bm-foot">%s%s</div>' % (pending(d), actions(d))

def tag(t):
    return '<span class="bm-tag %s">%s</span>' % (t, e(TAGS[t]))

def figure(f):
    if not f: return ''
    return '<span class="bm-fig"><span class="bm-fv">%s</span><span class="bm-fl">%s</span>%s</span>' % (e(f['v']), e(f['l']), tag(f['tag']))

def dots(p, cls='bm-dots'):
    """Step marks for one place: the drawn record of its progress."""
    if not p['steps']:
        return '<span class="%s"><i class="s-empty"></i><i class="s-empty"></i><i class="s-empty"></i></span>' % cls
    return '<span class="%s">%s</span>' % (cls, ''.join('<i class="s-%s"></i>' % s for _, s in p['steps']))

def prog_line(p):
    if not p['prog']: return 'Nothing yet'
    return '%d of %d %s' % tuple(p['prog'])

def steps_list(p, inline=False):
    o, i = ('span', 'span') if inline else ('ol', 'li')
    return '<%s class="bm-steps">%s</%s>' % (o, ''.join(
        '<%s class="s-%s"><i aria-hidden="true"></i><span>%s</span><em>%s</em></%s>' % (i, s, e(t), STEP[s], i) for t, s in p['steps']), o)

def open_btn(p):
    return '<button class="bm-open" type="button" data-text="Take me to %s">Open %s %s</button>' % (e(p['name']), e(p['name']), ico(SEND, 'currentColor', 16))

def place_ico(p, c='currentColor', w=20):
    return ico(ICONS[p['name']], c, w)

# ------------------------------------------------------------------------------------------
# A - the ward bay: four beds side by side under one curtain rail
def canvas_a(d, empty):
    beds = []
    for i, p in enumerate(d['places']):
        sel = p['status'] == 'now'
        beds.append(
            '<button class="a-bed js-pick" type="button" data-grp="a" data-key="%s" data-s="%s" aria-pressed="%s" aria-controls="a-det-%s"%s>'
            '<span class="a-head"><span data-n="Bed %d">Bed %d · %s</span></span>'
            '<span class="a-frame"><span class="a-pillow">%s</span>'
            '<span class="a-name">%s</span>'
            '<span class="a-sheet"><span class="a-hl">%s</span>%s</span>'
            '<span class="a-clip"><span class="a-cliptop"></span>%s<span class="a-pl">%s</span></span></span>'
            '<span class="a-st">%s</span></button>' % (
                p['key'], p['status'], 'true' if sel else 'false', p['key'], pt(p.get('pt')), i + 1, i + 1, e(STATUS[p['status']]),
                place_ico(p, 'currentColor', 18), e(p['name']), e(p['head']), figure(p['fig']), dots(p), e(prog_line(p)), e(STATUS[p['status']])))
        if p['steps']:
            body = '<div class="a-dh"><b>%s</b><span>%s</span><span class="a-dhint">Pick another bed to see its steps</span></div>%s%s' % (e(p['name']), e(prog_line(p)), steps_list(p), open_btn(p))
        else:
            body = '<div class="a-dh"><b>%s</b><span>%s</span></div><p class="a-dnone">%s</p>%s' % (e(p['name']), 'Empty bed', e(p['head']), open_btn(p))
        beds.append('<div class="a-det" id="a-det-%s" data-det="a:%s"%s>%s</div>' % (p['key'], p['key'], '' if sel else ' hidden', body))
    hint = ''
    drawing = '<section class="a-bay" aria-label="The four parts of the work, one bed each"><div class="a-rail" aria-hidden="true"></div><div class="a-grid">%s</div>%s</section>' % (''.join(beds), hint)
    emblem = '<span class="bm-emb a-emb">%s</span>' % ico(BED_ICO, '#d4a94f', 30)
    return masthead(d, emblem) + standing(d, empty) + drawing + foot(d)

CSS_A = '''
.bm-a .a-emb{width:56px;height:56px;border-radius:14px;background:var(--ink);display:flex;align-items:center;justify-content:center}
.a-bay{margin-top:4px}
.a-rail{height:10px;border-top:2.5px solid var(--ink);margin:0 4px;background:radial-gradient(circle at 50% 3px,transparent 2.5px,var(--ink) 3px,var(--ink) 4px,transparent 4.5px) 0 0/26px 10px repeat-x}
.a-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px 16px;margin-top:2px}
.a-bed{display:flex;flex-direction:column;align-items:stretch;text-align:left;background:none;border:0;padding:0;min-width:0;transition:transform .15s ease}
.a-head{height:20px;border-radius:9px 9px 2px 2px;background:var(--ink);margin:0 8px;display:flex;align-items:center;justify-content:center}
.a-head span{font-size:10.5px;font-weight:600;letter-spacing:.06em;color:var(--card)}
.a-frame{display:flex;flex-direction:column;gap:4px;flex-grow:1;border:2px solid var(--ink);border-top-width:3px;border-radius:4px 4px 16px 16px;background:var(--card);padding:10px 12px 0;position:relative}
.a-pillow{height:20px;margin:0 16px;border-radius:13px;background:var(--soft);border:1.5px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--ink)}
.a-name{font-family:'Bebas Neue',sans-serif;font-size:27px;line-height:1;margin-top:2px}
.a-sheet{display:flex;flex-direction:column;gap:6px;border-top:2px solid var(--ink);margin:0 -12px;padding:8px 12px 10px;background:repeating-linear-gradient(180deg,transparent 0 12px,rgba(14,58,59,.035) 12px 13px);flex-grow:1}
.a-hl{font-size:13px;line-height:1.38}
.a-clip{margin:0 -12px;padding:8px 12px 10px;border-top:1.5px dashed var(--line);display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--mut);position:relative}
.a-cliptop{display:none}
.a-pl{font-weight:600}
.a-st{display:none;align-self:center;margin-top:6px;padding:3px 12px;border-radius:12px;font-size:12px;font-weight:600;border:1.5px solid var(--ink)}
.a-bed[data-s=now] .a-head{background:#d4a94f}.a-bed[data-s=now] .a-head span{color:var(--ink)}
.a-bed[data-s=now] .a-st{background:#d4a94f;border-color:#d4a94f}
.a-bed[data-s=started] .a-st{background:var(--ink);color:var(--card)}
.a-bed[data-s=none] .a-frame,.a-bed[data-s=empty] .a-frame{border-style:dashed;border-color:var(--grey);background:transparent}
.a-bed[data-s=none] .a-head,.a-bed[data-s=empty] .a-head{background:var(--grey)}
.a-bed[data-s=none] .a-sheet,.a-bed[data-s=empty] .a-sheet{border-top:2px dashed var(--grey);background:none}
.a-bed[data-s=none] .a-hl,.a-bed[data-s=empty] .a-hl{color:var(--mut)}
.a-bed[data-s=none] .a-st,.a-bed[data-s=empty] .a-st{border:1.5px dashed var(--grey);color:var(--mut)}
.a-bed[data-s=empty] .a-pillow{border-style:dashed;background:transparent}
.a-bed[aria-pressed=true]{transform:translateY(-3px)}
.a-bed[aria-pressed=true] .a-frame{box-shadow:6px 6px 0 rgba(14,58,59,.14)}
.a-bed[aria-pressed=true] .a-head span::after{content:" ▾"}
.a-det{grid-column:1/-1;grid-row:2;border:2px solid var(--ink);border-radius:12px;background:var(--card);padding:8px 14px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.a-det[hidden]{display:none}
.a-dh{display:flex;flex-direction:column;min-width:110px;max-width:150px}.a-dh .a-dhint{font-style:italic;font-size:11px;margin-top:2px}.a-dh b{font-family:'Bebas Neue',sans-serif;font-size:24px;font-weight:400;line-height:1}.a-dh span{font-size:12px;color:var(--mut)}
.a-det .bm-steps{flex:1 1 380px;flex-direction:row;flex-wrap:wrap;gap:4px 18px}
.a-dnone{flex:1 1 300px;font-size:13.5px;color:var(--mut)}
@container lp (max-width:699px){
 .a-grid{grid-template-columns:1fr;gap:10px}
 .a-bed{flex-direction:row;flex-wrap:wrap}
 .a-head{width:20px;height:auto;margin:8px 0;border-radius:9px 2px 2px 9px}
 .a-head span{writing-mode:vertical-rl;transform:rotate(180deg)}
 .a-frame{display:grid;grid-template-columns:28px minmax(0,1fr);column-gap:10px;border-top-width:2px;border-left-width:3px;border-radius:4px 16px 16px 4px;padding:10px 12px 0 8px;flex:1 1 0;min-width:0}
 .a-pillow{grid-row:1/span 3;width:26px;height:auto;margin:6px 0 10px}
 .a-sheet{margin:0 -12px 0 0;padding-left:0;border-top-width:1.5px}
 .a-clip{margin:0 -12px 0 0;padding-left:0}
 .a-st{display:block;position:absolute;right:10px;top:10px;margin:0}
 .a-head span{font-size:0}
 .a-head span::before{content:attr(data-n);font-size:10.5px}
 .a-bed{position:relative}
 .a-name{padding-right:130px}
 .a-bed[aria-pressed=true] .a-st::after{content:""}
 .a-bed[aria-pressed=true]{transform:none}
 .a-det{grid-row:auto;flex-direction:column;align-items:stretch}
 .a-det .bm-steps{flex:none;flex-direction:column}
 .a-dh{display:none}
 .a-name{padding-right:124px}
 .a-st{right:10px;top:8px}
}
'''

# ------------------------------------------------------------------------------------------
# B - the ward plan: four rooms off one corridor, a small bed for every step
BED_SVG = ('<svg viewBox="0 0 40 54" width="40" height="54" aria-hidden="true"><rect class="h" x="4" y="2" width="32" height="6" rx="3"/>'
           '<rect class="f" x="6" y="8" width="28" height="43" rx="4"/><rect class="p" x="11" y="12" width="18" height="8" rx="4"/>'
           '<path class="k" d="M6 25h28v22a4 4 0 01-4 4H10a4 4 0 01-4-4z"/></svg>')

def canvas_b(d, empty):
    rooms = []
    total = sum(len(p['steps']) for p in d['places']); made = sum(1 for p in d['places'] for _, s in p['steps'] if s == 'done')
    for i, p in enumerate(d['places']):
        if p['steps']:
            beds = ''.join('<button class="b-bed s-%s js-bed" type="button" aria-pressed="false" data-cap="%s · %s" aria-label="%s: %s">%s</button>' % (
                s, e(t), STEP[s], e(t), STEP[s], BED_SVG) for t, s in p['steps'])
            cap = 'Pick a bed to see its step'
        else:
            beds = ''.join('<span class="b-bed s-empty" aria-hidden="true">%s</span>' % BED_SVG for _ in range(3))
            cap = 'Beds are set up as the work starts'
        rooms.append(
            '<div class="b-room b-r%d" data-s="%s"%s><span class="b-door" aria-hidden="true"></span>'
            '<div class="b-plate"><span class="b-pn">%s %s</span><span class="b-ps">%s</span></div>'
            '<div class="b-body"><div class="b-txt"><p class="b-hl">%s</p>%s</div><div class="b-beds">%s</div></div>'
            '<div class="b-cap"><span class="b-capt" aria-live="polite">%s</span><span class="b-pl">%s</span></div></div>' % (
                i + 1, p['status'], pt(p.get('pt')), place_ico(p, 'currentColor', 18), e(p['name']), e(STATUS[p['status']]),
                e(p['head']), figure(p['fig']), beds, e(cap), e(prog_line(p))))
    station = ('<div class="b-corr"><span class="b-cl">Corridor</span><div class="b-stn"><span class="b-sk">Nurses’ station</span>'
               '<span class="b-sv">%s</span><span class="b-bar"><i style="width:%d%%"></i></span></div><span class="b-cl">Corridor</span></div>') % (
        ('%d of %d beds made up' % (made, total)) if total else 'No beds set up yet', int(100 * made / total) if total else 0)
    plan = '<section class="b-plan" aria-label="The ward plan: one room for each part of the work">%s%s%s</section>' % (''.join(rooms[:2]), station, ''.join(rooms[2:]))
    key = ('<div class="b-key" aria-hidden="true"><span><i class="k-done"></i>Made up: done</span><span><i class="k-now"></i>In use now</span>'
           '<span><i class="k-later"></i>Still to do</span><span><i class="k-none"></i>Not started</span></div>')
    emblem = '<span class="bm-emb b-emb">%s</span>' % ico(BED_ICO, '#d4a94f', 30)
    return masthead(d, emblem) + standing(d, empty) + plan + key + foot(d)

CSS_B = '''
.bm-b .a-emb,.bm-b .b-emb{width:56px;height:56px;border-radius:4px;background:var(--ink);display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 3px var(--ink),inset 0 0 0 5px rgba(212,169,79,.5)}
.b-plan{display:grid;grid-template-columns:1fr 1fr;border:3.5px solid var(--ink);border-radius:4px;background:var(--card);background-image:linear-gradient(rgba(28,37,66,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(28,37,66,.045) 1px,transparent 1px);background-size:20px 20px}
.b-room{position:relative;padding:10px 14px 8px;display:flex;flex-direction:column;gap:6px;min-width:0}
.b-r1,.b-r3{border-right:2.5px solid var(--ink)}
.b-r1,.b-r2{border-bottom:2.5px solid var(--ink)}
.b-r3,.b-r4{border-top:2.5px solid var(--ink)}
.b-door{position:absolute;left:28px;width:46px;height:46px;pointer-events:none}
.b-r1 .b-door,.b-r2 .b-door{bottom:-2.5px;border-bottom:3px solid var(--card)}
.b-r3 .b-door,.b-r4 .b-door{top:-2.5px;border-top:3px solid var(--card)}
.b-r1 .b-door::after,.b-r2 .b-door::after{content:"";position:absolute;left:0;bottom:0;width:44px;height:44px;border-top:1.5px dashed var(--line);border-right:1.5px dashed var(--line);border-radius:0 44px 0 0}
.b-r3 .b-door::after,.b-r4 .b-door::after{content:"";position:absolute;left:0;top:0;width:44px;height:44px;border-bottom:1.5px dashed var(--line);border-right:1.5px dashed var(--line);border-radius:0 0 44px 0}
.b-plate{display:flex;align-items:center;justify-content:space-between;gap:8px}
.b-pn{display:inline-flex;align-items:center;gap:7px;background:var(--ink);color:var(--card);padding:3px 10px 2px;border-radius:3px;font-family:'Bebas Neue',sans-serif;font-size:23px;line-height:1.1}
.b-pn svg{margin-top:-2px}
.b-ps{font-size:12px;font-weight:600;padding:2px 10px;border-radius:10px;border:1.5px solid var(--ink)}
.b-room[data-s=now] .b-ps{background:#d4a94f;border-color:#d4a94f}
.b-room[data-s=now] .b-pn{box-shadow:inset 0 -3px 0 #d4a94f}
.b-room[data-s=started] .b-ps{background:var(--ink);color:var(--card)}
.b-room[data-s=none] .b-ps,.b-room[data-s=empty] .b-ps{border-style:dashed;border-color:var(--grey);color:var(--mut)}
.b-room[data-s=none] .b-pn,.b-room[data-s=empty] .b-pn{background:transparent;color:var(--mut);box-shadow:inset 0 0 0 1.5px var(--grey)}
.b-hl{font-size:13.5px;line-height:1.38}
.b-room[data-s=none] .b-hl,.b-room[data-s=empty] .b-hl{color:var(--mut)}
.b-body{display:flex;gap:12px;align-items:flex-start}.b-txt{flex:1 1 0;min-width:0;display:flex;flex-direction:column;gap:6px}
.b-beds{display:flex;flex-wrap:wrap;gap:4px;justify-content:flex-end;max-width:150px}
.b-bed{width:44px;height:58px;padding:2px;border:0;background:none;border-radius:6px;display:flex;align-items:center;justify-content:center}
.b-bed svg .h{fill:var(--ink)}.b-bed svg .f{fill:var(--card);stroke:var(--ink);stroke-width:2}.b-bed svg .p{fill:var(--soft);stroke:var(--ink);stroke-width:1.2}.b-bed svg .k{fill:none}
.b-bed.s-done svg .k{fill:var(--ink)}
.b-bed.s-now svg .k{fill:#d4a94f}.b-bed.s-now svg .h{fill:#d4a94f}
.b-bed.s-later svg .k{fill:var(--soft)}
.b-bed.s-none svg .f,.b-bed.s-empty svg .f{stroke:var(--grey);stroke-dasharray:4 3;fill:transparent}.b-bed.s-none svg .h,.b-bed.s-empty svg .h{fill:var(--grey)}
.b-bed.s-none svg .p,.b-bed.s-empty svg .p{stroke:var(--grey);fill:transparent}
.b-bed[aria-pressed=true]{outline:3px solid #d4a94f;outline-offset:1px}
.b-cap{display:flex;justify-content:space-between;gap:10px;font-size:12px;color:var(--mut);border-top:1.5px dashed var(--line);padding-top:6px;margin-top:auto}
.b-capt{font-style:italic}.b-capt.is-set{font-style:normal;color:var(--ink);font-weight:600}
.b-pl{font-weight:600;white-space:nowrap}
.b-corr{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:6px 14px;background:repeating-linear-gradient(90deg,var(--line) 0 14px,transparent 14px 26px) 0 50%/100% 1.5px no-repeat}
.b-cl{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);background:var(--card);padding:0 6px}
.b-stn{display:flex;align-items:center;gap:10px;background:var(--ink);color:var(--card);border-radius:22px;padding:6px 16px}
.b-sk{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#E8D3A2}
.b-sv{font-family:'Bebas Neue',sans-serif;font-size:21px;line-height:1}
.b-bar{width:90px;height:8px;border-radius:4px;background:rgba(250,251,253,.25);overflow:hidden}.b-bar i{display:block;height:100%;background:#d4a94f}
.b-key{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:6px;font-size:12px;color:var(--mut)}
.b-key span{display:inline-flex;align-items:center;gap:6px}.b-key i{width:12px;height:12px;border-radius:3px;border:1.5px solid var(--ink)}
.b-key .k-done{background:var(--ink)}.b-key .k-now{background:#d4a94f;border-color:#d4a94f}.b-key .k-later{background:var(--soft)}.b-key .k-none{border:1.5px dashed var(--grey)}
@container lp (max-width:699px){
 .b-plan{grid-template-columns:1fr 1fr}
 .b-r1,.b-r2,.b-corr{grid-column:1/-1}
 .b-r1{border-right:0}
 .b-body{flex-direction:column}.b-beds{max-width:none;justify-content:flex-start}
 .b-r3 .b-plate,.b-r4 .b-plate{flex-direction:column;align-items:flex-start}
 .b-r3 .b-cap,.b-r4 .b-cap{flex-direction:column;gap:2px}
 .b-corr{order:-1;border-bottom:2.5px solid var(--ink);background:none;justify-content:center}
 .b-cl{display:none}
 .b-r1,.b-r2{border-top:0;border-bottom:2.5px solid var(--ink)}
 .b-r3,.b-r4{border-top:0}
 .b-door{display:none}
}
'''

# ------------------------------------------------------------------------------------------
# C - the quilt: one big bed, the quilt sewn from four patches
def canvas_c(d, empty):
    patches = []
    for i, p in enumerate(d['places']):
        back = steps_list(p, True) if p['steps'] else '<span class="c-none">%s</span>' % e(p['head'])
        patches.append(
            '<div class="c-patch c-p%d" data-s="%s"%s><button class="c-turn js-turn" type="button" aria-expanded="false">'
            '<span class="c-front"><span class="c-top"><span class="c-name">%s %s</span><span class="c-st">%s</span></span>'
            '<span class="c-hl">%s</span>%s<span class="c-pr">%s<span>%s</span></span></span>'
            '<span class="c-back"><span class="c-top"><span class="c-name">%s steps</span><span class="c-st">Turn back</span></span>%s</span>'
            '<span class="c-fold" aria-hidden="true"></span></button></div>' % (
                i + 1, p['status'], pt(p.get('pt')), place_ico(p, 'currentColor', 18), e(p['name']), e(STATUS[p['status']]),
                e(p['head']), figure(p['fig']), dots(p), e(prog_line(p)), e(p['name']), back))
    total = sum(len(p['steps']) for p in d['places']); done = sum(1 for p in d['places'] for _, s in p['steps'] if s == 'done')
    now = next((p['name'] for p in d['places'] if p['status'] == 'now'), None)
    pillow = ('<div class="c-pillow"><span class="c-pk">On the pillow</span><span class="c-pv">%s</span><span class="c-pt">%s</span></div>') % (
        ('%d of %d' % (done, total)) if total else '0', ('steps done. %s is in use now.' % now) if now else 'Nothing started yet.')
    bed = ('<section class="c-bed" aria-label="One bed, its quilt sewn from the four parts of the work"><div class="c-headb" aria-hidden="true"><span>Head of the bed</span></div>%s'
           '<div class="c-quilt">%s</div><div class="c-footb" aria-hidden="true"></div></section><p class="bm-hint">Turn back a patch to see its steps.</p>') % (pillow, ''.join(patches))
    emblem = '<span class="bm-emb c-emb">%s</span>' % ico(BED_ICO, '#d4a94f', 30)
    return masthead(d, emblem) + standing(d, empty) + bed + foot(d)

CSS_C = '''
.bm-c .c-emb{width:58px;height:58px;border-radius:50%;background:var(--ink);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 3px var(--g),0 0 0 4.5px var(--ink)}
.c-bed{display:grid;grid-template-columns:22px 150px minmax(0,1fr) 16px;align-items:stretch;margin-top:4px}
.c-headb{background:var(--ink);border-radius:12px 4px 4px 12px;display:flex;align-items:center;justify-content:center}
.c-headb span{writing-mode:vertical-rl;transform:rotate(180deg);font-size:10.5px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#E8D3A2}
.c-footb{background:var(--ink);border-radius:4px 10px 10px 4px;margin:14px 0}
.c-pillow{margin:10px 0;border:2px solid var(--ink);border-left:0;border-radius:0 34px 34px 0;background:var(--card);display:flex;flex-direction:column;justify-content:center;gap:4px;padding:12px 16px}
.c-pk{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.c-pv{font-family:'Bebas Neue',sans-serif;font-size:44px;line-height:.9}
.c-pt{font-size:12.5px;line-height:1.35}
.c-quilt{display:grid;grid-template-columns:1fr 1fr;gap:0;border:2.5px solid var(--ink);border-radius:6px 22px 22px 6px;overflow:hidden;background:var(--card)}
.c-patch{position:relative;min-width:0}
.c-p1{background:var(--p1);border-right:2px solid var(--ink);border-bottom:2px solid var(--ink)}
.c-p2{background:var(--p2);border-bottom:2px solid var(--ink)}
.c-p3{background:var(--p3);border-right:2px solid var(--ink)}
.c-p4{background:var(--p4)}
.c-turn{display:block;width:100%;height:100%;text-align:left;background:none;border:0;padding:14px 16px 14px;position:relative;min-height:176px}
.c-turn::before{content:"";position:absolute;inset:6px;border:1.5px dashed rgba(58,31,22,.32);border-radius:10px;pointer-events:none}
.c-front,.c-back{display:flex;flex-direction:column;gap:7px;position:relative}
.c-back{display:none}
.c-turn[aria-expanded=true] .c-front{display:none}.c-turn[aria-expanded=true] .c-back{display:flex}
.c-turn[aria-expanded=true]{background:var(--card)}
.c-top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.c-name{display:inline-flex;align-items:center;gap:7px;font-family:'Bebas Neue',sans-serif;font-size:26px;line-height:1}
.c-name svg{margin-top:-3px}
.c-st{font-size:12px;font-weight:600;padding:2px 11px;border-radius:12px;border:1.5px solid var(--ink);white-space:nowrap}
.c-hl{font-size:13.5px;line-height:1.38}
.c-pr{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:600;color:var(--mut)}
.c-fold{position:absolute;right:0;bottom:0;width:0;height:0;border-style:solid;border-width:0 0 26px 26px;border-color:transparent transparent var(--card) transparent;filter:drop-shadow(-1.5px -1.5px 0 rgba(58,31,22,.35))}
.c-patch[data-s=now] .c-st{background:#d4a94f;border-color:#d4a94f}
.c-patch[data-s=now] .c-turn::before{border:2px solid #d4a94f}
.c-patch[data-s=started] .c-st{background:var(--ink);color:var(--card)}
.c-patch[data-s=none],.c-patch[data-s=empty]{background:var(--soft)}
.c-patch[data-s=none] .c-st,.c-patch[data-s=empty] .c-st{border-style:dashed;border-color:var(--grey);color:var(--mut)}
.c-patch[data-s=none] .c-hl,.c-patch[data-s=empty] .c-hl,.c-patch[data-s=none] .c-name,.c-patch[data-s=empty] .c-name{color:var(--mut)}
.c-patch[data-s=none] .c-turn::before,.c-patch[data-s=empty] .c-turn::before{border-color:var(--grey)}
.c-none{font-size:13.5px;color:var(--mut)}
@container lp (max-width:699px){
 .c-bed{grid-template-columns:1fr;grid-template-rows:auto}
 .c-headb{height:22px;border-radius:12px 12px 4px 4px;margin:0}
 .c-headb span{writing-mode:horizontal-tb;transform:none}
 .c-pillow{margin:0 12px;border:2px solid var(--ink);border-top:0;border-radius:0 0 30px 30px;flex-direction:row;flex-wrap:wrap;align-items:center;column-gap:12px;padding:8px 16px 12px}
 .c-pk{flex-basis:100%}.c-pv{font-size:38px}.c-pt{flex:1 1 150px}
 .c-quilt{grid-template-columns:1fr;border-radius:6px 6px 22px 22px;margin-top:8px}
 .c-p1,.c-p2,.c-p3{border-right:0;border-bottom:2px solid var(--ink)}
 .c-turn{min-height:0}
 .c-footb{height:16px;margin:0 14px;border-radius:4px 4px 10px 10px}
}
'''

# ------------------------------------------------------------------------------------------
BASE_CSS = '''
.lp-host{container-type:inline-size;container-name:lp;width:100%}
.lp{box-sizing:border-box;font-family:'Poppins','Segoe UI',system-ui,sans-serif}
.lp *,.lp *::before,.lp *::after{box-sizing:border-box}
.lp button{font:inherit;color:inherit;cursor:pointer}
.lp :focus-visible{outline:3px solid #d4a94f;outline-offset:2px}
.lp p,.lp h1,.lp h2,.lp h3{margin:0}
.lp ul,.lp ol{margin:0;padding:0;list-style:none}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.bm{padding:18px 30px 24px;color:var(--ink);--gold:#d4a94f;--dgold:#6B4F16;--amber:#8A5608;--green:#2F6B4F;--red:#8E2F1C}
.bm-mast{display:flex;align-items:center;justify-content:space-between;gap:18px;padding-bottom:12px;border-bottom:2px solid var(--ink)}
.bm-id{display:flex;align-items:center;gap:14px;min-width:0}
.bm-emb{flex-shrink:0}
.bm-kick{font-size:12px;font-weight:600;color:var(--mut)}
.bm-name{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:48px;line-height:.95;white-space:nowrap}
.bm-sub{font-size:12px;color:var(--mut)}
.lp-stamp{display:flex;align-items:center;gap:12px}
.lp-stamp-txt{display:flex;flex-direction:column;text-align:right}
.lp-stamp-at{font-size:13px;font-weight:600}
.lp-stamp-txt{max-width:300px}.lp-stamp-since{font-size:12px;color:var(--mut)}
.lp-refresh{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;flex-shrink:0;border:1.5px solid var(--ink);background:var(--card);border-radius:var(--btnr);font-size:13px;font-weight:500}
.lp-refresh.is-done svg{transform:rotate(360deg);transition:transform .6s ease}
.bm-stand{margin:10px 0 10px}
.bm-claim{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:38px;line-height:1}
.bm-deck{font-size:14px;color:var(--mut);margin-top:4px}
.bm-stand.is-empty .bm-claim{color:var(--mut)}
.bm-hint{font-size:12px;color:var(--mut);font-style:italic;margin-top:6px}
.bm-tag{display:inline-block;align-self:flex-start;font-size:10.5px;font-weight:600;padding:1px 7px;border-radius:3px;white-space:nowrap}
.bm-tag.yours{border:1.5px solid var(--green);color:var(--green)}.bm-tag.guess{border:1.5px dashed var(--dgold);color:var(--dgold)}.bm-tag.need{border:1.5px dashed var(--red);color:var(--red)}
.bm-fig{display:flex;flex-direction:column;gap:2px}
.bm-fv{font-family:'Bebas Neue',sans-serif;font-size:26px;line-height:1}
.bm-fl{font-size:11.5px;color:var(--mut);line-height:1.3}
.bm-dots{display:inline-flex;gap:4px;flex-shrink:0}
.bm-dots i{width:11px;height:11px;border-radius:50%;border:1.5px solid var(--ink)}
.bm-dots .s-done{background:var(--ink)}.bm-dots .s-now{background:#d4a94f;border-color:#d4a94f}.bm-dots .s-later{background:transparent}
.bm-dots .s-none,.bm-dots .s-empty{border:1.5px dashed var(--grey)}
.bm-steps{display:flex;flex-direction:column}.bm-steps > *{display:flex;align-items:center;gap:8px;font-size:13px;line-height:1.35;padding:2px 0}
.bm-steps > * > i{width:13px;height:13px;border-radius:50%;border:1.5px solid var(--ink);flex-shrink:0}
.bm-steps > * > em{font-style:normal;font-size:11px;font-weight:600;color:var(--mut);white-space:nowrap}
.bm-steps .s-done i{background:var(--ink)}.bm-steps .s-now i{background:#d4a94f;border-color:#d4a94f;box-shadow:0 0 0 3px rgba(212,169,79,.3)}
.bm-steps .s-now span{font-weight:600}.bm-steps .s-none i{border-style:dashed;border-color:var(--grey)}.bm-steps .s-none span{color:var(--mut)}
.bm-open{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 14px;border:1.5px solid var(--ink);border-radius:var(--btnr);background:transparent;font-size:13px;font-weight:600;white-space:nowrap}
.bm-foot{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:24px;margin-top:12px;align-items:start}
.bm-lab{font-size:13px;font-weight:600;margin-bottom:8px}
.bm-pi{display:flex;gap:10px;font-size:13.5px;line-height:1.38;margin-bottom:6px}
.bm-pm{width:15px;height:15px;border:2px solid var(--ink);border-radius:4px;flex-shrink:0;margin-top:3px}
.bm-pi.wait .bm-pm{border:2px dashed var(--amber)}
.bm-need{font-size:12.5px;font-weight:600;color:var(--amber);margin-left:6px;white-space:nowrap}
.lp-acts{display:flex;flex-direction:column;gap:8px}
.lp-act{display:flex;flex-direction:column;align-items:flex-start;gap:1px;text-align:left;min-height:52px;padding:7px 16px;border:1.5px solid var(--ink);background:var(--card);border-radius:var(--btnr)}
.lp-act-k{font-weight:600;font-size:14px}.lp-act-d{font-size:12.5px;color:var(--mut)}
.lp .lp-act-go{background:var(--ink);color:var(--card);box-shadow:inset 6px 0 0 #d4a94f;padding-left:20px}.lp-act-go .lp-act-d{color:inherit;opacity:.85}
.lp .is-lit{outline:4px solid #d4a94f !important;outline-offset:3px;border-radius:6px}
@media (prefers-reduced-motion:reduce){.lp *{animation:none !important;transition:none !important}}
@container lp (max-width:699px){
 .bm{padding:16px 14px 22px}
 .bm-mast{flex-direction:column;align-items:flex-start;gap:10px}
 .bm-name{font-size:42px;white-space:normal}
 .lp-stamp-txt{max-width:none}
 .bm-need{display:block;margin-left:0;white-space:normal}
 .lp-stamp{width:100%;justify-content:space-between}.lp-stamp-txt{text-align:left}
 .bm-claim{font-size:34px}
 .bm-foot{grid-template-columns:1fr;gap:16px}
}
'''

SAMPLES = {'a': (canvas_a, CSS_A), 'b': (canvas_b, CSS_B), 'c': (canvas_c, CSS_C)}

# ------------------------------------------------------------------------------------------
# App shell: the same layout for every tool; the colours come from the tool's theme.
def shell_css(t):
    return '''
.bm-app,.bm-m{color:%(ink)s}
.bm-app .sh-bar{border-bottom-color:rgba(0,0,0,.14)}.bm-app .sh-rail{border-right-color:rgba(0,0,0,.14)}
.bm-app .sh-rail .sh-home,.bm-m .sh-homem{background:%(ink)s;box-shadow:0 0 0 3px %(ground)s,0 0 0 5.5px #d4a94f}
.bm-app .sh-bar .sh-t{color:%(ink)s}.bm-app .sh-bar small{color:%(ink)s;opacity:.8}
.bm-app .sh-btn-o,.bm-m .sh-btn-o{border-color:%(ink)s;color:%(ink)s}
.sh-rail a.sh-tab{width:60px;border-radius:0 12px 12px 0;color:%(ink)s;writing-mode:vertical-rl;transform:rotate(180deg);display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:13px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.bm-m .sh-mt{border-bottom-color:rgba(0,0,0,.14)}
.sh-mid main{flex-grow:1}
body{margin:0;background:%(ground)s}
''' % t

def desktop(t, canvas, chat):
    tabs = ''.join('<a class="sh-tab" href="#" style="height:%dpx;background:%s">%s</a>' % (h, c, n)
                   for (n, _), c, h in zip(TABS, t['rail'], [136, 124, 124, 140, 128]))
    rail = '<nav class="sh-rail" aria-label="Sections"><a class="sh-home" href="#" aria-current="page" aria-label="Home">%s</a>%s</nav>' % (ico(HOME, '#d4a94f', 22), tabs)
    bar = ('<header class="sh-bar"><div><span class="sh-t">%s</span><small>Home</small></div>'
           '<div style="display:flex;gap:10px"><button class="sh-btn-o">Guided tour</button><button class="sh-btn-g">Your tasks for the day</button></div></header>') % TOOL
    panel = ('<aside class="sh-chat" aria-label="Chat with Tojo"><div class="sh-panel"><div class="sh-ph"><div class="sh-av">T</div><div>'
             '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:28px;line-height:1">Tojo</div><div style="font-size:12px;color:#9CA9A1">250-bed hospital, Bhubaneswar</div></div></div>'
             '<div class="sh-pb">%s</div><div class="sh-inp"><label for="tojo-input" class="sr">Message Tojo</label><textarea id="tojo-input" rows="2" placeholder="Write to Tojo…"></textarea>'
             '<div style="display:flex;align-items:center"><button class="sh-ib" aria-label="Attach a file">%s</button><button class="sh-ib" aria-label="Attach a spreadsheet">%s</button>'
             '<button class="sh-ib" aria-label="Voice note">%s</button><span style="flex-grow:1"></span><button class="sh-send" aria-label="Send">%s</button></div></div></div></aside>') % (
        chat, ico(CLIP), ico(SHEET), ico(MIC), ico(SEND, '#10241a'))
    return '<div class="sh-app bm-app" style="background:%s">%s<div class="sh-mid">%s<main>%s</main></div>%s</div>' % (t['ground'], rail, bar, canvas, panel)

def mobile(t, canvas, chat):
    top = ('<div class="sh-mt"><div style="display:flex;align-items:center;gap:12px"><a href="#" class="sh-homem" aria-current="page" aria-label="Home" style="width:44px;height:44px;border-radius:50%%;display:flex;align-items:center;justify-content:center">%s</a>'
           '<div><div style="font-family:\'Bebas Neue\',sans-serif;font-size:24px;line-height:1">Virevo</div><div style="font-size:12px;opacity:.8">%s · Home</div></div></div><button class="sh-btn-o">Tour</button></div>') % (ico(HOME, '#d4a94f', 20), TOOL)
    who = '<div class="sh-who" style="color:inherit"><span class="sh-av" style="width:30px;height:30px;font-size:17px">T</span>Tojo</div>'
    inp = ('<div class="sh-mi" style="position:static"><div class="sh-box"><label for="tojo-input" class="sr">Message Tojo</label><input id="tojo-input" placeholder="Write to Tojo…">'
           '<button class="sh-ib" style="width:40px;height:40px" aria-label="Attach a file">%s</button><button class="sh-ib" style="width:40px;height:40px;border-radius:50%%;background:rgba(16,36,26,.08)" aria-label="Voice note">%s</button></div>'
           '<button class="sh-send" aria-label="Send">%s</button></div>') % (ico(CLIP, '#10241a', 19), ico(MIC, '#10241a', 19), ico(SEND, '#10241a'))
    foot = '<nav class="sh-mf" style="position:static" aria-label="Sections">%s</nav>' % ''.join('<a href="#" aria-label="%s">%s</a>' % (n, ico(dd, '#F3F1EA', 22)) for n, dd in TABS)
    return '<div class="sh-m bm-m" style="background:%s">%s<div class="sh-mc">%s%s<div class="sh-mpanel">%s</div></div>%s%s</div>' % (t['ground'], top, who, canvas, chat, inp, foot)

JS = r'''
(function(){
  var input=document.getElementById('tojo-input');
  var pts=[].slice.call(document.querySelectorAll('.sh-pt'));
  function sel(){return pts.filter(function(p){return p.getAttribute('aria-pressed')==='true';}).map(function(p){return p.getAttribute('data-n');});}
  function tags(){return sel().map(function(n){return '@Point'+n;}).join(' ');}
  function say(t){var g=tags();input.value=(g?g+' ':'')+t;input.focus();}
  pts.forEach(function(p){p.addEventListener('click',function(){
    p.setAttribute('aria-pressed',p.getAttribute('aria-pressed')==='true'?'false':'true');
    var s=sel();[].slice.call(document.querySelectorAll('.lp [data-pt]')).forEach(function(el){el.classList.toggle('is-lit',s.indexOf(el.getAttribute('data-pt'))>=0);});
    var g=tags();input.value=(g?g+' ':'')+input.value.replace(/@Point\d+\s*/g,'');});});
  [].slice.call(document.querySelectorAll('.sh-pr,.lp-act,.bm-open')).forEach(function(b){b.addEventListener('click',function(ev){ev.stopPropagation();say(b.getAttribute('data-text'));});});
  [].slice.call(document.querySelectorAll('.lp-refresh')).forEach(function(b){b.addEventListener('click',function(){
    var s=b.closest('.lp-stamp');s.querySelector('.lp-stamp-at').textContent=b.getAttribute('data-fresh');
    s.querySelector('.lp-stamp-since').textContent=b.getAttribute('data-fresh-since');b.classList.add('is-done');});});
  /* A: pick a bed, its steps open under the row (desktop) or under the bed (phone) */
  [].slice.call(document.querySelectorAll('.js-pick')).forEach(function(b){b.addEventListener('click',function(){
    var g=b.getAttribute('data-grp'),k=b.getAttribute('data-key');
    [].slice.call(document.querySelectorAll('.js-pick[data-grp="'+g+'"]')).forEach(function(o){o.setAttribute('aria-pressed',o===b?'true':'false');});
    [].slice.call(document.querySelectorAll('[data-det^="'+g+':"]')).forEach(function(d){d.hidden=d.getAttribute('data-det')!==g+':'+k;});});});
  /* B: pick a small bed, the room caption names its step */
  [].slice.call(document.querySelectorAll('.js-bed')).forEach(function(b){b.addEventListener('click',function(){
    var room=b.closest('.b-room');[].slice.call(room.querySelectorAll('.js-bed')).forEach(function(o){o.setAttribute('aria-pressed',o===b?'true':'false');});
    var c=room.querySelector('.b-capt');c.textContent=b.getAttribute('data-cap');c.classList.add('is-set');});});
  /* C: turn back a patch to see its steps */
  [].slice.call(document.querySelectorAll('.js-turn')).forEach(function(b){b.addEventListener('click',function(){
    b.setAttribute('aria-expanded',b.getAttribute('aria-expanded')==='true'?'false':'true');});});
})();
'''

FONTS = None
def page(sample, state, view):
    global FONTS
    if FONTS is None: FONTS = embedded_fonts()
    t = THEMES[sample]; fn, css = SAMPLES[sample]; d = DATA[state]
    canvas = '<div class="lp-host"><div class="lp bm bm-%s" data-lp-state="%s" style="%s">%s</div></div>' % (sample, state, t['vars'], fn(d, state == 'empty'))
    chat = chat_html(d['chat'])
    body = desktop(t, canvas, chat) if view == 'desktop' else mobile(t, canvas, chat)
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Bed Management home, sample %s</title>%s<style>%s%s%s%s</style></head><body>%s<script>%s</script></body></html>') % (
        sample.upper(), FONTS, SHELL_CSS, shell_css(t), BASE_CSS, css, body, JS)

def build(out):
    os.makedirs(out, exist_ok=True)
    pages = {}
    for s in SAMPLES:
        for st in ('filled', 'empty'):
            for v in ('desktop', 'mobile'):
                h = page(s, st, v); pages['%s.%s.%s' % (s, v, st)] = h
                open(os.path.join(out, 'home-%s.%s.%s.html' % (s, v, st)), 'w').write(h)
    return pages


# ------------------------------------------------------------------------------------------
# Review file: all three samples, both states, desktop and phone side by side, all live.
ABOUT = {
 'a': ('The ward bay', 'Four beds side by side under one curtain rail. Each part of the work is one bed. The headboard says how far it has got, the foot chart counts the steps. Pick a bed to open its steps.', 'Linen and deep teal'),
 'b': ('The ward plan', 'A ward seen from above. Each part of the work is a room off one corridor, with one small bed for each step. The nurses’ station counts the beds made up. Pick a small bed to read its step.', 'Pale slate and navy ink'),
 'c': ('The quilt', 'One big bed. Its quilt is sewn from four patches, one for each part of the work, and the pillow holds the overall count. Turn back a patch to see its steps.', 'Sand and brick'),
}
def review(pages):
    data = json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')
    about = json.dumps(ABOUT, ensure_ascii=False)
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>Sample %s</b><span>%s</span><i style="background:%s"></i></button>' % (
        k, 'true' if k == 'a' else 'false', k.upper(), e(v[0]), THEMES[k]['ground']) for k, v in ABOUT.items())
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bed Management home samples</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@400;500;600&display=swap">
<style>
:root{--bg:#F4F1EA;--ink:#10241a;--mut:#4d5a52;--line:#d6d0c2;--card:#fff}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Poppins,system-ui,sans-serif}
.rv{max-width:1880px;margin:0 auto;padding:24px 20px 60px}
h1{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:44px;line-height:1;margin:0}
.rv-intro{color:var(--mut);font-size:14px;margin:6px 0 18px;max-width:900px}
.rv-bar{display:flex;flex-wrap:wrap;gap:12px;align-items:stretch;margin-bottom:14px}
.rv-s{display:flex;flex-direction:column;align-items:flex-start;gap:2px;min-height:56px;padding:8px 16px 8px 44px;border:1.5px solid var(--ink);border-radius:10px;background:var(--card);font:inherit;color:inherit;cursor:pointer;position:relative;text-align:left}
.rv-s i{position:absolute;left:12px;top:50%;width:22px;height:22px;margin-top:-11px;border-radius:50%;border:1.5px solid var(--ink)}
.rv-s b{font-size:12px}.rv-s span{font-size:14px;font-weight:600}
.rv-s[aria-pressed=true]{background:var(--ink);color:#F3F1EA;box-shadow:inset 0 -4px 0 #d4a94f}
.rv-st{display:flex;border:1.5px solid var(--ink);border-radius:24px;overflow:hidden;align-self:center}
.rv-st button{min-height:44px;padding:0 18px;border:0;background:var(--card);font:500 13px Poppins,sans-serif;color:var(--ink);cursor:pointer}
.rv-st button[aria-pressed=true]{background:#d4a94f;font-weight:600}
.rv-about{background:var(--card);border:1.5px solid var(--line);border-radius:10px;padding:10px 16px;font-size:14px;margin-bottom:16px}
.rv-about b{font-weight:600}.rv-about em{font-style:normal;color:var(--mut);font-size:12.5px;margin-left:8px}
.rv-views{display:flex;gap:24px;align-items:flex-start}
.rv-col{display:flex;flex-direction:column;gap:6px}
.rv-lab{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.rv-desk{flex:1 1 auto;min-width:0}
.rv-dwrap{width:100%;overflow:hidden;border:1.5px solid var(--line);border-radius:10px;background:#fff}
.rv-dwrap iframe{width:1440px;border:0;transform-origin:0 0;display:block}
.rv-phone iframe{width:390px;border:0;display:block}
.rv-phone .rv-pwrap{width:390px;border:10px solid #1b1b1b;border-radius:34px;overflow:hidden;background:#fff}
.rv-note{font-size:12.5px;color:var(--mut);margin-top:14px}
@media (max-width:1000px){.rv-views{flex-direction:column}.rv-phone .rv-pwrap{width:370px;max-width:100%}}
</style></head><body><div class="rv">
<h1>Bed Management · home page samples</h1>
<p class="rv-intro">Three ways to lay out the four summaries so the page says “beds” at a glance. Every sample keeps the same zones, the same chat panel and the same three buttons as the Discharge Process pages. Everything is live: pick a bed, press Refresh now, pick a point in the chat, or press a button to fill the message box.</p>
<div class="rv-bar">@@PICKS@@<div class="rv-st" role="group" aria-label="Page state"><button type="button" data-st="filled" aria-pressed="true">In progress</button><button type="button" data-st="empty" aria-pressed="false">First visit</button></div></div>
<div class="rv-about" id="about"></div>
<div class="rv-views">
 <div class="rv-col rv-desk"><div class="rv-lab">Desktop · 1440 wide, shown to fit</div><div class="rv-dwrap" id="dwrap"><iframe id="fd" title="Desktop view"></iframe></div></div>
 <div class="rv-col rv-phone"><div class="rv-lab">Phone · 390 wide</div><div class="rv-pwrap"><iframe id="fm" title="Phone view"></iframe></div></div>
</div>
<p class="rv-note">Colours shown here are for the home page only. Once a sample is picked, the four place pages (Diagnosis, Solutions, Automations, Processes) are drawn to follow it.</p>
</div>
<script>
var P=@@DATA@@, A=@@ABOUT@@, cur={s:'a',st:'filled'};
var fd=document.getElementById('fd'), fm=document.getElementById('fm'), dw=document.getElementById('dwrap');
function fit(){var sc=Math.min(1,dw.clientWidth/1440);fd.style.transform='scale('+sc+')';
  try{var h=fd.contentDocument.documentElement.scrollHeight;fd.style.height=h+'px';dw.style.height=Math.ceil(h*sc)+'px';}catch(e){}
  try{fm.style.height=fm.contentDocument.documentElement.scrollHeight+'px';}catch(e){}}
function show(){fd.srcdoc=P[cur.s+'.desktop.'+cur.st];fm.srcdoc=P[cur.s+'.mobile.'+cur.st];
  var a=A[cur.s];document.getElementById('about').innerHTML='<b>Sample '+cur.s.toUpperCase()+' · '+a[0]+'.</b> '+a[1]+'<em>Colours: '+a[2]+'</em>';}
[fd,fm].forEach(function(f){f.addEventListener('load',function(){fit();setTimeout(fit,400);
  try{f.contentDocument.addEventListener('click',function(){setTimeout(fit,50);});}catch(e){}});});
window.addEventListener('resize',fit);
[].slice.call(document.querySelectorAll('.rv-s')).forEach(function(b){b.addEventListener('click',function(){cur.s=b.getAttribute('data-s');
  [].slice.call(document.querySelectorAll('.rv-s')).forEach(function(o){o.setAttribute('aria-pressed',o===b?'true':'false');});show();});});
[].slice.call(document.querySelectorAll('.rv-st button')).forEach(function(b){b.addEventListener('click',function(){cur.st=b.getAttribute('data-st');
  [].slice.call(document.querySelectorAll('.rv-st button')).forEach(function(o){o.setAttribute('aria-pressed',o===b?'true':'false');});show();});});
show();
</script></body></html>'''.replace('@@PICKS@@', picks).replace('@@ABOUT@@', about).replace('@@DATA@@', data)

def main():
    out = os.path.join(ROOT, 'out', 'landing', 'home')
    pages = build(out)
    rv = os.path.join(out, 'bed-management-home-samples.html')
    open(rv, 'w').write(review(pages))
    print('built', len(pages), 'pages and', rv)

if __name__ == '__main__':
    main()
