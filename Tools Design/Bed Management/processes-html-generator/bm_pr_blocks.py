"""
bm_pr_blocks — Bed Management's own Processes drawings (drafts, 6 Oct 2026).

Five new drawings for the Processes place, in the look of the approved Processes landing page (B, the trial ward:
pale clay, deep brown, rust, pill buttons). Each carries the common tool layer: the first item raised with its sheet
open, on a phone each sheet right under its item and every pickable item stacked, entries typed in the drawing added
to the chat message.

  day-dial     the ward's day on a wall clock, 8 AM to 8 PM: today's admission window against the new one,
               and the fixed times of the new day; picking a time moves the clock hand         (bm-pr-01)
  ward-pins    the trial ward seen from above, each change pinned in the room where it happens  (bm-pr-02)
  round-cards  the doctor's round: a card per patient with the predicted date to confirm or change (bm-pr-04)
  slip         the OPD prescription, its fields pulled into the bed plan                         (bm-pr-06)
  clipboard    what we need from you to start, typed straight into the drawing                    (bm-pr-11)

Classes carry their own prefixes (yd, yw, yr, yp, yk) so they never meet the other drawings in this place.
Colours come from the canvas variables. register(G) is called by bm_processes_html with the generator's helpers
(e, L, B = bm_so_blocks for the sheets).
"""
import math

G = {}
def e(s): return G['e'](s)
def pt(o): return ' data-tj-point="%d"' % int(o['point']) if isinstance(o, dict) and o.get('point') is not None else ''
def pick(grp, key, first, cls=''): return G['L'].pick_attrs(grp, key, first, cls)
def sheet(s, grp, first, where): return G['B'].sheet(s, grp, first, where)
def desk(boxes): return '<div class="bx-desk-wrap">%s</div>' % ''.join(boxes)
PIN = '<svg class="yh-pin" viewBox="0 0 16 20" aria-hidden="true"><path d="M8 19s6-6.2 6-11A6 6 0 002 8c0 4.8 6 11 6 11z"/><circle cx="8" cy="8" r="2.3"/></svg>'
def hint(t): return '<p class="tl-hint so-hint"><span class="yh-hs" aria-hidden="true">%s</span>%s</p>' % (PIN, e(t))
def cond(t): return '<p class="sx-cond so-cap">%s</p>' % e(t) if t else ''

def register(helpers):
    G.update(helpers)
    return {'day-dial': r_dial, 'ward-pins': r_ward, 'round-cards': r_round, 'slip': r_slip, 'clipboard': r_clip}

def hrs(t):
    h, m = [int(x) for x in t.split(':')]; return h + m / 60.0
def clk(t):
    v = hrs(t) if isinstance(t, str) else t; hh = int(v); mm = int(round((v - hh) * 60))
    if (hh, mm) == (12, 0): return 'noon'
    return '%d%s %s' % (hh % 12 or 12, ':%02d' % mm if mm else '', 'AM' if hh < 12 else 'PM')
def deg(t):
    v = hrs(t) if isinstance(t, str) else t; return (v % 12) * 30.0           # 0 = twelve o'clock, clockwise

