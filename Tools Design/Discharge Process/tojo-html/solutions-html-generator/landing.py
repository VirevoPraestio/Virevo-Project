"""
Solutions tab — landing page samples.
Look: the drafting table. Pale blueprint ground with a faint grid, navy ink, drawing sheets with
corner marks, revision triangles for each time a solution is redrawn, and a title block that holds
the update stamp. Sentence-case labels (the Diagnosis tab keeps its uppercase ones).
  A  Drawing sheets    each solution is a sheet; earlier revisions sit behind it like tracing paper
  B  Iteration tracks  each solution travels from idea to agreed; revision marks sit on its track
  C  Revision log      what was redrawn and why, beside a register of every solution
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'landing-common'))
from landing_common import e, canvas_wrap  # noqa: E402

TAB = 'Solutions'
THEME = {'ground': '#E3EAF0', 'rail_bg': '#15304D', 'rail_fg': '#F1D493'}

STATUS = {'agreed': 'Agreed', 'shaping': 'Being shaped', 'new': 'New', 'waiting': 'Waiting on you', 'blank': 'Not started', 'idea': 'Idea', 'parked': 'Parked'}
STAGES = ['Idea', 'Shaped', 'Tested with you', 'Agreed']
STAGE_OF = {'new': 0, 'waiting': 0, 'idea': 0, 'parked': 0, 'shaping': 1, 'agreed': 3, 'blank': -1}

DATA = {
    'filled': {
        'stamp': {'at': 'Brought up to date at midnight, 28 September', 'since': '1 conversation since then is not in yet',
                  'fresh': 'Brought up to date just now, 9:42 AM', 'fresh_since': 'Everything you have said is in'},
        'standing': 'Five solutions on the table. Two are agreed.',
        'deck': 'Each comes from a cause Diagnosis found, is tested against what it depends on, and is redrawn when something changes.',
        'solutions': [
            {'n': 1, 'title': 'Start the going-home work on the evening round', 'rev': 2, 'status': 'agreed', 'from': 'Hours nobody uses overnight',
             'changed': 'Start with the consultants who decide latest', 'why': 'Your real times', 'when': '28 Sep',
             'cons': [('Doctors sign only an early summary in the evening', 1, 'People'), ('Decisions come anywhere from 6 to 9 PM', 1, 'Timing'),
                      ('Cash and insured patients leave at different times', 0, 'Patients')]},
            {'n': 2, 'title': 'Papers and bill that prepare themselves', 'rev': 1, 'status': 'shaping', 'from': 'Hours nobody uses overnight',
             'changed': 'Bill kept up to date from the first day', 'why': 'Your billing times', 'when': '26 Sep',
             'cons': [('Your IT team must link the hospital software first', 0, 'Systems'), ('Typists have the most to give up', 0, 'People'),
                      ('Doctors sign on a phone', 1, 'Systems')]},
            {'n': 3, 'title': 'One person in charge of discharge', 'rev': 2, 'status': 'agreed', 'from': 'Nobody in charge',
             'changed': 'Two helpers, not three, sized to your busy hours', 'why': 'Your busy hours', 'when': '26 Sep',
             'cons': [('Costs ₹10 to 11.5 lakh a year', 1, 'Cost'), ('Head of Operations must approve', 0, 'People')]},
            {'n': 4, 'title': 'Get the bed ready sooner after the patient leaves', 'rev': 0, 'status': 'new', 'from': 'Bed empty for 75 minutes',
             'changed': 'Your real times showed the bed empty for 75 minutes', 'why': '', 'when': '28 Sep',
             'cons': [('Housekeeping staff on each shift', 0, 'People'), ('The bed desk needs real times', 0, 'Systems')]},
            {'n': 5, 'title': 'Separate discharge work from admission work', 'rev': 0, 'status': 'waiting', 'from': 'A question still open',
             'changed': 'Opened by a question Diagnosis still has to ask', 'why': '', 'when': '25 Sep',
             'cons': [('Only needed if one team does both today', 0, 'People')]},
        ],
        'pending': [
            {'text': 'Redraw the evening plan for consultants who decide after 8 PM.', 'who': 'tojo', 'pt': 1},
            {'text': 'Weigh cash and insured patients separately.', 'who': 'tojo', 'pt': 1},
            {'text': 'Draft the case for your Head of Operations.', 'who': 'tojo', 'pt': 3},
            {'text': 'Ask if one team does both discharges and admissions.', 'who': 'you', 'need': 'Needs your answer', 'pt': 5},
        ],
        'actions': {'go': {'detail': 'Settle the open points on the paperwork', 'say': 'Let’s settle the open points on the paperwork'},
                    'add': {'detail': 'Add a solution or a worry of your own', 'say': 'I want to add a solution: '},
                    'jump': {'tab': 'Automations', 'detail': 'Two solutions run as automations', 'say': 'Take me to Automations'}},
        'chat': {'text': ['Here’s where the solutions stand. Two are agreed, two are being shaped, and your real times raised a new one.',
                          'Seven points are still open. The paperwork has the most of them.'],
                 'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
                 'note': 'A solution is only as good as what it depends on.',
                 'points': [{'n': 1, 'label': 'Starting on the evening round'}, {'n': 2, 'label': 'Papers and bill that prepare themselves'},
                            {'n': 3, 'label': 'One person in charge'}, {'n': 4, 'label': 'Getting the bed ready sooner'},
                            {'n': 5, 'label': 'Separating discharge and admission work'}],
                 'prompts': ['Let’s settle the paperwork’s open points', 'What if our IT team can’t link the systems?', 'What changed since yesterday?']},
    },
    'empty': {
        'stamp': {'at': 'Nothing to bring up to date yet', 'since': 'This page fills in as Diagnosis finds causes',
                  'fresh': 'Checked just now, 9:42 AM', 'fresh_since': 'No solutions yet'},
        'standing': 'No solutions yet',
        'deck': 'Solutions appear here as Diagnosis finds what causes the delay. You can also bring one of your own to test.',
        'solutions': [
            {'n': None, 'title': 'Appears once Diagnosis names a cause', 'rev': 0, 'status': 'blank', 'from': '—', 'changed': '', 'why': '', 'when': '', 'cons': []},
            {'n': None, 'title': 'Appears once Diagnosis names a cause', 'rev': 0, 'status': 'blank', 'from': '—', 'changed': '', 'why': '', 'when': '', 'cons': []},
            {'n': None, 'title': 'Or one you bring yourself', 'rev': 0, 'status': 'blank', 'from': '—', 'changed': '', 'why': '', 'when': '', 'cons': []},
        ],
        'pending': [
            {'text': 'Wait for Diagnosis to name what causes the delay.', 'who': 'tojo'},
            {'text': 'Turn each cause into one or more solutions.', 'who': 'tojo'},
            {'text': 'Work through what each one depends on: cost, people, systems, patients and timing.', 'who': 'tojo'},
        ],
        'actions': {'go': {'detail': 'Begin in Diagnosis', 'say': 'Take me to Diagnosis'},
                    'add': {'detail': 'Add a solution you already have in mind', 'say': 'I already have a solution in mind: '},
                    'jump': {'tab': 'Automations', 'detail': 'Fills in once solutions are agreed', 'say': 'Take me to Automations'}},
        'chat': {'text': ['This is your Solutions page. Nothing is on it yet.',
                          'Solutions appear as Diagnosis finds the causes. If you already have one in mind, add it and we’ll test it.'],
                 'note': 'Every solution starts with a cause.', 'points': [],
                 'prompts': ['Start with the diagnosis', 'I already have a solution in mind', 'What kinds of solutions are there?']},
    },
}

LENSES = ['Cost', 'People', 'Systems', 'Patients', 'Timing']

# --- shared pieces ---------------------------------------------------------------------------
BULB = ('<svg class="so-emblem" viewBox="0 0 48 48" aria-hidden="true"><path d="M17 36h14M19 42h10" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M24 5a13 13 0 00-8 23.2c1.5 1.4 2 2.8 2 4.8h12c0-2 .5-3.4 2-4.8A13 13 0 0024 5z" fill="none" stroke="currentColor" stroke-width="3"/>'
        '<path d="M24 12v6M24 18l-4 5M24 18l4 5" stroke="#d4a94f" stroke-width="2.4" stroke-linecap="round"/><circle cx="24" cy="18" r="2" fill="#d4a94f"/></svg>')

def tri(n, cls=''):
    """A drafting revision triangle carrying the revision number."""
    return ('<span class="so-tri %s" title="Revision %d"><svg viewBox="0 0 26 23" aria-hidden="true"><path d="M13 2L24.5 21.5H1.5z"/></svg><b>%d</b><span class="sr">Revision %d</span></span>' % (cls, n, n, n))

def masthead(m):
    """Title-block masthead: emblem and name on the left; the drawing's title block (the update stamp) on the right."""
    return ('<header class="so-mast"><div class="so-id">%s<div><div class="so-eyebrow">Discharge Process</div><h2 class="so-tab">Solutions</h2></div></div>'
            '<div class="so-block"><div class="so-block-l">Updated every night at midnight</div>%s</div></header>' % (BULB, m.stamp()))

