"""
Supply Chain and Procurement: the home page, round two (8 Oct 2026, for review).

Avishek's feedback on A, B, C: keep C's clean design and colours, keep the notebook of A and the
receipt of B, and do not change the Virevo type at all. So all three here use the Virevo fonts and
type scale (07 §2) through the V skin, and the Financial identity lives in shapes, paper, marks,
frame dress and drawings:

  report sheet   flat planes, heavy rules, numbered sections, a hard lime block when raised (from C)
  ledger paper   ruled lines, a double margin, double rules under totals (from A)
  receipt        torn zigzag edges, dashed tear lines, dotted leaders (from B)

  D  The clean ledger      receipt for the month's money; the work as lines in a ledger book;
                           what Tojo still has to do on ruled paper.
  E  Receipts on the rail  the month's account on ruled paper with a double-ruled total; one
                           receipt per part of the work, clipped to a black rail.
  F  The notebook          the month's receipt stapled on; the work in an open notebook, the parts
                           on the left page and the open part's steps on the right page.

The words are the same as round one (landing.py DATA). Run:  python3 landing2.py  ->  out/landing/
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sc_common as C
from sc_common import e, ico, ICONS, CHEV, sel, sel_cls, box, pt, tag, say_btn, standing, section, pending, actions, STAMP, MARK
from skins import SKINS
from landing import DATA, STEP, STATUS, counts, prog, place_detail, OUT, KICK, THEMES as T1

def segs(p, cls='sg'):
    return ''.join('<i class="%s s-%s"></i>' % (cls, s) for _, s in p['steps']) or '<i class="%s s-empty"></i>' % cls

def frac(p):
    d, n = counts(p)
    return ('%d/%d' % (d, n)) if n else '—'

def emb():
    return '<span class="bm-emb">%s</span>' % ico(MARK, 'var(--hi)', 28)

def receipt(m, cls, staple=False):
    """The month's money as a till receipt (from B), in Virevo type."""
    if not m:
        return '<aside class="v-rc is-empty %s"><b class="v-rch">This month</b><p>Prints once a month of supplier bills is in.</p></aside>' % cls
    lines = ''.join('<div class="v-l"><span>%s</span><i aria-hidden="true"></i><b>%s</b></div>' % (e(a), e(v)) for a, v, _ in m['lines'])
    return ('<aside class="v-rc %s"%s>%s<div class="v-rh"><b class="v-rch">This month</b>%s</div><p class="v-sm">%s</p><div class="v-cut" aria-hidden="true"></div>'
            '<div class="v-lines">%s</div><div class="v-cut" aria-hidden="true"></div>'
            '<div class="v-tot"><span>Total lost</span><b>%s</b></div><p class="v-sm">%s</p><div class="v-cut" aria-hidden="true"></div>'
            '<div class="v-saved"><span>Saved so far</span><b>%s</b></div><div class="v-code" aria-hidden="true"></div></aside>') % (
        cls, pt(1), '<span class="v-staple" aria-hidden="true"></span>' if staple else '', tag(m['tag']), e(m['spend']), lines,
        e(m['lost']), e(m['share']), e(m['saved']))

def account(m, cls):
    """The month's money as a ledger account (from A), in Virevo type."""
    if not m:
        return '<aside class="v-ac is-empty %s"><b class="v-ach">The month’s account</b><p>Fills in once a month of supplier bills is in.</p></aside>' % cls
    lines = ''.join('<div class="v-al"><span>%s</span><b>%s</b></div>' % (e(a), e(v)) for a, v, _ in m['lines'])
    return ('<aside class="v-ac %s"%s><div class="v-ah"><b class="v-ach">The month’s account</b>%s</div><p class="v-sm">%s</p>'
            '<div class="v-alines">%s</div><div class="v-atot"><span>Lost in all</span><b>%s</b></div><p class="v-sm">%s</p>'
            '<div class="v-asaved"><span>Saved so far</span><b>%s</b></div></aside>') % (
        cls, pt(1), tag(m['tag']), e(m['spend']), lines, e(m['lost']), e(m['share']), e(m['saved']))

def key_html(cls):
    return ('<div class="v-key %s" aria-hidden="true"><span><i class="sg s-done"></i>Done</span><span><i class="sg s-now"></i>Now</span>'
            '<span><i class="sg s-later"></i>Still to do</span><span><i class="sg s-none"></i>Not started</span></div>') % cls

