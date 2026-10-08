"""
Bed Management - the tool's own home page. Approved look: Sample B, the ward plan (30 Sep 2026),
redrawn with more space (v2): a desktop page may now run to 1.5-2 screens.

A ward seen from above: one room for each place off one corridor, one small bed for each step,
the nurses' station in the corridor counting the beds made up.
The unchosen v1 samples (A ward bay, C quilt) are kept in home_v1_samples.py for reference.
Run:  python3 home.py [--measure]  -> out/bed-management/home/
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from bm_common import *  # noqa: F401,F403
from bm_common import e, ico, ICONS, BED_ICO, STAMP, ROOT, bed_svg, bed_key, BED_CSS, masthead, emblem, standing, section, pending, actions, tag, build, review, measure, pt

STATUS = {'now': 'In use now', 'started': 'Being made ready', 'none': 'Not made up yet', 'empty': 'Empty room'}
STEP = {'done': 'Done', 'now': 'Now', 'later': 'Still to do', 'none': 'Not started'}

THEME = {'ground': '#E2E6EE', 'ink': '#1C2542', 'rail_bg': '#1C2542', 'rail_fg': '#d4a94f',
         'rail': ['#D8DDE8', '#E3E0EA', '#D5DCE6', '#DFE2EC', '#D9DEE6'],
         'vars': '--g:#E2E6EE;--card:#FAFBFD;--ink:#1C2542;--mut:#4A536E;--line:#B5BCCE;--soft:#EDF0F6;--grey:#8D94A8;--btnr:6px;--gridc:rgba(28,37,66,.045)'}

DATA = {
 'filled': {
  'claim': 'Beds come free too late for the patients who need them',
  'deck': 'Diagnosis is past halfway. Three fixes are on the table. Nothing is switched on or changed on the wards yet.',
  'places': [
   {'name': 'Diagnosis', 'status': 'now', 'pt': 1, 'head': 'Beds come free after 2 PM. Most new patients arrive by 11 AM.',
    'fig': ('75 minutes', 'Bed empty after the patient leaves', 'yours'), 'unit': 'stages done',
    'steps': [['Walk a bed’s day', 'done'], ['Count beds free each morning', 'done'], ['Match arrivals to free beds', 'now'], ['Price the wait', 'later'], ['Name the cause', 'later']]},
   {'name': 'Solutions', 'status': 'started', 'pt': 3, 'head': 'Three fixes on the table. One is taking shape.',
    'fig': ('About 1 hour', 'Could come off each bed’s wait', 'guess'), 'unit': 'fixes agreed',
    'steps': [['One bed list everyone can see', 'now'], ['Housekeeping called the moment a patient leaves', 'later'], ['Tomorrow’s free beds planned tonight', 'later']]},
   {'name': 'Automations', 'status': 'none', 'head': 'Three ideas wait for the one bed list to be agreed.', 'fig': None, 'unit': 'switched on',
    'steps': [['Bed marked free when the patient leaves', 'none'], ['Housekeeping told on their phone', 'none'], ['Tomorrow’s free beds listed tonight', 'none']]},
   {'name': 'Processes', 'status': 'none', 'head': 'Three changes wait for a trial ward.', 'fig': None, 'unit': 'tried on a ward',
    'steps': [['One bed owner on every shift', 'none'], ['Patients home by 11 AM on most days', 'none'], ['A 10-minute bed huddle at 8 AM', 'none']]},
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
  'claim': 'Nothing here yet',
  'deck': 'Start with Diagnosis. Tojo walks one bed’s day with you and fills this page as you go.',
  'places': [
   {'name': 'Diagnosis', 'status': 'empty', 'head': 'Fills in as you walk a bed’s day with Tojo.', 'fig': None, 'steps': []},
   {'name': 'Solutions', 'status': 'empty', 'head': 'Fills in once the cause is named.', 'fig': None, 'steps': []},
   {'name': 'Automations', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': []},
   {'name': 'Processes', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': []},
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

def room(i, p):
    if p['steps']:
        beds = ''.join('<button class="bmb s-%s js-cap" type="button" aria-pressed="false" data-cap="%s · %s" aria-label="%s: %s">%s</button>' % (
            s, e(t), STEP[s], e(t), STEP[s], bed_svg(44)) for t, s in p['steps'])
        cap = 'Pick a bed to read its step'
        done = sum(1 for _, s in p['steps'] if s == 'done')
        prog = '%d of %d %s' % (done, len(p['steps']), p['unit'])
    else:
        beds = ''.join('<span class="bmb s-empty">%s</span>' % bed_svg(44) for _ in range(3))
        cap, prog = 'Beds are set up as the work starts', 'Nothing yet'
    fig = ''
    if p['fig']:
        v, l, t = p['fig']
        fig = '<div class="h-fig"><span class="h-fv">%s</span><span class="h-fl">%s</span>%s</div>' % (e(v), e(l), tag(t))
    return ('<div class="h-room h-r%d" data-s="%s" data-capbox%s><span class="h-door" aria-hidden="true"></span>'
            '<div class="h-plate"><span class="h-pn">%s %s</span><span class="h-ps">%s</span></div>'
            '<p class="h-hl">%s</p>%s<div class="h-beds">%s</div>'
            '<div class="h-cap"><span class="js-capt" aria-live="polite">%s</span><b>%s</b></div></div>') % (
        i + 1, p['status'], pt(p.get('pt')), ico(ICONS[p['name']], 'currentColor', 20), e(p['name']), e(STATUS[p['status']]),
        e(p['head']), fig, beds, e(cap), e(prog))

def canvas(state):
    d = DATA[state]; empty = state == 'empty'
    rooms = [room(i, p) for i, p in enumerate(d['places'])]
    total = sum(len(p['steps']) for p in d['places']); made = sum(1 for p in d['places'] for _, s in p['steps'] if s == 'done')
    station = ('<div class="h-corr"><span class="h-cl">Corridor</span><div class="h-stn"><span class="h-sk">Nurses’ station</span>'
               '<span class="h-sv">%s</span><span class="h-bar"><i style="width:%d%%"></i></span></div><span class="h-cl">Corridor</span></div>') % (
        ('%d of %d beds made up' % (made, total)) if total else 'No beds set up yet', int(100 * made / total) if total else 0)
    plan = '<div class="h-plan bm-paper">%s%s%s</div>%s' % (''.join(rooms[:2]), station, ''.join(rooms[2:]), bed_key(('Made up: done', 'In use now', 'Still to do', 'Not started')))
    return (masthead('Virevo · 250-bed hospital, Bhubaneswar', 'Bed Management', emblem(BED_ICO), STAMP[state])
            + standing(d['claim'], d['deck'], empty)
            + section('Where each part of the work stands', plan, 'h-sec', 'One room for each part. Pick a small bed to read its step.')
            + pending(d['pending']) + actions(d['actions']))

CSS = BED_CSS + '''
.h-plan{display:grid;grid-template-columns:1fr 1fr;border:3.5px solid var(--ink);border-radius:4px}
.h-room{position:relative;padding:22px 24px 18px;display:flex;flex-direction:column;gap:12px;min-width:0}
.h-r1,.h-r3{border-right:2.5px solid var(--ink)}
.h-r1,.h-r2{border-bottom:2.5px solid var(--ink)}
.h-r3,.h-r4{border-top:2.5px solid var(--ink)}
.h-door{position:absolute;left:34px;width:52px;height:52px;pointer-events:none}
.h-r1 .h-door,.h-r2 .h-door{bottom:-2.5px;border-bottom:3px solid var(--card)}
.h-r3 .h-door,.h-r4 .h-door{top:-2.5px;border-top:3px solid var(--card)}
.h-r1 .h-door::after,.h-r2 .h-door::after{content:"";position:absolute;left:0;bottom:0;width:50px;height:50px;border-top:1.5px dashed var(--line);border-right:1.5px dashed var(--line);border-radius:0 50px 0 0}
.h-r3 .h-door::after,.h-r4 .h-door::after{content:"";position:absolute;left:0;top:0;width:50px;height:50px;border-bottom:1.5px dashed var(--line);border-right:1.5px dashed var(--line);border-radius:0 0 50px 0}
.h-plate{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.h-pn{display:inline-flex;align-items:center;gap:8px;background:var(--ink);color:var(--card);padding:4px 12px 3px;border-radius:3px;font-family:'Bebas Neue',sans-serif;font-size:26px;line-height:1.1}
.h-pn svg{margin-top:-2px}
.h-ps{font-size:12.5px;font-weight:600;padding:3px 12px;border-radius:12px;border:1.5px solid var(--ink)}
.h-room[data-s=now] .h-ps{background:#d4a94f;border-color:#d4a94f}
.h-room[data-s=now] .h-pn{box-shadow:inset 0 -3px 0 #d4a94f}
.h-room[data-s=started] .h-ps{background:var(--ink);color:var(--card)}
.h-room[data-s=none] .h-ps,.h-room[data-s=empty] .h-ps{border-style:dashed;border-color:var(--grey);color:var(--mut)}
.h-room[data-s=none] .h-pn,.h-room[data-s=empty] .h-pn{background:transparent;color:var(--mut);box-shadow:inset 0 0 0 1.5px var(--grey)}
.h-hl{font-size:15px;line-height:1.5;max-width:380px}
.h-room[data-s=none] .h-hl,.h-room[data-s=empty] .h-hl{color:var(--mut)}
.h-fig{display:flex;flex-direction:column;gap:3px}
.h-fv{font-family:'Bebas Neue',sans-serif;font-size:32px;line-height:1}
.h-fl{font-size:12.5px;color:var(--mut)}
.h-beds{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.h-cap{display:flex;justify-content:space-between;gap:12px;font-size:12.5px;color:var(--mut);border-top:1.5px dashed var(--line);padding-top:10px;margin-top:auto}
.h-cap .js-capt{font-style:italic}.h-cap .js-capt.is-set{font-style:normal;color:var(--ink);font-weight:600}
.h-cap b{font-weight:600;white-space:nowrap}
.h-corr{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px 18px;background:repeating-linear-gradient(90deg,var(--line) 0 14px,transparent 14px 26px) 0 50%/100% 1.5px no-repeat}
.h-cl{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);background:var(--card);padding:0 8px}
.h-stn{display:flex;align-items:center;gap:12px;background:var(--ink);color:var(--card);border-radius:26px;padding:9px 20px}
.h-sk{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#E8D3A2}
.h-sv{font-family:'Bebas Neue',sans-serif;font-size:24px;line-height:1}
.h-bar{width:110px;height:9px;border-radius:5px;background:rgba(250,251,253,.25);overflow:hidden}.h-bar i{display:block;height:100%;background:#d4a94f}
@container lp (max-width:699px){
 .h-plan{grid-template-columns:1fr}
 .h-r1,.h-r3{border-right:0}
 .h-corr{order:-1;border-bottom:2.5px solid var(--ink);background:none;justify-content:center;padding:12px}
 .h-cl{display:none}
 .h-stn{flex-wrap:wrap;justify-content:center;border-radius:14px}
 .h-r1,.h-r2,.h-r3{border-top:0;border-bottom:2.5px solid var(--ink)}
 .h-r4{border-top:0}
 .h-door{display:none}
 .h-room{padding:18px 16px 14px}
}
'''

ABOUT = {'b': ('The ward plan, with more space', 'A ward seen from above. Each part of the work is a room off one corridor, with one small bed for each step. The nurses’ station counts the beds made up. Pick a small bed to read its step.', 'Pale slate and navy ink')}

def main():
    out = os.path.join(ROOT, 'out', 'landing', 'home')
    pages = build(out, 'home-v2', ['b'], {'b': THEME}, lambda k, st: (None, canvas(st), CSS, DATA[st]['chat'], 'bm-home'))
    rv = os.path.join(out, 'bed-management-home-v2.html')
    open(rv, 'w').write(review('Bed Management · home page, Sample B redrawn',
        'The ward plan you picked, redrawn with more room. The desktop page now runs past one screen so each part can breathe: bigger rooms, larger text, the list of what Tojo still has to do in two columns, and the three buttons in one row.',
        ABOUT, {'b': THEME}, pages))
    print('built', rv)
    if '--measure' in sys.argv: measure(out, 'home-v2')

if __name__ == '__main__':
    main()
