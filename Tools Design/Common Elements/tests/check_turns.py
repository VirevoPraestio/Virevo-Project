"""
Browser check for rendered turns (needs: pip install playwright && playwright install chromium).

For every spec given: validate → render canvas/desktop/mobile → open in headless Chromium and check
  · no JavaScript errors · no horizontal overflow at desktop (1440) or phone (390) width
  · real canvas height vs the one-screen budget (desktop 780px, mobile 1500px) and vs the estimate
  · chat side: every point toggles "@PointN" into the input and lights its canvas item(s);
    every prompt fills the input; point + prompt combine as "@PointN <prompt>"
  · canvas side: every expander opens and closes, every stop can be picked, calculators compute
Usage:  python3 tests/check_turns.py examples/*.json
"""
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'diagnosis-html-generator'))
import diagnosis_html
from playwright.sync_api import sync_playwright

def check(pg, spec, tmp, name):
    probs, notes = [], []
    reg = diagnosis_html.load_registry()
    for x in diagnosis_html.plain_check(spec, reg): probs.append('plain English: ' + x)
    errs, warns = diagnosis_html.validate(spec, reg)
    if errs: return ['validation: ' + '; '.join(errs)], notes
    est = spec['_estimate']
    paths = {}
    for view in ('canvas', 'desktop', 'mobile'):
        p = os.path.join(tmp, '%s.%s.html' % (name, view))
        open(p, 'w', encoding='utf-8').write(diagnosis_html.render_page(spec, view)); paths[view] = p
    jserr = []
    pg.on('pageerror', lambda x: jserr.append(str(x)))
    # real canvas heights at the two canvas widths
    for w, key, budget in ((864, 'wide_px', reg['budget']['wide_px']), (362, 'narrow_px', reg['budget']['narrow_px'])):
        pg.set_viewport_size({'width': w, 'height': 900}); pg.goto('file://' + paths['canvas']); pg.wait_for_timeout(150)
        h = pg.evaluate("document.querySelector('.tj').getBoundingClientRect().height")
        tag = 'desktop' if w == 864 else 'mobile'
        notes.append('%s canvas %dpx (estimate %d, budget %d)' % (tag, h, est[key], budget))
        if h > budget: probs.append('%s canvas %dpx is over the %dpx budget' % (tag, h, budget))
        if pg.evaluate('document.documentElement.scrollWidth') > w: probs.append('%s canvas scrolls sideways' % tag)
    # desktop preview: chat + canvas interaction
    for view, w in (('desktop', 1440), ('mobile', 390)):
        pg.set_viewport_size({'width': w, 'height': 900}); pg.goto('file://' + paths[view]); pg.wait_for_timeout(200)
        if pg.evaluate('document.documentElement.scrollWidth') > w: probs.append('%s preview scrolls sideways' % view)
        inp = pg.locator('#tojo-input')
        for p in spec['chat'].get('points', []):
            b = pg.locator('.sh-pt[data-n="%d"]' % p['n']); b.click()
            v = inp.input_value(); lit = pg.locator('.tj-lit').count()
            if '@Point%d' % p['n'] not in v: probs.append('%s: point %d did not reach the input (%r)' % (view, p['n'], v))
            if p.get('canvas') and lit == 0: probs.append('%s: point %d lit nothing on the canvas' % (view, p['n']))
            b.click()
            if pg.locator('.tj-lit').count(): probs.append('%s: point %d stayed lit after unselecting' % (view, p['n']))
        if spec['chat'].get('points'):
            pg.locator('.sh-pt').first.click(); pg.locator('.sh-pr').first.click()
            want = '@Point1 ' + spec['chat']['prompts'][0]
            if inp.input_value() != want: probs.append('%s: point+prompt gave %r, wanted %r' % (view, inp.input_value(), want))
        for i, t in enumerate(spec['chat']['prompts']):
            pg.locator('.sh-pr').nth(i).click()
        # canvas interactions (visible layout only)
        root = '.tj-desk, .tj-stack > section:not(:has(.tj-desk))' if view == 'desktop' else '.tj-mob, .tj-stack > section:not(:has(.tj-mob))'
        toggles = [t for t in pg.locator('.tj details.tj-more > summary').all() if t.is_visible()]
        for k, t in enumerate(toggles):
            t.click(); body = t.locator('xpath=..').locator('.tj-more-body')
            n = body.locator('li').count()
            if body.is_hidden(): probs.append('%s: expander %d did not open' % (view, k))
            elif n < 2 and len(body.inner_text().split()) < 12: probs.append('%s: expander %d (“%s”) opens to almost nothing (F8)' % (view, k, t.inner_text().strip()))
            t.click()
            if not body.is_hidden(): probs.append('%s: expander %d did not close' % (view, k))
        picks = [x for x in pg.locator('.tj [data-tj-pick]').all() if x.is_visible()]
        for x in picks[:4]:
            x.click(); key = x.get_attribute('data-tj-pick')
            vis = [q for q in pg.locator('[data-tj-panel="%s"]' % key).all() if q.is_visible()]
            if not vis: probs.append('%s: stop %s opened no panel' % (view, key))
        calcs = pg.locator('.tj [data-step]').all()
        vals = [c.inner_text() for c in calcs if c.is_visible()]
        if vals: notes.append('%s calculator: %s' % (view, ' → '.join(vals)))
        notes.append('%s: %d points, %d prompts, %d expanders, %d stops checked' % (view, len(spec['chat'].get('points', [])), len(spec['chat']['prompts']), len(toggles), min(4, len(picks))))
    if jserr: probs.append('JS errors: ' + '; '.join(jserr))
    return probs, notes

def main(files):
    tmp = tempfile.mkdtemp(); bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch()
        for f in files:
            spec = json.load(open(f, encoding='utf-8'))
            pg = br.new_page()
            probs, notes = check(pg, spec, tmp, os.path.basename(f)[:-5]); pg.close()
            print(('FAIL ' if probs else 'ok   ') + os.path.basename(f))
            for n in notes: print('       ·', n)
            for x in probs: print('       ✗', x)
            bad += bool(probs)
        br.close()
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main(sys.argv[1:])
