"""
Diagnosis tab — landing page samples (A: route walked, B: case sheet, C: the lens).
The same look as the Diagnosis canvas: route map on sage, forest ink, gold for "now",
uppercase Poppins labels, Bebas titles, 2px ink borders and flat offset shadows.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'landing-common'))
from landing_common import e, canvas_wrap  # noqa: E402

TAB = 'Diagnosis'
THEME = {'ground': '#DCE3DA', 'rail_bg': '#10241a', 'rail_fg': '#d4a94f'}

STOPS = [('A', 'The doctors'), ('B', 'Supply count'), ('C', 'Pharmacy returns'), ('D', 'Billing'), ('E', 'Insurance desk'), ('F', 'Bed desk'),
         ('G', 'Housekeeping'), ('H', 'Transport'), ('I', 'Operating theatre'), ('J', 'Family briefing'), ('K', 'Cash counter')]
STAGES = ['Walk the chain', 'Price the wait', 'Name the cause', 'Check real times', 'Last stops']

DATA = {
    'filled': {
        'stamp': {'at': 'Brought up to date at midnight, 28 September', 'since': '2 conversations since then are not in yet',
                  'fresh': 'Brought up to date just now, 9:42 AM', 'fresh_since': 'Everything you have said is in'},
        'standing': 'Unused hours overnight, and nobody in charge',
        'deck': 'The cause is named and your real times back it up. Four stops are still to walk.',
        'stops': {'A': 'done', 'B': 'done', 'C': 'done', 'D': 'done', 'E': 'done', 'F': 'done', 'G': 'now', 'H': 'later', 'I': 'later', 'J': 'later', 'K': 'done'},
        'stages': ['done', 'done', 'done', 'done', 'now'],
        'stage_notes': ['7 of 11 stops', '₹10.9 crore a year', 'Two causes', 'A normal Tuesday', '4 stops left'],
        'findings': [
            {'label': 'Hours each patient waits to leave', 'value': '5 hours 15 minutes', 'src': 'yours', 'pt': 2},
            {'label': 'Yearly cost of the waiting', 'value': '₹10.9 crore', 'src': 'derived', 'state': 'outcome'},
            {'label': 'When doctors decide who goes home', 'value': '6 to 9 PM', 'src': 'yours', 'pt': 3},
            {'label': 'Bed empty after the patient leaves', 'value': '75 minutes', 'src': 'yours', 'state': 'target', 'pt': 1},
        ],
        'story': [('What you told us', 'Patients are ready by 10 in the morning but leave at about 3:15 in the afternoon.'),
                  ('What is really happening', 'Doctors decide in the evening, but nothing starts until they sign the next morning.'),
                  ('Why', 'The overnight hours go unused, and no one person owns the whole discharge.')],
        'pending': [
            {'text': 'Walk the last four stops: housekeeping, transport, the operating theatre and the family briefing.', 'who': 'tojo'},
            {'text': 'Find out why the bed stays empty for 75 minutes after the patient leaves.', 'who': 'tojo', 'pt': 1},
            {'text': 'Work out how many days the wait adds to each stay.', 'who': 'you', 'need': 'Needs your average stay in days', 'pt': 4},
        ],
        'actions': {'go': {'detail': 'Walk the housekeeping stop', 'say': 'Let’s walk the housekeeping stop'},
                    'add': {'detail': 'Tell Tojo something new', 'say': 'I want to add something about our discharges: '},
                    'jump': {'tab': 'Solutions', 'detail': 'Five solutions are waiting', 'say': 'Take me to Solutions'}},
        'chat': {'text': ['Here’s where the diagnosis stands. The cause is named, and your real times back it up.',
                          'Four stops on the chain are still to walk. Housekeeping comes first, because of the empty bed.'],
                 'pointer': 'Pick a point to add to it, or choose what to do next on the page.',
                 'note': 'The cause is found. Four stops are still to check.',
                 'points': [{'n': 1, 'label': 'Housekeeping and the empty bed'}, {'n': 2, 'label': 'Hours each patient waits'},
                            {'n': 3, 'label': 'When doctors decide'}, {'n': 4, 'label': 'The average stay figure'}],
                 'prompts': ['Let’s walk the housekeeping stop', 'Why does the bed stay empty so long?', 'Skip ahead to the solutions']},
    },
    'empty': {
        'stamp': {'at': 'Nothing to bring up to date yet', 'since': 'This page fills in as you talk to Tojo',
                  'fresh': 'Checked just now, 9:42 AM', 'fresh_since': 'No conversations yet'},
        'standing': 'Nothing checked yet',
        'deck': 'Tojo starts by walking your discharge, one stop at a time, before suggesting anything.',
        'stops': {k: ('next' if k == 'A' else 'later') for k, _ in STOPS},
        'stages': ['next', 'later', 'later', 'later', 'later'],
        'stage_notes': ['11 stops', 'Your own figures', 'Plain words', 'One normal day', 'Anything missed'],
        'findings': [
            {'label': 'Hours each patient waits to leave', 'value': '—', 'src': 'needed'},
            {'label': 'Yearly cost of the waiting', 'value': '—', 'src': 'needed'},
            {'label': 'When doctors decide who goes home', 'value': '—', 'src': 'needed'},
            {'label': 'Bed empty after the patient leaves', 'value': '—', 'src': 'needed'},
        ],
        'story': [('What you told us', 'Nothing yet.'), ('What is really happening', 'Found by walking the chain.'), ('Why', 'Named once the evidence is in.')],
        'pending': [
            {'text': 'Walk the 11 stops of your discharge, one question at a time.', 'who': 'tojo'},
            {'text': 'Put a price on the wait, using your own figures.', 'who': 'tojo'},
            {'text': 'Name what is really causing the delay.', 'who': 'tojo'},
        ],
        'actions': {'go': {'detail': 'Start with the doctors', 'say': 'Let’s start with the doctors'},
                    'add': {'detail': 'Tell Tojo what you already know', 'say': 'Here is what I already know about our discharges: '},
                    'jump': {'tab': 'Solutions', 'detail': 'Fills in once this starts', 'say': 'Take me to Solutions'}},
        'chat': {'text': ['This is your Diagnosis page. It fills in as we talk.',
                          'We start by walking your discharge, one stop at a time, before I suggest anything.'],
                 'note': 'Look closely before fixing anything.', 'points': [],
                 'prompts': ['Start with the doctors', 'How long will this take?', 'I already know the cause']},
    },
}

SRC = {'yours': 'Your number', 'derived': 'Worked out from yours', 'needed': 'Need from you'}

# --- shared pieces -------------------------------------------------------------------------
LENS = ('<svg class="dx-emblem" viewBox="0 0 48 48" aria-hidden="true"><circle cx="21" cy="21" r="14" fill="none" stroke="currentColor" stroke-width="3"/>'
        '<path d="M31.5 31.5L43 43" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>'
        '<path d="M12 21h5l2.5-5 4 10 2.5-5h3" fill="none" stroke="#d4a94f" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def masthead(m, sub='Discharge Process'):
    return ('<header class="dx-mast"><div class="dx-id">%s<div><div class="dx-eyebrow">%s</div><h2 class="dx-tab">Diagnosis</h2></div></div>%s</header>' % (LENS, e(sub), m.stamp()))

def standing(m):
    d = m.d
    return '<div class="dx-stand"><div class="dx-label">Where this stands</div><h3 class="dx-claim">%s</h3><p class="dx-deck">%s</p></div>' % (e(d['standing']), e(d['deck']))

def findings(m, cls='dx-finds'):
    out = []
    for f in m.d['findings']:
        out.append('<div class="dx-find dx-st-%s"%s><div class="dx-find-l">%s</div><div class="dx-find-v">%s</div><span class="dx-src dx-src-%s">%s</span></div>' % (
            f.get('state', 'plain'), m.pt(f.get('pt')), e(f['label']), e(f['value']), f['src'], SRC[f['src']]))
    return '<div class="%s">%s</div>' % (cls, ''.join(out))

def pending(m):
    items = []
    for p in m.d['pending']:
        need = '<span class="dx-need">%s</span>' % e(p['need']) if p.get('need') else ''
        items.append('<li class="dx-pend-i dx-who-%s"%s><span class="dx-tick" aria-hidden="true"></span><span>%s%s</span></li>' % (p['who'], m.pt(p.get('pt')), e(p['text']), need))
    return '<section class="dx-pend"><div class="dx-label">What Tojo still has to do</div><ul>%s</ul></section>' % ''.join(items)

def route(m):
    """Serpentine route on wide canvases (6 then 5 stops), a vertical line on narrow ones."""
    st = m.d['stops']
    def stop(k, n):
        s = st[k]
        lit = m.pt(1) if k == 'G' and m.state == 'filled' else ''
        return '<li class="dx-stop dx-s-%s"%s><span class="dx-dot">%s</span><span class="dx-sn">%s</span><span class="sr">%s</span></li>' % (s, lit, k, e(n), {'done': 'walked', 'now': 'walking now', 'next': 'first', 'later': 'still to walk'}[s])
    row1 = ''.join(stop(k, n) for k, n in STOPS[:6]); row2 = ''.join(stop(k, n) for k, n in reversed(STOPS[6:]))
    walked = sum(1 for v in st.values() if v == 'done')
    legend = ('<div class="dx-legend"><span><i class="dx-lg dx-s-done"></i>Walked</span><span><i class="dx-lg dx-s-now"></i>Now</span><span><i class="dx-lg dx-s-later"></i>Still to walk</span>'
              '<b>%d of 11 walked</b></div>' % walked)
    return ('<section class="dx-route"><div class="dx-route-head"><div class="dx-label">The road to going home</div>%s</div>'
            '<div class="dx-track"><ol class="dx-row dx-r1">%s</ol><ol class="dx-row dx-r2">%s</ol></div></section>') % (legend, row1, row2)

def stages(m, cls='dx-stages'):
    out = []
    for i, (name, s, note) in enumerate(zip(STAGES, m.d['stages'], m.d['stage_notes'])):
        out.append('<li class="dx-stage dx-s-%s"><span class="dx-sdot">%d</span><span class="dx-sname">%s</span><span class="dx-snote">%s</span></li>' % (s, i + 1, e(name), e(note)))
    return '<ol class="%s">%s</ol>' % (cls, ''.join(out))

# --- Sample A: the route walked -----------------------------------------------------------
def sample_a(m):
    inner = ('%s<div class="dx-a-body">%s%s%s<div class="dx-a-foot">%s%s</div></div>' % (
        masthead(m), standing(m), route(m), findings(m), pending(m), m.actions('dx-acts-col')))
    return canvas_wrap('lp-dx', 'lp-dx-a', inner, m.state)

# --- Sample B: the case sheet (a pulse line whose beats are the stages) ---------------------
def ecg(m):
    """One pulse line across the sheet. Each stage is a beat; beats still to come are flat and dashed."""
    xs = [60, 230, 400, 570, 740]; path_done, path_todo = [], []
    for i, x in enumerate(xs):
        seg = 'L%d 50 L%d 50 L%d 16 L%d 80 L%d 50 ' % (x - 30, x - 8, x, x + 8, x + 16)
        flat = 'L%d 50 L%d 50 ' % (x - 30, x + 16)
        s = m.d['stages'][i]
        (path_done if s == 'done' else path_todo).append((seg if s == 'done' else flat, i))
    last_done = max([i for _, i in path_done], default=-1)
    d1 = 'M0 50 ' + ''.join(s for s, _ in path_done) + ('L%d 50' % (xs[last_done] + 60) if last_done >= 0 else 'L0 50')
    start = xs[last_done] + 60 if last_done >= 0 else 0
    d2 = 'M%d 50 L800 50' % start
    dots = ''.join('<circle cx="%d" cy="%s" r="6" class="dx-beat dx-s-%s"/>' % (x, '16' if m.d['stages'][i] == 'done' else '50', m.d['stages'][i]) for i, x in enumerate(xs))
    labels = ''.join('<li class="dx-s-%s"><b>%s</b><span>%s</span></li>' % (s, e(n), e(t)) for n, s, t in zip(STAGES, m.d['stages'], m.d['stage_notes']))
    return ('<section class="dx-ecg"><svg viewBox="0 0 800 96" preserveAspectRatio="none" aria-hidden="true"><path d="%s" class="dx-ecg-on"/><path d="%s" class="dx-ecg-off"/>%s</svg>'
            '<ol class="dx-ecg-l">%s</ol></section>') % (d1, d2, dots, labels)

def story(m):
    rows = ''.join('<li><span class="dx-label">%s</span><p>%s</p></li>' % (e(a), e(b)) for a, b in m.d['story'])
    return '<section class="dx-story"><div class="dx-sheet-t">Findings</div><ol>%s</ol></section>' % rows

def vitals(m):
    rows = []
    for f in m.d['findings']:
        rows.append('<li class="dx-vit dx-st-%s"%s><span class="dx-vit-l">%s</span><span class="dx-vit-v">%s</span><span class="dx-src dx-src-%s">%s</span></li>' % (
            f.get('state', 'plain'), m.pt(f.get('pt')), e(f['label']), e(f['value']), f['src'], SRC[f['src']]))
    return '<section class="dx-vitals"><div class="dx-sheet-t">Readings</div><ul>%s</ul></section>' % ''.join(rows)

def sample_b(m):
    inner = ('%s<div class="dx-b-sheet"><div class="dx-b-top"><div class="dx-label">Where this stands</div><h3 class="dx-claim">%s</h3></div>%s'
             '<div class="dx-b-cols">%s%s</div></div><div class="dx-b-foot">%s%s</div>') % (
        masthead(m), e(m.d['standing']), ecg(m), story(m), vitals(m), pending(m), m.actions('dx-acts-row'))
    return canvas_wrap('lp-dx', 'lp-dx-b', inner, m.state)

# --- Sample C: the lens (the diagnosis under the glass, evidence pinned around it) ----------
def lens(m):
    import math
    segs = []; n = len(STAGES); gap = 6
    for i, s in enumerate(m.d['stages']):
        a0 = 45 + gap + i * 360 / n + gap / 2; a1 = 45 + gap + (i + 1) * 360 / n - gap / 2
        r = 150; cx = cy = 170
        p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
        p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
        segs.append('<path class="dx-arc dx-s-%s" d="M%.1f %.1f A%d %d 0 0 1 %.1f %.1f"/>' % (s, p0[0], p0[1], r, r, p1[0], p1[1]))
    done = sum(1 for s in m.d['stages'] if s == 'done')
    return ('<div class="dx-lens"><svg viewBox="0 0 340 340" aria-hidden="true"><circle cx="170" cy="170" r="128" class="dx-glass"/>%s'
            '<path d="M262 262 L318 318" class="dx-handle"/></svg><div class="dx-lens-in"><div class="dx-label">Under the glass</div><h3 class="dx-claim">%s</h3>'
            '<div class="dx-lens-n"><b>%d</b> of 5 stages done</div></div></div>') % (''.join(segs), e(m.d['standing']), done)

def sample_c(m):
    st = ''.join('<li class="dx-s-%s"><span class="dx-sdot">%d</span>%s</li>' % (s, i + 1, e(n)) for i, (n, s) in enumerate(zip(STAGES, m.d['stages'])))
    inner = ('%s<div class="dx-c-body"><div class="dx-c-left">%s<ol class="dx-c-stages">%s</ol></div>'
             '<div class="dx-c-right"><div class="dx-label">The evidence</div>%s%s</div></div>%s') % (
        masthead(m), lens(m), st, findings(m, 'dx-pins'), pending(m), m.actions('dx-acts-row'))
    return canvas_wrap('lp-dx', 'lp-dx-c', inner, m.state)

SAMPLES = [('a', 'Route walked', 'The 11-stop route as the progress drawing, findings below.', sample_a),
           ('b', 'Case sheet', 'A pulse line where each beat is a stage done, with findings and readings.', sample_b),
           ('c', 'Under the glass', 'The diagnosis inside a lens, the stages as its rim, evidence pinned beside it.', sample_c)]

CSS = r'''
.lp-dx{--ground:#DCE3DA;--card:#F7F9F5;--ink:#10241a;--muted:#44544A;--gold:#d4a94f;--gold-t:#6B4F16;--red:#8E2F1C;--amber:#B8862B;--green:#2f7350;--later:#879689;
  background:var(--ground);color:var(--ink);padding:18px 32px 22px;display:flex;flex-direction:column;gap:14px}
.lp-dx .dx-label{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.lp-dx .dx-mast{display:flex;align-items:center;justify-content:space-between;gap:18px;padding-bottom:14px;border-bottom:2px solid var(--ink)}
.lp-dx .dx-id{display:flex;align-items:center;gap:14px}
.lp-dx .dx-emblem{width:46px;height:46px;color:var(--ink);flex-shrink:0}
.lp-dx .dx-eyebrow{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.lp-dx .dx-tab{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:48px;line-height:.9;letter-spacing:.01em}
.lp-dx .lp-stamp{display:flex;align-items:center;gap:14px;text-align:right}
.lp-dx .lp-stamp-txt{display:flex;flex-direction:column;gap:2px}
.lp-dx .lp-stamp-at{font-size:13px;font-weight:600}
.lp-dx .lp-stamp-since{font-size:12px;color:var(--muted)}
.lp-dx .lp-refresh{background:transparent;border:1.5px solid var(--ink);border-radius:22px;font-size:13px;font-weight:500}
.lp-dx .lp-refresh:hover{background:var(--card)}
.lp-dx .dx-claim{margin:2px 0 0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:40px;line-height:.95;letter-spacing:.01em}
.lp-dx .dx-deck{margin-top:6px;font-size:15px;color:var(--muted);max-width:76ch}
/* findings */
.lp-dx .dx-finds{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.lp-dx .dx-find{background:var(--card);border:2px solid var(--ink);padding:10px 12px 12px;display:flex;flex-direction:column;gap:4px;align-items:flex-start}
.lp-dx .dx-find-l{font-size:12px;font-weight:600;line-height:1.3}
.lp-dx .dx-find-v{font-family:'Bebas Neue',sans-serif;font-size:30px;line-height:1}
.lp-dx .dx-st-outcome{border-color:var(--red)} .lp-dx .dx-st-outcome .dx-find-v,.lp-dx .dx-st-outcome .dx-vit-v{color:var(--red)}
.lp-dx .dx-st-target{border-color:var(--amber)}
.lp-dx .dx-src{font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;padding:2px 7px;border:1.5px solid var(--green);color:var(--green)}
.lp-dx .dx-src-derived{border-style:dashed;border-color:var(--gold-t);color:var(--gold-t)}
.lp-dx .dx-src-needed{border-style:dashed;border-color:var(--red);color:var(--red)}
/* pending */
.lp-dx .dx-pend ul{display:flex;flex-direction:column;gap:8px;margin-top:8px}
.lp-dx .dx-pend-i{display:flex;gap:10px;font-size:14px;line-height:1.45}
.lp-dx .dx-tick{flex-shrink:0;width:16px;height:16px;margin-top:3px;border:2px solid var(--ink);border-radius:50%}
.lp-dx .dx-who-you .dx-tick{border-style:dashed;border-color:var(--red)}
.lp-dx .dx-need{display:block;font-size:12px;font-weight:600;color:var(--red)}
/* actions */
.lp-dx .lp-acts{display:flex;gap:10px}
.lp-dx .dx-acts-col{flex-direction:column}
.lp-dx .lp-act{justify-content:center;padding:9px 16px;border:2px solid var(--ink);background:var(--card);border-radius:6px;font-size:14px}
.lp-dx .lp-act-d{font-size:12.5px;color:var(--muted)}
.lp-dx .lp-act-go{background:var(--gold);border-color:var(--gold);box-shadow:6px 6px 0 rgba(16,36,26,.18)}
.lp-dx .lp-act-go .lp-act-d{color:#3b2c0c}
.lp-dx .lp-act:hover{transform:translate(-1px,-1px)}
/* route map */
.lp-dx .dx-route{background:var(--card);border:2px solid var(--ink);box-shadow:8px 8px 0 rgba(16,36,26,.12);padding:12px 18px 14px}
.lp-dx .dx-route-head{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.lp-dx .dx-legend{display:flex;gap:14px;align-items:center;font-size:12px;color:var(--muted)} .lp-dx .dx-legend b{color:var(--ink);font-weight:600}
.lp-dx .dx-legend span{display:flex;align-items:center;gap:6px}
.lp-dx .dx-lg{width:12px;height:12px;border-radius:50%;border:2px solid var(--ink);display:inline-block}
.lp-dx .dx-track{position:relative;margin-top:10px;padding:0 6px}
.lp-dx .dx-row{position:relative;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));align-items:start}
.lp-dx .dx-row::before{content:'';position:absolute;left:8%;right:8%;top:17px;border-top:4px solid var(--ink)}
.lp-dx .dx-r2{margin-top:6px;grid-template-columns:repeat(6,minmax(0,1fr))} .lp-dx .dx-r2 .dx-stop:first-child{grid-column:2}
.lp-dx .dx-r2::before{left:calc(16.66% + 8%)}
.lp-dx .dx-track::after{content:'';position:absolute;left:calc(6px + (100% - 12px) * .9167);top:17px;width:48px;height:66px;border:4px solid var(--ink);border-left:none;border-radius:0 32px 32px 0}
.lp-dx .dx-stop{min-height:56px}
.lp-dx .dx-stop{position:relative;display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center}
.lp-dx .dx-dot{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:20px;border:3px solid var(--ink);background:var(--card);position:relative;z-index:1}
.lp-dx .dx-sn{font-size:12px;font-weight:600;line-height:1.2}
.lp-dx .dx-s-done .dx-dot,.lp-dx .dx-lg.dx-s-done{background:var(--ink);color:var(--card)}
.lp-dx .dx-s-now .dx-dot,.lp-dx .dx-lg.dx-s-now{background:var(--gold);border-color:var(--ink)}
.lp-dx .dx-s-now .dx-dot{box-shadow:0 0 0 5px rgba(212,169,79,.35)}
.lp-dx .dx-s-next .dx-dot{border-color:var(--ink);box-shadow:0 0 0 5px rgba(212,169,79,.35)}
.lp-dx .dx-s-later .dx-dot,.lp-dx .dx-lg.dx-s-later{border-color:var(--later);color:var(--muted)}
.lp-dx .dx-s-later .dx-sn{color:var(--muted);font-weight:500}
/* sample A */
.lp-dx-a .dx-a-body{display:flex;flex-direction:column;gap:16px}
.lp-dx-a .dx-a-foot{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:24px;align-items:start}
/* sample B */
.lp-dx-b .dx-b-sheet{background:var(--card);border:2px solid var(--ink);box-shadow:8px 8px 0 rgba(16,36,26,.12);padding:14px 20px 14px;display:flex;flex-direction:column;gap:10px;
  background-image:linear-gradient(rgba(16,36,26,.06) 1px,transparent 1px);background-size:100% 26px}
.lp-dx-b .dx-ecg svg{width:100%;height:60px;display:block;overflow:visible}
.lp-dx-b .dx-ecg-on{fill:none;stroke:var(--ink);stroke-width:3;stroke-linejoin:round}
.lp-dx-b .dx-ecg-off{fill:none;stroke:var(--later);stroke-width:2.5;stroke-dasharray:6 7}
.lp-dx-b .dx-beat{fill:var(--card);stroke:var(--ink);stroke-width:2.5} .lp-dx-b .dx-beat.dx-s-done{fill:var(--ink)}
.lp-dx-b .dx-beat.dx-s-now,.lp-dx-b .dx-beat.dx-s-next{fill:var(--gold)} .lp-dx-b .dx-beat.dx-s-later{stroke:var(--later)}
.lp-dx-b .dx-ecg-l{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));text-align:center;gap:6px}
.lp-dx-b .dx-ecg-l li{display:flex;flex-direction:column;font-size:12px;line-height:1.3} .lp-dx-b .dx-ecg-l b{font-weight:600}
.lp-dx-b .dx-ecg-l span{color:var(--muted)} .lp-dx-b .dx-ecg-l .dx-s-now b{color:var(--gold-t)}
.lp-dx-b .dx-b-cols{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:22px;border-top:1.5px solid rgba(16,36,26,.25);padding-top:12px}
.lp-dx-b .dx-sheet-t{font-family:'Bebas Neue',sans-serif;font-size:22px;line-height:1;margin-bottom:6px}
.lp-dx-b .dx-story ol{display:flex;flex-direction:column;gap:6px}
.lp-dx-b .dx-story li{display:flex;flex-direction:column;gap:1px;padding-left:12px;border-left:3px solid var(--ink);font-size:14px;line-height:1.45}
.lp-dx-b .dx-story li:last-child{border-left-color:var(--gold)}
.lp-dx-b .dx-vitals ul{display:flex;flex-direction:column}
.lp-dx-b .dx-vit{display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:10px;align-items:center;padding:5px 0;border-bottom:1px dashed rgba(16,36,26,.3)}
.lp-dx-b .dx-vit-l{font-size:12.5px;font-weight:500;line-height:1.3} .lp-dx-b .dx-vit-v{font-family:'Bebas Neue',sans-serif;font-size:24px;line-height:1;text-align:right}
.lp-dx-b .dx-vit .dx-src{grid-column:1;grid-row:2;justify-self:start;margin-top:2px;font-size:10px}
.lp-dx-b .dx-vit-v{grid-row:1/3;grid-column:2}
.lp-dx-b .dx-st-target .dx-vit-v{color:var(--gold-t)}
.lp-dx-b .dx-b-foot{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px;align-items:start}
.lp-dx-b .dx-acts-row{flex-direction:column}
/* sample C */
.lp-dx-c .dx-c-body{display:grid;grid-template-columns:340px minmax(0,1fr);gap:26px;align-items:start}
.lp-dx-c .dx-lens{position:relative;width:340px;height:340px}
.lp-dx-c .dx-lens svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.lp-dx-c .dx-glass{fill:var(--card);stroke:var(--ink);stroke-width:3} .lp-dx-c .dx-handle{stroke:var(--ink);stroke-width:14;stroke-linecap:round}
.lp-dx-c .dx-arc{fill:none;stroke-width:12;stroke:var(--later);stroke-linecap:butt;opacity:.55}
.lp-dx-c .dx-arc.dx-s-done{stroke:var(--ink);opacity:1} .lp-dx-c .dx-arc.dx-s-now,.lp-dx-c .dx-arc.dx-s-next{stroke:var(--gold);opacity:1}
.lp-dx-c .dx-lens-in{position:absolute;left:62px;right:62px;top:92px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px}
.lp-dx-c .dx-lens-in .dx-claim{font-size:36px}
.lp-dx-c .dx-lens-n{font-size:13px;color:var(--muted)} .lp-dx-c .dx-lens-n b{font-family:'Bebas Neue',sans-serif;font-size:22px;color:var(--ink);font-weight:400}
.lp-dx-c .dx-c-stages{display:flex;flex-wrap:wrap;gap:6px 12px;margin-top:10px;font-size:12px;font-weight:500}
.lp-dx-c .dx-c-stages li{display:flex;align-items:center;gap:6px}
.lp-dx-c .dx-sdot{width:22px;height:22px;border-radius:50%;border:2px solid var(--later);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:var(--muted)}
.lp-dx-c .dx-s-done .dx-sdot{background:var(--ink);border-color:var(--ink);color:var(--card)} .lp-dx-c .dx-s-now .dx-sdot,.lp-dx-c .dx-s-next .dx-sdot{background:var(--gold);border-color:var(--ink);color:var(--ink)}
.lp-dx-c .dx-c-right{display:flex;flex-direction:column;gap:12px}
.lp-dx-c .dx-pins{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.lp-dx-c .dx-pins .dx-find{position:relative;box-shadow:5px 5px 0 rgba(16,36,26,.12)}
.lp-dx-c .dx-pins .dx-find::before{content:'';position:absolute;top:-7px;left:14px;width:12px;height:12px;border-radius:50%;background:var(--gold);border:2px solid var(--ink)}
.lp-dx-c .dx-acts-row .lp-act{flex:1 1 0}
/* first visit */
.lp-dx[data-lp-state=empty] .dx-find{border-style:dashed;border-color:rgba(16,36,26,.45);background:transparent}
.lp-dx[data-lp-state=empty] .dx-find-v{color:var(--later)}
.lp-dx[data-lp-state=empty] .dx-claim{color:var(--muted)}
/* narrow */
@container lp (max-width:699px){
  .lp-dx{padding:16px 14px 22px;gap:16px}
  .lp-dx .dx-mast{flex-direction:column;align-items:stretch;gap:12px}
  .lp-dx .lp-stamp{justify-content:space-between;text-align:left}
  .lp-dx .dx-tab{font-size:42px}
  .lp-dx .dx-claim{font-size:34px}
  .lp-dx .dx-finds{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .lp-dx .dx-find-v{font-size:26px}
  .lp-dx .lp-acts{flex-direction:column}
  .lp-dx .dx-track{padding:0}
  .lp-dx .dx-track::after{display:none}
  .lp-dx .dx-row{display:flex;flex-direction:column;gap:0}
  .lp-dx .dx-row::before{left:17px;right:auto;top:18px;bottom:18px;border-top:none;border-left:4px solid var(--ink)}
  .lp-dx .dx-r2{flex-direction:column-reverse;margin-top:0} .lp-dx .dx-r2::before{left:17px;top:0}
  .lp-dx .dx-stop{flex-direction:row;gap:12px;padding:4px 0;text-align:left}
  .lp-dx .dx-sn{font-size:14px}
  .lp-dx .dx-route-head{flex-direction:column;align-items:flex-start}
  .lp-dx .dx-legend{flex-wrap:wrap;gap:8px 12px}
  .lp-dx-a .dx-a-foot,.lp-dx-b .dx-b-cols,.lp-dx-b .dx-b-foot{grid-template-columns:minmax(0,1fr)}
  .lp-dx-b .dx-ecg svg{height:60px}
  .lp-dx-b .dx-ecg-l{grid-template-columns:repeat(5,minmax(0,1fr));gap:2px} .lp-dx-b .dx-ecg-l li{font-size:11px} .lp-dx-b .dx-ecg-l span{display:none}
  .lp-dx-b .dx-b-sheet{padding:14px 14px 16px}
  .lp-dx-c .dx-c-body{grid-template-columns:minmax(0,1fr)}
  .lp-dx-c .dx-c-left{display:flex;flex-direction:column;align-items:center}
  .lp-dx-c .dx-lens{width:300px;height:300px}
  .lp-dx-c .dx-lens-in{left:52px;right:52px;top:78px} .lp-dx-c .dx-lens-in .dx-claim{font-size:31px}
  .lp-dx-c .dx-c-stages{justify-content:center}
  .lp-dx-c .dx-pins{grid-template-columns:repeat(2,minmax(0,1fr))}
}
'''
