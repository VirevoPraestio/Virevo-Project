/* ===== Page 4 · Simulate: move the changes your six bring in, and watch the six move ===== */
/* How the simulation works (plain): only the changes you switch on move anything. Each change moves the numbers it affects,
   in proportion to how far you take it (from today towards best practice) and how strong the link is. Those numbers move
   the next ones, up to the six KPIs. Changes take time: staff are hired over about 3 months, equipment arrives over about 6,
   process changes take hold within a month, and an automation works from its go-live month, building up over 2 months. */
const RAMP = { w:[1,1], s:[1,1], p:[1,3], k:[1,6], a:[null,2] };   /* [start month, months to full effect] */
const S4 = { on:{}, val:{}, start:{}, month:12, saved:[] };
function changes4(){ const c = cover3(); return Object.keys(c.lev).sort((a,b)=> (c.lev[b]-c.lev[a]) || ITEMS[a].n.localeCompare(ITEMS[b].n)); }
function kind4(id){ return leverKind(ITEMS[id]); }
function init4(){ changes4().forEach(id => { if (S4.on[id] === undefined) S4.on[id] = true; if (S4.val[id] === undefined) S4.val[id] = valOf(id); if (S4.start[id] === undefined) S4.start[id] = kind4(id)==="a" ? (TS.go[id] || 3) : RAMP[kind4(id)][0]; }); }
function active4(id){ return !!S4.on[id] && (!isSwitch(ITEMS[id]) || S4.val[id] >= .5); }
function rampOf(id, m){ const k = kind4(id), len = RAMP[k][1], st = S4.start[id] ?? 1; return Math.max(0, Math.min(1, (m - st + 1) / len)); }
function leverFrac(id, m, off){ if (off === id || !active4(id)) return 0; const it = ITEMS[id]; const f = it.b === it.t ? (S4.val[id] === it.b ? 1 : 0) : Math.max(0, Math.min(1, (S4.val[id] - it.t)/(it.b - it.t))); return f * rampOf(id, m); }
function simFracs(m = S4.month, off = null){ const memo = {}, active = new Set(changes4());
  const f = id => { if (id in memo) return memo[id]; const it = ITEMS[id]; if (isLever(it)) return memo[id] = active.has(id) ? leverFrac(id, m, off) : 0;
    memo[id] = 0; const ins = INPUTS[id] || []; if (!ins.length) return 0; const tw = ins.reduce((s,x)=>s+x[1],0); return memo[id] = ins.reduce((s,[x,w]) => s + w*f(x), 0) / tw; };
  return f; }
function simVal(id, m = S4.month, off = null){ const it = ITEMS[id]; return it.t + simFracs(m, off)(id) * (it.b - it.t); }
function status4(id, m = S4.month){ const fs = simFracs(m)(id), ft = Math.min(1, fracOf(id)); return fs >= ft - 0.03 ? "hit" : fs >= ft*0.6 ? "near" : "far"; }
const ST4 = { hit:"Reaches your target", near:"Close to your target", far:"Well short of your target" };
function topHelpers4(kid, n=3){ const base = simFracs()(kid); return changes4().map(l => [l, base - simFracs(S4.month, l)(kid)]).filter(x => x[1] > 0.002).sort((a,b)=>b[1]-a[1]).slice(0,n); }
function deltaWords(id, df){ const it = ITEMS[id]; const d = Math.abs(df*(it.b - it.t)); return it.u.startsWith("%") ? `${d.toFixed(1)} points` : `${d.toLocaleString("en-IN",{maximumFractionDigits: it.dp||1})} ${unitOf(it)}`; }
function movedOthers(n=8){ const f = simFracs(); const six = new Set(S3.sel);
  return shownIds().filter(id => !isLever(ITEMS[id]) && !six.has(id) && f(id) > 0.02).sort((a,b)=>f(b)-f(a)).slice(0,n); }
function counts4(){ const ch = changes4(); return { n: ch.length, on: ch.filter(id=>active4(id)).length, hit: S3.sel.filter(id=>status4(id)==="hit").length }; }
const p4listeners = []; const changed4 = () => p4listeners.forEach(fn=>fn());
function saveScenario4(){ const name = "ABC"[S4.saved.length % 3]; const snap = { name, on:{...S4.on}, val:{...S4.val}, start:{...S4.start}, res: Object.fromEntries(S3.sel.map(id=>[id, simVal(id, 12)])) };
  S4.saved = S4.saved.filter(s => s.name !== name); S4.saved.push(snap); S4.saved.sort((a,b)=>a.name.localeCompare(b.name)); toast(`Saved as scenario ${name}. Page 5 will cost each saved scenario.`); changed4(); }
