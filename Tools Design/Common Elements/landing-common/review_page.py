"""
review_page — the review pages every tab generator writes (shared by all tabs).

  turn file : one turn, desktop and phone side by side, both live and clickable.
  tab book  : every turn of one tab, a list of turns on the side, the same two views for the chosen one.

Each view is the generator's own page, loaded into a frame. The fonts are stored once in the review page and
added to each frame as it is built, so the file stays small. Nothing here draws a turn: it only frames what the
generator drew.
"""
import json, os, re

from landing_common import e, embedded_fonts


def _fonts_css():
    return re.sub(r'</?style[^>]*>', '', embedded_fonts())


def _pack(turns):
    return json.dumps([{k: t[k] for k in ('id', 'type', 'user', 'title', 'note', 'desktop', 'mobile')} for t in turns],
                      ensure_ascii=False).replace('</', '<\\/')


CSS = r'''
/* Review desk: a quiet frame around the generator's pages. Chrome only; the turns keep their own look. */
:root{--bg:#EEF1F4;--panel:#FFFFFF;--ink:#16263A;--muted:#5A6B7E;--line:#D3DAE2;--accent:#2E5E8E;--gold:#B8862B;--chip:#E6ECF2;
  --display:'Bebas Neue','Arial Narrow',sans-serif;--body:'Poppins','Segoe UI',system-ui,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11161C;--panel:#1A222B;--ink:#E7ECF1;--muted:#9AA9B8;--line:#2C3743;--accent:#8DB7E2;--gold:#E0B25A;--chip:#24303C;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#11161C;--panel:#1A222B;--ink:#E7ECF1;--muted:#9AA9B8;--line:#2C3743;--accent:#8DB7E2;--gold:#E0B25A;--chip:#24303C;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--body);margin:0}
.rv{box-sizing:border-box;padding-block:18px 32px;padding-inline:16px;max-width:1720px;margin:0 auto;display:flex;flex-direction:column;gap:14px}
.rv *,.rv *::before,.rv *::after{box-sizing:border-box}
.rv-top{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;flex-wrap:wrap;border-bottom:1.5px solid var(--line);padding-bottom:10px}
.rv-top h1{margin:0;font-family:var(--display);font-weight:400;font-size:40px;line-height:.95;letter-spacing:.01em;text-wrap:balance}
.rv-top p{margin:4px 0 0;font-size:13px;color:var(--muted)}
.rv-body{display:grid;grid-template-columns:260px minmax(0,1fr);gap:16px;align-items:start}
.rv-body.rv-one{grid-template-columns:minmax(0,1fr)}
.rv-list{display:flex;flex-direction:column;gap:6px;position:sticky;top:calc(env(safe-area-inset-top,0px) + 10px);max-height:calc(100vh - 40px);overflow:auto;padding-right:2px}
.rv-list button{all:unset;box-sizing:border-box;cursor:pointer;display:grid;grid-template-columns:auto minmax(0,1fr);gap:2px 10px;padding:9px 11px;border-radius:6px;background:var(--panel);border:1.5px solid var(--line)}
.rv-list button:hover{border-color:var(--accent)}
.rv-list button[aria-current=true]{border-color:var(--accent);box-shadow:inset 4px 0 0 var(--accent)}
.rv-list button:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.rv-id{font-family:var(--display);font-size:22px;line-height:1;grid-row:span 2;align-self:center;min-width:52px}
.rv-ty{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--accent)}
.rv-um{font-size:12.5px;line-height:1.3;color:var(--ink);overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.rv-main{display:flex;flex-direction:column;gap:12px;min-width:0}
.rv-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap}
.rv-head h2{margin:0;font-family:var(--display);font-weight:400;font-size:30px;line-height:1}
.rv-head q{display:block;margin-top:4px;font-size:14px;color:var(--muted);quotes:"“" "”"}
.rv-note{font-size:12.5px;color:var(--muted);max-width:70ch;margin:2px 0 0}
.rv-seg{display:inline-flex;border:1.5px solid var(--line);border-radius:22px;overflow:hidden;background:var(--panel)}
.rv-seg button{all:unset;cursor:pointer;font-size:12.5px;font-weight:600;padding:0 14px;min-height:36px;display:flex;align-items:center;color:var(--muted)}
.rv-seg button[aria-pressed=true]{background:var(--ink);color:var(--panel)}
.rv-seg button:focus-visible{outline:3px solid var(--gold);outline-offset:-3px}
.rv-views{display:grid;grid-template-columns:minmax(0,1fr) 406px;gap:18px;align-items:start}
.rv-views[data-show=desktop]{grid-template-columns:minmax(0,1fr)} .rv-views[data-show=desktop] .rv-phone{display:none}
.rv-views[data-show=mobile]{grid-template-columns:minmax(0,1fr);justify-items:center} .rv-views[data-show=mobile] .rv-desk{display:none}
.rv-cap{display:flex;justify-content:space-between;align-items:center;font-size:11.5px;font-weight:600;color:var(--muted);margin-bottom:6px;gap:8px}
.rv-cap button{all:unset;cursor:pointer;color:var(--accent);font-weight:600;min-height:28px;display:flex;align-items:center}
.rv-cap button:focus-visible{outline:2px solid var(--gold)}
.rv-desk{min-width:0}
.rv-screen{position:relative;width:100%;overflow:hidden;border-radius:10px;border:1.5px solid var(--line);background:#fff;box-shadow:0 10px 30px rgba(10,20,35,.12)}
.rv-screen iframe{position:absolute;left:0;top:0;width:1440px;height:900px;border:0;transform-origin:0 0}
.rv-phone{width:406px;max-width:100%}
.rv-pbox{width:100%;overflow:hidden}
.rv-handset{border:8px solid #1c232b;border-radius:34px;overflow:hidden;background:#fff;width:406px;transform-origin:0 0}
.rv-handset iframe{display:block;width:390px;height:844px;border:0}
@media (max-width:1100px){.rv-body{grid-template-columns:minmax(0,1fr)}.rv-list{position:static;max-height:none;flex-direction:row;overflow-x:auto;padding-bottom:4px}.rv-list button{min-width:210px}
  .rv-views{grid-template-columns:minmax(0,1fr)}.rv-phone{justify-self:center}}
@media (prefers-reduced-motion:reduce){.rv *{transition:none!important}}
'''

