#!/usr/bin/env python3
"""
build_block_library — ONE block library for every tool (Common Elements).

What it holds
  1. How to use the library: which block to use when, how a turn is built, where each tool's generator lives.
  2. Universal patterns and Discharge Process: everything the old Tojo block library held, drawn by the same
     code (landing-common/build_library.py): the Diagnosis blocks, sample turns, landing pages, landing elements,
     shared parts, and the Solutions, Automations and Processes turn templates.
  3. Bed Management: its look, its five approved landing pages, its approved turn templates (with the samples not
     chosen as variations), its own blocks, and the common tool layer (picking and entries).

Rule for this file (the lesson of 30 Sep 2026): BLOCKS ONLY. Every template is drawn inline as its canvas, at the
desktop canvas width (864px) and the phone canvas width (362px). No app interface (rail, header, chat panel),
no frames, no whole pages. The old library was built this way and stayed shareable; the version that added
twenty framed whole-interface pages (6.6 MB) stopped opening for anyone but its owner.

  python3 build_block_library.py                       # writes ../out/block-library.html and the artifact copy
Standard library only. Needs the Bed Management folder beside Common Elements.
"""
import importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
COMMON = os.path.dirname(HERE)
TOOLS = os.path.dirname(COMMON)
BM = os.path.join(TOOLS, 'Bed Management')
sys.path[:0] = [os.path.join(COMMON, 'landing-common'), os.path.join(COMMON, 'diagnosis-html-generator'), os.path.join(COMMON, 'tool-layer')]
import landing_common as lc          # noqa: E402
import build_library as old          # noqa: E402  the old library's own builder, unchanged
import diagnosis_html as dh          # noqa: E402
e = lc.e
OUT = os.path.join(COMMON, 'out')

# ------------------------------------------------------------------------------------------ CSS scoping
def _split_sel(sel):
    out, depth, cur = [], 0, ''
    for ch in sel:
        if ch in '([': depth += 1
        elif ch in ')]': depth -= 1
        if ch == ',' and depth == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur); return [s.strip() for s in out if s.strip()]

def scope_css(css, pre):
    """Prefix every rule with `pre ` so a tool's page CSS cannot touch any other part of the library."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        head = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        if head.startswith('@'):
            if re.match(r'@(media|container|supports)', head): out.append('%s{%s}' % (head, scope_css(body, pre)))
            else: out.append('%s{%s}' % (head, body))
        elif head:
            sels = []
            for s in _split_sel(head):
                if s in ('html', 'body', ':root'): sels.append(pre)
                else: sels.append('%s %s' % (pre, s))
            out.append('%s{%s}' % (','.join(sels), body))
        i = k
    return '\n'.join(out)

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod); return mod

# ------------------------------------------------------------------------------------------ one canvas, its own picking groups
GRP = re.compile(r'(data-grp(?:-in)?="|data-box="|data-fill="|data-count-for="|data-cur-for="|id="|url\(#|for=")([a-z]+\d+)')
def uniq(html_, token):
    """Each template keeps its picking groups to itself: the group ids every canvas starts again from (tj1, socc1 ...)
    get the template's own prefix, so picking in one template never opens a sheet in another."""
    return GRP.sub(lambda m: '%s%s-%s' % (m.group(1), token, m.group(2)), html_)

# ------------------------------------------------------------------------------------------ the old library: universal patterns and the landing pages
def old_library():
    """The universal Diagnosis patterns, the four approved Discharge landing pages, their elements and shared parts, drawn by the old
    library's own code. The Discharge turn templates it used to show (the twelve sample turns and the Solutions, Automations and
    Processes templates) are superseded (5 Oct 2026) by the regenerated Discharge Process section below."""
    reg = dh.load_registry()
    base = dh.gallery(reg)
    base = re.sub(r'<section class="g-row" id="dp-\d\d">.*?</section>', '', base, flags=re.S)       # the old sample turns, now in the Discharge section
    base = base.replace('<a href="#sample-turns" style="background:#10241a;color:#F3F1EA">Sample turns</a>', '', 1)
    rows, toc, css, n_el, n_sh = old.section(os.path.join(lc.HERE, 'landing-elements.json'))
    return base, rows, toc, css, '', n_el, n_sh, 0

# ------------------------------------------------------------------------------------------ Bed Management
BADGE_OK = ('#2f7350', 'approved')
BADGE_VAR = ('#2E5E8E', 'variation')
BADGE_DRAFT = ('#B8862B', 'draft')

