"""
bm_au_blocks2 — more Bed Management Automations drawings (drafts, 1 Oct 2026): the library's switch-room motifs with the layer.

  helper      the library desk helper: what it would ask your IT team, each ask opening its sheet          (bm-au-02)
  relay       the library relay: the hand-over from discharge to the bed, each leg checked by the other side (bm-au-03)
  agent       the library thinker: its loop of notice, gather, check, draft, ask; each step opens its sheet   (bm-au-04)
  nightshift  the library night shift: the line from the 6 PM freeze to noon, with a clock you can play       (bm-au-06)
"""
import json, math
import bm_au_blocks as B
G = B.G
e, pt, pick, hint, desk, sheet = B.e, B.pt, B.pick, B.hint, B.desk, B.sheet

def register():
    return {'helper': r_helper, 'relay': r_relay, 'agent': r_agent, 'nightshift': r_nightshift}

# ------------------------------------------------------------------------------------------ helper
def r_helper(b, ctx):
    au = G['au']; grp = ctx.uid('auhp'); items, boxes = [], []
    for i, x in enumerate(b['asks']):
        s = b['sheets'][i]; first = i == 0
        items.append('<li><button type="button"%s%s><span class="hp-n">%d</span><span class="au-hi-t"><b>%s</b><em>%s</em></span>%s</button></li>%s' % (
            pick(grp, s['key'], first, 'au-hi'), pt(x), i + 1, e(x['title']), e(x['who']),
            '<span class="ax-tag ax-tag-%s">%s</span>' % (e(x.get('tag_state', 'waiting')), e(x['tag'])) if x.get('tag') else '', sheet(s, grp, first, 'mob-li')))
        boxes.append(sheet(s, grp, first, 'desk'))
    return ('<section class="ax-block ax-hp au-hp" data-block="helper">%s<div class="hp-grid"><div class="hp-bot">%s<div class="hp-bubble">%s</div></div>'
            '<div class="hp-main"><div class="ax-label">%s</div><ol class="hp-list au-hl">%s</ol><p class="hp-park">%s</p></div></div>%s</section>') % (
        hint(b.get('hint') or 'Pick an ask to see why it is needed and who in IT does it.'), au.BOT, e(b['says']), e(b['label']), ''.join(items), e(b['park']), desk(boxes))

# ------------------------------------------------------------------------------------------ relay
def r_relay(b, ctx):
    grp = ctx.uid('aurl'); legs = b['legs']; n = len(legs); items, boxes = [], []
    for i, l in enumerate(legs):
        s = b['sheets'][i]; first = i == 0
        items.append(('<li class="rl-leg rl-side-%s" data-leg="%d" style="grid-column:%d;grid-row:%d"><button type="button"%s%s><span class="rl-who"><i class="rl-%s"></i>%s</span><b>%s</b>'
                      '<span class="rl-t"><span class="rl-today">%s</span><span class="rl-with">%s</span></span></button>%s</li>%s') % (
            l['side'], i + 1, i + 1, 1 if l['side'] == 'dis' else 2, pick(grp, s['key'], first, 'rl-b'), pt(l), l['side'], e(l['who']), e(l['name']), e(l['today']), e(l['with']),
            '<span class="rl-check" title="Checked by the other side" aria-hidden="true"></span>' if l.get('checked') else '',
            sheet(s, grp, first, 'mob-li').replace('<li class="bx bx-mob', '<li style="grid-column:1/-1" class="bx bx-mob', 1)))
        boxes.append(sheet(s, grp, first, 'desk'))
    pts = ' '.join('%.2f,%d' % ((i + .5) * 100.0 / n, 25 if l['side'] == 'dis' else 75) for i, l in enumerate(legs))
    path = '<svg class="rl-path" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline points="%s"/></svg>' % pts
    g = b['gap']
    return ('<section class="ax-block ax-rl au-rl" data-block="relay" data-state="today">%s<div class="rl-bar"><div class="rl-switch au-rl-sw" role="group" aria-label="Which picture">'
            '<button type="button" data-state="today" aria-pressed="true">Today</button><button type="button" data-state="with" aria-pressed="false">%s</button></div>'
            '<p class="au-rl-gap"><span class="ax-label">%s</span> <b class="rl-today">%s</b><b class="rl-with">%s</b></p></div>'
            '<div class="rl-lanes" style="--n:%d"><span class="rl-lane rl-lane-dis">%s</span><span class="rl-lane rl-lane-bed">%s</span><div class="rl-track">%s</div><ol>%s</ol></div>%s%s</section>') % (
        hint(b.get('hint') or 'Pick a leg of the hand-over. Switch to see it with both sides linked.'), e(b['with_label']), e(g['label']), e(g['today']), e(g['with']), n,
        e(b['lane_dis']), e(b['lane_bed']), path, ''.join(items), '<p class="ax-cond">%s</p>' % e(b['condition']) if b.get('condition') else '', desk(boxes))

