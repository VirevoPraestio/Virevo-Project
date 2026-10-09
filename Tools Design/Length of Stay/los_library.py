"""
los_library: the Length of Stay section of the one Tojo block library, under Financial Tools
(approved 8 Oct 2026: home A, the patient's path, and the four place pages).

What it adds or changes, and nothing else (every other template stays byte for byte the same):
  * the Length of Stay section after Revenue & EBITDA: its colours, then the five landing pages,
    each as its canvas at 864px and 362px with its first-visit state under a fold;
  * the Financial Tools lead, the guide's line about the two groups and the "In this build"
    sentences now name Length of Stay;
  * contents links and one guide row.

Blocks only (rules/08 §7). Each page's picking groups get their own prefix. CSS is scoped under .lsx.
Needs the Revenue & EBITDA section (rev_library.py) to be in the library first.

Used two ways:
  build_block_library.py   calls inject(page, scope_css) after rev_library on a full rebuild;
  python3 los_library.py LIB.html OUT.html   updates an existing library file in place.
"""
import os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import los_landing as H
# this tool's places.py, loaded under its own name (Revenue & EBITDA also has a places.py)
_spec = importlib.util.spec_from_file_location('los_places', os.path.join(HERE, 'places.py'))
P = importlib.util.module_from_spec(_spec); sys.modules['los_places'] = P; _spec.loader.exec_module(P)
C, L2, L3 = H.C, H.L2, H.L3

e = C.e
MARK_A, MARK_B = '<!--los-section-->', '<!--/los-section-->'
CSS_A, CSS_B = '/*los-css*/', '/*/los-css*/'
TOC_A, TOC_B = '<!--los-toc-->', '<!--/los-toc-->'
AFTER_SEC, AFTER_CSS, AFTER_TOC = '<!--/rev-section-->', '/*/rev-css*/', '<!--/rev-toc-->'
SCOPE = '<span class="g-scope g-scope-one" title="Only Length of Stay uses this template">Length of Stay only</span>'
FIN = '<span class="g-scope g-scope-all" style="background:#0F1012;color:#C6E43F" title="The Financial look, shared by every Financial tool">Financial Tools look</span>'
OK = '<span class="g-status" style="background:#2f7350">approved</span>'
FILES = {'home': 'los_landing.a_canvas', 'diagnosis': 'places.dg_canvas', 'solutions': 'places.so_canvas',
         'automations': 'places.au_canvas', 'processes': 'places.pr_canvas'}
WHAT = {
 'home': 'The stay drawn as a route through the hospital: Emergency, ICU, step-down, wards, home. Each stop shows its days now against the goal, '
         'the extra days a month and what they cost; a double-ruled total for the whole hospital. Each part of the work is a patient wristband with one day box per step. '
         'On a phone the bands stack and each opens under itself.',
 'diagnosis': 'One typical stay followed day by day: a strip of the days in each area with the extra hatched, then each step as a line of the chart (when, where, what happened, the extra); '
              'the tapped line opens beside the chart. Below it, the extra days of the month split by cause, one square for every 13 days.',
 'solutions': 'One ruled entry per fix: its four stops, the days it frees a month, and the beds that gives back every day, drawn as beds; a double-ruled total. '
              'Each entry opens to its by-hand and automatic versions side by side.',
 'automations': 'A 24-hour clock face, night shaded, each helper set at the hour it runs. Under it, one bedside monitor per helper showing the list or warning it would put up, '
                'with its four lamps; its box says what it reads, who sees it and when it runs.',
 'processes': 'A whiteboard week with each change as a magnet on its days, the new role and a two-month trial; who owns the flow in each area, Emergency to home; '
              'the numbers we watch, now and plan.',
}
NAMES = {'home': 'aqua, petrol and coral red', 'diagnosis': 'pale rose, deep cobalt and spring green',
         'solutions': 'pale lemon, graphite and magenta', 'automations': 'pale butter, ox-blood and monitor yellow',
         'processes': 'whiteboard, indigo and marker cyan'}

