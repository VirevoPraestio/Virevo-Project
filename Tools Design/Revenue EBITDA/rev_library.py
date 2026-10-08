"""
rev_library: the Revenue & EBITDA section of the one Tojo block library, under Financial Tools
(approved 8 Oct 2026: home A, the cheque book, and the four place pages).

What it adds or changes, and nothing else (every other template stays byte for byte the same):
  * the Revenue & EBITDA section after Supply Chain and Procurement: its colours, then the five
    landing pages, each as its canvas at 864px and 362px with its first-visit state under a fold;
  * the Financial Tools lead, the guide's line about the two groups and the "In this build"
    sentences now name Revenue & EBITDA;
  * contents links and one guide row.

Blocks only (rules/08 §7). Each page's picking groups get their own prefix. CSS is scoped under .rvx.
Needs the Financial Tools section of scp_library.py to be in the library first.

Used two ways:
  build_block_library.py   calls inject(page, scope_css) after scp_library on a full rebuild;
  python3 rev_library.py LIB.html OUT.html   updates an existing library file in place.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rev_landing as H
import places as P
C, L2, L3 = H.C, H.L2, H.L3

e = C.e
MARK_A, MARK_B = '<!--rev-section-->', '<!--/rev-section-->'
CSS_A, CSS_B = '/*rev-css*/', '/*/rev-css*/'
TOC_A, TOC_B = '<!--rev-toc-->', '<!--/rev-toc-->'
SCOPE = '<span class="g-scope g-scope-one" title="Only Revenue &amp; EBITDA uses this template">Revenue &amp; EBITDA only</span>'
FIN = '<span class="g-scope g-scope-all" style="background:#0F1012;color:#C6E43F" title="The Financial look, shared by every Financial tool">Financial Tools look</span>'
OK = '<span class="g-status" style="background:#2f7350">approved</span>'
FILES = {'home': 'rev_landing.a_canvas', 'diagnosis': 'places.dg_canvas', 'solutions': 'places.so_canvas',
         'automations': 'places.au_canvas', 'processes': 'places.pr_canvas'}
WHAT = {
 'home': 'The month’s money as a profit and loss on ledger paper: money in, each cost, and what is left on a double-ruled line, against the goal. '
         'The work as a book of cheques, one per part, each made out for what that part brings back; its counterfoil ticks the steps done and a signature line waits for when it is agreed. '
         'On a phone the cheques stack and each opens under itself.',
 'diagnosis': '₹1,000 of bills followed to the bank, each step a statement line with the day, what was lost and the balance left; the tapped line opens beside the statement. '
              'Below it, the monthly gap split four ways on a ring, the leading cause in the highlight.',
 'solutions': 'One ruled entry per fix: its four stops, what it costs to start, what it brings back each month, and a twelve-month strip marking the month it pays for itself; '
              'a double-ruled total. Each entry opens to its by-hand and automatic versions side by side.',
 'automations': 'The money’s journey from the patient leaving to month end, seven stops, each helper hung at the stop where it acts. '
                'Under it, one card per helper with its four lamps and the note it would send; its box says what it reads, who gets the note and when it runs.',
 'processes': 'Daily, weekly, monthly and new-role lanes with the changes in them and a two-month trial; who owns each line of the profit and loss; '
              'the numbers we watch, now against plan, with which way is better.',
}
NAMES = {'home': 'banknote green, bottle green and marigold', 'diagnosis': 'peach, deep plum and electric blue',
         'solutions': 'pale olive, deep teal and tangerine', 'automations': 'ice blue, navy and hot pink',
         'processes': 'orchid pink, aubergine and sea green'}

def _own_groups(html, k):
    tok = 'rev' + k[:2]
    html = re.sub(r'data-grp="([a-z]+)"', lambda m: 'data-grp="%s%s"' % (tok, m.group(1)), html)
    return re.sub(r'data-box="([a-z]+):', lambda m: 'data-box="%s%s:' % (tok, m.group(1)), html)

def _canvas(k, state):
    place, spec, label, title = P.PAGES[k]
    if spec is None:
        fn, cls = H.a_canvas, 'rv rv-home rv-a'
    else:
        fn, cls = spec[0], 'rv rv-%s' % k
    t = P.THEMES[k]
    return '<div class="rvx"><div class="lp-host"><div class="lp bm skin-v %s" style="%s">%s</div></div></div>' % (cls, t['vars'], _own_groups(fn(state), k))

def section(scope_css):
    rows, toc = [], []
    rows.append('<h2 class="g-h2" id="revenue-ebitda">Revenue &amp; EBITDA <span class="g-domtag g-domfin">Financial Tools</span></h2>'
                '<p class="g-lead">The fifth tool and the second Financial one: the money the hospital earns each month and how much of it is left after every cost '
                '(EBITDA: what is left before loan interest, tax and the wearing out of buildings and machines). Same five zones and the same behaviour as every tool '
                '(first element raised with its box open, on a phone each box under its element and every pick stacked, the three buttons). '
                'Same Financial look as Supply Chain and Procurement; only the colours change. Example figures are made up for an example 250-bed hospital and marked Example only or Tojo’s guess.</p>')
    toc.append('<a href="#revenue-ebitda" style="background:#0C2E26;color:#F2B233">Revenue &amp; EBITDA</a>')
    chips = ''.join('<div class="bml-chip"><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 5px %s"></i><b>%s</b><span>%s</span></div>' % (
        P.THEMES[k]['ground'], P.THEMES[k]['ink'], P.THEMES[k]['hi'], e(v[2]), e(v[3])) for k, v in P.PAGES.items())
    words = '; '.join('%s %s' % (P.PAGES[k][2], NAMES[k]) for k in P.PAGES)
    rows.append('<section class="g-row" id="rev-look"><div class="g-meta"><div class="g-id">Revenue &amp; EBITDA · the look <span>palette</span></div>%s%s%s'
                '<p><b>One palette per place: ground, ink and a highlight,</b> none used by another tool. %s. The rail carries each place’s ground. '
                'Every text pair clears 4.5:1.</p></div><div class="g-views"><div><div class="bml-chips">%s</div></div></div></section>' % (
                    OK, FIN, '<p>The Financial look as set out under Supply Chain and Procurement: Virevo type unchanged, flat frame, report sheet, ledger paper and receipt.</p>', e(words), chips))
    toc.append('<a href="#rev-look">rev look</a>')
    rows.append('<h3 class="g-h3" id="rev-landing">Approved landing pages</h3>')
    for k, v in P.PAGES.items():
        label, name = v[2], v[3].replace(' (approved)', '')
        full = _canvas(k, 'filled')
        meta = ('<p><b>%s landing page, %s.</b> %s</p><p class="g-small">Drawn by <code>Revenue EBITDA/%s</code> with the V skin (<code>Supply Chain Procurement/skins.py</code>), '
                'on the Bed Management page parts loaded as a copy (<code>sc_common.py</code>). Five zones in the fixed order: masthead with Refresh now, where this stands, '
                'the drawing, what Tojo still has to do, the three buttons.</p>'
                '<details class="g-first"><summary>See its first-visit state</summary><div style="width:864px;margin-top:8px">%s</div></details>') % (
            e(label), e(name), e(WHAT[k]), FILES[k].replace('.', '.py · '), _canvas(k, 'empty'))
        rows.append(('<section class="g-row" id="rev-landing-%s"><div class="g-meta"><div class="g-id">Revenue &amp; EBITDA · %s <span>%s</span></div>%s%s%s</div>'
                     '<div class="g-views"><div><div class="g-cap">Desktop canvas · 864px</div><div style="width:864px">%s</div></div>'
                     '<div><div class="g-cap">Mobile canvas · 362px</div><div style="width:362px">%s</div></div></div></section>') % (
            k, e(label), e(name), OK, SCOPE, meta, full, full))
        toc.append('<a href="#rev-landing-%s">rev-%s</a>' % (k, k))
    B = C.B
    page_css = (C._accent(B.BASE_CSS + B.SEL_CSS) + H.SK['css'] + L2.V_SHARED_CSS + L3.PLACE_CSS + H.A_CSS
                + ''.join(v[1][1] for v in P.PAGES.values() if v[1]))
    return ''.join(rows), ''.join(toc), scope_css(page_css, '.rvx')

GUIDE_ROW = '<tr><td>Revenue &amp; EBITDA · landing pages</td><td><code>Revenue EBITDA/rev_landing.py</code>, <code>places.py</code> (data)</td><td><code>Revenue EBITDA/rev_landing.py</code>, <code>places.py</code>, <code>rev_library.py</code></td></tr>'
REPL = [
 ('Tools in this group: Supply Chain and Procurement.</p>', 'Tools in this group: Supply Chain and Procurement, Revenue &amp; EBITDA.</p>'),
 ('<b>Financial Tools</b>: Supply Chain and Procurement. ', '<b>Financial Tools</b>: Supply Chain and Procurement, Revenue &amp; EBITDA. '),
 ('and the five Supply Chain and Procurement landing pages (Financial Tools). Everything is drawn',
  'and the five landing pages each of Supply Chain and Procurement and Revenue &amp; EBITDA (Financial Tools). Everything is drawn'),
 ('and the Supply Chain and Procurement landing pages (Financial Tools).',
  'and the Supply Chain and Procurement and Revenue &amp; EBITDA landing pages (Financial Tools).'),
]

def inject(lib, scope_css):
    if '<!--/scp-section-->' not in lib:
        raise SystemExit('run scp_library first: the Financial Tools section is missing')
    rows, toc, css = section(scope_css)
    if MARK_A in lib:
        lib = re.sub(re.escape(MARK_A) + '.*?' + re.escape(MARK_B), lambda m: MARK_A + rows + MARK_B, lib, count=1, flags=re.S)
    else:
        i = lib.find('<!--/scp-section-->') + len('<!--/scp-section-->')
        lib = lib[:i] + MARK_A + rows + MARK_B + lib[i:]
    if CSS_A in lib:
        lib = re.sub(re.escape(CSS_A) + '.*?' + re.escape(CSS_B), lambda m: CSS_A + css + CSS_B, lib, count=1, flags=re.S)
    else:
        i = lib.find('/*/scp-css*/') + len('/*/scp-css*/')
        lib = lib[:i] + CSS_A + css + CSS_B + lib[i:]
    if TOC_A in lib:
        lib = re.sub(re.escape(TOC_A) + '.*?' + re.escape(TOC_B), lambda m: TOC_A + toc + TOC_B, lib, count=1, flags=re.S)
    else:
        i = lib.find('<!--/scp-toc-->') + len('<!--/scp-toc-->')
        lib = lib[:i] + TOC_A + toc + TOC_B + lib[i:]
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
