/* ===== Page 2 · Option C · Hold, realistic or best: Tojo offers three marks for every target; the wheel shows where it pulls ===== */
LOOKS.push({ key:"tiers", letter:"C", name:"Three marks", note:"<b>C · Three marks.</b> Tojo offers three marks for every target: hold today's value, Tojo's realistic value, or best practice. Tap one, or type your own. Whole groups can be set in one tap. The wheel on the right is the page-1 formula seen from the other side: levers on the outside, measures in the middle, outcomes at the centre, each outcome ringed by what it asks (navy) and what is backed (green).",
css: P2_CSS + `
.lk-web .tg{display:grid;grid-template-columns:minmax(0,1fr) minmax(320px,440px);gap:24px;align-items:start}
.lk-web .grp{margin-bottom:18px}
.lk-web .grp-h{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin-bottom:8px}
.lk-web .grp-h h2{margin:0;font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1}
.lk-web .grp-h small{color:var(--w-mute);font-size:12.5px}
.lk-web .grp-h .bulk{margin-left:auto;display:flex;gap:6px}
.lk-web .grp-h .bulk button{border:1.5px solid var(--w-ink);background:#fff;border-radius:999px;padding:4px 12px;font-size:12.5px;font-weight:600;min-height:36px;color:var(--w-ink)}
.lk-web .cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.lk-web .cd{border:1.5px solid var(--w-line);border-radius:12px;background:var(--w-sheet);padding:10px 12px;display:flex;flex-direction:column;gap:8px;min-width:0}
.lk-web .cd.mine{border-color:var(--w-ink);box-shadow:4px 4px 0 var(--w-gold)}
.lk-web .cd .top{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.lk-web .cd .top small{display:block;font-size:11.5px;color:var(--w-mute)}
.lk-web .cd .val{font-family:var(--f-num);font-size:26px;line-height:1;text-align:right;white-space:nowrap}
.lk-web .cd .val small{display:block;font-family:var(--f-body);font-size:10.5px;color:var(--w-mute)}
.lk-web .tiers{display:grid;grid-template-columns:repeat(3,1fr);border:1.5px solid var(--w-ink);border-radius:10px;overflow:hidden}
.lk-web .tiers button{border:0;border-left:1.5px solid var(--w-ink);background:#fff;padding:5px 4px;min-height:44px;font-size:11px;font-weight:600;color:var(--w-mute);line-height:1.2}
.lk-web .tiers button:first-child{border-left:0}
.lk-web .tiers button b{display:block;font-family:var(--f-num);font-weight:400;font-size:17px;color:var(--w-ink)}
.lk-web .tiers button[aria-pressed="true"]{background:var(--w-ink);color:#E6EAF5}
.lk-web .tiers button[aria-pressed="true"] b{color:#fff}
.lk-web .tiers button[data-t="r"][aria-pressed="true"]{background:var(--w-gold);color:var(--w-ink)} .lk-web .tiers button[data-t="r"][aria-pressed="true"] b{color:var(--w-ink)}
.lk-web .own{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--w-mute)}
.lk-web .own .num{width:96px}
.lk-web .cd .sline{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.lk-web details.grp>summary{list-style:none;cursor:pointer;min-height:44px;display:flex;align-items:center;gap:10px}
.lk-web details.grp>summary::-webkit-details-marker{display:none}
.lk-web details.grp>summary h2::before{content:"▸ ";font-family:var(--f-body);font-size:18px}
.lk-web details.grp[open]>summary h2::before{content:"▾ "}
.lk-web .wh{position:sticky;top:calc(12px + env(safe-area-inset-top,0px));border:2px solid var(--w-ink);border-radius:18px;background:var(--w-sheet);box-shadow:8px 8px 0 rgba(22,33,62,.12)}
.lk-web .wh svg{display:block;width:100%;height:auto}
.lk-web .wh h2{margin:0;padding:12px 14px 0;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.lk-web .wh .lgw{display:flex;flex-wrap:wrap;gap:4px 12px;padding:8px 14px 12px;font-size:11.5px;color:var(--w-mute);border-top:1.5px solid var(--w-line)}
.lk-web .wh .hand{position:absolute;right:14px;top:10px;font-family:var(--f-hand);font-weight:700;font-size:21px;color:var(--w-gold-ink);transform:rotate(2deg)}
.lk-web .pw-e{fill:none;stroke:#C9D0DA;stroke-width:1}
.lk-web .pw-e.on{stroke:var(--w-gold);stroke-width:1.8}
.lk-web .pw-n{cursor:pointer}
.lk-web .pw-n .s{fill:#fff;stroke:var(--w-ink);stroke-width:1.6}
.lk-web .pw-n.on .s{fill:var(--w-gold)}
.lk-web .pw-n.mine .s{stroke:var(--w-gold-ink);stroke-width:2.6}
.lk-web .pw-m{cursor:pointer}
.lk-web .pw-m circle{stroke:var(--w-ink);stroke-width:1.2}
.lk-web .pw-k{cursor:pointer}
.lk-web .pw-k circle.base{fill:#fff;stroke:#DCE2EA;stroke-width:9}
.lk-web .pw-k .arcA{fill:none;stroke:var(--w-ink);stroke-width:5;stroke-linecap:round}
.lk-web .pw-k .arcB{fill:none;stroke:var(--w-yours);stroke-width:5;stroke-linecap:round}
.lk-web .pw-k.short .arcB{stroke:var(--w-none)}
.lk-web .pw-k text{font-family:var(--f-num);font-size:13px;fill:var(--w-ink)}
@media (max-width:1100px){.lk-web .tg{grid-template-columns:1fr}.lk-web .wh{position:relative;top:0}}
`,
mount(stage){
  const card = id => { const it = ITEMS[id];
    if (isSwitch(it)) return `<div class="cd" data-mine="${id}"><div class="top"><div>${nameBtn(id, it.c?` <span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${it.c}"></span>`:"")}<small>${it.k==="auto"?"Virevo automation suite":"Today: "+(it.t?"in place":"not in place")}</small></div><div class="val" data-tv="${id}"></div></div>
      <div class="tiers"><button type="button" data-p2="tier:${id}:t" data-tier="${id}:t" data-t="t"><b>${it.t?"On":"Off"}</b>Hold</button><button type="button" data-p2="tier:${id}:r" data-tier="${id}:r" data-t="r"><b>${it.r?"On":"Off"}</b>Realistic</button><button type="button" data-p2="tier:${id}:b" data-tier="${id}:b" data-t="b"><b>${it.b?"On":"Off"}</b>Best</button></div>
      ${it.k==="auto"?`<div class="sline"><label class="own" for="go-${id}">Goes live</label><select class="gomo" id="go-${id}" data-go="${id}">${Array.from({length:12},(_,i)=>`<option value="${i+1}" ${TS.go[id]===i+1?"selected":""}>Month ${i+1}</option>`).join("")}</select></div>`:""}</div>`;
    return `<div class="cd" data-mine="${id}"><div class="top"><div>${nameBtn(id)}<small>${srcMini(id)} ${esc(unitOf(it))}</small>${glyphsHTML(id)}</div><div class="val"><span data-tv="${id}"></span><small>your target</small></div></div>
      <div class="tiers"><button type="button" data-p2="tier:${id}:t" data-tier="${id}:t" data-t="t"><b>${esc(fmtV(id,it.t))}</b>Hold today</button><button type="button" data-p2="tier:${id}:r" data-tier="${id}:r" data-t="r"><b>${esc(fmtV(id,it.r))}</b>Realistic</button><button type="button" data-p2="tier:${id}:b" data-tier="${id}:b" data-t="b"><b>${esc(fmtV(id,it.b))}</b>Best</button></div>
      <div class="own"><label for="n-${id}">Or your own</label><input class="num" id="n-${id}" type="number" step="${stepOf(it)}" data-num="${id}" inputmode="decimal"></div></div>`; };
  const bulk = g => `<div class="bulk"><button type="button" data-bulk="${g}:t">Hold all</button><button type="button" data-bulk="${g}:r">All realistic</button><button type="button" data-bulk="${g}:b">All best</button></div>`;
  const grp = (g, title, sub, ids, open=true, det=false) => det
    ? `<details class="grp"${open?" open":""}><summary><div class="grp-h" style="margin:0;flex:1"><h2>${title}</h2><small>${sub}</small>${bulk(g)}</div></summary><div class="cards">${ids.map(card).join("")}</div></details>`
    : `<section class="grp"><div class="grp-h"><h2>${title}</h2><small>${sub}</small>${bulk(g)}</div><div class="cards">${ids.map(card).join("")}</div></section>`;
  this.groups = { out:KPIS.map(k=>k.id) }; Object.keys(KIND).forEach(k => this.groups[k] = LEVERS.filter(l=>l.k===k).map(l=>l.id));
  DOMAINS.forEach(d => this.groups["f-"+d.id] = d.ms.map(m=>m.id).filter(id=>ITEMS[id]));
  const html = grp("out","Outcomes","the nine KPIs", this.groups.out)
    + Object.keys(KIND).map(k => grp(k, KIND[k][0], KIND[k][1], this.groups[k])).join("")
    + `<h2 class="eb" style="margin:22px 0 8px">Measures, by data family</h2>` + DOMAINS.map((d,i) => this.groups["f-"+d.id].length ? grp("f-"+d.id, d.name, `${this.groups["f-"+d.id].length} targets`, this.groups["f-"+d.id], i===0, true) : "").join("");
  p2Mount(stage, `${p2Head("Hold, realistic or best", "For every target Tojo offers three marks. Tap one, type your own, or set a whole group at once. The wheel shows which levers you have moved and whether each outcome is backed.")}
    <div class="tools"><button type="button" class="act ghost" data-p2="reset">Reset everything to Tojo's realistic</button></div>
    <div class="tg"><div>${html}${p2CtaHTML()}</div><aside class="wh"><h2>Where your targets pull</h2><span class="hand" aria-hidden="true">gold = you moved it</span>${this.wheel()}
      <div class="lgw"><span>Outer ring: levers (● people, ■ equipment, ◆ ways of working, ▬ automations)</span><span>Middle: measures, darker = further toward best</span><span>Centre: outcomes, navy arc = asked, green = backed</span></div></aside></div>`);
  stage.querySelectorAll("[data-bulk]").forEach(b => b.addEventListener("click", () => { const [g,tier] = b.dataset.bulk.split(":");
    this.groups[g].forEach(id => { const it = ITEMS[id]; if (tier==="r") delete TS.user[id]; else TS.user[id] = tier==="t" ? it.t : it.b; }); p2listeners.forEach(fn=>fn(null)); }));
},
wheel(){
  const S = 440, C = S/2, RL = 196, RM = 140, RK = 74;
  const pt = (r,a) => [C + r*Math.cos(a), C + r*Math.sin(a)];
  const levers = LEVERS, ms = Object.values(ITEMS).filter(i=>i.kind==="ms"), ks = KPIS.filter(k=>k.id!=="EBITDA");
  const A = {}; levers.forEach((l,i) => A[l.id] = pt(RL, -Math.PI/2 + i*2*Math.PI/levers.length));
  ms.forEach((m,i) => A[m.id] = pt(RM, -Math.PI/2 + (i+.5)*2*Math.PI/ms.length));
  A.EBITDA = [C,C]; ks.forEach((k,i) => A[k.id] = pt(RK, -Math.PI/2 + i*2*Math.PI/ks.length));
  const edges = Object.entries(INPUTS).flatMap(([to,ins]) => ins.map(([f]) => A[f] && A[to] ? `<line class="pw-e" data-ef="${f}" x1="${A[f][0].toFixed(1)}" y1="${A[f][1].toFixed(1)}" x2="${A[to][0].toFixed(1)}" y2="${A[to][1].toFixed(1)}"/>` : "")).join("");
  const shape = (l,[x,y]) => { const s = l.k==="people" ? `<circle class="s" cx="${x}" cy="${y}" r="7"/>` : l.k==="kit" ? `<rect class="s" x="${x-6.5}" y="${y-6.5}" width="13" height="13" rx="2"/>` : l.k==="way" ? `<rect class="s" x="${x-6}" y="${y-6}" width="12" height="12" transform="rotate(45 ${x} ${y})"/>` : `<rect class="s" x="${x-9}" y="${y-5}" width="18" height="10" rx="5" style="${l.c?`stroke:${l.c}`:""}"/>`;
    return `<g class="pw-n" data-pl="${l.id}" data-ref="it:${l.id}" tabindex="0" role="button" aria-label="${esc(l.n)}"><circle cx="${x}" cy="${y}" r="13" fill="transparent"/>${s}</g>`; };
  const nodesL = levers.map(l => shape(l, A[l.id].map(v=>+v.toFixed(1)))).join("");
  const nodesM = ms.map(m => `<g class="pw-m" data-pm="${m.id}" data-ref="it:${m.id}" tabindex="0" role="button" aria-label="${esc(m.n)}"><circle cx="${A[m.id][0].toFixed(1)}" cy="${A[m.id][1].toFixed(1)}" r="5"/></g>`).join("");
  const nodesK = KPIS.map(k => { const [x,y] = A[k.id], r = k.id==="EBITDA" ? 30 : 21;
    return `<g class="pw-k" data-pk="${k.id}" data-ref="it:${k.id}" tabindex="0" role="button" aria-label="${esc(k.n)}"><circle class="base" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r}"/><path class="arcA" d=""/><path class="arcB" d=""/><text x="${x.toFixed(1)}" y="${(y+4).toFixed(1)}" text-anchor="middle" style="${k.id==="EBITDA"?"font-size:15px":""}">${esc(k.id==="EBITDA"?"EBITDA":k.s.length>9?k.s.slice(0,8)+"…":k.s)}</text></g>`; }).join("");
  this.A = A;
  return `<svg viewBox="0 0 ${S} ${S}" role="img" aria-label="Levers, measures and outcomes, with your targets marked">${edges}${nodesM}${nodesL}${nodesK}</svg>`;
},
update(root){ syncTargets(root); syncGlyphs(root);
  const arc = (x,y,r,f) => { if (f <= 0.001) return ""; if (f >= 0.999) return `M${x} ${y-r} a${r} ${r} 0 1 1 -0.01 0`; const a = -Math.PI/2 + f*2*Math.PI; return `M${x} ${y-r} A${r} ${r} 0 ${f>.5?1:0} 1 ${(x+r*Math.cos(a)).toFixed(1)} ${(y+r*Math.sin(a)).toFixed(1)}`; };
  root.querySelectorAll("[data-pl]").forEach(g => { const id = g.dataset.pl, moved = valOf(id) !== ITEMS[id].t; g.classList.toggle("on", moved); g.classList.toggle("mine", TS.user[id]!==undefined); });
  root.querySelectorAll(".pw-e").forEach(e => e.classList.toggle("on", valOf(e.dataset.ef) !== ITEMS[e.dataset.ef].t && TS.user[e.dataset.ef]!==undefined));
  root.querySelectorAll("[data-pm]").forEach(g => { const f = fracOf(g.dataset.pm); g.querySelector("circle").style.fill = `rgba(22,33,62,${(0.08+0.9*f).toFixed(2)})`; });
  root.querySelectorAll("[data-pk]").forEach(g => { const id = g.dataset.pk, [x,y] = this.A[id], r = id==="EBITDA" ? 30 : 21, t = tension(id);
    g.querySelector(".arcA").setAttribute("d", arc(x, y, r+7, fracOf(id))); g.querySelector(".arcB").setAttribute("d", arc(x, y, r, backed(id)??0)); g.classList.toggle("short", t>.15); });
}});
