"""
Build the complete Tojo block library: the Diagnosis block library (from diagnosis_html.py gallery)
plus every element taken from the landing-page samples, the shared landing parts, and the four
approved landing pages. Elements are cut from the rendered samples, so they always match the
templates exactly.

  python3 build_library.py -o ../out/gallery.html
"""
import argparse, json, os, re, sys
import landing_common as lc
from build_landing import load, TABS

sys.path.insert(0, lc.DIAG)
import diagnosis_html as dh  # noqa: E402

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
TAG = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9-]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>')

def cut(html_s, cls):
    """Outer HTML of the first element whose class list contains cls."""
    pat = re.compile(r'class="([^"]*)"')
    for m in TAG.finditer(html_s):
        if m.group(1): continue
        c = pat.search(m.group(3))
        if not c or cls not in c.group(1).split(): continue
        depth = 0
        for n in TAG.finditer(html_s, m.start()):
            name = n.group(2).lower(); selfc = n.group(3).rstrip().endswith('/')
            if name in VOID or selfc: 
                if n.start() == m.start(): return n.group(0)
                continue
            depth += -1 if n.group(1) else 1
            if depth == 0: return html_s[m.start():n.end()]
    raise KeyError(cls)

TABCLS = {'diagnosis': 'lp-dx', 'solutions': 'lp-so', 'automations': 'lp-au', 'processes': 'lp-pr'}
PREFIX = {'diagnosis': 'dx', 'solutions': 'so', 'automations': 'au', 'processes': 'pr'}
BADGE = {'approved': ('#2f7350', 'approved in landing page'), 'variation': ('#2E5E8E', 'variation')}

def render(mod, tab, sample, state='filled'):
    fn = {k: f for k, _, _, f in mod.SAMPLES}[sample]
    return fn(lc.Mode('html', state, mod.DATA))

def wrap(tab, sample, inner, state='filled'):
    return '<div class="lp-host"><div class="lp %s %s-%s lp-el" data-lp-state="%s">%s</div></div>' % (TABCLS[tab], TABCLS[tab], sample, state, inner)

def scope(tab_or_all, drawn_in=''):
    return dh.scope_badge(tab_or_all, drawn_in)

def row(rid, title, tag, badge, meta, desk, mob):
    color, label = badge
    return ('<section class="g-row" id="%s"><div class="g-meta"><div class="g-id">%s <span>%s</span></div><span class="g-status" style="background:%s">%s</span>%s</div>'
            '<div class="g-views"><div><div class="g-cap">Desktop canvas · 864px</div><div style="width:864px">%s</div></div>'
            '<div><div class="g-cap">Mobile canvas · 362px</div><div style="width:362px">%s</div></div></div></section>') % (rid, lc.e(title), lc.e(tag), color, label, meta, desk, mob)