# shared paper and money parts for D, E, F
V_SHARED_CSS = r'''
.v-top{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:40px;align-items:start;margin:26px 0 4px}
.v-top .bm-stand{margin:4px 0 0}
.v-sm{font-size:13px;line-height:1.5;color:var(--mut)}
/* the receipt */
.v-rc{position:relative;background:var(--card);padding:22px 20px 26px;display:flex;flex-direction:column;gap:8px;-webkit-mask:var(--zig);mask:var(--zig);filter:drop-shadow(0 6px 8px rgba(0,0,0,.12))}
.v-rh{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
.v-rch{font-size:12.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.v-cut{border-top:2px dashed var(--grey)}
.v-lines{display:flex;flex-direction:column;gap:6px}
.v-l{display:flex;align-items:baseline;gap:6px;font-size:13.5px;line-height:1.4}
.v-l span{min-width:0}
.v-l i{flex:1 1 16px;min-width:12px;border-bottom:2px dotted var(--grey);transform:translateY(-4px)}
.v-l b{font-weight:600;white-space:nowrap}
.v-tot{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.v-tot span{font-size:12.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.v-tot b{font:400 30px/1 var(--f-d);background:linear-gradient(transparent 52%,var(--hi) 52% 92%,transparent 92%);padding:0 4px}
.v-saved{display:flex;justify-content:space-between;font-size:12.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.v-saved b{color:var(--mut)}
.v-code{height:30px;margin-top:4px;background:repeating-linear-gradient(90deg,var(--ink) 0 2px,transparent 2px 4px,var(--ink) 4px 7px,transparent 7px 9px,var(--ink) 9px 10px,transparent 10px 13px)}
.v-rc.is-empty{background:transparent;-webkit-mask:none;mask:none;filter:none;border:2px dashed var(--grey);color:var(--mut)}
.v-rc.is-empty p{font-size:14px}
/* the account (ledger paper) */
.v-ac{background:var(--card);padding:16px 20px 18px 34px;display:flex;flex-direction:column;gap:6px;border-top:6px solid var(--ink);
 background-image:linear-gradient(90deg,transparent 16px,var(--ink) 16px 17px,transparent 17px 20px,var(--ink) 20px 21px,transparent 21px),repeating-linear-gradient(transparent 0 27px,var(--rule) 27px 28px)}
.v-ah{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;padding-bottom:4px}
.v-ach{font-size:12.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase}
.v-alines{display:flex;flex-direction:column}
.v-al{display:grid;grid-template-columns:minmax(0,1fr) 92px;font-size:14px;line-height:28px}
.v-al span{min-width:0;line-height:1.4;padding:4px 10px 4px 0}
.v-al b{font-weight:600;text-align:right;border-left:1px solid var(--ink);padding:4px 0 4px 8px;line-height:1.4}
.v-atot{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:end;border-top:1.5px solid var(--ink);padding-top:8px;margin-top:2px}
.v-atot span{font-size:14px;font-weight:600}
.v-atot b{font:400 30px/1 var(--f-d);border-bottom:5px double var(--ink);padding:0 2px 2px;background:linear-gradient(transparent 50%,var(--hi) 50% 90%,transparent 90%)}
.v-asaved{display:flex;justify-content:space-between;font-size:13.5px;border-top:1px solid var(--rule);padding-top:6px}
.v-asaved b{font-weight:600}
.v-ac.is-empty{background:transparent;background-image:none;border:2px dashed var(--grey);border-top:6px solid var(--grey);color:var(--mut)}
.v-ac.is-empty p{font-size:14px}
/* step segments (from C) */
.sg{display:block;flex:1;height:100%}
.sg.s-done{background:var(--ink)}
.sg.s-now{background:var(--hi);box-shadow:inset 0 0 0 2px var(--ink)}
.sg.s-later{background:var(--soft);box-shadow:inset 0 0 0 1px var(--grey)}
.sg.s-none,.sg.s-empty{background:transparent;box-shadow:inset 0 0 0 1.5px var(--grey);background-image:repeating-linear-gradient(135deg,transparent 0 5px,rgba(0,0,0,.08) 5px 6px)}
.v-key{display:flex;flex-wrap:wrap;gap:6px 20px;font-size:12.5px;color:var(--mut)}
.v-key span{display:inline-flex;align-items:center;gap:7px}
.v-key .sg{width:18px;height:10px;flex:none}
/* status chips */
.v-st{display:inline-block;font-size:12px;font-weight:600;padding:3px 9px;background:var(--soft);white-space:nowrap}
.v-st.s-now{background:var(--hi);color:var(--ink)}
.v-st.s-started{background:var(--ink);color:var(--card)}
.v-st.s-none,.v-st.s-empty{background:transparent;box-shadow:inset 0 0 0 1px var(--grey);color:var(--mut)}
/* the box for one part: same parts in every look */
.vx-box{display:flex;flex-direction:column;gap:10px;padding:18px 22px 20px;background:var(--card);border-top:6px solid var(--ink)}
.vx-bh{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.vx-box h4{font:400 30px/1 var(--f-d)}
.vx-st{font-size:12px;font-weight:600;padding:3px 9px;background:var(--soft)}
.vx-st.s-now{background:var(--hi)}.vx-st.s-started{background:var(--ink);color:var(--card)}
.vx-st.s-none{background:transparent;box-shadow:inset 0 0 0 1px var(--grey);color:var(--mut)}
.vx-box>p{font-size:14.5px;line-height:1.55}
.vx-fig{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;font-size:13.5px;color:var(--mut)}
.vx-fv{font:400 30px/1 var(--f-d);color:var(--ink)}
.vx-steps{display:flex;flex-direction:column;counter-reset:st}
.vx-steps li{display:flex;align-items:baseline;gap:10px;font-size:14px;line-height:1.45;padding:5px 0;counter-increment:st}
.vx-steps li::before{content:counter(st);font:400 18px/1 var(--f-d);color:var(--mut);min-width:14px}
.vx-steps .mk{display:none}
.vx-sn{min-width:0}
.vx-ss{margin-left:auto;padding-left:14px;font-size:12.5px;font-weight:600;color:var(--mut);white-space:nowrap}
.vx-steps li.s-done .vx-ss{color:var(--ink)}
.vx-steps li.s-now .vx-sn{font-weight:600;background:linear-gradient(transparent 55%,var(--hi) 55% 95%,transparent 95%)}
.vx-steps li.s-now .vx-ss{background:var(--hi);color:var(--ink);padding:1px 8px}
.vx-box .bm-open{align-self:flex-start}
.skin-v .bx-mob{background:transparent;border:0}
.skin-v .bx-mob::before{display:none}
.skin-v .bx-mob .vx-box{padding:14px 16px 16px}
@container lp (max-width:699px){
 .v-top{grid-template-columns:1fr;gap:22px;margin:22px 0 4px}
 .v-ac{padding:14px 14px 16px 28px;background-image:linear-gradient(90deg,transparent 12px,var(--ink) 12px 13px,transparent 13px 16px,var(--ink) 16px 17px,transparent 17px),repeating-linear-gradient(transparent 0 27px,var(--rule) 27px 28px)}
 .v-al{grid-template-columns:minmax(0,1fr) 80px}
 .vx-steps li{display:grid;grid-template-columns:16px minmax(0,1fr);column-gap:10px}
 .vx-ss{grid-column:2;margin:2px 0 0;padding:0;justify-self:start}
 .vx-steps li.s-now .vx-ss{padding:1px 8px}
 .vx-box h4{font-size:26px}
}
'''