def _own_groups(html, k):
    tok = 'los' + k[:2]
    html = re.sub(r'data-grp="([a-z]+)"', lambda m: 'data-grp="%s%s"' % (tok, m.group(1)), html)
    return re.sub(r'data-box="([a-z]+):', lambda m: 'data-box="%s%s:' % (tok, m.group(1)), html)

def _canvas(k, state):
    place, spec, label, title = P.PAGES[k]
    if spec is None:
        fn, cls = H.a_canvas, 'ls ls-home ls-a'
    else:
        fn, cls = spec[0], 'ls ls-%s' % k
    t = P.THEMES[k]
    return '<div class="lsx"><div class="lp-host"><div class="lp bm skin-v %s" style="%s">%s</div></div></div>' % (cls, t['vars'], _own_groups(fn(state), k))

def section(scope_css):
    rows, toc = [], []
    rows.append('<h2 class="g-h2" id="length-of-stay">Length of Stay <span class="g-domtag g-domfin">Financial Tools</span></h2>'
                '<p class="g-lead">The sixth tool and the third Financial one: how long patients stay, of every kind. The wait in Emergency for a bed, days in the ICU, in step-down, '
                'on the wards, and the hospital as a whole. Every extra day is a bed someone else waits for and a day the hospital pays for. Same five zones and the same behaviour as every tool '
                '(first element raised with its box open, on a phone each box under its element and every pick stacked, the three buttons). '
                'Same Financial look as Supply Chain and Procurement; only the colours change. Example figures are made up for an example 250-bed hospital and marked Example only or Tojo’s guess.</p>')
    toc.append('<a href="#length-of-stay" style="background:#0B2F3A;color:#FF8A80">Length of Stay</a>')
    chips = ''.join('<div class="bml-chip"><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 5px %s"></i><b>%s</b><span>%s</span></div>' % (
        P.THEMES[k]['ground'], P.THEMES[k]['ink'], P.THEMES[k]['hi'], e(v[2]), e(v[3])) for k, v in P.PAGES.items())
    words = '; '.join('%s %s' % (P.PAGES[k][2], NAMES[k]) for k in P.PAGES)
    rows.append('<section class="g-row" id="los-look"><div class="g-meta"><div class="g-id">Length of Stay · the look <span>palette</span></div>%s%s%s'
                '<p><b>One palette per place: ground, ink and a highlight,</b> none used by another tool. %s. The rail carries each place’s ground. '
                'Every text pair clears 4.5:1.</p></div><div class="g-views"><div><div class="bml-chips">%s</div></div></div></section>' % (
                    OK, FIN, '<p>The Financial look as set out under Supply Chain and Procurement: Virevo type unchanged, flat frame, report sheet, ledger paper and receipt. '
                    'The drawings are of a hospital stay: the route from Emergency to home, wristbands, a patient’s chart, beds, a ward clock, bedside monitors and the bed board.</p>', e(words), chips))
    toc.append('<a href="#los-look">los look</a>')
    rows.append('<h3 class="g-h3" id="los-landing">Approved landing pages</h3>')
    for k, v in P.PAGES.items():
        label, name = v[2], v[3].replace(' (approved)', '')
        full = _canvas(k, 'filled')
        meta = ('<p><b>%s landing page, %s.</b> %s</p><p class="g-small">Drawn by <code>Length of Stay/%s</code> with the V skin (<code>Supply Chain Procurement/skins.py</code>), '
                'on the Bed Management page parts loaded as a copy (<code>sc_common.py</code>). Five zones in the fixed order: masthead with Refresh now, where this stands, '
                'the drawing, what Tojo still has to do, the three buttons.</p>'
                '<details class="g-first"><summary>See its first-visit state</summary><div style="width:864px;margin-top:8px">%s</div></details>') % (
            e(label), e(name), e(WHAT[k]), FILES[k].replace('.', '.py · '), _canvas(k, 'empty'))
        rows.append(('<section class="g-row" id="los-landing-%s"><div class="g-meta"><div class="g-id">Length of Stay · %s <span>%s</span></div>%s%s%s</div>'
                     '<div class="g-views"><div><div class="g-cap">Desktop canvas · 864px</div><div style="width:864px">%s</div></div>'
                     '<div><div class="g-cap">Mobile canvas · 362px</div><div style="width:362px">%s</div></div></div></section>') % (
            k, e(label), e(name), OK, SCOPE, meta, full, full))
        toc.append('<a href="#los-landing-%s">los-%s</a>' % (k, k))
    B = C.B
    page_css = (C._accent(B.BASE_CSS + B.SEL_CSS) + H.SK['css'] + L2.V_SHARED_CSS + L3.PLACE_CSS + H.A_CSS
                + ''.join(v[1][1] for v in P.PAGES.values() if v[1]))
    return ''.join(rows), ''.join(toc), scope_css(page_css, '.lsx')