function loadScenario4(n){ const s = S4.saved.find(x=>x.name===n); if (!s) return; S4.on = {...s.on}; S4.val = {...s.val}; S4.start = {...s.start}; toast(`Scenario ${n} loaded.`); changed4(); }
function fmtMonth(m){ return `month ${m}`; }

/* ---------- shared parts ---------- */
function p4Head(title, lede){ return `<div class="p2head"><div><div class="eb">Simulation · step 4 of 7 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>${title}</h1><p class="lede">${lede}</p></div>
  <div class="pulse" role="group" aria-label="Readings">
    <button type="button" class="pz" data-ref="p4:hit"><span class="pl">Of your six, reaching target</span><b data-v="p4hit"></b><small data-v="p4hitSub"></small></button>
    <button type="button" class="pz" data-ref="p4:on"><span class="pl">Changes switched on</span><b data-v="p4on"></b><small>of the ones your six bring in</small></button>
    <button type="button" class="pz" data-ref="p4:month"><span class="pl">Showing</span><b data-v="p4m"></b><small>move the month below</small></button>
    <button type="button" class="pz" data-ref="p4:saved"><span class="pl">Scenarios saved</span><b data-v="p4s"></b><small data-v="p4sSub"></small></button></div></div>`; }
function monthBarHTML(){ return `<div class="mbar"><label for="m4">Month of the project</label><input id="m4" type="range" min="1" max="12" step="1" data-m4><output data-v="m4o"></output>
  <div class="scen"><button type="button" class="act" data-p4="save">Save as a scenario</button><span data-v="scenbtns"></span></div></div>`; }
function changeControl4(id){ const it = ITEMS[id];
  if (isSwitch(it)) return `<button type="button" class="sw" data-sw4="${id}" aria-pressed="false">On</button>${it.x==="a"?`<label class="sr-only" for="st4-${id}">Go-live month</label><select class="gomo" id="st4-${id}" data-st4="${id}">${Array.from({length:12},(_,i)=>`<option value="${i+1}">Live in month ${i+1}</option>`).join("")}</select>`:""}`;
  const [mn,mx] = rangeOf(it); return `<label class="sr-only" for="v4-${id}">Level for ${esc(it.n)}</label><input class="num" id="v4-${id}" type="number" step="${stepOf(it)}" min="${mn}" max="${mx}" data-v4="${id}" inputmode="decimal">`; }
