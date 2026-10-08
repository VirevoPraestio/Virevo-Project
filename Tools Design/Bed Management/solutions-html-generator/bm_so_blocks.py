"""
bm_so_blocks — Bed Management Solutions drawings (drafts, 1 Oct 2026).

The Solutions motifs come from the block library (07 §1.3 "Show the thinking"): the lightbulb (an idea reached), the jigsaw
(parts that only work together), the route with its doors, the drafting sheet. Here they are drawn in Bed Management's
Solutions look (the fit-out: sage ground, green-slate ink, plan paper, gold = now) and carry the common tool layer:
the first item is raised with its sheet open, on a phone each sheet opens right under its item, every pickable item
is stacked one above the other on a phone, and every sheet can take an entry that is added to the chat message.

  heading   the library heading, with the door plate from the landing page (part n of 5, its four stops)
  circuit   the steps of a part as switches on one wire; the bulb at the end lights when the current reaches it
  jigsaw    the steps as pieces locked together; picking one outlines the pieces it relies on
  route     the library route: stations on a trail, then doors into the other parts (layered)
  effect    the quantity named, in five looks that change with the turn

register(G) is called by bm_solutions_html with its helpers (e, L, so, C).
"""
G = {}
def e(s): return G['e'](s)
def pt(o): return ' data-tj-point="%d"' % int(o['point']) if isinstance(o, dict) and o.get('point') is not None else ''
def pick(grp, key, first, cls=''): return G['L'].pick_attrs(grp, key, first, cls)
def hint(t): return '<p class="tl-hint so-hint"><span class="sx-pz-hand" aria-hidden="true"></span>%s</p>' % e(t)
def desk(boxes): return '<div class="bx-desk-wrap">%s</div>' % ''.join(boxes)
STAGES = ['Idea', 'Shaped', 'Tested with you', 'Agreed']

def register(helpers):
    G.update(helpers)
    return {'heading': r_heading, 'circuit': r_circuit, 'jigsaw': r_jigsaw, 'route': r_route, 'effect': r_effect}

# ------------------------------------------------------------------------------------------ the sheet (drafting sheet, both layouts)
def sheet(s, grp, first, where):
    L = G['L']; fill = '%s:%s' % (grp, s['key'])
    label = s.get('entry_label') or ('%s · %s' % (s['when'], s['title']))
    entry = L.entry(label, s['entry'], s.get('entry_hint', 'Type what happens at your hospital'), open_=s.get('entry_open', False), fill=fill) if s.get('entry') else ''
    lines = ''.join('<div class="so-ln" data-state="%s"><dt>%s</dt><dd>%s</dd></div>' % (e(x.get('state', 'plain')), e(x['label']), e(x['value'])) for x in s.get('lines', []))
    ask = L.say(s['ask']['label'], s['ask']['say'], 'so-ask') if s.get('ask') else ''
    tag = 'li' if where == 'mob-li' else 'div'; w = 'mob' if where.startswith('mob') else 'desk'
    return ('<%s class="bx bx-%s so-sheet%s" data-box="%s:%s"%s><div class="so-sh-a"><small>%s</small><h3>%s</h3><p>%s</p>%s</div>%s%s</%s>') % (
        tag, w, '' if entry else ' one', grp, e(s['key']), '' if first else ' hidden', e(s['when']), e(s['title']), e(s['text']), ask,
        '<dl class="so-sh-dl">%s</dl>' % lines if lines else '', '<div class="so-sh-e">%s</div>' % entry if entry else '', tag)

# ------------------------------------------------------------------------------------------ heading with the door plate
def r_heading(b, ctx):
    h = G['so'].r_heading(b)
    p = b.get('plate')
    if not p: return h
    at = STAGES.index(p['stage'])
    stops = ''.join('<li class="%s"><i></i><span>%s</span></li>' % ('is-done' if i < at else ('is-at' if i == at else ''), e(x)) for i, x in enumerate(STAGES))
    plate = ('<div class="so-plate" aria-label="%s, %s"><div class="so-pl-top"><span class="so-pl-n">Part %d of %d</span><span class="so-pl-name">%s</span></div>'
             '<ol class="so-pl-st">%s</ol></div>') % (e(p['name']), e(p['stage']), p['part'], p['of'], e(p['name']), stops)
    return '<div class="so-hdw">%s%s</div>' % (h, plate)

