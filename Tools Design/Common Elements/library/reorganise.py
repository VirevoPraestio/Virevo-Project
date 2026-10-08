"""
reorganise: lay the one Tojo block library out the way Avishek asked on 8 Oct 2026.

  * No template belongs to one tool. Every template is open to every tool and every place.
    Templates are grouped by what they show, in eight groups:
      Logical · Process flow · Time flows · Selection · Financial · Numbers and measures ·
      People and ownership · Universal elements
    Inside each group: patterns and elements first, then worked turns (whole example
    responses), then drawing blocks (single drawings, described in words).
  * Every template carries a "How to use this template" card: what it shows, its key uses in
    order, the kinds of logic it can show, the responses it is best for, and, when its drawing
    carries a picture (beds, clocks, timelines, money, people), a note saying when to use it.
    The cards are written in library/template_uses.json.
  * Only the landing pages belong to a tool and a place. They come last, by group, by tool,
    by place (home, Diagnosis, Solutions, Automations, Processes), each tool's colours first.
  * The leftovers of the old sample turns (chat panels and phone canvases whose turns were
    replaced on 5 Oct) are dropped.

The source library (every injector writes to it) stays in the old order:
    out/block-library.source.html   -> this script ->   out/block-library.artifact.html
Run:  python3 reorganise.py SOURCE.html OUT.html
"""
import html, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
USES = os.path.join(HERE, 'template_uses.json')

ROW = re.compile(r'<section class="g-row[^"]*" id="([^"]+)"')
SEC = re.compile(r'<(/?)section\b')
DIV = re.compile(r'<(/?)div\b')

def _end(s, i, pat):
    depth = 0
    for m in pat.finditer(s, i):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return s.find('>', m.start()) + 1
    raise ValueError('unclosed element at %d' % i)

def split_rows(s):
    order, rows, i = [], {}, 0
    for m in ROW.finditer(s):
        if m.start() < i:
            continue
        j = _end(s, m.start(), SEC)
        order.append(m.group(1)); rows[m.group(1)] = s[m.start():j]; i = j
    return order, rows

e = lambda t: html.escape(t, quote=False)

CATS = [
 ('logical', 'Logical', 'Sides of an argument: claims and evidence, cause and effect, what people say against what is happening, before against after.', '#7A2E8C'),
 ('process', 'Process flow', 'Steps in order, routes, chains and hand-offs: where the work moves, stops or waits.', '#1E5AA8'),
 ('time', 'Time flows', 'Hours, days, weeks and trials: when things happen and how long they take.', '#0E7A6B'),
 ('selection', 'Selection', 'Several options side by side, and one or a few to pick or agree.', '#B0451A'),
 ('financial', 'Financial', 'Money effects: what it costs, what it saves, what comes back and when it pays for itself.', '#2F7350'),
 ('measures', 'Numbers and measures', 'Readings, gauges, counts and targets: how big, and how far from the goal.', '#8A5A00'),
 ('people', 'People and ownership', 'Who owns what: roles, seats, sign-offs and teams.', '#A0174F'),
 ('universal', 'Universal elements', 'Parts any response can use, whatever it is about: headings, notes, stamps, buttons and lists.', '#10241a'),
]
CAT = {k: (n, d, c) for k, n, d, c in CATS}
KINDS = [('pattern', 'Patterns and elements', 'Drawn at full size. Any tool redraws them in its own look and colours.'),
         ('turn', 'Worked turns', 'Whole example responses, built from several drawings. Use the shape and the logic; change the words to the tool’s own.'),
         ('block', 'Drawing blocks', 'Single drawings used inside the worked turns, described in words. Each says where it is drawn.')]