# ------------------------------------------------------------------------------------------ agent
def r_agent(b, ctx):
    au = G['au']; grp = ctx.uid('auag'); loop = b['loop']; n = len(loop)
    R, Cc = 118, 150
    nodes = []
    for i, l in enumerate(loop):
        a = -math.pi / 2 + 2 * math.pi * i / n; x, y = Cc + R * math.cos(a), Cc + R * math.sin(a)
        nodes.append('<g class="ag-node" data-stage="%s"><circle cx="%.1f" cy="%.1f" r="26"/><text x="%.1f" y="%.1f">%s</text></g>' % (e(l['id']), x, y, x, y + 4, e(l['name'])))
    ring = '<circle class="ag-ring" cx="%d" cy="%d" r="%d"/><circle class="ag-run" cx="%d" cy="%d" r="%d"/>' % (Cc, Cc, R, Cc, Cc, R)
    steps, boxes = [], []
    for i, st in enumerate(b['steps']):
        s = b['sheets'][i]; first = i == 0
        steps.append('<li><button type="button"%s data-stages="%s"%s><span class="hp-n">%d</span><span class="au-hi-t"><small>%s</small><b>%s</b></span></button></li>%s' % (
            pick(grp, s['key'], first, 'au-hi au-ag-s'), ','.join(st['stages']), pt(st), i + 1, e(st['when']), e(st['title']), sheet(s, grp, first, 'mob-li')))
        boxes.append(sheet(s, grp, first, 'desk'))
    never = ''.join('<li>%s</li>' % e(x) for x in b['never'])
    return ('<section class="ax-block ax-ag au-ag" data-block="agent">%s<div class="ag-grid"><div class="ag-stage"><svg class="ag-loop" viewBox="0 0 300 300" aria-hidden="true">%s%s</svg>'
            '<div class="ag-person">%s</div><div class="ag-cap">%s</div></div><div class="ag-side"><div class="ax-label">%s</div><ol class="au-hl">%s</ol></div></div>%s'
            '<div class="ag-never"><span class="ax-label">%s</span><ul>%s</ul></div></section>') % (
        hint(b.get('hint') or 'Pick a step. The loop lights where Tojo is, and the sheet says what it checks first.'), ring, ''.join(nodes), au.SILHOUETTE, e(b['caption']),
        e(b['steps_label']), ''.join(steps), desk(boxes), e(b['never_label']), never)

