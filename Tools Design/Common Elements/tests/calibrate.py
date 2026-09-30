"""
Calibrate block height costs in blocks/registry.json against real rendering.
Renders every example turn and every gallery sample in headless Chromium at the desktop (864px)
and mobile (362px) canvas widths, measures each block, and sets each block's base cost so the
estimate never undershoots what was measured (per-item costs are kept; +6% margin).
Usage:  python3 tests/calibrate.py      (re-run after changing CSS or adding blocks)
"""
import json, os, sys, glob, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'diagnosis-html-generator'))
import diagnosis_html
from playwright.sync_api import sync_playwright

reg = diagnosis_html.load_registry(); by = {b['id']: b for b in reg['blocks']}
specs = [json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(ROOT, 'examples', '*.json')))]
samples = json.load(open(os.path.join(ROOT, 'blocks', 'samples.json'), encoding='utf-8'))
specs += [{'canvas': {'blocks': [dict(v, type=k)]}} for k, v in samples.items()]
obs = {}
tmp = tempfile.mkdtemp()
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page()
    for i, spec in enumerate(specs):
        path = os.path.join(tmp, '%d.html' % i)
        open(path, 'w', encoding='utf-8').write(diagnosis_html.page('cal', diagnosis_html.render_canvas(spec)))
        for w, key in ((864, 'wide'), (362, 'narrow')):
            pg.set_viewport_size({'width': w, 'height': 900}); pg.goto('file://' + path); pg.wait_for_timeout(120)
            hs = pg.evaluate("Array.from(document.querySelectorAll('.tj-stack > *')).map(s => s.getBoundingClientRect().height)")
            for b, h in zip(spec['canvas']['blocks'], hs):
                obs.setdefault((b['type'], key), []).append((b, h))
    br.close()
for (t, key), items in sorted(obs.items()):
    c = by[t].setdefault('cost', {})
    per = c.get('per_item_' + key, 0)
    def n_items(b):
        lists = [v for v in b.values() if isinstance(v, list)]
        return len(lists[0]) if lists else 0
    pts = [(n_items(b), h - c.get('detail_' + key, 0)) for b, h in items]
    ns = {n for n, _ in pts}
    if len(ns) >= 2:                       # fit base + per-item by least squares
        mn = sum(n for n, _ in pts) / len(pts); mh = sum(h for _, h in pts) / len(pts)
        per = max(0, sum((n - mn) * (h - mh) for n, h in pts) / sum((n - mn) ** 2 for n, _ in pts))
        c['per_item_' + key] = int(round(per))
    base = sum(h - per * n for n, h in pts) / len(pts) * 1.03   # mean fit, +3%
    old = c.get(key); c[key] = int(round(base))
    print('%-17s %-6s base %5s → %5d   (%d observations, max %dpx)' % (t, key, old, c[key], len(items), max(h for _, h in items)))
reg['calibrated'] = 'tests/calibrate.py against %d renders' % len(specs)
json.dump(reg, open(diagnosis_html.REG_PATH, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