def bed_management():
    sys.path[:0] = [BM, os.path.join(BM, 'diagnosis-html-generator')]
    v3 = load(os.path.join(BM, 'v3.py'), 'bm_v3')
    C = sys.modules['bm_common']
    g = load(os.path.join(BM, 'diagnosis-html-generator', 'bm_diagnosis_html.py'), 'bm_dg')
    greg = g.load_registry()
    rows, toc, css_parts = [], [], []
    rows.append('<h2 class="g-h2" id="bed-management">Bed Management</h2><p class="g-lead">The second tool. Same layout as every tool, its own colours and drawings. '
                'Each place has its own palette; the home page is a ward plan, and every place page draws from it. Turn templates use the universal patterns above, '
                'redrawn in Bed Management’s colours, with the common tool layer on top.</p>')
    toc.append('<a href="#bed-management" style="background:#1A2B45;color:#F3F1EA">Bed Management</a>')
    # look
    chips = []
    for k, (place, t, fn, css, data, cls, label, name) in v3.PAGES.items():
        chips.append('<div class="bml-chip"><i style="background:%s;border-color:%s"></i><b>%s</b><span>%s · ground %s · ink %s</span></div>' % (t['ground'], t['ink'], e(label), e(name), t['ground'], t['ink']))
    rows.append(old.row('bm-look', 'Bed Management · the look', 'palette', BADGE_OK,
                        dh.scope_badge('Bed Management', '') + '<p><b>One palette per place.</b> Gold #d4a94f is now, next and picked in every place; the chat panel stays forest. '
                        'Turn backgrounds change every four turns (Diagnosis: the morning count, then the lamp-lit sheet. Solutions: the fit-out, then plan paper).</p>',
                        '<div class="bml-chips">%s</div>' % ''.join(chips), '<div class="bml-chips">%s</div>' % ''.join(chips)))
    # landing pages
    rows.append('<h3 class="g-h3" id="bm-landing">Approved landing pages</h3>')
    toc.append('<a href="#bm-landing">bm landing pages</a>')
    for k, (place, t, fn, css, data, cls, label, name) in v3.PAGES.items():
        css_parts.append(C.BED_CSS + css)
        def canvas(state):
            return '<div class="bmx"><div class="lp-host"><div class="lp bm %s" style="%s">%s</div></div></div>' % (cls, t['vars'], fn(state))
        full = canvas('filled')
        meta = ('<p><b>%s landing page, %s.</b> Drawn by <code>Bed Management/v3.py</code> (%s). Five zones in the fixed order: masthead with Refresh now, '
                'where this stands, the drawing, what Tojo still has to do, the three buttons.</p><p class="g-small">The first element loads raised with its box open; on a phone each box opens under its element.</p>'
                '<details class="g-first"><summary>See its first-visit state</summary><div style="width:864px;margin-top:8px">%s</div></details>') % (
            e(label), e(name), 'home.py' if k == 'home' else k + '/' + k + '.py', canvas('empty'))
        rows.append(old.row('bm-landing-%s' % k, 'Bed Management · %s' % label, name, BADGE_OK, dh.scope_badge('Bed Management', '') + meta, full, full))
        toc.append('<a href="#bm-landing-%s">bm-%s</a>' % (k, k))
    # turn templates
    rows.append('<h3 class="g-h3" id="bm-turns">Diagnosis turn templates</h3><p class="g-lead">Each is drawn by <code>Bed Management/diagnosis-html-generator/bm_diagnosis_html.py</code> '
                'from its spec. The drawing is a universal pattern from this library; the sheets and Add yours fields are the common tool layer. '
                'Try it: pick a moment, press Add yours, type, then add a second entry. Both are written into the message (here, a hidden message box).</p>')
    toc.append('<a href="#bm-turns">bm turns</a>')
    ex = os.path.join(BM, 'examples', 'diagnosis')
    for fn_ in sorted(f for f in os.listdir(ex) if f.startswith('bm-dg-') and f.endswith('.json')):
        spec = json.load(open(os.path.join(ex, fn_), encoding='utf-8'))
        errs, _ = g.validate(spec, greg)
        if errs: raise SystemExit('%s is invalid: %s' % (fn_, errs[:3]))
        rv = spec.get('review', {}); sm = spec['turn'].get('sample', {})
        cv = '<div class="bmx">%s</div>' % uniq(g.render_canvas(spec, greg), 'bmdg%s' % fn_[6:-5].replace('-', ''))
        types = [b['type'] for b in spec['canvas']['blocks'][1:]]
        meta = ('<p><b>%s · %s.</b> %s</p><p class="g-small"><b>Turn:</b> %s · <b>Blocks:</b> %s · <b>Review:</b> %s</p>') % (
            e(spec['turn']['id']), e(sm.get('name') or spec['canvas']['blocks'][0]['title']), e(sm.get('what') or spec['turn'].get('note_for_review', '')), e(spec['turn'].get('transcript', {}).get('label', '')), e(', '.join(types)), e(rv.get('note', 'Draft: awaiting review')))
        badge = BADGE_OK if rv.get('status') == 'approved' else (BADGE_VAR if rv.get('status') == 'not chosen' else BADGE_DRAFT)
        rid = spec['turn']['id'] + ('-' + sm['letter'].lower() if sm.get('letter') else '')
        name = ('Sample %s' % sm['letter']) if sm.get('letter') else spec['canvas']['blocks'][0]['title']
        rows.append(old.row(rid, '%s · %s' % (spec['turn']['id'], name), 'turn', badge, dh.scope_badge('Bed Management', '') + meta, cv, cv))
        toc.append('<a href="#%s">%s</a>' % (rid, rid))
    # own blocks and the tool layer
    rows.append('<h3 class="g-h3" id="bm-own">Bed Management drawings and the tool layer</h3><p class="g-lead">The drawings Bed Management Diagnosis uses, one per turn, so no two turns look alike. '
                'Each is drawn by <code>Bed Management/diagnosis-html-generator/bm_blocks.py</code>. On a phone every pickable item is stacked, one above the other, and its sheet opens under it.</p>')
    first_use = {}
    for fn_ in sorted(f for f in os.listdir(ex) if f.startswith('bm-dg-') and f.endswith('.json')):
        sp = json.load(open(os.path.join(ex, fn_), encoding='utf-8'))
        for bl in sp['canvas']['blocks']:
            first_use.setdefault(bl['type'], sp['turn']['id'])
    for b in greg['blocks']:
        col = '#2f7350' if b['status'] == 'approved' else '#B8862B'
        rows.append('<section class="g-row" id="bm-block-%s"><div class="g-meta"><div class="g-id">%s <span>Bed Management drawing</span></div><span class="g-status" style="background:%s">%s</span>%s'
                    '<p><b>%s.</b> %s</p><p class="g-small"><b>Use when:</b> %s<br><b>Avoid when:</b> %s%s<br><b>Drawn in:</b> %s, shown above</p></div></section>' % (
                        e(b['id']), e(b['id']), col, e(b['status']), dh.scope_badge(b['scope'] if b['scope'] != 'universal' else 'all', 'Bed Management'),
                        e(b.get('category', '').capitalize()), e(b['purpose']), e('; '.join(b['use_when'])), e('; '.join(b['avoid_when'])),
                        ('<br><b>Interaction:</b> ' + e(b['interaction'])) if b.get('interaction') else '', e(first_use.get(b['id'], 'not used yet'))))
    lay = greg['layers']
    rows.append('<section class="g-row"><div class="g-meta"><div class="g-id">tool layer <span>picking and entries</span></div><span class="g-status" style="background:#2f7350">approved</span>%s'
                '<p><b>Common.</b> Any generator can add it to %s. Each item of the drawing gets a sheet; the first is raised with its sheet open; on a phone the sheet opens under its item. '
                'A sheet may carry an Add yours field: the entry is written into the chat message with where it came from, and every entry is added, never replaced. '
                'Code: <code>Common Elements/tool-layer/tojo_layer.py</code>.</p><p class="g-small">Slots it adds: sheets (one per item, in order: key, when, title, text, and each tool’s own lines), ask_more (one closing entry).</p></div></section>' % (
                    dh.scope_badge('all', 'Bed Management'), e(', '.join(lay['applies_to']))))
    toc.append('<a href="#bm-own">bm blocks</a>')
    css = scope_css('\n'.join(dict.fromkeys(css_parts)) + C.BASE_CSS + C.SEL_CSS, '.bmx') + g.theme_css(greg) + scope_css(g.LAYER_CSS + g.bm_blocks.CSS + g.ACTIONS_CSS, '.bmx')
    js = C.SEL_JS + g.RUNTIME + g.bm_blocks.BC_JS
    return ''.join(rows), ''.join(toc), css, js