LANDING = re.compile(r'^(landing-(diagnosis|solutions|automations|processes)|(bm|odl|scp|rev|los)-(look|landing-.*))$')
PLACES = ['home', 'diagnosis', 'solutions', 'automations', 'processes']
TOOLS = [  # group, heading id, name, row prefix, colours for the contents chip
 ('ops', 'discharge-process', 'Discharge Process', 'landing-', ('#10241a', '#d4a94f')),
 ('ops', 'bed-management', 'Bed Management', 'bm-', ('#1A2B45', '#F3F1EA')),
 ('ops', 'opd-diagnostic-leak', 'OPD Diagnostic Leak', 'odl-', ('#2B1E05', '#F1E3B9')),
 ('fin', 'supply-chain-procurement', 'Supply Chain and Procurement', 'scp-', ('#0F1012', '#C6E43F')),
 ('fin', 'revenue-ebitda', 'Revenue &amp; EBITDA', 'rev-', ('#0C2E26', '#F2B233')),
 ('fin', 'length-of-stay', 'Length of Stay', 'los-', ('#0B2F3A', '#FF8A80')),
]

OWN_LEAD = {
 'discharge-process': '<p class="g-lead">The first tool: getting patients home on time. Its four place pages. The landing elements and shared parts they were built from, '
                      'and all its turn templates, are now open to every tool under Templates.</p>',
 'bed-management': '<p class="g-lead">The second tool: getting the right patient into the right bed. Its colours and its five landing pages; the home page is a ward plan and every place page draws from it. '
                   'Its turn templates and drawings are now open to every tool under Templates.</p>',
}

TURN_IDS = {}   # a turn named without its sample letter points to sample a

def kind(k):
    if '-block-' in k or k == 'bm-so-actions':
        return 'block'
    if re.match(r'^(dp|bm)-(dg|so|au|pr)-\d', k):
        return 'turn'
    return 'pattern'

def origin(k):
    if k.startswith('dp-'):
        return 'Discharge Process'
    if k.startswith('bm-'):
        return 'Bed Management'
    if re.match(r'^(dx|so|au|pr)-', k) or k in ('update-stamp', 'three-buttons', 'tojo-to-do'):
        return 'the Discharge Process landing pages'
    return None

def badge(k):
    n, _, c = CAT[k]
    return '<span class="g-cat" style="--c:%s">%s</span>' % (c, e(n))

def use_card(k, u):
    lst = lambda xs, tag='ul': '<%s>%s</%s>' % (tag, ''.join('<li>%s</li>' % e(x) for x in xs), tag)
    o = origin(k)
    motif = ('<p class="g-motif"><b>Picture in it:</b> %s</p>' % e(u['motif'])) if u.get('motif') else ''
    first = ('First drawn for %s. ' % o) if o else ''
    return ('<div class="g-use"><div class="g-use-h">How to use this template</div><p class="g-use-shows"><b>Shows:</b> %s</p>'
            '<div class="g-use-cols"><div><b>Key uses, most typical first</b>%s</div><div><b>Logic it can show</b>%s</div><div><b>Best for</b>%s</div></div>%s'
            '<p class="g-origin">%sOpen to every tool and every place: redraw it in the tool’s own look and colours, with the tool’s own words.</p></div>') % (
        e(u['shows']), lst(u['key_uses'], 'ol'), lst(u['logic']), lst(u['best_for']), motif, first)

def rework_template(k, row, u):
    i = row.find('<div class="g-meta">'); j = _end(row, i, DIV)
    meta = row[i:j]
    badges = '<span class="g-scope g-scope-all" title="Every tool in every group may use this template">Every tool</span>' + badge(u['category']) + (
        badge(u['also']) if u.get('also') and u['also'] != u['category'] else '')
    status = ''.join(re.findall(r'<span class="g-status"[^>]*>.*?</span>', meta))
    meta = re.sub(r'<span class="g-(status|scope)[^"]*"[^>]*>.*?</span>', '', meta)
    meta = re.sub(r'<div>\s*</div>', '', meta)
    meta = re.sub(r'(<div class="g-id">.*?)(</div>)', lambda m: re.sub(r'<span>(?:Bed Management|Discharge)(?: \w+)? drawing</span>', '<span>drawing</span>', m.group(1))
                  + '<em class="g-name">%s</em><span class="g-badges">%s%s</span>' % (e(u['name']), status, badges) + m.group(2), meta, count=1, flags=re.S)
    meta = re.sub(r'Drawn in:</b> ([a-z0-9-]+), shown above', lambda m: 'Drawn in:</b> <a href="#%s">%s</a>' % (TURN_IDS.get(m.group(1), m.group(1)), m.group(1)), meta)
    meta = re.sub(r'\bin any tab\b', 'in any place', meta)
    meta = re.sub(r'\btabs?\b', 'place', meta)
    meta = meta.replace('Drawn in:</b> not used yet, shown above', 'Drawn in:</b> not used in a turn yet')
    meta = meta[:-len('</div>')] + use_card(k, u) + '</div>'
    return row[:i] + meta + row[j:]

