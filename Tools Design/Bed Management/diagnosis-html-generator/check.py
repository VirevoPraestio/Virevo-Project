"""Browser checks for Bed Management Diagnosis pages: no sideways scroll, no "tab", first item raised with its sheet open,
tapping another switches, phone order, and entries: two entries both land in the chat message. --shots DIR for screenshots."""
import glob, os, sys
from playwright.sync_api import sync_playwright
PAGES = os.path.abspath(sys.argv[1]); shots = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sorted(glob.glob(os.path.join(PAGES, '*.html'))):
        name = os.path.basename(f)[:-5]; mob = name.endswith('mobile')
        pg = b.new_page(viewport={'width': 390, 'height': 844} if mob else {'width': 1440, 'height': 900})
        pg.goto('file://' + f.replace(' ', '%20')); pg.wait_for_timeout(300)
        if shots:
            pg.screenshot(path=os.path.join(shots, name + '.top.png'))
        r = pg.evaluate('''(mob)=>{const out=[];const sc=document.querySelector(mob?'.sh-mc':'.sh-mid');
          if(sc.scrollWidth>sc.clientWidth+1) out.push('sideways scroll');
          if(/\\btabs?\\b/i.test(document.body.innerText)) out.push('says tab');
          const g=[...new Set([...document.querySelectorAll('.tl-pick')].map(x=>x.dataset.grp))];
          g.forEach(k=>{const els=[...document.querySelectorAll('.tl-pick[data-grp="'+k+'"]')].filter(x=>x.offsetParent||x.getClientRects().length);
            const up=els.find(x=>x.classList.contains('is-up'));if(!up){out.push(k+': nothing raised');return;}
            const vis=q=>[...document.querySelectorAll('[data-box="'+k+':'+q+'"]')].filter(x=>x.offsetParent);
            if(!vis(up.dataset.key).length) out.push(k+': no open sheet');
            const o=els.find(x=>x!==up);o.click();if(!vis(o.dataset.key).length||up.classList.contains('is-up')) out.push(k+': switch fails');
            if(mob){const bx=vis(o.dataset.key)[0];if(bx&&o.compareDocumentPosition(bx)!==4) out.push('phone sheet not after item');}
            up.click();});
          const ents=[...document.querySelectorAll('.tl-entry')].filter(x=>x.offsetParent);
          ents.slice(0,2).forEach((en,i)=>{en.querySelector('.tl-add').click();const ta=en.querySelector('textarea');ta.value='test entry '+(i+1);ta.dispatchEvent(new Event('input'));});
          document.querySelector('.sh-pr').click();
          const v=document.getElementById('tojo-input').value;
          if(ents.length>=2&&!(v.includes('test entry 1')&&v.includes('test entry 2'))) out.push('entries do not both reach the message: '+v);
          if(mob){const seq=['.sh-um','.bm-mt','.tj','.bm-mr'].map(s=>document.querySelector('.sh-mc '+s));
            for(let i=1;i<seq.length;i++) if(!seq[i]||seq[i-1].compareDocumentPosition(seq[i])!==4) out.push('phone order wrong');}
          return {out, msg:v};}''', mob)
        print('%-26s %s' % (name, 'ok' if not r['out'] else '; '.join(r['out'])))
        if name.endswith('A.desktop'): print('   message after two entries and a prompt:\n   ' + r['msg'].replace('\n', '\n   '))
        bad += bool(r['out'])
        if shots:
            pg.add_style_tag(content='html,body{height:auto!important;overflow:visible!important}.sh-app,.sh-mid,.sh-m,.sh-mc{height:auto!important;overflow:visible!important}.sh-rail,.sh-chat{height:900px!important}')
            pg.wait_for_timeout(150); pg.screenshot(path=os.path.join(shots, name + '.png'), full_page=True)
        pg.close()
    b.close()
sys.exit(1 if bad else 0)