def detail(p):
    return place_detail(p, 'vx')

# ==========================================================================================
# D · THE CLEAN LEDGER
def d_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    top = '<div class="v-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), receipt(d['money'], 'vd-rc'))
    rows, desk = [], []
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        inner = ('<span class="vd-no">%d</span><span class="vd-part"><span class="vd-pn">%s%s</span><span class="vd-hl">%s</span></span>'
                 '<span class="vd-ent"><span class="vd-seg" aria-hidden="true">%s</span><span class="vd-prog">%s</span></span>'
                 '<span class="vd-sat"><span class="v-st s-%s">%s</span></span>%s') % (
            i + 1, ico(ICONS[p['name']], 'currentColor', 18), e(p['name']), e(p['head']), segs(p), e(prog(p)) or 'No steps yet',
            p['status'], e(STATUS[p['status']]), '' if empty else CHEV)
        if empty:
            rows.append('<div class="vd-row is-empty">%s</div>' % inner); continue
        rows.append('<button class="vd-row %s" type="button" data-s="%s"%s%s>%s</button>' % (sel_cls(first), p['status'], sel('vd', k, first), pt(p.get('pt')), inner))
        det = detail(p); rows.append(box('vd', k, det, first, 'mob')); desk.append(box('vd', k, det, first, 'desk'))
    head = '<div class="vd-head" aria-hidden="true"><span>No.</span><span>Part of the work</span><span>Entries</span><span>Stands at</span></div>'
    foot = '<div class="vd-foot"><span>Parts finished so far</span><b>%s</b></div>' % ('None of 4' if not empty else '—')
    book = '<div class="vd-book%s">%s<div class="vd-rows">%s</div>%s</div>' % (' is-empty' if empty else '', head, ''.join(rows), foot)
    sub = 'One line in the book for each part of the work. Tap a line to read it.' if not empty else 'One line in the book for each part of the work'
    body = book + (key_html('vd-key') if not empty else '') + ('<div class="vd-desk">%s</div>' % ''.join(desk) if desk else '')
    return (C.masthead(KICK, emb(), STAMP[state]) + top + section('Where each part of the work stands', body, 'vd-sec', sub)
            + pending(d['pending']) + actions(d['actions']))