# ------------------------------------------------------------------------------------------ nightshift
def r_nightshift(b, ctx):
    au = G['au']; grp = ctx.uid('auns')
    st = b['stations']; t0, t1 = b['from'], b['to']
    fmap, anchors = au._line_map(st, t0, t1)
    x = lambda t: fmap(au._hours(t))
    now = b['start_at']
    night = b['night']
    band = '<span class="ns-night" style="left:%.2f%%;width:%.2f%%"><em>%s</em></span>' % (x(night['from']), x(night['to']) - x(night['from']), e(night['label']))
    wide, rows, tray, boxes = [], [], [], []
    for k, s in enumerate(st):
        sh = b['sheets'][k]; first = k == 0
        h = au._hours(s['at']); icon = au.HAND if s.get('hand') else au.GEAR
        wide.append('<button type="button"%s data-h="%.2f"%s style="left:%.2f%%"><span class="ns-box">%s<b>%d</b></span><span class="ns-lab"><small>%s</small>%s</span></button>' % (
            pick(grp, sh['key'], first, 'ns-st au-nst ' + ('ns-up' if k % 2 == 0 else 'ns-down') + (' ns-human' if s.get('hand') else '')), h, pt(s), anchors[k + 1][1],
            icon, k + 1, e(au._clock(s['at'])), e(s['title'])))
        rows.append('<li><button type="button"%s data-h="%.2f"><span class="ns-rt">%s</span><span class="ns-box">%s<b>%d</b></span><span class="ns-rl">%s</span></button></li>%s' % (
            pick(grp, sh['key'], first, 'ns-row' + (' ns-human' if s.get('hand') else '')), h, e(au._clock(s['at'])), icon, k + 1, e(s['title']), sheet(sh, grp, first, 'mob-li')))
        tray.append('<li class="ns-out" data-h="%.2f"><span class="ns-chk" aria-hidden="true"></span><span>%s</span></li>' % (h, e(s['makes'])))
        boxes.append(sheet(sh, grp, first, 'desk'))
    lv = b['goal']
    near = min(range(len(st)), key=lambda k: abs(au._hours(st[k]['at']) - au._hours(lv['at'])))   # the label sits on the side away from the nearest station
    goal = '<span class="ns-leave%s" style="left:%.2f%%"><span>%s <b>%s</b> %s</span></span>' % (' ns-leave-low' if near % 2 == 0 else '', x(lv['at']), e(lv['label']), e(au._clock(lv['at'])), au.src(lv['source']))
    opts = ''.join('<option value="%.2f"%s>%s</option>' % (au._hours(t), ' selected' if t == now else '', e(au._clock(t))) for t in b['clock'])
    return ('<section class="ax-block ax-ns au-ns" data-block="nightshift" data-now="%.2f" data-map="%s">%s'
            '<div class="ns-bar"><button type="button" class="ns-play" aria-label="Play the night">%s<span>%s</span></button>'
            '<label class="ns-clock"><span>Show the line at</span><input type="range" class="ns-range" min="%.2f" max="%.2f" step="0.25" value="%.2f" aria-label="Time of day"><output class="ns-now"></output></label>'
            '<select class="ns-pick" aria-label="Jump to a time">%s</select></div>'
            '<div class="ns-wide"><div class="ns-ticks"></div><div class="ns-floor">%s<div class="ns-belt"><span class="ns-flow" aria-hidden="true"></span></div>'
            '<span class="ns-hand" aria-hidden="true"></span>%s%s</div></div><ol class="ns-narrow">%s</ol>'
            '<div class="au-ns-low"><div class="ns-tray"><div class="ax-label">%s <b class="ns-now2"></b></div><ul>%s</ul></div></div>%s%s</section>') % (
        au._hours(now), json.dumps(anchors), hint(b.get('hint') or 'Play the night or move the clock. Pick a station to open it.'),
        '<svg viewBox="0 0 16 16" aria-hidden="true"><path class="ns-pl" d="M4 2.5 L13 8 L4 13.5 Z"/><path class="ns-pa" d="M4 3 V13 M11 3 V13"/></svg>', e(b['play']),
        au._hours(t0), au._hours(t1) + (24 if au._hours(t1) < au._hours(t0) else 0), au._hours(now), opts, band, ''.join(wide), goal, ''.join(rows),
        e(b['ready_label']), ''.join(tray), '<p class="ax-cond">%s</p>' % e(b['condition']) if b.get('condition') else '', desk(boxes))

JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  function clock(h){var v=h%24,hh=Math.floor(v),mm=Math.round((v-hh)*60);if(mm===60){hh++;mm=0;}
    if(hh===0&&mm===0)return 'midnight';if(hh===12&&mm===0)return 'noon';return ((hh%12)||12)+(mm?':'+(mm<10?'0':'')+mm:'')+' '+(hh<12?'AM':'PM');}
  /* relay: today, or with both sides linked */
  $$('.au-rl').forEach(function(rl){$$('.au-rl-sw button',rl).forEach(function(b){b.addEventListener('click',function(){rl.setAttribute('data-state',b.getAttribute('data-state'));
    $$('.au-rl-sw button',rl).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});});});});
  /* agent: the picked step lights its stages on the loop */
  $$('.au-ag').forEach(function(ag){function on(b){var st=(b.getAttribute('data-stages')||'').split(',');
      $$('.ag-node',ag).forEach(function(x){x.classList.toggle('is-on',st.indexOf(x.getAttribute('data-stage'))>=0);});}
    $$('.au-ag-s',ag).forEach(function(b){b.addEventListener('click',function(){on(b);});});var up=ag.querySelector('.au-ag-s.is-up');if(up)on(up);});
  /* nightshift: the clock moves along the line (the library's logic) */
  $$('.au-ns').forEach(function(n){var r=n.querySelector('.ns-range'),min=+r.min,max=+r.max,timer=null,play=n.querySelector('.ns-play'),pick=n.querySelector('.ns-pick');
    var mp=JSON.parse(n.getAttribute('data-map')),lab=play.querySelector('span').textContent;
    function px(h){if(h<=mp[0][0])return mp[0][1];for(var i=1;i<mp.length;i++){if(h<=mp[i][0]){var a=mp[i-1],b=mp[i];return a[1]+(b[1]-a[1])*((h-a[0])/((b[0]-a[0])||1));}}return mp[mp.length-1][1];}
    function at(h){r.value=h;n.querySelector('.ns-hand').style.left=px(h)+'%';n.querySelector('.ns-now').textContent=clock(h);n.querySelector('.ns-now2').textContent=clock(h);
      $$('[data-h]',n).forEach(function(x){x.classList.toggle('is-done',+x.getAttribute('data-h')<=h+0.001);});}
    function stop(){if(timer){clearInterval(timer);timer=null;}play.classList.remove('is-on');play.querySelector('span').textContent=lab;}
    r.addEventListener('input',function(){stop();at(+r.value);});pick.addEventListener('change',function(){stop();at(+pick.value);});
    play.addEventListener('click',function(){if(timer){stop();return;}var h=+r.value>=max-0.01?min:+r.value;play.classList.add('is-on');play.querySelector('span').textContent='Pause';
      if(reduce){at(max);stop();return;}timer=setInterval(function(){h+=0.25;if(h>=max){h=max;at(h);stop();return;}at(h);},120);});
    at(+n.getAttribute('data-now'));});
})();
'''

CSS = r'''
/* helper and agent: the list of asks or steps, each a pickable row */
.ax .au-hl{display:flex;flex-direction:column;gap:6px}
.au-hi{width:100%;display:grid;grid-template-columns:24px minmax(0,1fr) auto;gap:10px;align-items:center;padding:8px 10px;text-align:left;font:inherit;color:var(--ink);background:#fff;border:1.5px solid var(--line);border-radius:12px;cursor:pointer}
.au-hi-t{display:flex;flex-direction:column;gap:2px;min-width:0}.au-hi-t b{font-size:13.5px;font-weight:600;line-height:1.3}.au-hi-t em,.au-hi-t small{font-style:normal;font-size:11.5px;color:var(--muted);line-height:1.35}
.au-hi-t small{font-weight:700;text-transform:uppercase;letter-spacing:.04em;font-size:10.5px;color:var(--teal)}
.au-hi.tl-pick.is-up{border-color:var(--gold)}
.ax .au-hl li.bx{margin:2px 0 8px}
.ax[data-theme="bm"] .hp-n{color:var(--teal-l)}
.ax[data-theme="bm"] .ax-bot-s,.ax[data-theme="bm"] .ax-bot-s2{fill:#3B357A}.ax[data-theme="bm"] .ax-bot-scr{fill:#191730}.ax[data-theme="bm"] .ax-bot-e,.ax[data-theme="bm"] .ax-bot-t{fill:var(--teal-l)}
.au-hp .hp-main{gap:8px}
/* relay */
.au-rl-gap{flex:1 1 300px;font-size:13px;line-height:1.4}.au-rl-gap b{font-weight:600}
.ax-rl[data-state=today] .au-rl-gap .rl-with,.ax-rl[data-state=with] .au-rl-gap .rl-today{display:none}
.au-rl .rl-b.tl-pick.is-up{border-color:var(--gold);background:#FFF8E6!important}
.au-rl .rl-lanes ol>li.bx{grid-row:3}
.ax[data-theme="bm"] .rl-t{font-size:11.5px;color:var(--muted);line-height:1.35}
/* agent */
.au-ag{display:flex;flex-direction:column;gap:12px}
.au-ag .ag-side{gap:6px}
.ax[data-theme="bm"] .ag-node.is-on circle{fill:#3B357A}.ax[data-theme="bm"] .ag-node.is-on circle{filter:drop-shadow(0 0 6px rgba(201,194,245,.8))}
/* nightshift */
.au-ns{display:flex;flex-direction:column;gap:12px}
.au-ns .ns-st.tl-pick,.au-ns .ns-st.tl-pick.is-up{position:absolute;background:none!important;box-shadow:none!important;transform:translateX(-50%)}
.au-ns .ns-leave>span{bottom:auto;top:6px}.au-ns .ns-leave.ns-leave-low>span{top:auto;bottom:4px}
.au-ns .ns-st.is-up .ns-box{outline:2.5px solid var(--gold);outline-offset:2px}
.au-ns .ns-row.tl-pick,.au-ns .ns-row.tl-pick.is-up{background:none!important;box-shadow:none!important;transform:none}
.au-ns .ns-row.is-up .ns-box{outline:2.5px solid var(--gold);outline-offset:2px}
.au-ns-low{display:block}
.ax[data-theme="bm"] .ns-st.is-done .ns-box,.ax[data-theme="bm"] .ns-row.is-done .ns-box{background:#3B357A;box-shadow:0 0 14px rgba(201,194,245,.45)}
.ax[data-theme="bm"] .ns-belt{background:#191730;border-color:#4A4669}.ax[data-theme="bm"] .ns-flow{background:repeating-linear-gradient(90deg,transparent 0 14px,rgba(201,194,245,.3) 14px 17px,transparent 17px 30px)}
.ax[data-theme="bm"] .ns-box{background:#312E4A;border-color:#4A4669}.ax[data-theme="bm"] .ns-night{background:rgba(201,194,245,.07);border-color:rgba(201,194,245,.35)}
.ax[data-theme="bm"] .ns-gear,.ax[data-theme="bm"] .ax-gear{stroke:var(--teal-l)}
.au-ns .ns-row{box-sizing:border-box;padding-right:12px}
.au-ns .ns-narrow li.bx{margin:4px 0 10px;position:relative;z-index:2}
@container ax (max-width:699px){
 .ax .so-bar{flex-direction:column;align-items:stretch}.ax .so-bar .so-pre{width:100%;text-align:left}
 .au-hi{grid-template-columns:24px minmax(0,1fr)}.au-hi .ax-tag{grid-column:2;justify-self:start}
 .au-rl .rl-lanes ol>li.bx{grid-row:auto}
}
'''
