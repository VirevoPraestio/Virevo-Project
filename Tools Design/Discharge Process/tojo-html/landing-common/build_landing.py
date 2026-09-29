"""
Build every landing-page sample: plain HTML previews (desktop + mobile, both states) into
out/landing/, and design-canvas artboards into out/landing/design-canvas/.

  python3 build_landing.py              # everything
  python3 build_landing.py diagnosis    # one tab
  APPROVED=1 python3 build_landing.py   # only the approved template per tab (landing-registry.json)
"""
import importlib.util, json, os, sys
import landing_common as lc

ROOT = lc.ROOT
TABS = {'diagnosis': 'diagnosis-html-generator', 'solutions': 'solutions-html-generator',
        'automations': 'automations-html-generator', 'processes': 'processes-html-generator'}
OUT = os.path.join(ROOT, 'out', 'landing')

def load(tab):
    path = os.path.join(ROOT, TABS[tab], 'landing.py')
    spec = importlib.util.spec_from_file_location('landing_' + tab, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def build(tab, heights=None, dc=False):
    mod = load(tab); os.makedirs(OUT, exist_ok=True); made = []
    reg = json.load(open(os.path.join(lc.HERE, 'landing-registry.json')))
    only = reg['tabs'][tab]['approved'] if os.environ.get('APPROVED') == '1' else None
    for key, name, blurb, fn in mod.SAMPLES:
        if only and key != only: continue
        for view in ('desktop', 'mobile'):
            for state in ('filled', 'empty'):
                canvas = fn(lc.Mode('html', state, mod.DATA))
                page = lc.plain_page(mod.TAB, mod.THEME, mod.CSS, canvas, mod.DATA[state]['chat'], view)
                p = os.path.join(OUT, '%s-%s.%s.%s.html' % (tab, key, view, state)); open(p, 'w', encoding='utf-8').write(page); made.append(p)
            if dc:
                h = (heights or {}).get('%s-%s.%s' % (tab, key, view), 900 if view == 'desktop' else 2400)
                cf = fn(lc.Mode('dc', 'filled', mod.DATA)); ce = fn(lc.Mode('dc', 'empty', mod.DATA))
                title = '%s landing %s — %s, %s' % (mod.TAB, key.upper(), name, view)
                d = os.path.join(OUT, 'design-canvas'); os.makedirs(d, exist_ok=True)
                fn_dc = '%s-%s-%s.dc.html' % (mod.TAB, key.upper(), view.capitalize())
                open(os.path.join(d, fn_dc), 'w', encoding='utf-8').write(lc.dc_page(mod.TAB, mod.THEME, mod.CSS, cf, ce, mod.DATA, view, h, title))
    return made

if __name__ == '__main__':
    tabs = sys.argv[1:] or list(TABS)
    hp = os.path.join(OUT, 'heights.json')
    heights = json.load(open(hp)) if os.path.exists(hp) else {}
    for t in tabs:
        print(t, len(build(t, heights, dc=os.environ.get('DC') == '1')), 'files')