JS = r'''
(function(){
  var T=JSON.parse(document.getElementById('rv-data').textContent), F=document.getElementById('rv-fonts').textContent;
  var list=document.querySelector('.rv-list'), head=document.querySelector('.rv-head'), views=document.querySelector('.rv-views');
  var desk=views.querySelector('.rv-screen'), hand=views.querySelector('.rv-handset'), full=false, cur=null;
  function doc(t,v){return t[v].replace('<html lang="en">','<html lang="en" data-frame="'+t.id+'-'+v+'">').replace('</head>','<style>'+F+'</style></head>');}
  var pbox=views.querySelector('.rv-pbox');
  function fit(){var f=desk.querySelector('iframe');if(f){var s=desk.clientWidth/1440;f.style.transform='scale('+s+')';desk.style.height=Math.round(900*s)+'px';}
    var p=Math.min(1,(pbox.clientWidth||406)/406);hand.style.transform=p<1?'scale('+p+')':'';pbox.style.height=Math.round(hand.offsetHeight*p)+'px';}
  function show(i){cur=T[i];
    [].slice.call(list?list.querySelectorAll('button'):[]).forEach(function(b,k){b.setAttribute('aria-current',k===i?'true':'false');});
    head.querySelector('h2').textContent=cur.id+' · '+cur.title;
    var q=head.querySelector('q');q.textContent=cur.user||'';q.hidden=!cur.user;
    var n=head.querySelector('.rv-note');n.textContent=cur.note||'';n.hidden=!cur.note;
    desk.innerHTML='';hand.innerHTML='';
    var a=document.createElement('iframe');a.title=cur.id+' on desktop, 1440 by 900';a.setAttribute('srcdoc',doc(cur,'desktop'));desk.appendChild(a);
    var b=document.createElement('iframe');b.title=cur.id+' on a phone, 390 wide';b.setAttribute('srcdoc',doc(cur,'mobile'));hand.appendChild(b);
    b.style.height='844px';full=false;views.querySelector('.rv-full').textContent='Show full length';fit();
    try{if(list)history.replaceState(null,'','#'+cur.id);}catch(e){}}
  window.addEventListener('message',function(ev){var d=ev.data||{};if(!d.tojoHeight||!cur)return;
    if(d.tojoId===cur.id+'-mobile'){hand.setAttribute('data-h',d.tojoHeight);if(full){hand.querySelector('iframe').style.height=d.tojoHeight+'px';fit();}}});
  views.querySelector('.rv-full').addEventListener('click',function(ev){full=!full;var f=hand.querySelector('iframe');
    f.style.height=full?(hand.getAttribute('data-h')||2400)+'px':'844px';ev.currentTarget.textContent=full?'Show one screen':'Show full length';fit();});
  [].slice.call(document.querySelectorAll('.rv-seg button')).forEach(function(b){b.addEventListener('click',function(){
    [].slice.call(document.querySelectorAll('.rv-seg button')).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
    views.setAttribute('data-show',b.getAttribute('data-show'));lastW=-1;setTimeout(fit,0);});});
  if(list){T.forEach(function(t,i){var b=document.createElement('button');b.type='button';
    b.innerHTML='<span class="rv-id"></span><span class="rv-ty"></span><span class="rv-um"></span>';
    b.querySelector('.rv-id').textContent=t.id;b.querySelector('.rv-ty').textContent=t.type;b.querySelector('.rv-um').textContent=t.user||t.title;
    b.addEventListener('click',function(){show(i);});list.appendChild(b);});}
  var lastW=-1,raf=0;function refit(){cancelAnimationFrame(raf);raf=requestAnimationFrame(function(){var w=views.clientWidth;if(w===lastW)return;lastW=w;fit();});}
  if(window.ResizeObserver){new ResizeObserver(refit).observe(views);}window.addEventListener('resize',refit);
  var h=(location.hash||'').slice(1), start=0;T.forEach(function(t,i){if(t.id===h)start=i;});show(start);
})();
'''


