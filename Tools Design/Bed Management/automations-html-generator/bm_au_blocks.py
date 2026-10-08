"""
bm_au_blocks — Bed Management Automations drawings (drafts, 1 Oct 2026).

The Automations motifs come from the block library (07 §1.4, the switch room): drawn switches, the main switch every
automation waits on, wires from one bus, lamps, the charcoal screen where the machine works, the digital brain and its
glowing network. Here they are drawn in Bed Management's Automations look (the night shift, from the approved landing
page: lilac-grey ground, ink-violet panels, violet = switched on) and carry the common tool layer.

  heading   the library heading, with the station plate from the landing page (four lamps: idea, built, testing, switched on)
  sources   the library switchboard, layered: records as switches, the main switch on top, automations as lamps
  brain     the library brain, layered: the day's records flow in pass by pass and the engine's outputs fill
  panel     the landing page's station panel: one row per automation, four lamps, stepped through the build
  effect    the quantity named, in five looks that change with the turn
  actions   the three buttons that close every turn (rules/08 §8)

register(G) is called by bm_automations_html with its helpers (e, L, au, C).
"""
G = {}
def e(s): return G['e'](s)
def pt(o): return ' data-tj-point="%d"' % int(o['point']) if isinstance(o, dict) and o.get('point') is not None else ''
def pick(grp, key, first, cls=''): return G['L'].pick_attrs(grp, key, first, cls)
def hint(t): return '<p class="tl-hint au-hint"><span class="au-ping" aria-hidden="true"></span>%s</p>' % e(t)
def desk(boxes): return '<div class="bx-desk-wrap">%s</div>' % ''.join(boxes)
STAGES = ['Idea', 'Built', 'Testing', 'Switched on']

def register(helpers):
    G.update(helpers)
    return {'heading': r_heading, 'sources': r_sources, 'brain': r_brain, 'panel': r_panel, 'effect': r_effect}

# ------------------------------------------------------------------------------------------ the sheet: an instrument panel
def sheet(s, grp, first, where):
    L = G['L']; fill = '%s:%s' % (grp, s['key'])
    label = s.get('entry_label') or ('%s · %s' % (s['when'], s['title']))
    entry = L.entry(label, s['entry'], s.get('entry_hint', 'Type what your hospital has today'), open_=s.get('entry_open', False), fill=fill) if s.get('entry') else ''
    lines = ''.join('<div class="au-ln" data-state="%s"><dt>%s</dt><dd>%s</dd></div>' % (e(x.get('state', 'plain')), e(x['label']), e(x['value'])) for x in s.get('lines', []))
    hand = ''
    if s.get('hand'):
        hand = '<div class="au-hand">%s<span><b>A person’s hand here: %s</b>%s</span></div>' % (G['au'].HAND, e(s['hand']['who']), e(s['hand']['does']))
    ask = L.say(s['ask']['label'], s['ask']['say'], 'au-ask') if s.get('ask') else ''
    tag = 'li' if where == 'mob-li' else 'div'; w = 'mob' if where.startswith('mob') else 'desk'
    return ('<%s class="bx bx-%s au-sheet%s" data-box="%s:%s"%s><div class="au-sh-top"><span class="au-led" aria-hidden="true"></span><small>%s</small></div>'
            '<div class="au-sh-in"><div class="au-sh-a"><h3>%s</h3><p>%s</p>%s%s</div>%s%s</div></%s>') % (
        tag, w, '' if entry else ' one', grp, e(s['key']), '' if first else ' hidden', e(s['when']), e(s['title']), e(s['text']), hand, ask,
        '<dl class="au-sh-dl">%s</dl>' % lines if lines else '', '<div class="au-sh-e">%s</div>' % entry if entry else '', tag)

# ------------------------------------------------------------------------------------------ heading with the station plate
def r_heading(b, ctx):
    h = G['au'].r_heading(b)
    p = b.get('plate')
    if not p: return h
    at = STAGES.index(p['stage'])
    lamps = ''.join('<li class="%s"><i></i><span>%s</span></li>' % ('is-done' if i < at else ('is-at' if i == at else ''), e(x)) for i, x in enumerate(STAGES))
    plate = ('<div class="au-plate" aria-label="%s, %s"><div class="au-pl-top"><span class="au-pl-n">%s</span><b>%s</b></div><ol class="au-pl-l">%s</ol></div>') % (
        e(p['name']), e(p['stage']), e(p['tag']), e(p['name']), lamps)
    return '<div class="au-hdw">%s%s</div>' % (h, plate)

