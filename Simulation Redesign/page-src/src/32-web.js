/* ===== Option B · One formula: every file, measure and KPI on one wheel; links firm up as data arrives ===== */
const WEB_CSS = `
.lk-web{--w-paper:#EEF1F4;--w-sheet:#FBFCFD;--w-ink:#16213E;--w-mute:#4E5A73;--w-line:#C9D0DA;--w-yours:#1E7A4C;--w-ref:#6C4BB4;--w-paper2:#C76A12;--w-none:#B23B3B;--w-gold:#d4a94f;--w-gold-ink:#6B4F16;
  --pk-bg:#16213E;--pk-fg:#F4F6FA;--pk-line:#34416A;--sh-bg:#FBFCFD;--sh-fg:#16213E;--sh-mute:#4E5A73;--sh-line:#D6DCE4;--sh-card:#fff;--c-ok:#1E7A4C;--c-warn:#8A5A00;--c-bad:#B23B3B;
  background:var(--w-paper);background-image:radial-gradient(circle at 1px 1px,rgba(22,33,62,.09) 1px,transparent 0);background-size:22px 22px;color:var(--w-ink);padding:18px clamp(16px,3vw,40px) 120px;min-height:100vh}
.lk-web .jr ol{list-style:none;margin:0;padding:0;display:flex;align-items:center;gap:0;overflow:auto;scrollbar-width:none}
.lk-web .jr li{flex:0 0 auto;display:flex;align-items:center}
.lk-web .jr li+li::before{content:"";width:26px;height:2px;background:var(--w-line);margin:0 4px}
.lk-web .jr button{display:flex;align-items:center;gap:8px;border:1.5px solid var(--w-line);background:var(--w-sheet);color:var(--w-mute);border-radius:10px;padding:5px 12px 5px 5px;min-height:44px}
.lk-web .jr button b{width:30px;height:30px;border-radius:7px;display:grid;place-items:center;background:var(--w-paper);font-family:var(--f-num);font-weight:400;font-size:18px;color:var(--w-ink)}
.lk-web .jr button span{display:flex;flex-direction:column;align-items:flex-start;font-size:13px;font-weight:600;line-height:1.15}
.lk-web .jr button small{font-weight:400;font-size:11px}
.lk-web .jr .now button{border-color:var(--w-ink);background:var(--w-ink);color:#fff}
.lk-web .jr .now button b{background:var(--w-gold);color:var(--w-ink)}
.lk-web .jr button[aria-disabled]{cursor:default}
.lk-web .grid{display:grid;grid-template-columns:minmax(300px,420px) minmax(0,1fr);gap:24px;margin-top:22px;align-items:start}
.lk-web .eb{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--w-mute)}
.lk-web h1{font-family:var(--f-num);font-weight:400;font-size:clamp(44px,5.4vw,62px);line-height:.92;margin:6px 0 10px;text-wrap:balance}
.lk-web .lede{margin:0 0 16px;color:var(--w-mute)}
.lk-web .pulse{display:grid;grid-template-columns:1fr 1fr;gap:0;border:2px solid var(--w-ink);border-radius:12px;background:var(--w-sheet);overflow:hidden;margin-bottom:16px}
.lk-web .pz{position:relative;text-align:left;border:0;background:transparent;color:var(--w-ink);padding:12px 14px;min-height:44px}
.lk-web .pz:nth-child(odd){border-right:1.5px solid var(--w-line)} .lk-web .pz:nth-child(-n+2){border-bottom:1.5px solid var(--w-line)}
.lk-web .pz:hover{background:#F1F4F8}
.lk-web .pz .pl{display:block;font-size:10.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .pz b{display:block;font-family:var(--f-num);font-weight:400;font-size:36px;line-height:1}
.lk-web .pz b i{font-style:normal;font-size:20px;color:var(--w-mute)}
.lk-web .pz small{display:block;font-size:11.5px;color:var(--w-mute)}
.lk-web .pz[data-ref="pulse:links"] b{color:var(--w-yours)}
.lk-web .intake{display:grid;gap:8px;margin-bottom:16px}
.lk-web .drop{display:flex;flex-direction:column;gap:2px;border:2px dashed var(--w-ink);border-radius:12px;padding:14px 16px;cursor:pointer;background:var(--w-sheet)}
.lk-web .drop:hover,.lk-web .drop:focus-within{background:#fff;box-shadow:6px 6px 0 rgba(22,33,62,.12)}
.lk-web .dz-big{font-family:var(--f-num);font-size:28px;line-height:1}
.lk-web .dz-sub{font-size:13px;color:var(--w-mute)}
.lk-web .acts{display:flex;flex-wrap:wrap;gap:8px}
.lk-web .act{border:2px solid var(--w-ink);background:var(--w-ink);color:#fff;border-radius:10px;padding:8px 14px;font-weight:600;font-size:13.5px;min-height:44px}
.lk-web .act.ghost{background:transparent;color:var(--w-ink)}
.lk-web .intake-note{margin:0;font-size:12.5px;color:var(--w-mute)}
.lk-web h2{margin:0 0 8px;font-size:11.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--w-mute)}
.lk-web .watch{list-style:none;margin:0 0 16px;padding:0;display:grid;gap:6px}
.lk-web .wi{width:100%;display:flex;gap:10px;align-items:center;text-align:left;border:1.5px solid var(--w-line);border-radius:10px;padding:8px 10px;background:var(--w-sheet);color:var(--w-ink);min-height:44px}
.lk-web .wi:hover{border-color:var(--w-ink)}
.lk-web .wi i{flex:0 0 26px;height:26px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-weight:700;font-size:13px;border:2px dashed var(--w-ref);color:var(--w-ref)}
.lk-web .wi-manual i{border:2px solid var(--w-paper2);color:var(--w-paper2)} .lk-web .wi-none i{border:2px dotted var(--w-none);color:var(--w-none)}
.lk-web .wi b{display:block;font-size:13.5px} .lk-web .wi small{display:block;font-size:12px;color:var(--w-mute)}
.lk-web .wheel{position:relative;border:2px solid var(--w-ink);border-radius:18px;background:var(--w-sheet);box-shadow:8px 8px 0 rgba(22,33,62,.12)}
.lk-web .wheel>svg{display:block;width:100%;height:auto}
.lk-web .wheel .hand{position:absolute;right:18px;top:14px;font-family:var(--f-hand);font-weight:700;font-size:25px;color:var(--w-gold-ink);max-width:220px;text-align:right;line-height:1.05;transform:rotate(2deg)}
.lk-web .lg{display:flex;flex-wrap:wrap;gap:6px 16px;padding:10px 16px;border-top:1.5px solid var(--w-line);font-size:12.5px;color:var(--w-mute)}
.lk-web .lg span{display:inline-flex;align-items:center;gap:6px}
.lk-web .e{fill:none;stroke-linecap:round;transition:opacity .2s,stroke .3s}
.lk-web .e.yours{stroke:var(--w-yours);opacity:.55}
.lk-web .e.ref,.lk-web .e.manual,.lk-web .e.none{stroke:var(--w-ref);stroke-dasharray:4 5;opacity:.38}
.lk-web .e.kk{stroke:var(--w-ink);opacity:.35}
.lk-web svg.focus .e{opacity:.06} .lk-web svg.focus .e.hl{opacity:.95}
.lk-web svg.focus .mn:not(.hl),.lk-web svg.focus .kn:not(.hl){opacity:.35}
.lk-web .mn,.lk-web .kn,.lk-web .ft,.lk-web .arc{cursor:pointer}
.lk-web .mn circle.d{stroke-width:2.2;transition:fill .3s}
.lk-web .mn.yours circle.d{fill:var(--w-yours);stroke:var(--w-yours)}
.lk-web .mn.ref circle.d{fill:#fff;stroke:var(--w-ref);stroke-dasharray:3 2.4}
.lk-web .mn.manual circle.d{fill:#FBE4CC;stroke:var(--w-paper2)}
.lk-web .mn.none circle.d{fill:#fff;stroke:var(--w-none);stroke-dasharray:1.5 2.5}
.lk-web .mn text{font-size:11.5px;fill:var(--w-ink);font-family:var(--f-body)}
.lk-web .mn.pop circle.d{animation:wpop .6s ease}
@keyframes wpop{40%{r:12}}
.lk-web .kn circle{fill:var(--w-sheet);stroke:var(--w-ink);stroke-width:2}
.lk-web .kn.core circle{fill:var(--w-ink)}
.lk-web .kn text.k{font-family:var(--f-num);font-size:18px;fill:var(--w-ink);letter-spacing:.02em}
.lk-web .kn.core text.k{fill:#fff;font-size:26px}
.lk-web .kn text.p{font-size:11px;font-weight:600;fill:var(--w-yours)}
.lk-web .kn.core text.p{fill:var(--w-gold)}
.lk-web .arc path.band{fill:none;stroke:#E3E8EF;stroke-width:26}
.lk-web .arc:hover path.band,.lk-web .arc:focus path.band{stroke:#D3DBE6}
.lk-web .arc text{font-size:13px;font-weight:600;fill:var(--w-ink);letter-spacing:.06em;text-transform:uppercase}
.lk-web .ft rect{fill:#DCE2EA;stroke:var(--w-line)}
.lk-web .ft.in rect{fill:var(--w-ink);stroke:var(--w-ink)}
.lk-web .ft.need:not(.in) rect{fill:#fff;stroke:var(--w-none);stroke-width:1.5}
.lk-web .fam{display:none;list-style:none;margin:14px 0 0;padding:0;gap:6px}
.lk-web .fam button{width:100%;display:grid;grid-template-columns:1fr auto;gap:4px 10px;text-align:left;border:1.5px solid var(--w-line);border-radius:10px;padding:10px 12px;background:var(--w-sheet);color:var(--w-ink);min-height:44px}
.lk-web .fam small{color:var(--w-mute);font-size:12px}
.lk-web .fam .bar{grid-column:1/-1;height:6px;border-radius:3px;background:#DCE2EA;overflow:hidden}.lk-web .fam .bar i{display:block;height:100%;background:var(--w-yours)}
.lk-web .cta{display:grid;gap:8px}
.lk-web .go{border:2px solid var(--w-line);background:transparent;color:var(--w-mute);border-radius:12px;padding:10px 22px;font-weight:600;font-size:15px;min-height:52px}
.lk-web .go.ready{background:var(--w-gold);border-color:var(--w-ink);color:var(--w-ink);box-shadow:5px 5px 0 var(--w-ink)}
.lk-web .cta-note{font-size:13px;color:var(--w-mute)}
@media (max-width:1060px){.lk-web .grid{grid-template-columns:1fr}.lk-web .side{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}.lk-web .side>.head{grid-column:1/-1}}
@media (max-width:700px){.lk-web .side{display:block}.lk-web .fam{display:grid}.lk-web .wheel .hand{display:none}.lk-web .mn text,.lk-web .arc text{display:none}}
`;
LOOKS.push({ key:"web", step:0, letter:"B", name:"One formula", note:"<b>B · One formula.</b> The single formula drawn as a wheel. Outer ring: the ten data families and their files. Middle ring: the measures. Centre: the KPIs, with EBITDA at the heart. A solid green link is learned from your data; a dashed violet link uses reference weights. Rest on any KPI or measure to see what it pulls.",
css: WEB_CSS,
mount(stage){
  const C = 540, RK = 150, RM = 290, RA = 468, RF = 506, S = 1080;
  const pt = (r,a) => [C + r*Math.cos(a), C + r*Math.sin(a)];
  // measures around the middle ring, grouped by family, with a gap between families
  const total = DOMAINS.reduce((s,d)=>s+d.ms.length,0), gapA = 0.09, step = (2*Math.PI - gapA*DOMAINS.length)/total;
  let a = -Math.PI/2 + gapA/2; const MP = {}, arcs = [];
  DOMAINS.forEach(d => { const a0 = a; d.ms.forEach(m => { MP[m.id] = a + step/2; a += step; }); arcs.push([d,a0,a]); a += gapA; });
  const KPOS = { EBITDA:[C,C] }; KPIS.filter(k=>k.id!=="EBITDA").forEach((k,i,arr)=>{ KPOS[k.id] = pt(RK, -Math.PI/2 + i*2*Math.PI/arr.length); });
  const edges = LINKS.map(([s,t,w],i) => {
    const tp = KPOS[t]; if (!tp) return "";
    if (MS[s]) { const sp = pt(RM, MP[s]), cp = pt(RM*0.55, MP[s]);
      return `<path class="e" data-s="${s}" data-t="${t}" d="M${sp[0].toFixed(1)} ${sp[1].toFixed(1)} Q${cp[0].toFixed(1)} ${cp[1].toFixed(1)} ${tp[0].toFixed(1)} ${tp[1].toFixed(1)}" stroke-width="${(0.8+w*2.6).toFixed(2)}"/>`; }
    const sp = KPOS[s]; return `<path class="e kk" data-s="${s}" data-t="${t}" d="M${sp[0].toFixed(1)} ${sp[1].toFixed(1)} L${tp[0].toFixed(1)} ${tp[1].toFixed(1)}" stroke-width="${(1+w*2.5).toFixed(2)}"/>`;
  }).join("");
  const mnodes = Object.values(MS).map(m => { const [x,y] = pt(RM, MP[m.id]); const ang = MP[m.id]; const right = Math.cos(ang) >= 0;
    const [lx,ly] = pt(RM + 14, ang);
    return `<g class="mn" data-ms="${m.id}" data-ref="ms:${m.id}" tabindex="0" role="button" aria-label="${esc(m.n)}"><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="14" fill="transparent"/><circle class="d" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="7"/>
      <text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" dy="4" text-anchor="${right?"start":"end"}" transform="rotate(${(right? ang*180/Math.PI : ang*180/Math.PI+180).toFixed(1)} ${lx.toFixed(1)} ${ly.toFixed(1)})">${esc(m.n.length>30?m.n.slice(0,29)+"…":m.n)}</text></g>`; }).join("");
  const arcEls = arcs.map(([d,a0,a1]) => { const p0 = pt(RA,a0), p1 = pt(RA,a1); const large = (a1-a0) > Math.PI ? 1 : 0; const mid = (a0+a1)/2; const flip = Math.sin(mid) > 0.1;
    const t0 = pt(RA, flip ? a1 : a0), t1 = pt(RA, flip ? a0 : a1);
    const files = d.files.map((f,i) => { const fa = a0 + (i+0.5)*(a1-a0)/d.files.length; const [fx,fy] = pt(RF, fa);
      return `<g class="ft${REQUIRED.includes(f)?" need":""}" data-file="${f}" data-ref="file:${f}" tabindex="0" role="button" aria-label="${esc(FILE_NAME[f])}"><rect x="${(fx-6).toFixed(1)}" y="${(fy-6).toFixed(1)}" width="12" height="12" rx="2.5" transform="rotate(${(fa*180/Math.PI).toFixed(1)} ${fx.toFixed(1)} ${fy.toFixed(1)})"/></g>`; }).join("");
    return `<g class="arc" data-ref="dom:${d.id}" tabindex="0" role="button" aria-label="${esc(d.name)}"><path class="band" d="M${p0[0].toFixed(1)} ${p0[1].toFixed(1)} A${RA} ${RA} 0 ${large} 1 ${p1[0].toFixed(1)} ${p1[1].toFixed(1)}"/>
      <path id="arc-${d.id}" fill="none" d="M${t0[0].toFixed(1)} ${t0[1].toFixed(1)} A${RA} ${RA} 0 ${large} ${flip?0:1} ${t1[0].toFixed(1)} ${t1[1].toFixed(1)}"/>
      <text dy="4.5"><textPath href="#arc-${d.id}" startOffset="50%" text-anchor="middle">${esc(d.short)}</textPath></text></g>${files}`; }).join("");
  const knodes = KPIS.map(k => { const [x,y] = KPOS[k.id]; const core = k.id==="EBITDA"; const r = core?62:44;
    return `<g class="kn${core?" core":""}" data-k="${k.id}" data-ref="kpi:${k.id}" tabindex="0" role="button" aria-label="${esc(k.n)}"><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r}"/>
      <text class="k" x="${x.toFixed(1)}" y="${(y-(core?2:1)).toFixed(1)}" text-anchor="middle">${esc(k.s||k.n)}</text><text class="p" data-kp="${k.id}" x="${x.toFixed(1)}" y="${(y+(core?22:17)).toFixed(1)}" text-anchor="middle"></text></g>`; }).join("");
  stage.innerHTML = `<div class="lk lk-web">${journeyHTML()}
    <div class="grid"><div class="side"><div class="head"><div class="eb">Simulation · step 1 of 8 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>One formula, built from your data</h1><p class="lede">Every file you send firms up the links it feeds. Where a file is missing, the link still works, using reference weights, drawn dashed until your numbers replace them.</p></div>
      ${pulseHTML()}<div>${intakeHTML()}<h2>Links still on reference</h2>${watchHTML()}${ctaHTML()}</div></div>
      <div><div class="wheel"><div class="hand" aria-hidden="true">solid = learned from you</div>
        <svg viewBox="0 0 ${S} ${S}" role="img" aria-label="The formula wheel: families and files outside, measures in the middle ring, KPIs at the centre">${edges}${arcEls}${mnodes}${knodes}</svg>
        <div class="lg"><span><svg width="26" height="8"><line x1="1" y1="4" x2="25" y2="4" stroke="#1E7A4C" stroke-width="3"/></svg>Link from your data</span><span><svg width="26" height="8"><line x1="1" y1="4" x2="25" y2="4" stroke="#6C4BB4" stroke-width="2.5" stroke-dasharray="4 4"/></svg>Link from reference</span><span><svg width="12" height="12"><circle cx="6" cy="6" r="5" fill="#FBE4CC" stroke="#C76A12" stroke-width="2"/></svg>On paper</span><span><svg width="12" height="12"><circle cx="6" cy="6" r="5" fill="#fff" stroke="#B23B3B" stroke-width="2" stroke-dasharray="1.5 2"/></svg>Not recorded</span><span><svg width="12" height="12"><rect x="1" y="1" width="10" height="10" rx="2" fill="#16213E"/></svg>File in</span><span><svg width="12" height="12"><rect x="1" y="1" width="10" height="10" rx="2" fill="#fff" stroke="#B23B3B" stroke-width="1.5"/></svg>Needed, not sent</span></div>
      </div>
      <ul class="fam" aria-label="Data families">${DOMAINS.map(d=>`<li><button type="button" data-ref="dom:${d.id}"><b>${esc(d.name)}</b><small data-v="fm-${d.id}"></small><span class="bar"><i data-bar="${d.id}"></i></span></button></li>`).join("")}</ul></div>
    </div></div>`;
  wireIntake(stage);
  const svg = stage.querySelector(".wheel svg");
  const focus = id => { svg.classList.add("focus"); svg.querySelectorAll(".e").forEach(e => e.classList.toggle("hl", e.dataset.s===id || e.dataset.t===id));
    const near = new Set([id]); LINKS.forEach(l => { if (l[0]===id) near.add(l[1]); if (l[1]===id) near.add(l[0]); });
    svg.querySelectorAll(".mn,.kn").forEach(n => n.classList.toggle("hl", near.has(n.dataset.ms||n.dataset.k))); };
  const unfocus = () => { svg.classList.remove("focus"); svg.querySelectorAll(".hl").forEach(n=>n.classList.remove("hl")); };
  svg.querySelectorAll(".mn,.kn").forEach(n => { n.addEventListener("pointerenter", () => focus(n.dataset.ms||n.dataset.k)); n.addEventListener("pointerleave", unfocus); n.addEventListener("focus", () => focus(n.dataset.ms||n.dataset.k)); n.addEventListener("blur", unfocus); });
},
update(root, arrived){
  root.querySelectorAll(".ft").forEach(g => g.classList.toggle("in", !!ST.files[g.dataset.file]));
  root.querySelectorAll(".mn").forEach(g => { const was = g.classList.contains("yours"); const s = msState(MS[g.dataset.ms]); g.setAttribute("class", "mn " + s + (s==="yours" && !was && arrived ? " pop" : "")); });
  root.querySelectorAll(".e:not(.kk)").forEach(e => { const s = msState(MS[e.dataset.s]); e.classList.remove("yours","ref","manual","none"); e.classList.add(s); });
  root.querySelectorAll("[data-kp]").forEach(t => { const sh = kpiShare(t.dataset.kp); t.textContent = sh ? `${sh.pct}% yours` : ""; });
  DOMAINS.forEach(d => { const s = domStats(d); root.querySelectorAll(`[data-v="fm-${d.id}"]`).forEach(t => t.textContent = `${s.inn}/${s.of} files · ${s.yours}/${s.msN} measures`); root.querySelectorAll(`[data-bar="${d.id}"]`).forEach(b => b.style.width = (s.yours/s.msN*100)+"%"); });
}});