# ------------------------------------------------------------------------------------------ Bed Management · Solutions
def bm_solutions():
    sys.path.insert(0, os.path.join(BM, 'solutions-html-generator'))
    sg = load(os.path.join(BM, 'solutions-html-generator', 'bm_solutions_html.py'), 'bm_so')
    sreg = sg.load_registry()
    rows, toc = [], []
    rows.append('<h3 class="g-h3" id="bm-so-turns">Solutions turn templates</h3><p class="g-lead">Each is drawn by <code>Bed Management/solutions-html-generator/bm_solutions_html.py</code> '
                'from its spec, using the Solutions motifs of this library (the lightbulb, the jigsaw, the maze, the knots, the route, the drafting sheet and the door plates) '
                'in Bed Management’s Solutions colours, with the common tool layer. Every turn ends with the three buttons: Proceed with next step, Add more, Jump to Automations.</p>')
    toc.append('<a href="#bm-so-turns">bm solutions turns</a>')
    ex = os.path.join(BM, 'examples', 'solutions')
    files = ['bm-so-01-A.json', 'bm-so-01-B.json', 'bm-so-01-C.json'] + sorted(f for f in os.listdir(ex) if re.match(r'bm-so-\d\d\.json$', f))
    first_use = {}
    for fn_ in files:
        spec = json.load(open(os.path.join(ex, fn_), encoding='utf-8'))
        errs, _ = sg.validate(spec, sreg)
        if errs: raise SystemExit('%s is invalid: %s' % (fn_, errs[:3]))
        rv = spec.get('review', {}); sm = spec['turn'].get('sample', {})
        for bl in spec['canvas']['blocks']: first_use.setdefault(bl['type'], spec['turn']['id'])
        cv = '<div class="bmx">%s</div>' % uniq(sg.render_canvas(spec, sreg), 'bmso%s' % fn_[6:-5].replace('-', ''))
        types = [b['type'] for b in spec['canvas']['blocks'][1:]]
        meta = ('<p><b>%s · %s.</b> %s</p><p class="g-small"><b>Turn:</b> %s · <b>Blocks:</b> %s · <b>Theme:</b> %s · <b>Review:</b> %s</p>') % (
            e(spec['turn']['id']), e(sm.get('name') or spec['canvas']['blocks'][0]['title']), e(sm.get('what') or spec['turn'].get('context', '')),
            e(spec['turn'].get('transcript', {}).get('label', '')), e(', '.join(types)), e(sreg['tones']['list'][sg.tone_of(spec, sreg)]['name']), e(rv.get('note', 'Draft: awaiting review')))
        badge = BADGE_OK if rv.get('status') == 'approved' else BADGE_DRAFT
        rid = spec['turn']['id'] + ('-' + sm['letter'].lower() if sm.get('letter') else '')
        name = ('Sample %s · %s' % (sm['letter'], sm['name'])) if sm.get('letter') else spec['canvas']['blocks'][0]['title']
        rows.append(old.row(rid, '%s · %s' % (spec['turn']['id'], name), 'turn', badge, dh.scope_badge('Bed Management', '') + meta, cv, cv))
        toc.append('<a href="#%s">%s</a>' % (rid, rid))
    rows.append('<h3 class="g-h3" id="bm-so-own">Bed Management Solutions drawings</h3><p class="g-lead">One main drawing per turn, so no two turns look alike. '
                'Drawn by <code>bm_so_blocks.py</code> and <code>bm_so_blocks2.py</code> beside the generator. Each says which library motif it is built from.</p>')
    for b in sreg['blocks']:
        col = '#2f7350' if b['status'] == 'approved' else '#B8862B'
        rows.append('<section class="g-row" id="bm-so-block-%s"><div class="g-meta"><div class="g-id">%s <span>Bed Management Solutions drawing</span></div><span class="g-status" style="background:%s">%s</span>%s'
                    '<p><b>Built from:</b> %s. %s</p><p class="g-small"><b>Use when:</b> %s<br><b>Avoid when:</b> %s%s<br><b>Drawn in:</b> %s, shown above</p></div></section>' % (
                        e(b['id']), e(b['id']), col, e(b['status']), dh.scope_badge(b['scope'] if b['scope'] != 'Bed Management Solutions' else 'Bed Management', 'Bed Management'),
                        e(b.get('from', '')), e(b['purpose']), e('; '.join(b['use_when'])), e('; '.join(b['avoid_when'])),
                        ('<br><b>Interaction:</b> ' + e(b['interaction'])) if b.get('interaction') else '', e(first_use.get(b['id'], 'not used yet'))))
    rows.append('<section class="g-row" id="bm-so-actions"><div class="g-meta"><div class="g-id">the three buttons <span>every turn</span></div><span class="g-status" style="background:#2f7350">approved</span>%s'
                '<p><b>On every turn, not only landing pages</b> (rules/08 §8): Proceed with next step (naming the step), Add more, Jump to the next place. '
                'Same order and look as the landing page. The generator refuses a spec without <code>canvas.actions</code>.</p></div></section>' % dh.scope_badge('all', 'Bed Management'))
    toc.append('<a href="#bm-so-own">bm solutions blocks</a>')
    css = scope_css(sg.L.CSS + sg.bm_so_blocks.CSS + sg.bm_so_blocks2.CSS, '.bmx') + '.bmx .sx .tl-entry .tj-label{text-transform:none;letter-spacing:0;font-weight:400}'
    js = sg.bm_so_blocks.JS + sg.bm_so_blocks2.JS
    return ''.join(rows), ''.join(toc), css, js