function wire4(root){
  root.querySelectorAll("[data-m4]").forEach(r => r.addEventListener("input", () => { S4.month = +r.value; changed4(); }));
  root.querySelectorAll("[data-inc4]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); const id = b.dataset.inc4; if (isSwitch(ITEMS[id])) { const now = active4(id); S4.on[id] = true; S4.val[id] = now ? 0 : 1; } else S4.on[id] = !S4.on[id]; changed4(); }));
  root.querySelectorAll("[data-sw4]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); const id = b.dataset.sw4; S4.val[id] = S4.val[id] >= .5 ? 0 : 1; changed4(); }));
  root.querySelectorAll("[data-st4]").forEach(s => s.addEventListener("change", () => { S4.start[s.dataset.st4] = +s.value; changed4(); }));
  root.querySelectorAll("[data-v4]").forEach(n => n.addEventListener("change", () => { const id = n.dataset.v4, it = ITEMS[id]; if (n.value === "") S4.val[id] = valOf(id); else S4.val[id] = Math.round(+n.value/stepOf(it))*stepOf(it); changed4(); }));
  root.querySelectorAll("[data-r4]").forEach(r => r.addEventListener("input", () => { const id = r.dataset.r4, it = ITEMS[id]; S4.val[id] = Math.round(+r.value/stepOf(it))*stepOf(it); changed4(); }));
  root.querySelectorAll("[data-p4]").forEach(b => b.addEventListener("click", () => { const a = b.dataset.p4;
    if (a==="save") saveScenario4(); else if (a==="go") goNext4(); else if (a==="all") { changes4().forEach(id => S4.on[id] = true); changed4(); } else if (a==="none") { changes4().forEach(id => { S4.on[id] = false; if (isSwitch(ITEMS[id])) S4.val[id] = 0; }); changed4(); }
    else if (a==="reset") { S4.val = {}; S4.start = {}; S4.on = {}; init4(); changed4(); } }));
  root.addEventListener("click", e => { const b = e.target.closest("[data-load4]"); if (b) loadScenario4(b.dataset.load4); });
}
function sync4(root){ const c = counts4(); const set = (k,v) => root.querySelectorAll(`[data-v="${k}"]`).forEach(e => e.innerHTML = v);
  set("p4hit", `${c.hit}<i>/${S3.sel.length}</i>`); set("p4hitSub", `by ${fmtMonth(S4.month)}`);
  set("p4on", `${c.on}<i>/${c.n}</i>`); set("p4m", `Month ${S4.month}`); set("p4s", `${S4.saved.length}`); set("p4sSub", S4.saved.length ? S4.saved.map(s=>s.name).join(", ") : "save one to compare later");
  set("m4o", `Month ${S4.month}${S4.month===12?" · the end of year one":""}`);
  set("scenbtns", S4.saved.map(s => `<button type="button" class="act ghost" data-load4="${s.name}">Load ${s.name}</button>`).join(""));
  set("p4cta", S4.saved.length ? `${S4.saved.length} scenario${S4.saved.length>1?"s":""} saved. Page 5 adds the cost and time of each.` : "Save at least one scenario to carry it to page 5.");
  root.querySelectorAll("[data-m4]").forEach(r => { if (document.activeElement !== r) r.value = S4.month; });
  root.querySelectorAll("[data-inc4]").forEach(b => { const on = active4(b.dataset.inc4); b.setAttribute("aria-pressed", on); b.textContent = on ? "In the plan" : "Left out"; });
  root.querySelectorAll("[data-chg]").forEach(r => r.classList.toggle("off", !active4(r.dataset.chg)));
  root.querySelectorAll("[data-sw4]").forEach(b => { const on = S4.val[b.dataset.sw4] >= .5; b.setAttribute("aria-pressed", on); b.textContent = ITEMS[b.dataset.sw4].x==="a" ? (on?"Switched on":"Off") : (on?"Yes":"No"); });
  root.querySelectorAll("[data-st4]").forEach(s => s.value = S4.start[s.dataset.st4]);
  root.querySelectorAll("[data-v4]").forEach(n => { if (document.activeElement !== n) n.value = S4.val[n.dataset.v4]; });
  root.querySelectorAll("[data-r4]").forEach(r => { if (document.activeElement !== r) r.value = S4.val[r.dataset.r4]; });
  root.querySelectorAll("[data-sv]").forEach(e => e.textContent = fmtV(e.dataset.sv, simVal(e.dataset.sv)));
  root.querySelectorAll("[data-st]").forEach(e => { const s = status4(e.dataset.st); e.textContent = ST4[s]; e.dataset.state = s; });
  root.querySelectorAll('[data-p4="go"]').forEach(b => b.classList.toggle("ready", S4.saved.length > 0)); }
function p4Cta(){ return `<div class="cta"><button type="button" class="go" data-p4="go">Take my scenarios to What's possible <span aria-hidden="true">→</span></button><span class="cta-note" data-v="p4cta"></span></div>`; }
function goNext4(){ if (!S4.saved.length) { toast("Save at least one scenario first."); return; } toast(`${S4.saved.length} scenario${S4.saved.length>1?"s":""} ready for page 5, What's possible. That page comes in the next round.`); }
function p4Mount(stage, inner){ init4(); stage.innerHTML = `<div class="lk lk-web">${journeyHTML(3)}${inner}</div>`; wire4(stage); }

/* ---------- details and chat ---------- */
function p4_detailFor(ref){ const [t,id] = ref.split(":");
  if (t==="it" && S3.sel.includes(id)) { const [h,st] = p2_detailFor(ref); const it = ITEMS[id], hs = topHelpers4(id, 5);
    return [`<div class="d-eyebrow">One of your six · ${esc(GNAME[it.g])}</div><div class="d-title">${esc(it.n)}</div>
      <div class="d-four"><div><span>${hasData(id)?"Today":"Typical start"}</span><b>${fmtV(id,it.t)}</b></div><div class="now"><span>Simulated, ${fmtMonth(S4.month)}</span><b>${fmtV(id, simVal(id))}</b></div><div><span>Your target</span><b>${fmtV(id)}</b></div><div><span>Best practice</span><b>${fmtV(id,it.b)}</b></div></div>
      <p class="d-sub"><span class="d-pill ${status4(id)==="hit"?"ahead":status4(id)==="near"?"watch":"off"}">${ST4[status4(id)]}</span></p>
      <div class="d-sec"><h4>The changes doing the most for it</h4><ul class="d-ms">${hs.map(([l,d])=>`<li><span class="src src-yours">${esc({a:"Automation",k:"Equipment",w:"Process",p:"Staff"}[kind4(l)])}</span><span><b>${esc(ITEMS[l].n)}</b> · without it, ${esc(it.n)} would be about ${esc(deltaWords(id, d))} worse</span></li>`).join("") || "<li><span></span><span>No change in your plan reaches it yet.</span></li>"}</ul></div>
      <div class="d-why"><span>How we look at it</span>${esc(it.why)}</div>`, st]; }
  if (t==="it") { const it = ITEMS[id]; if (isLever(it)) { const k = kind4(id), r = RAMP[k];
      return [`<div class="d-eyebrow">A change · ${esc(KINDNAME[k])}</div><div class="d-title">${esc(it.n)}</div>
        <p class="d-sub">${S4.on[id]?"In the plan":"Left out of the plan"} · level ${esc(withU(id, S4.val[id]))} (today ${esc(withU(id, it.t))}, best ${esc(withU(id, it.b))})</p>
        <div class="d-why"><span>How we look at it</span>${esc(it.why)}</div>
        <div class="d-sec"><h4>How long it takes</h4><p style="margin:0">${k==="a"?`Goes live in month ${S4.start[id]} and reaches full effect about ${r[1]} months later.`:k==="k"?"Bought and installed over about six months, starting in month "+S4.start[id]+".":k==="p"?"Hired and trained over about three months, starting in month "+S4.start[id]+".":"Takes hold within a month of starting, in month "+S4.start[id]+"."}</p></div>
        <div class="d-sec"><h4>What it affects downstream</h4><ul class="d-ms">${(OUTPUTS[id]||[]).map(o=>`<li><span class="src src-yours">affects</span><span><b>${esc(ITEMS[o].n)}</b></span></li>`).join("")}</ul></div>`, "ahead"]; }
    return p2_detailFor(ref); }
  if (t==="p4") return [`<div class="d-eyebrow">How the simulation works</div><div class="d-title">Only the changes you switch on move anything</div>
    <p style="margin:0 0 8px">Each change moves the numbers it affects, in proportion to how far you take it (from today towards best practice) and how strong the link is. Those numbers move the next ones, up to your six.</p>
    <p style="margin:0">Changes take time: staff are hired over about three months, equipment over about six, process changes within a month, and an automation works from its go-live month, building up over two months. Move the month to see the year unfold.</p>
    <div class="d-sec"><h4>Your six, ${fmtMonth(S4.month)}</h4><ul class="d-list">${S3.sel.map(s=>`<li><span class="ck ${status4(s)==="hit"?"y":"late"}">${status4(s)==="hit"?"✓":"!"}</span><span>${esc(ITEMS[s].n)}: ${esc(withU(s, simVal(s)))}</span><em>target ${esc(withU(s))}</em></li>`).join("")}</ul></div>`, "watch"];
  return ["",""]; }
function p4_peekFor(ref){ const [t,id] = ref.split(":"); if (t==="it") { const it = ITEMS[id];
    if (isLever(it)) return `<div class="pk-t">${esc(it.n)}</div><div class="pk-m">${S4.on[id]?"In the plan":"Left out"} · level ${esc(withU(id, S4.val[id]))}</div><div class="pk-hint">Click for how long it takes and what it affects</div>`;
    return `<div class="pk-t">${esc(it.n)}</div><div class="pk-n">${esc(fmtV(id, simVal(id)))}</div><div class="pk-m">Today ${esc(fmtV(id,it.t))} · target ${esc(fmtV(id))} · ${fmtMonth(S4.month)}</div>${S3.sel.includes(id)?`<div class="pk-m"><b>${ST4[status4(id)]}</b></div>`:""}`; }
  return `<div class="pk-t">How the simulation works</div><div class="pk-hint">Click to read it</div>`; }
function p4_contextFor(ref){ const [t,id] = ref.split(":"); if (t==="it") { const it = ITEMS[id]; return { kind: isLever(it)?"Change":"KPI", point:`${it.n} in this scenario`, title:it.n, lines:[isLever(it)?`${S4.on[id]?"In the plan":"Left out"} · level ${withU(id, S4.val[id])}`:`Simulated ${withU(id, simVal(id))} by ${fmtMonth(S4.month)} · target ${withU(id)}`] }; } return { kind:"Scenario", point:"this scenario", title:"Scenario", lines:[] }; }
function p4_chatOpening(){ const c = counts4(); const miss = S3.sel.filter(id => status4(id)!=="hit");
  return { msg:[ `I have switched on all ${c.n} changes your six bring in, each at the level you set on page 2. By ${fmtMonth(S4.month)}, ${c.hit} of your six reach their target.`,
      miss.length ? `${miss.map(id => `${ITEMS[id].n} reaches ${withU(id, simVal(id))} against ${withU(id)}`).join("; ")}. The biggest help would come from pushing ${topHelpers4(miss[0],2).map(x=>ITEMS[x[0]].n).join(" and ") || "more changes"} further.` : "All six reach their targets.",
      "Switch changes off to see what each one is worth, move the month to see when results arrive, and save the versions you like as scenarios." ],
    note: miss.length ? `${ITEMS[miss[0]].n} needs more.` : "All six on target.",
    points: [ ...miss.slice(0,2).map(id => `${ITEMS[id].n}: ${withU(id, simVal(id))} against ${withU(id)}`), `${c.on} of ${c.n} changes switched on`, "When the results arrive" ],
    asks: [ "Which change is worth the most?", "What happens if we skip the hiring?", "How does the simulation work?" ] }; }
function p4_fillChat(){ const c = p4_chatOpening();
  document.getElementById("chatSub").textContent = "Simulation · step 4 of 7 · simulate";
  chatBody.innerHTML = `<div class="msg">${c.msg.map(m=>`<p>${esc(m)}</p>`).join("")}</div><div class="lbl">Tojo's note</div><div class="note">${esc(c.note)}</div>
  <div class="lbl">Add to a point — pick one or more</div>${c.points.map((t,i)=>`<button class="pt" type="button" aria-pressed="false"><b>P${i+1}</b> ${esc(t)}</button>`).join("")}
  <div class="lbl">Or ask next</div>${c.asks.map(t=>`<button class="ask" type="button">${esc(t)}</button>`).join("")}`;
  chatBody.querySelectorAll(".pt").forEach(b => b.onclick = () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")==="true"?"false":"true"));
  chatBody.querySelectorAll(".ask").forEach(b => b.onclick = () => { chatIn.value = b.textContent; chatIn.focus(); }); }
function p4_replyFor(text, ctx){ const q = text.toLowerCase();
  if (q.includes("worth the most")) { const tot = {}; S3.sel.forEach(k => topHelpers4(k, 30).forEach(([l,d]) => tot[l] = (tot[l]||0) + d)); const top = Object.entries(tot).sort((a,b)=>b[1]-a[1]).slice(0,3);
    return [ `Across your six, the changes that matter most are ${top.map(([l])=>ITEMS[l].n).join(", ")}.`, "I measured this by switching each change off in turn and seeing how far your six fall. Costs come on page 5, so the best value may still be a smaller change." ]; }
  if (q.includes("hiring")) { const f = simFracs(S4.month, null), hires = changes4().filter(id=>kind4(id)==="p"); const before = S3.sel.map(id=>[id, simVal(id)]);
    const keep = {...S4.on}; hires.forEach(id => S4.on[id] = false); const after = S3.sel.map(id=>[id, simVal(id)]); S4.on = keep;
    return [ `Without the ${hires.length} staffing changes: ${after.map(([id,v],i)=>`${ITEMS[id].n} ${withU(id, v)} (instead of ${withU(id, before[i][1])})`).join("; ")}.`, "I have not changed your plan. Switch the staff numbers off on the page to try it." ]; }
  if (q.includes("how does")) return [ "Only the changes you switch on move anything. Each change moves the numbers it affects, in proportion to how far you take it and how strong the link is, and those move the next ones up to your six.", "Changes take time: hiring about three months, equipment about six, process changes a month, automations from their go-live month." ];
  if (ctx && ctx.ref) { const [,id] = ctx.ref.split(":"); const it = ITEMS[id]; if (it) return isLever(it) ? [ `${it.n} is ${S4.on[id]?"in the plan":"left out"} at ${withU(id, S4.val[id])}.`, it.why ] : [ `${it.n}: ${withU(id, simVal(id))} by ${fmtMonth(S4.month)}, target ${withU(id)}.`, topHelpers4(id,3).length ? `It depends most on ${topHelpers4(id,3).map(x=>ITEMS[x[0]].n).join(", ")}.` : "No change in the plan reaches it yet." ]; }
  return [ `${counts4().hit} of your six reach target by ${fmtMonth(S4.month)}.`, "Ask about any change or KPI on the page." ]; }
function p4_fillCommon(){}