# ------------------------------------------------------------------------------------------ sources: the library switchboard, layered
def _switch(on, label):
    return ('<button type="button" class="so-sw" role="switch" aria-checked="%s" aria-label="%s"><span class="so-track"><span class="so-knob"></span></span></button>' % (
        'true' if on else 'false', e(label)))

def r_sources(b, ctx):
    grp = ctx.uid('ausr'); srcs, sheets = b['sources'], b['sheets']; on = b.get('default_on', [])
    m = b['main']
    main = ('<li class="so-src au-main" data-id="%s"%s>%s<div class="so-b"><small class="au-mk">%s</small><b>%s</b><span>%s</span></div><span class="so-wire" aria-hidden="true"></span></li>') % (
        e(m['id']), pt(m), _switch(m['id'] in on, m['name']), e(m['tag']), e(m['name']), e(m['line']))
    rows, boxes = [], []
    for i, s in enumerate(srcs):
        sh = sheets[i]; first = i == 0
        tagc = {'waiting': 'Waiting on your IT team', 'needed': 'Need from you', 'ours': 'We bring it', 'linked': 'Linked'}[s['link']]
        rows.append(('<li class="so-src" data-id="%s"%s>%s<button type="button"%s><b>%s</b><span>%s</span><span class="ax-tag ax-tag-%s">%s</span></button>'
                     '<span class="so-wire" aria-hidden="true"></span></li>%s') % (
            e(s['id']), pt(s), _switch(s['id'] in on, s['name']), pick(grp, sh['key'], first, 'so-b au-sb'), e(s['name']), e(s['holds']),
            {'ours': 'none', 'needed': 'needed'}.get(s['link'], s['link']), e(tagc), sheet(sh, grp, first, 'mob-li')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    lamps = ''.join('<li class="so-auto" data-needs="%s"%s><span class="so-lamp" aria-hidden="true"></span><span><b>%s</b><em class="so-why"></em></span></li>' % (
        ','.join(a['needs']), pt(a), e(a['name'])) for a in b['automations'])
    names = {s['id']: s['short'] for s in srcs}; names[m['id']] = m['short']
    import json
    pres = ''.join('<button type="button" class="so-pre" data-on="%s">%s</button>' % (','.join(p['on']), e(p['label'])) for p in b.get('presets', []))
    return ('<section class="ax-block ax-so au-so" data-block="sources" data-names=\'%s\'>%s<div class="so-bar"><span class="ax-label">Try it:</span>%s</div>'
            '<div class="so-board"><div class="so-col"><div class="ax-label">%s</div><ul class="so-srcs">%s%s</ul></div>'
            '<div class="so-bus" aria-hidden="true"><span></span></div>'
            '<div class="so-col"><div class="ax-label">%s</div><ul class="so-autos">%s</ul><p class="so-read" aria-live="polite"></p></div></div>%s%s</section>') % (
        json.dumps(names).replace("'", '&#39;'), hint(b.get('hint') or 'Flip a switch to link a record. Pick a record to see what your IT team gives.'), pres,
        e(b['src_label']), main, ''.join(rows), e(b['auto_label']), lamps, '<p class="ax-cond">%s</p>' % e(b['condition']) if b.get('condition') else '', desk(boxes))

# ------------------------------------------------------------------------------------------ brain: the library brain, layered, over one day
def r_brain(b, ctx):
    au = G['au']; grp = ctx.uid('aubr')
    kinds, outs, passes, sheets = b['kinds'], b['outputs'], b['passes'], b['sheets']
    sel = len(passes) if b.get('start_full') else 1
    kin = ''.join('<li class="br-k" data-k="%s"%s><span class="br-dot" aria-hidden="true"></span><span><b>%s</b><em>%s</em></span><span class="br-c">0</span></li>' % (
        e(k['k']), pt(k), e(k['name']), e(k['example'])) for k in kinds)
    sec = ''.join('<li class="br-s" data-kinds="%s"%s><span><b>%s</b></span><span class="br-bar" aria-hidden="true"><i></i></span><span class="br-p">0%%</span></li>' % (
        ','.join(o['from']), pt(o), e(o['name'])) for o in outs)
    btn, boxes = [], []
    for i, p in enumerate(passes):
        sh = sheets[i]; first = i == sel - 1
        btn.append('<div class="au-pass"><button type="button"%s data-day="%d"%s><b>%s</b><span>%s</span></button>%s</div>' % (
            pick(grp, sh['key'], first, 'br-day au-day'), i + 1, pt(p), e(p['label']), e(p['what']), sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    import json
    evs = json.dumps([[ev for ev in p['brings']] for p in passes])
    return ('<section class="ax-block ax-br au-br" data-block="brain" data-day="%d" data-evs=\'%s\'>%s<div class="br-days au-days" role="group" aria-label="%s" style="--np:%d">%s'
            '<button type="button" class="br-play au-play">%s</button></div>'
            '<div class="br-screen"><div class="br-col"><div class="br-h">%s</div><ul class="br-kinds">%s</ul></div>'
            '<div class="br-mid">%s<div class="br-count"><b class="br-n">0</b> %s</div></div>'
            '<div class="br-col"><div class="br-h">%s</div><ul class="br-secs">%s</ul></div></div>%s%s</section>') % (
        sel, evs.replace("'", '&#39;'), hint(b.get('hint') or 'Pick a time of day. The records flow in and the engine’s answers fill.'), e(b['passes_label']), len(passes), ''.join(btn),
        e(b['play']), e(b['in_label']), kin, au._brain_svg(len(kinds), len(outs)), e(b['count_label']), e(b['out_label']), sec,
        '<p class="ax-cond">%s</p>' % e(b['condition']) if b.get('condition') else '', desk(boxes))

# ------------------------------------------------------------------------------------------ panel: the station panel, stepped through the build
def r_panel(b, ctx):
    grp = ctx.uid('aupn'); rows, boxes = [], []
    phases = b['phases']; n = len(phases)
    mains = ''.join('<li class="pn-main" data-on-at="%d"><span class="pn-msw" aria-hidden="true"><i></i></span><span><small>%s</small><b>%s</b><em>%s</em></span></li>' % (
        m['on_at'], e(m['tag']), e(m['name']), e(m['line'])) for m in b['mains'])
    for i, a in enumerate(b['automations']):
        sh = b['sheets'][i]; first = i == 0
        lamps = ''.join('<i class="pn-lamp" data-s="%d" aria-hidden="true"></i>' % k for k in range(4))
        rows.append('<li class="pn-li"><button type="button"%s data-stages="%s"%s><span class="pn-n">%d</span><span class="pn-t"><b>%s</b><em>%s</em></span><span class="pn-lamps">%s</span></button>%s</li>' % (
            pick(grp, sh['key'], first, 'pn-row'), ','.join(str(x) for x in a['stages']), pt(a), i + 1, e(a['name']), e(a['line']), lamps, sheet(sh, grp, first, 'mob-li')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    steps = ''.join('<button type="button" class="pn-ph" data-ph="%d" aria-pressed="%s"><small>%s</small><b>%s</b></button>' % (
        k, 'true' if k == 0 else 'false', e(p['when']), e(p['name'])) for k, p in enumerate(phases))
    heads = ''.join('<span>%s</span>' % e(x) for x in STAGES)
    return ('<section class="ax-block au-pn" data-block="panel" data-ph="0" data-n="%d">%s<div class="pn-steps" role="group" aria-label="%s">%s</div>'
            '<div class="pn-board"><ul class="pn-mains">%s</ul><div class="pn-head" aria-hidden="true"><span>%s</span><span class="pn-heads">%s</span></div><ol class="pn-rows">%s</ol>'
            '<div class="pn-foot"><span>%s</span><b class="pn-count" aria-live="polite"></b></div></div><p class="pn-read" aria-live="polite"></p>%s</section>') % (
        n, hint(b.get('hint') or 'Step through the build. The lamps light as each automation moves on. Pick a row to open it.'), e(b['phases_label']), steps,
        mains, e(b['rows_label']), heads, ''.join(rows), e(b['foot']), desk(boxes))

# ------------------------------------------------------------------------------------------ effect
EFFECT_STYLES = ['panel', 'meter', 'banner', 'ticket', 'stamp']
def r_effect(b, ctx):
    n = getattr(ctx, 'turn', 1); k = getattr(ctx, 'eff', 0); ctx.eff = k + 1
    style = EFFECT_STYLES[(n + k + getattr(ctx, 'sample', 0)) % len(EFFECT_STYLES)]
    sw = '<span class="au-eff-sw" aria-hidden="true"><i></i></span>'
    return ('<section class="ax-block au-eff au-eff-%s" data-block="effect" data-state="%s">%s<div class="au-eff-b"><div class="ax-label">%s</div><div class="au-eff-v">%s</div><p>%s</p></div></section>') % (
        style, e(b.get('state', 'plain')), sw, e(b['label']), e(b['value']), e(b['sub']))

# ------------------------------------------------------------------------------------------ the three buttons
def actions(a):
    btn = lambda k, head, d: '<button type="button" class="au-act au-act-%s" data-say-lead data-text="%s"><span class="au-act-k">%s</span><span class="au-act-d">%s</span></button>' % (
        k, e(d['say']), e(head), e(d['detail']))
    return '<nav class="au-acts" aria-label="What to do next">%s%s%s</nav>' % (
        btn('go', 'Proceed with next step', a['go']), btn('add', 'Add more', a['add']), btn('jump', 'Jump to ' + a['jump']['tab'], a['jump']))

JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  /* sources: flip switches; an automation lights when every record it needs is linked (the library's logic) */
  $$('.au-so').forEach(function(so){var names=JSON.parse(so.getAttribute('data-names'));
    function on(){return $$('.so-src',so).filter(function(s){return s.querySelector('.so-sw').getAttribute('aria-checked')==='true';}).map(function(s){return s.getAttribute('data-id');});}
    function upd(){var o=on(),k=0,autos=$$('.so-auto',so);
      $$('.so-src',so).forEach(function(s){s.classList.toggle('is-on',o.indexOf(s.getAttribute('data-id'))>=0);});
      autos.forEach(function(a){var need=a.getAttribute('data-needs').split(','),miss=need.filter(function(x){return o.indexOf(x)<0;});
        a.classList.toggle('is-on',!miss.length);if(!miss.length)k++;
        a.querySelector('.so-why').textContent=miss.length?('Waits on '+miss.map(function(x){return names[x];}).join(' and ')):'Can switch on';});
      so.querySelector('.so-read').textContent=k+' of '+autos.length+' can switch on with these links.';
      $$('.so-pre',so).forEach(function(p){var want=p.getAttribute('data-on').split(',').filter(Boolean).sort().join(',');p.setAttribute('aria-pressed',want===o.slice().sort().join(',')?'true':'false');});}
    $$('.so-sw',so).forEach(function(b){b.addEventListener('click',function(ev){ev.stopPropagation();b.setAttribute('aria-checked',b.getAttribute('aria-checked')==='true'?'false':'true');upd();});});
    $$('.so-pre',so).forEach(function(p){p.addEventListener('click',function(){var want=p.getAttribute('data-on').split(',');
      $$('.so-src',so).forEach(function(s){s.querySelector('.so-sw').setAttribute('aria-checked',want.indexOf(s.getAttribute('data-id'))>=0?'true':'false');});upd();});});
    upd();});
  /* brain: pick a time of day; records flow in and the outputs fill (the library's logic) */
  $$('.au-br').forEach(function(br){var ev=JSON.parse(br.getAttribute('data-evs')),timer=null;
    function day(d){br.setAttribute('data-day',d);var c={},tot=0;
      for(var i=0;i<d;i++){ev[i].forEach(function(k){c[k]=(c[k]||0)+1;tot++;});}
      var all={};ev.forEach(function(x){x.forEach(function(k){all[k]=(all[k]||0)+1;});});
      $$('.br-k',br).forEach(function(k){var v=c[k.getAttribute('data-k')]||0;k.querySelector('.br-c').textContent=v;k.classList.toggle('is-on',v>0);
        k.classList.toggle('is-new',(ev[d-1]||[]).indexOf(k.getAttribute('data-k'))>=0);});
      $$('.br-s',br).forEach(function(s){var ks=s.getAttribute('data-kinds').split(','),a=0,b=0;ks.forEach(function(k){a+=c[k]||0;b+=all[k]||0;});
        var p=b?Math.round(100*a/b):0;s.querySelector('.br-bar i').style.width=p+'%';s.querySelector('.br-p').textContent=p+'%';s.classList.toggle('is-full',p===100);});
      br.querySelector('.br-n').textContent=tot;
      br.classList.remove('is-pulse');void br.offsetWidth;br.classList.add('is-pulse');}
    $$('.au-day',br).forEach(function(b){b.addEventListener('click',function(){if(timer){clearInterval(timer);timer=null;}day(+b.getAttribute('data-day'));});});
    br.querySelector('.au-play').addEventListener('click',function(){if(timer)clearInterval(timer);var d=1,days=$$('.au-day',br);days[0].click();if(reduce){days[ev.length-1].click();return;}
      timer=setInterval(function(){d++;if(d>ev.length){clearInterval(timer);timer=null;return;}days[d-1].click();},1100);});
    day(+br.getAttribute('data-day'));});
  /* panel: step through the build; each row's lamps light to its stage at that step */
  $$('.au-pn').forEach(function(pn){var n=+pn.getAttribute('data-n');
    function ph(k){pn.setAttribute('data-ph',k);var on=0;
      $$('.pn-ph',pn).forEach(function(b){b.setAttribute('aria-pressed',+b.getAttribute('data-ph')===k?'true':'false');});
      $$('.pn-main',pn).forEach(function(m){m.classList.toggle('is-on',k>=+m.getAttribute('data-on-at'));});
      $$('.pn-row',pn).forEach(function(r){var st=r.getAttribute('data-stages').split(',').map(Number)[k];
        $$('.pn-lamp',r).forEach(function(l){var s=+l.getAttribute('data-s');l.classList.toggle('is-on',s<=st);l.classList.toggle('is-at',s===st);});
        if(st===3)on++;});
      pn.querySelector('.pn-count').textContent=on+' of '+$$('.pn-row',pn).length+' switched on';
      var cur=pn.querySelector('.pn-ph[data-ph="'+k+'"]');pn.querySelector('.pn-read').textContent=cur?cur.querySelector('small').textContent+': '+cur.querySelector('b').textContent:'';}
    $$('.pn-ph',pn).forEach(function(b){b.addEventListener('click',function(){ph(+b.getAttribute('data-ph'));});});
    ph(0);});
})();
'''

CSS = r'''
/* ---- Bed Management Automations: the night shift on the library's switch room ---- */
.ax[data-theme="bm"]{--ground:#E5E4EC;--panel:#FBFBFD;--ink:#25233A;--muted:#54526A;--teal:#4B3FA0;--teal-l:#C9C2F5;--off:#93919F;--amber:#8A5608;--gold:#d4a94f;--gold-t:#6B4F16;
  --screen:#25233A;--screen-2:#312E4A;--glow:#C9C2F5;--red:#8E2F1C;--green:#2F6B4F;--line:rgba(37,35,58,.14);--soft:#EEEDF5;--acc:#4B3FA0;--card:#FBFBFD;
  background-image:radial-gradient(rgba(37,35,58,.07) 1px,transparent 1.2px);background-size:18px 18px;padding:24px 34px 32px}
.ax[data-theme="bm"][data-tone="night"]{--ground:#DEDCE8;--panel:#FDFDFF;--soft:#E9E7F1;background-image:linear-gradient(rgba(37,35,58,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(37,35,58,.05) 1px,transparent 1px);background-size:22px 22px}
.ax .tj-lit{outline:4px solid var(--gold)!important;outline-offset:3px}
.ax[data-theme="bm"] .ax-eyebrow::before{box-shadow:inset 13px 0 0 -2px var(--teal-l)}
.ax[data-theme="bm"] .br-screen::before{background:radial-gradient(circle at 50% 50%,rgba(201,194,245,.16),transparent 55%)}
.ax[data-theme="bm"] .br-k.is-new{background:#3B357A}
.ax[data-theme="bm"] .so-auto.is-on .so-lamp{box-shadow:0 0 0 4px rgba(75,63,160,.18)}
.au-hint{display:flex;align-items:center;gap:8px;font-style:normal;font-weight:600;color:var(--teal)}
.au-ping{width:14px;height:14px;border-radius:50%;border:2px solid var(--teal);position:relative;flex-shrink:0}
.au-ping::after{content:"";position:absolute;inset:2px;border-radius:50%;background:var(--teal)}
/* heading + station plate */
.au-hdw{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:22px;align-items:end;border-bottom:2px solid var(--ink)}
.au-hdw .ax-hd{border-bottom:0}
.au-plate{background:var(--ink);color:#F3F1FA;border-radius:14px;padding:10px 14px 12px;margin-bottom:12px;min-width:280px}
.au-pl-top{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.au-pl-n{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--ink);background:var(--teal-l);padding:2px 7px;border-radius:8px}
.au-pl-top b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:22px;line-height:1}
.ax .au-pl-l{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));column-gap:8px}
.au-pl-l li{display:flex;flex-direction:column;align-items:flex-start;gap:5px;font-size:10.5px;line-height:1.2;color:#B9B5CF;min-width:0}
.au-pl-l i{width:16px;height:16px;border-radius:50%;border:2px dashed #8F8BAA}
.au-pl-l .is-done i{background:var(--teal-l);border:2px solid var(--teal-l)}.au-pl-l .is-at i{background:var(--gold);border:2px solid var(--gold);box-shadow:0 0 0 4px rgba(212,169,79,.3)}
.au-pl-l .is-at span{color:#fff;font-weight:700}
/* sheets: an instrument panel */
.au-sheet{position:relative;display:flex;flex-direction:column;background:var(--panel);border:2px solid var(--ink);border-radius:14px;overflow:hidden;box-shadow:0 8px 0 -2px rgba(37,35,58,.12)}
.au-sh-top{display:flex;align-items:center;gap:8px;background:var(--ink);color:#E4E1F5;padding:6px 14px}
.au-sh-top small{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.au-led{width:9px;height:9px;border-radius:50%;background:var(--gold);box-shadow:0 0 6px var(--gold)}
.au-sh-in{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr) minmax(0,.95fr);gap:12px 22px;padding:14px 16px 16px}
.au-sheet.one .au-sh-in{grid-template-columns:minmax(0,1.15fr) minmax(0,1fr)}
.au-sheet.bx-mob{display:none}
.au-sh-a{display:flex;flex-direction:column;gap:6px;align-items:flex-start;min-width:0}
.au-sh-a h3{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:30px;line-height:.95;color:var(--ink)}
.au-sh-a p{font-size:14px;line-height:1.5}
.au-hand{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:10px;background:var(--soft);font-size:12.5px;line-height:1.35}
.au-hand b{display:block;font-size:12.5px}.au-hand .ax-hand{width:56px;height:34px;flex-shrink:0}
.au-hand .ax-hand-m{fill:none;stroke:var(--teal);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}.au-hand .ax-hand-j{fill:var(--teal)}
.au-hand .ax-hand-p{fill:none;stroke:var(--gold-t);stroke-width:2.4;stroke-linecap:round}
.au-sh-dl{display:flex;flex-direction:column;gap:10px;min-width:0;border-left:1px dashed var(--off);padding-left:18px}
.au-ln{display:flex;flex-direction:column;gap:2px}.au-ln dt{font-size:11.5px;font-weight:600;color:var(--muted)}.au-ln dd{font-size:13.5px;line-height:1.4;overflow-wrap:anywhere}
.au-ln[data-state="outcome"] dd{color:var(--red);font-weight:600}.au-ln[data-state="target"] dd{color:var(--amber)}.au-ln[data-state="start"] dd{color:var(--teal);font-weight:600}
.au-sh-e{min-width:0;border-left:1px dashed var(--off);padding-left:18px}
.au-sheet .tl-field textarea{background:#fff}
/* sources, layered */
.au-so{display:flex;flex-direction:column;gap:12px}
.au-so .so-src{grid-template-columns:auto minmax(0,1fr)}
.au-sb{display:flex;flex-direction:column;align-items:flex-start;gap:2px;width:100%;text-align:left;font:inherit;color:var(--ink);background:none;border:0;padding:2px 4px;border-radius:8px}
.au-sb b{display:block;font-size:13px;font-weight:600;line-height:1.3}.au-sb>span:not(.ax-tag){display:block;font-size:12px;color:var(--muted);line-height:1.35;margin-bottom:4px}
.au-sb.tl-pick.is-up{transform:none;box-shadow:0 0 0 2.5px var(--gold)!important;background:#FFF8E6!important}
.au-so li.bx{margin:2px 0 6px}
.au-main{background:var(--ink)!important;border-color:var(--ink)!important;color:#F3F1FA}
.au-main .so-b b{color:#fff;font-size:14px}.au-main .so-b>span{color:#C9C5DD!important}
.au-mk{display:block;font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--teal-l)}
.au-main .so-track{background:#56527A}
/* brain, layered */
.au-br{display:flex;flex-direction:column;gap:12px}
.ax .au-days{display:grid;grid-template-columns:repeat(var(--np,5),minmax(0,1fr)) auto;gap:6px}
.au-pass{display:flex;flex-direction:column;min-width:0}
.au-day{width:100%;height:100%;font:inherit;color:var(--ink)}
.au-day.tl-pick.is-up{background:var(--ink)!important;color:#fff;box-shadow:0 0 0 2.5px var(--gold),0 7px 0 -1px rgba(37,35,58,.22)!important}
.au-day.tl-pick.is-up span{color:var(--teal-l)}
.au-play{align-self:stretch}
.ax[data-theme="bm"] .ax-brain-o,.ax[data-theme="bm"] .ax-brain-g{stroke:#8F86D6}
/* panel: the station panel */
.au-pn{display:flex;flex-direction:column;gap:12px}
.pn-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.pn-ph{display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:8px 12px;min-height:52px;text-align:left;font:inherit;color:var(--ink);background:var(--panel);border:1.5px solid var(--off);border-radius:12px;cursor:pointer}
.pn-ph small{font-size:10.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}.pn-ph b{font-size:13px;font-weight:600;line-height:1.3}
.pn-ph[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:#fff}.pn-ph[aria-pressed="true"] small{color:var(--teal-l)}
.pn-board{background:var(--ink);border-radius:16px;padding:14px 16px;color:#EDEBF7}
.ax .pn-mains{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
.pn-main{display:flex;align-items:center;gap:12px;padding:10px 12px;border:1.5px solid #4A4669;border-radius:12px;background:#2E2B47}
.pn-msw{width:26px;height:42px;border-radius:13px;border:2px solid #8F8BAA;position:relative;flex-shrink:0}
.pn-msw i{position:absolute;left:3px;bottom:3px;width:16px;height:16px;border-radius:50%;background:#8F8BAA;transition:bottom .3s,background .3s}
.pn-main.is-on .pn-msw{border-color:var(--teal-l)}.pn-main.is-on .pn-msw i{bottom:19px;background:var(--teal-l);box-shadow:0 0 8px var(--teal-l)}
.pn-main small{display:block;font-size:10px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--teal-l)}
.pn-main b{display:block;font-size:13.5px;font-weight:600;color:#fff}.pn-main em{display:block;font-style:normal;font-size:11.5px;color:#B9B5CF}
.pn-head{display:grid;grid-template-columns:minmax(0,1fr) 300px;font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#B9B5CF;padding:0 12px 6px}
.pn-heads{display:grid;grid-template-columns:repeat(4,1fr);text-align:center}
.ax .pn-rows{display:flex;flex-direction:column;gap:6px}
.pn-li{display:flex;flex-direction:column;min-width:0}
.pn-row{width:100%;display:grid;grid-template-columns:30px minmax(0,1fr) 300px;align-items:center;gap:10px;padding:10px 12px;text-align:left;font:inherit;color:#EDEBF7;background:#2E2B47;border:1.5px solid #3B3858;border-radius:12px;cursor:pointer}
.pn-row.tl-pick.is-up{background:#3B357A!important;box-shadow:0 0 0 2.5px var(--gold),0 7px 0 -1px rgba(0,0,0,.3)!important}
.pn-n{width:26px;height:26px;border-radius:50%;border:1.5px solid #B9B5CF;display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:700}
.pn-t b{display:block;font-size:13.5px;font-weight:600;color:#fff;line-height:1.3}.pn-t em{display:block;font-style:normal;font-size:11.5px;color:#C9C5DD;line-height:1.35}
.pn-lamps{display:grid;grid-template-columns:repeat(4,1fr);justify-items:center}
.pn-lamp{width:20px;height:20px;border-radius:50%;border:2px dashed #8F8BAA;transition:all .3s}
.pn-lamp.is-on{border:2px solid var(--teal-l);background:#6E63C9}
.pn-lamp.is-at{background:var(--teal-l);box-shadow:0 0 10px var(--teal-l)}
.pn-foot{display:flex;justify-content:space-between;gap:10px;margin-top:10px;padding-top:10px;border-top:1px solid #4A4669;font-size:12px;color:#C9C5DD}
.pn-count{color:var(--teal-l)}
.pn-read{font-size:13.5px;font-weight:600;padding:8px 12px;border-left:4px solid var(--gold);background:rgba(251,251,253,.7);border-radius:0 8px 8px 0}
.au-pn li.bx{margin:4px 0 8px}
.au-pn .au-sheet{color:var(--ink)}
/* effect: five looks */
.au-eff{display:flex;align-items:center;gap:20px;padding:18px 22px;border-radius:16px;background:var(--panel);border:2px solid var(--ink)}
.au-eff[data-state="outcome"]{border-color:var(--red)}.au-eff[data-state="target"]{border-color:var(--amber)}
.au-eff-sw{width:30px;height:48px;border-radius:15px;border:2.5px solid var(--ink);position:relative;flex-shrink:0}
.au-eff-sw i{position:absolute;left:4px;top:4px;width:17px;height:17px;border-radius:50%;background:var(--teal)}
.au-eff-b{display:flex;flex-direction:column;gap:5px;min-width:0}
.au-eff-v{font-family:'Bebas Neue',sans-serif;font-size:44px;line-height:.92}
.au-eff[data-state="outcome"] .au-eff-v{color:var(--red)}.au-eff[data-state="target"] .au-eff-v{color:var(--amber)}
.au-eff p{font-size:14px;line-height:1.45;max-width:62ch}
.au-eff-panel{background:var(--ink);border-color:var(--ink);color:#F3F1FA}.au-eff-panel .ax-label{color:var(--teal-l)}.au-eff-panel .au-eff-v{color:#fff!important}.au-eff-panel p{color:#D6D3E6}
.au-eff-panel .au-eff-sw{border-color:var(--teal-l)}.au-eff-panel .au-eff-sw i{background:var(--teal-l);top:auto;bottom:4px;box-shadow:0 0 8px var(--teal-l)}
.au-eff-meter{background:transparent;border:0;border-bottom:6px solid var(--ink);border-radius:0;padding:4px 0 14px}.au-eff-meter .au-eff-v{font-size:52px}
.au-eff-banner{background:var(--teal);border-color:var(--teal);color:#fff}.au-eff-banner .ax-label{color:#E4E0FF}.au-eff-banner .au-eff-v{color:#fff!important}.au-eff-banner p{color:#EEEBFF}.au-eff-banner .au-eff-sw{border-color:#fff}.au-eff-banner .au-eff-sw i{background:#fff}
.au-eff-ticket{border-style:dashed;border-radius:12px}
.au-eff-stamp{border:3px double var(--ink);border-radius:4px;transform:rotate(-.6deg)}
/* the three buttons */
.au-acts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:6px;padding-top:16px;border-top:2px solid var(--ink)}
.ax .au-act{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:3px;min-height:64px;padding:10px 16px;text-align:left;font:inherit;color:var(--ink);background:var(--panel);border:1.5px solid var(--ink);border-radius:12px;cursor:pointer}
.au-act-k{font-weight:600;font-size:15px}.au-act-d{font-size:12.5px;color:var(--muted);line-height:1.35}
.ax .au-act-go{background:var(--ink);color:#fff;box-shadow:inset 6px 0 0 var(--gold);padding-left:22px}.ax .au-act-go .au-act-d{color:inherit;opacity:.85}
.ax .au-act.is-said{outline:3px solid var(--gold);outline-offset:2px}
/* ---- phone ---- */
@container ax (max-width:699px){
 .ax[data-theme="bm"]{padding:18px 14px 26px}
 .au-hdw{grid-template-columns:minmax(0,1fr);gap:10px}.au-plate{min-width:0}
 .au-sheet.bx-mob{display:flex;margin-top:8px}.au-sheet.bx-mob[hidden]{display:none}
 .au-sh-in,.au-sheet.one .au-sh-in{grid-template-columns:minmax(0,1fr)}
 .au-sh-dl,.au-sh-e{border-left:0;padding-left:0;border-top:1px dashed var(--off);padding-top:12px}
 .au-sh-a h3{font-size:26px}
 .ax .au-days{grid-template-columns:minmax(0,1fr)}
 .au-day{height:auto}
 .pn-steps{grid-template-columns:minmax(0,1fr)}
 .ax .pn-mains{grid-template-columns:minmax(0,1fr)}
 .pn-head{grid-template-columns:minmax(0,1fr);padding:0 4px 6px}.pn-head>span:first-child{display:none}
 .pn-heads{font-size:9.5px}
 .pn-row{grid-template-columns:28px minmax(0,1fr);row-gap:10px}
 .pn-lamps{grid-column:1/-1}
 .pn-board{padding:12px}
 .au-eff{flex-direction:column;align-items:flex-start;gap:12px;padding:16px}.au-eff-v{font-size:38px}
 .au-acts{grid-template-columns:minmax(0,1fr);gap:10px}
}
'''