GUIDE_ROW = '<tr><td>Length of Stay · landing pages</td><td><code>Length of Stay/los_landing.py</code>, <code>places.py</code> (data)</td><td><code>Length of Stay/los_landing.py</code>, <code>places.py</code>, <code>los_library.py</code></td></tr>'
REPL = [
 ('Tools in this group: Supply Chain and Procurement, Revenue &amp; EBITDA.</p>', 'Tools in this group: Supply Chain and Procurement, Revenue &amp; EBITDA, Length of Stay.</p>'),
 ('<b>Financial Tools</b>: Supply Chain and Procurement, Revenue &amp; EBITDA. ', '<b>Financial Tools</b>: Supply Chain and Procurement, Revenue &amp; EBITDA, Length of Stay. '),
 ('and the five landing pages each of Supply Chain and Procurement and Revenue &amp; EBITDA (Financial Tools). Everything is drawn',
  'and the five landing pages each of Supply Chain and Procurement, Revenue &amp; EBITDA and Length of Stay (Financial Tools). Everything is drawn'),
 ('and the Supply Chain and Procurement and Revenue &amp; EBITDA landing pages (Financial Tools).',
  'and the Supply Chain and Procurement, Revenue &amp; EBITDA and Length of Stay landing pages (Financial Tools).'),
]

def inject(lib, scope_css):
    if AFTER_SEC not in lib:
        raise SystemExit('run rev_library first: the Revenue & EBITDA section is missing')
    rows, toc, css = section(scope_css)
    def put(a, b, new, after):
        nonlocal lib
        if a in lib:
            lib = re.sub(re.escape(a) + '.*?' + re.escape(b), lambda m: a + new + b, lib, count=1, flags=re.S)
        else:
            i = lib.find(after) + len(after)
            lib = lib[:i] + a + new + b + lib[i:]
    put(MARK_A, MARK_B, rows, AFTER_SEC)
    put(CSS_A, CSS_B, css, AFTER_CSS)
    put(TOC_A, TOC_B, toc, AFTER_TOC)
    if GUIDE_ROW not in lib:
        lib = lib.replace('</table><p class="g-small">In this build:', GUIDE_ROW + '</table><p class="g-small">In this build:', 1)
    for a, b in REPL:
        lib = lib.replace(a, b)
    return lib

if __name__ == '__main__':
    lib_py = os.path.join(os.path.dirname(HERE), 'Common Elements', 'library', 'build_block_library.py')
    code = open(lib_py, encoding='utf-8').read()
    ns = {}
    exec(compile('import re\n' + code[code.find('def _split_sel'):code.find('def load(')], 'scope', 'exec'), ns)
    src, dst = sys.argv[1], sys.argv[2]
    out = inject(open(src, encoding='utf-8').read(), ns['scope_css'])
    open(dst, 'w', encoding='utf-8').write(out)
    print('wrote', dst, len(out))