def standing(m):
    return '<div class="so-stand"><h3 class="so-claim">%s</h3><p class="so-deck">%s</p></div>' % (e(m.d['standing']), e(m.d['deck']))

def cons_list(s, m):
    return '<ul class="so-cons">%s</ul>' % ''.join(
        '<li class="so-c-%s"><span class="so-cm" aria-hidden="true"></span><span>%s</span><span class="sr">%s</span></li>' % ('ok' if ok else 'open', e(t), 'settled' if ok else 'still open')
        for t, ok, _ in s['cons'])

def counts(m):
    c = [x for s in m.d['solutions'] for x in s['cons']]
    return sum(1 for x in c if x[1]), sum(1 for x in c if not x[1])

def pending(m):
    items = []
    for p in m.d['pending']:
        need = '<span class="so-need">%s</span>' % e(p['need']) if p.get('need') else ''
        items.append('<li class="so-pend-i so-who-%s"%s><span class="so-pm" aria-hidden="true"></span><span>%s%s</span></li>' % (p['who'], m.pt(p.get('pt')), e(p['text']), need))
    return '<section class="so-pend"><div class="so-label">What Tojo still has to do</div><ul>%s</ul></section>' % ''.join(items)

def status_chip(s):
    return '<span class="so-chip so-st-%s">%s</span>' % (s['status'], STATUS[s['status']])

