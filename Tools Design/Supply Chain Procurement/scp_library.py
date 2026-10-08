"""
scp_library: the Supply Chain and Procurement section of the one Tojo block library, and the
grouping of the library by domain (approved 8 Oct 2026).

What it adds or replaces, and nothing else (every other template stays byte for byte the same):
  * a "Response templates · every tool" heading over the universal patterns, saying every tool
    in every domain draws its turns from them;
  * an "Operations Tools" heading before the Discharge Process landing pages, and an
    "Operations Tools" tag on the Discharge Process, Bed Management and OPD Diagnostic Leak headings;
  * a "Financial Tools" heading and the Supply Chain and Procurement section: the Financial look,
    then the five approved landing pages (home: the notebook; the four places), each as its canvas at
    864px and 362px with its first-visit state under a fold;
  * contents links, one guide row, one guide line about domains, and the "In this build" sentences.

Blocks only (rules/08 §7). Each page's picking groups get their own prefix. CSS is scoped under .scx.

Used two ways:
  build_block_library.py   calls inject(page, scope_css) after the OPD section on a full rebuild;
  python3 scp_library.py LIB.html OUT.html   updates an existing library file in place.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sc_common as C
import landing2 as L2
import landing3 as L3

e = C.e
MARK_A, MARK_B = '<!--scp-section-->', '<!--/scp-section-->'
CSS_A, CSS_B = '/*scp-css*/', '/*/scp-css*/'
TOC_A, TOC_B = '<!--scp-toc-->', '<!--/scp-toc-->'
RESP_A, RESP_B = '<!--dom-resp-->', '<!--/dom-resp-->'
OPS_A, OPS_B = '<!--dom-ops-->', '<!--/dom-ops-->'
OPSTOC_A, OPSTOC_B = '<!--dom-ops-toc-->', '<!--/dom-ops-toc-->'
DOMLI_A, DOMLI_B = '<!--dom-li-->', '<!--/dom-li-->'
OPS_TAG = '<span class="g-domtag">Operations Tools</span>'
SCOPE = '<span class="g-scope g-scope-one" title="Only Supply Chain and Procurement uses this template">Supply Chain and Procurement only</span>'
FIN = '<span class="g-scope g-scope-all" style="background:#0F1012;color:#C6E43F" title="The Financial look, shared by every Financial tool">Financial Tools look</span>'
OK = '<span class="g-status" style="background:#2f7350">approved</span>'
FILES = {'home': 'landing2.f_canvas', 'diagnosis': 'landing3.dg_canvas', 'solutions': 'landing3.so_canvas',
         'automations': 'landing3.au_canvas', 'processes': 'landing3.pr_canvas'}
WHAT = {
 'home': 'The notebook. The month’s money as a till receipt stapled on, its total marked in the highlight. The work as an open spiral notebook: the four parts on the left page with their step bars and counts, the open part’s steps on the right page, and a hand note marking where we are. On a phone the notebook closes to one page and each part opens under itself.',
 'diagnosis': 'The item’s receipt. One item followed from the ward’s request to the patient’s bill, each loss printed as a line with its amount, the tapped line opening beside the receipt. Below it, the four possible main causes as report bars, the leading one in ink, one square per piece of evidence.',
 'solutions': 'The ledger of fixes. One ruled entry per fix with a double margin, its four stops ticked across, what it brings back in the money column, and a double-ruled total. Each entry opens to its by-hand and automatic versions side by side.',
 'automations': 'The helpers’ day. A flat 24-hour bar, night in ink, each helper pinned at the hour it runs. Under it, one card per helper with its four lamps and the slip it would print. Its box says what it reads, who gets the slip, when it runs and what it waits for.',
 'processes': 'The week planner. A ruled notebook week with the changes pinned on their days, the daily look as a strip across the week, the four-week trial at the foot. Then a signature register (who signs for what) and the numbers we watch, now against goal.',
}
LOOK = ('<p><b>The Financial look, shared by every Financial tool.</b> The Virevo type is unchanged (Bebas Neue, Poppins, Caveat, at the 07 sizes); '
        'what marks the domain is the paper and the shapes: a flat frame with no rounded corners, heavy rules, numbered sections, a flat chat panel in the page’s ink, '
        'a hard block in the highlight when an item is raised, and the three papers of money: the <b>report sheet</b> (flat planes, big figures), '
        '<b>ledger paper</b> (ruled lines, a double margin, double-ruled totals) and the <b>receipt</b> (torn zigzag edges, dashed tear lines, dotted leaders). '
        'Each tool in the domain, and each place in it, changes only its colours.</p>')

def _own_groups(html, k):
    tok = 'scp' + k[:2]
    html = re.sub(r'data-grp="([a-z]+)"', lambda m: 'data-grp="%s%s"' % (tok, m.group(1)), html)
    return re.sub(r'data-box="([a-z]+):', lambda m: 'data-box="%s%s:' % (tok, m.group(1)), html)

def _page(k):
    place, spec, label, title = L3.PAGES[k]
    if spec is None:
        return L2.f_canvas, 'sc sc-home vf', L3.PLACE_CSS
    fn, css, data = spec
    return fn, 'sc sc-%s' % k, css

def _canvas(k, state):
    fn, cls, _ = _page(k)
    t = L3.THEMES[k]
    inner = _own_groups(fn(state), k)
    return '<div class="scx"><div class="lp-host"><div class="lp bm skin-v %s" style="%s">%s</div></div></div>' % (cls, t['vars'], inner)

def section(scope_css):
    rows, toc = [], []
    rows.append('<h2 class="g-h2 g-dom" id="financial-tools">Financial Tools</h2><p class="g-lead">Tools about money: what the hospital buys, pays and bills. '
                'They share the Financial look below and use the same response templates as every other tool. Tools in this group: Supply Chain and Procurement.</p>')
    toc.append('<a href="#financial-tools" style="background:#0F1012;color:#C6E43F">Financial Tools</a>')
    rows.append('<h2 class="g-h2" id="supply-chain-procurement">Supply Chain and Procurement <span class="g-domtag g-domfin">Financial Tools</span></h2>'
                '<p class="g-lead">The fourth tool and the first Financial one: money lost on supplies, from the price paid to items never billed. Same five zones and the same behaviour '
                'as every tool (first element raised with its box open, on a phone each box under its element and every pick stacked, the three buttons). '
                'Example figures are made up for an example 250-bed hospital and marked Example only or Tojo’s guess.</p>')
    toc.append('<a href="#supply-chain-procurement" style="background:#0F1012;color:#EEEEE9">Supply Chain and Procurement</a>')
    chips = ''.join('<div class="bml-chip"><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 5px %s"></i><b>%s</b><span>%s</span></div>' % (
        L3.THEMES[k]['ground'], L3.THEMES[k]['ink'], L3.THEMES[k]['hi'], e(v[2]), e(v[3])) for k, v in L3.PAGES.items())
    rows.append('<section class="g-row" id="scp-look"><div class="g-meta"><div class="g-id">Supply Chain and Procurement · the look <span>palette</span></div>%s%s%s'
                '<p><b>One palette per place: ground, ink and a highlight.</b> Home keeps report white, black and lime; Diagnosis steel and signal orange; Solutions lilac and violet; '
                'Automations mint and coral; Processes sand and sky blue. The rail carries each place’s ground.</p></div><div class="g-views"><div><div class="bml-chips">%s</div></div></div></section>' % (
                    OK, FIN, LOOK, chips))
    toc.append('<a href="#scp-look">scp look</a>')
    rows.append('<h3 class="g-h3" id="scp-landing">Approved landing pages</h3>')
    for k, v in L3.PAGES.items():
        label, name = v[2], v[3].replace(' (approved)', '')
        full = _canvas(k, 'filled')
        meta = ('<p><b>%s landing page, %s.</b> %s</p><p class="g-small">Drawn by <code>Supply Chain Procurement/%s</code> with the V skin (<code>skins.py</code>), '
                'on the Bed Management page parts loaded as a copy (<code>sc_common.py</code>). Five zones in the fixed order: masthead with Refresh now, where this stands, '
                'the drawing, what Tojo still has to do, the three buttons.</p>'
                '<details class="g-first"><summary>See its first-visit state</summary><div style="width:864px;margin-top:8px">%s</div></details>') % (
            e(label), e(name), e(WHAT[k]), FILES[k].replace('.', '.py · '), _canvas(k, 'empty'))
        rows.append(('<section class="g-row" id="scp-landing-%s"><div class="g-meta"><div class="g-id">Supply Chain and Procurement · %s <span>%s</span></div>%s%s%s</div>'
                     '<div class="g-views"><div><div class="g-cap">Desktop canvas · 864px</div><div style="width:864px">%s</div></div>'
                     '<div><div class="g-cap">Mobile canvas · 362px</div><div style="width:362px">%s</div></div></div></section>') % (
            k, e(label), e(name), OK, SCOPE, meta, full, full))
        toc.append('<a href="#scp-landing-%s">scp-%s</a>' % (k, k))
    B = C.B
    sk = L3.SK
    page_css = C._accent(B.BASE_CSS + B.SEL_CSS) + sk['css'] + L2.V_SHARED_CSS + L2.F_CSS + L3.PLACE_CSS + ''.join(
        v[1][1] for v in L3.PAGES.values() if v[1])
    dom_css = ('.g-dom{border-top:6px solid #0F1012;padding-top:14px}'
               '.g-domtag{display:inline-block;vertical-align:middle;margin-left:12px;font:600 12px Poppins,sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:3px 10px;background:#10241a;color:#F3F1EA}'
               '.g-domtag.g-domfin{background:#0F1012;color:#C6E43F}')
    return ''.join(rows), ''.join(toc), dom_css + scope_css(page_css, '.scx')

GUIDE_ROW = '<tr><td>Supply Chain and Procurement · landing pages</td><td><code>Supply Chain Procurement/landing3.py</code> (data)</td><td><code>Supply Chain Procurement/landing2.py</code>, <code>landing3.py</code>, <code>scp_library.py</code></td></tr>'
DOM_LI = ('<li><b>Two groups of tools.</b> <b>Operations Tools</b>: Discharge Process, Bed Management, OPD Diagnostic Leak. <b>Financial Tools</b>: Supply Chain and Procurement. '
          'Each group has its own look (shapes, paper, frame); the Virevo type is the same everywhere. <b>Every tool in every group uses the response templates</b> (the universal patterns), '
          'redrawn in its own look.</li>')
RESP = ('<h2 class="g-h2 g-dom" id="response-templates">Response templates · every tool</h2><p class="g-lead">The universal patterns below are open to every tool in both groups, '
        'Operations Tools and Financial Tools. Each tool redraws them in its own look and colours through its own generator.</p>')
OPS = ('<h2 class="g-h2 g-dom" id="operations-tools">Operations Tools</h2><p class="g-lead">Tools about how the hospital runs: Discharge Process, Bed Management and OPD Diagnostic Leak. '
       'They share the Operations look: rounded outlines, warm paper and drawn pictures. First come the Discharge Process landing pages, the landing elements and the shared parts '
       '(the elements and shared parts are open to every tool), then each Operations tool in turn.</p>')

def inject(lib, scope_css):
    rows, toc, css = section(scope_css)
    def put(s, a, b, new, anchor):
        if a in s:
            return re.sub(re.escape(a) + '.*?' + re.escape(b), lambda m: a + new + b, s, count=1, flags=re.S)
        i = s.find(anchor)
        if i < 0: raise SystemExit('anchor not found: ' + anchor[:60])
        return s[:i] + a + new + b + s[i:]
    # the two domain headings and the response-template heading
    lib = put(lib, RESP_A, RESP_B, RESP, '<section class="g-row" id="heading">')
    lib = put(lib, OPS_A, OPS_B, OPS, '<h2 class="g-h2" id="landing-pages">')
    for hid, name in (('discharge-process', 'Discharge Process'), ('bed-management', 'Bed Management'), ('opd-diagnostic-leak', 'OPD Diagnostic Leak')):
        old = '<h2 class="g-h2" id="%s">%s</h2>' % (hid, name)
        lib = lib.replace(old, '<h2 class="g-h2" id="%s">%s %s</h2>' % (hid, name, OPS_TAG), 1)
    # this tool's section, after OPD, before the library's closing script
    lib = put(lib, MARK_A, MARK_B, rows, '<textarea id="tojo-input" hidden')
    if CSS_A in lib:
        lib = re.sub(re.escape(CSS_A) + '.*?' + re.escape(CSS_B), lambda m: CSS_A + css + CSS_B, lib, count=1, flags=re.S)
    else:
        j = lib.find('</style>', lib.find('/*/odl-css*/'))
        lib = lib[:j] + CSS_A + css + CSS_B + lib[j:]
    # contents: the groups and this tool
    if OPSTOC_A not in lib:
        i = lib.find('<a href="#landing-pages"', lib.find('<div class="g-toc2">'))
        lib = lib[:i] + OPSTOC_A + '<a href="#response-templates" style="background:#C6E43F;color:#0F1012">Response templates</a><a href="#operations-tools" style="background:#10241a;color:#d4a94f">Operations Tools</a>' + OPSTOC_B + lib[i:]
    toc_end = lib.find('</div>', lib.find('<div class="g-toc2">'))
    if TOC_A not in lib:
        lib = lib[:toc_end] + TOC_A + toc + TOC_B + lib[toc_end:]
    else:
        lib = re.sub(re.escape(TOC_A) + '.*?' + re.escape(TOC_B), lambda m: TOC_A + toc + TOC_B, lib, count=1, flags=re.S)
    # the guide
    if GUIDE_ROW not in lib:
        lib = lib.replace('</table><p class="g-small">In this build:', GUIDE_ROW + '</table><p class="g-small">In this build:', 1)
    if DOMLI_A not in lib:
        anchor = '<li><b>Approved</b>, <b>variation</b>'
        lib = lib.replace(anchor, DOMLI_A + DOM_LI + DOMLI_B + anchor, 1)
    lib = lib.replace('and the five OPD Diagnostic Leak landing pages. Everything is drawn',
                      'the five OPD Diagnostic Leak landing pages (Operations Tools), and the five Supply Chain and Procurement landing pages (Financial Tools). Everything is drawn', 1)
    lib = lib.replace('the Bed Management templates and the OPD Diagnostic Leak landing pages.',
                      'the Bed Management templates and the OPD Diagnostic Leak landing pages (Operations Tools), and the Supply Chain and Procurement landing pages (Financial Tools).', 1)
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