D_CSS = r'''
.vd-rc .v-code{height:18px}
.vd-rc{gap:6px;padding:20px 20px 22px}
.vd-book{position:relative;background:var(--card);border-top:6px solid var(--ink);
 background-image:linear-gradient(90deg,transparent 18px,var(--ink) 18px 19px,transparent 19px 22px,var(--ink) 22px 23px,transparent 23px)}
.vd-head,.vd-row{display:grid;grid-template-columns:70px minmax(0,1fr) 200px 140px;align-items:stretch}
.vd-head{border-bottom:3px double var(--ink)}
.vd-head span{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut);padding:10px 12px}
.vd-head span:first-child{padding-left:30px}
.vd-head span:nth-child(3),.vd-head span:nth-child(4){border-left:1px solid var(--line)}
.vd-row{width:100%;border:0;border-bottom:1px solid var(--rule);background:transparent;text-align:left;padding:0;color:var(--ink)}
.lp .vd-row.is-up{background:var(--card)}
.vd-no{font:400 26px/1 var(--f-d);color:var(--mut);padding:12px 8px 0 30px}
.vd-part{display:flex;flex-direction:column;gap:3px;padding:9px 12px;min-width:0}
.vd-pn{display:inline-flex;align-items:center;gap:8px;font:400 28px/1 var(--f-d)}
.vd-pn svg{flex-shrink:0;color:var(--mut)}
.vd-hl{font-size:14px;line-height:1.45}
.vd-ent{display:flex;flex-direction:column;justify-content:center;gap:6px;padding:9px 14px;border-left:1px solid var(--line)}
.vd-seg{display:flex;gap:3px;height:14px}
.vd-prog{font-size:12.5px;color:var(--mut)}
.vd-sat{display:flex;align-items:center;padding:9px 12px;border-left:1px solid var(--line)}
.vd-row .sel-chev{display:none}
.vd-row[data-s=none] .vd-pn,.vd-row[data-s=none] .vd-hl,.vd-row.is-empty .vd-pn,.vd-row.is-empty .vd-hl{color:var(--mut)}
.vd-foot{display:flex;justify-content:space-between;align-items:baseline;padding:6px 14px 6px 100px;border-top:3px double var(--ink);font-size:14px}
.vd-foot b{font:400 22px var(--f-d)}
.vd-key{margin-top:14px}
.vd-desk{margin-top:14px}
.vd .bm-sec-pend .bm-pend{background:var(--card);padding:6px 20px 6px 40px;
 background-image:linear-gradient(90deg,transparent 18px,var(--ink) 18px 19px,transparent 19px 22px,var(--ink) 22px 23px,transparent 23px)}
.vd .bm-sec-pend .bm-pi{border-top:0;border-bottom:1px solid var(--rule);padding:8px 0}
@container lp (max-width:699px){
 .vd-book{background-image:linear-gradient(90deg,transparent 8px,var(--ink) 8px 9px,transparent 9px 12px,var(--ink) 12px 13px,transparent 13px)}
 .vd-head{display:none}
 .vd-row{grid-template-columns:40px minmax(0,1fr) 26px;grid-template-areas:"no part chev" "no ent ent" "no sat sat";padding:2px 0 12px}
 .vd-no{grid-area:no;padding:14px 0 0 20px;font-size:22px}
 .vd-part{grid-area:part;padding:12px 6px 4px}
 .vd-ent{grid-area:ent;border-left:0;padding:4px 12px 4px 6px}
 .vd-sat{grid-area:sat;border-left:0;padding:4px 6px}
 .vd-row .sel-chev{display:inline-block;grid-area:chev;margin:22px 0 0}
 .vd-pn{font-size:26px}
 .vd-rows .bx-mob{margin:2px 10px 12px 20px}
 .vd-foot{padding:10px 12px 10px 24px}
 .vd .bm-sec-pend .bm-pend{padding:4px 12px 4px 28px;background-image:linear-gradient(90deg,transparent 8px,var(--ink) 8px 9px,transparent 9px 12px,var(--ink) 12px 13px,transparent 13px)}
}
'''

