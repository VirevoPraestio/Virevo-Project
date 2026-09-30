"""QA for the Bed Management home samples: canvas heights, sideways scroll, the word 'tab', screenshots."""
import glob, os, re, json
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'landing', 'home')
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sorted(glob.glob(os.path.join(OUT, 'home-*.html'))):
        n = os.path.basename(f)[5:-5]; mob = '.mobile.' in n
        pg = b.new_page(viewport={'width': 390 if mob else 1440, 'height': 900})
        pg.goto('file://' + f); pg.wait_for_timeout(300)
        r = pg.evaluate('''()=>{const c=document.querySelector('.lp-host');const t=document.body.innerText;
          return {canvas:Math.round(c.getBoundingClientRect().height),page:document.documentElement.scrollHeight,
          side:document.documentElement.scrollWidth>window.innerWidth,tab:/\\btabs?\\b/i.test(t)}}''')
        res[n] = r
        pg.screenshot(path=os.path.join(OUT, 'shots', n + '.png'), full_page=True)
        pg.close()
    b.close()
for k, v in res.items():
    flag = []
    if not '.mobile.' in k and v['canvas'] > 824: flag.append('OVER 824')
    if '.mobile.' in k and v['canvas'] > 1500: flag.append('OVER 1500')
    if v['side']: flag.append('SIDEWAYS')
    if v['tab']: flag.append('WORD TAB')
    print(k.ljust(24), v['canvas'], v['page'], ' '.join(flag))
