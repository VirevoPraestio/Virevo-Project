import glob, os, sys
from playwright.sync_api import sync_playwright
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'landing', 'approved'); SH=OUT+'/shots'; os.makedirs(SH, exist_ok=True)
only = sys.argv[1] if len(sys.argv) > 1 else ''
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in sorted(glob.glob(OUT+'/v3-*.html')):
        n=os.path.basename(f)[3:-5]
        if only not in n: continue
        mob='.mobile.' in n; W,Hh=(390,844) if mob else (1440,900)
        pg=b.new_page(viewport={'width':W,'height':Hh}); errs=[]; pg.on('pageerror',lambda x: errs.append(str(x)))
        pg.goto('file://'+f.replace(' ','%20')); pg.wait_for_timeout(250)
        r=pg.evaluate('''()=>{const t=document.querySelector('.lp').innerText+' '+document.querySelector('.sh-chat,.sh-mpanel').innerText;
          const ch=document.querySelector(mob?'.sh-mpanel':'.sh-chat');
          return {side:document.documentElement.scrollWidth>window.innerWidth||document.querySelector(mob?'.sh-mc':'.sh-mid').scrollWidth>document.querySelector(mob?'.sh-mc':'.sh-mid').clientWidth+1,
           tab:/\\btabs?\\b/i.test(t),chat:Math.round(ch.getBoundingClientRect().height),doc:document.documentElement.scrollHeight,
           canvas:Math.round(document.querySelector('.lp-host').getBoundingClientRect().height),
           up:document.querySelectorAll('.js-sel.is-up').length,open:[...document.querySelectorAll('.bx')].filter(x=>!x.hidden&&x.offsetParent).length}}'''.replace('mob?', 'true?' if mob else 'false?'))
        pg.screenshot(path=SH+'/'+n+'.screen.png')
        # tap the second element, check it rises and its own box shows right after it (phone) / in the shared box (desktop)
        sw=''
        els=pg.locator('.js-sel')
        if els.count()>1:
            keys=pg.evaluate("()=>[...new Set([...document.querySelectorAll('.js-sel')].map(x=>x.dataset.grp+':'+x.dataset.key))]")
            g,k=keys[1].split(':')
            pg.locator('.js-sel[data-grp="%s"][data-key="%s"]'%(g,k)).first.click(); pg.wait_for_timeout(300)
            sw=pg.evaluate('''([g,k])=>{const up=[...document.querySelectorAll('.js-sel.is-up')].map(x=>x.dataset.key);
              const vis=[...document.querySelectorAll('.bx')].filter(x=>!x.hidden&&x.offsetParent).map(x=>x.dataset.box);
              let near='';const el=document.querySelector('.js-sel[data-grp="'+g+'"][data-key="'+k+'"]');const n=el.nextElementSibling;
              if(n&&n.classList.contains('bx-mob'))near=n.hidden?'next-hidden':'next-open';
              return 'up='+up.join(',')+' open='+vis.join(',')+' '+near}''',[g,k])
        pg.set_viewport_size({'width':W,'height':6000}); pg.wait_for_timeout(200)
        pg.locator('.lp-host').screenshot(path=SH+'/'+n+'.canvas.png')
        fl=(['SIDEWAYS'] if r['side'] else [])+(['WORD TAB'] if r['tab'] else [])+(['JS '+errs[0][:60]] if errs else [])+(['CHAT>SCREEN'] if r['chat']>Hh else [])+(['PAGE SCROLLS'] if r['doc']>Hh+1 else [])
        print('%-26s canvas %5d chat %4d up %d open %d | %s %s'%(n,r['canvas'],r['chat'],r['up'],r['open'],sw,' '.join(fl)))
        pg.close()
    b.close()