# ==========================================================================================
# E · RECEIPTS ON THE RAIL
def e_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    top = '<div class="v-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), account(d['money'], 've-ac'))
    slips, desk = [], []
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        inner = ('<span class="ve-clip" aria-hidden="true"></span><span class="ve-sh"><span class="ve-no">%02d</span>%s</span><span class="ve-pn">%s</span>'
                 '<span class="ve-cut" aria-hidden="true"></span><span class="ve-seg" aria-hidden="true">%s</span>'
                 '<span class="ve-num"><b>%s</b><span>%s</span></span><span class="v-st s-%s">%s</span><span class="ve-hl">%s</span>%s') % (
            i + 1, ico(ICONS[p['name']], 'currentColor', 17), e(p['name']), segs(p), frac(p), e(p.get('unit', '')) if p['steps'] else 'no steps yet',
            p['status'], e(STATUS[p['status']]), e(p['head']), '' if empty else CHEV)
        if empty:
            slips.append('<div class="ve-slip is-empty" data-s="empty">%s</div>' % inner); continue
        slips.append('<button class="ve-slip %s" type="button" data-s="%s"%s%s>%s</button>' % (sel_cls(first), p['status'], sel('ve', k, first), pt(p.get('pt')), inner))
        det = detail(p); slips.append(box('ve', k, det, first, 'mob')); desk.append(box('ve', k, det, first, 'desk'))
    total = sum(len(p['steps']) for p in d['places']); done = sum(counts(p)[0] for p in d['places'])
    head = ('<div class="ve-rh"><span><b>%d</b> of %d steps done</span>%s</div>' % (done, total, key_html('ve-key'))) if not empty else ''
    rail = '<div class="ve-rail%s">%s<div class="ve-bar" aria-hidden="true"></div><div class="ve-slips">%s</div></div>' % (
        ' is-empty' if empty else '', head, ''.join(slips))
    sub = 'One receipt for each part of the work. Tap a receipt to read it.' if not empty else 'One receipt for each part of the work'
    body = rail + ('<div class="ve-desk">%s</div>' % ''.join(desk) if desk else '')
    return (C.masthead(KICK, emb(), STAMP[state]) + top + section('Where each part of the work stands', body, 've-sec', sub)
            + pending(d['pending']) + actions(d['actions']))

E_CSS = r'''
.ve-rh{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;font-size:14px;margin-bottom:14px}
.ve-rh b{font:400 26px var(--f-d)}
.ve-rail{position:relative}
.ve-bar{height:14px;background:var(--ink);margin:0 -6px}
.ve-slips{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;align-items:start;margin-top:-2px}
.ve-slip{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:8px;text-align:left;border:0;background:var(--card);color:var(--ink);
 padding:22px 16px 26px;-webkit-mask:var(--zigb);mask:var(--zigb);min-width:0}
.skin-v .ve-slip.is-up{box-shadow:none !important;transform:translate(-3px,-3px);filter:drop-shadow(0 0 1.5px var(--ink)) drop-shadow(7px 7px 0 var(--hi))}
.skin-v .ve-slip:not(.is-up):hover{box-shadow:none;filter:drop-shadow(0 0 1px var(--ink))}
.ve-clip{position:absolute;left:50%;top:0;width:44px;height:12px;margin-left:-22px;background:var(--grey)}
.ve-sh{display:flex;align-items:center;gap:8px;color:var(--mut)}
.ve-no{font:400 18px/1 var(--f-d)}
.ve-pn{font:400 28px/1 var(--f-d)}
.ve-cut{align-self:stretch;border-top:2px dashed var(--grey)}
.ve-seg{display:flex;gap:3px;height:16px;align-self:stretch}
.ve-num{display:flex;align-items:baseline;gap:8px}
.ve-num b{font:400 30px/1 var(--f-d)}
.ve-num span{font-size:12.5px;color:var(--mut)}
.ve-hl{font-size:14px;line-height:1.45}
.ve-slip[data-s=none] .ve-pn,.ve-slip[data-s=none] .ve-hl,.ve-slip[data-s=none] .ve-num b,.ve-slip.is-empty .ve-pn,.ve-slip.is-empty .ve-hl,.ve-slip.is-empty .ve-num b{color:var(--mut)}
.ve-slip .sel-chev{position:absolute;right:16px;top:26px;margin:0}
.ve-rail.is-empty .ve-bar{background:transparent;border:2px dashed var(--grey)}
.ve-rail.is-empty .ve-slip{background:transparent;-webkit-mask:none;mask:none;border:2px dashed var(--grey);border-top:0}
.ve-rail.is-empty .ve-clip{display:none}
.ve-desk{margin-top:22px}
.ve-desk .vx-box{border-top:0;padding-top:26px;-webkit-mask:var(--zig);mask:var(--zig);padding-bottom:28px}
@container lp (max-width:699px){
 .ve-bar{display:none}
 .ve-slips{grid-template-columns:1fr;gap:14px;margin-top:0}
 .ve-slip{padding:20px 44px 24px 16px}
 .ve-slip .sel-chev{display:inline-block;top:24px}
 .ve-slips .bx-mob{margin:-4px 0 6px}
 .ve-slips .bx-mob .vx-box{border-top:0;-webkit-mask:var(--zig);mask:var(--zig);padding:22px 16px 26px}
}
'''