# --- Sample A: drawing sheets ------------------------------------------------------------------
def sheet(s, m):
    layers = ''.join('<span class="so-layer" style="--k:%d" aria-hidden="true"></span>' % k for k in range(min(s['rev'], 2), 0, -1))
    head = ('<div class="so-sh-head"><span class="so-sh-n">%s</span>%s%s</div>' % (
        'Solution %d' % s['n'] if s['n'] else 'Empty sheet', tri(s['rev']) if s['n'] else '', status_chip(s)))
    body = ('<h4 class="so-sh-t">%s</h4>' % e(s['title']))
    if s['n']:
        body += '<div class="so-from">From: %s</div>%s' % (e(s['from']), cons_list(s, m))
    return '<article class="so-sheet so-st-%s"%s>%s<div class="so-sh-in">%s%s</div></article>' % (s['status'], m.pt(s['n']), layers, head, body)

def sample_a(m):
    ok, op = counts(m)
    tally = ''
    if m.state == 'filled':
        tally = ('<div class="so-tally"><div class="so-label">What the solutions depend on</div><div class="so-dim"><span class="so-dim-ok" style="flex:%d">%d settled</span>'
                 '<span class="so-dim-open" style="flex:%d">%d still open</span></div><p>Settled points hold unless something changes. Open ones need you or Tojo.</p></div>') % (ok, ok, op, op)
    inner = ('%s%s<div class="so-sheets">%s%s</div><div class="so-a-foot">%s%s</div>' % (
        masthead(m), standing(m), ''.join(sheet(s, m) for s in m.d['solutions']), tally, pending(m), m.actions('so-acts-col')))
    return canvas_wrap('lp-so', 'lp-so-a', inner, m.state)