# ------------------------------------------------------------------------------------------ circuit: switches on one wire, a bulb at the end
SWITCH = ('<svg class="cc-sw" viewBox="0 0 44 22" aria-hidden="true"><circle class="cc-sw-a" cx="6" cy="15" r="3.4"/><circle class="cc-sw-b" cx="38" cy="15" r="3.4"/>'
          '<path class="cc-sw-off" d="M8.5 13.5 L33 3"/><path class="cc-sw-on" d="M8.5 15 H35.5"/></svg>')
PLUG = ('<svg class="cc-plug" viewBox="0 0 40 40" aria-hidden="true"><rect x="7" y="9" width="22" height="22" rx="4"/><path d="M29 20h9M2 15h5M2 25h5"/>'
        '<path class="cc-plug-z" d="M19 13l-4 8h6l-4 8"/></svg>')

def r_circuit(b, ctx):
    grp = ctx.uid('socc'); steps, sheets = b['steps'], b['sheets']; n = len(steps); cols = n // 2
    cells, boxes = [], []
    src = b['source']
    cells.append('<li class="cc-src" style="--r:1;--c:1">%s<b>%s</b><em>%s</em><span class="cc-w cc-w-r" data-w="0" aria-hidden="true"></span></li>' % (PLUG, e(src['label']), e(src['line'])))
    for i, s in enumerate(steps):
        sh = sheets[i]; first = i == 0
        if i < cols: r, c, w = 1, 2 + i, ('cc-w-r' if i < cols - 1 else 'cc-w-elbow')
        else: r, c, w = 2, 2 + (cols - 1 - (i - cols)), 'cc-w-l'
        state = s.get('state') or ('outcome' if i == n - 1 else 'plain')
        cells.append(('<li class="cc-cell" style="--r:%d;--c:%d" data-i="%d"><button type="button"%s data-state="%s"%s>%s<span class="cc-k">Step %d</span>'
                      '<span class="cc-when">%s</span><b>%s</b><em>%s</em></button><span class="cc-w %s" data-w="%d" aria-hidden="true"></span></li>') % (
            r, c, i + 1, pick(grp, sh['key'], first, 'cc-node'), e(state), pt(s), SWITCH, i + 1, e(s['when']), e(s['title']), e(s['line']), w, i + 1))
        cells.append(sheet(sh, grp, first, 'mob-li'))
        boxes.append(sheet(sh, grp, first, 'desk'))
    g = b['goal']
    bulb = G['so'].BULB.replace('class="sx-bulb"', 'class="sx-bulb cc-bulb"')
    cells.append('<li class="cc-goal" style="--r:2;--c:1">%s<b>%s</b><em>%s</em></li>' % (bulb, e(g['label']), e(g['line'])))
    return ('<section class="sx-block so-circuit" data-block="circuit" data-at="1" data-n="%d" style="--cols:%d">%s<div class="cc-wrap"><span class="cc-live" aria-hidden="true"></span>'
            '<ol class="cc-board">%s</ol></div><p class="cc-read" aria-live="polite"><b class="cc-read-n">Step 1 of %d</b> <span>%s</span></p>%s</section>') % (
        n, cols, hint(b.get('hint') or 'Pick a switch. The current runs to it, and the bulb lights at the last one.'), ''.join(cells), n, e(b['readout']), desk(boxes))

# ------------------------------------------------------------------------------------------ jigsaw: the steps as pieces that only work together
JG = {'w': {'w': 300, 'h': 172, 'K': 92}, 'n': {'w': 360, 'h': 140, 'K': 88}}
JG_M = 30