# ==========================================================================================
# F · THE NOTEBOOK
def f_canvas(state):
    d = DATA[state]; empty = state == 'empty'
    top = '<div class="v-top">%s%s</div>' % (standing(d['claim'], d['deck'], empty), receipt(d['money'], 'vf-rc', staple=True))
    rows, desk = [], []
    for i, p in enumerate(d['places']):
        k = str(i); first = i == 0 and not empty
        note = '<span class="vf-hand" aria-hidden="true">We are here</span>' if p['status'] == 'now' else ''
        inner = ('<span class="vf-no">%d</span><span class="vf-main"><span class="vf-pn">%s%s</span><span class="vf-hl">%s</span>'
                 '<span class="vf-seg" aria-hidden="true">%s</span></span><span class="vf-side"><b class="vf-fr">%s</b><span class="v-st s-%s">%s</span></span>%s%s') % (
            i + 1, ico(ICONS[p['name']], 'currentColor', 18), e(p['name']), e(p['head']), segs(p), frac(p), p['status'], e(STATUS[p['status']]),
            note, '' if empty else CHEV)
        if empty:
            rows.append('<div class="vf-row is-empty">%s</div>' % inner); continue
        rows.append('<button class="vf-row %s" type="button" data-s="%s"%s%s>%s</button>' % (sel_cls(first), p['status'], sel('vf', k, first), pt(p.get('pt')), inner))
        det = detail(p); rows.append(box('vf', k, det, first, 'mob')); desk.append(box('vf', k, det, first, 'desk'))
    total = sum(len(p['steps']) for p in d['places']); done = sum(counts(p)[0] for p in d['places'])
    left = ('<div class="vf-page vf-left"><div class="vf-ph"><span>The four parts</span><b>%s</b></div><div class="vf-rows">%s</div></div>') % (
        ('%d of %d steps done' % (done, total)) if not empty else 'No steps yet', ''.join(rows))
    right = ('<div class="vf-page vf-right"><div class="vf-ph"><span>The open part</span><b>Tap a part on the left</b></div>%s</div>' % ''.join(desk)) if desk else (
        '<div class="vf-page vf-right is-empty"><div class="vf-ph"><span>The open part</span></div><p class="vf-wait">Each part’s steps are written here once it starts.</p></div>')
    rings = '<div class="vf-rings" aria-hidden="true">%s</div>' % ('<i></i>' * 9)
    book = '<div class="vf-book%s">%s%s%s</div>' % (' is-empty' if empty else '', left, rings, right)
    sub = 'An open notebook: the parts on the left, the open part’s steps on the right.' if not empty else 'An open notebook, one line for each part of the work'
    body = book + (key_html('vf-key') if not empty else '')
    return (C.masthead(KICK, emb(), STAMP[state]) + top + section('Where each part of the work stands', body, 'vf-sec', sub)
            + pending(d['pending']) + actions(d['actions']))

