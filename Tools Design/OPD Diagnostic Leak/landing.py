"""
OPD Diagnostic Leak: the tool's home page and the four place pages (8 Oct 2026, for review).

Same five zones as every landing page, in the same order (06 §11.2): masthead with stamp and
Refresh now, where this stands, the drawing, what Tojo still has to do, the three buttons.
Same behaviour as Bed Management v3: chat one screen tall with its own scroll, the first element
raised with its box open, on a phone each box opens right under its element, pickable items stacked.

What is new for this tool:
  home        the leak line: one pipe from the clinic to the test rooms, a valve for each part
              of the work, drops falling where tests still leave. A split top: the claim on the
              left, the leak meter on the right.
  Diagnosis   the sieve: 100 tests written, and how many are left at each step, with the reason
              each group drops out; the four possible main causes weighed below.
  Solutions   the prescription pad: each fix written as a line, with its four stops as boxes to
              tick, and its by-hand and automatic versions side by side.
  Automations one patient's visit: the helpers placed on the stations of a visit where they act.
  Processes   the busy-hours board: patients per hour against what the desk can do, the changes
              pinned under the hours they act, the numbers we watch and the roles beside it.

Example figures come from the case study in opd-diagnostic-leakage.md §0 (40 new and 400 returning
outpatients a day; 1 in 10 new and 2 in 10 returning patients finish their tests here; about
₹1.5 lakh lost a day; about 5% of profit). Everything else is marked Example only or Tojo's guess.

Run:  python3 landing.py [--measure]   ->  out/landing/
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import odl_common as C
from odl_common import (e, ico, ICONS, CHEV, sel, sel_cls, box, pt, tag, say_btn, masthead, standing, section,
                        pending, actions, emblem, STAMP, THEMES, TOOL)

OUT = os.path.join(HERE, 'out', 'landing')
KICK = 'Virevo · ' + C.HOSPITAL

# ==========================================================================================
# Shared CSS for this tool's pages (on top of the Bed Management base)
TOOL_CSS = '''
.od .bm-emb{box-shadow:inset 0 0 0 3px var(--ink),inset 0 0 0 5px var(--hi);border-radius:50%}
.od .lp-act-go{box-shadow:inset 6px 0 0 var(--hi)}
.od .bm-tag.guess{border-color:var(--mut);color:var(--mut)}
.od-st{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;padding:3px 11px;border-radius:12px;border:1.5px solid var(--ink);white-space:nowrap}
.od-st.s-done{background:var(--ink);color:var(--card)}
.od-st.s-now{background:var(--hi);border-color:var(--hi);color:#fff}
.od-st.s-later{background:var(--soft)}
.od-st.s-none,.od-st.s-empty{border-style:dashed;border-color:var(--grey);color:var(--mut)}
.od-steps{display:flex;flex-direction:column;gap:8px}
.od-steps li{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;font-size:14px;line-height:1.45;padding:8px 0;border-bottom:1.5px dashed var(--line)}
.od-steps li:last-child{border-bottom:0}
.od-box{display:flex;flex-direction:column;gap:12px;padding:18px 22px;background:var(--card);border:2px solid var(--ink);border-radius:10px;border-left:7px solid var(--hi)}
.od-box h4{font-size:17px;font-weight:600}
.od-box p{font-size:14.5px;line-height:1.55}
.od-lab{font-size:12px;font-weight:600;color:var(--mut);letter-spacing:.02em}
.od-two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.od-two>div{display:flex;flex-direction:column;gap:6px;min-width:0}
.od-bul{display:flex;flex-direction:column;gap:5px}
.od-bul li{position:relative;padding-left:15px;font-size:13.5px;line-height:1.5}
.od-bul li::before{content:"";position:absolute;left:1px;top:.6em;width:6px;height:6px;border-radius:50%;background:var(--hi)}
.od .bm-open{align-self:flex-start}
.od-empty{border:2px dashed var(--grey);border-radius:10px;padding:16px 18px;color:var(--mut);font-size:13.5px;line-height:1.5;background:transparent}
.od .bx-mob{background:transparent;border:0}
.od .bx-mob::before{border-left:2px solid var(--ink);border-top:2px solid var(--ink);background:var(--card);z-index:1;top:-7px}
.od .bx-mob .od-box{padding:14px 16px}
.od p,.od li,.od b,.od em,.od span{overflow-wrap:anywhere}
@container lp (max-width:699px){
 .od-two{grid-template-columns:1fr}
 .od-box h4{font-size:16px}
}
'''

def steps_list(steps, labels):
    return '<ul class="od-steps">%s</ul>' % ''.join(
        '<li><span>%s</span><span class="od-st s-%s">%s</span></li>' % (e(t), s, e(labels[s])) for t, s in steps)

# ==========================================================================================
# HOME · the leak line
STEP = {'done': 'Done', 'now': 'Now', 'later': 'Still to do', 'none': 'Not started'}
STATUS = {'now': 'In use now', 'started': 'Taking shape', 'none': 'Not started', 'empty': 'Nothing yet'}
HOME = {
 'filled': {
  'claim': 'Tests are written here, but most are done somewhere else',
  'deck': 'Diagnosis is two steps in. Four fixes are on the table, each with a by-hand and an automatic version. Nothing is switched on or changed yet.',
  'meter': {'lost': '₹1.5 lakh', 'lost_l': 'lost each day to tests done elsewhere', 'share': 'About 5 rupees of every 100 rupees of profit',
            'here': 'About 2 in 10', 'here_l': 'patients finish their tests here', 'closed': 0, 'tag': 'example'},
  'places': [
   {'name': 'Diagnosis', 'status': 'now', 'pt': 1, 'head': 'Only about 2 in 10 patients finish their tests here.',
    'fig': ('1 in 10', 'new patients who finish their tests here', 'example'), 'unit': 'steps done',
    'steps': [['Put a number on the leak', 'done'], ['Follow one prescription from the doctor to the test', 'done'],
              ['Check the desk staff in the busy hours', 'now'], ['Check how scans are booked', 'later'], ['Name the main cause', 'later']]},
   {'name': 'Solutions', 'status': 'started', 'pt': 3, 'head': 'Four fixes on the table. One is taking shape.',
    'fig': ('About half', 'of the lost tests could come back', 'guess'), 'unit': 'fixes agreed',
    'steps': [['Record every prescription', 'now'], ['Walk each patient to the test desk', 'later'],
              ['Keep urgent scan slots free, then fill them', 'later'], ['Share yesterday’s numbers every morning', 'later']]},
   {'name': 'Automations', 'status': 'none', 'head': 'Four helpers wait for the fixes to be agreed.', 'fig': None, 'unit': 'switched on',
    'steps': [['Reads each prescription and works out its value', 'none'], ['Books the test from the prescription', 'none'],
              ['Keeps the patient company through the visit', 'none'], ['Sends yesterday’s numbers at 8 AM', 'none']]},
   {'name': 'Processes', 'status': 'none', 'head': 'Four changes and one new role wait for a trial.', 'fig': None, 'unit': 'tried',
    'steps': [['Scan every prescription at the desk', 'none'], ['Guest services in the busy hours', 'none'],
              ['A Scheduling Manager for the scans', 'none'], ['A ten-minute look at the numbers each morning', 'none']]},
  ],
  'pending': [
   {'text': 'Count the desk staff on each shift and the patients they see each hour.', 'need': 'Needs your staff list for the outpatient desk', 'pt': 2},
   {'text': 'Find out who books scans, and what happens when an urgent case comes in.', 'pt': 4},
   {'text': 'Check whether every prescription is recorded, or the leak is worked out from footfall.'},
   {'text': 'Split the leak by test room: X-ray, MRI, lab, heart tests.', 'need': 'Needs last month’s bills by department'},
  ],
  'actions': {'go': {'detail': 'Check the desk staff in the busy hours', 'say': 'Let’s check the desk staff in the busy hours'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about our outpatient tests: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Pick up where you left off', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Here is where the OPD Diagnostic Leak work stands, across all four parts.',
                    'Diagnosis is two steps in. Doctors write the tests, but only about 2 in 10 patients finish them here.',
                    'Two things would sharpen this: your desk staff by shift, and who books the scans.'],
           'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
           'note': 'Patients are willing. The way tests are booked lets them go.',
           'points': [{'n': 1, 'label': 'Tests that leave the hospital'}, {'n': 2, 'label': 'Desk staff in the busy hours'},
                      {'n': 3, 'label': 'The four fixes'}, {'n': 4, 'label': 'How scans are booked'}],
           'prompts': ['Let’s check the desk staff in the busy hours', 'Why do patients take tests elsewhere?', 'Show me the four fixes']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Start with Diagnosis. Tojo follows one prescription from the doctor’s desk to the test room with you, and fills this page as you go.',
  'meter': None,
  'places': [
   {'name': 'Diagnosis', 'status': 'empty', 'head': 'Fills in as you follow one prescription with Tojo.', 'fig': None, 'steps': []},
   {'name': 'Solutions', 'status': 'empty', 'head': 'Fills in once the main cause is named.', 'fig': None, 'steps': []},
   {'name': 'Automations', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': []},
   {'name': 'Processes', 'status': 'empty', 'head': 'Fills in once a fix is agreed.', 'fig': None, 'steps': []},
  ],
  'pending': [
   {'text': 'Follow one prescription, from the doctor writing it to the test being done.'},
   {'text': 'Put a number on the tests that leave each day.', 'need': 'Needs a week of outpatient numbers'},
   {'text': 'Find out how scans and lab tests are booked today.'},
  ],
  'actions': {'go': {'detail': 'Follow one prescription with Tojo', 'say': 'Let’s follow one prescription'},
              'add': {'detail': 'Share a report or a bill list', 'say': 'Here is what I already know about our outpatient tests: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Every conversation starts here', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Welcome to OPD Diagnostic Leak. This page fills in as we talk.',
                    'We start by following one prescription: the doctor writes a test, and we see where the patient goes next.'],
           'note': 'Follow one slip. The rest follows.', 'points': [],
           'prompts': ['Let’s follow one prescription', 'What should I bring?', 'How does this work?']},
 },
}

def valve_svg(frac, size=64):
    """A valve wheel. frac = how far it is closed (0 to 1): the arc fills and the handle turns."""
    r = 26; circ = 2 * 3.14159 * r
    return ('<svg class="op-wheel" viewBox="0 0 64 64" width="%d" height="%d" aria-hidden="true">'
            '<circle cx="32" cy="32" r="%d" class="w-ring"/><circle cx="32" cy="32" r="%d" class="w-arc" stroke-dasharray="%.1f %.1f" transform="rotate(-90 32 32)"/>'
            '<g transform="rotate(%d 32 32)"><path class="w-spoke" d="M32 10v44M10 32h44"/></g><circle cx="32" cy="32" r="7" class="w-hub"/></svg>') % (
        size, size, r, r, circ * frac, circ, int(90 * frac))

def drips(n):
    return '<span class="op-drips" aria-hidden="true">%s</span>' % ''.join(
        '<i class="op-drip" style="--d:%.1fs;--x:%dpx"></i>' % (0.6 * i, (i - 1) * 12) for i in range(n))

def home_canvas(state):
    d = HOME[state]; empty = state == 'empty'
    # the top: claim on the left, the leak meter on the right
    m = d['meter']
    if m:
        meter = ('<aside class="oh-meter"%s><div class="oh-mh"><span class="od-lab">The leak today</span>%s</div>'
                 '<div class="oh-mv">%s</div><div class="oh-ml">%s</div><p class="oh-ms">%s</p>'
                 '<div class="oh-mrow"><div><b>%s</b><span>%s</span></div></div>'
                 '<div class="oh-jar" aria-label="Leak closed so far: none yet"><span class="od-lab">Closed so far</span><span class="oh-bar"><i style="width:%d%%"></i></span><b>None yet</b></div></aside>') % (
            pt(1), tag(m['tag']), e(m['lost']), e(m['lost_l']), e(m['share']), e(m['here']), e(m['here_l']), m['closed'])
    else:
        meter = '<aside class="oh-meter is-empty"><span class="od-lab">The leak today</span><p>Fills in once the tests that leave each day have a number.</p></aside>'
    top = '<div class="oh-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), meter)

    valves, desk = [], []
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        done = sum(1 for _, s in p['steps'] if s == 'done')
        frac = done / len(p['steps']) if p['steps'] else 0
        prog = ('%d of %d %s' % (done, len(p['steps']), p['unit'])) if p['steps'] else ''
        n_drips = 0 if empty else (3 if frac < .34 else 2 if frac < .67 else 1 if frac < 1 else 0)
        inner = ('<span class="op-wrap">%s%s</span><span class="op-txt"><span class="op-pn">%s%s</span><span class="od-st s-%s">%s</span>'
                 '<span class="op-hl">%s</span><span class="op-prog">%s</span></span>%s') % (
            valve_svg(frac), drips(n_drips), ico(ICONS[p['name']], 'currentColor', 18), e(p['name']), p['status'],
            e(STATUS[p['status']]), e(p['head']), e(prog), CHEV if not empty else '')
        if empty:
            valves.append('<div class="op-valve is-empty" data-s="empty">%s</div>' % inner)
            continue
        valves.append('<button class="op-valve %s" type="button" data-s="%s"%s%s>%s</button>' % (
            sel_cls(first), p['status'], sel('ov', k, first), pt(p.get('pt')), inner))
        fig = ''
        if p['fig']:
            v, l, t = p['fig']
            fig = '<div class="op-fig"><span class="op-fv">%s</span><span>%s</span>%s</div>' % (e(v), e(l), tag(t))
        det = ('<div class="od-box"><div class="op-bh"><h4>%s</h4><span class="od-st s-%s">%s</span></div><p>%s</p>%s%s%s</div>') % (
            e(p['name']), p['status'], e(STATUS[p['status']]), e(p['head']), fig, steps_list(p['steps'], STEP),
            say_btn('Open ' + p['name'], 'Take me to ' + p['name']))
        valves.append(box('ov', k, det, first, 'mob'))
        desk.append(box('ov', k, det, first, 'desk'))
    src = ('<div class="op-end op-src"><svg viewBox="0 0 48 48" width="44" height="44" aria-hidden="true"><path class="t-body" d="M6 14h22v8H6z"/><path class="t-body" d="M28 16h10a4 4 0 014 4v8h-8v-4h-6z"/><path class="t-body" d="M14 8h6v6h-6z"/></svg>'
           '<b>Tests written in the clinic</b><span>%s</span></div>') % ('440 patients a day' if not empty else 'Your outpatients each day')
    out = ('<div class="op-end op-out"><svg viewBox="0 0 48 48" width="44" height="44" aria-hidden="true"><path class="t-body" d="M10 10h28v28H10z"/><path class="t-mark" d="M17 24l5 5 10-11"/></svg>'
           '<b>Tests done here</b><span>%s</span></div>') % ('About 2 in 10' if not empty else 'Counted as we go')
    line = '<div class="op-line%s"><div class="op-pipe" aria-hidden="true"></div>%s<div class="op-valves">%s</div>%s</div>' % (
        ' is-empty' if empty else '', src, ''.join(valves), out)
    key = ('<div class="bm-key op-key" aria-hidden="true"><span><i class="k-wheel"></i>The valve turns shut as each part is done</span>'
           '<span><i class="k-drop"></i>Drops: tests still leaving</span></div>') if not empty else ''
    sub = 'One valve for each part of the work. Tap a valve to read its steps.' if not empty else 'One valve for each part of the work'
    body = line + key + ('<div class="op-desk">%s</div>' % ''.join(desk) if desk else '')
    return (masthead(KICK, TOOL, emblem(), STAMP[state]) + top
            + section('Where each part of the work stands', body, 'op-sec', sub) + pending(d['pending']) + actions(d['actions']))

HOME_CSS = '''
.od-home .bm-name{font-size:46px}
.od-home .lp-stamp-txt{max-width:230px}
.od-home .bm-id{flex-shrink:1}
.oh-top{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:32px;align-items:start;margin:30px 0 8px}
.oh-top .bm-stand{margin:6px 0 0}
.oh-meter{position:relative;background:var(--ink);color:var(--card);border-radius:16px 16px 16px 4px;padding:20px 22px;display:flex;flex-direction:column;gap:6px;box-shadow:0 10px 0 -4px var(--hi)}
.oh-meter .od-lab{color:var(--line)}
.oh-mh{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.oh-meter .bm-tag.guess{border-color:var(--line);color:var(--line)}
.oh-mv{font-family:'Bebas Neue',sans-serif;font-size:56px;line-height:.95;color:var(--hi)}
.oh-ml{font-size:14px;font-weight:500}
.oh-ms{font-size:12.5px;color:var(--line);line-height:1.45}
.oh-mrow{display:flex;gap:14px;border-top:1.5px dashed rgba(255,255,255,.25);padding-top:10px;margin-top:4px}
.oh-mrow div{display:flex;flex-direction:column}.oh-mrow b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:28px;line-height:1}.oh-mrow span{font-size:12.5px;color:var(--line)}
.oh-jar{display:flex;align-items:center;gap:10px;margin-top:6px;flex-wrap:wrap}
.oh-bar{flex:1 1 80px;height:10px;border-radius:5px;background:rgba(255,255,255,.18);overflow:hidden;min-width:60px}.oh-bar i{display:block;height:100%;background:var(--hi)}
.oh-jar b{font-size:12.5px;font-weight:600}
.oh-meter.is-empty{background:transparent;color:var(--mut);border:2px dashed var(--grey);box-shadow:none}
.oh-meter.is-empty .od-lab{color:var(--mut)}.oh-meter.is-empty p{font-size:14px;line-height:1.5}
/* the line */
.op-line{position:relative;display:grid;grid-template-columns:104px minmax(0,1fr) 104px;gap:8px;align-items:start;padding:26px 18px 22px;border:3px solid var(--ink);border-radius:14px;background:var(--card)}
.op-pipe{position:absolute;left:70px;right:70px;top:58px;height:16px;border-radius:8px;background:var(--soft);border:2.5px solid var(--ink);box-shadow:inset 0 4px 0 rgba(255,255,255,.7)}
.op-end{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;padding-top:4px}
.op-end svg{background:var(--card);border-radius:8px}
.op-end b{font-size:13px;line-height:1.3}.op-end span{font-size:12px;color:var(--mut)}
.op-out span{font-family:'Bebas Neue',sans-serif;font-size:22px;color:var(--ink);line-height:1}
.op-line.is-empty .op-out span{font-family:inherit;font-size:12px;color:var(--mut);line-height:1.4}
.t-body{fill:var(--card);stroke:var(--ink);stroke-width:2.5;stroke-linejoin:round}.t-mark{fill:none;stroke:var(--hi);stroke-width:3.5;stroke-linecap:round;stroke-linejoin:round}
.op-valves{position:relative;z-index:1;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.op-valve{display:flex;flex-direction:column;align-items:center;gap:8px;padding:6px 8px 12px;border:0;background:transparent;border-radius:12px;text-align:center;min-width:0}
.lp .op-valve.is-up{background:var(--soft)}
.op-wrap{position:relative;display:flex;flex-direction:column;align-items:center;height:96px}
.op-wheel{background:var(--card);border-radius:50%}
.w-ring{fill:var(--card);stroke:var(--ink);stroke-width:3}
.w-arc{fill:none;stroke:var(--hi);stroke-width:7;stroke-linecap:round}
.w-spoke{stroke:var(--ink);stroke-width:3;stroke-linecap:round}.w-hub{fill:var(--ink)}
.op-valve[data-s=none] .w-ring,.op-valve[data-s=empty] .w-ring{stroke:var(--grey);stroke-dasharray:5 4}
.op-valve[data-s=none] .w-spoke,.op-valve[data-s=empty] .w-spoke{stroke:var(--grey)}.op-valve[data-s=none] .w-hub,.op-valve[data-s=empty] .w-hub{fill:var(--grey)}
.op-drips{position:relative;width:40px;height:30px}
.op-drip{position:absolute;left:calc(50% - 5px + var(--x));top:0;width:10px;height:13px;background:var(--hi);border-radius:50% 50% 50% 50%/60% 60% 40% 40%;clip-path:polygon(50% 0,100% 55%,100% 100%,0 100%,0 55%);animation:od-drip 1.8s ease-in infinite;animation-delay:var(--d)}
@keyframes od-drip{0%{transform:translateY(-4px);opacity:0}20%{opacity:1}100%{transform:translateY(20px);opacity:0}}
.op-txt{display:flex;flex-direction:column;align-items:center;gap:6px;min-width:0;width:100%}
.op-pn{display:inline-flex;align-items:center;gap:6px;font-family:'Bebas Neue',sans-serif;font-size:22px;line-height:1;white-space:nowrap;overflow-wrap:normal !important;max-width:100%}
.op-pn svg{flex-shrink:0;width:16px;height:16px}
.op-hl{font-size:13px;line-height:1.45;color:var(--ink)}
.op-valve[data-s=none] .op-hl,.op-valve[data-s=empty] .op-hl,.op-valve[data-s=none] .op-pn,.op-valve[data-s=empty] .op-pn{color:var(--mut)}
.op-valve .od-st{white-space:normal;text-align:center}
.op-prog{font-size:12px;font-weight:600;color:var(--mut)}
.op-line.is-empty .op-pipe{border-style:dashed;border-color:var(--grey);background:transparent}
.op-key .k-wheel{border-radius:50%;border:2px solid var(--ink);background:conic-gradient(var(--hi) 0 40%,transparent 0)}
.op-key .k-drop{border:0;background:var(--hi);border-radius:50% 50% 50% 50%/60% 60% 40% 40%}
.op-desk{margin-top:18px}
.op-bh{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.op-fig{display:flex;flex-direction:column;gap:3px;font-size:12.5px;color:var(--mut)}
.op-fv{font-family:'Bebas Neue',sans-serif;font-size:30px;line-height:1;color:var(--ink)}
@media (prefers-reduced-motion:reduce){.op-drip{animation:none;opacity:.9;transform:translateY(calc(var(--x) * .3 + 8px))}}
@container lp (max-width:699px){
 .oh-top{grid-template-columns:1fr;gap:18px;margin:22px 0 4px}
 .oh-mv{font-size:46px}
 .op-line{grid-template-columns:1fr;padding:16px 12px}
 .op-pipe{left:42px;right:auto;top:60px;bottom:60px;width:16px;height:auto}
 .op-end{flex-direction:row;text-align:left;gap:12px;padding-left:20px}
 .op-end b{font-size:13.5px}
 .op-valves{grid-template-columns:1fr;gap:6px}
 .op-valve{flex-direction:row;align-items:flex-start;text-align:left;gap:12px;padding:8px 10px}
 .op-wrap{height:auto;flex-direction:row;align-items:center;flex-shrink:0;width:86px}
 .op-wheel{width:52px;height:52px}
 .op-drips{flex-shrink:0;width:30px;height:36px;transform:rotate(-90deg)}
 .op-txt{align-items:flex-start}
 .op-valve .sel-chev{margin-top:10px}
 .op-valves .bx-mob{margin:6px 0 10px 0}
 .op-valves .bx-mob::before{left:40px}
}
'''

# ==========================================================================================
# DIAGNOSIS · the sieve
DG = {
 'filled': {
  'claim': 'Most patients leave with the slip in their hand',
  'deck': 'Two of five steps done. We followed 100 tests from the doctor’s desk. The biggest loss comes when no scan slot is free the same day.',
  'rows': [
   {'label': 'Test written by the doctor', 'n': 100, 'why': None, 'tag': 'example',
    'found': 'We start with 100 tests written in one morning. Doctors write them for almost every new patient and for many returning ones.',
    'points': 'The doctors are writing the tests. Prescribing is not the problem.'},
   {'label': 'Patient told where to go next', 'n': 74, 'why': 'Left with the slip. No one told them where the test room is.', 'tag': 'guess', 'pt': 2,
    'found': 'At the busy hours, the desk staff take payment and point to the next counter. About 1 patient in 4 leaves without being told what to do next.',
    'points': 'Staff in the busy hours. The desk has no time beyond billing.'},
   {'label': 'Offered a slot the same day', 'n': 41, 'why': 'No scan slot free today. Asked to come back.', 'tag': 'guess', 'pt': 4,
    'found': 'Scans are booked one after another. No slot is kept free for a patient who walks in from the doctor’s room, so MRI and CT patients are asked to return.',
    'points': 'How scans are booked. This is where most tests are lost.'},
   {'label': 'Test done here', 'n': 19, 'why': 'Went to an outside lab, or did not do the test at all.', 'tag': 'example',
    'found': 'Of the patients asked to come back, most do the test at an outside centre near home. Some never do it.',
    'points': 'Patients sent elsewhere. Still to check whether anyone points them outside.'},
   {'label': 'Report back to the doctor', 'n': 17, 'why': 'Report reached the doctor after the patient’s next visit.', 'tag': 'guess',
    'found': 'A few reports reach the doctor late. The doctor then trusts the hospital’s own reports a little less.',
    'points': 'Small for now. We will check the time a report takes.'},
  ],
  'causes': [
   {'name': 'Staff in the busy hours', 'w': 3, 'state': 'Being checked', 'pt': 2},
   {'name': 'How scans are booked', 'w': 4, 'state': 'Leading so far', 'lead': True, 'pt': 4},
   {'name': 'How the desk works', 'w': 2, 'state': 'Some signs'},
   {'name': 'Patients sent elsewhere', 'w': 1, 'state': 'Not checked yet'},
  ],
  'pending': [
   {'text': 'Count the desk staff and the bills they make each hour.', 'need': 'Needs your staff list for the outpatient desk', 'pt': 2},
   {'text': 'Find out who books scans, and what happens when an urgent case comes in.', 'need': 'Needs a word with your scan room in-charge', 'pt': 4},
   {'text': 'Check whether doctors are full-time or part-time, and how they are paid.'},
   {'text': 'Name the main cause, so the fixes start in the right place.'},
  ],
  'actions': {'go': {'detail': 'Check the desk staff in the busy hours', 'say': 'Let’s check the desk staff in the busy hours'},
              'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about how tests are lost: '},
              'jump': {'tab': 'Solutions', 'detail': 'See the four fixes so far', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['Diagnosis is two of five steps in.', 'Of 100 tests written, about 19 are done here. Most are lost when no scan slot is free the same day.'],
           'pointer': 'Pick a point to add to it, or tap a step of the sieve.',
           'note': 'The doctor writes the test. The booking lets it go.',
           'points': [{'n': 1, 'label': 'The leak, in rupees'}, {'n': 2, 'label': 'Patients not told where to go'},
                      {'n': 3, 'label': 'The four causes'}, {'n': 4, 'label': 'No same-day scan slot'}],
           'prompts': ['Our desk has four staff each shift', 'How sure are these numbers?', 'Let’s look at scan booking']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Tojo follows 100 tests from the doctor’s desk to the report, and shows where patients drop out.',
  'rows': [{'label': l} for l in ['Test written by the doctor', 'Patient told where to go next', 'Offered a slot the same day', 'Test done here', 'Report back to the doctor']],
  'causes': [{'name': n} for n in ['Staff in the busy hours', 'How scans are booked', 'How the desk works', 'Patients sent elsewhere']],
  'pending': [
   {'text': 'Follow one prescription, from the doctor writing it to the test being done.'},
   {'text': 'Put a number on the tests that leave each day.', 'need': 'Needs a week of outpatient numbers'},
   {'text': 'Find out whether every prescription is recorded today.'},
  ],
  'actions': {'go': {'detail': 'Follow one prescription with Tojo', 'say': 'Let’s follow one prescription'},
              'add': {'detail': 'Share a report or a bill list', 'say': 'Here is what I already know about our tests: '},
              'jump': {'tab': 'Solutions', 'detail': 'Fills in once the cause is named', 'say': 'Take me to Solutions'}},
  'chat': {'text': ['This is Diagnosis. We find out where prescribed tests are lost.', 'We start by following one prescription from the doctor’s desk.'],
           'note': 'Start with one slip.', 'points': [],
           'prompts': ['Let’s follow one prescription', 'We do not track prescriptions', 'What should I bring?']},
 },
}

def dg_canvas(state):
    d = DG[state]; empty = state == 'empty'
    rows, desk = [], []
    for i, r in enumerate(d['rows']):
        k = str(i); first = i == 0 and not empty
        if empty:
            rows.append('<div class="ds-row is-empty"><span class="ds-n">?</span><span class="ds-l">%s</span><span class="ds-bar"><i></i></span></div>' % e(r['label']))
            continue
        lost = d['rows'][i - 1]['n'] - r['n'] if i else 0
        why = ('<span class="ds-why"><i class="ds-dot" aria-hidden="true"></i><b>%d lost</b> %s</span>' % (lost, e(r['why']))) if r['why'] else '<span class="ds-why ds-start">The start: every test the doctors wrote</span>'
        rows.append(('<button class="ds-row %s" type="button"%s%s><span class="ds-n">%d</span><span class="ds-main"><span class="ds-l">%s</span>'
                     '<span class="ds-bar"><i style="width:%d%%"></i></span>%s</span>%s</button>') % (
            sel_cls(first), sel('ds', k, first), pt(r.get('pt')), r['n'], e(r['label']), r['n'], why, CHEV))
        det = ('<div class="od-box"><div class="op-bh"><h4>%s</h4>%s</div><div class="od-two"><div><span class="od-lab">What we found</span><p>%s</p></div>'
               '<div><span class="od-lab">What it points to</span><p>%s</p></div></div></div>') % (
            e(r['label']), tag(r['tag']), e(r['found']), e(r['points']))
        rows.append(box('ds', k, det, first, 'mob'))
        desk.append(box('ds', k, det, first, 'desk'))
    sieve = '<div class="ds-sieve">%s</div>' % ''.join(rows)
    if not empty:
        sieve += '<div class="ds-desk">%s</div>' % ''.join(desk)
    sub = 'One hundred tests written. Each row shows how many are left. Tap a row.' if not empty else 'Fills in as we follow one prescription'
    # the four causes, weighed
    cs = []
    for c in d['causes']:
        if empty:
            cs.append('<div class="dc-c is-empty"><span class="dc-n">%s</span><span class="dc-w">%s</span><span class="dc-s">Not weighed yet</span></div>' % (
                e(c['name']), ''.join('<i></i>' for _ in range(5))))
        else:
            cs.append('<div class="dc-c%s"%s><span class="dc-n">%s</span><span class="dc-w" aria-label="%d of 5">%s</span><span class="dc-s">%s</span></div>' % (
                ' is-lead' if c.get('lead') else '', pt(c.get('pt')), e(c['name']), c['w'],
                ''.join('<i class="on"></i>' if j < c['w'] else '<i></i>' for j in range(5)), e(c['state'])))
    causes = '<div class="dc-grid"%s>%s</div><p class="bm-hint">%s</p>' % (
        pt(3) if not empty else '', ''.join(cs),
        'Each dot is one piece of evidence. The main cause is named once the scan booking is checked.' if not empty else 'Tojo weighs each cause as the evidence comes in.')
    return (masthead(KICK, 'Diagnosis', emblem(ico_path('Diagnosis')), STAMP[state]) + standing(d['claim'], d['deck'], empty)
            + section('The sieve', sieve, 'ds-sec', sub)
            + section('Which cause leads so far', causes, 'dc-sec', 'Four possible main causes')
            + pending(d['pending']) + actions(d['actions']))

def ico_path(name):
    return ICONS[name]

DG_CSS = '''
.ds-sieve{display:flex;flex-direction:column;gap:8px;padding:18px;border:3px solid var(--ink);border-radius:14px;background:var(--card);
  background-image:repeating-linear-gradient(90deg,transparent 0 calc(10% - 1px),var(--gridc) calc(10% - 1px) 10%)}
.ds-row{display:grid;grid-template-columns:64px minmax(0,1fr) auto;align-items:center;gap:14px;width:100%;padding:10px 12px;border:1.5px solid transparent;border-radius:10px;background:transparent;text-align:left}
.lp .ds-row.is-up{background:var(--soft);border-color:var(--ink)}
.ds-n{font-family:'Bebas Neue',sans-serif;font-size:40px;line-height:1;text-align:right}
.ds-main{display:flex;flex-direction:column;gap:6px;min-width:0}
.ds-l{font-size:15px;font-weight:600}
.ds-bar{display:block;height:16px;border-radius:3px;background:repeating-linear-gradient(90deg,var(--line) 0 2px,transparent 2px 10%);border:1.5px solid var(--ink);overflow:hidden}
.ds-bar i{display:block;height:100%;background:var(--ink);box-shadow:inset -5px 0 0 var(--hi)}
.ds-why{display:flex;align-items:baseline;gap:8px;font-size:13px;color:var(--mut);line-height:1.4}
.ds-why b{color:var(--hi);font-weight:700;white-space:nowrap}
.ds-dot{flex-shrink:0;width:9px;height:11px;background:var(--hi);border-radius:50% 50% 50% 50%/60% 60% 40% 40%;clip-path:polygon(50% 0,100% 55%,100% 100%,0 100%,0 55%);transform:translateY(1px)}
.ds-start{font-style:italic}
.ds-row .sel-chev{display:inline-block}
.ds-row.is-empty{grid-template-columns:64px minmax(0,1fr) minmax(0,1.2fr);cursor:default;color:var(--mut)}
.ds-row.is-empty .ds-n{color:var(--grey)}
.ds-row.is-empty .ds-bar i{display:none}
.ds-row.is-empty .ds-bar{border-style:dashed;border-color:var(--grey);background:none}
.ds-desk{margin-top:16px}
.dc-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.dc-c{display:flex;flex-direction:column;gap:8px;padding:14px 16px;border:2px solid var(--ink);border-radius:12px;background:var(--card);min-width:0}
.dc-c.is-lead{background:var(--ink);color:var(--card);box-shadow:0 6px 0 -2px var(--hi)}
.dc-n{font-size:14.5px;font-weight:600;line-height:1.35}
.dc-w{display:flex;gap:5px}.dc-w i{width:14px;height:14px;border-radius:50%;border:2px solid currentColor}.dc-w i.on{background:var(--hi);border-color:var(--hi)}
.dc-s{font-size:12.5px;font-weight:600;color:var(--mut)}.dc-c.is-lead .dc-s{color:var(--hi)}
.dc-c.is-empty{border-style:dashed;border-color:var(--grey);color:var(--mut);background:transparent}
@container lp (max-width:699px){
 .ds-sieve{padding:10px}
 .ds-row{grid-template-columns:46px minmax(0,1fr) auto;gap:10px;padding:10px 8px}
 .ds-n{font-size:32px}
 .ds-l{font-size:14px}
 .ds-row.is-empty{grid-template-columns:46px minmax(0,1fr)}
 .ds-row.is-empty .ds-bar{grid-column:1/-1}
 .dc-grid{grid-template-columns:1fr 1fr}
 .ds-sieve .bx-mob{margin:4px 0 8px}
}
'''

# ==========================================================================================
# SOLUTIONS · the prescription pad
STOPS = ['Idea', 'Shaped', 'Tested with you', 'Agreed']
PATH = {'ready': 'Ready', 'draft': 'Drafted', 'none': 'Not yet'}
SO = {
 'filled': {
  'claim': 'Four fixes, each with a by-hand and an automatic version',
  'deck': 'One fix is taking shape. None is agreed yet. Every fix works by hand first, so the hospital can start without any new software.',
  'fixes': [
   {'name': 'Record every prescription', 'stage': 1, 'pt': 1, 'hand': 'draft', 'auto': 'draft',
    'what': 'Every prescription is scanned at the desk. Its tests and their value are written down, so the tests that leave can be counted each day.',
    'by_hand': 'A desk executive scans each slip and types its tests into a sheet. The sheet is matched with the day’s bills each evening.',
    'by_auto': 'A helper reads the scanned slip, lists its tests, and works out their value from the hospital’s price list.',
    'needs': ['A scanner at each outpatient desk', 'Doctors and their secretaries agreeing to share every slip']},
   {'name': 'Walk each patient to the test desk', 'stage': 0, 'pt': 2, 'hand': 'draft', 'auto': 'none',
    'what': 'A guest services person takes each patient from the doctor’s room to the test desk, and stays until the test is booked.',
    'by_hand': 'Guest services staff on the floor in the busy hours, sized to the number of patients each hour.',
    'by_auto': 'A phone helper tells the patient the wait, the queue and the room, and calls a staff member when asked.',
    'needs': ['A count of guest services staff per hour', 'The busy hours, from your desk records']},
   {'name': 'Keep urgent scan slots free, then fill them', 'stage': 0, 'pt': 3, 'hand': 'draft', 'auto': 'none',
    'what': 'Some scan slots are kept free for urgent cases. If no urgent case comes by that time, the next outpatient moves up into the slot.',
    'by_hand': 'The scan room keeps a written slot plan. The in-charge moves the next patient up at the slot time.',
    'by_auto': 'A booking helper holds the free slots and moves the next patient up by itself.',
    'needs': ['A word with the scan room in-charge', 'Radiologists agreeing not to change the order']},
   {'name': 'Share yesterday’s numbers every morning', 'stage': 0, 'hand': 'none', 'auto': 'none',
    'what': 'Each morning, every department, specialty and doctor sees the tests written and the tests done here the day before. Numbers only, no praise or blame.',
    'by_hand': 'The desk manager pins one sheet at 8 AM and sends it on the staff group.',
    'by_auto': 'A helper sends the sheet at 8 AM to every department.',
    'needs': ['The management team agreeing to share the numbers openly']},
  ],
  'pending': [
   {'text': 'Shape the second fix: how many guest services staff in each busy hour.', 'need': 'Needs your patients per hour', 'pt': 2},
   {'text': 'Test the first fix with you: who scans the slip, and when.', 'pt': 1},
   {'text': 'Check that each fix also works with no new software.'},
  ],
  'actions': {'go': {'detail': 'Test fix 1 with you', 'say': 'Let’s test the first fix: recording every prescription'},
              'add': {'detail': 'Suggest a fix of your own', 'say': 'I have an idea for a fix: '},
              'jump': {'tab': 'Automations', 'detail': 'See the helpers for these fixes', 'say': 'Take me to Automations'}},
  'chat': {'text': ['Four fixes are written up. The first is taking shape: record every prescription.', 'Each fix has a by-hand version, so you can start without new software.'],
           'pointer': 'Pick a point to add to it, or tap a fix on the pad.',
           'note': 'Count every slip first. The rest builds on it.',
           'points': [{'n': 1, 'label': 'Record every prescription'}, {'n': 2, 'label': 'Walk patients to the test desk'},
                      {'n': 3, 'label': 'Urgent scan slots'}],
           'prompts': ['We already scan some slips', 'Why record every prescription?', 'Let’s test fix 1']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'The fixes are written here once Diagnosis names the main cause. Each one will come with a by-hand and an automatic version.',
  'fixes': [], 'pending': [
   {'text': 'Name the main cause in Diagnosis first.'},
   {'text': 'Write the first fix, with its by-hand version.'},
  ],
  'actions': {'go': {'detail': 'Name the main cause first', 'say': 'Let’s name the main cause'},
              'add': {'detail': 'Suggest a fix of your own', 'say': 'I have an idea for a fix: '},
              'jump': {'tab': 'Automations', 'detail': 'Fills in once a fix is agreed', 'say': 'Take me to Automations'}},
  'chat': {'text': ['This is Solutions. The fixes are written here once the main cause is named.'],
           'note': 'A fix waits for its cause.', 'points': [],
           'prompts': ['Take me back to Diagnosis', 'What kind of fixes come up?', 'Can I suggest a fix?']},
 },
}

def so_canvas(state):
    d = SO[state]; empty = state == 'empty'
    lines, desk = [], []
    for i, f in enumerate(d['fixes']):
        k = str(i); first = i == 0
        ticks = ''.join('<span class="rx-t%s"><i aria-hidden="true"></i>%s</span>' % (' on' if j <= f['stage'] else '', e(s)) for j, s in enumerate(STOPS))
        paths = ('<span class="rx-paths"><span class="rx-p p-%s">By hand: %s</span><span class="rx-p p-%s">Automatic: %s</span></span>') % (
            f['hand'], PATH[f['hand']], f['auto'], PATH[f['auto']])
        lines.append(('<button class="rx-line %s" type="button"%s%s><span class="rx-no">%d</span><span class="rx-main"><b class="rx-name">%s</b>'
                      '<span class="rx-ticks">%s</span>%s</span>%s</button>') % (
            sel_cls(first), sel('rx', k, first), pt(f.get('pt')), i + 1, e(f['name']), ticks, paths, CHEV))
        det = ('<div class="od-box"><h4>%s</h4><p>%s</p><div class="od-two rx-two"><div class="rx-way"><span class="od-lab">By hand</span><p>%s</p></div>'
               '<div class="rx-way rx-auto"><span class="od-lab">Automatic</span><p>%s</p></div></div>'
               '<div><span class="od-lab">What it relies on</span><ul class="od-bul">%s</ul></div></div>') % (
            e(f['name']), e(f['what']), e(f['by_hand']), e(f['by_auto']), ''.join('<li>%s</li>' % e(x) for x in f['needs']))
        lines.append(box('rx', k, det, first, 'mob'))
        desk.append(box('rx', k, det, first, 'desk'))
    if empty:
        lines = ['<div class="rx-blank"><span></span><span></span><span></span><p>Fixes are written here once the main cause is named.</p></div>']
    agreed = sum(1 for f in d['fixes'] if f['stage'] == 3)
    pad = ('<div class="rx-pad"><div class="rx-head"><div><span class="rx-hk">Fixes for</span><b>%s</b></div><span class="rx-date">%s</span></div>'
           '<div class="rx-lines%s">%s</div><div class="rx-foot"><span class="rx-sign">%s</span><span class="rx-stamp">%s</span></div></div>') % (
        e(C.HOSPITAL), 'Written up 7 October' if not empty else 'Not written yet', ' is-empty' if empty else '', ''.join(lines),
        'Agreed with you', ('%d of %d agreed' % (agreed, len(d['fixes']))) if not empty else 'None yet')
    body = pad + ('<div class="rx-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'One line for each fix. Its four stops are ticked as it moves. Tap a line.' if not empty else 'One line for each fix'
    return (masthead(KICK, 'Solutions', emblem(ICONS['Solutions']), STAMP[state]) + standing(d['claim'], d['deck'], empty)
            + section('The prescription pad', body, 'rx-sec', sub) + pending(d['pending']) + actions(d['actions']))

SO_CSS = '''
.rx-pad{position:relative;max-width:900px;background:var(--card);border:2.5px solid var(--ink);border-radius:6px 6px 14px 14px;padding:0 0 18px;
  box-shadow:8px 8px 0 var(--line)}
.rx-pad::before{content:"";position:absolute;left:0;right:0;top:-2.5px;height:12px;background:var(--ink);border-radius:6px 6px 0 0}
.rx-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;padding:26px 26px 14px;border-bottom:2px solid var(--ink);flex-wrap:wrap}
.rx-hk{display:block;font-size:12px;font-weight:600;color:var(--mut)}
.rx-head b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:28px;line-height:1}
.rx-date{font-family:'Caveat',cursive;font-size:22px;color:var(--mut)}
.rx-lines{position:relative;display:flex;flex-direction:column;padding:6px 14px 0 14px}
.rx-lines::before{content:"";position:absolute;left:66px;top:0;bottom:0;width:2px;background:var(--hi-soft);border-left:1.5px solid var(--hi);opacity:.55}
.rx-line{position:relative;display:grid;grid-template-columns:46px minmax(0,1fr) auto;gap:14px;align-items:start;width:100%;padding:14px 12px;border:0;border-bottom:1.5px dashed var(--line);background:transparent;text-align:left;border-radius:8px}
.lp .rx-line.is-up{background:var(--soft)}
.rx-no{font-family:'Caveat',cursive;font-size:38px;font-weight:700;line-height:.9;color:var(--hi);text-align:center}
.rx-main{display:flex;flex-direction:column;gap:9px;min-width:0}
.rx-name{font-size:16.5px;font-weight:600;line-height:1.35}
.rx-ticks{display:flex;flex-wrap:wrap;gap:6px 14px}
.rx-t{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;color:var(--mut)}
.rx-t i{width:16px;height:16px;border:2px solid var(--ink);border-radius:3px;position:relative}
.rx-t.on{color:var(--ink);font-weight:600}
.rx-t.on i{background:var(--ink)}.rx-t.on i::after{content:"";position:absolute;left:3.5px;top:0;width:5px;height:9px;border:solid var(--card);border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}
.rx-paths{display:flex;flex-wrap:wrap;gap:8px}
.rx-p{font-size:12px;font-weight:600;padding:3px 10px;border-radius:12px;border:1.5px solid var(--ink)}
.rx-p.p-ready{background:var(--hi);border-color:var(--hi);color:#fff}
.rx-p.p-draft{background:var(--hi-soft);border-color:var(--hi)}
.rx-p.p-none{border-style:dashed;border-color:var(--grey);color:var(--mut)}
.rx-line .sel-chev{display:inline-block;margin-top:8px}
.rx-foot{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;padding:22px 26px 0;flex-wrap:wrap}
.rx-sign{min-width:200px;border-top:1.5px solid var(--ink);padding-top:6px;font-size:12px;font-weight:600;color:var(--mut)}
.rx-stamp{font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:.04em;color:var(--hi);border:2.5px solid var(--hi);border-radius:6px;padding:2px 12px;transform:rotate(-4deg)}
.rx-two .rx-way{padding:12px 14px;border-radius:10px;background:var(--soft)}
.rx-two .rx-auto{background:var(--hi-soft)}
.rx-desk{margin-top:26px;max-width:900px}
.rx-lines.is-empty::before{display:none}
.rx-blank{display:flex;flex-direction:column;gap:22px;padding:24px 12px}
.rx-blank span{display:block;height:2px;border-top:2px dashed var(--grey)}
.rx-blank p{font-size:14px;color:var(--mut)}
@container lp (max-width:699px){
 .rx-pad{box-shadow:4px 4px 0 var(--line)}
 .rx-head{padding:22px 16px 12px}
 .rx-lines{padding:4px 6px 0}
 .rx-line{grid-template-columns:30px minmax(0,1fr) auto;gap:10px;padding:12px 6px}
 .rx-no{font-size:32px}
 .rx-name{font-size:15px}
 .rx-foot{padding:18px 16px 0}
 .rx-sign{min-width:0;flex:1 1 140px}
 .rx-lines .bx-mob{margin:6px 0 10px}
}
'''

# ==========================================================================================
# AUTOMATIONS · one patient's visit
STATIONS = ['Arrives', 'Sees the doctor', 'Pays and books', 'Test room', 'Report to the doctor', 'Goes home', 'Next morning']
LAMPS = ['Idea', 'Built', 'Tested', 'Switched on']
AU = {
 'filled': {
  'claim': 'Four helpers, placed where they act in a patient’s visit',
  'deck': 'All four are ideas for now. They wait for the fixes to be agreed. Each one speeds up a by-hand step that works without it.',
  'helpers': [
   {'name': 'Prescription reader', 'from': 1, 'to': 2, 'stage': 0, 'pt': 1,
    'does': 'Reads each scanned prescription, lists its tests, and works out their value from the price list. Keeps a running count of tests not done here.',
    'when': 'The moment the slip is scanned at the desk', 'needs': ['A scanner at each outpatient desk', 'The hospital’s price list, kept up to date'],
    'hand': 'A desk executive types each slip into a sheet.'},
   {'name': 'Booking helper', 'from': 2, 'to': 3, 'stage': 0, 'pt': 2,
    'does': 'Books the test straight from the prescription once staff confirm it. Holds urgent slots free and moves the next patient up when no urgent case comes.',
    'when': 'While the patient is at the desk', 'needs': ['The prescription reader', 'A slot plan for each scan machine, one machine at a time'],
    'hand': 'The scan room in-charge keeps a written slot plan.'},
   {'name': 'Visit companion', 'from': 0, 'to': 5, 'stage': 0, 'pt': 3,
    'does': 'On the patient’s phone for the whole visit. Shows the wait and the queue, calls them when their slot comes, calls staff or a wheelchair when asked, and tells the parking attendant to bring the car round.',
    'when': 'From arrival to going home', 'needs': ['A phone number taken at the desk', 'Staff phones that get the calls'],
    'hand': 'Guest services staff walk the patient through the visit.'},
   {'name': 'Morning numbers', 'from': 5, 'to': 6, 'span': 'Every morning at 8 AM', 'stage': 0,
    'does': 'Sends yesterday’s tests written and tests done here, by department, specialty and doctor. Numbers only, no praise or blame.',
    'when': 'Every morning at 8 AM', 'needs': ['The prescription reader', 'The management team agreeing to share the numbers'],
    'hand': 'The desk manager pins one sheet at 8 AM.'},
  ],
  'pending': [
   {'text': 'Find out what software the desks use for prescriptions and bills today.', 'need': 'Needs a word with your IT team', 'pt': 1},
   {'text': 'Check whether any scanning or booking was tried before.'},
   {'text': 'Pick which helper is built first, once the fixes are agreed.'},
  ],
  'actions': {'go': {'detail': 'Find out what software you use', 'say': 'Let’s look at the software our desks use today'},
              'add': {'detail': 'Tell Tojo about a system', 'say': 'Our desks use this software: '},
              'jump': {'tab': 'Processes', 'detail': 'See the changes for people', 'say': 'Take me to Processes'}},
  'chat': {'text': ['Four helpers are placed on a patient’s visit, where each one acts.', 'All four wait for the fixes to be agreed. Each speeds up a by-hand step.'],
           'pointer': 'Pick a point to add to it, or tap a helper on the visit.',
           'note': 'Each helper speeds up a step that already works by hand.',
           'points': [{'n': 1, 'label': 'The prescription reader'}, {'n': 2, 'label': 'The booking helper'}, {'n': 3, 'label': 'The visit companion'}],
           'prompts': ['We tried a scanning app once', 'Which helper comes first?', 'Do we need new software?']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'Helpers are placed on a patient’s visit once a fix is agreed. Each one speeds up a step that also works by hand.',
  'helpers': [],
  'pending': [{'text': 'Agree a fix in Solutions first.'}, {'text': 'Find out what software the desks use today.'}],
  'actions': {'go': {'detail': 'Agree a fix first', 'say': 'Take me to the fixes'},
              'add': {'detail': 'Tell Tojo about a system', 'say': 'Our desks use this software: '},
              'jump': {'tab': 'Processes', 'detail': 'Fills in once a fix is agreed', 'say': 'Take me to Processes'}},
  'chat': {'text': ['This is Automations. Helpers are placed on a patient’s visit once a fix is agreed.'],
           'note': 'Fix the step by hand first.', 'points': [],
           'prompts': ['Take me to the fixes', 'What can be automatic?', 'Do we need new software?']},
 },
}

def au_canvas(state):
    d = AU[state]; empty = state == 'empty'
    stn = ''.join('<span class="av-stn%s" style="grid-column:%d"><i aria-hidden="true"></i>%s</span>' % (' av-next' if j == 6 else '', j + 1, e(s)) for j, s in enumerate(STATIONS))
    toks, desk = [], []
    for i, h in enumerate(d['helpers']):
        k = str(i); first = i == 0
        lamps = ''.join('<span class="av-l%s"><i aria-hidden="true"></i>%s</span>' % (' on' if j <= h['stage'] else '', e(s)) for j, s in enumerate(LAMPS))
        span = h.get('span') or '%s to %s' % (STATIONS[h['from']], STATIONS[h['to']].lower())
        toks.append(('<button class="av-tok %s" type="button" style="--a:%d;--b:%d;--r:%d"%s%s><span class="av-tn"><b>%s</b><em>%s</em></span>'
                     '<span class="av-state">Idea</span>%s</button>') % (
            sel_cls(first), h['from'] + 1, h['to'] + 2, i + 1, sel('av', k, first), pt(h.get('pt')), e(h['name']), e(span), CHEV))
        det = ('<div class="od-box"><h4>%s</h4><p>%s</p><div class="av-lamps">%s</div><div class="od-two"><div><span class="od-lab">When it runs</span><p>%s</p></div>'
               '<div><span class="od-lab">What it needs first</span><ul class="od-bul">%s</ul></div></div>'
               '<p class="av-hand"><b>Without it:</b> %s</p></div>') % (
            e(h['name']), e(h['does']), lamps, e(h['when']), ''.join('<li>%s</li>' % e(x) for x in h['needs']), e(h['hand']))
        toks.append(box('av', k, det, first, 'mob'))
        desk.append(box('av', k, det, first, 'desk'))
    if empty:
        toks = ['<div class="av-ghost" style="--a:1;--b:8">Helpers are placed here once a fix is agreed</div>']
    board = ('<div class="av-board"><div class="av-route">%s<span class="av-path" aria-hidden="true"></span></div><div class="av-toks">%s</div></div>') % (stn, ''.join(toks))
    body = board + ('<div class="av-desk">%s</div>' % ''.join(desk) if desk else '')
    sub = 'A patient’s visit, left to right. Each helper sits over the steps where it acts. Tap a helper.' if not empty else 'A patient’s visit, left to right'
    return (masthead(KICK, 'Automations', emblem(ICONS['Automations']), STAMP[state]) + standing(d['claim'], d['deck'], empty)
            + section('One patient’s visit', body, 'av-sec', sub) + pending(d['pending']) + actions(d['actions']))

AU_CSS = '''
.av-board{padding:22px 18px 20px;border:3px solid var(--ink);border-radius:14px;background:var(--card)}
.av-route,.av-toks{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));column-gap:8px}
.av-route{position:relative;align-items:start;padding-bottom:18px;border-bottom:2px dashed var(--line);margin-bottom:16px}
.av-path{position:absolute;left:calc(100% / 14);right:calc(100% / 7 + 100% / 14);top:9px;height:4px;background:var(--ink);border-radius:2px;z-index:0}
.av-stn{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:8px;font-size:12.5px;font-weight:600;text-align:center;line-height:1.3}
.av-stn i{width:22px;height:22px;border-radius:50%;background:var(--card);border:4px solid var(--ink)}
.av-next{color:var(--mut)}.av-next i{border-style:dashed;border-color:var(--grey)}
.av-toks{row-gap:10px;align-items:start}
.av-tok{grid-column:var(--a)/var(--b);grid-row:var(--r);display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 14px;border:2px solid var(--ink);border-radius:999px;background:var(--soft);text-align:left;min-width:0}
.lp .av-tok.is-up{background:var(--ink);color:var(--card)}
.av-tn{display:flex;flex-direction:column;min-width:0}
.av-tn b{font-size:14px;line-height:1.25}.av-tn em{font-style:normal;font-size:12px;color:var(--mut)}
.av-tok.is-up .av-tn em{color:var(--line)}
.av-state{font-size:11.5px;font-weight:600;padding:2px 9px;border-radius:10px;border:1.5px dashed currentColor;white-space:nowrap}
.av-tok .sel-chev{display:none}
.av-ghost{grid-column:var(--a)/var(--b);padding:14px;border:2px dashed var(--grey);border-radius:999px;text-align:center;font-size:13.5px;color:var(--mut)}
.av-lamps{display:flex;flex-wrap:wrap;gap:8px 16px}
.av-l{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;color:var(--mut)}
.av-l i{width:14px;height:14px;border-radius:50%;border:2px solid var(--ink)}
.av-l.on{color:var(--ink);font-weight:600}.av-l.on i{background:var(--hi);border-color:var(--hi);box-shadow:0 0 0 3px var(--hi-soft)}
.av-hand{font-size:13.5px;padding:10px 12px;border-radius:8px;background:var(--soft)}
.av-desk{margin-top:18px}
@container lp (max-width:699px){
 .av-board{padding:14px 10px}
 .av-route{grid-template-columns:1fr;row-gap:0;padding-bottom:10px}
 .av-stn{grid-column:1 !important;flex-direction:row;gap:12px;text-align:left;padding:6px 0 6px 6px}
 .av-path{left:15px;right:auto;top:14px;bottom:24px;width:4px;height:auto}
 .av-toks{grid-template-columns:1fr}
 .av-tok,.av-ghost{grid-column:1 / -1;grid-row:auto;border-radius:14px}
 .av-tok .sel-chev{display:inline-block}
 .av-toks .bx-mob{margin:4px 0 8px}
}
'''

# ==========================================================================================
# PROCESSES · the busy-hours board
HOURS = ['8 AM', '9', '10', '11', '12 PM', '1', '2', '3', '4', '5', '6', '7 PM']
PR = {
 'filled': {
  'claim': 'The desk is short-staffed for four hours a day',
  'deck': 'Worked out from your example numbers: most bills come between 9 AM and 1 PM. Four process changes and one new role are drafted. None is tried yet.',
  'bills': [12, 108, 112, 110, 110, 16, 14, 14, 14, 14, 14, 12],
  'can': 68,
  'changes': [
   {'n': 1, 'name': 'Scan every prescription at the desk', 'short': 'Scan every slip, all day', 'at': 0, 'span': 12, 'state': 'Drafted', 'pt': 1,
    'what': 'Every slip is scanned before the bill is made, all day.',
    'how': ['The desk executive scans the slip first, then bills', 'Its tests are typed in by hand, or read by the helper', 'Matched with the day’s bills each evening']},
   {'n': 2, 'name': 'Guest services in the busy hours', 'short': 'Guest services', 'at': 1, 'span': 4, 'state': 'Drafted', 'pt': 2,
    'what': 'Guest services staff walk patients from the doctor to the test desk between 9 AM and 1 PM.',
    'how': ['Sized to patients per hour, with 5 to 10 minutes per patient', 'Stays with the patient until the test is booked', 'Calls a wheelchair for the 1 in 20 who need help']},
   {'n': 3, 'name': 'Urgent scan slots kept free, then filled', 'short': 'Urgent scan slots, all day', 'at': 0, 'span': 12, 'state': 'Idea',
    'what': 'Free slots through the day for urgent cases. The next outpatient moves up if no urgent case comes.',
    'how': ['One slot plan for each scan machine', 'A slot booked for a ward patient never moves', 'No patient is pushed back for an urgent case']},
   {'n': 4, 'name': 'Yesterday’s numbers at 8 AM', 'short': '8 AM', 'at': 0, 'span': 1, 'state': 'Idea',
    'what': 'Tests written and tests done here, by department, specialty and doctor, shared each morning.',
    'how': ['Numbers only, no praise or blame', 'Good performers are thanked each month, with no bonus scheme', 'The management team agrees to share them openly']},
  ],
  'measures': [
   {'name': 'Patients who finish their tests here', 'now': '2 in 10', 'goal': '5 in 10', 'tag': 'example'},
   {'name': 'Tests booked the same day', 'now': 'Not counted', 'goal': '8 in 10', 'tag': 'goal'},
   {'name': 'Urgent cases that used a free slot', 'now': 'Not counted', 'goal': 'All', 'tag': 'goal'},
   {'name': 'Bills done within the time set, guidance included', 'now': 'No time set', 'goal': 'To agree', 'tag': 'need'},
  ],
  'roles': [
   {'name': 'Scheduling Manager', 'why': 'Needed above 200 outpatients a day. You see about 440.', 'state': 'New role', 'pt': 3},
   {'name': 'Guest services staff', 'why': 'Sized to the busy hours, 9 AM to 1 PM.', 'state': 'Count to agree'},
   {'name': 'Desk executives', 'why': 'Trained to guide each patient, not only to bill.', 'state': 'Training'},
  ],
  'pending': [
   {'text': 'Check the desk count: how many bill at once in the busy hours.', 'need': 'Needs your staff list by shift', 'pt': 2},
   {'text': 'Agree the time a bill should take, including guiding the patient.', 'need': 'Needs your desk manager'},
   {'text': 'Pick one outpatient floor for a two-week trial.'},
  ],
  'actions': {'go': {'detail': 'Check the desk count by shift', 'say': 'Let’s check the desk staff count by shift'},
              'add': {'detail': 'Tell Tojo about your staff', 'say': 'Our outpatient desk staff: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Back to the start', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['Most bills come between 9 AM and 1 PM. In those hours the desk can make about 68 bills an hour, but about 110 are needed.',
                    'Four changes and one new role are drafted.'],
           'pointer': 'Pick a point to add to it, or tap a change.',
           'note': 'Staff ahead of the rush. The tests follow.',
           'points': [{'n': 1, 'label': 'Scan every prescription'}, {'n': 2, 'label': 'Short of staff 9 AM to 1 PM'}, {'n': 3, 'label': 'The Scheduling Manager'}],
           'prompts': ['We have six desk staff in the morning', 'Why add staff before the tests grow?', 'Let’s plan the trial']},
 },
 'empty': {
  'claim': 'Nothing here yet',
  'deck': 'The board fills in with your patients by the hour, the changes, the numbers we watch and the roles, once a fix is agreed.',
  'bills': [], 'can': 0, 'changes': [], 'measures': [], 'roles': [],
  'pending': [{'text': 'Agree a fix in Solutions first.'}, {'text': 'Count patients at the desk by the hour.', 'need': 'Needs one week of desk numbers'}],
  'actions': {'go': {'detail': 'Agree a fix first', 'say': 'Take me to the fixes'},
              'add': {'detail': 'Tell Tojo about your staff', 'say': 'Our outpatient desk staff: '},
              'jump': {'tab': 'Diagnosis', 'detail': 'Back to the start', 'say': 'Take me to Diagnosis'}},
  'chat': {'text': ['This is Processes. The changes for people, the numbers we watch and the roles land here.'],
           'note': 'People first, then the numbers.', 'points': [],
           'prompts': ['Take me to the fixes', 'What changes for the desk staff?', 'Do we need new roles?']},
 },
}

def pr_canvas(state):
    d = PR[state]; empty = state == 'empty'
    if empty:
        chart = ('<div class="pc-chart is-empty"><div class="pc-bars">%s</div><div class="pc-hrs">%s</div><p class="pc-ghost">Fills in with your patients at the desk, hour by hour.</p></div>') % (
            ''.join('<span class="pc-col"><i style="height:%d%%"></i></span>' % h for h in [20, 70, 75, 72, 70, 25, 20, 20, 20, 20, 20, 18]),
            ''.join('<span>%s</span>' % h for h in HOURS))
        body = chart
    else:
        mx = 120.0
        cols = []
        for b in d['bills']:
            ok = min(b, d['can']); over = max(0, b - d['can'])
            cols.append('<span class="pc-col" aria-label="%d bills"><i class="pc-ok" style="height:%.1f%%"></i>%s</span>' % (
                b, 100 * ok / mx, ('<i class="pc-over" style="height:%.1f%%"></i><b>%d</b>' % (100 * over / mx, b)) if over else ''))
        pins = ''.join('<span class="pc-pin%s" style="grid-column:%d / span %d" aria-label="%s"><b>%d</b><span>%s</span></span>' % (
            ' is-short' if c['span'] < 3 else '', c['at'] + 1, c['span'], e(c['name']), c['n'], e(c['short'])) for c in d['changes'])
        chart = ('<div class="pc-chart"%s><div class="pc-plot"><span class="pc-can" style="bottom:%.1f%%"><em>What the desk can do: %d bills an hour</em></span>'
                 '<div class="pc-bars">%s</div></div><div class="pc-hrs">%s</div><div class="pc-pins">%s</div>'
                 '<div class="bm-key"><span><i class="k-ok"></i>Bills the desk can make</span><span><i class="k-over"></i>Bills it cannot keep up with</span>%s</div></div>') % (
            pt(2), 100 * d['can'] / mx, d['can'], ''.join(cols), ''.join('<span>%s</span>' % h for h in HOURS), pins, tag('example'))
        legend, desk = [], []
        for c in d['changes']:
            k = str(c['n']); first = c['n'] == 1
            legend.append('<button class="pc-lg %s" type="button"%s%s><span class="pc-ln">%d</span><span><b>%s</b><em>%s</em></span>%s</button>' % (
                sel_cls(first), sel('pc', k, first), pt(c.get('pt')), c['n'], e(c['name']), e(c['state']), CHEV))
            det = '<div class="od-box"><h4>%s</h4><p>%s</p><div><span class="od-lab">How it will work</span><ul class="od-bul">%s</ul></div></div>' % (
                e(c['name']), e(c['what']), ''.join('<li>%s</li>' % e(x) for x in c['how']))
            legend.append(box('pc', k, det, first, 'mob'))
            desk.append(box('pc', k, det, first, 'desk'))
        reads = ''.join('<div class="pc-read"><span class="pc-rn">%s</span><span class="pc-rv"><b>%s</b><span>now</span></span><span class="pc-rg">Goal: %s</span>%s</div>' % (
            e(m['name']), e(m['now']), e(m['goal']), tag(m['tag'])) for m in d['measures'])
        roles = ''.join('<div class="pc-role"%s><span class="pc-badge" aria-hidden="true"></span><span><b>%s</b><em>%s</em></span><span class="od-st s-later">%s</span></div>' % (
            pt(r.get('pt')), e(r['name']), e(r['why']), e(r['state'])) for r in d['roles'])
        body = ('<div class="pc-top">%s<div class="pc-side"><h4 class="od-lab">The changes</h4>%s</div></div><div class="pc-desk">%s</div>'
                '<div class="pc-low"><div><h4 class="bm-lab">The numbers we will watch</h4><div class="pc-reads">%s</div></div>'
                '<div><h4 class="bm-lab">Team and roles</h4><div class="pc-roles">%s</div></div></div>') % (chart, ''.join(legend), ''.join(desk), reads, roles)
    sub = 'Bills at the outpatient desk, hour by hour. Each change sits under the hours it acts. Tap a change.' if not empty else 'Bills at the outpatient desk, hour by hour'
    return (masthead(KICK, 'Processes', emblem(ICONS['Processes']), STAMP[state]) + standing(d['claim'], d['deck'], empty)
            + section('The busy-hours board', body, 'pc-sec', sub) + pending(d['pending']) + actions(d['actions']))

PR_CSS = '''
.pc-top{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);gap:20px;align-items:start}
.pc-chart{padding:18px 16px 14px;border:3px solid var(--ink);border-radius:14px;background:var(--card);min-width:0}
.pc-plot{position:relative;height:200px}
.pc-bars,.pc-hrs,.pc-pins{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:5px}
.pc-bars{height:100%;align-items:end}
.pc-col{position:relative;display:flex;flex-direction:column-reverse;height:100%;justify-content:flex-start}
.pc-col i{display:block;width:100%}
.pc-ok{background:var(--ink);border-radius:0 0 2px 2px}
.pc-over{background:repeating-linear-gradient(45deg,var(--hi) 0 5px,var(--hi-soft) 5px 9px);border:2px solid var(--hi);border-bottom:0;border-radius:3px 3px 0 0}
.pc-col b{display:block;text-align:center;font-size:11px;font-weight:700;line-height:1.4;color:var(--hi)}
.pc-can{position:absolute;left:-4px;right:-4px;border-top:2.5px dashed var(--hi);z-index:2}
.pc-can em{position:absolute;right:4px;top:-24px;font-style:normal;font-size:11.5px;font-weight:600;background:var(--card);padding:1px 6px;border-radius:4px;color:var(--ink)}
.pc-hrs{margin-top:6px;font-size:11px;color:var(--mut);text-align:center}
.pc-pins{margin-top:10px;row-gap:5px}
.pc-pin{display:flex;align-items:center;gap:6px;min-width:0;padding:3px 8px 3px 3px;border-radius:12px;background:var(--soft);border:1.5px solid var(--line);font-size:11.5px;line-height:1.3}
.pc-pin b{flex-shrink:0;display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:50%;background:var(--ink);color:var(--card);font-size:11px}
.pc-pin span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pc-pin.is-short{padding-right:3px;justify-content:center}.pc-pin.is-short span{display:none}
.pc-chart .bm-key{margin-top:12px;align-items:center}
.bm-key .k-ok{background:var(--ink)}.bm-key .k-over{background:var(--hi);border-color:var(--hi)}
.pc-side{display:flex;flex-direction:column;gap:8px;min-width:0}
.pc-lg{display:flex;align-items:center;gap:12px;width:100%;padding:10px 12px;border:2px solid var(--ink);border-radius:10px;background:var(--card);text-align:left}
.lp .pc-lg.is-up{background:var(--soft)}
.pc-ln{flex-shrink:0;width:30px;height:30px;border-radius:50%;background:var(--ink);color:var(--card);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.pc-lg.is-up .pc-ln{background:var(--hi)}
.pc-lg span:nth-child(2){display:flex;flex-direction:column;min-width:0;flex:1 1 auto}
.pc-lg b{font-size:14px;line-height:1.3}.pc-lg em{font-style:normal;font-size:12px;color:var(--mut)}
.pc-desk{margin-top:16px}
.pc-low{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:30px}
.pc-low h4{margin-bottom:10px}
.pc-reads,.pc-roles{display:flex;flex-direction:column;gap:8px}
.pc-read{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 12px;align-items:center;padding:10px 14px;border-radius:10px;background:var(--card);border:1.5px solid var(--line)}
.pc-rn{font-size:13.5px;font-weight:600;line-height:1.35}
.pc-rv{display:flex;align-items:baseline;gap:6px;justify-self:end}.pc-rv b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:24px;line-height:1}.pc-rv span{font-size:11.5px;color:var(--mut)}
.pc-rg{font-size:12.5px;color:var(--mut)}
.pc-read .bm-tag{justify-self:end}
.pc-role{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:12px;align-items:center;padding:10px 14px;border-radius:10px;background:var(--card);border:1.5px solid var(--line)}
.pc-role span:nth-child(2){display:flex;flex-direction:column;min-width:0}
.pc-role b{font-size:14px}.pc-role em{font-style:normal;font-size:12.5px;color:var(--mut);line-height:1.4}
.pc-badge{width:26px;height:32px;border-radius:4px;border:2px solid var(--ink);background:linear-gradient(var(--hi) 0 8px,var(--card) 8px);position:relative}
.pc-badge::after{content:"";position:absolute;left:7px;top:12px;width:8px;height:8px;border-radius:50%;background:var(--ink)}
.pc-chart.is-empty{position:relative}
.pc-chart.is-empty .pc-bars{height:160px}
.pc-chart.is-empty .pc-col i{display:block;border:2px dashed var(--grey);border-bottom:0;border-radius:3px 3px 0 0}
.pc-ghost{margin-top:12px;font-size:13.5px;color:var(--mut)}
@container lp (max-width:699px){
 .pc-top{grid-template-columns:1fr}
 .pc-chart{padding:12px 8px 10px}
 .pc-plot{height:170px}
 .pc-bars,.pc-hrs,.pc-pins{column-gap:3px}
 .pc-hrs span{font-size:9.5px}
 .pc-pins{grid-template-columns:1fr}
 .pc-pin{grid-column:1 !important}
 .pc-pin span{white-space:normal}
 .pc-pin.is-short{justify-content:flex-start}.pc-pin.is-short span{display:inline}
 .pc-can em{top:-22px;font-size:10.5px}
 .pc-col b{font-size:9.5px}
 .pc-low{grid-template-columns:1fr;gap:20px}
 .pc-side .bx-mob{margin:2px 0 8px}
}
'''

# ==========================================================================================
PAGES = {
 'home': (None, home_canvas, HOME_CSS, HOME, 'od od-home', 'Home', 'The leak line'),
 'diagnosis': ('Diagnosis', dg_canvas, DG_CSS, DG, 'od od-dg', 'Diagnosis', 'The sieve'),
 'solutions': ('Solutions', so_canvas, SO_CSS, SO, 'od od-so', 'Solutions', 'The prescription pad'),
 'automations': ('Automations', au_canvas, AU_CSS, AU, 'od od-au', 'Automations', 'One patient’s visit'),
 'processes': ('Processes', pr_canvas, PR_CSS, PR, 'od od-pr', 'Processes', 'The busy-hours board'),
}
PALETTE = {
 'home': 'Saffron paper, warm black ink, vermilion drop',
 'diagnosis': 'Khaki, olive black ink, magenta',
 'solutions': 'Rose, raspberry ink, turquoise',
 'automations': 'Apricot, burnt umber ink, cobalt blue',
 'processes': 'Lagoon, deep sea ink, orange',
}

def build():
    os.makedirs(OUT, exist_ok=True)
    pages, words = {}, []
    for k, (place, fn, css, data, cls, label, _) in PAGES.items():
        t = THEMES[k]
        for st in ('filled', 'empty'):
            canvas = fn(st)
            for v in ('desktop', 'mobile'):
                h = C.page(t, place, canvas, C._accent(C.B.BED_CSS) + TOOL_CSS + css, data[st]['chat'], v, 'OPD Diagnostic Leak %s' % label, cls)
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(OUT, 'odl-%s.%s.%s.html' % (k, v, st)), 'w', encoding='utf-8').write(h)
            words += [(k, st, w) for w in C.plain_check(_text(canvas) + ' ' + json.dumps(data[st]['chat'], ensure_ascii=False))]
    return pages, words

def _text(h):
    import re
    return re.sub(r'<[^>]+>', ' ', h)

def review(pages):
    tpl = open(os.path.join(HERE, 'review_template.html'), encoding='utf-8').read()
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>%s</b><span>%s</span><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 4px %s"></i></button>' % (
        k, 'true' if k == 'home' else 'false', e(v[5]), e(v[6]), THEMES[k]['ground'], THEMES[k]['ink'], THEMES[k]['hi']) for k, v in PAGES.items())
    about = {k: '<b>%s · %s.</b> Colours: %s.' % (e(v[5]), e(v[6]), e(PALETTE[k])) for k, v in PAGES.items()}
    return (tpl.replace('@@PICKS@@', picks).replace('@@ABOUT@@', json.dumps(about, ensure_ascii=False))
               .replace('@@DATA@@', json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')))

if __name__ == '__main__':
    pages, words = build()
    if words:
        print('PLAIN ENGLISH:', words)
    rv = os.path.join(OUT, 'opd-diagnostic-leak-landing-pages.html')
    open(rv, 'w', encoding='utf-8').write(review(pages))
    print('built', rv, os.path.getsize(rv))