def r_jigsaw(b, ctx):
    so = G['so']; grp = ctx.uid('sojg'); ps, sheets = b['pieces'], b['sheets']; n = len(ps); cols = (n + 1) // 2
    names = {i + 1: p['title'] for i, p in enumerate(ps)}
    cells, boxes = [], []
    for i, p in enumerate(ps):
        sh = sheets[i]; first = i == 0
        r, c = (0, i) if i < cols else (1, i - cols)
        svgs = []
        for key, rows_, cols_, rr, cc in (('w', 2, cols, r, c), ('n', n, 1, i, 0)):
            d = JG[key]; W, H, K = d['w'], d['h'], d['K']
            path = so._piece_path(rr, cc, rows_, cols_, W, H, K)
            svgs.append('<svg class="jg-sv jg-sv-%s" viewBox="%.1f %.1f %d %d" style="left:%.3f%%;top:%.3f%%;width:%.3f%%;height:%.3f%%" aria-hidden="true"><path d="%s"/></svg>' % (
                key, cc * W - JG_M, rr * H - JG_M, W + 2 * JG_M, H + 2 * JG_M, -100.0 * JG_M / W, -100.0 * JG_M / H, 100.0 * (W + 2 * JG_M) / W, 100.0 * (H + 2 * JG_M) / H, path))
        last = i == n - 1
        bulb = so.BULB.replace('class="sx-bulb"', 'class="sx-bulb jg-bulb"') if last else ''
        rel = ','.join(str(x) for x in p.get('relies_on', []))
        cells.append(('<div class="jg-cell" style="--r:%d;--c:%d"><button type="button"%s data-rel="%s" data-n="%d" data-state="%s"%s>%s<span class="jg-face">%s<span class="jg-tx"><small>Piece %d · %s</small>'
                      '<b>%s</b><em>%s</em></span></span></button></div>') % (
            r + 1, c + 1, pick(grp, sh['key'], first, 'jg-p'), rel, i + 1, 'outcome' if last else 'plain', pt(p), ''.join(svgs), bulb, i + 1, e(p['when']), e(p['title']), e(p['line'])))
        if p.get('label'): cells[-1] = cells[-1].replace('<small>Piece %d · %s</small>' % (i + 1, e(p['when'])), '<small>%s</small>' % e(p['label']))
        rel_names = ', '.join('Piece %d, %s' % (x, names[x]) for x in p.get('relies_on', [])) or 'Nothing before it'
        sh2 = dict(sh); sh2['lines'] = [{'label': 'Relies on', 'value': rel_names, 'state': 'target'}] + list(sh.get('lines', []))
        cells.append(sheet(sh2, grp, first, 'mob'))
        boxes.append(sheet(sh2, grp, first, 'desk'))
    return ('<section class="sx-block so-jig" data-block="jigsaw" style="--cols:%d">%s<div class="jg-board">%s</div>'
            '<p class="jg-read"><span class="jg-key jg-key-up"></span>The piece you picked <span class="jg-key jg-key-rel"></span>The pieces it relies on</p>%s%s</section>') % (
        cols, hint(b.get('hint') or 'Pick a piece. The pieces it relies on are outlined.'), ''.join(cells), '<p class="sx-cond">%s</p>' % e(b['condition']) if b.get('condition') else '', desk(boxes))