F_CSS = r'''
.v-staple{position:absolute;left:50%;top:12px;width:46px;height:5px;margin-left:-23px;background:#8E9096;box-shadow:0 1px 0 rgba(0,0,0,.25)}
.vf-rc{padding-top:30px;transform:rotate(-1.2deg)}
.vf-book{position:relative;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);background:var(--card);border-top:6px solid var(--ink);box-shadow:0 0 0 1px var(--line)}
.vf-page{position:relative;padding:14px 22px 22px 22px;min-width:0;
 background-image:repeating-linear-gradient(transparent 0 31px,var(--rule) 31px 32px);background-position:0 46px}
.vf-left{padding-left:40px;background-image:linear-gradient(90deg,transparent 22px,var(--ink) 22px 23px,transparent 23px 26px,var(--ink) 26px 27px,transparent 27px),repeating-linear-gradient(transparent 0 31px,var(--rule) 31px 32px);background-position:0 0,0 46px;
 border-right:1px solid var(--line);box-shadow:inset -14px 0 16px -14px rgba(0,0,0,.18)}
.vf-right{box-shadow:inset 14px 0 16px -14px rgba(0,0,0,.18)}
.vf-rings{position:absolute;left:50%;top:18px;bottom:18px;width:22px;margin-left:-11px;display:flex;flex-direction:column;justify-content:space-between;pointer-events:none}
.vf-rings i{display:block;height:9px;border-radius:5px;background:var(--g);box-shadow:inset 0 0 0 2px var(--ink)}
.vf-ph{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap;padding-bottom:8px;border-bottom:3px double var(--ink);margin-bottom:6px}
.vf-ph span{font-size:12px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--mut)}
.vf-ph b{font-size:12.5px;font-weight:600}
.vf-rows{display:flex;flex-direction:column;padding-top:18px}
.vf-row{position:relative;display:grid;grid-template-columns:24px minmax(0,1fr) auto;gap:10px;align-items:start;width:100%;border:0;border-bottom:1px solid var(--rule);background:transparent;text-align:left;padding:12px 8px 12px 0;color:var(--ink)}
.lp .vf-row.is-up{background:var(--card)}
.vf-no{font:400 24px/1 var(--f-d);color:var(--mut);padding-top:3px}
.vf-main{display:flex;flex-direction:column;gap:4px;min-width:0}
.vf-pn{display:inline-flex;align-items:center;gap:8px;font:400 26px/1 var(--f-d)}
.vf-pn svg{flex-shrink:0;color:var(--mut)}
.vf-hl{font-size:13.5px;line-height:1.45}
.vf-seg{display:flex;gap:3px;height:10px;margin-top:4px;max-width:200px}
.vf-side{display:flex;flex-direction:column;align-items:flex-end;gap:6px}
.vf-fr{font:400 28px/1 var(--f-d)}
.vf-row[data-s=none] .vf-pn,.vf-row[data-s=none] .vf-hl,.vf-row[data-s=none] .vf-fr,.vf-row.is-empty .vf-pn,.vf-row.is-empty .vf-hl,.vf-row.is-empty .vf-fr{color:var(--mut)}
.vf-hand{position:absolute;left:-26px;top:-17px;font:700 21px/1 var(--f-n);color:var(--ink);transform:rotate(-8deg);white-space:nowrap;background:linear-gradient(transparent 55%,var(--hi) 55% 90%,transparent 90%);padding:0 3px;pointer-events:none}
.vf-row .sel-chev{display:none}
.vf-right .vx-box{border-top:0;background:transparent;padding:4px 0 0}
.vf-right .vx-steps li{border-bottom:1px solid var(--rule)}
.vf-wait{font-size:14px;color:var(--mut);padding-top:12px}
.vf-book.is-empty{border-top-color:var(--grey)}
.vf-key{margin-top:14px}
@container lp (max-width:699px){
 .vf-rc{transform:none}
 .vf-book{grid-template-columns:1fr}
 .vf-right,.vf-rings{display:none}
 .vf-left{padding:14px 12px 16px 34px;border-right:0;box-shadow:none;background-image:linear-gradient(90deg,transparent 14px,var(--ink) 14px 15px,transparent 15px 18px,var(--ink) 18px 19px,transparent 19px),repeating-linear-gradient(transparent 0 31px,var(--rule) 31px 32px)}
 .vf-row{grid-template-columns:22px minmax(0,1fr) 22px;padding:14px 4px 12px 0}
 .vf-side{grid-column:2;flex-direction:row;align-items:center;gap:10px}
 .vf-row .sel-chev{display:inline-block;grid-column:3;grid-row:1;margin-top:8px}
 .vf-hand{left:auto;right:30px;top:-10px;font-size:20px}
 .vf-rows .bx-mob{margin:4px 0 12px}
 .vf-rows .bx-mob .vx-box{border-top:3px double var(--ink)}
}
'''

