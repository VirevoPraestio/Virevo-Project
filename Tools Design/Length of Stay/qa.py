"""Browser check for the Revenue & EBITDA pages (08 §5, F6, F7).
Fails a page on: sideways scroll, the word "tab", text running outside its box, a script error,
phone picks side by side, or picking that does not raise the tapped item and open its box.
Run: python3 qa.py   (needs Playwright)"""
import glob, os
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out', 'landing')

CHECK = r'''()=>{
 const lp=document.querySelector('.lp'); const res={};
 res.side=document.documentElement.scrollWidth>window.innerWidth+1;
 const t=lp.innerText+' '+(document.querySelector('.sh-chat,.sh-mpanel')||{innerText:''}).innerText;
 res.tab=/\btabs?\b/i.test(t);
 res.h=Math.round(document.querySelector('.lp-host').getBoundingClientRect().height);
 const over=[];
 lp.querySelectorAll('p,li,b,em,span,h1,h2,h3,h4,button').forEach(el=>{
   if(!el.offsetParent) return;
   const cs=getComputedStyle(el); if(cs.overflow==='hidden'||cs.textOverflow==='ellipsis') return;
   if(el.scrollWidth>el.clientWidth+2 && el.clientWidth>0 && cs.display!=='inline') over.push((el.className||el.tagName)+': '+el.innerText.slice(0,30));
 });
 res.over=over.slice(0,5);
 // phone: picks of one group must be stacked
 const side=[];
 const groups={}; lp.querySelectorAll('.js-sel').forEach(b=>{if(b.offsetParent)(groups[b.dataset.grp]=groups[b.dataset.grp]||[]).push(b.getBoundingClientRect());});
 Object.entries(groups).forEach(([g,rs])=>{for(let i=1;i<rs.length;i++){if(Math.abs(rs[i].top-rs[i-1].top)<4)side.push(g);}});
 res.sideBySide=[...new Set(side)];
 res.groups=Object.keys(groups);
 return res;}'''

def main():
    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for f in sorted(glob.glob(os.path.join(OUT, os.environ.get('QA_GLOB','los-*.html')))):
            n = os.path.basename(f)[4:-5]; mob = '.mobile.' in n
            pg = b.new_page(viewport={'width': 390 if mob else 1440, 'height': 900})
            errs = []; pg.on('pageerror', lambda x: errs.append(str(x)))
            pg.goto('file://' + f); pg.wait_for_timeout(200)
            r = pg.evaluate(CHECK)
            flags = []
            if r['side']: flags.append('SIDEWAYS')
            if r['tab']: flags.append('WORD TAB')
            if r['over']: flags.append('OVERFLOW %s' % r['over'])
            if errs: flags.append('JS %s' % errs[0])
            if mob and r['sideBySide']: flags.append('PICKS SIDE BY SIDE %s' % r['sideBySide'])
            # picking: tap the last item of each group; it must be raised with its own box shown
            for g in r['groups']:
                ok = pg.evaluate('''(g)=>{const bs=[...document.querySelectorAll('.js-sel[data-grp="'+g+'"]')].filter(b=>b.offsetParent);
                  const last=bs[bs.length-1]; last.click(); const k=last.dataset.key;
                  const up=bs.filter(b=>b.classList.contains('is-up')); const box=[...document.querySelectorAll('[data-box="'+g+':'+k+'"]')].filter(x=>x.offsetParent);
                  return up.length===1 && up[0]===last && box.length===1;}''', g)
                if not ok: flags.append('PICK FAILS ' + g)
            if not mob and r['h'] > 1900: flags.append('OVER 2 SCREENS')
            bad += bool(flags)
            print('%-28s %5d  %s' % (n, r['h'], ' '.join(flags) or 'ok'))
            pg.close()
        b.close()
    print('pages with problems:', bad)

if __name__ == '__main__':
    main()
