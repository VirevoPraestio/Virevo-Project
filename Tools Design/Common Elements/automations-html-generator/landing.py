"""
Automations tab — landing page samples.
Look: the switch room. Pale steel ground, charcoal ink, rounded instrument panels, drawn switches,
wires and signal bars. Teal means switched on; gold marks the one to do next; dashed amber waits on
someone. Sentence-case labels.
  A  Switchboard    every automation is a switch on one wire; the main switch is the link it all needs
  B  Overnight arc  each automation placed at the hour it runs, from the evening round to leaving
  C  Signal bars    how ready each automation is, from idea to switched on
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'landing-common'))
from landing_common import e, canvas_wrap  # noqa: E402

TAB = 'Automations'
THEME = {'ground': '#E4E7EA', 'rail_bg': '#1C2A33', 'rail_fg': '#8FD3CD'}
LEVELS = ['Idea', 'Designed', 'Linked', 'Tested', 'Switched on']
LEVEL = {'idea': 0, 'designed': 1, 'linked': 2, 'testing': 3, 'live': 4, 'blank': -1}
STATUS = {'idea': 'Idea', 'designed': 'Designed', 'linked': 'Linked', 'testing': 'Testing', 'live': 'Switched on', 'blank': 'Empty'}

DATA = {
    'filled': {
        'stamp': {'at': 'Brought up to date at midnight, 28 September', 'since': '1 conversation since then is not in yet',
                  'fresh': 'Brought up to date just now, 9:42 AM', 'fresh_since': 'Everything you have said is in'},
        'standing': 'Six automations designed. None switched on yet.',
        'deck': 'All of them wait on one link: your IT team connecting the hospital software and the report system.',
        'main': {'title': 'Link to the hospital software', 'text': 'Your IT team connects billing, the report system and clinical notes.', 'status': 'waiting', 'pt': 1},
        'autos': [
            {'n': 1, 'title': 'Discharge summary written from the evening round', 'when': 'Evening round, 6 to 9 PM', 'hour': 19.5, 'status': 'designed', 'pt': 2},
            {'n': 2, 'title': 'Running bill kept up to date', 'when': 'All through the stay', 'hour': 22, 'status': 'designed'},
            {'n': 3, 'title': 'Supply count worked out for the nurses', 'when': 'When the bill is drawn up', 'hour': 23.5, 'status': 'designed'},
            {'n': 4, 'title': 'Insurance request sent the evening before', 'when': 'About 9 PM', 'hour': 21, 'status': 'designed', 'pt': 3},
            {'n': 5, 'title': 'Final summary signed on a phone', 'when': 'Morning round', 'hour': 32.5, 'status': 'designed'},
            {'n': 6, 'title': 'Alerts to housekeeping and transport', 'when': 'When the patient leaves', 'hour': 39.25, 'status': 'idea', 'pt': 4},
        ],
        'evidence': 'Other hospitals saved 6 to 8 hours a discharge. Not yet measured here.',
        'pending': [
            {'text': 'List exactly what your IT team must link first.', 'who': 'tojo', 'pt': 1},
            {'text': 'Check which reports arrive late and would hold up the summary.', 'who': 'tojo', 'pt': 2},
            {'text': 'Design the alerts for the bed left empty.', 'who': 'tojo', 'pt': 4},
            {'text': 'Confirm the insurance desk will accept an evening request.', 'who': 'you', 'need': 'Needs your insurance desk’s answer', 'pt': 3},
        ],
        'actions': {'go': {'detail': 'Map what your IT team must link', 'say': 'Let’s map what our IT team must link first'},
                    'add': {'detail': 'Name a task you’d like done for you', 'say': 'I’d like this done automatically: '},
                    'jump': {'tab': 'Processes', 'detail': 'See what changes on the wards', 'say': 'Take me to Processes'}},
        'chat': {'text': ['Here’s where the automations stand. Six are designed, and none are switched on, because they all wait on one link.',
                          'The quickest win is the summary written from the evening round.'],
                 'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
                 'note': 'Nothing switches on until the software is linked.',
                 'points': [{'n': 1, 'label': 'The link to the hospital software'}, {'n': 2, 'label': 'Summary from the evening round'},
                            {'n': 3, 'label': 'Insurance sent the evening before'}, {'n': 4, 'label': 'Alerts for the empty bed'}],
                 'prompts': ['What exactly does our IT team need?', 'Which one saves the most time?', 'Can we test one without the link?']},
    },
    'empty': {
        'stamp': {'at': 'Nothing to bring up to date yet', 'since': 'This page fills in as solutions are agreed',
                  'fresh': 'Checked just now, 9:42 AM', 'fresh_since': 'No automations yet'},
        'standing': 'No automations yet',
        'deck': 'Automations appear here once Solutions agree on work that should run without anyone typing it.',
        'main': {'title': 'Link to the hospital software', 'text': 'Checked once the first automation is agreed.', 'status': 'blank'},
        'autos': [{'n': None, 'title': 'Empty switch', 'when': '—', 'hour': 19 + 6 * i, 'status': 'blank'} for i in range(3)],
        'evidence': '',
        'pending': [
            {'text': 'Wait for Solutions to agree what should run on its own.', 'who': 'tojo'},
            {'text': 'Check what your hospital software can share.', 'who': 'tojo'},
            {'text': 'Plan the order in which to switch them on.', 'who': 'tojo'},
        ],
        'actions': {'go': {'detail': 'Begin in Solutions', 'say': 'Take me to Solutions'},
                    'add': {'detail': 'Name a task you’d like done for you', 'say': 'I’d like this done automatically: '},
                    'jump': {'tab': 'Processes', 'detail': 'Fills in as solutions are agreed', 'say': 'Take me to Processes'}},
        'chat': {'text': ['This is your Automations page. Nothing is on it yet.',
                          'Automations appear once a solution needs work done without anyone typing it.'],
                 'note': 'Automate what people repeat, not what they decide.', 'points': [],
                 'prompts': ['What could we automate first?', 'Start with Solutions', 'Do we need new software?']},
    },
}

BOLT = ('<svg class="au-emblem" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" stroke-width="3"/>'
        '<path d="M26.5 9L15 27h8l-2 12 12-18h-8z" fill="#8FD3CD" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/></svg>')

def masthead(m):
    return ('<header class="au-mast"><div class="au-id">%s<div><div class="au-eyebrow">Discharge Process</div><h2 class="au-tab">Automations</h2></div></div>'
            '<div class="au-meter">%s<span class="au-mid">Updates itself every night at midnight</span></div></header>' % (BOLT, m.stamp()))

def standing(m):
    return '<div class="au-stand"><h3 class="au-claim">%s</h3><p class="au-deck">%s</p></div>' % (e(m.d['standing']), e(m.d['deck']))

def pending(m):
    items = []
    for p in m.d['pending']:
        need = '<span class="au-need">%s</span>' % e(p['need']) if p.get('need') else ''
        items.append('<li class="au-pend-i au-who-%s"%s><span class="au-pm" aria-hidden="true"></span><span>%s%s</span></li>' % (p['who'], m.pt(p.get('pt')), e(p['text']), need))
    return '<section class="au-pend"><div class="au-label">What Tojo still has to do</div><ul>%s</ul></section>' % ''.join(items)

def toggle(status):
    lab = STATUS[status]
    return '<span class="au-sw au-sw-%s" aria-hidden="true"><span class="au-knob"></span></span><span class="sr">%s</span>' % (status, lab)

def counts(m):
    c = {k: 0 for k in LEVEL}
    for a in m.d['autos']: c[a['status']] += 1
    return c

# --- A: switchboard ---------------------------------------------------------------------------
def sample_a(m):
    mn = m.d['main']
    rows = ''.join('<li class="au-row au-st-%s"%s><span class="au-tap" aria-hidden="true"></span>%s<div class="au-row-b"><span class="au-row-t">%s</span>'
                   '<span class="au-row-w">%s</span></div><span class="au-tag au-tag-%s">%s</span></li>' % (
                       a['status'], m.pt(a.get('pt')), toggle(a['status']), e(a['title']), e(a['when']), a['status'], STATUS[a['status']]) for a in m.d['autos'])
    c = counts(m)
    tally = ''.join('<li><b>%d</b>%s</li>' % (c[k], lab) for k, lab in (('live', 'Switched on'), ('testing', 'Testing'), ('designed', 'Designed'), ('idea', 'Idea only')))
    main = ('<div class="au-main au-main-%s"%s><div class="au-lever" aria-hidden="true"><span></span></div><div><div class="au-label">Main switch</div>'
            '<div class="au-main-t">%s</div><p>%s</p><span class="au-tag au-tag-%s">%s</span></div></div>') % (
        mn['status'], m.pt(mn.get('pt')), e(mn['title']), e(mn['text']), 'waiting' if mn['status'] == 'waiting' else 'blank',
        'Waiting on your IT team' if mn['status'] == 'waiting' else 'Not checked yet')
    ev = '<p class="au-ev">%s</p>' % e(m.d['evidence']) if m.d['evidence'] else ''
    inner = ('%s%s<section class="au-board">%s<div class="au-bus"><ol>%s</ol></div><div class="au-side"><ul class="au-tally">%s</ul>%s</div></section>'
             '<div class="au-foot">%s%s</div>') % (masthead(m), standing(m), main, rows, tally, ev, pending(m), m.actions('au-acts-col'))
    return canvas_wrap('lp-au', 'lp-au-a', inner, m.state)

# --- B: the overnight arc -------------------------------------------------------------------
def sample_b(m):
    # Arc from 6 PM (hour 18) to 4 PM next day (hour 40): the stretch where the automations do their work.
    h0, h1, cx, cy, r = 18, 40, 250, 206, 176
    def pos(h, rr=r):
        a = math.pi * (1 - (h - h0) / (h1 - h0))
        return cx + rr * math.cos(a), cy - rr * math.sin(a)
    ticks = []
    for h, lab in ((18, '6 PM'), (22, '10 PM'), (26, '2 AM'), (30, '6 AM'), (34, '10 AM'), (38, '2 PM')):
        x0, y0 = pos(h, r - 8); x1, y1 = pos(h, r + 8); xl, yl = pos(h, r + 26)
        ticks.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="au-tick"/><text x="%.1f" y="%.1f" class="au-tl">%s</text>' % (x0, y0, x1, y1, xl, yl + 4, lab))
    night = 'M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (*pos(18), r, r, *pos(30))
    day = 'M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (*pos(30), r, r, *pos(40))
    marks = []
    for a in m.d['autos']:
        k = [x['n'] for x in sorted(m.d['autos'], key=lambda z: z['hour'])].index(a['n']) if a['n'] else 0
        x, y = pos(a['hour']); lx, ly = pos(a['hour'], r - (40 if k % 2 == 0 else 80))
        marks.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="au-lead"/><circle cx="%.1f" cy="%.1f" r="15" class="au-mk au-mk-%s"/>'
                     '<text x="%.1f" y="%.1f" class="au-mkn">%s</text>' % (x, y, lx, ly, lx, ly, a['status'], lx, ly + 5, a['n'] or ''))
    svg = ('<svg viewBox="0 0 500 236" class="au-arc" aria-hidden="true"><path d="%s" class="au-night"/><path d="%s" class="au-day"/>%s%s'
           '<text x="%.1f" y="%.1f" class="au-zone">Overnight, while the ward sleeps</text><text x="%.1f" y="%.1f" class="au-zone">Morning to going home</text></svg>') % (
        night, day, ''.join(ticks), ''.join(marks), 140, 230, 380, 230)
    key = ''.join('<li class="au-st-%s"%s><span class="au-kn">%s</span><div><b>%s</b><span>%s · %s</span></div></li>' % (
        a['status'], m.pt(a.get('pt')), a['n'] or '·', e(a['title']), e(a['when']), STATUS[a['status']]) for a in m.d['autos'])
    mn = m.d['main']
    gate = ('<div class="au-gate au-main-%s"%s><span class="au-lock" aria-hidden="true"></span><div><b>%s</b><span>%s</span></div></div>' % (
        mn['status'], m.pt(mn.get('pt')), e(mn['title']), 'Every automation waits on this' if mn['status'] == 'waiting' else e(mn['text'])))
    inner = ('%s%s<section class="au-clock"><div class="au-clock-l">%s</div><div class="au-clock-r">%s<ol class="au-key">%s</ol></div></section><div class="au-foot">%s%s</div>') % (
        masthead(m), standing(m), svg, gate, key, pending(m), m.actions('au-acts-col'))
    return canvas_wrap('lp-au', 'lp-au-b', inner, m.state)

# --- C: signal bars ---------------------------------------------------------------------------
def bars(level):
    return '<span class="au-bars" aria-hidden="true">%s</span>' % ''.join('<i class="%s" style="height:%dpx"></i>' % ('on' if i <= level else '', 8 + i * 6) for i in range(5))

def sample_c(m):
    rows = ''.join('<li class="au-sig au-st-%s"%s>%s<div class="au-sig-b"><b>%s</b><span>%s</span></div><span class="au-tag au-tag-%s">%s</span></li>' % (
        a['status'], m.pt(a.get('pt')), bars(LEVEL[a['status']]), e(a['title']), e(a['when']), a['status'], STATUS[a['status']]) for a in m.d['autos'])
    n = len([a for a in m.d['autos'] if a['n']]); tot = max(n, 1)
    lv = [sum(1 for a in m.d['autos'] if a['n'] and LEVEL[a['status']] >= i) for i in range(5)]
    ladder = ''.join('<li class="%s"><span class="au-lad-bar"><span style="width:%d%%"></span></span><span class="au-lad-l">%s</span><b>%d of %d</b></li>' % (
        'is-zero' if lv[i] == 0 else '', 100 * lv[i] // tot if n else 0, LEVELS[i], lv[i], n) for i in range(5))
    mn = m.d['main']
    block = ('<div class="au-block au-main-%s"%s><b>Holding everything at “Designed”</b><span>%s. %s</span></div>' % (mn['status'], m.pt(mn.get('pt')), e(mn['title']), e(mn['text']))
             if mn['status'] == 'waiting' else '<div class="au-block au-main-blank"><b>Nothing to hold up yet</b><span>%s</span></div>' % e(mn['text']))
    inner = ('%s%s<section class="au-c-body"><div class="au-ready"><div class="au-label">How far they have got</div><ol class="au-ladder">%s</ol>%s</div>'
             '<ol class="au-sigs">%s</ol></section><div class="au-foot">%s%s</div>') % (masthead(m), standing(m), ladder, block, rows, pending(m), m.actions('au-acts-col'))
    return canvas_wrap('lp-au', 'lp-au-c', inner, m.state)

SAMPLES = [('a', 'Switchboard', 'Each automation is a switch on one wire, behind the main switch they all need.', sample_a),
           ('b', 'Overnight arc', 'Each automation placed at the hour it runs, from the evening round to going home.', sample_b),
           ('c', 'Signal bars', 'How ready each automation is, from idea to switched on, with what holds them back.', sample_c)]

CSS = r'''
.lp-au{--ground:#E4E7EA;--panel:#F9FAFB;--ink:#1C2A33;--muted:#4B5963;--teal:#0F6E6B;--teal-l:#8FD3CD;--gold:#d4a94f;--amber:#8A5608;--off:#8C98A0;
  background:var(--ground);color:var(--ink);padding:18px 32px 22px;display:flex;flex-direction:column;gap:14px}
.lp-au .au-label{font-size:13px;font-weight:600;color:var(--muted)}
.lp-au .au-mast{display:flex;justify-content:space-between;align-items:center;gap:18px}
.lp-au .au-id{display:flex;align-items:center;gap:14px}
.lp-au .au-emblem{width:46px;height:46px;color:var(--ink)}
.lp-au .au-eyebrow{font-size:13px;font-weight:500;color:var(--muted)}
.lp-au .au-tab{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:48px;line-height:.9;letter-spacing:.01em}
.lp-au .au-meter{display:flex;flex-direction:column;align-items:flex-end;gap:4px}
.lp-au .lp-stamp{display:flex;align-items:center;gap:12px;background:var(--ink);color:#EEF2F4;border-radius:12px;padding:6px 6px 6px 14px}
.lp-au .lp-stamp-txt{display:flex;flex-direction:column}
.lp-au .lp-stamp-at{font-size:13px;font-weight:600} .lp-au .lp-stamp-since{font-size:12px;color:#B7C2C8}
.lp-au .lp-stamp-since::before{content:'';display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--gold);margin-right:6px;vertical-align:1px}
.lp-au .lp-refresh{background:var(--teal-l);color:var(--ink);border:none;border-radius:8px;font-size:13px;font-weight:600}
.lp-au .au-mid{font-size:11.5px;color:var(--muted)}
.lp-au .au-claim{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:37px;line-height:.95;letter-spacing:.01em}
.lp-au .au-deck{margin-top:5px;font-size:14.5px;color:var(--muted);max-width:80ch;line-height:1.45}
.lp-au .au-tag{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:12px;white-space:nowrap;border:1.5px solid var(--ink)}
.lp-au .au-tag-live{background:var(--teal);border-color:var(--teal);color:#fff}
.lp-au .au-tag-testing{border-color:var(--teal);color:var(--teal)}
.lp-au .au-tag-designed{border-color:var(--ink)}
.lp-au .au-tag-idea,.lp-au .au-tag-blank{border-style:dashed;border-color:var(--off);color:var(--muted)}
.lp-au .au-tag-waiting{border-style:dashed;border-color:var(--amber);color:var(--amber)}
.lp-au .au-pend ul{display:flex;flex-direction:column;gap:7px;margin-top:7px}
.lp-au .au-pend-i{display:flex;gap:10px;font-size:14px;line-height:1.4}
.lp-au .au-pm{flex-shrink:0;width:10px;height:10px;margin-top:6px;border-radius:50%;background:var(--ink);box-shadow:0 0 0 3px rgba(28,42,51,.15)}
.lp-au .au-who-you .au-pm{background:transparent;border:2px dashed var(--amber);box-shadow:none;width:12px;height:12px}
.lp-au .au-need{display:block;font-size:12px;font-weight:600;color:var(--amber)}
.lp-au .lp-acts{display:flex;gap:8px}
.lp-au .au-acts-col{flex-direction:column}
.lp-au .lp-act{justify-content:center;padding:6px 16px;min-height:52px;background:var(--panel);border:1.5px solid rgba(28,42,51,.35);border-radius:12px;font-size:14px}
.lp-au .lp-act-d{font-size:12.5px;color:var(--muted)}
.lp-au .lp-act-go{background:var(--ink);border-color:var(--ink);color:#EEF2F4;padding-left:40px;position:relative}
.lp-au .lp-act-go::before{content:'';position:absolute;left:14px;top:50%;margin-top:-8px;width:16px;height:16px;border-radius:50%;background:var(--gold);box-shadow:0 0 0 4px rgba(212,169,79,.3)}
.lp-au .lp-act-go .lp-act-d{color:#B7C2C8}
.lp-au .lp-act:hover{border-color:var(--teal)}
.lp-au .au-foot{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:24px;align-items:start}
/* switches */
.lp-au .au-sw{position:relative;flex-shrink:0;width:48px;height:26px;border-radius:13px;background:#CBD2D7;border:1.5px solid var(--ink)}
.lp-au .au-knob{position:absolute;top:2px;left:2px;width:19px;height:19px;border-radius:50%;background:var(--panel);border:1.5px solid var(--ink)}
.lp-au .au-sw-live{background:var(--teal)} .lp-au .au-sw-live .au-knob{left:24px}
.lp-au .au-sw-testing{background:var(--teal-l)} .lp-au .au-sw-testing .au-knob{left:13px}
.lp-au .au-sw-idea,.lp-au .au-sw-blank{border-style:dashed;border-color:var(--off);background:transparent} .lp-au .au-sw-idea .au-knob,.lp-au .au-sw-blank .au-knob{border-style:dashed;border-color:var(--off);background:transparent}
/* A */
.lp-au-a .au-board{display:grid;grid-template-columns:200px minmax(0,1fr) 150px;background:var(--panel);border:1.5px solid var(--ink);border-radius:16px;overflow:hidden}
.lp-au-a .au-main{background:var(--ink);color:#EEF2F4;padding:14px 16px;display:flex;flex-direction:column;gap:12px}
.lp-au-a .au-main .au-label{color:#B7C2C8} .lp-au-a .au-main-t{font-size:15px;font-weight:600;line-height:1.3;margin:2px 0 4px} .lp-au-a .au-main p{font-size:12.5px;color:#C9D2D7;line-height:1.4;margin-bottom:8px}
.lp-au-a .au-main .au-tag-waiting{border-color:var(--gold);color:var(--gold)} .lp-au-a .au-main .au-tag-blank{border-color:#8C98A0;color:#C9D2D7}
.lp-au-a .au-lever{width:44px;height:64px;border:2px solid #EEF2F4;border-radius:10px;position:relative}
.lp-au-a .au-lever span{position:absolute;left:8px;right:8px;bottom:8px;height:22px;border-radius:5px;background:var(--gold)}
.lp-au-a .au-bus{position:relative;padding:8px 18px 8px 34px}
.lp-au-a .au-bus::before{content:'';position:absolute;left:18px;top:0;bottom:0;border-left:3px dashed var(--off)}
.lp-au-a .au-row{position:relative;display:grid;grid-template-columns:48px minmax(0,1fr) auto;column-gap:12px;align-items:center;padding:7px 0;border-bottom:1px solid rgba(28,42,51,.1)}
.lp-au-a .au-row:last-child{border-bottom:none}
.lp-au-a .au-tap{position:absolute;left:-16px;top:50%;width:16px;border-top:2px solid var(--off)}
.lp-au-a .au-row-b{display:flex;flex-direction:column} .lp-au-a .au-row-t{font-size:13.5px;font-weight:600;line-height:1.3} .lp-au-a .au-row-w{font-size:12px;color:var(--muted)}
.lp-au-a .au-side{border-left:1.5px solid rgba(28,42,51,.15);padding:14px;display:flex;flex-direction:column;gap:12px}
.lp-au-a .au-tally{display:flex;flex-direction:column;gap:6px;font-size:12.5px;color:var(--muted)}
.lp-au-a .au-tally b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:26px;color:var(--ink);margin-right:8px;vertical-align:-3px}
.lp-au-a .au-ev{font-size:12px;line-height:1.4;color:var(--muted);border-top:1px dashed rgba(28,42,51,.3);padding-top:10px;font-style:italic}
/* B */
.lp-au-b .au-clock{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:18px;align-items:start;background:var(--panel);border:1.5px solid var(--ink);border-radius:16px;padding:10px 16px 12px}
.lp-au-b .au-arc{width:100%;height:auto;display:block;overflow:visible}
.lp-au-b .au-night{fill:none;stroke:var(--ink);stroke-width:10} .lp-au-b .au-day{fill:none;stroke:#CBD2D7;stroke-width:10}
.lp-au-b .au-tick{stroke:var(--ink);stroke-width:1.5} .lp-au-b .au-tl{font:500 12px Poppins,sans-serif;fill:var(--muted);text-anchor:middle}
.lp-au-b .au-zone{font:600 12px Poppins,sans-serif;fill:var(--ink);text-anchor:middle}
.lp-au-b .au-lead{stroke:var(--ink);stroke-width:1.5;stroke-dasharray:3 3}
.lp-au-b .au-mk{fill:var(--panel);stroke:var(--ink);stroke-width:2} .lp-au-b .au-mk-live{fill:var(--teal);stroke:var(--teal)} .lp-au-b .au-mk-idea,.lp-au-b .au-mk-blank{stroke-dasharray:4 3;stroke:var(--off)}
.lp-au-b .au-mkn{font:700 13px Poppins,sans-serif;fill:var(--ink);text-anchor:middle}
.lp-au-b .au-clock-r{display:flex;flex-direction:column;gap:10px;padding-top:6px}
.lp-au-b .au-gate{display:flex;gap:10px;align-items:center;padding:8px 10px;border-radius:10px;border:1.5px dashed var(--amber);background:#FBF6EC}
.lp-au-b .au-main-blank.au-gate{border-color:var(--off);background:transparent}
.lp-au-b .au-gate div{display:flex;flex-direction:column} .lp-au-b .au-gate b{font-size:13px;font-weight:600} .lp-au-b .au-gate span{font-size:12px;color:var(--muted)}
.lp-au-b .au-lock{flex-shrink:0;width:16px;height:13px;border:2px solid var(--amber);border-radius:3px;position:relative;margin-top:6px}
.lp-au-b .au-lock::before{content:'';position:absolute;left:2px;right:2px;top:-9px;height:9px;border:2px solid var(--amber);border-bottom:none;border-radius:6px 6px 0 0}
.lp-au-b .au-key{display:flex;flex-direction:column;gap:5px}
.lp-au-b .au-key li{display:flex;gap:9px;align-items:flex-start}
.lp-au-b .au-kn{flex-shrink:0;width:24px;height:24px;border-radius:50%;border:2px solid var(--ink);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700}
.lp-au-b .au-st-idea .au-kn,.lp-au-b .au-st-blank .au-kn{border-style:dashed;border-color:var(--off)}
.lp-au-b .au-key div{display:flex;flex-direction:column} .lp-au-b .au-key b{font-size:13px;font-weight:600;line-height:1.3} .lp-au-b .au-key span{font-size:11.5px;color:var(--muted)}
/* C */
.lp-au-c .au-c-body{display:grid;grid-template-columns:260px minmax(0,1fr);gap:18px;align-items:start}
.lp-au-c .au-ready{background:var(--ink);color:#EEF2F4;border-radius:16px;padding:14px 16px;display:flex;flex-direction:column;gap:12px}
.lp-au-c .au-ready .au-label{color:#B7C2C8}
.lp-au-c .au-ladder{display:flex;flex-direction:column-reverse;gap:8px}
.lp-au-c .au-ladder li{display:grid;grid-template-columns:minmax(0,1fr) auto;row-gap:3px;font-size:12.5px}
.lp-au-c .au-lad-bar{grid-column:1/-1;height:8px;border-radius:4px;background:rgba(238,242,244,.15);overflow:hidden} .lp-au-c .au-lad-bar span{display:block;height:100%;background:var(--teal-l)}
.lp-au-c .au-ladder b{font-weight:600} .lp-au-c .au-ladder .is-zero{color:#9AA7AE}
.lp-au-c .au-block{border:1.5px dashed var(--gold);border-radius:10px;padding:8px 10px;display:flex;flex-direction:column;gap:2px;font-size:12px;color:#C9D2D7;line-height:1.4}
.lp-au-c .au-block b{color:var(--gold);font-size:13px} .lp-au-c .au-main-blank.au-block{border-color:#8C98A0} .lp-au-c .au-main-blank.au-block b{color:#EEF2F4}
.lp-au-c .au-sigs{background:var(--panel);border:1.5px solid var(--ink);border-radius:16px;padding:4px 16px}
.lp-au-c .au-sig{display:grid;grid-template-columns:52px minmax(0,1fr) auto;column-gap:12px;align-items:center;padding:8px 0;border-bottom:1px solid rgba(28,42,51,.1)}
.lp-au-c .au-sig:last-child{border-bottom:none}
.lp-au-c .au-bars{display:flex;align-items:flex-end;gap:3px;height:34px} .lp-au-c .au-bars i{width:7px;border-radius:2px;background:#D5DBDF;border:1px solid #B4BEC4}
.lp-au-c .au-bars i.on{background:var(--ink);border-color:var(--ink)} .lp-au-c .au-st-live .au-bars i.on{background:var(--teal);border-color:var(--teal)}
.lp-au-c .au-st-idea .au-bars i.on{background:var(--gold);border-color:var(--gold)}
.lp-au-c .au-sig-b{display:flex;flex-direction:column} .lp-au-c .au-sig-b b{font-size:13.5px;font-weight:600;line-height:1.3} .lp-au-c .au-sig-b span{font-size:12px;color:var(--muted)}
/* first visit */
.lp-au[data-lp-state=empty] .au-claim{color:var(--muted)}
.lp-au[data-lp-state=empty] .au-row-t,.lp-au[data-lp-state=empty] .au-sig-b b,.lp-au[data-lp-state=empty] .au-key b{color:var(--muted);font-weight:500}
/* narrow */
@container lp (max-width:699px){
  .lp-au{padding:16px 14px 22px;gap:16px}
  .lp-au .au-mast{flex-direction:column;align-items:stretch;gap:12px}
  .lp-au .au-meter{align-items:stretch} .lp-au .lp-stamp{justify-content:space-between}
  .lp-au .au-tab{font-size:42px} .lp-au .au-claim{font-size:34px}
  .lp-au .lp-acts{flex-direction:column}
  .lp-au .au-foot{grid-template-columns:minmax(0,1fr)}
  .lp-au-a .au-board{grid-template-columns:minmax(0,1fr)}
  .lp-au-a .au-main{flex-direction:row;align-items:flex-start}
  .lp-au-a .au-side{border-left:none;border-top:1.5px solid rgba(28,42,51,.15)} .lp-au-a .au-tally{flex-direction:row;flex-wrap:wrap;gap:4px 14px}
  .lp-au-a .au-row{grid-template-columns:48px minmax(0,1fr);row-gap:4px} .lp-au-a .au-row .au-tag{grid-column:2;justify-self:start}
  .lp-au-b .au-clock{grid-template-columns:minmax(0,1fr);padding:8px 10px 12px}
  .lp-au-c .au-c-body{grid-template-columns:minmax(0,1fr)}
  .lp-au-c .au-sig{grid-template-columns:44px minmax(0,1fr);row-gap:4px} .lp-au-c .au-sig .au-tag{grid-column:2;justify-self:start}
}
'''