def section(reg_path):
    cat = json.load(open(reg_path, encoding='utf-8'))
    lreg = json.load(open(os.path.join(lc.HERE, 'landing-registry.json'), encoding='utf-8'))
    mods = {t: load(t) for t in TABS}
    cache = {}
    def page(t, s, st='filled'):
        k = (t, s, st)
        if k not in cache: cache[k] = render(mods[t], t, s, st)
        return cache[k]
    rows, toc, css = [], [], ''.join(m.CSS for m in mods.values())
    # 1. approved landing pages, whole
    rows.append('<h2 class="g-h2" id="landing-pages">Approved landing pages</h2><p class="g-lead">One per tab, shown whole. The same five zones in the same order, drawn in each tab’s own look.</p>')
    toc.append('<a href="#landing-pages" style="background:#10241a;color:#F3F1EA">Landing pages</a>')
    for t in TABS:
        s = lreg['tabs'][t]['approved']; nm = lreg['tabs'][t]['samples'][s]['name']
        full = page(t, s)
        meta = '<p><b>%s landing page, %s.</b> Template %s in <code>%s-html-generator/landing.py</code>.</p><p class="g-small">First visit shows the same zones as dashed outlines, each saying what fills it.</p>' % (t.capitalize(), lc.e(nm), s.upper(), t)
        rows.append(row('landing-%s' % t, '%s · %s' % (t.capitalize(), nm), 'landing ' + s.upper(), BADGE['approved'], scope(t.capitalize()) + meta, full, full))
    # 2. shared parts, one variant per tab
    rows.append('<h2 class="g-h2" id="shared-parts">Shared landing parts</h2><p class="g-lead">The same part in every tab, each drawn in that tab’s look.</p>')
    toc.append('<a href="#shared-parts" style="background:#10241a;color:#F3F1EA">Shared parts</a>')
    for sh in cat['shared']:
        desk = []
        for t in TABS:
            s = lreg['tabs'][t]['approved']; sel = sh['selector'].replace('{p}', PREFIX[t])
            desk.append('<div class="g-var"><div class="g-vcap">%s</div>%s</div>' % (t.capitalize(), wrap(t, s, cut(page(t, s), sel))))
        meta = '<p><b>%s.</b> %s</p><p class="g-small"><b>Reuse in:</b> %s</p>' % (lc.e(sh['name']), lc.e(sh['purpose']), lc.e(sh['reuse_in']))
        rows.append(row(sh['id'], sh['name'], 'shared', BADGE['approved'], scope('all', 'every place') + meta, ''.join(desk), ''.join(desk)))
        toc.append('<a href="#%s">%s</a>' % (sh['id'], sh['id']))
    # 3. elements by tab
    for t in TABS:
        rows.append('<h2 class="g-h2" id="el-%s">%s elements</h2><p class="g-lead">Drawn in the %s look. Approved ones are part of the approved landing page; variations come from the samples not chosen, and are ready to use as patterns in turns.</p>' % (t, t.capitalize(), t.capitalize()))
        toc.append('<a href="#el-%s" style="background:#10241a;color:#F3F1EA">%s</a>' % (t, t.capitalize()))
        for el in [x for x in cat['elements'] if x['tab'] == t]:
            piece = wrap(t, el['sample'], cut(page(t, el['sample']), el['selector']))
            empty = wrap(t, el['sample'], cut(page(t, el['sample'], 'empty'), el['selector']), 'empty')
            meta = ('<p><b>%s.</b> %s</p><p class="g-small"><b>Reuse in:</b> %s<br><b>From:</b> %s landing sample %s</p>'
                    '<details class="g-first"><summary>See its first-visit state</summary><div style="width:864px;margin-top:8px">%s</div></details>') % (
                lc.e(el['name']), lc.e(el['purpose']), lc.e(el['reuse_in']), t.capitalize(), el['sample'].upper(), empty)
            sc = scope(t.capitalize()) if el['status'] == 'approved' else scope('all', t.capitalize())
            rows.append(row(el['id'], el['name'], el['id'], BADGE[el['status']], sc + meta, piece, piece))
            toc.append('<a href="#%s">%s</a>' % (el['id'], el['id']))
    css += lc.LP_BASE_CSS + '''
.g-h2{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:44px;margin:40px 32px 4px;line-height:1}
.g-lead{margin:0 32px 18px;max-width:780px;font-size:14.5px;color:#44544A;line-height:1.5}
.g-var{margin-bottom:14px}.g-vcap{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#44544A;margin-bottom:4px}
.g-first summary{cursor:pointer;font-size:13px;font-weight:600;display:inline-flex;min-height:40px;align-items:center;padding:0 14px;border:1.5px solid #10241a;border-radius:20px}
.lp-el{padding:16px 18px 18px !important}
.g-toc2{display:flex;flex-wrap:wrap;gap:8px;padding:0 32px 20px}
.g-toc2 a{font-size:13px;padding:6px 12px;border:1.5px solid #10241a;border-radius:16px;color:#10241a;text-decoration:none}
'''
    return ''.join(rows), ''.join(toc), css, len(cat['elements']), len(cat['shared'])

GENS = [('solutions', 'Solutions', 'solutions_html'), ('automations', 'Automations', 'automations_html'), ('processes', 'Processes', 'processes_html')]