# --- Sample B: iteration tracks ----------------------------------------------------------------
def track(s, m):
    at = STAGE_OF[s['status']]
    stops = ''.join('<li class="%s"><span class="so-tk-dot"></span><span class="so-tk-l">%s</span></li>' % (
        'is-done' if i < at else ('is-at' if i == at else ''), e(n)) for i, n in enumerate(STAGES))
    revs = ''
    if s['n'] and s['rev']:
        revs = '<div class="so-tk-rev">%s<span>%s</span></div>' % (tri(s['rev']), e(s['changed']))
    elif s['n']:
        revs = '<div class="so-tk-rev so-tk-rev0"><span>%s</span></div>' % e(s['changed'])
    ok = sum(1 for c in s['cons'] if c[1]); op = len(s['cons']) - ok
    marks = ''.join('<i class="so-m-ok"></i>' for _ in range(ok)) + ''.join('<i class="so-m-open"></i>' for _ in range(op))
    dep = ('<div class="so-tk-dep"><span class="so-marks" aria-hidden="true">%s</span><span>%d of %d settled</span></div>' % (marks, ok, len(s['cons']))) if s['n'] else '<div class="so-tk-dep"><span>—</span></div>'
    return ('<li class="so-tk so-st-%s"%s><div class="so-tk-name"><span class="so-tk-n">%s</span><span class="so-tk-t">%s</span>%s</div>'
            '<ol class="so-tk-line" aria-label="Stage">%s</ol>%s</li>') % (s['status'], m.pt(s['n']), s['n'] or '·', e(s['title']), revs, stops, dep)

def sample_b(m):
    head = ('<div class="so-tk-head" aria-hidden="true"><span>Solution</span><span class="so-tk-scale">%s</span><span>Depends on</span></div>' %
            ''.join('<b>%s</b>' % e(x) for x in STAGES))
    inner = ('%s%s<section class="so-tracks">%s<ol>%s</ol></section><div class="so-b-foot">%s%s</div>' % (
        masthead(m), standing(m), head, ''.join(track(s, m) for s in m.d['solutions']), pending(m), m.actions('so-acts-col')))
    return canvas_wrap('lp-so', 'lp-so-b', inner, m.state)

