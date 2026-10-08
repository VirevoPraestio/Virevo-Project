"""
odl_library: the OPD Diagnostic Leak section of the one Tojo block library (approved 8 Oct 2026).

Blocks only (rules/08 §7): each landing page is drawn as its canvas, at the desktop canvas width (864px)
and the phone width (362px), with its first-visit state under a fold. No app interface, no frames.
Each page's picking groups get their own prefix, so picking in one template never opens a sheet in another.

Used two ways:
  build_block_library.py   calls section(scope_css) when the whole library is rebuilt;
  python3 odl_library.py LIB.html OUT.html   adds (or replaces) only this section in an existing library file,
                                             leaving every other template untouched.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import odl_common as C
import landing as L

e = C.e
MARK_A, MARK_B = '<!--odl-section-->', '<!--/odl-section-->'
CSS_A, CSS_B = '/*odl-css*/', '/*/odl-css*/'
TOC_A, TOC_B = '<!--odl-toc-->', '<!--/odl-toc-->'
SCOPE = '<span class="g-scope g-scope-one" title="Only OPD Diagnostic Leak uses this template">OPD Diagnostic Leak only</span>'
OK = '<span class="g-status" style="background:#2f7350">approved</span>'
FILES = {'home': 'home_canvas', 'diagnosis': 'dg_canvas', 'solutions': 'so_canvas', 'automations': 'au_canvas', 'processes': 'pr_canvas'}
WHAT = {
 'home': 'The tool’s own landing page, with a different layout from the other tools: a split top (the claim on the left, the leak meter on the right), then one pipe from the clinic to the test rooms with a valve for each place. A valve turns shut as its place is done; drops fall where tests still leave. Tap a valve to read its steps.',
 'diagnosis': 'The sieve: 100 tests written, how many are left at each step, and why each group drops out. Below it, the four possible main causes weighed, one dot per piece of evidence. Tap a row.',
 'solutions': 'The prescription pad: one handwritten line per fix, its four stops as boxes to tick, and its by-hand and automatic versions side by side (every fix must work by hand too). Tap a line.',
 'automations': 'One patient’s visit: the stations from arrival to going home, and each helper placed over the stations where it acts. Tap a helper; its box says what it does, when it runs, what it needs, and how the step works without it.',
 'processes': 'The busy-hours board: bills per hour against what the desk can make, with the shortfall striped; each change pinned under the hours it acts; the numbers we will watch and the team and roles beside it. Tap a change.',
}

def _own_groups(html, k):
    tok = 'odl' + k[:2]
    html = re.sub(r'data-grp="([a-z]+)"', lambda m: 'data-grp="%s%s"' % (tok, m.group(1)), html)
    return re.sub(r'data-box="([a-z]+):', lambda m: 'data-box="%s%s:' % (tok, m.group(1)), html)

def _canvas(k, state):
    place, fn, css, data, cls, label, name = L.PAGES[k]
    t = C.THEMES[k]
    inner = _own_groups(fn(state), k)
    return '<div class="odx"><div class="lp-host"><div class="lp bm %s" style="%s">%s</div></div></div>' % (cls, t['vars'], inner)

def section(scope_css):
    rows, toc = [], []
    rows.append('<h2 class="g-h2" id="opd-diagnostic-leak">OPD Diagnostic Leak</h2><p class="g-lead">The third tool: tests written in the outpatient clinic that are done somewhere else. '
                'Same five zones and the same behaviour as every tool (first element raised with its box open, on a phone each box under its element and every pick stacked, the three buttons), '
                'but its own home layout and colours no other tool uses. Each place’s highlight takes the place of the shared gold. Example figures come from the case study in '
                '<code>opd-diagnostic-leakage.md</code> §0; anything else is marked Example only or Tojo’s guess.</p>')
    toc.append('<a href="#opd-diagnostic-leak" style="background:#2B1E05;color:#F1E3B9">OPD Diagnostic Leak</a>')
    chips = ''.join('<div class="bml-chip"><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 5px %s"></i><b>%s</b><span>%s · %s</span></div>' % (
        C.THEMES[k]['ground'], C.THEMES[k]['ink'], C.THEMES[k]['hi'], e(v[5]), e(v[6]), e(L.PALETTE[k])) for k, v in L.PAGES.items())
    rows.append('<section class="g-row" id="odl-look"><div class="g-meta"><div class="g-id">OPD Diagnostic Leak · the look <span>palette</span></div>%s%s'
                '<p><b>One palette per place: ground, ink and a highlight.</b> The highlight marks now, next and picked (the raised edge, the first button, the emblem), in place of the gold the other tools share. '
                'None of these colours is used by Discharge Process or Bed Management.</p></div><div class="g-views"><div><div class="bml-chips">%s</div></div></div></section>' % (OK, SCOPE, chips))
    rows.append('<h3 class="g-h3" id="odl-landing">Approved landing pages</h3>')
    toc.append('<a href="#odl-landing">odl landing pages</a>')
    for k, v in L.PAGES.items():
        label, name = v[5], v[6]
        full = _canvas(k, 'filled')
        meta = ('<p><b>%s landing page, %s.</b> %s</p><p class="g-small">Drawn by <code>OPD Diagnostic Leak/landing.py</code> (<code>%s</code>), on the Bed Management page parts loaded as a copy '
                '(<code>odl_common.py</code>). Five zones in the fixed order: masthead with Refresh now, where this stands, the drawing, what Tojo still has to do, the three buttons.</p>'
                '<details class="g-first"><summary>See its first-visit state</summary><div style="width:864px;margin-top:8px">%s</div></details>') % (
            e(label), e(name), e(WHAT[k]), FILES[k], _canvas(k, 'empty'))
        rows.append(('<section class="g-row" id="odl-landing-%s"><div class="g-meta"><div class="g-id">OPD Diagnostic Leak · %s <span>%s</span></div>%s%s%s</div>'
                     '<div class="g-views"><div><div class="g-cap">Desktop canvas · 864px</div><div style="width:864px">%s</div></div>'
                     '<div><div class="g-cap">Mobile canvas · 362px</div><div style="width:362px">%s</div></div></div></section>') % (
            k, e(label), e(name), OK, SCOPE, meta, full, full))
        toc.append('<a href="#odl-landing-%s">odl-%s</a>' % (k, k))
    B = C.B
    css = C._accent(B.BASE_CSS + B.SEL_CSS + B.BED_CSS) + L.TOOL_CSS + ''.join(v[2] for v in L.PAGES.values())
    return ''.join(rows), ''.join(toc), scope_css(css, '.odx')

GUIDE_ROW = '<tr><td>OPD Diagnostic Leak · landing pages</td><td><code>OPD Diagnostic Leak/landing.py</code> (data)</td><td><code>OPD Diagnostic Leak/landing.py</code>, <code>odl_library.py</code></td></tr>'

def inject(lib, scope_css):
    """Add this section to an existing library page, or replace it if it is already there. Nothing else changes
    except the table of contents link, one row of the guide table and the two sentences that list what the library holds."""
    rows, toc, css = section(scope_css)
    def put(s, a, b, new, anchor, before=True):
        if a in s:
            return re.sub(re.escape(a) + '.*?' + re.escape(b), lambda m: a + new + b, s, count=1, flags=re.S)
        i = s.find(anchor)
        if i < 0: raise SystemExit('anchor not found: ' + anchor[:60])
        return s[:i] + a + new + b + s[i:] if before else s[:i + len(anchor)] + a + new + b + s[i + len(anchor):]
    lib = put(lib, MARK_A, MARK_B, rows, '<textarea id="tojo-input" hidden')
    if CSS_A in lib:
        lib = re.sub(re.escape(CSS_A) + '.*?' + re.escape(CSS_B), lambda m: CSS_A + css + CSS_B, lib, count=1, flags=re.S)
    else:
        j = lib.find('</style>', lib.find('.bmx '))          # the library's own stylesheet, the one holding the scoped tool rules
        lib = lib[:j] + CSS_A + css + CSS_B + lib[j:]
    toc_end = lib.find('</div>', lib.find('<div class="g-toc2">'))
    if TOC_A not in lib:
        lib = lib[:toc_end] + TOC_A + toc + TOC_B + lib[toc_end:]
    else:
        lib = re.sub(re.escape(TOC_A) + '.*?' + re.escape(TOC_B), lambda m: TOC_A + toc + TOC_B, lib, count=1, flags=re.S)
    if GUIDE_ROW not in lib:
        lib = lib.replace('</table><p class="g-small">In this build:', GUIDE_ROW + '</table><p class="g-small">In this build:', 1)
    lib = lib.replace('and the Bed Management Diagnosis, Solutions, Automations and Processes templates.',
                      'the Bed Management Diagnosis, Solutions, Automations and Processes templates, and the five OPD Diagnostic Leak landing pages.', 1)
    lib = lib.replace('the regenerated Discharge Process turn templates and the Bed Management templates.',
                      'the regenerated Discharge Process turn templates, the Bed Management templates and the OPD Diagnostic Leak landing pages.', 1)
    return lib

if __name__ == '__main__':
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'Common Elements', 'library'))
    from importlib import util
    spec = util.spec_from_file_location('bbl', os.path.join(os.path.dirname(HERE), 'Common Elements', 'library', 'build_block_library.py'))
    src, dst = sys.argv[1], sys.argv[2]
    # only the CSS scoping helper is needed from the builder; read it without running the builder
    code = open(spec.origin, encoding='utf-8').read()
    ns = {}
    exec(compile('import re\n' + code[code.find('def _split_sel'):code.find('def load(')], 'scope', 'exec'), ns)
    out = inject(open(src, encoding='utf-8').read(), ns['scope_css'])
    open(dst, 'w', encoding='utf-8').write(out)
    print('wrote', dst, len(out))
