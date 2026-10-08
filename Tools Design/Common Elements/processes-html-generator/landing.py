"""
Processes tab — landing page samples. Processes covers three things: process changes, the measures
we watch (KPI monitoring) and team and role changes.
Look: the ward board. Pale heather ground, aubergine ink, a white board with magnet strips, instrument
readouts for the measures, and seats for the roles. Sentence-case labels.
  A  Ward board        three columns on one board, the trial strip across the bottom
  B  Readouts & seats  the measures as instrument windows, the changes as a lane, the roles as seats
  C  The loop          plan, try on one ward, measure, adjust, spread: each area pinned to its place on it
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'landing-common'))
from landing_common import e, canvas_wrap  # noqa: E402

TAB = 'Processes'
THEME = {'ground': '#ECE8EE', 'rail_bg': '#2A1E30', 'rail_fg': '#E9C8F0'}
LOOP = ['Plan', 'Try on one ward', 'Measure', 'Adjust', 'Spread to all wards']

DATA = {
    'filled': {
        'stamp': {'at': 'Brought up to date at midnight, 28 September', 'since': '1 conversation since then is not in yet',
                  'fresh': 'Brought up to date just now, 9:42 AM', 'fresh_since': 'Everything you have said is in'},
        'standing': 'The trial is planned. Nothing has changed on the wards yet.',
        'deck': 'Changes, measures and new roles in one place. A two-week trial on one ward comes first.',
        'loop_at': 0,
        'trial': {'title': 'Two-week trial on one ward', 'status': 'Not started', 'note': 'No new staff and no new system needed', 'pt': 1},
        'changes': [
            {'t': 'The evening round starts the paperwork', 's': 'agreed'},
            {'t': 'Discharge papers drafted before signing', 's': 'agreed', 'flag': 'Biggest hold-up', 'pt': 2},
            {'t': 'Bill and supply count kept up to date', 's': 'agreed'},
            {'t': 'Insurance asked the evening before', 's': 'agreed'},
            {'t': 'Family and transport told the night before', 's': 'agreed'},
            {'t': 'Bed made ready as the patient leaves', 's': 'new'},
        ],
        'measures': [
            {'t': 'Hours from ready to home', 'v': '5 hours 15 minutes', 's': 'confirmed', 'pt': 3},
            {'t': 'Insurance approval time', 'v': 'About 1 hour', 's': 'confirmed'},
            {'t': 'Bed empty after the patient leaves', 'v': '75 minutes', 's': 'confirmed'},
            {'t': 'Patients home by 10 AM', 'v': '—', 's': 'new'},
            {'t': 'Decisions made on the evening round', 'v': '—', 's': 'new'},
            {'t': 'Money won back each month', 'v': '—', 's': 'new'},
        ],
        'roles': [
            {'t': 'Discharge Manager', 'seats': 1, 'filled': 0, 'note': 'Recommended now, before the trial', 'pt': 4},
            {'t': 'Discharge Executives', 'seats': 2, 'filled': 0, 'note': 'One for 8 to 11 AM, one for 6 to 9 PM', 'pt': 5},
        ],
        'roles_note': '₹10 to 11.5 lakh a year. Your Head of Operations approves.', 'roles_cost': '₹10 to 11.5 lakh a year',
        'pending': [
            {'text': 'Pick the trial ward with you, starting with the latest-deciding consultants.', 'who': 'tojo', 'pt': 1},
            {'text': 'Write the job outline for the Discharge Manager.', 'who': 'tojo', 'pt': 4},
            {'text': 'Set a goal for each measure after the first trial week.', 'who': 'tojo', 'pt': 3},
            {'text': 'Name who will record the times on the trial ward.', 'who': 'you', 'need': 'Needs a name from you'},
        ],
        'actions': {'go': {'detail': 'Pick the trial ward', 'say': 'Let’s pick the trial ward'},
                    'add': {'detail': 'Add a change, a measure or a role', 'say': 'I want to add a change: '},
                    'jump': {'tab': 'Diagnosis', 'detail': 'Four stops still to walk', 'say': 'Take me back to Diagnosis'}},
        'chat': {'text': ['Here’s where the processes stand. The changes are agreed on paper and the trial is planned, but nothing has been tried on a ward yet.',
                          'Three measures already have a starting number. The other three start in the trial.'],
                 'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
                 'note': 'Prove it on one ward before changing them all.',
                 'points': [{'n': 1, 'label': 'The trial ward'}, {'n': 2, 'label': 'Discharge papers, the biggest hold-up'},
                            {'n': 3, 'label': 'Hours from ready to home'}, {'n': 4, 'label': 'The Discharge Manager'},
                            {'n': 5, 'label': 'The two Discharge Executives'}],
                 'prompts': ['Which ward should we start on?', 'Why hire the manager before the trial?', 'What will the trial cost us?']},
    },
    'empty': {
        'stamp': {'at': 'Nothing to bring up to date yet', 'since': 'This page fills in as solutions are agreed',
                  'fresh': 'Checked just now, 9:42 AM', 'fresh_since': 'Nothing agreed yet'},
        'standing': 'Nothing to change yet',
        'deck': 'Process changes, the measures we watch and any new roles appear here once solutions are agreed.',
        'loop_at': -1,
        'trial': {'title': 'A trial on one ward', 'status': 'Planned later', 'note': 'Every change is tried small first'},
        'changes': [], 'measures': [], 'roles': [], 'roles_note': '',
        'pending': [
            {'text': 'Wait for Solutions to agree what should change.', 'who': 'tojo'},
            {'text': 'Pick the few measures that show whether it worked.', 'who': 'tojo'},
            {'text': 'Size any new roles to your busy hours, not your daily total.', 'who': 'tojo'},
        ],
        'actions': {'go': {'detail': 'Begin in Diagnosis', 'say': 'Take me to Diagnosis'},
                    'add': {'detail': 'Tell Tojo about a change already under way', 'say': 'We have already started this change: '},
                    'jump': {'tab': 'Diagnosis', 'detail': 'Where it all starts', 'say': 'Take me to Diagnosis'}},
        'chat': {'text': ['This is your Processes page. It covers process changes, the measures we watch and changes to roles.',
                          'It fills in once solutions are agreed.'],
                 'note': 'Change how the work flows, then measure it.', 'points': [],
                 'prompts': ['What usually changes first?', 'Start with Diagnosis', 'Which measures matter most?']},
    },
}

LOOPICO = ('<svg class="pr-emblem" viewBox="0 0 48 48" aria-hidden="true"><path d="M10 20a14 14 0 0124-8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
           '<path d="M34 5v8h-8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
           '<path d="M38 28a14 14 0 01-24 8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
           '<path d="M14 43v-8h8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><circle cx="24" cy="24" r="4" fill="#d4a94f"/></svg>')
ICO = {'changes': '<path d="M4 7h11M11 3l4 4-4 4M20 17H9M13 13l-4 4 4 4"/>',
       'measures': '<path d="M4 17a8 8 0 0116 0"/><path d="M12 17l4-5"/><circle cx="12" cy="17" r="1.5"/>',
       'roles': '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6M15 14.5c3 0 5.5 2 5.5 5.5"/>'}

def ico(k):
    return '<svg class="pr-ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % ICO[k]

def masthead(m):
    return ('<header class="pr-mast"><div class="pr-id">%s<div><div class="pr-eyebrow">Discharge Process</div><h2 class="pr-tab">Processes</h2>'
            '<div class="pr-subs">Process changes · Measures we watch · Team and role changes</div></div></div><div class="pr-stampw">%s<span class="pr-mid">Refreshed every night at midnight</span></div></header>' % (LOOPICO, m.stamp()))

def standing(m):
    return '<div class="pr-stand"><h3 class="pr-claim">%s</h3><p class="pr-deck">%s</p></div>' % (e(m.d['standing']), e(m.d['deck']))

def pending(m):
    items = []
    for p in m.d['pending']:
        need = '<span class="pr-need">%s</span>' % e(p['need']) if p.get('need') else ''
        items.append('<li class="pr-pend-i pr-who-%s"%s><span class="pr-pm" aria-hidden="true"></span><span>%s%s</span></li>' % (p['who'], m.pt(p.get('pt')), e(p['text']), need))
    return '<section class="pr-pend"><div class="pr-label">What Tojo still has to do</div><ul>%s</ul></section>' % ''.join(items)

def ghost(n, text):
    return ''.join('<li class="pr-ghost"><span>%s</span></li>' % e(text) for _ in range(n))

def change_items(m):
    if not m.d['changes']: return ghost(2, 'Appears once a solution is agreed')
    return ''.join('<li class="pr-mag pr-s-%s"%s><span class="pr-dot"></span><span>%s%s</span></li>' % (
        c['s'], m.pt(c.get('pt')), e(c['t']), '<b class="pr-flag">%s</b>' % e(c['flag']) if c.get('flag') else '') for c in m.d['changes'])

def measure_items(m):
    if not m.d['measures']: return ghost(2, 'Chosen once the fix is agreed')
    return ''.join('<li class="pr-mag pr-m-%s"%s><span class="pr-dot"></span><span class="pr-mt">%s</span><b class="pr-mv">%s</b></li>' % (
        x['s'], m.pt(x.get('pt')), e(x['t']), e(x['v']) if x['s'] == 'confirmed' else 'New') for x in m.d['measures'])

def seats(r):
    return '<span class="pr-seats" aria-label="%d of %d filled">%s</span>' % (r['filled'], r['seats'], ''.join(
        '<svg viewBox="0 0 28 30" class="pr-seat %s" aria-hidden="true"><path d="M7 3h14v13H7z"/><path d="M4 16h20v5H4zM7 21v7M21 21v7"/></svg>' % ('on' if i < r['filled'] else '') for i in range(r['seats'])))

def role_items(m):
    if not m.d['roles']: return ghost(1, 'Sized once the work is known')
    out = ''.join('<li class="pr-mag pr-role"%s>%s<span><b>%s</b><span class="pr-rn">%s</span></span></li>' % (
        m.pt(r.get('pt')), seats(r), e(r['t']), e(r['note'])) for r in m.d['roles'])
    return out + ('<li class="pr-cost">%s</li>' % e(m.d['roles_note']) if m.d['roles_note'] else '')

def col_summary(m, k):
    d = m.d
    if k == 'changes':
        return '%d agreed on paper · %d new · %d tried' % tuple(sum(1 for c in d['changes'] if c['s'] == k) for k in ('agreed', 'new', 'tried')) if d['changes'] else 'None yet'
    if k == 'measures':
        return '%d with a starting number · %d new' % (sum(1 for c in d['measures'] if c['s'] == 'confirmed'), sum(1 for c in d['measures'] if c['s'] == 'new')) if d['measures'] else 'None yet'
    if not d['roles']: return 'None yet'
    n = sum(r['seats'] - r.get('filled', 0) for r in d['roles'])
    return '%d %s to hire%s' % (n, 'person' if n == 1 else 'people', (' · ' + d['roles_cost']) if d.get('roles_cost') else '')

# --- A: ward board -----------------------------------------------------------------------------
def sample_a(m):
    cols = [('changes', 'Process changes', change_items(m)), ('measures', 'Measures we watch', measure_items(m)), ('roles', 'Team and role changes', role_items(m))]
    board = ''.join('<section class="pr-col pr-col-%s"><div class="pr-col-h">%s<div><h4>%s</h4><span>%s</span></div></div><ul>%s</ul></section>' % (
        k, ico(k), e(t), e(col_summary(m, k)), items) for k, t, items in cols)
    tr = m.d['trial']
    weeks = ''.join('<i>%s</i>' % d for d in ('Week 1', 'Week 2'))
    strip = ('<div class="pr-strip"%s><div><b>%s</b><span>%s</span></div><div class="pr-weeks" aria-hidden="true">%s</div><span class="pr-trial-s">%s</span></div>' % (
        m.pt(tr.get('pt')), e(tr['title']), e(tr['note']), weeks, e(tr['status'])))
    inner = ('%s%s<div class="pr-board"><div class="pr-cols">%s</div>%s</div><div class="pr-foot">%s%s</div>') % (
        masthead(m), standing(m), board, strip, pending(m), m.actions('pr-acts-col'))
    return canvas_wrap('lp-pr', 'lp-pr-a', inner, m.state)

# --- B: readouts and seats ----------------------------------------------------------------------
def sample_b(m):
    if m.d['measures']:
        reads = ''.join('<li class="pr-read pr-m-%s"%s><span class="pr-rt">%s</span><span class="pr-win">%s</span><span class="pr-rs">%s</span></li>' % (
            x['s'], m.pt(x.get('pt')), e(x['t']), e(x['v']) if x['s'] == 'confirmed' else '—', 'Your number' if x['s'] == 'confirmed' else 'New, starts in the trial') for x in m.d['measures'])
    else:
        reads = ''.join('<li class="pr-read pr-m-new"><span class="pr-rt">Measure to choose</span><span class="pr-win">—</span><span class="pr-rs">Picked once the fix is agreed</span></li>' for _ in range(3))
    if m.d['changes']:
        lane = ''.join('<li class="pr-ln pr-s-%s"%s><span>%s</span>%s</li>' % (c['s'], m.pt(c.get('pt')), e(c['t']), '<b class="pr-flag">%s</b>' % e(c['flag']) if c.get('flag') else '') for c in m.d['changes'])
    else:
        lane = '<li class="pr-ln pr-ghost-ln"><span>Changes appear once a solution is agreed</span></li>'
    if m.d['roles']:
        seat = ''.join('<li%s>%s<b>%s</b><span>%s</span></li>' % (m.pt(r.get('pt')), seats(r), e(r['t']), e(r['note'])) for r in m.d['roles'])
        seat += '<li class="pr-cost">%s</li>' % e(m.d['roles_note'])
    else:
        seat = '<li class="pr-ghost"><span>Seats appear once roles are sized</span></li>'
    tr = m.d['trial']
    inner = ('%s%s<section class="pr-panel"><div class="pr-ph">%s<h4>Measures we watch</h4><span>%s</span></div><ol class="pr-reads">%s</ol></section>'
             '<div class="pr-b-row"><section class="pr-panel"><div class="pr-ph">%s<h4>Process changes</h4><span>%s</span></div><ol class="pr-lane">%s</ol>'
             '<div class="pr-trial"%s><b>%s</b> %s</div></section>'
             '<section class="pr-panel"><div class="pr-ph">%s<h4>Team and role changes</h4></div><ul class="pr-seatplan">%s</ul></section></div>'
             '<div class="pr-foot">%s%s</div>') % (
        masthead(m), standing(m), ico('measures'), e(col_summary(m, 'measures')), reads, ico('changes'), e(col_summary(m, 'changes')), lane,
        m.pt(tr.get('pt')), e(tr['title']) + ':', e(tr['status'].lower()), ico('roles'), seat, pending(m), m.actions('pr-acts-col'))
    return canvas_wrap('lp-pr', 'lp-pr-b', inner, m.state)

# --- C: the loop --------------------------------------------------------------------------------
def sample_c(m):
    at = m.d['loop_at']; cx, cy, r = 150, 150, 108; n = len(LOOP)
    nodes = []; arcs = []
    for i, name in enumerate(LOOP):
        a = math.radians(-90 + i * 360 / n); x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        a2 = math.radians(-90 + (i + 1) * 360 / n - 14); a1 = math.radians(-90 + i * 360 / n + 14)
        arcs.append('<path d="M%.1f %.1f A%d %d 0 0 1 %.1f %.1f" class="pr-arc" marker-end="url(#pr-ah)"/>' % (
            cx + r * math.cos(a1), cy + r * math.sin(a1), r, r, cx + r * math.cos(a2), cy + r * math.sin(a2)))
        cls = 'is-at' if i == at else ('is-done' if i < at else '')
        nodes.append('<g class="pr-node %s"><circle cx="%.1f" cy="%.1f" r="17"/><text x="%.1f" y="%.1f">%d</text></g>' % (cls, x, y, x, y + 5, i + 1))
    svg = ('<svg viewBox="0 0 300 300" class="pr-loop" aria-hidden="true"><defs><marker id="pr-ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0 0L10 5L0 10z" class="pr-ahp"/></marker></defs>%s%s<text x="150" y="146" class="pr-loop-c">%s</text><text x="150" y="168" class="pr-loop-s">%s</text></svg>') % (
        ''.join(arcs), ''.join(nodes), 'Now: plan' if at == 0 else ('Not started' if at < 0 else 'Now: ' + LOOP[at].lower()), 'One ward, two weeks' if at >= 0 else 'Starts once agreed')
    names = ''.join('<li class="%s"><span>%d</span>%s</li>' % ('is-at' if i == at else '', i + 1, e(x)) for i, x in enumerate(LOOP))
    def card(k, title, where, body):
        return '<section class="pr-card pr-card-%s"><div class="pr-ph">%s<h4>%s</h4><em>%s</em></div><span class="pr-cs">%s</span><ul>%s</ul></section>' % (k, ico(k), e(title), e(where), e(col_summary(m, k)), body)
    ch = m.d['changes']
    ch_body = (''.join('<li class="pr-s-%s"%s>%s%s</li>' % (c['s'], m.pt(c.get('pt')), e(c['t']), ' <b class="pr-flag">%s</b>' % e(c['flag']) if c.get('flag') else '') for c in ch[:2])
               + ('<li class="pr-more">and %d more</li>' % (len(ch) - 2) if len(ch) > 2 else '')) if ch else '<li class="pr-ghost"><span>None yet</span></li>'
    ms = m.d['measures']
    conf = [x for x in ms if x['s'] == 'confirmed']; new = [x for x in ms if x['s'] != 'confirmed']
    ms_body = (''.join('<li class="pr-m-%s"%s>%s <b>%s</b></li>' % (x['s'], m.pt(x.get('pt')), e(x['t']), e(x['v'])) for x in conf)
               + ('<li class="pr-more">New, starting in the trial: %s</li>' % e(', '.join(x['t'].lower() for x in new)) if new else '')) if ms else '<li class="pr-ghost"><span>None yet</span></li>'
    rl = m.d['roles']
    rl_body = (''.join('<li%s>%s %s <b>%d to hire</b></li>' % (m.pt(r.get('pt')), seats(r), e(r['t']), r['seats']) for r in rl)) if rl else '<li class="pr-ghost"><span>None yet</span></li>'
    inner = ('%s%s<div class="pr-c-body"><div class="pr-c-left"%s>%s<ol class="pr-loop-names">%s</ol></div><div class="pr-cards">%s%s%s</div></div><div class="pr-foot">%s%s</div>') % (
        masthead(m), standing(m), m.pt(m.d['trial'].get('pt')), svg, names,
        card('roles', 'Team and role changes', 'At step 1, plan', rl_body), card('changes', 'Process changes', 'At step 2, try', ch_body),
        card('measures', 'Measures we watch', 'At step 3, measure', ms_body), pending(m), m.actions('pr-acts-col'))
    return canvas_wrap('lp-pr', 'lp-pr-c', inner, m.state)

SAMPLES = [('a', 'Ward board', 'Three columns on one board — changes, measures, roles — with the trial strip across the bottom.', sample_a),
           ('b', 'Readouts and seats', 'The measures as instrument readouts, the changes as a lane, the roles as seats to fill.', sample_b),
           ('c', 'The loop', 'Plan, try, measure, adjust, spread — each area pinned to where it sits on the loop.', sample_c)]

CSS = r'''
.lp-pr{--ground:#ECE8EE;--board:#FCFBFD;--ink:#2A1E30;--muted:#5A4D60;--plum:#6D4A77;--plum-l:#E9C8F0;--gold:#d4a94f;--amber:#8A5608;--green:#2F6B4F;--off:#9C92A1;
  background:var(--ground);color:var(--ink);padding:18px 32px 22px;display:flex;flex-direction:column;gap:14px}
.lp-pr .pr-label{font-size:13px;font-weight:600;color:var(--muted)}
.lp-pr .pr-mast{display:flex;justify-content:space-between;align-items:center;gap:18px}
.lp-pr .pr-id{display:flex;align-items:center;gap:14px}
.lp-pr .pr-emblem{width:46px;height:46px;color:var(--ink)}
.lp-pr .pr-eyebrow{font-size:13px;font-weight:500;color:var(--muted)}
.lp-pr .pr-tab{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:48px;line-height:.9;letter-spacing:.01em}
.lp-pr .pr-subs{font-size:12px;color:var(--plum);font-weight:500;margin-top:2px;white-space:nowrap}
.lp-pr .pr-stampw{display:flex;flex-direction:column;align-items:flex-end;gap:4px}
.lp-pr .lp-stamp{display:flex;align-items:center;gap:12px;background:var(--board);border:1.5px solid var(--ink);border-radius:24px;padding:5px 5px 5px 16px}
.lp-pr .lp-stamp-txt{display:flex;flex-direction:column} .lp-pr .lp-stamp-at{font-size:13px;font-weight:600;white-space:nowrap} .lp-pr .lp-stamp-since{font-size:12px;color:var(--muted)}
.lp-pr .lp-refresh{background:var(--plum);color:#fff;border:none;border-radius:20px;font-size:13px;font-weight:500}
.lp-pr .pr-mid{font-size:11.5px;color:var(--muted)}
.lp-pr .pr-claim{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:37px;line-height:.95;letter-spacing:.01em}
.lp-pr .pr-deck{margin-top:5px;font-size:14.5px;color:var(--muted);max-width:80ch;line-height:1.45}
.lp-pr .pr-ico{width:22px;height:22px;flex-shrink:0;color:var(--plum)}
.lp-pr .pr-flag{display:inline-block;margin-left:6px;font-size:10.5px;font-weight:600;padding:1px 7px;border:1.5px solid var(--amber);color:var(--amber);border-radius:10px;white-space:nowrap}
.lp-pr .pr-pend ul{display:flex;flex-direction:column;gap:7px;margin-top:7px}
.lp-pr .pr-pend-i{display:flex;gap:10px;font-size:14px;line-height:1.4}
.lp-pr .pr-pm{flex-shrink:0;width:14px;height:14px;margin-top:4px;border-radius:4px;border:2px solid var(--ink)}
.lp-pr .pr-who-you .pr-pm{border-style:dashed;border-color:var(--amber)}
.lp-pr .pr-need{display:block;font-size:12px;font-weight:600;color:var(--amber)}
.lp-pr .lp-acts{display:flex;gap:8px} .lp-pr .pr-acts-col{flex-direction:column}
.lp-pr .lp-act{justify-content:center;padding:6px 16px;min-height:52px;background:var(--board);border:1.5px solid var(--ink);border-radius:26px;font-size:14px}
.lp-pr .lp-act-d{font-size:12.5px;color:var(--muted)}
.lp-pr .lp-act-go{background:var(--plum);border-color:var(--plum);color:#fff} .lp-pr .lp-act-go .lp-act-d{color:#EBDDF0}
.lp-pr .lp-act-go{box-shadow:inset 6px 0 0 var(--gold)}
.lp-pr .lp-act:hover{border-color:var(--plum)}
.lp-pr .pr-foot{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:24px;align-items:start}
.lp-pr .pr-dot{flex-shrink:0;width:14px;height:14px;border-radius:50%;background:var(--plum);box-shadow:inset -2px -2px 0 rgba(0,0,0,.25);margin-top:2px}
.lp-pr .pr-s-new .pr-dot,.lp-pr .pr-m-new .pr-dot{background:var(--gold)}
.lp-pr .pr-m-confirmed .pr-dot{background:var(--green)}
.lp-pr .pr-ghost{border:1.5px dashed var(--off);border-radius:8px;padding:8px 10px;font-size:12.5px;color:var(--muted)}
.lp-pr .pr-seats{display:inline-flex;gap:4px;flex-shrink:0}
.lp-pr .pr-seat{width:22px;height:24px} .lp-pr .pr-seat path{fill:none;stroke:var(--plum);stroke-width:2;stroke-dasharray:3 2;stroke-linejoin:round}
.lp-pr .pr-seat.on path{fill:var(--plum);stroke-dasharray:none}
.lp-pr .pr-cost{font-size:12px;color:var(--muted);font-style:italic;border-top:1px dashed rgba(42,30,48,.3);padding-top:6px}
.lp-pr .pr-ph{display:flex;align-items:center;gap:8px} .lp-pr .pr-ph h4{margin:0;font-size:15px;font-weight:600} .lp-pr .pr-ph span{margin-left:auto;font-size:12px;color:var(--muted)}
/* A */
.lp-pr-a .pr-board{background:var(--board);border:1.5px solid var(--ink);border-radius:14px;box-shadow:0 6px 0 rgba(42,30,48,.12);overflow:hidden}
.lp-pr-a .pr-cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.lp-pr-a .pr-col{padding:10px 14px 12px;border-right:1.5px solid rgba(42,30,48,.14)} .lp-pr-a .pr-col:last-child{border-right:none}
.lp-pr-a .pr-col-h{display:flex;gap:9px;align-items:flex-start;padding-bottom:9px;margin-bottom:9px;border-bottom:2px solid var(--ink)}
.lp-pr-a .pr-col-h h4{margin:0;font-size:15px;font-weight:600;line-height:1.2} .lp-pr-a .pr-col-h span{font-size:11.5px;color:var(--muted)}
.lp-pr-a .pr-col ul{display:flex;flex-direction:column;gap:5px}
.lp-pr-a .pr-mag{display:flex;gap:8px;align-items:flex-start;font-size:12.5px;line-height:1.3;padding:4px 8px;background:#F4F0F6;border-radius:6px}
.lp-pr-a .pr-mt{flex:1} .lp-pr-a .pr-mv{font-weight:600;font-size:12px;text-align:right;max-width:44%}
.lp-pr-a .pr-m-new .pr-mv{font-weight:500;color:var(--amber)}
.lp-pr-a .pr-role{flex-direction:column;gap:5px} .lp-pr-a .pr-role b{display:block;font-size:13px} .lp-pr-a .pr-rn{font-size:12px;color:var(--muted)}
.lp-pr-a .pr-role > span:last-child{display:block}
.lp-pr-a .pr-strip{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr) auto;gap:16px;align-items:center;padding:9px 14px;background:var(--ink);color:#F3EEF5}
.lp-pr-a .pr-strip div:first-child{display:flex;flex-direction:column} .lp-pr-a .pr-strip b{font-size:14px} .lp-pr-a .pr-strip span{font-size:12px;color:#CFC3D4}
.lp-pr-a .pr-weeks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px} .lp-pr-a .pr-weeks i{font-style:normal;font-size:11px;text-align:center;padding:4px;border:1.5px dashed #9C92A1;border-radius:4px;color:#CFC3D4}
.lp-pr-a .pr-trial-s{font-size:12px;font-weight:600;color:var(--gold) !important;border:1.5px solid var(--gold);border-radius:12px;padding:3px 10px;white-space:nowrap}
/* B */
.lp-pr-b .pr-panel{background:var(--board);border:1.5px solid var(--ink);border-radius:14px;padding:10px 14px 12px;display:flex;flex-direction:column;gap:9px}
.lp-pr-b .pr-reads{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px}
.lp-pr-b .pr-read{display:flex;flex-direction:column;gap:4px}
.lp-pr-b .pr-rt{font-size:11.5px;font-weight:600;line-height:1.25;min-height:29px}
.lp-pr-b .pr-win{font-family:'Bebas Neue',sans-serif;font-size:21px;line-height:1;padding:9px 8px 7px;background:var(--ink);color:#F3EEF5;border-radius:6px;box-shadow:inset 0 0 0 2px #4A3A52;min-height:40px;display:flex;align-items:center}
.lp-pr-b .pr-m-new .pr-win{background:transparent;color:var(--muted);box-shadow:none;border:1.5px dashed var(--off)}
.lp-pr-b .pr-rs{font-size:11px;color:var(--muted)} .lp-pr-b .pr-m-confirmed .pr-rs{color:var(--green);font-weight:600}
.lp-pr-b .pr-b-row{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:14px}
.lp-pr-b .pr-lane{display:flex;flex-direction:column;gap:0;position:relative;padding-left:16px}
.lp-pr-b .pr-lane::before{content:'';position:absolute;left:5px;top:6px;bottom:6px;border-left:2px solid var(--plum)}
.lp-pr-b .pr-ln{position:relative;font-size:12.5px;line-height:1.35;padding:3px 0}
.lp-pr-b .pr-ln::before{content:'';position:absolute;left:-15px;top:8px;width:8px;height:8px;border-radius:50%;background:var(--plum)}
.lp-pr-b .pr-ln.pr-s-new::before{background:var(--gold)} .lp-pr-b .pr-ghost-ln{color:var(--muted)} .lp-pr-b .pr-ghost-ln::before{background:transparent;border:1.5px dashed var(--off)}
.lp-pr-b .pr-trial{font-size:12.5px;padding:6px 10px;border-radius:8px;background:#F4F0F6;color:var(--muted)} .lp-pr-b .pr-trial b{color:var(--ink)}
.lp-pr-b .pr-seatplan{display:flex;flex-direction:column;gap:9px}
.lp-pr-b .pr-seatplan li{display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:10px;align-items:center}
.lp-pr-b .pr-seatplan li b{font-size:13px} .lp-pr-b .pr-seatplan li > span:last-child{grid-column:2;font-size:12px;color:var(--muted)}
.lp-pr-b .pr-seatplan .pr-seats{grid-row:1/3} .lp-pr-b .pr-seatplan .pr-seat{width:28px;height:30px}
.lp-pr-b .pr-seatplan .pr-cost,.lp-pr-b .pr-seatplan .pr-ghost{display:block}
/* C */
.lp-pr-c .pr-c-body{display:grid;grid-template-columns:270px minmax(0,1fr);gap:20px;align-items:start}
.lp-pr-c .pr-c-left{display:flex;flex-direction:column;gap:8px}
.lp-pr-c .pr-loop{width:270px;height:270px}
.lp-pr-c .pr-arc{fill:none;stroke:var(--plum);stroke-width:3} .lp-pr-c .pr-ahp{fill:var(--plum)}
.lp-pr-c .pr-node circle{fill:var(--board);stroke:var(--ink);stroke-width:2.5} .lp-pr-c .pr-node text{font:700 14px Poppins,sans-serif;fill:var(--ink);text-anchor:middle}
.lp-pr-c .pr-node.is-at circle{fill:var(--gold);stroke:var(--ink)} .lp-pr-c .pr-node.is-done circle{fill:var(--ink)} .lp-pr-c .pr-node.is-done text{fill:#fff}
.lp-pr-c .pr-loop-c{font-family:'Bebas Neue',sans-serif;font-size:30px;fill:var(--ink);text-anchor:middle}
.lp-pr-c .pr-loop-s{font:500 12.5px Poppins,sans-serif;fill:var(--muted);text-anchor:middle}
.lp-pr-c .pr-loop-names{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 12px;font-size:12px}
.lp-pr-c .pr-loop-names li{display:flex;gap:6px;align-items:center} .lp-pr-c .pr-loop-names span{width:20px;height:20px;border-radius:50%;border:1.5px solid var(--ink);display:flex;align-items:center;justify-content:center;font-size:10.5px;font-weight:700}
.lp-pr-c .pr-loop-names .is-at span{background:var(--gold)} .lp-pr-c .pr-loop-names .is-at{font-weight:600}
.lp-pr-c .pr-cards{display:flex;flex-direction:column;gap:8px}
.lp-pr-c .pr-card{background:var(--board);border:1.5px solid var(--ink);border-radius:14px;padding:7px 14px 9px;display:flex;flex-direction:column;gap:3px;position:relative}
.lp-pr-c .pr-card::before{content:'';position:absolute;left:-21px;top:18px;width:20px;border-top:2px dashed var(--plum)}
.lp-pr-c .pr-card em{margin-left:auto;font-style:normal;font-size:11.5px;font-weight:600;color:var(--plum)}
.lp-pr-c .pr-cs{font-size:11.5px;color:var(--muted)}
.lp-pr-c .pr-card ul{display:flex;flex-direction:column;gap:3px}
.lp-pr-c .pr-card li{font-size:12.5px;line-height:1.35;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.lp-pr-c .pr-card li b{font-weight:600} .lp-pr-c .pr-card .pr-m-new b{color:var(--amber);font-weight:500}
.lp-pr-c .pr-card .pr-more{color:var(--muted);font-style:italic}
.lp-pr-c .pr-card .pr-seat{width:18px;height:20px}
/* first visit */
.lp-pr[data-lp-state=empty] .pr-claim{color:var(--muted)}
/* narrow */
@container lp (max-width:699px){
  .lp-pr{padding:16px 14px 22px;gap:16px}
  .lp-pr .pr-mast{flex-direction:column;align-items:stretch;gap:12px}
  .lp-pr .pr-stampw{align-items:stretch} .lp-pr .lp-stamp{justify-content:space-between}
  .lp-pr .pr-tab{font-size:42px} .lp-pr .pr-claim{font-size:34px}
  .lp-pr .pr-subs,.lp-pr .lp-stamp-at{white-space:normal}
  .lp-pr .lp-acts{flex-direction:column} .lp-pr .pr-foot{grid-template-columns:minmax(0,1fr)}
  .lp-pr-a .pr-cols{grid-template-columns:minmax(0,1fr)} .lp-pr-a .pr-col{border-right:none;border-bottom:1.5px solid rgba(42,30,48,.14)}
  .lp-pr-a .pr-strip{grid-template-columns:minmax(0,1fr) auto} .lp-pr-a .pr-weeks{display:none}
  .lp-pr-b .pr-reads{grid-template-columns:repeat(2,minmax(0,1fr))} .lp-pr-b .pr-b-row{grid-template-columns:minmax(0,1fr)}
  .lp-pr-c .pr-c-body{grid-template-columns:minmax(0,1fr)} .lp-pr-c .pr-c-left{align-items:center} .lp-pr-c .pr-card::before{display:none}
}
'''