# ------------------------------------------------------------------------------------------ Bed Management · Automations
def bm_automations():
    sys.path.insert(0, os.path.join(BM, 'automations-html-generator'))
    ag = load(os.path.join(BM, 'automations-html-generator', 'bm_automations_html.py'), 'bm_au')
    areg = ag.load_registry()
    rows, toc = [], []
    rows.append('<h3 class="g-h3" id="bm-au-turns">Automations turn templates</h3><p class="g-lead">Each is drawn by <code>Bed Management/automations-html-generator/bm_automations_html.py</code> '
                'from its spec, with the Automations motifs of this library (the switchboard, the engine on a screen, the station panel, the desk helper, the relay, the thinker, the night shift) '
                'in Bed Management’s Automations colours (the station panel), with the common tool layer. Every turn ends with the three buttons: Proceed with next step, Add more, Jump to Processes.</p>')
    toc.append('<a href="#bm-au-turns">bm automations turns</a>')
    ex = os.path.join(BM, 'examples', 'automations')
    files = ['bm-au-01-A.json', 'bm-au-01-B.json', 'bm-au-01-C.json'] + sorted(f for f in os.listdir(ex) if re.match(r'bm-au-\d\d\.json$', f))
    first_use = {}
    for fn_ in files:
        spec = json.load(open(os.path.join(ex, fn_), encoding='utf-8'))
        errs, _ = ag.validate(spec, areg)
        if errs: raise SystemExit('%s is invalid: %s' % (fn_, errs[:3]))
        rv = spec.get('review', {}); sm = spec['turn'].get('sample', {})
        for bl in spec['canvas']['blocks']: first_use.setdefault(bl['type'], spec['turn']['id'])
        cv = '<div class="bmx">%s</div>' % uniq(ag.render_canvas(spec, areg), 'bmau%s' % fn_[6:-5].replace('-', ''))
        types = [b['type'] for b in spec['canvas']['blocks'][1:]]
        meta = ('<p><b>%s · %s.</b> %s</p><p class="g-small"><b>Turn:</b> %s · <b>Blocks:</b> %s · <b>Theme:</b> %s · <b>Review:</b> %s</p>') % (
            e(spec['turn']['id']), e(sm.get('name') or spec['canvas']['blocks'][0]['title']), e(sm.get('what') or spec['turn'].get('context', '')),
            e(spec['turn'].get('transcript', {}).get('label', '')), e(', '.join(types)), e(areg['tones']['list'][ag.tone_of(spec, areg)]['name']), e(rv.get('note', 'Draft: awaiting review')))
        badge = BADGE_OK if rv.get('status') == 'approved' else BADGE_DRAFT
        rid = spec['turn']['id'] + ('-' + sm['letter'].lower() if sm.get('letter') else '')
        name = ('Sample %s · %s' % (sm['letter'], sm['name'])) if sm.get('letter') else spec['canvas']['blocks'][0]['title']
        rows.append(old.row(rid, '%s · %s' % (spec['turn']['id'], name), 'turn', badge, dh.scope_badge('Bed Management', '') + meta, cv, cv))
        toc.append('<a href="#%s">%s</a>' % (rid, rid))
    rows.append('<h3 class="g-h3" id="bm-au-own">Bed Management Automations drawings</h3><p class="g-lead">One main drawing per turn. Drawn by <code>bm_au_blocks.py</code> and <code>bm_au_blocks2.py</code> '
                'beside the generator, each from a library Automations motif.</p>')
    for b in areg['blocks']:
        col = '#2f7350' if b['status'] == 'approved' else '#B8862B'
        rows.append('<section class="g-row" id="bm-au-block-%s"><div class="g-meta"><div class="g-id">%s <span>Bed Management Automations drawing</span></div><span class="g-status" style="background:%s">%s</span>%s'
                    '<p><b>Built from:</b> %s. %s</p><p class="g-small"><b>Use when:</b> %s<br><b>Avoid when:</b> %s%s<br><b>Drawn in:</b> %s, shown above</p></div></section>' % (
                        e(b['id']), e(b['id']), col, e(b['status']), dh.scope_badge(b['scope'] if b['scope'] not in ('Bed Management Automations',) else 'Bed Management', 'Bed Management'),
                        e(b.get('from', '')), e(b['purpose']), e('; '.join(b['use_when'])), e('; '.join(b['avoid_when'])),
                        ('<br><b>Interaction:</b> ' + e(b['interaction'])) if b.get('interaction') else '', e(first_use.get(b['id'], 'not used yet'))))
    toc.append('<a href="#bm-au-own">bm automations blocks</a>')
    css = scope_css(ag.bm_au_blocks.CSS + ag.bm_au_blocks2.CSS, '.bmx')
    js = ag.bm_au_blocks.JS + ag.bm_au_blocks2.JS
    return ''.join(rows), ''.join(toc), css, js