# ==========================================================================================
THEMES = {k: T1['c'] for k in 'def'}   # C's colours: report white, black, lime
PAGES = {
 'd': (d_canvas, D_CSS, 'D', 'The clean ledger', 'vd'),
 'e': (e_canvas, E_CSS, 'E', 'Receipts on the rail', 've'),
 'f': (f_canvas, F_CSS, 'F', 'The notebook', 'vf'),
}
COMMON_NOTE = ('<em>All three: C’s flat frame and colours (report white, black, lime), and the Virevo type unchanged: Bebas Neue for names, claims and figures, '
               'Poppins for reading, Caveat for Tojo’s Note, at the 07 sizes. The domain shows in the paper: report sheet, ledger paper, receipt.</em>')
ABOUT = {
 'd': ('<b>D · The clean ledger.</b> The month’s money is a till receipt, torn top and bottom, with the total marked in lime. '
       'The work is a ledger book: a double margin, ruled lines, one line per part, a step bar for its entries and a double rule under the total. '
       'What Tojo still has to do sits on the same ruled paper.' + COMMON_NOTE),
 'e': ('<b>E · Receipts on the rail.</b> The month’s money is a ledger account: ruled paper, a double margin, a money column and a double-ruled total. '
       'The work is four receipts clipped to a black rail, each with its step bar and a big count, torn at the foot. The open part prints below as a docket.' + COMMON_NOTE),
 'f': ('<b>F · The notebook.</b> The month’s money is a till receipt stapled on. The work is an open spiral notebook: the four parts on the left page, '
       'the open part’s steps on the right page, a hand note marking where we are. On a phone the notebook closes to one page, and each part opens under itself.' + COMMON_NOTE),
}

def build():
    os.makedirs(OUT, exist_ok=True)
    pages, words = {}, []
    for k, (fn, css, letter, label, cls) in PAGES.items():
        sk, t = SKINS[k], THEMES[k]
        for st in ('filled', 'empty'):
            canvas = fn(st)
            for v in ('desktop', 'mobile'):
                h = C.page(sk, t, None, canvas, V_SHARED_CSS + css, DATA[st]['chat'], v, 'Supply Chain and Procurement · %s' % label, 'sc sc-home ' + cls)
                pages['%s.%s.%s' % (k, v, st)] = h
                open(os.path.join(OUT, 'scp-home-%s.%s.%s.html' % (k, v, st)), 'w', encoding='utf-8').write(h)
            words += [(k, st, w) for w in C.plain_check(re.sub(r'<[^>]+>', ' ', canvas) + ' ' + json.dumps(DATA[st]['chat'], ensure_ascii=False))]
    return pages, words

def review(pages):
    tpl = open(os.path.join(HERE, 'review_template.html'), encoding='utf-8').read()
    tpl = tpl.replace('the home page in three looks', 'the home page, round two')
    tpl = re.sub(r'<p class="rv-intro">.*?</p>', '<p class="rv-intro">Round two. C’s clean frame and colours, with A’s notebook and B’s receipt, and the Virevo type kept exactly as it is in every other tool. '
                 'The layout is unchanged: rail, header, page and chat in the same places, five zones in the same order. Pick a look below. Scroll inside each view; every page opens with its first part raised and its box open.</p>', tpl, flags=re.S)
    tpl = tpl.replace("cur={s:'a',st:'filled'}", "cur={s:'d',st:'filled'}")
    picks = ''.join('<button class="rv-s" type="button" data-s="%s" aria-pressed="%s"><b>Sample %s</b><span>%s</span><i style="background:%s;border-color:%s;box-shadow:inset 0 0 0 4px %s"></i></button>' % (
        k, 'true' if k == 'd' else 'false', v[2], e(v[3]), THEMES[k]['ground'], THEMES[k]['ink'], THEMES[k]['hi']) for k, v in PAGES.items())
    return (tpl.replace('@@PICKS@@', picks).replace('@@ABOUT@@', json.dumps(ABOUT, ensure_ascii=False))
               .replace('@@DATA@@', json.dumps(pages, ensure_ascii=False).replace('</', '<\\/')))

if __name__ == '__main__':
    pages, words = build()
    if words:
        print('PLAIN ENGLISH:', words)
    rv = os.path.join(OUT, 'supply-chain-home-round-2.html')
    open(rv, 'w', encoding='utf-8').write(review(pages))
    print('built', rv, os.path.getsize(rv))