# --- Sample C: revision log and register --------------------------------------------------------
def sample_c(m):
    sols = m.d['solutions']
    if m.state == 'filled':
        log = sorted([s for s in sols], key=lambda s: s['when'], reverse=True)[:4]
        logs = ''.join('<li%s><span class="so-lg-when">%s</span>%s<div><b>%s</b><span>%s.%s</span></div></li>' % (
            m.pt(s['n']), e(s['when']), tri(s['rev'], 'so-tri-s') if s['rev'] else '<span class="so-new">New</span>',
            e(s['title']), e(s['changed']), ' Because of ' + e(s['why'].lower()) + '.' if s['why'] else '') for s in log)
    else:
        logs = '<li class="so-lg-empty"><div><b>Nothing redrawn yet</b><span>Every change to a solution is logged here, with what caused it.</span></div></li>'
    reg = []
    for s in sols:
        ok = sum(1 for c in s['cons'] if c[1]); tot = len(s['cons'])
        bar = ('<span class="so-rg-bar" aria-label="%d of %d settled"><span style="width:%d%%"></span></span>' % (ok, tot, 100 * ok // tot)) if tot else '<span class="so-rg-bar"></span>'
        lens = ' · '.join(sorted({c[2] for c in s['cons']}, key=LENSES.index)) if s['cons'] else 'Cost, people, systems, patients, timing'
        reg.append('<li class="so-rg so-st-%s"%s><span class="so-rg-n">%s</span><div class="so-rg-b"><div class="so-rg-t">%s</div><div class="so-rg-l">%s</div></div>'
                   '<div class="so-rg-r">%s%s</div></li>' % (s['status'], m.pt(s['n']), s['n'] or '·', e(s['title']), e(lens), status_chip(s), bar))
    inner = ('%s%s<div class="so-c-body"><section class="so-log"><div class="so-label">Redrawn lately</div><ol>%s</ol></section>'
             '<section class="so-reg"><div class="so-label">Every solution</div><ol>%s</ol></section></div><div class="so-c-foot">%s%s</div>') % (
        masthead(m), standing(m), logs, ''.join(reg), pending(m), m.actions('so-acts-row'))
    return canvas_wrap('lp-so', 'lp-so-c', inner, m.state)

SAMPLES = [('a', 'Drawing sheets', 'Each solution is a drawing sheet; revisions stack behind it like tracing paper.', sample_a),
           ('b', 'Iteration tracks', 'Each solution travels from idea to agreed, with its revision marked on the way.', sample_b),
           ('c', 'Revision log', 'What was redrawn lately and why, beside a register of every solution.', sample_c)]

CSS = r'''
.lp-so{--ground:#E3EAF0;--sheet:#F8FAFC;--ink:#15304D;--muted:#4A5D72;--line:#2E5E8E;--grid:rgba(21,48,77,.07);--gold:#d4a94f;--gold-t:#6B4F16;--amber:#8A5608;--green:#2F6B4F;
  background-color:var(--ground);background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:24px 24px;
  color:var(--ink);padding:18px 32px 22px;display:flex;flex-direction:column;gap:14px}
.lp-so .so-label{font-size:13px;font-weight:600;color:var(--muted)}
.lp-so .so-mast{display:flex;justify-content:space-between;align-items:stretch;gap:18px}
.lp-so .so-id{display:flex;align-items:center;gap:14px}
.lp-so .so-emblem{width:44px;height:44px;color:var(--ink)}
.lp-so .so-eyebrow{font-size:13px;font-weight:500;color:var(--muted)}
.lp-so .so-tab{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:48px;line-height:.9;letter-spacing:.01em}
.lp-so .so-block{border:1.5px solid var(--ink);background:var(--sheet);display:grid;grid-template-columns:auto auto;align-items:center;column-gap:14px;padding:5px 6px 6px 12px;position:relative}
.lp-so .so-block-l{grid-column:1/-1;font-size:11px;font-weight:600;color:var(--muted);border-bottom:1px solid rgba(21,48,77,.25);padding-bottom:3px;margin-bottom:5px}
.lp-so .so-block .lp-stamp{display:contents}
.lp-so .lp-stamp-txt{display:flex;flex-direction:column}
.lp-so .lp-stamp-at{font-size:13px;font-weight:600} .lp-so .lp-stamp-since{font-size:12px;color:var(--muted)}
.lp-so .lp-refresh{background:var(--ink);color:#F8FAFC;border:none;border-radius:2px;font-size:13px;font-weight:500}
.lp-so .lp-refresh:hover{background:var(--line)}
.lp-so .so-claim{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:37px;line-height:.95;letter-spacing:.01em}
.lp-so .so-deck{margin-top:5px;font-size:14.5px;color:var(--muted);max-width:78ch;line-height:1.45}
.lp-so .so-tri{position:relative;display:inline-flex;width:26px;height:23px;align-items:flex-end;justify-content:center;flex-shrink:0}
.lp-so .so-tri svg{position:absolute;inset:0;width:100%;height:100%} .lp-so .so-tri path{fill:var(--sheet);stroke:var(--ink);stroke-width:1.6;stroke-linejoin:round}
.lp-so .so-tri b{position:relative;font-size:11px;font-weight:700;line-height:1;padding-bottom:3px}
.lp-so .so-chip{font-size:11.5px;font-weight:600;padding:2px 9px;border-radius:12px;border:1.5px solid var(--ink);white-space:nowrap}
.lp-so .so-chip.so-st-agreed{background:var(--ink);color:#F8FAFC}
.lp-so .so-chip.so-st-shaping{border-color:var(--line);color:var(--line)}
.lp-so .so-chip.so-st-new{background:var(--gold);border-color:var(--gold);color:#2b2008}
.lp-so .so-chip.so-st-waiting{border-style:dashed;border-color:var(--amber);color:var(--amber)}
.lp-so .so-chip.so-st-idea,.lp-so .so-chip.so-st-parked{border-style:dashed;color:var(--muted);border-color:rgba(21,48,77,.4)}
.lp-so .so-chip.so-st-blank{border-style:dashed;color:var(--muted);border-color:rgba(21,48,77,.4)}
.lp-so .so-cons{display:flex;flex-direction:column;gap:4px}
.lp-so .so-cons li{display:flex;gap:8px;font-size:12.5px;line-height:1.35}
.lp-so .so-cm{flex-shrink:0;width:13px;height:13px;margin-top:2px;border:1.6px solid var(--ink);border-radius:50%}
.lp-so .so-c-ok .so-cm{background:var(--ink);box-shadow:inset 0 0 0 2.5px var(--sheet)}
.lp-so .so-c-open .so-cm{border-style:dashed;border-color:var(--amber)}
.lp-so .so-pend ul{display:flex;flex-direction:column;gap:7px;margin-top:7px}
.lp-so .so-pend-i{display:flex;gap:10px;font-size:14px;line-height:1.4}
.lp-so .so-pm{flex-shrink:0;width:14px;height:14px;margin-top:4px;border:1.8px solid var(--ink);transform:rotate(45deg)}
.lp-so .so-who-you .so-pm{border-style:dashed;border-color:var(--amber)}
.lp-so .so-need{display:block;font-size:12px;font-weight:600;color:var(--amber)}
.lp-so .lp-acts{display:flex;gap:8px}
.lp-so .so-acts-col{flex-direction:column}
.lp-so .lp-act{justify-content:center;padding:6px 16px;min-height:52px;border:1.5px solid var(--ink);background:var(--sheet);border-radius:2px;font-size:14px;position:relative}
.lp-so .lp-act-d{font-size:12.5px;color:var(--muted)}
.lp-so .lp-act-go{background:var(--ink);color:#F8FAFC} .lp-so .lp-act-go .lp-act-d{color:#C9D6E3}
.lp-so .lp-act-go::after{content:'';position:absolute;right:14px;top:50%;width:18px;border-top:2px solid var(--gold)}
.lp-so .lp-act:hover{border-color:var(--line)}
/* A: sheets */
.lp-so-a .so-sheets{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px 16px}
.lp-so-a .so-sheet{position:relative;margin:0 8px 8px 0}
.lp-so-a .so-layer{position:absolute;inset:0;transform:translate(calc(var(--k) * 4px),calc(var(--k) * 4px));background:var(--sheet);border:1.2px solid rgba(21,48,77,.45)}
.lp-so-a .so-sh-in{position:relative;background:var(--sheet);border:1.5px solid var(--ink);padding:8px 12px 10px;height:100%;display:flex;flex-direction:column;gap:4px}
.lp-so-a .so-sh-in::before,.lp-so-a .so-sh-in::after{content:'';position:absolute;width:9px;height:9px;border:1.5px solid var(--line)}
.lp-so-a .so-sh-in::before{top:3px;left:3px;border-right:none;border-bottom:none} .lp-so-a .so-sh-in::after{bottom:3px;right:3px;border-left:none;border-top:none}
.lp-so-a .so-sh-head{display:flex;align-items:center;gap:8px} .lp-so-a .so-sh-n{font-size:12px;font-weight:600;color:var(--muted);margin-right:auto}
.lp-so-a .so-sh-t{margin:0;font-size:14.5px;font-weight:600;line-height:1.3}
.lp-so-a .so-from{font-size:11.5px;color:var(--line);font-style:italic}
.lp-so-a .so-sheet.so-st-new .so-sh-in{border-color:var(--gold);box-shadow:0 0 0 3px rgba(212,169,79,.25)}
.lp-so-a .so-sheet.so-st-blank .so-sh-in{border-style:dashed;background:transparent;min-height:110px} .lp-so-a .so-st-blank .so-sh-t{color:var(--muted);font-weight:500}
.lp-so-a .so-tally{border:1.5px dashed var(--ink);padding:10px 12px;display:flex;flex-direction:column;gap:8px;margin:0 8px 8px 0;font-size:12.5px;color:var(--muted);line-height:1.4}
.lp-so-a .so-dim{display:flex;gap:4px;position:relative;padding:0 8px}
.lp-so-a .so-dim::before,.lp-so-a .so-dim::after{content:'';position:absolute;top:-4px;bottom:-4px;border-left:1.5px solid var(--ink)} .lp-so-a .so-dim::before{left:0} .lp-so-a .so-dim::after{right:0}
.lp-so-a .so-dim span{font-size:12px;font-weight:600;text-align:center;padding:5px 4px;white-space:nowrap}
.lp-so-a .so-dim-ok{background:var(--ink);color:#F8FAFC} .lp-so-a .so-dim-open{border:1.5px dashed var(--amber);color:var(--amber)}
.lp-so-a .so-a-foot,.lp-so-b .so-b-foot{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:24px;align-items:start}
/* B: tracks */
.lp-so-b .so-tracks{background:var(--sheet);border:1.5px solid var(--ink);padding:6px 16px 8px}
.lp-so-b .so-tk-head,.lp-so-b .so-tk{display:grid;grid-template-columns:minmax(0,1.75fr) minmax(0,1fr) 104px;column-gap:16px;align-items:center}
.lp-so-b .so-tk-head{font-size:11.5px;font-weight:600;color:var(--muted);padding:6px 0;border-bottom:1.5px solid var(--ink)}
.lp-so-b .so-tk-scale{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));text-align:center} .lp-so-b .so-tk-scale b{font-weight:600}
.lp-so-b .so-tk{padding:7px 0;border-bottom:1px dashed rgba(21,48,77,.3)} .lp-so-b .so-tk:last-child{border-bottom:none}
.lp-so-b .so-tk-name{display:grid;grid-template-columns:24px minmax(0,1fr);column-gap:8px;row-gap:3px;align-items:start}
.lp-so-b .so-tk-n{width:24px;height:24px;border:1.5px solid var(--ink);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700}
.lp-so-b .so-tk-t{font-size:13.5px;font-weight:600;line-height:1.3}
.lp-so-b .so-tk-rev{grid-column:2;display:flex;align-items:center;gap:6px;font-size:12px;color:var(--line);line-height:1.3} .lp-so-b .so-tk-rev .so-tri{transform:scale(.85)}
.lp-so-b .so-tk-line{position:relative;display:grid;grid-template-columns:repeat(4,minmax(0,1fr))}
.lp-so-b .so-tk-line::before{content:'';position:absolute;left:12.5%;right:12.5%;top:8px;border-top:1.5px solid var(--ink)}
.lp-so-b .so-tk-line::after{content:'';position:absolute;right:calc(12.5% - 6px);top:3px;border:6px solid transparent;border-left:9px solid var(--ink);border-right:none}
.lp-so-b .so-tk-line li{display:flex;flex-direction:column;align-items:center;position:relative}
.lp-so-b .so-tk-dot{width:17px;height:17px;border-radius:50%;background:var(--sheet);border:1.5px solid rgba(21,48,77,.45);position:relative;z-index:1}
.lp-so-b .so-tk-l{display:none}
.lp-so-b .is-done .so-tk-dot{background:var(--ink);border-color:var(--ink)}
.lp-so-b .is-at .so-tk-dot{background:var(--gold);border:2px solid var(--ink);width:21px;height:21px;margin-top:-2px}
.lp-so-b .so-st-agreed .is-at .so-tk-dot{background:var(--ink);box-shadow:0 0 0 4px rgba(212,169,79,.6)}
.lp-so-b .so-st-waiting .is-at .so-tk-dot{background:var(--sheet);border-style:dashed;border-color:var(--amber)}
.lp-so-b .so-tk-dep{display:flex;flex-direction:column;gap:3px;font-size:12px;color:var(--muted)}
.lp-so-b .so-marks{display:flex;gap:3px} .lp-so-b .so-marks i{width:12px;height:12px;border-radius:50%;border:1.6px solid var(--ink)}
.lp-so-b .so-marks .so-m-ok{background:var(--ink)} .lp-so-b .so-marks .so-m-open{border-style:dashed;border-color:var(--amber)}
/* C: log and register */
.lp-so-c .so-c-body{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:22px;align-items:start}
.lp-so-c .so-log ol{margin-top:8px;position:relative;display:flex;flex-direction:column;gap:10px;padding-left:4px}
.lp-so-c .so-log ol::before{content:'';position:absolute;left:68px;top:8px;bottom:8px;border-left:1.5px dashed var(--line)}
.lp-so-c .so-log li{display:grid;grid-template-columns:48px 34px minmax(0,1fr);column-gap:8px;align-items:start;position:relative}
.lp-so-c .so-lg-when{font-size:11.5px;font-weight:600;color:var(--muted);padding-top:4px;white-space:nowrap}
.lp-so-c .so-log li > div{background:var(--sheet);border:1.5px solid var(--ink);padding:7px 10px;display:flex;flex-direction:column;gap:2px}
.lp-so-c .so-log b{font-size:13px;font-weight:600;line-height:1.3} .lp-so-c .so-log li span{font-size:12px;color:var(--muted);line-height:1.35}
.lp-so-c .so-new{display:inline-flex;align-items:center;justify-content:center;height:22px;padding:0 5px;font-size:10.5px;font-weight:700;background:var(--gold);color:#2b2008 !important}
.lp-so-c .so-lg-empty{grid-template-columns:minmax(0,1fr) !important} .lp-so-c .so-lg-empty > div{border-style:dashed !important;background:transparent !important}
.lp-so-c .so-log:has(.so-lg-empty) ol::before{display:none}
.lp-so-c .so-reg ol{margin-top:8px;background:var(--sheet);border:1.5px solid var(--ink)}
.lp-so-c .so-rg{display:grid;grid-template-columns:28px minmax(0,1fr) auto;column-gap:10px;align-items:center;padding:8px 12px;border-bottom:1px solid rgba(21,48,77,.2)}
.lp-so-c .so-rg:last-child{border-bottom:none}
.lp-so-c .so-rg-n{font-family:'Bebas Neue',sans-serif;font-size:24px;line-height:1;color:var(--line)}
.lp-so-c .so-rg-t{font-size:13.5px;font-weight:600;line-height:1.3} .lp-so-c .so-rg-l{font-size:11.5px;color:var(--muted)}
.lp-so-c .so-rg-r{display:flex;flex-direction:column;align-items:flex-end;gap:5px}
.lp-so-c .so-rg-bar{width:84px;height:6px;border:1px solid var(--ink);display:block} .lp-so-c .so-rg-bar span{display:block;height:100%;background:var(--ink)}
.lp-so-c .so-st-blank .so-rg-t{color:var(--muted);font-weight:500}
.lp-so-c .so-c-foot{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:22px;align-items:start}
.lp-so-c .so-acts-row{flex-direction:column}
/* first visit */
.lp-so[data-lp-state=empty] .so-claim{color:var(--muted)}
/* narrow */
@container lp (max-width:699px){
  .lp-so{padding:16px 14px 22px;gap:16px}
  .lp-so .so-mast{flex-direction:column;align-items:stretch;gap:12px}
  .lp-so .so-tab{font-size:42px} .lp-so .so-claim{font-size:34px}
  .lp-so .lp-acts{flex-direction:column}
  .lp-so-a .so-sheets{grid-template-columns:minmax(0,1fr)}
  .lp-so-a .so-a-foot,.lp-so-b .so-b-foot,.lp-so-c .so-c-body,.lp-so-c .so-c-foot{grid-template-columns:minmax(0,1fr)}
  .lp-so-b .so-tracks{padding:4px 12px}
  .lp-so-b .so-tk-head{display:none}
  .lp-so-b .so-tk{grid-template-columns:minmax(0,1fr);row-gap:8px;padding:12px 0}
  .lp-so-b .so-tk-l{display:block;font-size:10.5px;color:var(--muted);margin-top:3px;text-align:center;line-height:1.2}
  .lp-so-b .so-tk-dep{flex-direction:row;align-items:center;gap:8px}
  .lp-so-c .so-rg{grid-template-columns:24px minmax(0,1fr);row-gap:6px} .lp-so-c .so-rg-r{grid-column:2;flex-direction:row;align-items:center;justify-content:space-between}
}
'''
