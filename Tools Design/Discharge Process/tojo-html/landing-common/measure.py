"""Render the plain previews in Chromium, record page heights and screenshots (QA only)."""
import json, os, sys, glob
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out', 'landing')
files = sorted(glob.glob(os.path.join(OUT, (sys.argv[1] if len(sys.argv) > 1 else '') + '*.html')))
res = json.load(open(os.path.join(OUT, 'heights.json'))) if os.path.exists(os.path.join(OUT, 'heights.json')) else {}
shots = os.path.join(OUT, 'shots'); os.makedirs(shots, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for f in files:
        base = os.path.basename(f)[:-5]; tabkey, view, state = base.split('.')
        w = 1440 if view == 'desktop' else 390
        pg = b.new_page(viewport={'width': w, 'height': 900}); pg.goto('file://' + f); pg.wait_for_timeout(250)
        h = pg.evaluate('document.documentElement.scrollHeight')
        ch = pg.evaluate("(() => { const m = document.querySelector('.lp'); return m ? Math.round(m.getBoundingClientRect().height) : 0 })()")
        ow = pg.evaluate('document.documentElement.scrollWidth') > w
        pg.screenshot(path=os.path.join(shots, base + '.png'), full_page=True)
        k = '%s.%s' % (tabkey, view); res[k] = max(res.get(k, 0) if state == 'empty' else 0, h) if False else max(h, res.get(k + '.' + ('empty' if state == 'filled' else 'filled'), 0))
        res[k + '.' + state] = h
        print('%-40s page %5d  canvas %4d%s' % (base, h, ch, '  SIDEWAYS SCROLL' if ow else ''))
        pg.close()
    b.close()
for k in list(res):
    if k.count('.') == 2:
        base = k.rsplit('.', 1)[0]; res[base] = max(res.get(base + '.filled', 0), res.get(base + '.empty', 0))
json.dump(res, open(os.path.join(OUT, 'heights.json'), 'w'), indent=1)