def bm_processes():
    """Bed Management Processes turn templates (approved 6 Oct 2026), drawn as canvases only."""
    gdir = os.path.join(BM, 'processes-html-generator')
    sys.path.insert(0, gdir)
    pg = load(os.path.join(gdir, 'bm_processes_html.py'), 'bm_pr_lib')
    reg = pg.load_registry(); base = pg.base
    rows, toc = [], []
    ex = os.path.join(BM, 'examples', 'processes')
    man = json.load(open(os.path.join(ex, 'turns.json'), encoding='utf-8'))
    rows.append('<h3 class="g-h3" id="bm-pr-turns">Processes turn templates</h3><p class="g-lead">%d turns in conversation order, drawn by <code>Bed Management/processes-html-generator/bm_processes_html.py</code> '
                'from their specs: the Processes motifs of this library (the ward board, the magnets, the name badges, the chairs and lamps, the instrument windows, the loop, the trial strip) and five '
                'Bed Management drawings (the day on a wall clock, the trial ward with pins, the doctor’s round cards, the OPD slip, the clipboard), in the trial ward look: pale clay, deep brown, rust. '
                'Every turn ends with the three buttons: Proceed with next step, Add more, Jump to Diagnosis.</p>' % len(man['turns']))
    toc.append('<a href="#bm-pr-turns">bm processes turns</a>')
    first_use = {}
    for t in man['turns']:
        spec = json.load(open(os.path.join(ex, t['file']), encoding='utf-8'))
        errs, _ = pg.validate(spec, reg)
        if errs: raise SystemExit('%s is invalid: %s' % (t['file'], errs[:3]))
        for bl in spec['canvas']['blocks']: first_use.setdefault(bl['type'], spec['turn']['id'])
        tid = spec['turn']['id']; rv = spec.get('review', {})
        cv = '<div class="bmx">%s</div>' % uniq(pg.render_canvas(spec, reg), tid.replace('-', ''))
        types = [b['type'] for b in spec['canvas']['blocks'][1:]]
        meta = ('<p><b>%s · %s.</b> %s</p><p class="g-small"><b>User’s message:</b> %s<br><b>Blocks:</b> %s · <b>Theme:</b> %s · <b>Review:</b> %s</p>') % (
            e(tid), e(spec['canvas']['blocks'][0]['title']), e(t.get('note', '')), e(spec['turn']['user_message']), e(', '.join(types)),
            e(reg['tones']['list'][pg.tone_of(spec, reg)]['name']), e(rv.get('note', 'Draft: awaiting review')))
        badge = BADGE_OK if rv.get('status') == 'approved' else BADGE_DRAFT
        rows.append(old.row(tid, '%s · %s' % (tid, spec['canvas']['blocks'][0]['title']), 'turn', badge, dh.scope_badge('Bed Management', '') + meta, cv, cv))
        toc.append('<a href="#%s">%s</a>' % (tid, tid))
    own = [b for b in reg['blocks'] if b.get('scope') == 'Bed Management Processes']
    rows.append('<h3 class="g-h3" id="bm-pr-own">Bed Management Processes drawings</h3><p class="g-lead">The five new drawings live in <code>bm_pr_blocks.py</code>; the library Processes motifs are '
                'loaded from <code>Discharge Process/processes-html-generator/dp_pr_blocks.py</code> as a private copy and drawn in the trial ward colours.</p>')
    for b in own:
        col = '#2f7350' if b.get('status') == 'approved' else '#B8862B'
        rows.append('<section class="g-row" id="bm-pr-block-%s"><div class="g-meta"><div class="g-id">%s <span>Bed Management Processes drawing</span></div><span class="g-status" style="background:%s">%s</span>%s'
                    '<p><b>Built from:</b> %s. %s</p><p class="g-small"><b>Use when:</b> %s<br><b>Avoid when:</b> %s%s<br><b>Drawn in:</b> %s, shown above</p></div></section>' % (
                        e(b['id']), e(b['id']), col, e(b.get('status', 'draft')), dh.scope_badge('Bed Management', 'Bed Management'), e(b.get('from', '')), e(b['purpose']),
                        e('; '.join(b.get('use_when', []))), e('; '.join(b.get('avoid_when', []))), ('<br><b>Interaction:</b> ' + e(b['interaction'])) if b.get('interaction') else '',
                        e(first_use.get(b['id'], 'not used yet'))))
    toc.append('<a href="#bm-pr-own">bm processes blocks</a>')
    css = scope_css(base.L.CSS + base.bm_so_blocks.CSS + base.bm_so_blocks2.CSS + base.PAGE_CSS, '.bmx')
    # the Processes motifs' own script (dp_pr_blocks.JS) is already on the page with the Discharge templates and works on every template; only the new drawings add theirs
    return ''.join(rows), ''.join(toc), css, pg.bm_pr_blocks.JS

