"""Browser checks for the Bed Management Diagnosis turns: no sideways scroll, no "tab", chat one screen tall on desktop,
first element raised with its box open, tapping another switches, phone order. Optional screenshots (--shots DIR)."""
import glob, os, sys, re
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'out', 'bed-management', 'diagnosis', 'pages')
shots = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sorted(glob.glob(os.path.join(PAGES, '*.html'))):
        name = os.path.basename(f)[:-5]; mob = name.endswith('mobile')
        pg = b.new_page(viewport={'width': 390, 'height': 844} if mob else {'width': 1440, 'height': 900})
        pg.goto('file://' + f); pg.wait_for_timeout(250)
        r = pg.evaluate('''(mob)=>{
          const out=[];const sc=document.querySelector(mob?'.sh-mc':'.sh-mid');
          if(sc.scrollWidth>sc.clientWidth+1) out.push('sideways scroll '+sc.scrollWidth+'>'+sc.clientWidth);
          [...document.querySelectorAll('.lp *')].forEach(el=>{const r=el.getBoundingClientRect();const R=document.querySelector('.lp').getBoundingClientRect();
            if(r.width&&el.offsetParent&&(r.right>R.right+2||r.left<R.left-2)&&!el.closest('svg')) out.push('overflows: '+el.className);});
          if(/\\btabs?\\b/i.test(document.body.innerText)) out.push('says tab');
          if(!mob){const c=document.querySelector('.sh-chat').getBoundingClientRect();if(c.height>901) out.push('chat taller than a screen '+c.height);}
          const g=[...new Set([...document.querySelectorAll('.js-sel')].map(x=>x.dataset.grp))];
          g.forEach(k=>{const els=[...document.querySelectorAll('.js-sel[data-grp="'+k+'"]')];
            if(!els[0].classList.contains('is-up')&&!els.some(x=>x.classList.contains('is-up'))) out.push(k+': nothing raised');
            const up=els.find(x=>x.classList.contains('is-up'));const bx=[...document.querySelectorAll('[data-box="'+k+':'+up.dataset.key+'"]')].filter(x=>x.offsetParent);
            if(!bx.length) out.push(k+': raised element has no open box');
            if(mob&&bx.length&&up.compareDocumentPosition(bx[0])!==4) out.push(k+': phone box not after its element');
            const other=els.find(x=>x!==up);other.click();
            const bx2=[...document.querySelectorAll('[data-box="'+k+':'+other.dataset.key+'"]')].filter(x=>x.offsetParent);
            if(!other.classList.contains('is-up')||!bx2.length||up.classList.contains('is-up')) out.push(k+': tapping another does not switch');
            up.click();});
          if(mob){const seq=['.sh-um','.bd-mt','.lp-host','.bd-mr'].map(s=>document.querySelector('.sh-mc '+s));
            for(let i=1;i<seq.length;i++) if(!seq[i]||seq[i-1].compareDocumentPosition(seq[i])!==4) out.push('phone order wrong at '+i);}
          const h=document.querySelector('.lp-host').getBoundingClientRect().height;
          return {out:[...new Set(out)].slice(0,8),h:Math.round(h)};}''', mob)
        print('%-22s %5dpx  %s' % (name, r['h'], 'ok' if not r['out'] else '; '.join(r['out'])))
        bad += bool(r['out'])
        if shots:
            pg.add_style_tag(content='html,body{height:auto!important;overflow:visible!important}.sh-app,.sh-mid,.sh-m,.sh-mc{height:auto!important;overflow:visible!important}.sh-rail,.sh-chat{height:900px!important}')
            pg.wait_for_timeout(100)
            pg.screenshot(path=os.path.join(shots, name + '.png'), full_page=True)
        pg.close()
    b.close()
sys.exit(1 if bad else 0)
