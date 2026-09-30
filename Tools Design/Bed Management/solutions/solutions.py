"""
Bed Management · Solutions page. Three samples, drawn from the home page's ward plan.
Look: the fit-out. Pale sage-grey ground, deep green-slate ink, plan paper, the small bed.

  A  Rooms being fitted out   each fix is a room on the plan; its walls, door and bed go in as it moves from idea to agreed
  B  The corridor of fixes    the fixes as rooms off one corridor, each door plate carrying its four stops
  C  Plan sheets              each fix as a drawn plan sheet, with a revision mark for each time it is redrawn

Run:  python3 solutions.py [--measure]  -> out/bed-management/solutions/
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from bm_common import (e, ico, ICONS, STAMP, bed_svg, BED_CSS, masthead, emblem, standing, section, pending,  # noqa: E402
                       actions, tag, pt, theme, place_main)

PLACE = 'Solutions'
THEME = theme('#E2EAE7', '#FAFCFB', '#173B38', '#46605C', '#B1C6C0', '#E7F0EC', '#8A9E99',
              ['#D6E0DC', '#DDE5E1', '#D3DED9', '#DBE3DF', '#D5DFDA'], '4px', '--acc:#2C7266')
STAGES = ['Idea', 'Shaped', 'Tested with you', 'Agreed']

DATA = {
 'filled': {
  'claim': 'Three fixes on the table. One is taking shape.',
  'deck': 'The one bed list is on its second drawing. The other two wait for the diagnosis to finish.',
  'fixes': [
   {'n': 1, 'name': 'One bed list everyone can see', 'stage': 1, 'pt': 1,
    'what': 'The wards, housekeeping and the admissions desk all see the same list of beds: in use, being cleaned and ready.',
    'deps': [['The bed list kept up to date as patients leave', 'open'], ['The admissions desk agrees to use it', 'settled']],
    'saves': ['About 1 hour', 'off each bed’s wait', 'guess'],
    'revs': [['1', 'A shared sheet on the ward wall, filled in by hand.'], ['2', 'One list on a screen, seen by the wards, housekeeping and admissions.']]},
   {'n': 2, 'name': 'Housekeeping called the moment a patient leaves', 'stage': 0, 'pt': 2,
    'what': 'The ward calls housekeeping when the patient walks out, not when the register is updated.',
    'deps': [['Who on the ward makes the call', 'open']],
    'saves': ['About 30 minutes', 'off each bed’s wait', 'guess'],
    'revs': [['1', 'The ward nurse calls housekeeping as the patient leaves.']]},
   {'n': 3, 'name': 'Tomorrow’s free beds planned tonight', 'stage': 0, 'pt': 3,
    'what': 'Each evening the ward lists who will go home tomorrow, so the morning’s new patients have beds waiting.',
    'deps': [['Doctors decide the evening before', 'open'], ['Joins up with the Discharge Process work', 'settled']],
    'saves': None,
    'revs': [['1', 'An evening list of tomorrow’s likely discharges, sent to admissions by 9 PM.']]},
  ],
  'pending': [
   {'text': 'Draw the one bed list a third time, with the housekeeping view added.'},
   {'text': 'Find who on the ward would make the housekeeping call.', 'need': 'Needs a name from you', 'pt': 4},
   {'text': 'Put a price on each fix once the wait is priced.'},
   {'text': 'Agree with you which fix to try first.'},
  ],
  'actions': {'go': {'detail': 'Redraw the one bed list', 'say': 'Let’s redraw the one bed list with the housekeeping view'},
              'add': {'detail': 'Suggest a fix of your own', 'say': 'Here is a fix I want to add: '},
              'jump': {'tab': 'Automations', 'detail': 'Three ideas are waiting', 'say': 'Take me to Automations'}},
  'chat': {'text': ['Here is where the fixes stand. The one bed list is on its second drawing.',
                    'The housekeeping call and the evening plan are still ideas. They get shaped once the diagnosis names the cause.'],
           'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
           'note': 'One list, seen by everyone, comes first.',
           'points': [{'n': 1, 'label': 'The one bed list'}, {'n': 2, 'label': 'The housekeeping call'},
                      {'n': 3, 'label': 'Planning tomorrow’s beds tonight'}, {'n': 4, 'label': 'Who makes the call'}],
           'prompts': ['Let’s redraw the bed list', 'Which fix saves the most time?', 'I have a fix of my own']},
 },
 'empty': {
  'claim': 'No fixes yet',
  'deck': 'Fixes are drawn once the diagnosis names why beds are late. Each one is shaped with you before it is agreed.',
  'fixes': [],
  'pending': [
   {'text': 'Wait for the diagnosis to name the cause.'},
   {'text': 'Draw the first fixes and test them with you.'},
   {'text': 'Agree which fix to try first.'},
  ],
  'actions': {'go': {'detail': 'Finish the diagnosis first', 'say': 'Take me back to the diagnosis'},
              'add': {'detail': 'Suggest a fix of your own', 'say': 'Here is a fix I want to add: '},
              'jump': {'tab': 'Automations', 'detail': 'Fills in once a fix is agreed', 'say': 'Take me to Automations'}},
  'chat': {'text': ['This is your Solutions page. Fixes appear here once the diagnosis names the cause.',
                    'If you already have a fix in mind, tell me and I will keep it ready.'],
           'note': 'Name the cause first. Then fix it.', 'points': [],
           'prompts': ['Take me to the diagnosis', 'I already have a fix in mind', 'How are fixes chosen?']},
 },
}

def top(d, empty):
    return masthead('Bed Management', PLACE, emblem(ICONS[PLACE]), STAMP['empty' if empty else 'filled']) + standing(d['claim'], d['deck'], empty)

def tail(d):
    return pending(d['pending']) + actions(d['actions'])

def track(f, cls='so-track', inline=False):
    o, it = ('span', 'span') if inline else ('ol', 'li')
    return '<%s class="%s" aria-label="%s">%s</%s>' % (o, cls, 'Now at: ' + STAGES[f['stage']], ''.join(
        '<%s class="s-%s"><i aria-hidden="true"></i><span>%s</span></%s>' % (it, 'done' if i < f['stage'] else 'now' if i == f['stage'] else 'later', e(n), it)
        for i, n in enumerate(STAGES)), o)

def deps(f):
    return '<ul class="so-deps">%s</ul>' % ''.join('<li class="d-%s"><i aria-hidden="true"></i>%s<em>%s</em></li>' % (
        s, e(t), 'Settled' if s == 'settled' else 'Still open') for t, s in f['deps'])

def saves(f):
    if not f['saves']: return '<p class="so-save is-none">What it saves: worked out once the wait is priced</p>'
    v, l, t = f['saves']
    return '<p class="so-save"><b>%s</b> %s %s</p>' % (e(v), e(l), tag(t))

def rev_badge(f):
    return '<span class="so-rev" title="Drawn %d times"><span>%s</span></span>' % (len(f['revs']), f['revs'][-1][0])

def empty_note(text):
    return '<div class="so-empty bm-paper"><span class="bmb s-empty">%s</span><p>%s</p></div>' % (bed_svg(40), e(text))

COMMON = BED_CSS + '''
.so-track{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));position:relative}
.so-track > *{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:6px;font-size:12px;color:var(--mut);padding-top:2px}
.so-track > *::before{content:"";position:absolute;left:0;right:0;top:9px;height:2px;background:var(--line)}
.so-track > *:last-child::before{right:auto;width:10px}
.so-track > *.s-done::before{background:var(--ink)}
.so-track i{position:relative;width:18px;height:18px;border-radius:50%;border:2px solid var(--ink);background:var(--card)}
.so-track .s-done i{background:var(--ink)}
.so-track .s-now i{background:#d4a94f;border-color:#d4a94f;box-shadow:0 0 0 4px rgba(212,169,79,.3)}
.so-track .s-now span{color:var(--ink);font-weight:600}
.so-deps{display:flex;flex-direction:column;gap:6px}
.so-deps li{display:flex;align-items:center;gap:8px;font-size:13.5px;line-height:1.4}
.so-deps i{width:12px;height:12px;border-radius:50%;flex-shrink:0}
.so-deps .d-settled i{background:var(--ink)}.so-deps .d-open i{border:2px dashed var(--amber)}
.so-deps em{font-style:normal;font-size:11.5px;font-weight:600;color:var(--mut);margin-left:auto;white-space:nowrap;padding-left:10px}
.so-deps .d-open em{color:var(--amber)}
.so-save{font-size:13.5px;color:var(--mut);display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.so-save b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:24px;color:var(--ink);line-height:1}
.so-save.is-none{font-style:italic}
.so-rev{display:inline-flex;align-items:flex-end;justify-content:center;width:30px;height:26px;background:var(--ink);clip-path:polygon(50% 0,100% 100%,0 100%);color:var(--card);font-size:11px;font-weight:700;padding-bottom:2px;flex-shrink:0}
.so-lab{font-size:12px;font-weight:600;color:var(--mut);margin-bottom:6px}
.so-empty{display:flex;align-items:center;gap:16px;border:2px dashed var(--grey);border-radius:6px;padding:26px 22px}
.so-empty p{font-size:14.5px;color:var(--mut)}
'''

# ------------------------------------------------------------------------------------------
# A · Rooms being fitted out
def room_svg(stage):
    """The room plan grows with the fix: idea = dashed outline, shaped = walls and door gap,
    tested = a bed in the room, agreed = the bed made up."""
    walls = ('<path class="w %s" d="M6 6h148v108H6z"/>' % ('dash' if stage == 0 else '')) if stage == 0 else (
        '<path class="w" d="M6 114V6h148v108H84"/><path class="w" d="M6 114h46"/><path class="dr" d="M52 114a32 32 0 0132-32"/>')
    bed = ''
    if stage >= 2:
        bed = ('<g class="bd %s"><rect x="100" y="18" width="40" height="6" rx="3" class="h"/><rect x="102" y="24" width="36" height="58" rx="4" class="f"/>'
               '<rect x="108" y="29" width="24" height="10" rx="5" class="p"/><path class="k" d="M102 46h36v32a4 4 0 01-4 4h-28a4 4 0 01-4-4z"/></g>') % ('made' if stage >= 3 else '')
    grid = '<path class="g" d="M6 34h148M6 62h148M6 90h148M40 6v108M76 6v108M112 6v108"/>' if stage == 0 else ''
    return '<svg class="sa-svg" viewBox="0 0 160 120" width="200" height="150" aria-hidden="true">%s%s%s</svg>' % (grid, walls, bed)

CAPS = ['Only an outline: idea', 'Walls up: shaped', 'Bed in: tested with you', 'Bed made up: agreed']
def stage_views(f):
    g = 'sa%d' % f['n']
    views = ''.join('<div class="sa-v" data-det="%s:%d"%s>%s<span class="sa-cap">%s%s</span></div>' % (
        g, i, '' if i == f['stage'] else ' hidden', room_svg(i), e(CAPS[i]), ' · now' if i == f['stage'] else ' · what it will look like' if i > f['stage'] else '') for i in range(4))
    btns = ''.join('<button class="sa-sb js-pick" type="button" data-grp="%s" data-key="%d" aria-pressed="%s" aria-label="Show the room at: %s">%d</button>' % (
        g, i, 'true' if i == f['stage'] else 'false', STAGES[i], i + 1) for i in range(4))
    return views + '<div class="sa-sbs" role="group" aria-label="See the room at each stop">%s</div>' % btns

def canvas_a(d, empty):
    if not d['fixes']:
        body = empty_note('The first fix appears here as a dashed outline, and its room is built as you shape it together.')
    else:
        body = ''.join(
            '<article class="sa-fix"%s><div class="sa-draw bm-paper">%s</div>'
            '<div class="sa-main"><div class="sa-h"><span class="sa-n">Fix %d</span>%s<span class="sa-rl">Drawn %s</span></div><h4>%s</h4><p class="sa-what">%s</p>%s%s</div>'
            '<div class="sa-side"><div class="so-lab">What it depends on</div>%s</div></article>' % (
                pt(f.get('pt')), stage_views(f),
                f['n'], rev_badge(f), 'once' if len(f['revs']) == 1 else '%d times' % len(f['revs']), e(f['name']), e(f['what']), track(f), saves(f), deps(f))
            for f in d['fixes'])
    agreed = sum(1 for f in d['fixes'] if f['stage'] == 3)
    sub = ('%d of %d agreed. The room is built as the fix is shaped. Press 1 to 4 to see each stop.' % (agreed, len(d['fixes']))) if d['fixes'] else 'Nothing drawn yet'
    return top(d, empty) + section('The fixes, as rooms being fitted out', '<div class="sa-list">%s</div>' % body, 'sa-sec', sub) + tail(d)

CSS_A = '''
.sa-list{display:flex;flex-direction:column;gap:22px}
.sa-fix{display:grid;grid-template-columns:220px minmax(0,1fr) 250px;gap:26px;align-items:start;padding:22px;background:var(--card);border:2px solid var(--ink);border-radius:4px}
.sa-draw{display:flex;flex-direction:column;align-items:center;gap:8px;padding:10px;border:1.5px solid var(--line);border-radius:4px}
.sa-svg .w{fill:none;stroke:var(--ink);stroke-width:5;stroke-linejoin:round}
.sa-svg .w.dash{stroke-width:2.5;stroke-dasharray:7 5;stroke:var(--grey)}
.sa-svg .dr{fill:none;stroke:var(--line);stroke-width:1.5;stroke-dasharray:4 3}
.sa-svg .g{stroke:var(--line);stroke-width:1;stroke-dasharray:2 4}
.sa-svg .bd .h{fill:var(--ink)}.sa-svg .bd .f{fill:var(--card);stroke:var(--ink);stroke-width:2}.sa-svg .bd .p{fill:var(--soft);stroke:var(--ink);stroke-width:1.2}.sa-svg .bd .k{fill:var(--soft)}
.sa-svg .bd.made .k{fill:var(--ink)}
.sa-cap{display:block;font-size:12px;color:var(--mut);text-align:center}
.sa-v{display:flex;flex-direction:column;align-items:center;gap:6px}.sa-v[hidden]{display:none}
.sa-sbs{display:flex;gap:6px;justify-content:center}
.sa-sb{width:40px;height:40px;border-radius:50%;border:1.5px solid var(--ink);background:var(--card);font-size:13px;font-weight:600}
.sa-sb[aria-pressed=true]{background:#d4a94f;border-color:#d4a94f}
.sa-main{display:flex;flex-direction:column;gap:12px;min-width:0}
.sa-h{display:flex;align-items:center;gap:10px}
.sa-n{font-size:12px;font-weight:600;color:var(--acc)}
.sa-rl{font-size:12px;color:var(--mut)}
.sa-main h4{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:30px;line-height:1}
.sa-what{font-size:14.5px;line-height:1.55}
.sa-side{border-left:1.5px dashed var(--line);padding-left:20px}
@container lp (max-width:699px){
 .sa-fix{grid-template-columns:1fr;gap:16px;padding:16px}
 .sa-draw{flex-direction:row;flex-wrap:wrap;justify-content:flex-start;gap:14px}
 .sa-v{flex-direction:row}
 .sa-svg{width:120px;height:90px}
 .sa-cap{text-align:left}
 .sa-side{border-left:0;border-top:1.5px dashed var(--line);padding:14px 0 0}
}
'''

# ------------------------------------------------------------------------------------------
# B · The corridor of fixes
def canvas_b(d, empty):
    if not d['fixes']:
        rooms = ''.join('<div class="sb-room is-empty"><span class="bmb s-empty">%s</span><p>A fix moves in here once the cause is named.</p></div>' % bed_svg(40) for _ in range(3))
        plan = '<div class="sb-plan bm-paper"><div class="sb-rooms">%s</div><div class="sb-corr"><span>Corridor</span><span class="sb-stn">Nurses’ station · no fixes yet</span></div></div>' % rooms
        return top(d, empty) + section('The corridor of fixes', plan, 'sb-sec', 'One room for each fix') + tail(d)
    rooms = ''.join(
        '<button class="sb-room js-pick s%d" type="button" data-grp="sb" data-key="%d" aria-pressed="%s"%s><span class="sb-plate"><span>Fix %d</span>%s</span>'
        '<b class="sb-name">%s</b>%s<span class="sb-door" aria-hidden="true"></span></button>' % (
            f['stage'], f['n'], 'true' if f['n'] == 1 else 'false', pt(f.get('pt')), f['n'], rev_badge(f), e(f['name']), track(f, 'so-track sb-track', True))
        for f in d['fixes'])
    agreed = sum(1 for f in d['fixes'] if f['stage'] == 3)
    dets = ''.join(
        '<div class="sb-det" data-det="sb:%d"%s><div><div class="so-lab">What it is</div><p class="sb-what">%s</p>%s</div>'
        '<div><div class="so-lab">What it depends on</div>%s</div><div><div class="so-lab">How it was drawn</div><ol class="sb-revs">%s</ol></div></div>' % (
            f['n'], '' if f['n'] == 1 else ' hidden', e(f['what']), saves(f), deps(f),
            ''.join('<li><span class="so-rev"><span>%s</span></span>%s</li>' % (r, e(t)) for r, t in f['revs'])) for f in d['fixes'])
    plan = ('<div class="sb-plan bm-paper"><div class="sb-rooms">%s</div><div class="sb-corr"><span>Corridor</span><span class="sb-stn">Nurses’ station · <b>%d of %d fixes agreed</b></span></div></div>%s') % (
        rooms, agreed, len(d['fixes']), dets)
    return top(d, empty) + section('The corridor of fixes', plan, 'sb-sec', 'One room for each fix. Each door plate carries its four stops, from idea to agreed. Pick a room to open it.') + tail(d)

CSS_B = '''
.sb-plan{border:3px solid var(--ink);border-radius:4px}
.sb-rooms{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.sb-room{position:relative;display:flex;flex-direction:column;align-items:stretch;gap:14px;text-align:left;background:transparent;border:0;border-right:2.5px solid var(--ink);border-bottom:2.5px solid var(--ink);padding:20px 20px 26px;min-width:0}
.sb-room:last-child{border-right:0}
.sb-room.is-empty{align-items:flex-start;color:var(--mut);font-size:14px;border-bottom-style:dashed}
.sb-plate{display:flex;align-items:center;justify-content:space-between}
.sb-plate>span:first-child{background:var(--ink);color:var(--card);font-size:12px;font-weight:600;padding:3px 10px;border-radius:3px}
.sb-room.s0 .sb-plate>span:first-child{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--ink)}
.sb-name{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:27px;line-height:1.05}
.sb-beds{display:none}
.sb-door{position:absolute;left:24px;bottom:-2.5px;width:50px;height:4px;background:var(--card)}
.sb-room[aria-pressed=true]{background:rgba(212,169,79,.14);box-shadow:inset 0 4px 0 #d4a94f}
.sb-corr{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px 20px;background:repeating-linear-gradient(90deg,var(--line) 0 14px,transparent 14px 26px) 0 50%/100% 1.5px no-repeat}
.sb-corr>span:first-child{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);background:var(--card);padding-right:8px}
.sb-stn{background:var(--ink);color:var(--card);border-radius:22px;padding:8px 18px;font-size:13px}
.sb-stn b{font-weight:600;color:#E8D3A2}
.sb-det{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:26px;margin-top:18px;padding:22px;background:var(--card);border:2px solid var(--ink);border-radius:4px}
.sb-det[hidden]{display:none}
.sb-what{font-size:14.5px;line-height:1.55;margin-bottom:12px}
.sb-revs{display:flex;flex-direction:column;gap:10px}
.sb-revs li{display:flex;gap:10px;align-items:flex-start;font-size:13.5px;line-height:1.45}
@container lp (max-width:699px){
 .sb-rooms{grid-template-columns:1fr}
 .sb-room{border-right:0;padding:16px}
 .sb-door{display:none}
 .sb-room[aria-pressed=true]{box-shadow:inset 4px 0 0 #d4a94f}
 .sb-corr{flex-direction:column;align-items:flex-start;background:none}
 .sb-det{grid-template-columns:1fr;gap:18px;padding:16px}
}
'''

# ------------------------------------------------------------------------------------------
# C · Plan sheets
def canvas_c(d, empty):
    if not d['fixes']:
        body = empty_note('Each fix gets its own plan sheet. A revision mark is added every time it is redrawn with you.')
        return top(d, empty) + section('Plan sheets', body, 'sc-sec') + tail(d)
    sheets = []
    for f in d['fixes']:
        revs = f['revs']
        marks = ''.join('<button class="sc-rm js-pick" type="button" data-grp="sc%d" data-key="%s" aria-pressed="%s" aria-label="Revision %s"><span class="so-rev"><span>%s</span></span></button>' % (
            f['n'], r, 'true' if r == revs[-1][0] else 'false', r, r) for r, _ in revs)
        notes = ''.join('<p class="sc-rn" data-det="sc%d:%s"%s><b>Drawing %s.</b> %s</p>' % (f['n'], r, '' if r == revs[-1][0] else ' hidden', r, e(t)) for r, t in revs)
        behind = ''.join('<span class="sc-behind b%d" aria-hidden="true"></span>' % i for i in range(1, len(revs)))
        sheets.append(
            '<article class="sc-sheet"%s>%s<div class="sc-face bm-paper"><div class="sc-main"><span class="sc-n">Fix %d</span><h4>%s</h4><p class="sc-what">%s</p>%s%s</div>'
            '<div class="sc-tb"><div class="sc-tbr"><span>Sheet</span><b>Fix %d of %d</b></div><div class="sc-tbr"><span>Revisions</span><div class="sc-rms">%s</div></div>%s'
            '<div class="sc-tbr"><span>Depends on</span>%s</div></div></div></article>' % (
                pt(f.get('pt')), behind, f['n'], e(f['name']), e(f['what']), track(f), saves(f), f['n'], len(d['fixes']), marks, notes, deps(f)))
    return top(d, empty) + section('Plan sheets', '<div class="sc-list">%s</div>' % ''.join(sheets), 'sc-sec',
                                   'One sheet for each fix. Sheets behind show earlier drawings. Pick a revision mark to read what changed.') + tail(d)

CSS_C = '''
.sc-list{display:flex;flex-direction:column;gap:34px}
.sc-sheet{position:relative;padding:0 14px 14px 0}
.sc-behind{position:absolute;inset:0;border:1.5px solid var(--ink);background:var(--soft);border-radius:2px}
.sc-behind.b1{transform:translate(10px,10px)}.sc-behind.b2{transform:translate(20px,20px)}
.sc-face{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 290px;border:2px solid var(--ink);border-radius:2px}
.sc-face::before,.sc-face::after{content:"";position:absolute;width:14px;height:14px;border:2px solid var(--acc)}
.sc-face::before{left:6px;top:6px;border-right:0;border-bottom:0}.sc-face::after{right:6px;bottom:6px;border-left:0;border-top:0}
.sc-main{display:flex;flex-direction:column;gap:14px;padding:26px 26px 24px}
.sc-n{font-size:12px;font-weight:600;color:var(--acc)}
.sc-main h4{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:32px;line-height:1}
.sc-what{font-size:14.5px;line-height:1.55;max-width:520px}
.sc-tb{border-left:2px solid var(--ink);display:flex;flex-direction:column;background:var(--card)}
.sc-tbr{padding:12px 16px;border-bottom:1.5px solid var(--ink);display:flex;flex-direction:column;gap:6px}
.sc-tbr:last-child{border-bottom:0;flex-grow:1}
.sc-tbr>span{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.sc-tbr b{font-size:14px}
.sc-rms{display:flex;gap:6px}
.sc-rm{padding:4px;border:0;background:none;border-radius:4px;min-width:40px;min-height:40px;display:flex;align-items:center;justify-content:center}
.sc-rm[aria-pressed=true]{outline:3px solid #d4a94f}
.sc-rn{padding:10px 16px 12px;border-bottom:1.5px solid var(--ink);font-size:13.5px;line-height:1.45;background:rgba(212,169,79,.1)}
.sc-rn[hidden]{display:none}
@container lp (max-width:699px){
 .sc-sheet{padding:0 8px 8px 0}
 .sc-behind.b1{transform:translate(6px,6px)}
 .sc-face{grid-template-columns:1fr}
 .sc-main{padding:20px 16px}
 .sc-main h4{font-size:28px}
 .sc-tb{border-left:0;border-top:2px solid var(--ink)}
}
'''

SAMPLES = {'a': (canvas_a, CSS_A), 'b': (canvas_b, CSS_B), 'c': (canvas_c, CSS_C)}
ABOUT = {
 'a': ('Rooms being fitted out', 'Each fix is one room on the plan. The room is built as the fix is shaped: a dashed outline for an idea, walls once it is shaped, a bed once it is tested with you, and the bed made up once agreed. Beside it: what it is, the four stops, what it saves and what it depends on.', 'The fit-out: pale sage-grey, deep green-slate, plan paper'),
 'b': ('The corridor of fixes', 'The home page’s plan, zoomed in: each fix is a room off one corridor, its door plate carrying the four stops, the nurses’ station counting fixes agreed. Pick a room to open what it is, what it depends on and how it was drawn.', 'The fit-out: pale sage-grey, deep green-slate, plan paper'),
 'c': ('Plan sheets', 'Each fix is a drawn plan sheet with a title block. Earlier drawings sit behind it, and each revision has a triangle mark. Pick a mark to read what changed in that drawing.', 'The fit-out: pale sage-grey, deep green-slate, plan paper'),
}

if __name__ == '__main__':
    place_main(PLACE, 'so', DATA, SAMPLES, COMMON, {k: THEME for k in SAMPLES}, ABOUT,
               'Three ways to draw the Solutions page for Bed Management, each taken from the ward plan on the home page. All three share one look for Solutions, the fit-out, and keep the same zones and three buttons.',
               'Each page may run to about two screens on desktop, so every part has room.')