# ------------------------------------------------------------------------------------------ Discharge Process, regenerated (5 Oct 2026)
DP = os.path.join(TOOLS, 'Discharge Process')
DP_PLACES = [('diagnosis', 'Diagnosis', 'the case sheet: sage ground, forest ink', 'Solutions'),
             ('solutions', 'Solutions', 'the blueprint: pale blue-grey ground, navy ink, a grid', 'Automations'),
             ('automations', 'Automations', 'the switch room: steel ground, charcoal ink, teal for what runs by itself', 'Processes'),
             ('processes', 'Processes', 'the ward board: heather ground, aubergine ink, plum', 'Diagnosis')]

def discharge_process():
    """Every Discharge Process turn template, regenerated with the latest generators (Discharge Process/<place>-html-generator/dp_<place>_html.py),
    drawn as its canvas only. Replaces the twelve old sample turns and the old Solutions, Automations and Processes templates."""
    sys.path[:0] = [DP]
    rows, toc, css, js = [], [], [], []
    rows.append('<h2 class="g-h2" id="discharge-process">Discharge Process</h2><p class="g-lead">The first tool, regenerated on 5 Oct 2026 with the latest generators: the ones built for Bed Management, '
                'loaded as copies and pointed at Discharge. Every turn has its own drawing, plain simple English, the common tool layer (the first item raised with its sheet open; on a phone every '
                'item stacked with its sheet under it; entries typed in the drawing and added to the message), the three buttons, and a background that changes every four turns. '
                'Same practice hospital as before: 250 beds, Bhubaneswar. Each place keeps the colours of its approved landing page.</p>')
    toc.append('<a href="#discharge-process" style="background:#10241a;color:#F3F1EA">Discharge Process</a>')
    for key, place, look, nxt in DP_PLACES:
        gdir = os.path.join(DP, '%s-html-generator' % key)
        sys.path.insert(0, gdir)
        mod = load(os.path.join(gdir, 'dp_%s_html.py' % key), 'dp_lib_%s' % key)
        reg = mod.load_registry(); base = mod.base
        ex = os.path.join(DP, 'examples', key)
        man = json.load(open(os.path.join(ex, 'turns.json'), encoding='utf-8'))
        rows.append('<h3 class="g-h3" id="dp-%s">%s turn templates</h3><p class="g-lead">%d turns in conversation order, drawn by <code>Discharge Process/%s-html-generator/dp_%s_html.py</code> '
                    'in the Discharge %s look: %s. Every turn ends with Proceed with next step, Add more, Jump to %s. Each note says which old template it replaces.</p>' % (
                        key, place, len(man['turns']), key, key, place, look, nxt))
        toc.append('<a href="#dp-%s">dp %s</a>' % (key, key))
        first_use = {}
        for t in man['turns']:
            spec = json.load(open(os.path.join(ex, t['file']), encoding='utf-8'))
            errs, _ = mod.validate(spec, reg)
            if errs: raise SystemExit('%s is invalid: %s' % (t['file'], errs[:3]))
            for bl in spec['canvas']['blocks']: first_use.setdefault(bl['type'], spec['turn']['id'])
            tid = spec['turn']['id']
            cv = '<div class="dpx">%s</div>' % uniq(mod.render_canvas(spec, reg), tid.replace('-', ''))
            types = [b['type'] for b in spec['canvas']['blocks'][1:]]
            rv = spec.get('review', {})
            meta = ('<p><b>%s · %s.</b> %s</p><p class="g-small"><b>User’s message:</b> %s<br><b>Blocks:</b> %s · <b>Theme:</b> %s · <b>Replaces:</b> %s · <b>Review:</b> %s</p>') % (
                e(tid), e(spec['canvas']['blocks'][0]['title']), e(t.get('note', '')), e(spec['turn']['user_message']), e(', '.join(types)),
                e(reg['tones']['list'][mod.tone_of(spec, reg)]['name']), e(spec['turn'].get('was', '')), e(rv.get('note', 'Draft: awaiting review')))
            badge = BADGE_OK if rv.get('status') == 'approved' else BADGE_DRAFT
            rows.append(old.row(tid, '%s · %s' % (tid, spec['canvas']['blocks'][0]['title']), 'turn', badge, dh.scope_badge('Discharge Process', '') + meta, cv, cv))
            toc.append('<a href="#%s">%s</a>' % (tid, tid))
        own = [b for b in reg['blocks'] if b.get('scope') == 'Discharge Process' or key == 'processes' and b['id'] in ('heading', 'swap', 'trial', 'badges', 'seats', 'readouts', 'loop', 'timesheet', 'night-lanes')]
        if own:
            rows.append('<h3 class="g-h3" id="dp-%s-own">Discharge %s drawings</h3><p class="g-lead">Drawn for Discharge where the latest generators had no drawing that fits; the rest of the place uses the layered library drawings shown in the turns above.</p>' % (key, place))
            for b in own:
                rows.append('<section class="g-row" id="dp-%s-block-%s"><div class="g-meta"><div class="g-id">%s <span>Discharge %s drawing</span></div><span class="g-status" style="background:%s">%s</span>%s'
                            '<p><b>Built from:</b> %s. %s</p><p class="g-small"><b>Use when:</b> %s<br><b>Avoid when:</b> %s%s<br><b>Drawn in:</b> %s, shown above</p></div></section>' % (
                                key, e(b['id']), e(b['id']), place, '#2f7350' if b.get('status') == 'approved' else '#B8862B', e(b.get('status', 'draft')), dh.scope_badge('Discharge Process', 'Discharge Process'), e(b.get('from', 'Discharge’s own')), e(b['purpose']),
                                e('; '.join(b.get('use_when', []))), e('; '.join(b.get('avoid_when', []))), ('<br><b>Interaction:</b> ' + e(b['interaction'])) if b.get('interaction') else '',
                                e(first_use.get(b['id'], 'not used yet'))))
            toc.append('<a href="#dp-%s-own">dp %s blocks</a>' % (key, key))
        # the CSS each place needs, scoped under .dpx (the library's own place CSS, solutions.css and automations.css, is loaded once for the page)
        if key == 'diagnosis':
            css.append(mod.theme_css(reg) + scope_css(base.LAYER_CSS + base.bm_blocks.CSS + base.ACTIONS_CSS, '.dpx'))
        elif key == 'automations':
            css.append(scope_css(base.L.CSS + base.bm_au_blocks.CSS + base.bm_au_blocks2.CSS + base.PAGE_CSS, '.dpx'))
            js.append(mod.dp_au_blocks.JS)
        else:
            css.append(scope_css(base.L.CSS + base.bm_so_blocks.CSS + base.bm_so_blocks2.CSS + base.PAGE_CSS, '.dpx'))
            if key == 'processes': js.append(mod.dp_pr_blocks.JS)
    return ''.join(rows), ''.join(toc), '\n'.join(dict.fromkeys(css)) + '.dpx .sx .tl-entry .tj-label,.dpx .ax .tl-entry .tj-label{text-transform:none;letter-spacing:0;font-weight:400}', '\n'.join(js)

