"""
dp_au_blocks — Discharge Process's own Automations drawing (draft, 5 Oct 2026).

  file   the going-home file: each paper the patient needs to leave (the summary, the bill, the insurance request,
         the medicines, the supplies going back), drawn as a sheet on the desk. Switch between today, when every
         paper starts after the morning signature, and with the automation, when each one has filled in by the
         time the doctor signs. A person's hand marks the papers someone says yes to. Each paper opens its sheet.
                                                                                                  (dp-au-01)
Drawn in the Discharge Automations look (the switch room: steel ground, charcoal ink, teal = running by itself)
through the library's automations.css variables. On a phone the papers stack one above the other, each sheet
right under its paper. register(G) is called by dp_automations_html with the generator's helpers.
"""
G = {}
def e(s): return G['e'](s)
def pt(o): return ' data-tj-point="%d"' % int(o['point']) if isinstance(o, dict) and o.get('point') is not None else ''

def register(helpers):
    G.update(helpers)
    return {'file': r_file}

def r_file(b, ctx):
    B = G['B']; au = G['au']
    grp = ctx.uid('aufl'); docs, items, boxes = b['docs'], [], []
    for i, d in enumerate(docs):
        s = b['sheets'][i]; first = i == 0
        items.append(('<li class="fl-cell"><button type="button"%s%s style="--tilt:%.1fdeg"><span class="fl-paper%s"><span class="fl-fold" aria-hidden="true"></span>'
                      '<span class="fl-no">%d</span><b class="fl-t">%s</b><span class="fl-lines" aria-hidden="true"><i></i><i></i><i></i><i></i></span>'
                      '<span class="fl-stamp fl-today"><small>Today</small>%s<em>%s</em></span><span class="fl-stamp fl-with"><small>With it</small>%s<em>%s</em></span>%s</span></button>%s</li>') % (
            B.pick(grp, s['key'], first, 'fl-doc'), pt(d), (-1.6 if i % 2 else 1.4), ' has-hand' if d.get('hand') else '', i + 1, e(d['title']), e(d['at_today']), e(d['today']), e(d['at_with']), e(d['with']),
            '<span class="fl-hand" title="A person says yes here">%s</span>' % au.HAND if d.get('hand') else '', B.sheet(s, grp, first, 'mob-li')))
        boxes.append(B.sheet(s, grp, first, 'desk'))
    sw = b['switch']
    return ('<section class="ax-block au-fl" data-block="file" data-state="today">%s<div class="fl-bar"><div class="fl-switch" role="group" aria-label="Which day">'
            '<button type="button" data-state="today" aria-pressed="true">%s</button><button type="button" data-state="with" aria-pressed="false">%s</button></div>'
            '<p class="fl-cap" aria-live="polite"><span class="fl-c-today">%s</span><span class="fl-c-with">%s</span></p></div>'
            '<div class="fl-desk"><div class="fl-tab"><span class="ax-label">%s</span><span class="fl-key"><i class="k-hand">%s</i>%s</span></div><ol class="fl-docs" style="--n:%d">%s</ol></div>%s%s</section>') % (
        B.hint(b.get('hint') or 'Switch between today and with the automation. Pick a paper to open it.'), e(sw['today']), e(sw['with']), e(sw['cap_today']), e(sw['cap_with']),
        e(b['label']), au.HAND, e(b.get('hand_key', 'A person says yes')), len(docs), ''.join(items),
        '<p class="ax-cond">%s</p>' % e(b['condition']) if b.get('condition') else '', B.desk(boxes))

JS = r'''
(function(){
  var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s));};
  $$('.au-fl').forEach(function(f){$$('.fl-switch button',f).forEach(function(b){b.addEventListener('click',function(){f.setAttribute('data-state',b.getAttribute('data-state'));
    $$('.fl-switch button',f).forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});});});});
})();
'''

