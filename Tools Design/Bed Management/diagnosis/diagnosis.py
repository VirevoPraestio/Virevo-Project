"""
Bed Management · Diagnosis page. Three samples, all drawn from the home page's ward plan.
Look: the night round. Pale blue-grey ground, deep navy ink, plan paper, door plates, the small bed mark.

  A  A bed's day, walked     one corridor with seven doors, one for each stop of a bed's day, and the time between them
  B  The morning count       one example ward of 20 beds, seen at 8 AM, 11 AM, 2 PM and 5 PM
  C  The station desk        five trays on the nurses' station (the stages), notes pinned above it (the evidence)

Run:  python3 diagnosis.py [--measure]  -> out/bed-management/diagnosis/
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from bm_common import (e, ico, ICONS, STAMP, bed_svg, bed_key, BED_CSS, masthead, emblem, standing, section, pending,  # noqa: E402
                       actions, tag, pt, theme, place_main)

PLACE = 'Diagnosis'
THEME = theme('#E1E7EF', '#FAFCFE', '#1A2B45', '#475672', '#B2BED0', '#E9EFF7', '#8B96AA',
              ['#D6DDE8', '#E1E7EF', '#D8DEE9', '#DDE2EC', '#D6DCE6'], '6px', '--acc:#2F5E9E')
STEP = {'done': 'Done', 'now': 'Now', 'later': 'Still to do', 'none': 'Not started', 'next': 'Next'}

DATA = {
 'filled': {
  'claim': 'Beds free up hours after new patients arrive',
  'deck': 'Two of five stages are done. Your numbers show the gap. Next, match each morning’s new patients to the beds free the night before.',
  'stages': [['Walk a bed’s day', 'done', 'Seven stops walked'], ['Count beds free each morning', 'done', 'One week counted'],
             ['Match arrivals to free beds', 'now', 'Needs admission times'], ['Price the wait', 'later', 'With your own figures'], ['Name the cause', 'later', 'In plain words']],
  'stops': [
   {'n': 1, 'name': 'Doctor says the patient can go', 'time': '10:30 AM', 'what': 'On the morning round. The patient is told, but nothing is written yet.', 'heard': 'We say yes in the morning. The papers come later.'},
   {'n': 2, 'name': 'Patient leaves the bed', 'time': '2:15 PM', 'what': 'After the bill, the medicines and the family are all ready.', 'heard': 'The family only comes after lunch.', 'pt': 3},
   {'n': 3, 'name': 'Bed marked free', 'time': '2:35 PM', 'what': 'The ward nurse updates the bed register by hand.', 'heard': 'We mark it when we get a minute.'},
   {'n': 4, 'name': 'Housekeeping called', 'time': '2:45 PM', 'what': 'A phone call to the housekeeping desk, once the register is updated.', 'heard': 'Sometimes nobody picks up.'},
   {'n': 5, 'name': 'Bed cleaned and ready', 'time': '3:30 PM', 'what': 'Cleaning takes about 30 minutes once the team arrives.', 'heard': 'We are one team for three floors.'},
   {'n': 6, 'name': 'Next patient called', 'time': '3:50 PM', 'what': 'The admissions desk hears the bed is ready and calls the patient up.', 'heard': 'We ring the ward to check first.'},
   {'n': 7, 'name': 'Next patient in bed', 'time': '4:40 PM', 'what': 'The patient waits in casualty or the lounge until then.', 'heard': 'Some have waited since the morning.'},
  ],
  'gaps': [['3 hours 45 minutes', 'red'], ['20 minutes', ''], ['10 minutes', ''], ['45 minutes', ''], ['20 minutes', ''], ['50 minutes', '']],
  'empty_bed': '75 minutes',
  'evidence': [
   {'label': 'Bed empty after the patient leaves', 'value': '75 minutes', 'src': 'yours', 'pt': 1},
   {'label': 'When most beds come free', 'value': 'After 2 PM', 'src': 'derived'},
   {'label': 'When most new patients arrive', 'value': 'By 11 AM', 'src': 'yours'},
   {'label': 'Discharges a day', 'value': '40 to 45', 'src': 'yours'},
   {'label': 'Beds in use most nights', 'value': '—', 'src': 'need', 'pt': 2},
  ],
  'story': [['What you told us', 'Patients wait for beds every morning, even though 40 to 45 people go home each day.'],
            ['What is really happening', 'Beds do come free, but mostly after 2 PM. The morning patients arrive before then.'],
            ['Why', 'Not named yet. Matching arrivals to free beds comes first.']],
  'ward': {
   '8 AM': {'use': 19, 'dirty': 0, 'ready': 1, 'wait': 1, 'line': 'One bed ready. One patient waiting.'},
   '11 AM': {'use': 18, 'dirty': 1, 'ready': 1, 'wait': 6, 'line': 'Six patients waiting, and only one bed ready.'},
   '2 PM': {'use': 14, 'dirty': 4, 'ready': 2, 'wait': 5, 'line': 'Beds are coming free, but four still wait to be cleaned.'},
   '5 PM': {'use': 16, 'dirty': 1, 'ready': 3, 'wait': 1, 'line': 'Most of the morning patients are finally in a bed.'},
  },
  'arrive': [1, 3, 4, 3, 1, 1, 0, 1, 0, 0], 'free': [0, 0, 0, 1, 1, 3, 4, 3, 1, 1],
  'pending': [
   {'text': 'Match each morning’s new patients to the beds free the night before.'},
   {'text': 'Find how many beds are in use most nights.', 'need': 'Needs your bed count at midnight', 'pt': 2},
   {'text': 'Time each step of an admission, from the doctor’s call to the patient in bed.', 'need': 'Needs times from your admissions desk', 'pt': 4},
   {'text': 'Check whether one team runs both discharges and admissions.'},
  ],
  'actions': {'go': {'detail': 'Match arrivals to free beds', 'say': 'Let’s match each morning’s new patients to the beds free the night before'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about our beds: '},
              'jump': {'tab': 'Solutions', 'detail': 'Three fixes are waiting', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['Here is where the diagnosis stands. You walked a bed’s day and counted the free beds for a week.',
                    'The gap is clear. Most beds come free after 2 PM, but most new patients arrive by 11 AM.'],
           'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
           'note': 'The gap is in the timing, not the number of beds.',
           'points': [{'n': 1, 'label': 'The 75 minutes of empty bed'}, {'n': 2, 'label': 'Beds in use most nights'},
                      {'n': 3, 'label': 'The wait before the patient leaves'}, {'n': 4, 'label': 'Admission times by step'}],
           'prompts': ['Let’s match arrivals to free beds', 'Why does the patient wait so long to leave?', 'Skip ahead to the fixes']},
 },
 'empty': {
  'claim': 'Nothing checked yet',
  'deck': 'Tojo starts by walking one bed’s day with you, from the patient leaving to the next patient in bed, before suggesting anything.',
  'stages': [['Walk a bed’s day', 'next', 'Seven stops'], ['Count beds free each morning', 'later', 'One week'], ['Match arrivals to free beds', 'later', 'Your admission times'],
             ['Price the wait', 'later', 'Your own figures'], ['Name the cause', 'later', 'Plain words']],
  'stops': [{'n': i + 1, 'name': n, 'time': '—', 'what': 'Walked with you, one question at a time.', 'heard': ''} for i, n in enumerate(
      ['Doctor says the patient can go', 'Patient leaves the bed', 'Bed marked free', 'Housekeeping called', 'Bed cleaned and ready', 'Next patient called', 'Next patient in bed'])],
  'gaps': [['—', '']] * 6, 'empty_bed': None,
  'evidence': [{'label': l, 'value': '—', 'src': 'need'} for l in ['Bed empty after the patient leaves', 'When most beds come free', 'When most new patients arrive', 'Discharges a day', 'Beds in use most nights']],
  'story': [['What you told us', 'Nothing yet.'], ['What is really happening', 'Found by walking a bed’s day.'], ['Why', 'Named once the evidence is in.']],
  'ward': None, 'arrive': None, 'free': None,
  'pending': [
   {'text': 'Walk one bed’s day, from the patient leaving to the next patient in.'},
   {'text': 'Count the beds free each morning for one week.', 'need': 'Needs your bed list for last week'},
   {'text': 'Find how many beds are in use most nights.'},
  ],
  'actions': {'go': {'detail': 'Walk a bed’s day with Tojo', 'say': 'Let’s walk a bed’s day'},
              'add': {'detail': 'Tell Tojo what you already know', 'say': 'Here is what I already know about our beds: '},
              'jump': {'tab': 'Solutions', 'detail': 'Fills in once the cause is named', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['This is your Diagnosis page. It fills in as we talk.',
                    'We start by walking one bed’s day, one stop at a time, before I suggest anything.'],
           'note': 'Look closely before fixing anything.', 'points': [],
           'prompts': ['Let’s walk a bed’s day', 'How long will this take?', 'I already know the cause']},
 },
}

def top(d, empty):
    return masthead('Bed Management', PLACE, emblem(ICONS[PLACE]), STAMP['empty' if empty else 'filled']) + standing(d['claim'], d['deck'], empty)

def tail(d):
    return pending(d['pending']) + actions(d['actions'])

def stages_strip(d):
    """The five stages as five doors off one short corridor, each with its small bed."""
    doors = ''.join('<li class="dg-stage s-%s"><span class="bmb s-%s">%s</span><span class="dg-sn">%d</span><b>%s</b><em>%s · %s</em></li>' % (
        s, 'later' if s == 'next' else s, bed_svg(30), i + 1, e(n), STEP[s], e(note)) for i, (n, s, note) in enumerate(d['stages']))
    done = sum(1 for _, s, _ in d['stages'] if s == 'done')
    return section('The five stages', '<ol class="dg-stages bm-paper">%s</ol>' % doors, 'dg-sec-stages', '%d of 5 done' % done)

def evidence(d, cls='dg-ev'):
    cards = ''.join('<li class="dg-card"%s><span class="dg-cl">%s</span><span class="dg-cv%s">%s</span>%s</li>' % (
        pt(c.get('pt')), e(c['label']), ' is-need' if c['src'] == 'need' else '', e(c['value']), tag(c['src'])) for c in d['evidence'])
    return section('The evidence so far', '<ul class="%s">%s</ul>' % (cls, cards), 'dg-sec-ev', 'Every figure says where it came from')

COMMON = BED_CSS + '''
.dg-stages{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));border:2.5px solid var(--ink);border-radius:4px}
.dg-stage{position:relative;display:flex;flex-direction:column;gap:6px;padding:16px 16px 16px;border-right:2px solid var(--ink)}
.dg-stage:last-child{border-right:0}
.dg-stage .bmb{align-self:flex-start}
.dg-sn{position:absolute;right:14px;top:12px;font-family:'Bebas Neue',sans-serif;font-size:28px;color:var(--line);line-height:1}
.dg-stage b{font-size:14px;font-weight:600;line-height:1.35}
.dg-stage em{font-style:normal;font-size:12.5px;color:var(--mut)}
.dg-stage.s-now{background:rgba(212,169,79,.14);box-shadow:inset 0 -4px 0 #d4a94f}
.dg-stage.s-next{box-shadow:inset 0 -4px 0 #d4a94f}
.dg-stage.s-later b,.dg-stage.s-next b{color:var(--mut)}
.dg-ev{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.dg-card{position:relative;display:flex;flex-direction:column;gap:6px;padding:18px 18px 16px;background:var(--card);border:2px solid var(--ink);border-radius:4px}
.dg-card::before{content:"";position:absolute;top:-7px;left:18px;width:12px;height:12px;border-radius:50%;background:#d4a94f;border:2px solid var(--ink)}
.dg-cl{font-size:13px;font-weight:600;line-height:1.35}
.dg-cv{font-family:'Bebas Neue',sans-serif;font-size:32px;line-height:1}
.dg-cv.is-need{color:var(--red)}
@container lp (max-width:699px){
 .dg-stages{grid-template-columns:1fr}
 .dg-stage{border-right:0;border-bottom:2px solid var(--ink);display:grid;grid-template-columns:34px 1fr;column-gap:12px;padding:12px 14px}
 .dg-stage:last-child{border-bottom:0}
 .dg-stage .bmb{grid-row:1/span 2}
 .dg-sn{top:10px}
 .dg-stage.s-now{box-shadow:inset 4px 0 0 #d4a94f}.dg-stage.s-next{box-shadow:inset 4px 0 0 #d4a94f}
 .dg-ev{grid-template-columns:1fr 1fr;gap:14px 10px}
 .dg-card{padding:16px 12px 12px}
 .dg-cv{font-size:28px}
}
'''

# ------------------------------------------------------------------------------------------
# A · A bed's day, walked
def canvas_a(d, empty):
    stops, gaps = d['stops'], d['gaps']
    doors = ''.join(
        '<button class="da-stop js-pick" type="button" data-grp="da" data-key="%d" aria-pressed="%s"%s><span class="da-num">%d</span>'
        '<span class="da-time">%s</span><span class="da-name">%s</span>%s<span class="da-door" aria-hidden="true"></span></button>' % (
            s['n'], 'true' if s['n'] == 2 and not empty else 'false', pt(s.get('pt')), s['n'], e(s['time']), e(s['name']),
            '<span class="da-gm %s">%s after stop %d</span>' % (gaps[s['n'] - 2][1], e(gaps[s['n'] - 2][0]), s['n'] - 1) if s['n'] > 1 and not empty else '') for s in stops)
    gl = ''.join('<span class="da-gap %s"><i>%s</i>%s</span>' % (c, e(g), '<b>Longest wait</b>' if c == 'red' else '') for g, c in gaps)
    bracket = ('<div class="da-brk"><span>Bed empty: <b>%s</b></span>%s</div>' % (e(d['empty_bed']), tag('yours'))) if d['empty_bed'] else ''
    dets = ''.join(
        '<div class="da-det" data-det="da:%d"%s><div class="da-dh"><span class="da-dn">Stop %d</span><b>%s</b><span>%s</span></div>'
        '<p class="da-what">%s</p>%s</div>' % (
            s['n'], '' if s['n'] == (1 if empty else 2) else ' hidden', s['n'], e(s['name']), e(s['time']), e(s['what']),
            '<p class="da-heard">“%s”<span>What people usually say</span></p>' % e(s['heard']) if s['heard'] else '') for s in stops)
    plan = ('<div class="da-plan bm-paper"><div class="da-row">%s</div><div class="da-corr"><span class="da-cl">Corridor · follow one bed from left to right</span><div class="da-gaps">%s</div>%s</div></div>'
            '<div class="da-dets">%s</div>') % (doors, gl, bracket, dets)
    walked = 'Seven stops, walked on a normal Tuesday' if not empty else 'Seven stops to walk with you'
    return top(d, empty) + section('A bed’s day', plan, 'da-sec', walked + '. Pick a door to see what happens there.') + stages_strip(d) + evidence(d) + tail(d)

CSS_A = '''
.da-plan{border:3px solid var(--ink);border-radius:4px;padding:0 0 18px}
.da-row{display:grid;grid-template-columns:repeat(7,minmax(0,1fr))}
.da-stop{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:4px;text-align:left;background:transparent;border:0;border-right:2px solid var(--ink);border-bottom:2.5px solid var(--ink);padding:14px 12px 22px;min-height:150px}
.da-stop:last-child{border-right:0}
.da-num{font-family:'Bebas Neue',sans-serif;font-size:30px;line-height:1;color:var(--acc)}
.da-time{font-size:12.5px;font-weight:600;color:var(--mut)}
.da-name{font-size:13.5px;font-weight:600;line-height:1.35}
.da-door{position:absolute;left:14px;bottom:-2.5px;width:40px;height:4px;background:var(--card)}
.da-gm{display:none}
.da-stop[aria-pressed=true]{background:rgba(212,169,79,.16);box-shadow:inset 0 4px 0 #d4a94f}
.da-corr{padding:14px 0 0}
.da-cl{display:block;font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);padding:0 14px 10px}
.da-gaps{display:grid;grid-template-columns:.5fr repeat(6,minmax(0,1fr)) .5fr;align-items:start}
.da-gaps::before{content:""}
.da-gap{display:flex;flex-direction:column;align-items:center;gap:2px;text-align:center;font-size:12.5px;font-weight:600;color:var(--ink);padding:0 4px}
.da-gap i{font-style:normal;padding:3px 8px;border-radius:12px;border:1.5px solid var(--line);background:var(--card)}
.da-gap.red i{border:2px solid var(--red);color:var(--red)}
.da-gap b{font-size:11px;color:var(--red)}
.da-brk{margin:14px calc(100%/14) 0 calc(100%/14 + 100%/7);width:calc(100%*3/7);display:flex;align-items:center;gap:10px;justify-content:center;border:2px solid var(--amber);border-top:0;border-radius:0 0 10px 10px;padding:8px 10px;font-size:13px;color:var(--amber)}
.da-brk b{font-size:14px}
.da-dets{margin-top:18px}
.da-det{display:grid;grid-template-columns:220px 1fr 1fr;gap:24px;align-items:start;padding:18px 20px;background:var(--card);border:2px solid var(--ink);border-radius:6px}
.da-det[hidden]{display:none}
.da-dh{display:flex;flex-direction:column;gap:2px}.da-dn{font-size:12px;font-weight:600;color:var(--acc)}.da-dh b{font-size:15px}.da-dh span{font-size:13px;color:var(--mut)}
.da-what{font-size:14.5px;line-height:1.5}
.da-heard{font-family:Caveat,cursive;font-weight:700;font-size:23px;line-height:1.15;color:var(--ink)}
.da-heard span{display:block;font-family:Poppins,sans-serif;font-weight:500;font-size:12px;color:var(--mut);margin-top:4px}
.bm-d-a[data-empty] .da-stop{border-style:dashed}
@container lp (max-width:699px){
 .da-plan{padding:0}
 .da-row{grid-template-columns:1fr}
 .da-stop{flex-direction:row;flex-wrap:wrap;align-items:baseline;column-gap:10px;min-height:0;border-right:0;border-bottom:2px solid var(--ink);padding:12px 14px}
 .da-name{flex-basis:100%}
 .da-door{display:none}
 .da-stop[aria-pressed=true]{box-shadow:inset 4px 0 0 #d4a94f}
 .da-corr{display:none}
 .da-gm{display:inline-block;flex-basis:100%;font-size:12px;font-weight:600;color:var(--mut)}.da-gm.red{color:var(--red)}
 .da-det{grid-template-columns:1fr;gap:10px;padding:16px}
}
'''

# ------------------------------------------------------------------------------------------
# B · The morning count
def ward_beds(w):
    kinds = ['use'] * w['use'] + ['dirty'] * w['dirty'] + ['ready'] * w['ready']
    return ['<span class="bmb db-%s">%s</span>' % (k, bed_svg(34)) for k in kinds]

def canvas_b(d, empty):
    if d['ward']:
        times = list(d['ward'])
        picks = ''.join('<button class="db-t js-pick" type="button" data-grp="db" data-key="%d" aria-pressed="%s">%s</button>' % (
            i, 'true' if t == '11 AM' else 'false', e(t)) for i, t in enumerate(times))
        def view(i, t, w):
            beds = ward_beds(w)
            return ('<div class="db-view" data-det="db:%d"%s><div class="db-ward bm-paper"><div class="db-bay">%s</div><div class="db-corr"><span>Corridor</span></div>'
                    '<div class="db-bay">%s</div><div class="db-stn"><span class="db-sk">Nurses’ station</span><span class="db-sv">%d</span><span class="db-sl">patients waiting for a bed</span></div></div>'
                    '<p class="db-line"><b>%s.</b> %s</p></div>') % (i, '' if t == '11 AM' else ' hidden', ''.join(beds[:10]), ''.join(beds[10:]), w['wait'], e(t), e(w['line']))
        views = ''.join(view(i, t, w) for i, (t, w) in enumerate(d['ward'].items()))
        key = ('<div class="db-key" aria-hidden="true"><span><i class="bmb db-use">%s</i>Patient in bed</span><span><i class="bmb db-dirty">%s</i>Empty, waiting to be cleaned</span>'
               '<span><i class="bmb db-ready">%s</i>Ready for a patient</span></div>') % (bed_svg(20), bed_svg(20), bed_svg(20))
        hours = ['8 AM', '9', '10', '11', '12 PM', '1', '2', '3', '4', '5 PM']
        mx = max(d['arrive'] + d['free'])
        bars = lambda xs, c: ''.join('<span class="db-b %s" style="height:%d%%" title="%d"></span>' % (c, 100 * x / mx if x else 3, x) for x in xs)
        clock = ('<div class="db-clock" aria-label="New patients arrive mostly 9 to 11 AM. Beds come free mostly 1 to 3 PM.">'
                 '<div class="db-lane"><span class="db-ll">New patients arriving</span><div class="db-bars">%s</div></div>'
                 '<div class="db-lane"><span class="db-ll">Beds coming free</span><div class="db-bars">%s</div></div>'
                 '<div class="db-lane db-hrs"><span class="db-ll"></span><div class="db-bars">%s</div></div></div>') % (
            bars(d['arrive'], 'arr'), bars(d['free'], 'fre'), ''.join('<span>%s</span>' % h for h in hours))
        body = ('<div class="db-top"><div class="db-ts" role="group" aria-label="Time of day">%s</div>%s</div>%s%s'
                '<div class="db-sub"><h4>Across the day</h4>%s%s</div>') % (picks, tag('derived'), views, key, clock, '')
        sub = 'One example ward of 20 beds, worked out from your week of counts. Pick a time.'
    else:
        empty_beds = ''.join('<span class="bmb s-empty">%s</span>' % bed_svg(34) for _ in range(10))
        body = ('<div class="db-ward bm-paper is-empty"><div class="db-bay">%s</div><div class="db-corr"><span>Corridor</span></div><div class="db-bay">%s</div>'
                '<div class="db-stn"><span class="db-sk">Nurses’ station</span><span class="db-sv">—</span><span class="db-sl">patients waiting for a bed</span></div></div>'
                '<p class="db-line">Fills in once you share one week of morning bed counts.</p>') % (empty_beds, empty_beds)
        sub = 'One ward, counted through the day'
    return top(d, empty) + section('The morning count', body, 'db-sec', sub) + stages_strip(d) + evidence(d) + tail(d)

CSS_B = '''
.db-top{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px;flex-wrap:wrap}
.db-ts{display:flex;border:1.5px solid var(--ink);border-radius:6px;overflow:hidden}
.db-t{min-height:44px;min-width:72px;padding:0 14px;border:0;border-right:1.5px solid var(--ink);background:var(--card);font-size:14px;font-weight:600}
.db-t:last-child{border-right:0}
.db-t[aria-pressed=true]{background:#d4a94f}
.db-view[hidden]{display:none}
.db-ward{display:grid;grid-template-columns:1fr 190px;grid-template-rows:auto auto auto;border:3px solid var(--ink);border-radius:4px}
.db-bay{grid-column:1;display:grid;grid-template-columns:repeat(10,minmax(0,1fr));justify-items:center;padding:16px 12px}
.db-bay:first-child{border-bottom:2px solid var(--ink)}
.db-bay:nth-child(3){border-top:2px solid var(--ink)}
.db-corr{grid-column:1;padding:10px 16px;font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);background:repeating-linear-gradient(90deg,var(--line) 0 14px,transparent 14px 26px) 0 50%/100% 1.5px no-repeat}
.db-corr span{background:var(--card);padding-right:8px}
.db-stn{grid-column:2;grid-row:1/span 3;border-left:3px solid var(--ink);background:var(--ink);color:var(--card);display:flex;flex-direction:column;justify-content:center;gap:4px;padding:18px}
.db-sk{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#E8D3A2}
.db-sv{font-family:'Bebas Neue',sans-serif;font-size:60px;line-height:.9}
.db-sl{font-size:13px;line-height:1.35}
.bmb.db-use svg .k{fill:var(--ink)}
.bmb.db-dirty svg .f{stroke:var(--amber);stroke-dasharray:4 3}.bmb.db-dirty svg .h{fill:var(--amber)}.bmb.db-dirty svg .p{stroke:var(--amber)}
.bmb.db-ready svg .f{stroke:var(--green);stroke-width:2.5}.bmb.db-ready svg .h{fill:var(--green)}.bmb.db-ready svg .k{fill:rgba(47,107,79,.14)}
.db-line{font-size:15px;line-height:1.5;margin-top:14px}
.db-key{display:flex;flex-wrap:wrap;gap:8px 24px;margin-top:12px;font-size:12.5px;color:var(--mut)}
.db-key span{display:inline-flex;align-items:center;gap:6px}.db-key i{font-style:normal}
.db-sub{margin-top:22px}
.db-sub h4{font-size:13.5px;font-weight:600;margin-bottom:10px}
.db-clock{display:flex;flex-direction:column;gap:8px;padding:16px 18px;background:var(--card);border:2px solid var(--ink);border-radius:6px}
.db-lane{display:grid;grid-template-columns:170px 1fr;align-items:end;gap:12px}
.db-ll{font-size:12.5px;font-weight:600;padding-bottom:2px}
.db-bars{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:6px;height:44px;align-items:end}
.db-hrs .db-bars{height:auto;font-size:12px;color:var(--mut);text-align:center}
.db-b{display:block;border-radius:3px 3px 0 0}
.db-b.arr{background:var(--acc)}.db-b.fre{background:var(--ink)}
.db-ward.is-empty{border-style:dashed}
@container lp (max-width:699px){
 .db-ward{grid-template-columns:1fr}
 .db-stn{grid-column:1;grid-row:auto;border-left:0;flex-direction:row;align-items:center;flex-wrap:wrap;gap:4px 12px;padding:12px 16px;order:-1}
 .db-sv{font-size:40px}.db-sk{flex-basis:100%}
 .db-bay{grid-template-columns:repeat(5,minmax(0,1fr));row-gap:8px;padding:12px 8px}
 .db-t{min-width:0;flex:1 1 0;padding:0 8px}
 .db-ts{width:100%}
 .db-lane{grid-template-columns:1fr;gap:4px}
 .db-hrs .db-bars{font-size:10.5px;white-space:nowrap;gap:2px}
 .db-clock{padding:14px 12px}
}
'''

# ------------------------------------------------------------------------------------------
# C · The station desk
def canvas_c(d, empty):
    trays = ''.join(
        '<button class="dc-tray js-pick s-%s" type="button" data-grp="dc" data-key="%d" aria-pressed="%s"><span class="dc-paper" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span class="dc-tn">Stage %d</span><b>%s</b><em>%s</em></button>' % (
            s, i, 'true' if s in ('now', 'next') else 'false', i + 1, e(n), STEP[s]) for i, (n, s, note) in enumerate(d['stages']))
    stage_dets = ''.join('<p class="dc-td" data-det="dc:%d"%s><b>%s.</b> %s · %s</p>' % (
        i, '' if s in ('now', 'next') else ' hidden', e(n), STEP[s], e(note)) for i, (n, s, note) in enumerate(d['stages']))
    notes = ''.join('<li class="dc-note"%s><span class="dc-pin" aria-hidden="true"></span><span class="dg-cl">%s</span><span class="dg-cv%s">%s</span>%s</li>' % (
        pt(c.get('pt')), e(c['label']), ' is-need' if c['src'] == 'need' else '', e(c['value']), tag(c['src'])) for c in d['evidence'])
    story = ''.join('<div class="dc-st"><h4>%s</h4><p>%s</p></div>' % (e(h), e(t)) for h, t in d['story'])
    board = '<div class="dc-board"><div class="dc-bh">Notice board</div><ul class="dc-notes">%s</ul></div>' % notes
    desk = ('<div class="dc-desk"><div class="dc-dh"><span>Nurses’ station</span><span>%d of 5 stages done</span></div><div class="dc-trays">%s</div>%s</div>') % (
        sum(1 for _, s, _ in d['stages'] if s == 'done'), trays, stage_dets)
    return (top(d, empty) + section('At the nurses’ station', board + desk, 'dc-sec', 'The evidence pinned up, the five stages in trays on the desk. Pick a tray.')
            + section('The story so far', '<div class="dc-story">%s</div>' % story, 'dc-sec2') + tail(d))

CSS_C = '''
.dc-board{border:3px solid var(--ink);border-radius:6px;padding:0 20px 22px;background:#EEF1F5;background-image:radial-gradient(rgba(26,43,69,.09) 1px,transparent 1.2px);background-size:9px 9px}
.dc-bh{display:inline-block;background:var(--ink);color:var(--card);font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;padding:5px 12px;border-radius:0 0 4px 4px;margin-bottom:22px}
.dc-notes{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px}
.dc-note{position:relative;display:flex;flex-direction:column;gap:6px;background:var(--card);border:1.5px solid var(--ink);padding:18px 14px 14px;box-shadow:3px 4px 0 rgba(26,43,69,.12)}
.dc-note .bm-tag{white-space:normal}
.dc-note:nth-child(odd){transform:rotate(-1.2deg)}.dc-note:nth-child(even){transform:rotate(1deg)}
.dc-pin{position:absolute;top:-8px;left:50%;margin-left:-8px;width:16px;height:16px;border-radius:50%;background:#d4a94f;border:2px solid var(--ink)}
.dc-desk{margin:-6px 18px 0;background:var(--ink);border-radius:0 0 28px 28px;padding:18px 20px 20px;color:var(--card)}
.dc-dh{display:flex;justify-content:space-between;font-size:11.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#E8D3A2;margin-bottom:14px}
.dc-trays{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
.dc-tray{display:flex;flex-direction:column;align-items:flex-start;gap:4px;text-align:left;background:rgba(250,252,254,.07);border:1.5px solid rgba(250,252,254,.35);border-radius:6px;padding:12px;color:var(--card);min-height:120px}
.dc-paper{display:flex;flex-direction:column;gap:3px;width:44px;height:30px;border:1.5px solid rgba(250,252,254,.6);border-radius:3px;padding:4px;margin-bottom:6px}
.dc-paper i{display:block;height:2px;background:rgba(250,252,254,.7)}
.dc-tray.s-done .dc-paper{background:var(--card)}.dc-tray.s-done .dc-paper i{background:var(--ink)}
.dc-tray.s-now .dc-paper,.dc-tray.s-next .dc-paper{background:#d4a94f;border-color:#d4a94f}.dc-tray.s-now .dc-paper i{background:var(--ink)}
.dc-tray.s-later .dc-paper{border-style:dashed}.dc-tray.s-later .dc-paper i{display:none}
.dc-tn{font-size:11px;color:#C9D2E0}
.dc-tray b{font-size:13.5px;font-weight:600;line-height:1.35}
.dc-tray em{font-style:normal;font-size:12px;color:#C9D2E0}
.dc-tray[aria-pressed=true]{border-color:#d4a94f;box-shadow:inset 0 0 0 1.5px #d4a94f}
.dc-td{margin-top:14px;font-size:14px;line-height:1.5;color:#E6EBF2}
.dc-td[hidden]{display:none}
.dc-story{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border-top:2px solid var(--ink)}
.dc-st{padding:16px 20px 4px 0}
.dc-st+.dc-st{padding-left:20px;border-left:1.5px dashed var(--line)}
.dc-st h4{font-size:13px;font-weight:600;color:var(--acc);margin-bottom:6px}
.dc-st p{font-size:14.5px;line-height:1.55}
@container lp (max-width:699px){
 .dc-board{padding:0 12px 18px}
 .dc-notes{grid-template-columns:1fr 1fr;gap:18px 10px}
 .dc-desk{margin:-6px 6px 0;padding:16px 12px}
 .dc-trays{grid-template-columns:1fr 1fr;gap:10px}
 .dc-tray{min-height:0}
 .dc-story{grid-template-columns:1fr}
 .dc-st,.dc-st+.dc-st{padding:14px 0;border-left:0;border-bottom:1.5px dashed var(--line)}
}
'''

SAMPLES = {'a': (canvas_a, CSS_A), 'b': (canvas_b, CSS_B), 'c': (canvas_c, CSS_C)}
ABOUT = {
 'a': ('A bed’s day, walked', 'One corridor with seven doors, one for each stop of a bed’s day, with the time between each stop on the corridor floor. The longest wait is marked, and the 75 minutes of empty bed is bracketed. Pick a door to read what happens there. The five stages and the evidence sit below.', 'The night round: pale blue-grey, deep navy, plan paper'),
 'b': ('The morning count', 'One example ward of 20 beds seen from above, with the nurses’ station counting patients waiting. Switch between 8 AM, 11 AM, 2 PM and 5 PM to watch beds free up too late. A day strip compares when patients arrive with when beds come free.', 'The night round: pale blue-grey, deep navy, plan paper'),
 'c': ('The station desk', 'The nurses’ station seen from above. The evidence is pinned on the notice board, the five stages sit as trays on the desk, and the story so far is written underneath. Pick a tray to read that stage.', 'The night round: pale blue-grey, deep navy, plan paper'),
}

if __name__ == '__main__':
    place_main(PLACE, 'dg', DATA, SAMPLES, COMMON, {k: THEME for k in SAMPLES}, ABOUT,
               'Three ways to draw the Diagnosis page for Bed Management, each taken from the ward plan on the home page: plan paper, door plates, the corridor and the small bed. All three share one look for Diagnosis, the night round, and keep the same zones and three buttons.',
               'Each page may run to about two screens on desktop, so every part has room.')