# ------------------------------------------------------------------------------------------ route: the library's trail of stations and doors, with the layer
def r_route(b, ctx):
    grp = ctx.uid('sort'); st, sheets = b['steps'], b['sheets']; items, boxes = [], []
    for i, s in enumerate(st):
        sh = sheets[i]; first = i == 0
        items.append((('<li class="rt-muted">' if s.get('muted') else '<li>') + '<button type="button"%s%s><span class="rt-n">%d</span><span><small class="rt-when">%s</small><b>%s</b><em>%s</em></span></button>%s</li>') % (
            pick(grp, sh['key'], first, 'rt-s'), pt(s), i + 1, e(sh['when']), e(s['title']), e(s['what']), sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    f = b['fork']
    TK = {'Automations': 'au', 'Processes': 'pr'}
    doors = ''.join('<button type="button" class="rt-door rt-%s" data-say-lead data-text="%s"><span class="rt-tab">%s</span><b>%s</b><em>%s</em></button>' % (
        TK.get(o.get('tab'), 'so'), e(o['say']), e(('Opens ' + o['tab']) if o.get('tab') else o['tag']), e(o['label']), e(o['what'])) for o in f['options'])
    return ('<section class="sx-block sx-route so-route" data-block="route">%s<ol class="rt-line" style="--n:%d">%s</ol>%s'
            '<div class="rt-fork"><div class="rt-q"><span class="rt-bulb">%s</span><b>%s</b></div><div class="rt-doors">%s</div></div></section>') % (
        hint(b.get('hint') or 'Pick a station to open it.'), len(st), ''.join(items), desk(boxes), G['so'].BULB, e(f['question']), doors)

# ------------------------------------------------------------------------------------------ effect: the quantity named
EFFECT_STYLES = ['plate', 'stamp', 'ticket', 'banner', 'meter']
CLOCK = ('<svg class="so-eff-clock" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="22" r="15"/><path d="M20 12v10l7 4M15 4h10M20 4v3"/></svg>')

def r_effect(b, ctx):
    n = getattr(ctx, 'turn', 1); k = getattr(ctx, 'eff', 0); ctx.eff = k + 1
    style = b.get('look') or EFFECT_STYLES[(n + k + getattr(ctx, 'sample', 0)) % len(EFFECT_STYLES)]
    mark = '<span class="so-eff-mk" aria-hidden="true"><span class="bm-bed">%s</span>%s</span>' % (G['C'].bed_svg(30), CLOCK)
    return ('<section class="sx-block so-eff so-eff-%s" data-block="effect" data-state="%s">%s<div class="so-eff-b"><div class="sx-label">%s</div><div class="so-eff-v">%s</div>'
            '<p>%s</p></div></section>') % (style, e(b.get('state', 'plain')), mark, e(b['label']), e(b['value']), e(b['sub']))

# ------------------------------------------------------------------------------------------ what the drawings do beyond the layer
JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  /* circuit: the current runs from the plug to the picked switch; the bulb lights at the last one */
  $$('.so-circuit').forEach(function(c){
    var n=+c.getAttribute('data-n'),read=c.querySelector('.cc-read-n'),live=c.querySelector('.cc-live'),wrap=c.querySelector('.cc-wrap');
    function at(k){c.setAttribute('data-at',k);
      $$('.cc-cell',c).forEach(function(x){x.classList.toggle('is-on',+x.getAttribute('data-i')<=k);});
      $$('.cc-w',c).forEach(function(w){var i=+w.getAttribute('data-w');w.classList.toggle('is-live',i<k||(k===n&&i===n));});
      c.classList.toggle('cc-glow',k===n);read.textContent=k===n?'All '+n+' steps on. The bulb is lit.':'Step '+k+' of '+n;
      var node=c.querySelector('.cc-cell[data-i="'+k+'"] .cc-node');
      if(node&&live&&wrap){var R=wrap.getBoundingClientRect(),r=node.getBoundingClientRect();live.style.height=Math.max(0,(k===n?wrap.scrollHeight:r.top-R.top+r.height/2))+'px';}}
    $$('.cc-node',c).forEach(function(b){b.addEventListener('click',function(){at(+b.closest('.cc-cell').getAttribute('data-i'));});});
    at(1);window.addEventListener('resize',function(){at(+c.getAttribute('data-at'));});
    setTimeout(function(){at(+c.getAttribute('data-at'));},350);});
  /* jigsaw: the picked piece outlines the pieces it relies on */
  $$('.so-jig').forEach(function(j){
    function rel(p){var r=(p.getAttribute('data-rel')||'').split(',').filter(Boolean);
      $$('.jg-p',j).forEach(function(x){x.classList.toggle('is-rel',r.indexOf(x.getAttribute('data-n'))>=0);});}
    $$('.jg-p',j).forEach(function(p){p.addEventListener('click',function(){rel(p);});});
    var up=j.querySelector('.jg-p.is-up');if(up)rel(up);});
})();
'''

CSS = r'''
/* ---- Bed Management Solutions: the fit-out look on the library's drafting table ---- */
.sx[data-theme="bm"]{--ground:#E2EAE7;--sheet:#FAFCFB;--card:#FAFCFB;--ink:#173B38;--muted:#46605C;--line:#2C7266;--acc:#2C7266;--grid:rgba(23,59,56,.06);
  --gold:#d4a94f;--gold-t:#6B4F16;--amber:#8A5608;--green:#2F6B4F;--red:#8E2F1C;--faint:rgba(23,59,56,.40);--wire:#7F948F;--soft:#E7F0EC;padding:26px 34px 34px}
.sx[data-theme="bm"][data-tone="paper"]{--ground:#EFEEE6;--sheet:#FFFEF9;--card:#FFFEF9;--soft:#F1EFE4;--grid:rgba(23,59,56,.0);
  background-image:radial-gradient(rgba(23,59,56,.13) 1px,transparent 1.3px);background-size:20px 20px}
.sx .tj-lit{outline:4px solid var(--gold)!important;outline-offset:3px}
.sx .bm-bed svg .h{fill:var(--ink)}.sx .bm-bed svg .f{fill:var(--card);stroke:var(--ink);stroke-width:2.2}.sx .bm-bed svg .p{fill:var(--ground);stroke:var(--ink);stroke-width:1.4}.sx .bm-bed svg .k{fill:none}
.so-hint{display:flex;align-items:center;gap:8px;font-style:normal;font-weight:600;color:var(--line)}
/* heading + door plate (from the Solutions landing page: each fix a room, its plate carries four stops) */
.so-hdw{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:22px;align-items:end;border-bottom:1.5px solid var(--ink)}
.so-hdw .sx-hd{border-bottom:0}
.so-plate{background:var(--sheet);border:2px solid var(--ink);padding:10px 14px 12px;margin-bottom:12px;min-width:270px;box-shadow:5px 5px 0 rgba(23,59,56,.12)}
.so-pl-top{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.so-pl-n{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;background:var(--ink);color:var(--sheet);padding:2px 7px}
.so-pl-name{font-family:'Bebas Neue',sans-serif;font-size:22px;line-height:1}
.sx .so-pl-st{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));column-gap:8px;position:relative}
.so-pl-st::before{content:"";position:absolute;left:8px;right:12%;top:7px;border-top:2px solid var(--ink)}
.so-pl-st li{position:relative;display:flex;flex-direction:column;gap:5px;font-size:10.5px;min-width:0;color:var(--muted);line-height:1.2}
.so-pl-st i{width:15px;height:15px;border-radius:50%;border:2px solid var(--ink);background:var(--sheet)}
.so-pl-st .is-done i{background:var(--ink)}.so-pl-st .is-at i{background:var(--gold);box-shadow:0 0 0 4px rgba(212,169,79,.3)}.so-pl-st .is-at span{color:var(--ink);font-weight:700}
/* sheets: the drafting sheet */
.so-sheet{position:relative;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr) minmax(0,.95fr);gap:12px 22px;background:var(--sheet);border:1.5px solid var(--ink);border-top:5px solid var(--gold);padding:16px 18px 18px;box-shadow:6px 6px 0 rgba(23,59,56,.10)}
.so-sheet.one{grid-template-columns:minmax(0,1.15fr) minmax(0,1fr)}
.so-sheet.bx-mob{display:none}
.so-sheet::after{content:"";position:absolute;right:6px;bottom:6px;width:9px;height:9px;border-right:1.5px solid var(--line);border-bottom:1.5px solid var(--line)}
.so-sh-a{display:flex;flex-direction:column;gap:5px;align-items:flex-start;min-width:0}
.so-sh-a small{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--line)}
.so-sh-a h3{margin:0;font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:32px;line-height:.95;color:var(--ink)}
.so-sh-a p{font-size:14px;line-height:1.5;color:var(--ink)}
.so-sh-a .tl-say{margin-top:6px}
.so-sh-dl{display:flex;flex-direction:column;gap:10px;min-width:0;border-left:1px dashed var(--faint);padding-left:18px}
.so-ln{display:flex;flex-direction:column;gap:2px;min-width:0}
.so-ln dt{font-size:11.5px;font-weight:600;color:var(--muted)}.so-ln dd{font-size:13.5px;line-height:1.4;overflow-wrap:anywhere}
.so-ln[data-state="outcome"] dd{color:var(--red);font-weight:600}.so-ln[data-state="target"] dd{color:var(--amber)}.so-ln[data-state="start"] dd{color:var(--green);font-weight:600}
.so-sh-e{min-width:0;border-left:1px dashed var(--faint);padding-left:18px}
.so-sheet .tl-field textarea{background:#fff}
/* ---- circuit ---- */
.cc-wrap{position:relative}
.cc-live{display:none}
.sx .cc-board{display:grid;grid-template-columns:118px repeat(var(--cols),minmax(0,1fr));grid-auto-rows:1fr;column-gap:46px;row-gap:58px;padding:8px 26px 8px 0}
.cc-board>li{position:relative;min-width:0;grid-row:var(--r);grid-column:var(--c)}
.cc-board>li.bx{grid-row:auto;grid-column:1/-1}
.cc-src,.cc-goal{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;text-align:center;padding:8px 6px;border:2px dashed var(--faint);background:rgba(250,252,251,.6)}
.cc-src b,.cc-goal b{font-size:13px;font-weight:700;line-height:1.25}.cc-src em,.cc-goal em{font-style:normal;font-size:11.5px;line-height:1.35;color:var(--muted)}
.cc-plug{width:38px;height:38px}.cc-plug rect{fill:var(--sheet);stroke:var(--ink);stroke-width:2.4}.cc-plug path{fill:none;stroke:var(--ink);stroke-width:2.4;stroke-linecap:round}
.cc-plug .cc-plug-z{stroke:var(--gold);stroke-width:2.2;stroke-linejoin:round}
.cc-goal{border-color:var(--red);transition:background .35s,box-shadow .35s}
.cc-goal .sx-bulb{width:46px;height:56px}
.cc-goal .sx-glass{fill:#EEF0EE;transition:fill .35s}.cc-goal .sx-rays{opacity:.15;animation:none}
.so-circuit.cc-glow .cc-goal{background:#FBF1D2;border-style:solid;box-shadow:0 0 0 6px rgba(212,169,79,.25),0 0 34px 6px rgba(212,169,79,.45)}
.so-circuit.cc-glow .cc-goal .sx-glass{fill:#F6DE9A}.so-circuit.cc-glow .cc-goal .sx-rays{opacity:1;animation:sx-glow 2.8s ease-in-out infinite}
.cc-node{width:100%;height:100%;display:flex;flex-direction:column;align-items:flex-start;gap:4px;text-align:left;font:inherit;color:var(--ink);background:var(--sheet);border:2px solid var(--ink);padding:10px 12px 12px;border-radius:3px}
.cc-node[data-state="outcome"]{border-color:var(--red)}
.cc-sw{width:44px;height:22px;margin-bottom:2px}.cc-sw circle{fill:var(--sheet);stroke:var(--ink);stroke-width:2}
.cc-sw-off,.cc-sw-on{stroke:var(--ink);stroke-width:3;stroke-linecap:round;transition:opacity .2s}.cc-sw-on{opacity:0}
.cc-cell.is-on .cc-sw-off{opacity:0}.cc-cell.is-on .cc-sw-on{opacity:1;stroke:var(--gold-t)}.cc-cell.is-on .cc-sw circle{fill:var(--gold)}
.cc-k{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.cc-when{font-size:11.5px;font-weight:700;color:var(--line);background:var(--soft);padding:1px 8px;border-radius:9px}
.cc-node b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:25px;line-height:.95;margin-top:2px}
.cc-node em{font-style:normal;font-size:12.5px;line-height:1.4;color:var(--muted)}
.cc-node[data-state="outcome"] b{color:var(--red)}
.cc-w{position:absolute;top:50%;border:0 solid var(--wire);transition:border-color .25s,filter .25s}
.cc-w-r{left:100%;width:46px;border-top-width:3px;border-top-style:dashed}
.cc-src .cc-w-r{left:100%}
.cc-w-l{right:100%;width:46px;border-top-width:3px;border-top-style:dashed}
.cc-w-elbow{left:100%;width:26px;height:calc(100% + 58px);border-width:3px 3px 3px 0;border-style:dashed;border-radius:0 22px 22px 0}
.cc-w.is-live{border-color:var(--gold);border-style:solid;filter:drop-shadow(0 0 4px rgba(212,169,79,.8))}
.cc-read{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline;font-size:13.5px;line-height:1.45;color:var(--ink);padding:10px 14px;border-left:4px solid var(--gold);background:rgba(250,252,251,.7)}
.cc-read b{font-weight:700}
.so-circuit .bx-desk-wrap{margin-top:2px}
/* ---- jigsaw ---- */
.jg-board{display:grid;grid-template-columns:repeat(var(--cols),minmax(0,1fr));gap:0;padding:34px 34px 30px;margin:0 auto;width:100%;max-width:880px}
.jg-cell{position:relative;grid-row:var(--r);grid-column:var(--c);aspect-ratio:300/172}
.so-jig .bx-mob{grid-column:1/-1}
.jg-p{position:absolute;inset:0;width:100%;height:100%;padding:0;margin:0;border:0;background:none!important;font:inherit;color:var(--ink);text-align:left;box-shadow:none!important}
.jg-p.tl-pick.is-up{background:none!important;box-shadow:none!important;transform:translateY(-7px);z-index:4}
.jg-sv{position:absolute;overflow:visible;pointer-events:none}
.jg-sv path{fill:var(--sheet);stroke:var(--ink);stroke-width:2;transition:fill .2s,stroke .2s}
.jg-sv-n{display:none}
.jg-p:hover .jg-sv path{fill:#FFFFFF}
.jg-p.is-up .jg-sv path{fill:#FFF8E6;stroke:var(--gold-t);stroke-width:3.2;filter:drop-shadow(0 10px 10px rgba(23,59,56,.28))}
.jg-p.is-rel .jg-sv path{fill:#F4F1E2;stroke:var(--amber);stroke-width:2.6;stroke-dasharray:7 5}
.jg-p[data-state="outcome"] .jg-sv path{stroke:var(--red)}
.jg-face{position:absolute;inset:17% 12% 15%;display:flex;align-items:center;gap:10px;min-width:0}
.jg-tx{display:flex;flex-direction:column;gap:3px;min-width:0}
.jg-tx small{font-size:10.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--line)}
.jg-tx b{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:25px;line-height:.95}
.jg-tx em{font-style:normal;font-size:12.5px;line-height:1.35;color:var(--muted)}
.jg-p[data-state="outcome"] .jg-tx b{color:var(--red)}
.jg-bulb{width:34px;height:42px}.jg-bulb .sx-glass{fill:#EEF0EE}.jg-bulb .sx-rays{opacity:.15;animation:none}
.jg-p.is-up .jg-bulb .sx-glass{fill:#F6DE9A}.jg-p.is-up .jg-bulb .sx-rays{opacity:1;animation:sx-glow 2.8s ease-in-out infinite}
.jg-read{display:flex;flex-wrap:wrap;align-items:center;gap:6px 14px;font-size:12.5px;color:var(--muted)}
.jg-key{display:inline-block;width:22px;height:14px;border:2px solid var(--gold-t);background:#FFF8E6;margin-right:-6px}.jg-key-rel{border:2px dashed var(--amber);background:#F4F1E2}
.so-jig{display:flex;flex-direction:column;gap:12px}
/* ---- route, layered ---- */
.so-route{display:flex;flex-direction:column;gap:16px}
.so-route .rt-line>li{display:flex;flex-direction:column;min-width:0}
.so-route .rt-s.tl-pick,.so-route .rt-s.tl-pick.is-up{background:none!important;box-shadow:none!important;transform:none}
.so-route .rt-s.is-up .rt-n{background:var(--gold);transform:translateY(-4px);box-shadow:0 0 0 4px rgba(212,169,79,.35)}
.so-route .rt-s.is-up>span:last-child{background:#FFF8E6;border:2px solid var(--gold-t);transform:translateY(-5px);box-shadow:0 0 0 1px var(--gold),0 7px 0 -1px rgba(23,59,56,.2),0 16px 24px -8px rgba(23,59,56,.32)}
.so-route .rt-s>span:last-child{transition:transform .18s,box-shadow .18s}
.rt-when{font-size:10.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--line)}
.so-route .rt-line>li:last-child .rt-n{border-color:var(--red);color:var(--red)}
.so-route .rt-door{font:inherit}
.so-route .rt-muted .rt-s>span:last-child{background:#ECEFEC;border-color:var(--wire)}.so-route .rt-muted .rt-n{border-color:var(--wire);color:var(--muted);background:#ECEFEC}
.so-route .rt-muted .rt-s b{color:var(--muted)}
.rt-so .rt-tab{background:var(--soft);color:var(--line);border:1px solid var(--line)}
.so-route .rt-door.is-said{background:#FBF1D2;border-color:var(--gold-t)}
.so-route .rt-q .sx-bulb{width:40px;height:50px}
/* ---- effect: five looks ---- */
.so-eff{display:flex;align-items:center;gap:22px;padding:18px 24px;background:#EADFCF;border:2px solid var(--ink)}
.so-eff[data-state="outcome"]{border-color:var(--red)}
.so-eff-mk{display:flex;align-items:center;gap:6px;flex-shrink:0}
.so-eff-clock{width:36px;height:36px}.so-eff-clock circle{fill:var(--sheet);stroke:var(--red);stroke-width:2.6}.so-eff-clock path{fill:none;stroke:var(--red);stroke-width:2.6;stroke-linecap:round}
.so-eff-b{display:flex;flex-direction:column;gap:5px;min-width:0}
.so-eff-v{font-family:'Bebas Neue',sans-serif;font-size:46px;line-height:.92;color:var(--ink)}
.so-eff[data-state="outcome"] .so-eff-v{color:var(--red)}
.so-eff p{font-size:14px;line-height:1.45;color:var(--ink);max-width:62ch}
.so-eff-plate{background:var(--sheet);border-radius:40px 40px 4px 4px;box-shadow:6px 6px 0 rgba(23,59,56,.12);position:relative}
.so-eff-plate::before,.so-eff-plate::after{content:"";position:absolute;top:14px;width:7px;height:7px;border-radius:50%;background:var(--ink)}
.so-eff-plate::before{left:22px}.so-eff-plate::after{right:22px}
.so-eff-stamp{background:var(--sheet);border:3px double var(--ink);transform:rotate(-.7deg)}
.so-eff-stamp[data-state="outcome"]{border-color:var(--red)}
.so-eff-ticket{background:var(--sheet);border:2px dashed var(--ink);border-radius:12px}
.so-eff-ticket .so-eff-mk{border-right:2px dashed var(--muted);padding-right:18px}
.so-eff-banner{background:var(--ink);border-color:var(--ink)}
.so-eff-banner .sx-label{color:var(--gold)}.so-eff-banner p{color:#DCE6E2}.so-eff-banner .so-eff-v{color:#F4E7C6}.so-eff-banner[data-state="outcome"] .so-eff-v{color:#F4B9A8}
.so-eff-banner .bm-bed svg .f{fill:transparent;stroke:#F3F1EA}.so-eff-banner .bm-bed svg .h{fill:#F3F1EA}.so-eff-banner .so-eff-clock circle{fill:transparent;stroke:#F4B9A8}.so-eff-banner .so-eff-clock path{stroke:#F4B9A8}
.so-eff-meter{background:transparent;border:0;border-bottom:6px solid var(--ink);padding:4px 0 14px}
.so-eff-meter[data-state="outcome"]{border-bottom-color:var(--red)}.so-eff-meter .so-eff-v{font-size:54px}
/* ---- phone: one column, every pickable item stacked, each sheet right under its item ---- */
@container sx (max-width:699px){
 .sx[data-theme="bm"]{padding:18px 14px 26px}
 .so-hdw{grid-template-columns:minmax(0,1fr);gap:10px}
 .so-plate{min-width:0;margin-bottom:14px}
 .so-sheet.bx-mob{display:grid}
 .so-sheet.bx-mob[hidden]{display:none}
 .so-sheet,.so-sheet.one{grid-template-columns:minmax(0,1fr);gap:12px;padding:14px 14px 16px;margin-top:8px}
 .so-sheet{isolation:isolate}
 .so-sheet::before{content:"";position:absolute;left:26px;top:-13px;width:15px;height:15px;background:var(--gold);transform:rotate(45deg);z-index:-1}
 .so-sh-dl,.so-sh-e{border-left:0;padding-left:0;border-top:1px dashed var(--faint);padding-top:12px}
 .so-sh-a h3{font-size:28px}
 .sx .cc-board{grid-template-columns:minmax(0,1fr);grid-auto-rows:auto;row-gap:12px;padding:0 0 0 34px}
 .cc-board>li{grid-row:auto;grid-column:auto}
 .cc-w{display:none}
 .cc-wrap::before{content:"";position:absolute;left:13px;top:24px;bottom:30px;border-left:3px dashed var(--wire)}
 .cc-live{display:block;position:absolute;left:13px;top:24px;width:0;border-left:3px solid var(--gold);filter:drop-shadow(0 0 4px rgba(212,169,79,.8));transition:height .3s;max-height:calc(100% - 54px)}
 .cc-cell::before{content:"";position:absolute;left:-28px;top:22px;width:13px;height:13px;border-radius:50%;background:var(--sheet);border:2.5px solid var(--ink);z-index:1}
 .cc-cell.is-on::before{background:var(--gold)}
 .cc-src,.cc-goal{flex-direction:row;justify-content:flex-start;text-align:left;gap:12px;padding:10px 12px}
 .cc-src>b,.cc-goal>b{flex:0 0 auto;max-width:42%}
 .cc-node b{font-size:24px}
 .jg-board{grid-template-columns:minmax(0,1fr);padding:30px 26px 26px}
 .jg-cell{grid-row:auto;grid-column:auto;aspect-ratio:360/140}
 .jg-sv-w{display:none}.jg-sv-n{display:block}
 .jg-face{inset:21% 11% 27%}
 .so-jig .bx-mob{margin:34px 0 34px}
 .so-route .rt-line>li{flex-direction:column}
 .so-eff{flex-direction:column;align-items:flex-start;gap:12px;padding:16px}
 .so-eff-plate::before,.so-eff-plate::after{top:12px}
 .so-eff-v{font-size:38px}.so-eff-meter .so-eff-v{font-size:44px}
 .so-eff-ticket .so-eff-mk{border-right:0;padding-right:0}
}
@media (prefers-reduced-motion:reduce){.jg-p.is-up{transform:none}.cc-live{transition:none}}
'''