CSS = r'''
/* ---- file: the going-home file, paper by paper ---- */
.au-fl{display:flex;flex-direction:column;gap:14px}
.fl-bar{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.fl-switch{display:inline-flex;background:var(--panel);border:1.5px solid var(--ink);border-radius:22px;padding:3px;gap:2px}
.ax .fl-switch button{border:0;background:transparent;border-radius:18px;font-size:13px;font-weight:600;padding:0 16px;min-height:36px;color:var(--ink)}
.ax .fl-switch button[aria-pressed=true]{background:var(--ink);color:var(--panel)}
.fl-cap{flex:1 1 280px;margin:0;font-size:13px;line-height:1.45;color:var(--muted)}
.au-fl[data-state=today] .fl-c-with,.au-fl[data-state=with] .fl-c-today{display:none}
.fl-desk{background:var(--screen);border-radius:14px;padding:16px 18px 22px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.06)}
.fl-tab{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.fl-tab .ax-label{color:var(--teal-l)}
.fl-key{display:inline-flex;align-items:center;gap:8px;font-size:12px;color:#C9D6DB}.fl-key .ax-hand{width:34px;height:22px}
.fl-docs{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:14px}
.fl-cell{display:flex;flex-direction:column;min-width:0}
.ax .fl-doc{display:block;width:100%;padding:0;border:0;background:transparent;font:inherit;color:var(--ink);text-align:left;border-radius:6px}
.fl-paper{position:relative;display:flex;flex-direction:column;gap:8px;min-height:208px;padding:14px 12px 12px;background:var(--panel);border-radius:4px;
  box-shadow:0 2px 0 rgba(0,0,0,.25),0 10px 18px -8px rgba(0,0,0,.5);clip-path:polygon(0 0,calc(100% - 18px) 0,100% 18px,100% 100%,0 100%)}
.fl-fold{position:absolute;right:0;top:0;width:18px;height:18px;background:linear-gradient(225deg,transparent 50%,#C9D2D8 50%)}
.ax .fl-doc{transform:rotate(var(--tilt))}.ax .fl-doc.tl-pick.is-up{transform:translateY(-5px)}.ax .fl-doc.tl-pick:not(.is-up):hover{transform:rotate(var(--tilt)) translateY(-2px)}
.fl-paper.has-hand .fl-t{padding-right:40px}
.fl-no{width:24px;height:24px;border-radius:50%;border:2px solid var(--ink);display:flex;align-items:center;justify-content:center;font-size:11.5px;font-weight:700}
.fl-t{font-size:13.5px;line-height:1.25}
.fl-lines{display:flex;flex-direction:column;gap:6px;margin:2px 0 4px}
.fl-lines i{display:block;height:3px;border-radius:2px;border-top:2px dashed var(--off);opacity:.7}
.fl-lines i:nth-child(2){width:86%}.fl-lines i:nth-child(3){width:92%}.fl-lines i:nth-child(4){width:60%}
.au-fl[data-state=with] .fl-lines i{border-top:0;height:4px;background:var(--teal);opacity:.85;transition:width .5s}
.fl-stamp{display:flex;flex-direction:column;gap:1px;margin-top:auto;padding:6px 8px;border:1.5px dashed var(--off);border-radius:4px;font-size:12px;line-height:1.3}
.fl-stamp small{font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.fl-stamp em{font-style:normal;color:var(--muted);font-size:11.5px}
.fl-stamp{font-family:'Bebas Neue',sans-serif;font-size:21px;line-height:1}
.fl-stamp small,.fl-stamp em{font-family:'Poppins',sans-serif;line-height:1.3}
.fl-today{color:var(--red)}
.fl-with{display:none;border-style:solid;border-color:var(--teal);color:var(--teal);background:rgba(15,110,107,.07)}
.au-fl[data-state=with] .fl-today{display:none}.au-fl[data-state=with] .fl-with{display:flex}
.fl-hand{position:absolute;right:8px;top:30px}.fl-hand .ax-hand{width:38px;height:24px}
.ax .fl-docs li.bx{margin:6px 0 8px}
@container ax (max-width:699px){
 .fl-desk{padding:12px 10px 14px}
 .fl-docs{grid-template-columns:minmax(0,1fr)!important;gap:10px}
 .ax .fl-doc,.ax .fl-doc.tl-pick.is-up{transform:none}
 .fl-paper{min-height:0;display:grid;grid-template-columns:24px minmax(0,1fr) auto;grid-template-areas:"no t t" "st st st";column-gap:10px;row-gap:8px;clip-path:none}
 .fl-no{grid-area:no}.fl-t{grid-area:t;align-self:center;padding-right:40px}.fl-lines{display:none}
 .fl-stamp{grid-area:st;margin:0}
 .fl-fold{display:none}
}
'''