def rework_landing(k, row, tool):
    if tool == 'Discharge Process':   # these rows still say "Diagnosis only"
        row = re.sub(r'(<span class="g-scope g-scope-one"[^>]*>)(\w+) only(</span>)', r'\1Discharge Process · \2 only\3', row, count=1)
    return row

def headings(s):
    """Each tool's heading and lead, as it stands in the source."""
    out = {}
    for gid, hid, name, pre, col in TOOLS:
        m = re.search(r'<h2 class="g-h2[^"]*" id="%s">.*?</h2>(\s*<p class="g-lead">.*?</p>)?' % hid, s, flags=re.S)
        lead = m.group(1) if m and m.group(1) else ''
        out[hid] = lead
    return out

def build(s, uses):
    s = s.replace('<section class="g-row"><div class="g-meta"><div class="g-id">tool layer', '<section class="g-row" id="tool-layer"><div class="g-meta"><div class="g-id">tool layer', 1)
    order, rows = split_rows(s)
    TURN_IDS.clear(); TURN_IDS.update({k[:-2]: k for k in order if re.search(r'-\d\d-a$', k)})
    leads = headings(s)
    land = [k for k in order if LANDING.match(k)]
    tmpl = [k for k in order if not LANDING.match(k)]
    missing = [k for k in tmpl if k not in uses]
    if missing:
        raise SystemExit('no "how to use" card for: ' + ', '.join(missing))
    # ---- templates, by group
    parts, toc = [], []
    counts = {c: sum(1 for k in tmpl if uses[k]['category'] == c) for c, *_ in CATS}
    index_rows = []
    for k in tmpl:
        u = uses[k]
        index_rows.append('<tr><td><a href="#%s">%s</a></td><td>%s</td><td>%s%s</td><td>%s</td><td>%s</td></tr>' % (
            k, e(k), e(u['name']), badge(u['category']), badge(u['also']) if u.get('also') and u['also'] != u['category'] else '',
            {'pattern': 'Pattern or element', 'turn': 'Worked turn', 'block': 'Drawing block'}[kind(k)], e(u['motif'] or '—')))
    chips = ''.join('<a class="g-catchip" href="#t-%s" style="--c:%s"><b>%s</b><span>%d</span><em>%s</em></a>' % (c, col, e(n), counts[c], e(d)) for c, n, d, col in CATS)
    parts.append('<h2 class="g-h2 g-dom" id="templates">Templates · every tool</h2>'
                 '<p class="g-lead">Every template below is open to every tool, Operations and Financial, and to every place in it. None belongs to one tool. '
                 'They are grouped by what they show. Each one carries a card: what it shows, its key uses in order, the logic it can show and the responses it is best for. '
                 'When a drawing carries a picture (beds, a clock, a timeline, money, people), its card says when to reach for it. Example words in a template came from the tool it was first drawn for; '
                 'the tool using it puts in its own words, look and colours.</p>'
                 '<div class="g-cats">%s</div>'
                 '<details class="g-index"><summary>All %d templates at a glance</summary><table class="lib-t g-idx"><tr><th>Template</th><th>Name</th><th>Group</th><th>Kind</th><th>Picture in it</th></tr>%s</table></details>' % (
                     chips, len(tmpl), ''.join(index_rows)))
    toc.append('<a href="#templates" style="background:#C6E43F;color:#0F1012">Templates · every tool</a>')
    for c, n, d, col in CATS:
        mine = [k for k in tmpl if uses[k]['category'] == c]
        also = [k for k in tmpl if uses[k].get('also') == c and uses[k]['category'] != c]
        parts.append('<h3 class="g-h3 g-cath" id="t-%s" style="--c:%s">%s <span>%d templates</span></h3><p class="g-lead">%s</p>' % (c, col, e(n), len(mine), e(d)))
        if also:
            parts.append('<p class="g-also"><b>Also useful here:</b> %s</p>' % ' '.join('<a href="#%s">%s</a>' % (k, e(uses[k]['name'])) for k in also))
        for kd, kn, kdesc in KINDS:
            ks = [k for k in mine if kind(k) == kd]
            if not ks:
                continue
            parts.append('<h4 class="g-h4" id="t-%s-%s">%s · %s <span>%d</span></h4><p class="g-small g-kdesc">%s</p>' % (c, kd, e(n), e(kn), len(ks), e(kdesc)))
            parts += [rework_template(k, rows[k], uses[k]) for k in ks]
        toc.append('<a href="#t-%s" style="background:%s;color:#fff">%s · %d</a>' % (c, col, e(n), len(mine)))
    # ---- landing pages, by group, tool and place
    parts.append('<h2 class="g-h2 g-dom" id="landing-pages">Landing pages · by tool and by place</h2>'
                 '<p class="g-lead">Only the landing pages belong to one tool and one place. Each tool starts with its colours, then its pages in the order of the rail: '
                 'home, Diagnosis, Solutions, Automations, Processes. Operations Tools share the Operations look (rounded outlines, warm paper, drawn pictures); '
                 'Financial Tools share the Financial look (flat frame, report sheet, ledger paper, receipt). The Virevo type is the same everywhere.</p>')
    toc.append('<a href="#landing-pages" style="background:#10241a;color:#F3F1EA">Landing pages</a>')
    used = set()
    for gid, gname, gcol in (('ops', 'Operations Tools', ('#10241a', '#d4a94f')), ('fin', 'Financial Tools', ('#0F1012', '#C6E43F'))):
        gh = 'operations-tools' if gid == 'ops' else 'financial-tools'
        parts.append('<h3 class="g-h3 g-grp" id="%s" style="--c:%s">%s</h3>' % (gh, gcol[0], gname))
        toc.append('<a href="#%s" style="background:%s;color:%s">%s</a>' % (gh, gcol[0], gcol[1], gname))
        for g, hid, name, pre, col in TOOLS:
            if g != gid:
                continue
            mine = [k for k in land if k.startswith(pre) and (pre != 'landing-' or k.count('-') == 1)]
            def rank(k):
                if k.endswith('-look'):
                    return -1
                tail = k.split('landing-')[-1]
                return PLACES.index(tail) if tail in PLACES else 9
            mine.sort(key=rank)
            used.update(mine)
            lead = OWN_LEAD.get(hid) or leads.get(hid) or ''
            tag = '<span class="g-domtag%s">%s</span>' % (' g-domfin' if gid == 'fin' else '', gname)
            parts.append('<h4 class="g-h4 g-tool" id="%s">%s %s</h4>%s' % (hid, name, tag, lead))
            parts += [rework_landing(k, rows[k], name.replace('&amp;', '&')) for k in mine]
            toc.append('<a href="#%s" style="background:%s;color:%s">%s</a>' % (hid, col[0], col[1], name))
    left = [k for k in land if k not in used]
    if left:
        raise SystemExit('landing rows not placed: %s' % left)
    # scripts that sat between the rows (the canvas runtime): keep them all, after the rows
    a, t = s.find('<!--dom-resp-->'), s.find('<textarea id="tojo-input"')
    spans = sorted((s.find(r), s.find(r) + len(r)) for r in rows.values())
    gaps, pos = [], a
    for x, y in spans:
        if x < a:
            continue
        if x > pos:
            gaps.append(s[pos:x])
        pos = y
    gaps.append(s[pos:t])
    scripts = re.findall(r'<script\b.*?</script>', ''.join(gaps), flags=re.S)
    parts += scripts
    return ''.join(parts), ''.join(toc), len(tmpl), len(land)

