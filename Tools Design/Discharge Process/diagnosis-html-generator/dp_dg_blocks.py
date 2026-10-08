"""
dp_dg_blocks — Discharge Process's own Diagnosis drawings (drafts, 5 Oct 2026).

  ward-map   the road to going home as a ward floor plan: each stop a room on one winding path, walked in order.
             The stop asked now is ink, the next is gold-edged, the rest wait. Each room opens its sheet with
             what the hospital usually hears and the question Tojo will ask there.          (dp-dg-01)

Drawn in the Discharge Diagnosis look (sage ground, forest ink, gold = now) through the page's colour variables.
Both layouts from one markup: four rooms to a row on a desktop, the path snaking left to right then back;
on a phone the rooms stack one above the other on one spine, each sheet right under its room.
register(G) is called by dp_diagnosis_html with the generator's helpers (sheet, pick_attrs, L, dh).
"""
G = {}
def e(s): return G['dh'].e(s)
def pt(o): return G['dh'].pt(o)
def pick(grp, key, first, cls=''): return G['pick_attrs'](grp, key, first, cls)
def sheet(sh, grp, first, where): return G['sheet'](sh, grp, first, where)
def desk(boxes): return '<div class="bx-desk-wrap">%s</div>' % ''.join(boxes)

def register(helpers):
    G.update(helpers)
    return {'ward-map': r_ward_map}

DOORSIGN = ('<svg viewBox="0 0 26 30" width="22" height="26" aria-hidden="true"><rect x="3" y="2" width="20" height="26" rx="2" fill="none" stroke="currentColor" stroke-width="2.2"/>'
            '<circle cx="17" cy="16" r="1.8" fill="currentColor"/></svg>')
STATUS = {'now': 'Asking now', 'next': 'Next', 'later': 'Later', 'done': 'Walked'}

def r_ward_map(b, ctx):
    grp = ctx.uid('dpwm'); stops, sheets = b['stops'], b['sheets']; n = len(stops); cols = 4
    rows = (n + cols - 1) // cols
    cells, boxes, pts = [], [], []
    for i, s in enumerate(stops):
        sh = sheets[i]; first = i == 0
        r, c = i // cols, i % cols
        if r % 2: c = cols - 1 - c
        pts.append('%.2f,%.2f' % ((c + .5) * 100.0 / cols, (r + .5) * 100.0 / rows))
        cells.append(('<li class="wm-cell" style="grid-row:%d;grid-column:%d"><button type="button"%s data-status="%s"%s>'
                      '<span class="wm-no">%s</span><span class="wm-st">%s</span><b class="wm-name">%s</b>%s</button>%s</li>') % (
            r + 1, c + 1, pick(grp, sh['key'], first, 'wm-room'), e(s.get('status', 'later')), pt(s), e(s.get('tag') or chr(65 + i)), e(STATUS[s.get('status', 'later')]),
            e(s['name']), '<span class="wm-heard">%s</span>' % e(s['heard']) if s.get('heard') else '', sheet(sh, grp, first, 'mob')))
        boxes.append(sheet(sh, grp, first, 'desk'))
    path = ('<svg class="wm-path" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline points="%s"/></svg>') % ' '.join(pts)
    return ('<section class="tj-block dp-wm" data-block="ward-map"><div class="wm-ends"><span class="wm-end wm-start">%s<b>%s</b></span>'
            '<span class="wm-count"><b>%d</b> stops, one team each</span><span class="wm-end wm-fin">%s<b>%s</b></span></div>'
            '<div class="wm-plan"><div class="wm-floor" style="--rows:%d">%s<ol class="wm-rooms" style="grid-template-rows:repeat(%d,auto)">%s</ol></div></div>%s%s%s</section>') % (
        DOORSIGN, e(b['start_label']), n, G['bedmark']('next', 26), e(b['end_label']), rows, path, rows, ''.join(cells),
        G['L'].hint(b.get('hint') or 'Tap a room to see what I will ask there.'), desk(boxes), G['dh'].divider(b.get('caption')))

CSS = r'''
/* ---- ward-map: the road to going home, as rooms on one winding path ---- */
.dp-wm{display:flex;flex-direction:column;gap:14px}
.wm-ends{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.wm-end{display:inline-flex;align-items:center;gap:8px;font-size:13px;color:var(--ink)}.wm-end b{font-weight:600}
.wm-count{font-size:12.5px;color:var(--muted)}.wm-count b{font-family:var(--f-display);font-size:24px;font-weight:400;color:var(--ink);vertical-align:-3px;margin-right:2px}
.wm-plan{background:var(--card);border:2px solid var(--ink);border-radius:4px;padding:16px;box-shadow:8px 8px 0 var(--shadow);
  background-image:linear-gradient(var(--faint) 1px,transparent 1px),linear-gradient(90deg,var(--faint) 1px,transparent 1px);background-size:26px 26px}
.wm-floor{position:relative}
.wm-path{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}
.wm-path polyline{fill:none;stroke:var(--ink);stroke-width:4;stroke-dasharray:2 9;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;opacity:.55}
.wm-rooms{position:relative;list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px 26px}
.wm-cell{display:flex;flex-direction:column;min-width:0}
.wm-room{position:relative;display:grid;grid-template-columns:auto minmax(0,1fr);grid-template-rows:auto auto auto;column-gap:10px;row-gap:3px;align-items:start;width:100%;min-height:112px;
  padding:12px 12px 12px 10px;text-align:left;font:inherit;color:var(--ink);background:var(--ground);border:2px solid var(--ink);border-radius:6px}
.wm-room::before{content:"";position:absolute;left:-2px;right:-2px;top:-8px;height:6px;border:2px solid var(--ink);border-bottom:0;border-radius:6px 6px 0 0;background:var(--card)}
.wm-no{grid-row:1/4;width:32px;height:32px;border-radius:50%;border:3px solid var(--ink);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;background:var(--card)}
.wm-st{font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.wm-name{font-size:14px;line-height:1.25}
.wm-heard{font-size:12px;line-height:1.35;color:var(--muted);font-style:italic}
.wm-room[data-status="now"] .wm-no{background:var(--ink);color:var(--gold)}
.wm-room[data-status="now"] .wm-st{color:var(--ink)}
.wm-room[data-status="next"]{border-color:var(--gold-text)}.wm-room[data-status="next"] .wm-no{border-color:var(--gold);background:#FFF8E6}
.wm-room[data-status="later"]{background:var(--card);border-style:dashed}.wm-room[data-status="later"] .wm-name{color:var(--muted)}.wm-room[data-status="later"]::before{border-style:dashed}
.wm-room[data-status="later"] .wm-no{border-width:2px;color:var(--muted)}
.wm-room[data-status="done"] .wm-no{background:var(--green);border-color:var(--green);color:#fff}
.dp-wm .bx-desk-wrap .bm-sheet{margin-top:4px}
@container tj (max-width:699px){
 .wm-plan{padding:12px 10px;box-shadow:5px 5px 0 var(--shadow)}
 .wm-path{display:none}
 .wm-rooms{grid-template-columns:minmax(0,1fr)!important;grid-template-rows:none!important;gap:12px;position:relative}
 .wm-rooms::before{content:"";position:absolute;left:25px;top:8px;bottom:8px;border-left:4px dotted var(--ink);opacity:.5}
 .wm-cell{grid-row:auto!important;grid-column:1!important}
 .wm-room{min-height:0}
 .wm-ends{flex-direction:column;align-items:flex-start;gap:6px}
}
'''