def page(title, heading, sub, turns, book=True, fragment=False):
    body = ('<div class="rv"><header class="rv-top"><div><h1>%s</h1><p>%s</p></div></header>'
            '<div class="rv-body%s">%s<main class="rv-main"><div class="rv-head"><div><h2></h2><q></q><p class="rv-note"></p></div>'
            '<div class="rv-seg" role="group" aria-label="Which view"><button type="button" data-show="both" aria-pressed="true">Both</button>'
            '<button type="button" data-show="desktop" aria-pressed="false">Desktop</button><button type="button" data-show="mobile" aria-pressed="false">Phone</button></div></div>'
            '<div class="rv-views" data-show="both"><section class="rv-desk" aria-label="Desktop view"><div class="rv-cap"><span>Desktop · 1440 × 900, live</span></div><div class="rv-screen"></div></section>'
            '<section class="rv-phone" aria-label="Phone view"><div class="rv-cap"><span>Phone · 390 wide, live</span><button type="button" class="rv-full">Show full length</button></div><div class="rv-pbox"><div class="rv-handset"></div></div></section></div>'
            '</main></div></div>') % (e(heading), e(sub), '' if book else ' rv-one', '<nav class="rv-list" aria-label="Turns"></nav>' if book else '')
    data = '<script type="application/json" id="rv-data">%s</script>' % _pack(turns)
    inner = '<title>%s</title><style id="rv-fonts">%s</style><style>%s</style>%s%s<script>%s</script>' % (e(title), _fonts_css(), CSS, body, data, JS)
    if fragment:
        return inner
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">%s</head><body>%s</body></html>' % (
        inner[:inner.index('</style>', inner.index('</style>') + 1) + 8], inner[inner.index('</style>', inner.index('</style>') + 1) + 8:])