CSS = r'''/*reorg-css*/
.g-name{display:block;font:500 15px/1.3 Poppins,sans-serif;letter-spacing:0;color:#3f4a44;margin-top:4px;text-transform:none}
.g-badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;font-size:14px;line-height:1}
.g-badges .g-status,.g-badges .g-scope{margin:0}
.g-id .g-badges .g-status,.g-id .g-badges .g-cat{color:#fff;font-size:12px}
.g-id .g-badges .g-scope{color:#10241a;font-size:12px}
.g-cat{display:inline-block;font:600 12px/1 Poppins,sans-serif;padding:5px 9px;margin:0 6px 4px 0;background:var(--c);color:#fff;border-radius:3px;justify-self:start;align-self:start}
.g-use{grid-column:1/-1;margin-top:10px;padding:14px 18px 12px;background:#fff;border:1.5px solid #10241a22;border-left:5px solid #10241a}
.g-use-h{font:400 22px/1 'Bebas Neue',sans-serif;letter-spacing:.02em;margin-bottom:6px}
.g-use-shows{font-size:14.5px;line-height:1.5;margin:0 0 10px}
.g-use-cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.g-use-cols b{display:block;font:600 11.5px Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#4a5a50;margin-bottom:4px}
.g-use-cols ol,.g-use-cols ul{margin:0;padding-left:18px;font-size:13.5px;line-height:1.45}
.g-use-cols li{margin:2px 0}
.g-motif{margin:10px 0 0;padding:8px 12px;background:#FFF5D6;border-left:4px solid #d4a94f;font-size:13.5px;line-height:1.45}
.g-origin{margin:8px 0 0;font-size:12.5px;color:#55635a}
.g-cats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:0 32px 16px;max-width:1260px}
.g-catchip{display:flex;flex-direction:column;gap:3px;padding:12px 14px;background:#fff;border-top:5px solid var(--c);text-decoration:none;color:#10241a}
.g-catchip b{font:400 22px/1 'Bebas Neue',sans-serif}
.g-catchip span{font:600 12px Poppins,sans-serif;color:var(--c)}
.g-catchip em{font-style:normal;font-size:12.5px;line-height:1.4;color:#4a5a50}
.g-index{margin:0 32px 28px;max-width:1260px}
.g-index summary{cursor:pointer;font:600 14px Poppins,sans-serif;padding:8px 0}
.g-idx td{font-size:13px;vertical-align:top}
.g-idx .g-cat{margin:0 4px 2px 0}
.g-cath{border-left:8px solid var(--c);padding-left:12px;margin-top:40px}
.g-cath span,.g-h4 span{font:600 13px Poppins,sans-serif;color:#55635a;margin-left:8px}
.g-h4{font:400 26px/1.1 'Bebas Neue',sans-serif;margin:26px 32px 4px}
.g-kdesc{margin:0 32px 8px}
.g-also{margin:0 32px 10px;font-size:13.5px;line-height:1.7}
.g-also a{display:inline-block;margin-right:6px;padding:1px 8px;background:#fff;border:1px solid #10241a33;border-radius:3px;text-decoration:none;color:#10241a;font-size:12.5px}
.g-grp{border-left:8px solid var(--c);padding-left:12px;margin-top:40px;font-size:34px}
.g-tool{font-size:30px;margin-top:34px}
@media (max-width:900px){.g-use-cols{grid-template-columns:1fr}.g-cats{grid-template-columns:1fr 1fr}}
/*/reorg-css*/'''