# ------------------------------------------------------------------------------------------ day-dial: the ward's day on a wall clock
def r_dial(b, ctx):
    grp = ctx.uid('prdd'); C0, R = 150, 132
    def P(a, r): a = math.radians(a - 90); return C0 + r * math.cos(a), C0 + r * math.sin(a)
    def arc(t0, t1, r):
        a0, a1 = deg(t0), deg(t1)
        if a1 <= a0: a1 += 360
        (x0, y0), (x1, y1) = P(a0, r), P(a1, r)
        return 'M%.1f %.1f A%d %d 0 %d 1 %.1f %.1f' % (x0, y0, r, r, 1 if a1 - a0 > 180 else 0, x1, y1)
    nums = ''.join('<text x="%.1f" y="%.1f" class="yd-num">%d</text>' % (P(h * 30, 98)[0], P(h * 30, 98)[1] + 5, h or 12) for h in range(12))
    ticks = ''.join('<path class="yd-tk%s" d="M%.1f %.1fL%.1f %.1f"/>' % ((' yd-tk-h' if m % 5 == 0 else ''), *P(m * 6, 116 if m % 5 else 110), *P(m * 6, 121)) for m in range(60))
    arcs = ''
    for w in b['windows']:
        arcs += '<path class="yd-arc yd-%s" data-state="%s" d="%s"/>' % (e(w['side']), e(w.get('state', 'plain')), arc(w['from'], w['to'], R - (16 if w.get('inner') else 0)))
    keys = ''.join('<span class="yd-key yd-key-%s"><i data-state="%s"></i><b>%s</b> %s to %s</span>' % (
        e(w['side']), e(w.get('state', 'plain')), e(w['label']), e(clk(w['from'])), e(clk(w['to']))) for w in b['windows'])
    rows, boxes, marks = [], [], []
    for i, m in enumerate(b['times']):
        s = b['sheets'][i]; first = i == 0
        x, y = P(deg(m['at']), 80)
        marks.append('<g class="yd-mk%s" data-cur-for="%s:%s"><circle cx="%.1f" cy="%.1f" r="11"/><text x="%.1f" y="%.1f">%d</text></g>' % (' is-cur' if first else '', grp, e(s['key']), x, y, x, y + 4, i + 1))
        rows.append('<li><button type="button"%s data-deg="%.1f"%s><span class="yd-n">%d</span><span class="yd-at">%s</span><span class="yd-tx"><b>%s</b><em>%s</em></span>%s</button>%s</li>' % (
            pick(grp, s['key'], first, 'yd-row'), deg(m['at']), pt(m), i + 1, e(clk(m['at'])), e(m['name']), e(m['who']),
            '<span class="yh-new">New</span>' if m.get('new') else '', sheet(s, grp, first, 'mob-li')))
        boxes.append(sheet(s, grp, first, 'desk'))
    sw = b['switch']; a0 = deg(b['times'][0]['at'])
    face = ('<svg viewBox="0 0 300 300" class="yd-svg" aria-hidden="true"><circle class="yd-rim" cx="150" cy="150" r="146"/><circle class="yd-face" cx="150" cy="150" r="139"/>'
            '%s%s%s%s<g class="yd-hand" style="transform:rotate(%.1fdeg)"><path d="M150 150L150 66"/><circle cx="150" cy="66" r="4"/></g><circle class="yd-hub" cx="150" cy="150" r="7"/></svg>') % (
        ticks, arcs, nums, ''.join(marks), a0)
    return ('<section class="sx-block px-x yd" data-block="day-dial" data-state="today">%s<div class="yd-bar"><div class="xh-seg" role="group" aria-label="Which day">'
            '<button type="button" data-s="today" aria-pressed="true">%s</button><button type="button" data-s="with" aria-pressed="false">%s</button></div>'
            '<p class="yd-cap" aria-live="polite"><span class="yd-c-today">%s</span><span class="yd-c-with">%s</span></p></div>'
            '<div class="yd-grid"><div class="yd-clock"><div class="yd-dial">%s<span class="yd-span">%s</span></div><div class="yd-keys">%s</div></div>'
            '<div class="yd-side"><span class="sx-label">%s</span><ol class="yd-list">%s</ol></div></div>%s%s</section>') % (
        hint(b.get('hint') or 'Pick a time to move the clock hand. Switch between today and the new day.'), e(sw['today']), e(sw['with']), e(sw['cap_today']), e(sw['cap_with']),
        face, e(b.get('span', '8 AM to 8 PM')), keys, e(b['times_label']), ''.join(rows), cond(b.get('caption')), desk(boxes))

# ------------------------------------------------------------------------------------------ ward-pins: the trial ward from above
def r_ward(b, ctx):
    grp = ctx.uid('prwp'); rooms = b['rooms']; pins = {}
    for i, c in enumerate(b['changes']): pins.setdefault(c['room'], []).append((i, c))
    cells = []
    for j, r in enumerate(rooms):
        ps = ''.join('<span class="yw-pin%s" data-cur-for="%s:%s">%s<b>%d</b></span>' % (' is-cur' if i == 0 else '', grp, e(b['sheets'][i]['key']), PIN, i + 1) for i, c in pins.get(j + 1, []))
        beds = ''.join('<i></i>' for _ in range(r.get('beds', 0)))
        cells.append('<div class="yw-room yw-%s" style="grid-area:%s"><span class="yw-rn">%s</span>%s<span class="yw-pins">%s</span></div>' % (
            e(r.get('kind', 'room')), e(r['area']), e(r['name']), '<span class="yw-beds">%s</span>' % beds if beds else '', ps))
    rows, boxes = [], []
    for i, c in enumerate(b['changes']):
        s = b['sheets'][i]; first = i == 0
        rows.append('<li><button type="button"%s%s><span class="yw-no">%s<b>%d</b></span><span class="yw-tx"><b>%s</b><em>%s · %s</em></span></button>%s</li>' % (
            pick(grp, s['key'], first, 'yw-row'), pt(c), PIN, i + 1, e(c['name']), e(rooms[c['room'] - 1]['name']), e(c['who']), sheet(s, grp, first, 'mob-li')))
        boxes.append(sheet(s, grp, first, 'desk'))
    return ('<section class="sx-block px-x yw" data-block="ward-pins">%s<div class="yw-grid"><div class="yw-planw"><div class="yw-plan" style="grid-template-areas:%s">%s'
            '<div class="yw-corr" style="grid-area:c"><span>%s</span></div></div><p class="yw-cap">%s</p></div>'
            '<div class="yw-side"><span class="sx-label">%s</span><ol class="yw-list">%s</ol></div></div><p class="xh-rule">%s</p>%s</section>') % (
        hint(b.get('hint') or 'Pick a change to see its pin on the ward.'), e(' '.join('"%s"' % x for x in b['layout'])), ''.join(cells), e(b.get('corridor', 'Corridor')),
        e(b['plan_label']), e(b['changes_label']), ''.join(rows), e(b['rule']), desk(boxes))

