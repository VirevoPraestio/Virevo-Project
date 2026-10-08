"""Browser QA for the Processes turns listed in examples/solutions/turns.json.

For each turn it draws the desktop page (1440 x 900) and the phone page (390 wide) in Chromium and reports
the canvas height against the budget, sideways scroll and script errors. It then opens the tab book and
checks that it lists every turn and loads both live views. No screenshots unless SHOTS=1; those are for
checking only and go to a scratch folder, never to the deliverables.

  python3 check.py            # every turn
  python3 check.py so-01      # turns whose id starts with so-01
"""
import json, os, sys, tempfile
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import processes_html as so

EXE = os.environ.get('CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
EX = os.path.join(ROOT, 'examples', 'processes'); OUT = os.path.join(ROOT, 'out', 'processes')
SHOTS = os.environ.get('SHOTS_DIR') or (tempfile.mkdtemp() if os.environ.get('SHOTS') == '1' else '')
reg = so.load_registry(); pick = sys.argv[1] if len(sys.argv) > 1 else ''
bad = 0; tmp = tempfile.mkdtemp()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE)
    for t in json.load(open(os.path.join(EX, 'turns.json'), encoding='utf-8'))['turns']:
        spec = json.load(open(os.path.join(EX, t['file']), encoding='utf-8'))
        if not spec['turn']['id'].startswith(pick): continue
        for view, w, budget in (('desktop', 1440, 824), ('mobile', 390, 1500)):
            f = os.path.join(tmp, '%s.%s.html' % (spec['turn']['id'], view)); open(f, 'w', encoding='utf-8').write(so.render_page(spec, view, reg))
            pg = b.new_page(viewport={'width': w, 'height': 900}); errs = []
            pg.on('pageerror', lambda ex: errs.append(str(ex)))
            pg.goto('file://' + f); pg.wait_for_timeout(2000)
            ch = pg.evaluate("(() => { const m = document.querySelector('.px, .lp'); return m ? Math.round(m.getBoundingClientRect().height) : 0 })()")
            side = pg.evaluate('document.documentElement.scrollWidth') > w
            flag = ('  OVER BUDGET' if ch > budget else '') + ('  SIDEWAYS SCROLL' if side else '') + ('  SCRIPT ERROR: ' + errs[0] if errs else '')
            bad += bool(flag)
            print('%-7s %-8s canvas %4d / %d%s' % (spec['turn']['id'], view, ch, budget, flag))
            if SHOTS: pg.screenshot(path=os.path.join(SHOTS, '%s.%s.png' % (spec['turn']['id'], view)), full_page=True)
            pg.close()
    book = os.path.join(OUT, 'processes-tab.html')
    if os.path.exists(book):
        pg = b.new_page(viewport={'width': 1440, 'height': 1000}); errs = []
        pg.on('pageerror', lambda ex: errs.append(str(ex)))
        pg.goto('file://' + book); pg.wait_for_timeout(1200)
        n = pg.evaluate("document.querySelectorAll('.rv-list button').length")
        frames = pg.evaluate("document.querySelectorAll('.rv-views iframe').length")
        print('tab book: %d turns listed, %d live views%s' % (n, frames, ('  SCRIPT ERROR: ' + errs[0]) if errs else ''))
        if SHOTS: pg.screenshot(path=os.path.join(SHOTS, 'book.png'), full_page=True)
        bad += bool(errs) or frames != 2
        pg.close()
    if SHOTS: print('screenshots for checking only:', SHOTS)
    b.close()
sys.exit(1 if bad else 0)
