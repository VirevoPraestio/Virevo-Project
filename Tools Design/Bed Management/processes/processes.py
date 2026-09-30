"""
Bed Management · Processes page. Three samples, drawn from the home page's ward plan.
Look: the day shift. Pale clay ground, deep brown ink, plan paper, pill buttons, magnets and seats.
Processes covers three things: process changes, the measures we watch, and team and role changes.

  A  The shift board     the ward's wall board: three columns of magnet strips, the trial strip across the foot
  B  The trial ward      one ward drawn from above, each change pinned where it happens, seats at the station
  C  Shift by shift      the ward's day, night shift and day shift, with each change and check at its hour

Run:  python3 processes.py [--measure]  -> out/bed-management/processes/
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from bm_common import (e, ico, ICONS, STAMP, bed_svg, BED_CSS, masthead, emblem, standing, section, pending,  # noqa: E402
                       actions, tag, pt, theme, place_main)

PLACE = 'Processes'
THEME = theme('#EDE6E3', '#FDFAF9', '#3A2522', '#69514D', '#D3BFBA', '#F5ECEA', '#A08E8A',
              ['#E3D9D5', '#E8DFDB', '#E1D7D3', '#E6DDD9', '#E2D8D4'], '22px', '--acc:#8C4B3F')

DATA = {
 'filled': {
  'claim': 'The changes are on paper. Nothing has been tried on a ward yet.',
  'deck': 'Three changes, three measures and one new role. A two-week trial on one ward comes first.',
  'changes': [
   {'n': 1, 'name': 'One bed owner on every shift', 'state': 'Agreed on paper', 'pt': 1, 'where': 'stn', 'at': [8, 20], 'span': True,
    'what': 'One named person on each shift keeps the bed list right and chases every empty bed.',
    'how': ['Named at the start of each shift, on the board', 'Checks the bed list every two hours', 'Calls housekeeping for each empty bed']},
   {'n': 2, 'name': 'Patients home by 11 AM on most days', 'state': 'New', 'where': 'bay', 'at': [11],
    'what': 'Patients who can go home leave before 11 AM, so their beds are ready for the morning’s new patients.',
    'how': ['Doctors mark tomorrow’s discharges on the evening round', 'Papers and medicines ready the night before', 'The family told the evening before']},
   {'n': 3, 'name': 'A 10-minute bed huddle at 8 AM', 'state': 'New', 'where': 'hk', 'at': [8],
    'what': 'The ward, housekeeping and admissions agree the day’s free beds in ten minutes.',
    'how': ['At the nurses’ station, standing, ten minutes', 'The ward, housekeeping and admissions all there', 'Agrees the day’s free beds and when each will be ready']},
  ],
  'measures': [
   {'name': 'Bed empty after the patient leaves', 'value': '75 minutes', 'kind': 'start', 'when': 'Every time a patient leaves', 'at': None},
   {'name': 'Beds free by 11 AM', 'value': '—', 'kind': 'need', 'pt': 2, 'when': 'Counted at 11 AM', 'at': 11},
   {'name': 'Patients waiting for a bed at noon', 'value': 'New', 'kind': 'new', 'when': 'Counted at 12 PM', 'at': 12},
  ],
  'roles': [
   {'name': 'Bed Manager', 'detail': 'One on each shift, day and night. To hire or name.', 'seats': [0, 0], 'pt': 4, 'shifts': ['day', 'night']},
   {'name': 'Housekeeping lead', 'detail': 'Already in post. One new duty: answers the bed call.', 'seats': [1], 'shifts': ['day']},
  ],
  'trial': {'name': 'Two-week trial on one ward', 'line': 'No new staff and no new system needed to start', 'state': 'Not started', 'weeks': 2},
  'pending': [
   {'text': 'Pick the trial ward with you.', 'need': 'Needs your choice of ward', 'pt': 3},
   {'text': 'Write the job outline for the Bed Manager.', 'pt': 4},
   {'text': 'Set a goal for each measure after the first trial week.'},
   {'text': 'Name who will record the times on the trial ward.', 'need': 'Needs a name from you'},
  ],
  'actions': {'go': {'detail': 'Pick the trial ward', 'say': 'Let’s pick the trial ward'},
              'add': {'detail': 'Add a change, a measure or a role', 'say': 'I want to add a change, a measure or a role: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Three stages still to finish', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Here is where the processes stand. The changes are agreed on paper, but nothing has been tried on a ward.',
                    'One measure already has a starting number. The other two start on the trial ward.'],
           'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
           'note': 'Try it on one ward before changing them all.',
           'points': [{'n': 1, 'label': 'The bed owner on every shift'}, {'n': 2, 'label': 'Beds free by 11 AM'},
                      {'n': 3, 'label': 'The trial ward'}, {'n': 4, 'label': 'The Bed Manager role'}],
           'prompts': ['Which ward should we start on?', 'Do we need to hire a Bed Manager?', 'What will the trial cost?']},
 },
 'empty': {
  'claim': 'Nothing changed yet',
  'deck': 'Process changes, the measures we watch and any new roles appear here once a fix is agreed. Each is tried on one ward first.',
  'changes': [], 'measures': [], 'roles': [],
  'trial': {'name': 'A trial on one ward', 'line': 'Planned once the changes are agreed', 'state': 'Not planned', 'weeks': 2},
  'pending': [
   {'text': 'Wait for the first fix to be agreed.'},
   {'text': 'List the teams that touch a bed: wards, housekeeping, admissions.', 'need': 'Needs your team list'},
   {'text': 'Plan a trial on one ward.'},
  ],
  'actions': {'go': {'detail': 'See the fixes first', 'say': 'Take me to the fixes'},
              'add': {'detail': 'Add a change, a measure or a role', 'say': 'I want to add a change, a measure or a role: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Every conversation starts here', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['This is your Processes page. It fills in once a fix is agreed.',
                    'It will hold the changes on the wards, the measures we watch and any new roles.'],
           'note': 'Change one ward first. Then spread it.', 'points': [],
           'prompts': ['Take me to the fixes', 'Who should be involved?', 'How does a trial work?']},
 },
}

HL = lambda h: '%d %s' % ((h - 1) % 12 + 1, 'AM' if h < 12 else 'PM')
CHAIR = '<svg viewBox="0 0 30 30" width="%d" height="%d" aria-hidden="true"><rect class="cb" x="5" y="3" width="20" height="6" rx="3"/><rect class="cs" x="4" y="10" width="22" height="17" rx="5"/></svg>'
def chair(filled, w=28):
    return '<span class="pr-seat %s">%s<span class="sr">%s</span></span>' % ('is-filled' if filled else 'is-empty', CHAIR % (w, w), 'Filled' if filled else 'Empty seat')

def top(d, empty):
    return masthead('Bed Management', PLACE, emblem(ICONS[PLACE]), STAMP['empty' if empty else 'filled']) + standing(d['claim'], d['deck'], empty)

def tail(d):
    return pending(d['pending']) + actions(d['actions'])

def mreading(m):
    if m['kind'] == 'start': return '<span class="pr-mv">%s</span>%s' % (e(m['value']), '<span class="pr-mk">Starting number</span>')
    if m['kind'] == 'need': return '<span class="pr-mv is-need">—</span>%s' % tag('need')
    return '<span class="pr-mv is-new">New</span><span class="pr-mk">Starts on the trial ward</span>'

def trial(d):
    t = d['trial']
    weeks = ''.join('<span class="pr-wk">Week %d</span>' % (i + 1) for i in range(t['weeks']))
    return ('<div class="pr-trial"%s><div><b>%s</b><span>%s</span></div><div class="pr-wks">%s</div><span class="pr-ts">%s</span></div>') % (
        pt(3) if d['changes'] else '', e(t['name']), e(t['line']), weeks, e(t['state']))

COMMON = BED_CSS + '''
.pr-seat{display:inline-flex}
.pr-seat .cb,.pr-seat .cs{stroke:var(--ink);stroke-width:2}
.pr-seat.is-filled .cb,.pr-seat.is-filled .cs{fill:var(--ink)}
.pr-seat.is-empty .cb,.pr-seat.is-empty .cs{fill:transparent;stroke:var(--amber);stroke-dasharray:4 3}
.pr-mv{font-family:'Bebas Neue',sans-serif;font-size:28px;line-height:1}
.pr-mv.is-need{color:var(--red)}.pr-mv.is-new{color:var(--acc)}
.pr-mk{font-size:11.5px;font-weight:600;color:var(--mut)}
.pr-trial{display:grid;grid-template-columns:minmax(0,1fr) auto auto;align-items:center;gap:18px;background:var(--ink);color:var(--card);padding:16px 20px;border-radius:0 0 14px 14px}
.pr-trial b{display:block;font-size:15px}.pr-trial span{font-size:13px;color:#E7D6D1}
.pr-wks{display:flex;gap:8px}
.pr-wk{min-width:92px;text-align:center;padding:8px 10px;border:1.5px dashed rgba(253,250,249,.55);border-radius:6px;font-size:12.5px !important;color:var(--card) !important}
.pr-ts{border:1.5px solid #d4a94f;color:#E8D3A2 !important;border-radius:14px;padding:4px 12px;font-weight:600;white-space:nowrap}
.pr-empty{border:2px dashed var(--grey);border-radius:14px;padding:26px 22px;font-size:14.5px;color:var(--mut)}
@container lp (max-width:699px){
 .pr-trial{grid-template-columns:1fr;gap:10px;padding:14px 16px}
 .pr-wks{display:none}
 .pr-ts{justify-self:start}
}
'''

# ------------------------------------------------------------------------------------------
# A · The shift board
def canvas_a(d, empty):
    if not d['changes']:
        cols = ''.join('<div class="pa-col"><div class="pa-ch"><b>%s</b></div><p class="pa-none">%s</p></div>' % (h, t) for h, t in [
            ('Process changes', 'Each change gets a magnet here.'), ('Measures we watch', 'Each measure gets a readout here.'), ('Team and role changes', 'Each new role gets a seat here.')])
        return top(d, empty) + section('The shift board', '<div class="pa-board is-empty"><div class="pa-cols">%s</div>%s</div>' % (cols, trial(d)), 'pa-sec') + tail(d)
    ch = ''.join('<li class="pa-mag"%s><i class="pa-dot %s" aria-hidden="true"></i><div><b>%s</b><p>%s</p><span class="pa-st">%s</span>'
                 '<details class="bm-more pa-more"><summary>See how it will work</summary><ul>%s</ul></details></div></li>' % (
        pt(c.get('pt')), 'agreed' if c['state'] != 'New' else 'new', e(c['name']), e(c['what']), e(c['state']), ''.join('<li>%s</li>' % e(x) for x in c['how'])) for c in d['changes'])
    ms = ''.join('<li class="pa-mag pa-m"%s><div><b>%s</b><p>%s</p></div><div class="pa-read">%s</div></li>' % (
        pt(m.get('pt')), e(m['name']), e(m['when']), mreading(m)) for m in d['measures'])
    rs = ''.join('<li class="pa-mag pa-r"%s><div class="pa-seats">%s</div><div><b>%s</b><p>%s</p></div></li>' % (
        pt(r.get('pt')), ''.join(chair(s) for s in r['seats']), e(r['name']), e(r['detail'])) for r in d['roles'])
    counts = ['%d agreed on paper · %d new · 0 tried' % (sum(1 for c in d['changes'] if c['state'] != 'New'), sum(1 for c in d['changes'] if c['state'] == 'New')),
              '1 with a starting number · 2 new', '2 seats to fill']
    cols = ''.join('<div class="pa-col"><div class="pa-ch">%s<b>%s</b><span>%s</span></div><ul>%s</ul></div>' % (ico(i, 'currentColor', 20), h, e(c), body) for (h, i, body), c in zip(
        [('Process changes', ICONS['Processes'], ch), ('Measures we watch', '<path d="M4 18a8 8 0 0116 0"/><path d="M12 18l4-6"/>', ms),
         ('Team and role changes', '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0112 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15 20a5 5 0 016-4.5"/>', rs)], counts))
    board = '<div class="pa-board"><div class="pa-cols">%s</div>%s</div>' % (cols, trial(d))
    return top(d, empty) + section('The shift board', board, 'pa-sec', 'The ward’s wall board: changes, measures and roles, with the trial across the foot') + tail(d)

CSS_A = '''
.pa-board{border:3px solid var(--ink);border-radius:16px;background:var(--card);overflow:hidden}
.pa-cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.pa-col{padding:20px 18px 22px;border-right:1.5px solid var(--line)}
.pa-col:last-child{border-right:0}
.pa-ch{display:grid;grid-template-columns:auto 1fr;column-gap:10px;align-items:center;padding-bottom:12px;margin-bottom:14px;border-bottom:2px solid var(--ink)}
.pa-ch b{font-size:16px}.pa-ch span{grid-column:2;font-size:12.5px;color:var(--mut)}
.pa-col ul{display:flex;flex-direction:column;gap:12px}
.pa-mag{display:flex;gap:12px;align-items:flex-start;padding:12px 14px;background:var(--soft);border-radius:8px;border-left:5px solid var(--ink)}
.pa-mag b{display:block;font-size:14px;line-height:1.35}.pa-mag p{font-size:13px;line-height:1.45;color:var(--mut);margin-top:3px}
.pa-dot{width:16px;height:16px;border-radius:50%;flex-shrink:0;margin-top:2px;background:var(--acc)}
.pa-dot.new{background:#d4a94f}
.pa-st{display:inline-block;margin-top:6px;font-size:11.5px;font-weight:600;color:var(--acc)}
.pa-m{flex-direction:column;gap:8px}.pa-read{display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 10px}
.pa-seats{display:flex;gap:4px;flex-shrink:0}
.pa-more{margin-top:10px}.pa-more>summary{min-height:40px;font-size:12.5px;background:var(--card)}
.pa-none{font-size:14px;color:var(--mut)}
.pa-board.is-empty{border-style:dashed}
@container lp (max-width:699px){
 .pa-cols{grid-template-columns:1fr}
 .pa-col{border-right:0;border-bottom:1.5px solid var(--line);padding:18px 14px}
}
'''

# ------------------------------------------------------------------------------------------
# B · The trial ward
def canvas_b(d, empty):
    if not d['changes']:
        beds = ''.join('<span class="bmb s-empty">%s</span>' % bed_svg(30) for _ in range(8))
        plan = ('<div class="pb-plan bm-paper is-empty"><div class="pb-bay"><span class="pb-rn">Beds bay</span><div class="pb-beds">%s</div></div>'
                '<div class="pb-stn"><span class="pb-rn">Nurses’ station</span></div><div class="pb-hk"><span class="pb-rn">Housekeeping</span></div></div>%s') % (beds, trial(d))
        return top(d, empty) + section('The trial ward', plan + '<p class="pr-empty" style="margin-top:18px">Each change will be pinned where it happens on this ward.</p>', 'pb-sec') + tail(d)
    pin = lambda c: '<button class="pb-pin js-pick" type="button" data-grp="pb" data-key="%d" aria-pressed="%s" aria-label="Change %d: %s">%d</button>' % (
        c['n'], 'true' if c['n'] == 1 else 'false', c['n'], e(c['name']), c['n'])
    at = lambda w: ''.join(pin(c) for c in d['changes'] if c['where'] == w)
    beds = ''.join('<span class="bmb s-%s">%s</span>' % ('done' if i not in (2, 5) else 'later', bed_svg(30)) for i in range(8))
    seats = ''.join('<span class="pb-seat"%s>%s<em>%s</em></span>' % (pt(r.get('pt')), ''.join(chair(s, 30) for s in r['seats']), e(r['name'])) for r in d['roles'])
    reads = ''.join('<div class="pb-read"%s><span class="pb-rl">%s</span>%s</div>' % (pt(m.get('pt')), e(m['name']), mreading(m)) for m in d['measures'])
    plan = ('<div class="pb-wrap"><div class="pb-plan bm-paper">'
            '<div class="pb-bay"><span class="pb-rn">Beds bay</span><div class="pb-beds">%s</div><div class="pb-pins">%s</div></div>'
            '<div class="pb-stn"><span class="pb-rn">Nurses’ station</span><div class="pb-pins">%s</div><div class="pb-seats">%s</div></div>'
            '<div class="pb-hk"><span class="pb-rn">Housekeeping room</span><div class="pb-pins">%s</div></div>'
            '<div class="pb-wall"><span class="pb-rn">On the station wall: the measures we watch</span><div class="pb-reads">%s</div></div></div>%s</div>') % (
        beds, at('bay'), at('stn'), seats, at('hk'), reads, trial(d))
    legend = ''.join('<button class="pb-lg js-pick" type="button" data-grp="pb" data-key="%d" aria-pressed="%s"%s><span class="pb-ln">%d</span><span><b>%s</b><em>%s</em></span></button>' % (
        c['n'], 'true' if c['n'] == 1 else 'false', pt(c.get('pt')), c['n'], e(c['name']), e(c['state'])) for c in d['changes'])
    dets = ''.join('<p class="pb-det" data-det="pb:%d"%s>%s</p>' % (c['n'], '' if c['n'] == 1 else ' hidden', e(c['what'])) for c in d['changes'])
    body = '<div class="pb-grid">%s<div class="pb-side"><h4>The changes</h4>%s%s</div></div>' % (plan, legend, dets)
    return top(d, empty) + section('The trial ward', body, 'pb-sec', 'One ward seen from above. Each change is pinned where it happens. Pick a pin or a change.') + tail(d)

CSS_B = '''
.pb-grid{display:grid;grid-template-columns:minmax(0,1fr) 260px;gap:24px;align-items:start}
.pb-plan{display:grid;grid-template-columns:1.5fr 1fr;grid-template-rows:auto auto auto;border:3px solid var(--ink);border-radius:14px 14px 0 0;overflow:hidden}
.pb-plan>div{position:relative;padding:14px 16px 16px;min-height:120px}
.pb-rn{display:block;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin-bottom:10px}
.pb-bay{grid-row:1/span 2;border-right:2.5px solid var(--ink)}
.pb-beds{display:grid;grid-template-columns:repeat(4,max-content);gap:10px 14px}
.pb-stn{border-bottom:2.5px solid var(--ink);background:rgba(58,37,34,.05);padding-right:64px !important}
.pb-hk{}
.pb-wall{grid-column:1/-1;border-top:2.5px solid var(--ink);min-height:0 !important}
.pb-pins{position:absolute;right:12px;top:10px;display:flex;gap:6px}
.pb-bay .pb-pins{top:auto;bottom:14px;right:auto;left:16px}
.pb-pin{width:40px;height:40px;border-radius:50% 50% 50% 4px;background:var(--acc);color:#fff;border:2px solid var(--card);font-weight:700;font-size:15px;box-shadow:0 2px 0 var(--ink)}
.pb-pin[aria-pressed=true]{background:#d4a94f;color:var(--ink);outline:3px solid var(--ink)}
.pb-seats{display:flex;flex-wrap:wrap;gap:10px 16px;margin-top:4px}
.pb-seat{display:flex;align-items:center;gap:4px}.pb-seat em{font-style:normal;font-size:12px;font-weight:600;margin-left:4px}
.pb-reads{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.pb-read{display:flex;flex-direction:column;gap:3px;background:var(--card);border:1.5px solid var(--ink);border-radius:8px;padding:10px 12px}
.pb-rl{font-size:12.5px;font-weight:600;line-height:1.35}
.pb-side h4{font-size:13.5px;font-weight:600;margin-bottom:10px}
.pb-lg{display:flex;gap:12px;align-items:flex-start;width:100%;text-align:left;background:var(--card);border:1.5px solid var(--ink);border-radius:12px;padding:12px;margin-bottom:10px}
.pb-lg b{display:block;font-size:14px;line-height:1.35}.pb-lg em{font-style:normal;font-size:12px;color:var(--acc);font-weight:600}
.pb-ln{flex-shrink:0;width:28px;height:28px;border-radius:50% 50% 50% 4px;background:var(--acc);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.pb-lg[aria-pressed=true]{box-shadow:0 0 0 3px #d4a94f}.pb-lg[aria-pressed=true] .pb-ln{background:#d4a94f;color:var(--ink)}
.pb-det{font-size:14px;line-height:1.55;padding:12px 14px;border-left:4px solid #d4a94f;background:var(--soft);border-radius:0 8px 8px 0}
.pb-det[hidden]{display:none}
.pb-plan.is-empty{border-style:dashed}
@container lp (max-width:699px){
 .pb-grid{grid-template-columns:1fr}
 .pb-plan{grid-template-columns:1fr}
 .pb-bay{grid-row:auto;border-right:0;border-bottom:2.5px solid var(--ink);padding-bottom:64px !important}
 .pb-beds{grid-template-columns:repeat(4,max-content)}
 .pb-reads{grid-template-columns:1fr}
}
'''

# ------------------------------------------------------------------------------------------
# C · Shift by shift: 8 PM to 8 PM, night then day
def canvas_c(d, empty):
    hrs = ['8 PM', '11 PM', '2 AM', '5 AM', '8 AM', '11 AM', '2 PM', '5 PM', '8 PM']
    ruler = ''.join('<span style="left:%.3f%%">%s</span>' % (i * 12.5, h) for i, h in enumerate(hrs))
    pos = lambda h: ((h - 20) % 24) / 24 * 100
    if not d['changes']:
        day = ('<div class="pc-day bm-paper is-empty"><div class="pc-shift pc-night"><b>Night shift</b><span>8 PM to 8 AM</span></div><div class="pc-shift pc-dayf"><b>Day shift</b><span>8 AM to 8 PM</span></div>'
               '<div class="pc-ruler">%s</div></div>%s') % (ruler, trial(d))
        return top(d, empty) + section('Shift by shift', day + '<p class="pr-empty" style="margin-top:18px">Each change will sit at the hour it happens.</p>', 'pc-sec') + tail(d)
    spans = ''.join('<div class="pc-span"%s><span>%d · %s</span><em>Every shift</em></div>' % (pt(c.get('pt')), c['n'], e(c['name'])) for c in d['changes'] if c.get('span'))
    def anchor(p, k):
        side = 'right:%.2f%%' % (100 - p) if p > 55 else 'left:%.2f%%' % p
        return ' style="%s;--row:%d"' % (side, k), (' rt' if p > 55 else '')
    ms_ = [c for c in d['changes'] if not c.get('span')]
    marks = ''.join('<span class="pc-mk%s"%s%s><i>%d</i><span>%s</span></span>' % (
        anchor(pos(c['at'][0]), k)[1], anchor(pos(c['at'][0]), k)[0], pt(c.get('pt')), c['n'], e(c['name'])) for k, c in enumerate(sorted(ms_, key=lambda c: c['at'][0])))
    cks = [m for m in d['measures'] if m['at']]
    checks = ''.join('<span class="pc-ck%s"%s%s><i aria-hidden="true"></i><span>%s</span></span>' % (
        anchor(pos(m['at']), k)[1], anchor(pos(m['at']), k)[0], pt(m.get('pt')), e(m['name'] + ' · ' + m['when'][0].lower() + m['when'][1:])) for k, m in enumerate(cks))
    seats = lambda sh: ''.join('<span class="pc-seat"%s>%s<em>%s</em></span>' % (pt(r.get('pt')), chair(r['seats'][min(i, len(r['seats']) - 1)] if r['seats'] else 0, 26), e(r['name']))
                               for r in d['roles'] for i, s in enumerate(r['shifts']) if s == sh)
    day = ('<div class="pc-day bm-paper"><div class="pc-shift pc-night"><b>Night shift</b><span>8 PM to 8 AM</span><div class="pc-seats">%s</div></div>'
           '<div class="pc-shift pc-dayf"><b>Day shift</b><span>8 AM to 8 PM</span><div class="pc-seats">%s</div></div>'
           '<div class="pc-lanes"><div class="pc-lane"><span class="pc-ll">Changes</span>%s%s</div><div class="pc-lane pc-lane2"><span class="pc-ll">Checks</span>%s</div></div>'
           '<div class="pc-ruler">%s</div></div>%s') % (seats('night'), seats('day'), spans, marks, checks, ruler, trial(d))
    cards = ''.join('<div class="pc-card"%s><span class="pc-n">%d</span><div><b>%s</b><p>%s</p><em>%s</em></div></div>' % (
        pt(c.get('pt')), c['n'], e(c['name']), e(c['what']), e(c['state'])) for c in d['changes'])
    reads = ''.join('<div class="pc-read"%s><span class="pb-rl">%s</span><span class="pc-when">%s</span>%s</div>' % (
        pt(m.get('pt')), e(m['name']), e(m['when']), mreading(m)) for m in d['measures'])
    roles = ''.join('<div class="pc-role"%s><div>%s</div><b>%s</b><p>%s</p></div>' % (pt(r.get('pt')), ''.join(chair(s, 28) for s in r['seats']), e(r['name']), e(r['detail'])) for r in d['roles'])
    return (top(d, empty) + section('Shift by shift', day, 'pc-sec', 'The ward’s day from 8 PM to 8 PM. Each change and each check at its hour, the seats in each shift.')
            + section('The changes', '<div class="pc-cards">%s</div>' % cards, 'pc-sec2')
            + section('Measures we watch and the team', '<div class="pc-two"><div class="pc-reads">%s</div><div class="pc-roles">%s</div></div>' % (reads, roles), 'pc-sec3') + tail(d))

CSS_C = '''
.pc-day{position:relative;display:grid;grid-template-columns:1fr 1fr;border:3px solid var(--ink);border-radius:14px 14px 0 0;overflow:hidden;padding-bottom:34px}
.pc-shift{padding:14px 16px 12px;display:flex;flex-direction:column;gap:2px}
.pc-shift b{font-size:15px}.pc-shift>span{font-size:12.5px;color:var(--mut)}
.pc-night{background:rgba(58,37,34,.88);color:var(--card)}.pc-night>span{color:#E7D6D1 !important}
.pc-dayf{border-left:2.5px solid var(--ink)}
.pc-seats{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:8px}
.pc-seat{display:inline-flex;align-items:center;gap:6px}.pc-seat em{font-style:normal;font-size:12px;font-weight:600}
.pc-night .pr-seat.is-empty .cb,.pc-night .pr-seat.is-empty .cs{stroke:#E8C98A}
.pc-lanes{grid-column:1/-1;border-top:2.5px solid var(--ink)}
.pc-lane{position:relative;height:176px;border-bottom:1.5px dashed var(--line)}
.pc-lane2{height:96px;border-bottom:0}
.pc-ll{position:absolute;left:10px;top:8px;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);background:var(--card);padding:0 6px}
.pc-span{position:absolute;left:12px;right:12px;top:34px;display:flex;justify-content:space-between;align-items:center;gap:10px;background:var(--acc);color:#fff;border-radius:16px;padding:6px 14px;font-size:13px;font-weight:600}
.pc-span em{font-style:normal;font-size:11.5px;opacity:.9}
.pc-mk{position:absolute;top:calc(78px + var(--row)*48px);display:flex;align-items:center;gap:8px;background:var(--card);border:1.5px solid var(--ink);border-radius:20px;padding:3px 14px 3px 3px;font-size:13px;white-space:nowrap;min-height:40px}
.pc-mk b{font-weight:600;color:var(--acc)}
.pc-mk::before{content:"";position:absolute;left:18px;top:calc(-8px - var(--row)*48px);height:calc(8px + var(--row)*48px);border-left:2px solid var(--ink)}
.pc-mk.rt{flex-direction:row-reverse;padding:3px 3px 3px 14px}.pc-mk.rt::before{left:auto;right:18px}
.pc-mk i{font-style:normal;font-weight:700;width:30px;height:30px;border-radius:50%;background:#d4a94f;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.pc-ck{position:absolute;top:calc(32px + var(--row)*28px);display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:600;white-space:nowrap}
.pc-ck.rt{flex-direction:row-reverse}.pc-ck.rt i{margin:0 -7px 0 0}
.pc-ck i{width:14px;height:14px;transform:rotate(45deg);border:2px solid var(--acc);background:var(--card);margin-left:-7px;flex-shrink:0}
.pc-ruler{position:absolute;left:0;right:0;bottom:0;height:32px;border-top:2.5px solid var(--ink);background:var(--card)}
.pc-ruler span{position:absolute;top:7px;transform:translateX(-50%);font-size:11.5px;font-weight:600;color:var(--mut);white-space:nowrap}
.pc-ruler span:first-child{transform:none;padding-left:6px}.pc-ruler span:last-child{transform:translateX(-100%);padding-right:6px}
.pc-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.pc-card{display:flex;gap:12px;padding:16px;background:var(--card);border:1.5px solid var(--ink);border-radius:14px}
.pc-n{flex-shrink:0;width:30px;height:30px;border-radius:50%;background:var(--ink);color:var(--card);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.pc-card b{display:block;font-size:14.5px;line-height:1.35}.pc-card p{font-size:13.5px;line-height:1.5;color:var(--mut);margin-top:4px}.pc-card em{display:block;font-style:normal;font-size:12px;font-weight:600;color:var(--acc);margin-top:6px}
.pc-two{display:grid;grid-template-columns:1.4fr 1fr;gap:20px}
.pc-reads{display:flex;flex-direction:column;gap:10px}
.pc-read{display:grid;grid-template-columns:1fr auto;grid-template-rows:auto auto;column-gap:14px;align-items:center;padding:12px 16px;background:var(--card);border:1.5px solid var(--ink);border-radius:12px}
.pc-read .pb-rl{font-size:14px;font-weight:600}.pc-when{grid-column:1;font-size:12.5px;color:var(--mut)}
.pc-read .pr-mv,.pc-read .bm-tag,.pc-read .pr-mk{grid-column:2;grid-row:1/span 2;justify-self:end}
.pc-read .pr-mv{grid-row:1}.pc-read .pr-mk,.pc-read .bm-tag{grid-row:2}
.pc-roles{display:flex;flex-direction:column;gap:10px}
.pc-role{padding:14px 16px;background:var(--soft);border-radius:12px;border-left:5px solid var(--ink)}
.pc-role b{display:block;font-size:14.5px;margin-top:6px}.pc-role p{font-size:13px;color:var(--mut);line-height:1.45}
.pc-day.is-empty{border-style:dashed}
@container lp (max-width:699px){
 .pc-day{grid-template-columns:1fr 1fr}
 .pc-shift{padding:12px 10px}
 .pc-seat em{display:none}
 .pc-lane,.pc-lane2{height:auto;padding:34px 10px 12px;display:flex;flex-direction:column;gap:8px}
 .pc-span{position:static;flex-direction:column;align-items:flex-start;border-radius:12px}
 .pc-mk,.pc-mk.rt{position:static;flex-direction:row;padding:3px 12px 3px 3px;white-space:normal;line-height:1.35;border-radius:16px}
 .pc-mk::before{display:none}
 .pc-ck,.pc-ck.rt{position:static;white-space:normal;margin-left:7px;flex-direction:row}.pc-ck.rt i{margin:0 0 0 -7px}
 .pc-day{padding-bottom:0}
 .pc-ruler{display:none}
 .pc-ruler span:nth-child(even){display:none}
 .pc-cards{grid-template-columns:1fr}
 .pc-two{grid-template-columns:1fr}
}
'''

SAMPLES = {'a': (canvas_a, CSS_A), 'b': (canvas_b, CSS_B), 'c': (canvas_c, CSS_C)}
ABOUT = {
 'a': ('The shift board', 'The ward’s wall board: process changes, measures we watch, and team and role changes in three columns of magnet strips, each role with its seats, filled or empty. The two-week trial runs across the foot.', 'The day shift: pale clay, deep brown, pill buttons'),
 'b': ('The trial ward', 'One ward seen from above, the one the trial will run on. Each change is pinned where it happens: the beds bay, the nurses’ station or the housekeeping room. The seats for new roles sit at the station and the measures hang on its wall. Pick a pin or a change.', 'The day shift: pale clay, deep brown, pill buttons'),
 'c': ('Shift by shift', 'The ward’s day from 8 PM to 8 PM, night shift then day shift. Changes and checks sit at their hour, and each shift shows its seats. The changes, the measures and the team follow underneath.', 'The day shift: pale clay, deep brown, pill buttons'),
}

if __name__ == '__main__':
    place_main(PLACE, 'pr', DATA, SAMPLES, COMMON, {k: THEME for k in SAMPLES}, ABOUT,
               'Three ways to draw the Processes page for Bed Management, each taken from the ward plan on the home page. All three share one look for Processes, the day shift, and keep the same zones and three buttons.',
               'Each page may run to about two screens on desktop, so every part has room.')