# ------------------------------------------------------------------------------------------ round-cards: the doctor's round
def r_round(b, ctx):
    grp = ctx.uid('prrc'); L = G['L']; cards, boxes = [], []
    for i, p in enumerate(b['patients']):
        s = b['sheets'][i]; first = i == 0
        pct = max(4, min(100, 100.0 * p['day'] / p['of']))
        cards.append(('<li class="yr-li"><article class="yr-card" data-st="open"><button type="button"%s%s><span class="yr-bed">%s</span><span class="yr-what"><b>%s</b><em>%s</em></span>'
                      '<span class="yr-stay"><span class="yr-bar"><i style="width:%.1f%%"></i></span><small>Day %d of about %d</small></span></button>'
                      '<div class="yr-date"><span class="sx-label">%s</span><b>%s</b><small>%s</small></div>'
                      '<div class="yr-acts"><button type="button" class="xh-pill yr-ok" aria-pressed="false">%s</button><button type="button" class="xh-pill yr-ch" aria-pressed="false">%s</button></div>'
                      '<div class="yr-new" hidden>%s</div><span class="yr-stamp" aria-hidden="true">%s</span></article>%s</li>') % (
            pick(grp, s['key'], first, 'yr-head'), pt(p), e(p['bed']), e(p['what']), e(p['doctor']), pct, p['day'], p['of'], e(b['predicted_label']), e(p['predicted']), e(p['basis']),
            e(b['confirm']), e(b['change']), L.inline('Bed %s · new date' % p['bed'], 'Type the date you expect', grp), e(b['stamp']), sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    return ('<section class="sx-block px-x yr" data-block="round-cards">%s<div class="yr-top"><div class="yr-mic"><span class="yr-mi" aria-hidden="true">'
            '<svg viewBox="0 0 20 20"><rect x="7" y="2" width="6" height="10" rx="3"/><path d="M4 9a6 6 0 0012 0M10 15v3"/></svg></span><span><b>%s</b> %s</span></div>'
            '<span class="yr-count" aria-live="polite"><b>0</b> of %d confirmed</span></div><ol class="yr-grid">%s</ol><p class="xh-rule">%s</p>%s%s</section>') % (
        hint(b.get('hint') or 'Pick a patient to see where the date comes from. Confirm it, or change it.'), e(b['round_label']), e(b['round_line']), len(b['patients']),
        ''.join(cards), e(b['rule']), cond(b.get('caption')), desk(boxes))

# ------------------------------------------------------------------------------------------ slip: the OPD prescription, pulled into the bed plan
def r_slip(b, ctx):
    grp = ctx.uid('prsl'); rows, boxes, plan = [], [], []
    for i, f in enumerate(b['fields']):
        s = b['sheets'][i]; first = i == 0
        rows.append('<li><button type="button"%s data-f="%d"%s><span class="yp-l">%s</span><span class="yp-v"><mark>%s</mark></span><span class="yp-to">%s</span></button>%s</li>' % (
            pick(grp, s['key'], first, 'yp-row'), i, pt(f), e(f['label']), e(f['value']), e(f['feeds']), sheet(s, grp, first, 'mob-li')))
        boxes.append(sheet(s, grp, first, 'desk'))
        plan.append('<li data-f="%d" class="%s" data-cur-for="%s:%s"><span>%s</span><b>%s</b></li>' % (i, 'is-cur' if first else '', grp, e(s['key']), e(f['feeds']), e(f['value'])))
    p = b['plan']
    return ('<section class="sx-block px-x yp" data-block="slip" data-pulled="0">%s<div class="yp-grid"><div class="yp-paper"><div class="yp-head"><b>%s</b><span>%s</span></div>'
            '<div class="yp-rx" aria-hidden="true">Rx</div><ol class="yp-fields">%s</ol><div class="yp-sign"><span>%s</span></div></div>'
            '<div class="yp-mid"><button type="button" class="xh-play yp-pull"><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M2 7h9M8 3l4 4-4 4"/></svg><span>%s</span></button></div>'
            '<div class="yp-plan"><div class="yp-ph"><span class="sx-label">%s</span><b>%s</b></div><ol class="yp-pl">%s</ol>'
            '<div class="yp-bed"><span>%s</span><b>%s</b><em>%s</em></div></div></div><p class="xh-rule">%s</p>%s%s</section>') % (
        hint(b.get('hint') or 'Pick a line of the slip to see what it feeds. Press the button to pull it into the bed plan.'), e(b['slip_title']), e(b['slip_sub']), ''.join(rows), e(b['slip_foot']),
        e(b['pull']), e(p['label']), e(p['title']), ''.join(plan), e(p['bed_label']), e(p['bed']), e(p['bed_note']), e(b['rule']), cond(b.get('caption')), desk(boxes))

# ------------------------------------------------------------------------------------------ clipboard: what we need from you, typed in
def r_clip(b, ctx):
    grp = ctx.uid('prck'); L = G['L']; items, boxes = [], []
    for i, a in enumerate(b['asks']):
        s = b['sheets'][i]; first = i == 0
        items.append('<li class="yk-li"><div role="button" tabindex="0"%s%s><span class="yk-box" aria-hidden="true"></span><span class="yk-tx"><b>%s</b><em>%s</em></span>%s</div>%s</li>' % (
            pick(grp, s['key'], first, 'yk-row'), pt(a), e(a['title']), e(a['who']), L.inline(a['title'], a['placeholder'], grp), sheet(s, grp, first, 'mob')))
        boxes.append(sheet(s, grp, first, 'desk'))
    have = ''.join('<li><svg class="xh-tick" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7"/></svg><span>%s</span></li>' % e(h) for h in b.get('have', []))
    return ('<section class="sx-block px-x yk" data-block="clipboard">%s<div class="yk-board"><div class="yk-clip" aria-hidden="true"></div><div class="yk-head"><b>%s</b><span>%s</span></div>'
            '<ol class="yk-list">%s</ol><p class="yk-count"><span class="sx-label">%s</span> <b data-count-for="%s" data-waiting="%s" data-done="%s">%s</b></p></div>'
            '%s%s%s</section>') % (
        hint(b.get('hint') or 'Type a rough answer on each line. Leave a line empty if you do not know yet.'), e(b['title']), e(b['sub']), ''.join(items),
        e(b.get('count_label', 'Lines filled')), grp, e(b.get('waiting', 'None filled yet')), e(b.get('done', 'All in. Send to Tojo.')), e(b.get('waiting', 'None filled yet')),
        ('<div class="yk-have"><span class="sx-label">%s</span><ul>%s</ul></div>' % (e(b['have_label']), have)) if have else '', cond(b.get('caption')), desk(boxes))

# ============================================================================================== behaviour beyond the layer
JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  var reduce=false;try{reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  function seg(root,attr,fn){$$('.xh-seg button['+attr+']',root).forEach(function(b){b.addEventListener('click',function(){
    $$('button',b.parentNode).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});fn(b.getAttribute(attr));});});}
  /* day-dial: today or the new day; picking a time turns the clock hand */
  $$('.yd').forEach(function(d){var hand=d.querySelector('.yd-hand');
    seg(d,'data-s',function(s){d.setAttribute('data-state',s);});
    $$('.yd-row',d).forEach(function(r){r.addEventListener('click',function(){hand.style.transform='rotate('+r.getAttribute('data-deg')+'deg)';});});});
  /* round-cards: confirm or change each predicted date */
  $$('.yr').forEach(function(rc){var cards=$$('.yr-card',rc);
    function upd(){rc.querySelector('.yr-count b').textContent=cards.filter(function(c){return c.getAttribute('data-st')==='ok';}).length;}
    cards.forEach(function(c){var ok=c.querySelector('.yr-ok'),ch=c.querySelector('.yr-ch'),nw=c.querySelector('.yr-new');
      ok.addEventListener('click',function(){var on=c.getAttribute('data-st')!=='ok';c.setAttribute('data-st',on?'ok':'open');ok.setAttribute('aria-pressed',on?'true':'false');ch.setAttribute('aria-pressed','false');nw.hidden=true;upd();});
      ch.addEventListener('click',function(){var on=c.getAttribute('data-st')!=='ch';c.setAttribute('data-st',on?'ch':'open');ch.setAttribute('aria-pressed',on?'true':'false');ok.setAttribute('aria-pressed','false');nw.hidden=!on;
        if(on){var i=nw.querySelector('input');if(i)i.focus();}upd();});});});
  /* slip: pull each line into the bed plan, one after another */
  $$('.yp').forEach(function(sl){var btn=sl.querySelector('.yp-pull'),lis=$$('.yp-pl li',sl),n=lis.length;
    btn.addEventListener('click',function(){var done=+sl.getAttribute('data-pulled')>=n;
      if(done){sl.setAttribute('data-pulled',0);sl.classList.remove('is-full');lis.forEach(function(l){l.classList.remove('is-in');});btn.querySelector('span').textContent=btn.getAttribute('data-l0');return;}
      lis.forEach(function(l,i){setTimeout(function(){l.classList.add('is-in');sl.setAttribute('data-pulled',i+1);if(i===n-1){btn.querySelector('span').textContent='Start again';sl.classList.add('is-full');}},reduce?0:i*260);});});
    btn.setAttribute('data-l0',btn.querySelector('span').textContent);});
  /* clipboard: tick each line as it is filled */
  $$('.yk').forEach(function(k){$$('.yk-li',k).forEach(function(li){var i=li.querySelector('.tl-inline');if(!i)return;
    i.addEventListener('input',function(){li.classList.toggle('is-in',!!i.value.trim());});});});
})();
'''

CSS = r'''
/* ---- marks shared by the trial ward drawings ---- */
.yh-pin{width:15px;height:19px;flex-shrink:0}.yh-pin path{fill:var(--plum)}.yh-pin circle{fill:#fff}
.yh-hs{display:inline-flex}.so-hint .yh-pin{width:13px;height:16px}
.yh-new{font-size:10.5px;font-weight:700;padding:1px 8px;border-radius:10px;background:var(--plum);color:#fff;white-space:nowrap;align-self:center}
/* ---- day-dial ---- */
.yd-bar{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center}
.yd-cap{font-size:13.5px;font-weight:500;margin:0;flex:1;min-width:220px}.yd-c-with{display:none}
.yd[data-state="with"] .yd-c-today{display:none}.yd[data-state="with"] .yd-c-with{display:inline}
.yd-grid{display:grid;grid-template-columns:minmax(260px,340px) minmax(0,1fr);gap:22px;align-items:start}
.yd-clock{display:flex;flex-direction:column;gap:10px;align-items:center}
.yd-dial{position:relative;width:100%;max-width:330px}
.yd-svg{width:100%;height:auto;display:block}
.yd-rim{fill:var(--ink)}.yd-face{fill:var(--board)}
.yd-tk{stroke:var(--off);stroke-width:1}.yd-tk-h{stroke:var(--ink);stroke-width:2.4}
.yd-num{font-family:'Bebas Neue',sans-serif;font-size:21px;text-anchor:middle;fill:var(--ink)}
.yd-arc{fill:none;stroke-width:12;stroke-linecap:round;transition:opacity .35s}
.yd-arc[data-state="outcome"]{stroke:var(--red)}.yd-arc[data-state="start"]{stroke:var(--green)}.yd-arc[data-state="target"]{stroke:var(--gold)}.yd-arc[data-state="plain"]{stroke:var(--off)}
.yd[data-state="today"] .yd-with,.yd[data-state="with"] .yd-today{opacity:0}
.yd-mk circle{fill:#fff;stroke:var(--plum);stroke-width:2;transition:fill .2s}.yd-mk text{font-size:11.5px;font-weight:700;text-anchor:middle;fill:var(--plum)}
.yd-mk.is-cur circle{fill:var(--plum)}.yd-mk.is-cur text{fill:#fff}
.yd[data-state="today"] .yd-mk{opacity:.35}
.yd-hand{transform-origin:150px 150px;transition:transform .6s cubic-bezier(.5,1.6,.5,1)}.yd-hand path{stroke:var(--ink);stroke-width:5;stroke-linecap:round}.yd-hand circle{fill:var(--gold)}
.yd-hub{fill:var(--gold);stroke:var(--ink);stroke-width:2}
.yd-span{position:absolute;left:50%;top:63%;transform:translateX(-50%);font-size:11px;font-weight:600;color:var(--muted);white-space:nowrap;background:var(--board);padding:0 6px}
.yd-keys{display:flex;flex-direction:column;gap:5px;width:100%;max-width:330px}
.yd-key{font-size:12.5px;display:flex;align-items:center;gap:8px;transition:opacity .3s}.yd-key i{width:22px;height:8px;border-radius:4px;flex-shrink:0;background:var(--off)}
.yd-key i[data-state="outcome"]{background:var(--red)}.yd-key i[data-state="start"]{background:var(--green)}.yd-key i[data-state="target"]{background:var(--gold)}
.yd[data-state="today"] .yd-key-with,.yd[data-state="with"] .yd-key-today{opacity:.38}
.yd-side{display:flex;flex-direction:column;gap:8px;min-width:0}
.yd-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px}
.sx .yd-row{width:100%;display:grid;grid-template-columns:30px 66px minmax(0,1fr) auto;gap:10px;align-items:center;text-align:left;background:var(--board);border:1.5px solid var(--ink);border-radius:26px;padding:6px 14px 6px 6px;font:inherit;color:var(--ink);cursor:pointer;min-height:48px}
.yd-n{width:30px;height:30px;border-radius:50%;background:var(--plum);color:#fff;font-weight:700;font-size:13px;display:flex;align-items:center;justify-content:center}
.yd-at{font-family:'Bebas Neue',sans-serif;font-size:21px;line-height:1}
.yd-tx{display:flex;flex-direction:column;min-width:0}.yd-tx b{font-size:14px;font-weight:600}.yd-tx em{font-style:normal;font-size:12px;color:var(--muted)}
@container sx (max-width:699px){.yd-grid{grid-template-columns:1fr}.yd-dial{max-width:280px}.sx .yd-row{grid-template-columns:30px 54px minmax(0,1fr);row-gap:4px}.yd-row .yh-new{grid-column:3;justify-self:start}}
/* ---- ward-pins ---- */
.yw-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:22px;align-items:start}
.yw-planw{display:flex;flex-direction:column;gap:8px}
.yw-plan{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-rows:auto;gap:0;background:var(--ink);border:4px solid var(--ink);border-radius:8px;padding:4px;row-gap:4px;column-gap:4px}
.yw-room{position:relative;min-height:92px;background:var(--board);padding:8px 9px;display:flex;flex-direction:column;gap:6px;min-width:0}
.yw-room.yw-desk{background:var(--soft)}.yw-room.yw-office{background:var(--soft)}
.yw-rn{font-size:12px;font-weight:700;line-height:1.2}
.yw-beds{display:flex;flex-wrap:wrap;gap:4px}.yw-beds i{width:15px;height:24px;border:1.5px solid var(--muted);border-radius:3px;background:#fff}
.yw-pins{display:flex;flex-wrap:wrap;gap:4px;margin-top:auto}
.yw-pin{display:inline-flex;align-items:center;gap:2px;padding:2px 7px 2px 4px;border-radius:12px;border:1.5px solid var(--plum);background:#fff;transition:transform .2s,background .2s}
.yw-pin b{font-size:11.5px;color:var(--plum)}
.yw-pin.is-cur{background:var(--plum);transform:translateY(-3px) scale(1.12);box-shadow:0 4px 0 rgba(58,37,34,.25)}.yw-pin.is-cur b{color:#fff}.yw-pin.is-cur .yh-pin path{fill:#fff}.yw-pin.is-cur .yh-pin circle{fill:var(--plum)}
.yw-corr{background:repeating-linear-gradient(90deg,var(--wash) 0 18px,var(--board) 18px 36px);display:flex;align-items:center;justify-content:center;min-height:34px}
.yw-corr span{font-size:11px;font-weight:600;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
.yw-cap{font-size:12px;color:var(--muted);margin:0}
.yw-side{display:flex;flex-direction:column;gap:8px;min-width:0}
.yw-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px}
.sx .yw-row{width:100%;display:flex;align-items:center;gap:10px;text-align:left;background:var(--board);border:1.5px solid var(--ink);border-radius:12px;padding:8px 12px;font:inherit;color:var(--ink);cursor:pointer;min-height:48px}
.yw-no{display:inline-flex;align-items:center;gap:2px;flex-shrink:0}.yw-no b{font-size:13px;color:var(--plum)}
.yw-tx{display:flex;flex-direction:column;min-width:0}.yw-tx b{font-size:14px;font-weight:600}.yw-tx em{font-style:normal;font-size:12px;color:var(--muted)}
@container sx (max-width:699px){.yw-grid{grid-template-columns:1fr}.yw-room{min-height:78px}.yw-rn{font-size:11px}.yw-beds i{width:11px;height:18px}}
/* ---- round-cards ---- */
.yr-top{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between}
.yr-mic{display:flex;align-items:center;gap:10px;font-size:13.5px}.yr-mic b{font-weight:600}
.yr-mi{width:34px;height:34px;border-radius:50%;background:var(--ink);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.yr-mi svg{width:18px;height:18px}.yr-mi rect{fill:var(--gold)}.yr-mi path{fill:none;stroke:#fff;stroke-width:1.8;stroke-linecap:round}
.yr-count{font-size:13px;font-weight:600;background:var(--board);border:1.5px solid var(--ink);border-radius:20px;padding:6px 14px}.yr-count b{color:var(--plum);font-size:15px}
.yr-grid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.yr-li{display:flex;flex-direction:column;gap:8px}
.yr-card{position:relative;background:var(--board);border:1.5px solid var(--ink);border-radius:14px;padding:6px 6px 12px;display:flex;flex-direction:column;gap:10px;box-shadow:0 5px 0 rgba(58,37,34,.12);height:100%;transition:background .25s}
.sx .yr-head{width:100%;display:flex;flex-direction:column;gap:6px;text-align:left;background:transparent;border:0;border-radius:10px;padding:8px;font:inherit;color:var(--ink);cursor:pointer}
.yr-bed{align-self:flex-start;font-family:'Bebas Neue',sans-serif;font-size:20px;line-height:1;background:var(--ink);color:#fff;border-radius:6px;padding:4px 9px 2px}
.yr-what{display:flex;flex-direction:column}.yr-what b{font-size:14.5px;font-weight:600}.yr-what em{font-style:normal;font-size:12px;color:var(--muted)}
.yr-stay{display:flex;flex-direction:column;gap:3px}.yr-stay small{font-size:11.5px;color:var(--muted)}
.yr-bar{height:8px;border-radius:4px;background:var(--wash);border:1px solid var(--pxline);overflow:hidden}.yr-bar i{display:block;height:100%;background:var(--plum)}
.yr-date{margin:0 8px;padding:8px 10px;border:2px dashed var(--plum);border-radius:10px;background:#fff;display:flex;flex-direction:column;gap:2px}
.yr-date b{font-family:'Bebas Neue',sans-serif;font-size:24px;line-height:1;color:var(--plum)}.yr-date small{font-size:11.5px;color:var(--muted)}
.yr-acts{display:flex;gap:8px;padding:0 8px;flex-wrap:wrap}.sx .yr-acts .xh-pill{flex:1;min-height:40px;padding:0 10px}
.sx .yr-ok[aria-pressed=true]{background:var(--green);border-color:var(--green);color:#fff}
.sx .yr-ch[aria-pressed=true]{background:var(--gold);border-color:var(--gold);color:var(--ink)}
.yr-new{padding:0 8px}.sx .yr .tl-inline{width:100%;min-height:40px;font:inherit;font-size:13px;border:2px dashed var(--gold-t);border-radius:8px;background:#fff;color:var(--ink);padding:0 10px}
.yr-stamp{position:absolute;right:12px;top:12px;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--green);border:2px solid var(--green);border-radius:6px;padding:2px 7px;transform:rotate(-8deg) scale(.6);opacity:0;transition:all .25s;background:#fff}
.yr-card[data-st="ok"]{background:#F1F6F1}.yr-card[data-st="ok"] .yr-stamp{opacity:1;transform:rotate(-8deg) scale(1)}
.yr-card[data-st="ok"] .yr-date{border-style:solid;border-color:var(--green)}.yr-card[data-st="ok"] .yr-date b{color:var(--green)}
@container sx (max-width:820px){.yr-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@container sx (max-width:699px){.yr-grid{grid-template-columns:1fr}}
/* ---- slip ---- */
.yp-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);grid-template-areas:'paper mid' 'paper plan';grid-template-rows:auto 1fr;gap:12px 18px;align-items:start}
.yp-paper{grid-area:paper}.yp-mid{grid-area:mid}.yp-plan{grid-area:plan}
.yp-paper{position:relative;background:#fff;border:1.5px solid var(--pxline);border-radius:4px;padding:16px 18px 14px 44px;box-shadow:6px 6px 0 rgba(58,37,34,.10);
  background-image:linear-gradient(90deg,transparent 30px,rgba(140,75,63,.35) 30px,rgba(140,75,63,.35) 31.5px,transparent 31.5px)}
.yp-head{display:flex;flex-direction:column;gap:2px;border-bottom:2px solid var(--ink);padding-bottom:8px;margin-bottom:8px}.yp-head b{font-size:15px}.yp-head span{font-size:12px;color:var(--muted)}
.yp-rx{position:absolute;left:8px;top:14px;font-family:'Bebas Neue',sans-serif;font-size:22px;color:var(--plum)}
.yp-fields{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.sx .yp-row{width:100%;display:grid;grid-template-columns:112px minmax(0,1fr);gap:2px 10px;text-align:left;background:transparent;border:0;border-bottom:1px dashed var(--pxline);border-radius:6px;padding:7px 8px;font:inherit;color:var(--ink);cursor:pointer;min-height:44px;align-items:center}
.yp-l{font-size:12px;color:var(--muted)}
.yp-v{font-family:'Caveat','Segoe Print',cursive;font-size:19px;line-height:1.15}
.yp-v mark{background:linear-gradient(transparent 55%,rgba(212,169,79,.55) 55%);color:var(--ink);padding:0 2px}
.yp-to{grid-column:2;font-size:11px;color:var(--plum);font-weight:600}
.yp-sign{margin-top:10px;text-align:right}.yp-sign span{font-family:'Caveat','Segoe Print',cursive;font-size:18px;border-top:1px solid var(--muted);padding:2px 10px 0}
.yp-mid{display:flex;justify-content:flex-start}
.yp-pull svg path{fill:none;stroke:var(--gold);stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.yp-plan{background:var(--board);border:2px solid var(--ink);border-radius:14px;padding:12px 14px;display:flex;flex-direction:column;gap:10px;box-shadow:0 6px 0 rgba(58,37,34,.12)}
.yp-ph{display:flex;flex-direction:column;gap:2px}.yp-ph b{font-size:15px}
.yp-pl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:5px}
.yp-pl li{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;padding:6px 9px;border-radius:8px;border:1.5px dashed var(--pxline);background:var(--wash);transition:all .3s}
.yp-pl li b{opacity:0;transition:opacity .3s;text-align:right}.yp-pl li span{color:var(--muted)}
.yp-pl li.is-in{border-style:solid;border-color:var(--plum);background:#fff}.yp-pl li.is-in b{opacity:1}
.yp-pl li.is-cur{box-shadow:0 0 0 3px var(--gold)}
.yp-bed{display:flex;flex-direction:column;gap:2px;padding:10px 12px;border-radius:10px;background:#fff;border:2px dashed var(--off);transition:all .3s}
.yp-bed span{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}.yp-bed b{font-family:'Bebas Neue',sans-serif;font-size:28px;line-height:1;color:var(--off)}.yp-bed em{font-style:normal;font-size:12px;color:var(--muted)}
.yp.is-full .yp-bed{background:var(--ink);border:2px solid var(--ink)}.yp.is-full .yp-bed span{color:#E6D6D1}.yp.is-full .yp-bed b{color:var(--gold)}.yp.is-full .yp-bed em{color:#EFE4E0}
@container sx (max-width:760px){.yp-grid{grid-template-columns:1fr;grid-template-areas:'paper' 'mid' 'plan';grid-template-rows:auto}}
@container sx (max-width:699px){.yp-paper{padding-left:40px}.sx .yp-row{grid-template-columns:1fr}.yp-to{grid-column:1}}
/* ---- clipboard ---- */
.yk-board{position:relative;background:#fff;border:2px solid var(--ink);border-radius:10px;padding:26px 18px 16px;box-shadow:0 0 0 10px #B68B5E,0 12px 0 10px rgba(58,37,34,.18);margin:14px 10px 18px}
.yk-clip{position:absolute;left:50%;top:-22px;width:120px;height:34px;transform:translateX(-50%);background:linear-gradient(#9AA0A6,#6E747A);border-radius:8px 8px 12px 12px;border:2px solid var(--ink)}
.yk-head{display:flex;flex-direction:column;gap:2px;margin-bottom:10px}.yk-head b{font-family:'Bebas Neue',sans-serif;font-size:28px;line-height:1}.yk-head span{font-size:13px;color:var(--muted)}
.yk-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
.yk-li{border-top:1px solid var(--pxline)}.yk-li:last-child{border-bottom:1px solid var(--pxline)}
.sx .yk-row{display:grid;grid-template-columns:26px minmax(0,1fr) minmax(170px,240px);gap:12px;align-items:center;padding:10px 6px;border-radius:8px;cursor:pointer;color:var(--ink)}
.yk-box{width:22px;height:22px;border:2px solid var(--ink);border-radius:4px;background:#fff;position:relative}
.yk-li.is-in .yk-box{background:var(--green);border-color:var(--green)}.yk-li.is-in .yk-box:after{content:'';position:absolute;left:6px;top:2px;width:6px;height:11px;border:solid #fff;border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}
.yk-tx{display:flex;flex-direction:column;min-width:0}.yk-tx b{font-size:14.5px;font-weight:600}.yk-tx em{font-style:normal;font-size:12px;color:var(--muted)}
.sx .yk .tl-inline{width:100%;min-height:40px;font:inherit;font-size:13px;border:2px dashed var(--plum);border-radius:8px;background:#fff;color:var(--ink);padding:0 10px}
.yk-count{margin:10px 0 0;font-size:13px}.yk-count b{color:var(--plum)}
.yk-have{display:flex;flex-direction:column;gap:6px}.yk-have ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.yk-have li{display:flex;align-items:center;gap:6px;font-size:13px;background:var(--board);border:1.5px solid var(--green);border-radius:18px;padding:5px 12px}
@container sx (max-width:699px){.yk-board{margin:14px 6px 18px;padding:24px 12px 14px}.sx .yk-row{grid-template-columns:26px minmax(0,1fr)}.yk-row .tl-inline{grid-column:1 / -1}}
'''