# ------------------------------------------------------------------------------------------ the guide
def guide(n_el, n_sh, n_t):
    ph = [('Universal patterns', 'Common Elements/blocks/registry.json', 'Common Elements/diagnosis-html-generator/diagnosis_html.py (and the library motifs in solutions_html.py, automations_html.py, processes_html.py)')] + \
         [('Discharge Process · %s' % p, 'Discharge Process/%s-html-generator/registry.json' % k, 'Discharge Process/%s-html-generator/dp_%s_html.py' % (k, k)) for k, p, _, _ in DP_PLACES] + \
         [('Bed Management · %s' % p, 'Bed Management/%s-html-generator/registry.json' % k, 'Bed Management/%s-html-generator/bm_%s_html.py' % (k, k)) for k, p in (('diagnosis', 'Diagnosis'), ('solutions', 'Solutions'), ('automations', 'Automations'), ('processes', 'Processes'))]
    places = ''.join('<tr><td>%s</td><td><code>%s</code></td><td><code>%s</code></td></tr>' % (a, b, c) for a, b, c in ph)
    return ('<section class="lib-guide" id="how-to-use"><h2 class="g-h2" style="margin-left:0">How to use this library</h2>'
            '<div class="lib-cols"><div><h3>One library, every tool</h3><p>Every tool draws its turns and landing pages from here. Each template carries a badge:</p>'
            '<ul><li><b>Universal pattern</b>: any tool and any place may use it, redrawn in that tool’s own colours by its own generator.</li>'
            '<li><b>[Place] only</b> or <b>[Tool] only</b>: only that place or tool uses it.</li><li><b>Approved</b>, <b>variation</b> (a sample not chosen, ready as a pattern) or <b>draft</b>.</li></ul></div>'
            '<div><h3>Which block, when</h3><ol><li>Decide the turn type (question, asking for figures, figures back, findings, diagnosis, overview, part, going deeper, challenge, recommendation).</li>'
            '<li>Pick the fewest blocks that carry what the chat cannot: approved first, then variations. Each block below says <i>use when</i> and <i>avoid when</i>.</li>'
            '<li>Never reuse a place’s main block in the next turn: every turn looks different. A fill-in-the-blank and its answered redraw are the one exception.</li>'
            '<li>Mark each figure as yours, worked out from yours, a guess, an example, a goal, or needed.</li></ol></div>'
            '<div><h3>How a turn is built</h3><p>Claude writes one JSON spec: the user’s message, the chat parts (text, note, @points, one question, three prompts) and the blocks with their words. '
            'The tool’s generator checks it and draws it. Nobody writes HTML by hand. Rules: <code>rules/06</code> (response), <code>rules/07</code> (block design), <code>rules/08</code> (shared turn rules).</p></div></div>'
            '<table class="lib-t"><tr><th>Place</th><th>Blocks listed in</th><th>Drawn by</th></tr>%s</table>'
            '<p class="g-small">In this build: the universal Diagnosis patterns, %d landing elements, %d shared parts, the 32 regenerated Discharge Process turn templates, and the Bed Management '
            'Diagnosis, Solutions, Automations and Processes templates. Everything is drawn as its canvas only, never inside the app interface. The Discharge turns of the old library '
            '(the twelve sample turns and the first Solutions, Automations and Processes templates) are replaced by the regenerated ones.</p></section>') % (places, n_el, n_sh)

