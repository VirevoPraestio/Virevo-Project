"""
Bed Management · Automations page. Three samples, drawn from the home page's ward plan.
Look: the night shift. Pale lilac-grey ground, deep ink-violet, plan paper, violet means switched on.

  A  Bed-head lights      each automation is the light on a bed-head panel, wired back to the nurses' station
  B  The ward at night    the automations placed on the ward's clock, from 6 PM to 6 PM the next day
  C  The station panel    the nurses' station status panel: one row of four lamps for each automation

Run:  python3 automations.py [--measure]  -> out/bed-management/automations/
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from bm_common import (e, ico, ICONS, STAMP, bed_svg, BED_CSS, masthead, emblem, standing, section, pending,  # noqa: E402
                       actions, tag, pt, theme, place_main)

PLACE = 'Automations'
THEME = theme('#E5E4EC', '#FBFBFD', '#25233A', '#54526A', '#BFBCD1', '#EEEDF5', '#93919F',
              ['#DAD9E3', '#E0DFE8', '#D8D7E2', '#DEDDE7', '#D9D8E2'], '12px', '--acc:#4B3FA0;--accl:#C9C2F5')
STAGES = ['Idea', 'Built', 'Testing', 'Switched on']

DATA = {
 'filled': {
  'claim': 'Three ideas wait on one thing: the bed list',
  'deck': 'Nothing is built yet. Each idea can be switched on once the one bed list is agreed in Solutions.',
  'main': {'name': 'The one bed list is agreed', 'state': 'Waiting · being shaped in Solutions'},
  'autos': [
   {'n': 1, 'name': 'Bed marked free when the patient leaves', 'stage': 0, 'pt': 1, 'hour': None,
    'when': 'Each time a patient leaves, any hour', 'from': 'The ward’s discharge record', 'to': 'The bed list',
    'what': 'The moment the discharge is closed, the bed shows as free on the list. Nobody has to update the register by hand.',
    'needs': ['A record of the time each patient leaves', 'The bed list on a screen', 'Your IT team to link the two']},
   {'n': 2, 'name': 'Housekeeping told on their phone', 'stage': 0, 'pt': None, 'hour': None,
    'when': 'Within 2 minutes of a bed going free', 'from': 'The bed list', 'to': 'Housekeeping staff phones',
    'what': 'The nearest housekeeping team gets a message with the ward and bed number.',
    'needs': ['Housekeeping staff carry phones on shift', 'A list of who is on duty', 'Bed marked free switched on first']},
   {'n': 3, 'name': 'Tomorrow’s free beds listed tonight', 'stage': 0, 'pt': 3, 'hour': 21,
    'when': 'Every night at 9 PM', 'from': 'The evening ward round notes', 'to': 'The admissions desk',
    'what': 'At 9 PM the admissions desk gets a list of beds likely to free up tomorrow, ward by ward.',
    'needs': ['Doctors mark likely discharges on the evening round', 'The bed list on a screen', 'An agreed time for the list']},
  ],
  'pending': [
   {'text': 'Find which system records when a patient leaves.', 'need': 'Needs a name from your IT team', 'pt': 2},
   {'text': 'Check whether housekeeping staff carry phones on shift.', 'need': 'Needs an answer from you'},
   {'text': 'Draw how the bed list updates itself.'},
   {'text': 'Work out what each automation costs to build.'},
  ],
  'actions': {'go': {'detail': 'Find where the leaving time is kept', 'say': 'Let’s find which system records when a patient leaves'},
              'add': {'detail': 'Tell Tojo about your systems', 'say': 'Here is what I know about our systems: '},
              'jump': {'tab': 'Processes', 'detail': 'Three changes are waiting', 'say': 'Take me to Processes'}},
  'chat': {'text': ['Here is where the automations stand. There are three ideas, and none is built yet.',
                    'All three hang off the one bed list. Once that is agreed, the first to build is the bed marked free when the patient leaves.'],
           'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
           'note': 'Build the bed list first. Everything else hangs off it.',
           'points': [{'n': 1, 'label': 'Bed marked free on its own'}, {'n': 2, 'label': 'Which system records leaving'},
                      {'n': 3, 'label': 'The 9 PM list for admissions'}],
           'prompts': ['Which should we build first?', 'What does the bed list need from IT?', 'Show me the 9 PM list']},
 },
 'empty': {
  'claim': 'Nothing to switch on yet',
  'deck': 'Automations are drawn once a fix is agreed. Each one does a job no one should have to do by hand.',
  'main': {'name': 'A fix is agreed in Solutions', 'state': 'Waiting'},
  'autos': [],
  'pending': [
   {'text': 'Wait for the first fix to be agreed.'},
   {'text': 'Find out which systems your wards already use.', 'need': 'Needs a list from your IT team'},
   {'text': 'Draw the first automation with you.'},
  ],
  'actions': {'go': {'detail': 'See the fixes first', 'say': 'Take me to the fixes'},
              'add': {'detail': 'Tell Tojo about your systems', 'say': 'Here is what I know about our systems: '},
              'jump': {'tab': 'Processes', 'detail': 'Fills in once a fix is agreed', 'say': 'Take me to Processes'}},
  'chat': {'text': ['This is your Automations page. It fills in once a fix is agreed.',
                    'Meanwhile, it helps to know which systems your wards and admissions desk use.'],
           'note': 'Fix it first. Then make it run on its own.', 'points': [],
           'prompts': ['Take me to the fixes', 'What systems should I list?', 'How does this work?']},
 },
}

def top(d, empty):
    return masthead('Bed Management', PLACE, emblem(ICONS[PLACE]), STAMP['empty' if empty else 'filled']) + standing(d['claim'], d['deck'], empty)

def tail(d):
    return pending(d['pending']) + actions(d['actions'])

def lamp_state(a):
    return ['idea', 'built', 'testing', 'on'][a['stage']]

def lamps(a, cls='au-lamps'):
    return '<span class="%s" aria-label="%s">%s</span>' % (cls, 'Now at: ' + STAGES[a['stage']], ''.join(
        '<span class="l %s"><i aria-hidden="true"></i><em>%s</em></span>' % ('lit' if i <= a['stage'] else '', e(n)) for i, n in enumerate(STAGES)))

def detail(a, hidden, grp):
    return ('<div class="au-det" data-det="%s:%d"%s><div class="au-dh"><span class="au-n">Automation %d</span><b>%s</b>%s</div>'
            '<p class="au-what">%s</p><dl class="au-dl"><div><dt>When it runs</dt><dd>%s</dd></div><div><dt>Takes from</dt><dd>%s</dd></div><div><dt>Gives to</dt><dd>%s</dd></div></dl>'
            '<details class="bm-more"><summary>See what it needs</summary><ul>%s</ul></details></div>') % (
        grp, a['n'], ' hidden' if hidden else '', a['n'], e(a['name']), lamps(a), e(a['what']), e(a['when']), e(a['from']), e(a['to']),
        ''.join('<li>%s</li>' % e(x) for x in a['needs']))

def main_switch(d, cls=''):
    return ('<div class="au-main %s"><span class="au-lever" aria-hidden="true"><i></i></span><span><span class="au-mk">Main switch · everything waits on it</span>'
            '<b>%s</b><em>%s</em></span></div>') % (cls, e(d['main']['name']), e(d['main']['state']))

COMMON = BED_CSS + '''
.au-lamps{display:inline-flex;gap:12px;flex-wrap:wrap}
.au-lamps .l{display:inline-flex;align-items:center;gap:5px;font-size:11.5px;color:var(--mut)}
.au-lamps .l em{font-style:normal}
.au-lamps i{width:13px;height:13px;border-radius:50%;border:2px dashed var(--grey)}
.au-lamps .l.lit i{border:2px solid var(--ink);background:var(--card)}
.au-lamps .l.lit:last-child i{background:var(--acc);border-color:var(--acc);box-shadow:0 0 0 4px rgba(75,63,160,.2)}
.au-det{padding:22px;background:var(--card);border:2px solid var(--ink);border-radius:var(--btnr);display:flex;flex-direction:column;gap:14px}
.au-det[hidden]{display:none}
.au-dh{display:flex;flex-wrap:wrap;align-items:center;gap:6px 16px}
.au-n{font-size:12px;font-weight:600;color:var(--acc);flex-basis:100%}
.au-dh b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:30px;line-height:1}
.au-what{font-size:14.5px;line-height:1.55;max-width:640px}
.au-dl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:0}
.au-dl div{border-top:1.5px dashed var(--line);padding-top:8px}
.au-dl dt{font-size:12px;font-weight:600;color:var(--mut)}.au-dl dd{margin:2px 0 0;font-size:14px;line-height:1.45}
.au-main{display:flex;align-items:center;gap:16px;padding:16px 20px;background:var(--ink);color:var(--card);border-radius:var(--btnr)}
.au-mk{display:block;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#E8D3A2}
.au-main b{display:block;font-size:16px;font-weight:600;margin-top:2px}
.au-main em{display:block;font-style:normal;font-size:13px;color:var(--accl)}
.au-lever{position:relative;flex-shrink:0;width:30px;height:54px;border-radius:15px;border:2px solid var(--accl);background:rgba(255,255,255,.05)}
.au-lever i{position:absolute;left:3px;bottom:3px;width:20px;height:20px;border-radius:50%;background:var(--grey)}
.au-empty{border:2px dashed var(--grey);border-radius:var(--btnr);padding:26px 22px;font-size:14.5px;color:var(--mut)}
@container lp (max-width:699px){
 .au-det{padding:16px}
 .au-dl{grid-template-columns:1fr;gap:10px}
}
'''

# ------------------------------------------------------------------------------------------
# A · Bed-head lights
def canvas_a(d, empty):
    if not d['autos']:
        beds = ''.join('<div class="aa-bay is-empty"><span class="aa-head"><span class="aa-lamp s-idea"></span><span class="aa-hn">An automation goes here</span></span><span class="bmb s-empty">%s</span></div>' % bed_svg(64) for _ in range(3))
        body = '<div class="aa-ward bm-paper"><div class="aa-bus"></div><div class="aa-bays">%s</div>%s</div>' % (beds, main_switch(d, 'aa-stn'))
        return top(d, empty) + section('Bed-head lights', body, 'aa-sec', 'Fills in once a fix is agreed') + tail(d)
    beds = ''.join(
        '<button class="aa-bay js-pick" type="button" data-grp="aa" data-key="%d" aria-pressed="%s"%s><span class="aa-head"><span class="aa-lamp s-%s" aria-hidden="true"></span>'
        '<span class="aa-hn">%s</span><span class="aa-hs">%s</span></span><span class="bmb s-later">%s</span><span class="aa-when">%s</span></button>' % (
            a['n'], 'true' if a['n'] == 1 else 'false', pt(a.get('pt')), lamp_state(a), e(a['name']), STAGES[a['stage']], bed_svg(64), e(a['when'])) for a in d['autos'])
    key = ('<div class="aa-key" aria-hidden="true"><span><i class="aa-lamp s-idea"></i>Idea</span><span><i class="aa-lamp s-built"></i>Built</span>'
           '<span><i class="aa-lamp s-testing"></i>Testing</span><span><i class="aa-lamp s-on"></i>Switched on</span></div>')
    body = ('<div class="aa-ward bm-paper"><div class="aa-bus"><span>One wire back to the nurses’ station</span></div><div class="aa-bays">%s</div>%s</div>%s<div class="aa-dets">%s</div>') % (
        beds, main_switch(d, 'aa-stn'), key, ''.join(detail(a, a['n'] != 1, 'aa') for a in d['autos']))
    return top(d, empty) + section('Bed-head lights', body, 'aa-sec', 'Each automation is the light over a bed, wired to the station. Pick a light.') + tail(d)

CSS_A = '''
.aa-ward{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 230px;grid-template-rows:auto 1fr;border:3px solid var(--ink);border-radius:6px;padding:0 0 0 0}
.aa-bus{grid-column:1/-1;height:46px;border-bottom:2.5px solid var(--ink);display:flex;align-items:center;padding:0 20px;position:relative}
.aa-bus::after{content:"";position:absolute;left:20px;right:115px;bottom:12px;height:0;border-top:2px solid var(--acc)}
.aa-bus span{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);background:var(--card);padding:0 8px;position:relative;z-index:1;margin-top:-12px}
.aa-bays{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.aa-bay{position:relative;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center;background:transparent;border:0;border-right:2px dashed var(--line);padding:0 14px 22px}
.aa-bay:last-child{border-right:2.5px solid var(--ink)}
.aa-bay::before{content:"";position:absolute;top:-12px;left:50%;height:12px;border-left:2px solid var(--acc)}
.aa-head{display:flex;flex-direction:column;align-items:center;gap:6px;width:100%;padding:12px 10px;margin-top:0;background:var(--soft);border:2px solid var(--ink);border-top:0;border-radius:0 0 10px 10px}
.aa-hn{font-size:14px;font-weight:600;line-height:1.35}
.aa-hs{font-size:12px;color:var(--mut)}
.aa-when{font-size:12.5px;color:var(--mut);line-height:1.4}
.aa-lamp{display:inline-block;width:22px;height:22px;border-radius:50%;border:2.5px dashed var(--grey);background:transparent}
.aa-lamp.s-built{border:2.5px solid var(--ink)}
.aa-lamp.s-testing{border:2.5px solid var(--amber);background:rgba(138,86,8,.18)}
.aa-lamp.s-on{border:2.5px solid var(--acc);background:var(--acc);box-shadow:0 0 0 6px rgba(75,63,160,.18)}
.aa-bay[aria-pressed=true] .aa-head{box-shadow:0 0 0 3px #d4a94f}
.aa-bay[aria-pressed=true]::after{content:"";position:absolute;bottom:0;left:30%;right:30%;height:4px;background:#d4a94f;border-radius:2px}
.aa-stn{grid-column:2;grid-row:2;border-radius:0;flex-direction:column;align-items:flex-start;justify-content:center}
.aa-bay.is-empty{color:var(--mut)}.aa-bay.is-empty .aa-head{border-style:dashed;background:transparent}
.aa-key{display:flex;flex-wrap:wrap;gap:8px 22px;margin:14px 0 18px;font-size:12.5px;color:var(--mut)}
.aa-key span{display:inline-flex;align-items:center;gap:8px}.aa-key i{width:14px;height:14px}
@container lp (max-width:699px){
 .aa-ward{grid-template-columns:1fr}
 .aa-bus{display:none}
 .aa-stn{grid-column:1;grid-row:1}
 .aa-bays{grid-template-columns:1fr}
 .aa-bay{flex-direction:row;align-items:center;text-align:left;border-right:0;border-bottom:2px dashed var(--line);padding:14px;gap:12px;flex-wrap:wrap}
 .aa-bay:last-child{border-right:0;border-bottom:0}
 .aa-bay::before{display:none}
 .aa-head{flex:1 1 0;align-items:flex-start;border:2px solid var(--ink);border-radius:10px;order:2}
 .aa-bay .bmb svg{width:44px;height:59px}
 .aa-when{flex-basis:100%;order:3}
 .aa-bay[aria-pressed=true]::after{display:none}
}
'''

# ------------------------------------------------------------------------------------------
# B · The ward at night (6 PM to 6 PM next day)
def canvas_b(d, empty):
    hours = ['6 PM', '9 PM', '12 AM', '3 AM', '6 AM', '9 AM', '12 PM', '3 PM', '6 PM']
    ticks = ''.join('<span style="left:%.3f%%">%s</span>' % (i * 12.5, h) for i, h in enumerate(hours))
    if not d['autos']:
        strip = '<div class="ab-clock bm-paper is-empty"><div class="ab-night" style="left:8.33%;width:50%"></div><div class="ab-ticks">' + ticks + '</div></div>'
        return top(d, empty) + section('The ward at night', main_switch(d) + strip + '<p class="au-empty">Each automation will sit here at the hour it runs.</p>', 'ab-sec', 'From 6 PM to 6 PM the next day') + tail(d)
    pos = lambda h: ((h - 18) % 24) / 24 * 100
    marks = ''.join('<button class="ab-mk js-pick" type="button" data-grp="ab" data-key="%d" aria-pressed="false" style="left:%.2f%%"%s><span class="ab-dot s-%s">%d</span><span class="ab-ml">%s</span></button>' % (
        a['n'], pos(a['hour']), pt(a.get('pt')), lamp_state(a), a['n'], e(a['when'])) for a in d['autos'] if a['hour'] is not None)
    events = [a for a in d['autos'] if a['hour'] is None]
    band = ('<div class="ab-band" style="left:%.2f%%;width:%.2f%%"><span>Most patients leave between 12 and 4 PM</span></div>' % (pos(12), pos(16) - pos(12)))
    ev = ''.join('<button class="ab-ev js-pick" type="button" data-grp="ab" data-key="%d" aria-pressed="%s"%s><span class="ab-dot s-%s">%d</span><span>%s</span></button>' % (
        a['n'], 'true' if a['n'] == 1 else 'false', pt(a.get('pt')), lamp_state(a), a['n'], e(a['name'])) for a in events)
    clock = ('<div class="ab-clock bm-paper"><div class="ab-night" style="left:%.2f%%;width:50%%"><span>Night shift</span></div>%s'
             '<div class="ab-lane ab-lane1"><span class="ab-ln">Runs at a set time</span>%s</div>'
             '<div class="ab-lane ab-lane2"><span class="ab-ln">Patients leaving</span>%s</div>'
             '<div class="ab-ticks">%s</div></div><div class="ab-evrow"><span class="ab-evh">Runs each time a patient leaves, whatever the hour</span><div class="ab-evs">%s</div></div>') % (pos(20), '', marks, band, ticks, ev)
    list_ = ''.join(detail(a, a['n'] != 1, 'ab') for a in d['autos'])
    return (top(d, empty) + section('The ward at night', main_switch(d) + clock + '<div class="ab-dets">%s</div>' % list_, 'ab-sec',
            'Each automation at the hour it runs, from 6 PM to 6 PM the next day. Pick one.') + tail(d))

CSS_B = '''
.ab-sec .au-main{margin-bottom:18px}
.ab-clock{position:relative;border:3px solid var(--ink);border-radius:6px;padding:16px 0 40px;overflow:hidden}
.ab-night{position:absolute;top:0;bottom:30px;background:rgba(37,35,58,.9)}
.ab-night span{position:absolute;right:10px;bottom:8px;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#E8D3A2}
.ab-lane{position:relative;height:96px;margin:0 0 6px;border-top:1.5px dashed var(--line)}
.ab-ln{position:absolute;left:12px;top:6px;font-size:11.5px;font-weight:600;color:var(--mut);background:var(--card);padding:1px 6px;border-radius:3px;z-index:1}
.ab-mk{position:absolute;top:28px;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:6px;background:none;border:0;padding:4px;border-radius:8px;min-width:44px}
.ab-ml{font-size:12px;font-weight:600;color:var(--card);white-space:nowrap;background:var(--ink);padding:2px 8px;border-radius:10px}
.ab-dot{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;font-weight:700;font-size:14px;border:2.5px dashed var(--grey);background:var(--card);color:var(--ink);flex-shrink:0}
.ab-dot.s-on{background:var(--acc);border:2.5px solid var(--acc);color:#fff}
.ab-band{position:absolute;top:30px;height:52px;background:repeating-linear-gradient(135deg,rgba(75,63,160,.12) 0 6px,transparent 6px 12px);border:1.5px solid var(--acc);border-radius:6px}
.ab-band span{position:absolute;left:8px;top:-22px;font-size:11.5px;color:var(--acc);font-weight:600;white-space:nowrap;transform:translateX(-40%)}
.ab-evrow{margin-top:14px;display:flex;flex-direction:column;gap:10px}.ab-evh{font-size:13px;font-weight:600}
.ab-evs{display:flex;flex-wrap:wrap;gap:10px}
.ab-ev{display:flex;align-items:center;gap:10px;min-height:44px;background:var(--card);border:1.5px solid var(--ink);border-radius:24px;padding:4px 16px 4px 4px;font-size:13px;font-weight:600;text-align:left}
.ab-lane2{height:90px}
.ab-ev[aria-pressed=true],.ab-mk[aria-pressed=true] .ab-dot{box-shadow:0 0 0 3px #d4a94f}
.ab-ticks{position:absolute;left:0;right:0;bottom:0;height:30px;border-top:2.5px solid var(--ink);background:var(--card)}
.ab-ticks span{position:absolute;top:6px;transform:translateX(-50%);font-size:11.5px;font-weight:600;color:var(--mut);white-space:nowrap}
.ab-ticks span:first-child{transform:none;padding-left:6px}.ab-ticks span:last-child{transform:translateX(-100%);padding-right:6px}
.ab-dets{margin-top:18px}
.ab-clock.is-empty{border-style:dashed;height:120px}
@container lp (max-width:699px){
 .ab-band span{display:none}
 .ab-ticks span:nth-child(even){display:none}
 .ab-ml{font-size:11px}
 .ab-mk{transform:none;margin-left:-21px;align-items:flex-start}
 .ab-lane1{height:120px}
 .ab-lane2{height:90px}
 .ab-ev{font-size:12.5px}
}
'''

# ------------------------------------------------------------------------------------------
# C · The station panel
def canvas_c(d, empty):
    head = '<div class="ac-row ac-hd"><span>Automation</span>%s<span></span></div>' % ''.join('<span class="ac-sh">%s</span>' % e(s) for s in STAGES)
    if not d['autos']:
        rows = ''.join('<div class="ac-row is-empty"><span class="ac-name">A new automation</span>%s<span></span></div>' % ''.join('<span class="ac-cell"><i></i></span>' for _ in STAGES) for _ in range(3))
    else:
        rows = ''.join(
            '<div class="ac-row"%s><button class="ac-name js-pick" type="button" data-grp="ac" data-key="%d" aria-pressed="%s"><span class="ac-no">%d</span><span><b>%s</b><em>%s</em></span></button>%s</div>' % (
                pt(a.get('pt')), a['n'], 'true' if a['n'] == 1 else 'false', a['n'], e(a['name']), e(a['when']),
                ''.join('<span class="ac-cell%s"><i aria-hidden="true"></i><span class="sr">%s: %s</span></span>' % (
                    ' lit' if i <= a['stage'] else '', e(s), 'yes' if i <= a['stage'] else 'not yet') for i, s in enumerate(STAGES))) for a in d['autos'])
    panel = ('<div class="ac-panel">%s<div class="ac-grid">%s%s</div><div class="ac-foot"><span>Nurses’ station · status panel</span><span>%s</span></div></div>') % (
        main_switch(d, 'ac-main'), head, rows, ('%d of %d switched on' % (sum(1 for a in d['autos'] if a['stage'] == 3), len(d['autos']))) if d['autos'] else 'Nothing built yet')
    dets = '<div class="ac-dets">%s</div>' % ''.join(detail(a, a['n'] != 1, 'ac') for a in d['autos']) if d['autos'] else ''
    return top(d, empty) + section('The station panel', panel + dets, 'ac-sec', 'One row for each automation. A lamp lights as it moves from idea to switched on. Pick a row.') + tail(d)

CSS_C = '''
.ac-panel{background:var(--ink);color:var(--card);border-radius:18px;padding:18px;box-shadow:inset 0 0 0 2px rgba(201,194,245,.25)}
.ac-main{background:rgba(255,255,255,.06);border:1.5px solid rgba(201,194,245,.35);margin-bottom:16px}
.ac-grid{display:flex;flex-direction:column}
.ac-row{display:grid;grid-template-columns:minmax(0,1.8fr) repeat(4,minmax(0,.55fr)) 0;align-items:center;border-top:1.5px solid rgba(201,194,245,.22)}
.ac-hd{border-top:0;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#E8D3A2;padding:6px 0}
.ac-sh{text-align:center}
.ac-name{display:flex;align-items:center;gap:12px;text-align:left;background:none;border:0;color:var(--card);padding:14px 10px 14px 4px;border-radius:10px;min-height:64px}
.ac-name b{display:block;font-size:14.5px;font-weight:600;line-height:1.35}
.ac-name em{display:block;font-style:normal;font-size:12.5px;color:var(--accl)}
.ac-no{flex-shrink:0;width:30px;height:30px;border-radius:50%;border:1.5px solid var(--accl);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700}
.ac-name[aria-pressed=true]{box-shadow:inset 0 0 0 2px #d4a94f}
.ac-cell{display:flex;justify-content:center}
.ac-cell i{width:24px;height:24px;border-radius:50%;border:2px dashed rgba(201,194,245,.45)}
.ac-cell.lit i{border:2px solid var(--accl);background:rgba(201,194,245,.25)}
.ac-cell.lit:nth-child(5) i{background:var(--accl);box-shadow:0 0 0 6px rgba(201,194,245,.2)}
.ac-row.is-empty .ac-name{color:var(--accl);font-style:italic;min-height:56px;align-items:center;display:flex}
.ac-foot{display:flex;justify-content:space-between;margin-top:12px;padding-top:12px;border-top:1.5px solid rgba(201,194,245,.22);font-size:12px;color:var(--accl)}
.ac-dets{margin-top:20px}
@container lp (max-width:699px){
 .ac-panel{padding:14px 12px;border-radius:14px}
 .ac-row{grid-template-columns:repeat(4,minmax(0,1fr));row-gap:4px;padding-bottom:12px}
 .ac-hd{display:none}
 .ac-name{grid-column:1/-1;min-height:0;padding:12px 4px 4px}
 .ac-cell{flex-direction:column;align-items:center}
 .ac-cell .sr{position:static;width:auto;height:auto;clip:auto;overflow:visible;font-size:10.5px;color:var(--accl);margin-top:4px;text-align:center}
}
'''

SAMPLES = {'a': (canvas_a, CSS_A), 'b': (canvas_b, CSS_B), 'c': (canvas_c, CSS_C)}
ABOUT = {
 'a': ('Bed-head lights', 'Each automation is the light on a bed-head panel. All three are wired back to the nurses’ station, where the main switch waits for the one bed list to be agreed. A light goes from dashed (idea) to solid (built), amber (testing) and violet (switched on). Pick a light to open what it does.', 'The night shift: pale lilac-grey, deep ink-violet, violet means switched on'),
 'b': ('The ward at night', 'The ward’s clock from 6 PM to 6 PM the next day, with the night shift shaded. Automations that run at a set time sit at their hour. Those that run when a patient leaves sit in their own lane, beside the hours when most patients leave. Pick one to open it.', 'The night shift: pale lilac-grey, deep ink-violet, violet means switched on'),
 'c': ('The station panel', 'The nurses’ station status panel, dark like a real one. The main switch sits at the top, then one row of four lamps for each automation: idea, built, testing, switched on. Pick a row to open what it does and what it needs.', 'The night shift: pale lilac-grey, deep ink-violet, violet means switched on'),
}

if __name__ == '__main__':
    place_main(PLACE, 'au', DATA, SAMPLES, COMMON, {k: THEME for k in SAMPLES}, ABOUT,
               'Three ways to draw the Automations page for Bed Management, each taken from the ward plan on the home page. All three share one look for Automations, the night shift, and keep the same zones and three buttons.',
               'Each page may run to about two screens on desktop, so every part has room.')