def reorganise(s, uses):
    body, toc, nt, nl = build(s, uses)
    a = s.find('<div id="sample-turns">')
    t = s.find('<textarea id="tojo-input"')
    head = s[:a]
    # the top: words, contents
    head = re.sub(r'<p>Registry v4 .*?</p>', '<p>8 Oct 2026 · %d templates open to every tool, grouped by what they show · %d landing-page rows, by tool and by place. '
                  'Each template is shown at the desktop canvas width and the mobile canvas width from the same markup.</p>' % (nt, nl), head, count=1, flags=re.S)
    head = re.sub(r'<div class="g-toc">.*?</div>', '', head, count=1, flags=re.S)
    head = re.sub(r'<p class="g-lead" style="margin-top:0">.*?</p>',
                  '<p class="g-lead" style="margin-top:0">One library for every tool, in two parts. <b>Templates</b>: every response template, open to every tool and every place, '
                  'grouped by what it shows (Logical, Process flow, Time flows, Selection, Financial, Numbers and measures, People and ownership, Universal elements), each with a card on how to use it. '
                  '<b>Landing pages</b>: the only tool-specific part, by group (Operations Tools, Financial Tools), by tool and by place.</p>', head, count=1, flags=re.S)
    head = re.sub(r'<div class="g-toc2">.*?</div>', '<div class="g-toc2"><a href="#how-to-use" style="background:#d4a94f;color:#10241a">How to use</a>%s</div>' % toc, head, count=1, flags=re.S)
    # the guide
    head = re.sub(r'<h3>One library, every tool</h3>.*?</ul>',
                  '<h3>One library, every tool</h3><p>Every tool draws its turns from the templates here, and its own landing pages.</p><ul>'
                  '<li><b>Every template is open to every tool</b> and every place: Discharge Process, Bed Management, OPD Diagnostic Leak, Supply Chain and Procurement, Revenue &amp; EBITDA, Length of Stay, and any tool to come. '
                  'The tool redraws it in its own look and colours, with its own words.</li>'
                  '<li><b>Groups.</b> Logical (sides of an argument), Process flow, Time flows, Selection (pick one or a few), Financial (money effects), Numbers and measures, People and ownership, Universal elements (parts any response can use). '
                  'A template may also be useful in a second group; that group lists it under “Also useful here”.</li>'
                  '<li><b>Pictures.</b> When a drawing carries a picture (beds, a clock, a timeline, money, people, a route), its card says when to use it: reach for it whenever the response is about that thing.</li>'
                  '<li><b>Landing pages</b> are the only tool-specific part: by tool and by place, at the end.</li>'
                  '<li><b>Approved</b>, <b>variation</b> (a sample not chosen, ready as a pattern) or <b>draft</b>.</li></ul>', head, count=1, flags=re.S)
    head = head.replace('Pick the fewest blocks that carry what the chat cannot: approved first, then variations. Each block below says <i>use when</i> and <i>avoid when</i>.',
                        'Find the group that matches what the response must show, then pick the fewest templates that carry what the chat cannot: approved first, then variations. '
                        'Each template’s card says what it shows, its key uses, the logic it can show and the responses it is best for.')
    head = re.sub(r'<p class="g-small">In this build:.*?</p>',
                  '<p class="g-small">In this build: %d templates open to every tool (the universal patterns, the 20 landing elements and 3 shared parts, the 32 Discharge Process turn templates and their drawings, '
                  'the Bed Management turn templates and their drawings), grouped by what they show; and the landing pages of all six tools: Discharge Process, Bed Management and OPD Diagnostic Leak (Operations Tools), '
                  'Supply Chain and Procurement, Revenue &amp; EBITDA and Length of Stay (Financial Tools). Everything is drawn as its canvas only, never inside the app interface.</p>' % nt, head, count=1, flags=re.S)
    head = head.replace('</style>', CSS + '</style>', 1) if '/*reorg-css*/' not in head else head
    # head ends inside <div style="margin:0">: close it, then the two parts, then the closing scripts
    return head + '</div>' + body + s[t:]

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    uses = json.load(open(USES, encoding='utf-8'))
    out = reorganise(open(src, encoding='utf-8').read(), uses)
    open(dst, 'w', encoding='utf-8').write(out)
    print('wrote', dst, len(out))