GUIDE_CSS = '''
.lib-guide{margin:8px 32px 30px;padding:22px 26px;background:#fff;border:2px solid #10241a}
.lib-cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px}.lib-cols h3{font-size:15px;margin:0 0 6px}
.lib-cols p,.lib-cols li{font-size:13.5px;line-height:1.55;color:#2c3a31}.lib-cols ul,.lib-cols ol{padding-left:18px;margin:6px 0}
.lib-t{border-collapse:collapse;margin-top:14px;font-size:13px}.lib-t th,.lib-t td{border-bottom:1px solid #cfd8cc;padding:6px 14px 6px 0;text-align:left}
.g-h3{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:32px;margin:30px 32px 4px;line-height:1}
.bml-chips{display:flex;flex-direction:column;gap:8px}.bml-chip{display:flex;align-items:center;gap:10px;font-size:13px}
.bml-chip i{width:30px;height:22px;border-radius:4px;border:3px solid}.bml-chip span{color:#44544A}
@media (max-width:1100px){.lib-cols{grid-template-columns:1fr}}
'''

def fragment(doc):
    """The same page without doctype, html, head and body, for publishing as an artifact."""
    head = re.search(r'<head>(.*?)</head>', doc, re.S).group(1)
    body = re.search(r'<body[^>]*>(.*)</body>', doc, re.S).group(1)
    head = re.sub(r'<meta[^>]*>', '', head)
    return head + '<div style="margin:0">' + body + '</div>'

def main():
    base, rows, toc, css, tjs, n_el, n_sh, n_t = old_library()
    brows, btoc, bcss, bjs = bed_management()
    srows, stoc, scss, sjs = bm_solutions()
    arows, atoc, acss, ajs = bm_automations()
    prows, ptoc, pcss, pjs = bm_processes()
    drows, dtoc, dcss, djs = discharge_process()
    brows += srows + arows + prows; btoc += stoc + atoc + ptoc; bcss += scss + acss + pcss; bjs += sjs + ajs + pjs
    place_css = ''.join(open(os.path.join(COMMON, '%s-html-generator' % k, 'assets', '%s.css' % k), encoding='utf-8').read() for k in ('solutions', 'automations'))
    intro = ('<p class="g-lead" style="margin-top:0">One library for every tool. It holds the universal patterns, the Discharge Process landing pages and their parts '
             '(<b>%d landing-page elements</b>, <b>%d shared parts</b>), the regenerated Discharge Process turn templates and the Bed Management templates. '
             'Templates only: each is drawn as its canvas, never inside the app. Every template carries a badge: <b>Universal pattern</b> means any tool may use it, redrawn in its own look.</p>'
             '<div class="g-toc2"><a href="#how-to-use" style="background:#d4a94f;color:#10241a">How to use</a>%s%s%s</div>%s') % (n_el, n_sh, toc, dtoc, btoc, guide(n_el, n_sh, n_t))
    page = base.replace('</style>', place_css + css + dcss + bcss + GUIDE_CSS + '</style>', 1)
    page = page.replace('<div id="sample-turns">', intro + '<div id="sample-turns">', 1)
    page = page.replace('</body>', rows + drows + brows + '<textarea id="tojo-input" hidden aria-hidden="true"></textarea><script>' + tjs + '</script><script>' + bjs + djs + '</script></body>', 1)
    page = page.replace('<title>Tojo block library</title>', '<title>Tojo Block Library</title>', 1)
    page = re.sub(r'<h1>Tojo block library</h1>', '<h1>Tojo Block Library · every tool</h1>', page, count=1)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'block-library.html'), 'w', encoding='utf-8').write(page)
    open(os.path.join(OUT, 'block-library.artifact.html'), 'w', encoding='utf-8').write(fragment(page))
    print('wrote', os.path.join(OUT, 'block-library.html'), len(page) // 1024, 'kB')

if __name__ == '__main__':
    main()