def turn_templates():
    """The approved turn templates of Solutions, Automations and Processes, each drawn from its first use in an approved turn."""
    import importlib.util
    rows, toc, css, js, n = [], [], '', [], 0
    for key, name, modname in GENS:
        path = os.path.join(lc.ROOT, '%s-html-generator' % key, modname + '.py')
        spec_ = importlib.util.spec_from_file_location('lib_' + modname, path)
        mod = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(mod)
        reg = mod.load_registry(); css += mod.css_all(); js.append(mod.PAGE_JS)
        ex = os.path.join(lc.ROOT, 'examples', key)
        turns = [json.load(open(os.path.join(ex, t['file']), encoding='utf-8')) for t in json.load(open(os.path.join(ex, 'turns.json'), encoding='utf-8'))['turns']]
        rows.append('<h2 class="g-h2" id="turns-%s">%s turn templates</h2><p class="g-lead">Every approved %s block, drawn by its generator from its first use in an approved turn. '
                    'Each is live: try it on the desktop and the phone width. The badge says whether it is for %s only or a universal pattern.</p>' % (key, name, name, name))
        toc.append('<a href="#turns-%s" style="background:#10241a;color:#F3F1EA">%s turns</a>' % (key, name))
        skipped = []
        for rb in reg['blocks']:
            if rb['id'] == 'landing': continue
            use = next(((t, b) for t in turns for b in t['canvas']['blocks'] if b.get('type') == rb['id']), None)
            if rb['status'] != 'approved' or not use:
                skipped.append(rb['id']); continue
            t, b = use; one = json.loads(json.dumps(t)); one['canvas']['blocks'] = [b]
            html_ = mod.render_canvas(one, reg)
            fb = rb.get('feedback', [])
            meta = ('<p><b>%s.</b> %s</p><p class="g-small"><b>Use when:</b> %s<br><b>Avoid when:</b> %s%s</p><p class="g-small"><b>Shown from:</b> turn %s · <b>Last feedback:</b> %s</p>') % (
                lc.e(rb.get('category', '').capitalize()), lc.e(rb['purpose']), lc.e('; '.join(rb['use_when'])), lc.e('; '.join(rb['avoid_when'])),
                ('<br><b>Interaction:</b> ' + lc.e(rb['interaction'])) if rb.get('interaction') else '', lc.e(t['turn']['id']), lc.e(fb[-1]['note'] if fb else 'none yet'))
            rid = '%s-%s' % (key[:2], rb['id'])
            rows.append(row(rid, '%s · %s' % (name, rb['id']), 'v%d' % rb.get('version', 1), ('#2f7350', 'approved') if rb['status'] == 'approved' else ('#B8862B', rb['status']),
                            scope(rb.get('scope', 'all') if rb.get('scope') != 'all' else 'all', name) + meta, html_, html_))
            toc.append('<a href="#%s">%s</a>' % (rid, rid)); n += 1
        if skipped:
            rows.append('<p class="g-lead"><b>Not shown (draft or unused in approved turns):</b> %s</p>' % lc.e(', '.join(skipped)))
    return ''.join(rows), ''.join(toc), css, '\n'.join(js), n

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('-o', '--out', default=os.path.join(lc.ROOT, 'out', 'gallery.html')); a = ap.parse_args()
    reg = dh.load_registry() if hasattr(dh, 'load_registry') else json.load(open(os.path.join(lc.ROOT, 'blocks', 'registry.json'), encoding='utf-8'))
    base = dh.gallery(reg)
    rows, toc, css, n_el, n_sh = section(os.path.join(lc.HERE, 'landing-elements.json'))
    trows, ttoc, tcss, tjs, n_t = turn_templates()
    rows += trows; toc += ttoc; css += tcss
    intro = ('<p class="g-lead" style="margin-top:0">This library holds the Diagnosis blocks, <b>%d landing-page elements</b>, <b>%d shared parts</b> and <b>%d approved turn templates</b> '
             'from Solutions, Automations and Processes. Every template carries a badge: <b>Universal pattern</b> means any place may use it, redrawn in its own look by its own generator. '
             '<b>Solutions only</b>, <b>Automations only</b> and so on mean only that place uses it.</p>'
             '<div class="g-toc2">%s</div>') % (n_el, n_sh, n_t, toc)
    base = base.replace('</style>', css + '</style>', 1)
    base = base.replace('<div id="sample-turns">', intro + '<div id="sample-turns">', 1)
    base = base.replace('</body>', rows + '<textarea id="tojo-input" hidden aria-hidden="true"></textarea><script>' + tjs + '</script></body>', 1)
    base = base.replace('<title>Tojo block library</title>', '<title>Tojo block library</title>', 1)
    open(a.out, 'w', encoding='utf-8').write(base)
    print('wrote', a.out, len(base) // 1024, 'kB')

if __name__ == '__main__':
    main()
