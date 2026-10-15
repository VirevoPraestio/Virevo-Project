/* ===== Page 4 · Simulate (rebuilt 14 Oct): Achievable or Dream, approve the changes, see the six move, freeze one plan =====
   Achievable = the KPI values that are realistic in 12 months (page 2's realistic values).
   Dream      = the KPI targets the user set on page 2.
   For each scenario we work out the level each change must reach: if every change that affects a KPI is taken a share F of the way
   from today to best practice, the KPI moves F × (its reach), where reach is how far it can move with only these changes.
   So the level a change needs = the KPI's required move ÷ its reach, taken over the six KPIs it affects (the highest one wins).
   Achievable levels are also capped at each change's own realistic value; Dream levels are not.
   Only approved changes move anything, and only approved changes cost money. */
const SIMR = { lvl:{}, own:{}, start:{}, frozen:null };
const RAMP5 = { w:1, s:1, p:3, k:6, a:2 };
function ch5(){ const c = cover3(); return Object.keys(c.lev).sort((a,b)=> (c.lev[b]-c.lev[a]) || ITEMS[a].n.localeCompare(ITEMS[b].n)); }
function startOf5(id){ const k = leverKind(ITEMS[id]); return SIMR.start[id] ?? (k==="a" ? (TS.go[id] || 3) : 1); }
function ramp5(id, m){ const k = leverKind(ITEMS[id]); return Math.max(0, Math.min(1, (m - startOf5(id) + 1) / RAMP5[k])); }
const lvFrac = (id, v) => { const it = ITEMS[id]; if (it.b === it.t) return v === it.b ? 1 : 0; return Math.max(0, Math.min(1, (v - it.t)/(it.b - it.t))); };
/* the simulation: approved changes only */
function fr5(m = 24, over = null){ const memo = {}, set = new Set(ch5()); const L = over || SIMR.lvl;
  const f = id => { if (id in memo) return memo[id]; const it = ITEMS[id];
    if (isLever(it)) { if (!set.has(id)) return memo[id] = 0; const v = valueOf5(id, L); return memo[id] = v===null ? 0 : lvFrac(id, v) * ramp5(id, m); }
    memo[id] = 0; const ins = INPUTS[id] || []; if (!ins.length) return 0; const tw = ins.reduce((s,x)=>s+x[1],0); return memo[id] = ins.reduce((s,[x,w]) => s + w*f(x), 0) / tw; };
  return f; }
function val5(id, m = 24, over = null){ const it = ITEMS[id]; return it.t + fr5(m, over)(id) * (it.b - it.t); }
/* reach: how far a KPI can move if every change affecting it goes to best practice */
const _reach = {};
function reach5(k){ if (k in _reach) return _reach[k]; const all = {}; ch5().forEach(l => all[l] = "best"); const memo = {}, set = new Set(ch5());
  const f = id => { if (id in memo) return memo[id]; const it = ITEMS[id]; if (isLever(it)) return memo[id] = set.has(id) ? 1 : 0; memo[id] = 0; const ins = INPUTS[id]||[]; if (!ins.length) return 0; const tw = ins.reduce((s,x)=>s+x[1],0); return memo[id] = ins.reduce((s,[x,w])=>s+w*f(x),0)/tw; };
  return _reach[k] = f(k); }
function goal5(k, mode){ const it = ITEMS[k]; return mode === "ach" ? it.r : valOf(k); }
function need5(k, mode){ return Math.min(1, fracOf(k, goal5(k, mode))); }
function levelFor(id, mode){ const it = ITEMS[id]; let F = 0;
  S3.sel.forEach(k => { if (!leversOf(k).includes(id)) return; const r = reach5(k); if (r <= 0.001) return; F = Math.max(F, Math.min(1, need5(k, mode) / r)); });
  if (mode === "ach") F = Math.min(F, lvFrac(id, it.r));
  if (isSwitch(it)) return F >= 0.5 ? 1 : 0;
  const st = stepOf(it); let v = it.t + F*(it.b - it.t); v = Math.round(v/st)*st; return v; }
const LV = {}; function levels5(){ for (const k in _reach) delete _reach[k]; ch5().forEach(id => LV[id] = { ach: levelFor(id,"ach"), drm: levelFor(id,"drm") }); }
function valueOf5(id, L = SIMR.lvl){ const c = L[id]; if (!c || c === "off") return null; if (c === "own") return SIMR.own[id] ?? LV[id].drm; return LV[id][c]; }
function approved5(){ return ch5().filter(id => valueOf5(id) !== null && valueOf5(id) !== ITEMS[id].t); }
function resetCost5(id){ delete SIMR.tot[id]; delete SIMR.ucOne[id]; delete SIMR.ucMo[id]; }
function setAll5(mode){ ch5().forEach(id => { SIMR.lvl[id] = mode; resetCost5(id); }); if (mode !== "off") GOALMODE = mode; changed5(); }
/* ---------- money: "Approve the Cost" ----------
   Every change has units, a one-time cost per unit, a monthly cost per unit, and a total cost.
   Total cost (formula) = units × (one-time per unit + monthly per unit × project length in months).
   Changing the units or either unit cost recalculates the total. Any value can be typed in by hand and need not match
   the formula; the plan uses the last value, calculated or typed. Clicking Not approved, Achievable or Dream puts every
   value back to the calculated one (units, both unit costs and the total).
   Monthly cost = units × monthly per unit (used for the Monthly cost tile and break-even).
   The rest of the total (total − monthly × project length) is treated as one-time cost. */
SIMR.ucOne = {}; SIMR.ucMo = {}; SIMR.tot = {}; SIMR.D = 12;
const isCount = id => ITEMS[id].d > 0 && ITEMS[id].u !== "time";
function unitsAdded(id, v){ const it = ITEMS[id]; if (v === null) return 0; if (isSwitch(it)) return v >= .5 && it.t < .5 ? 1 : 0; return it.d > 0 ? Math.max(0, +(v - it.t).toFixed(4)) : 0; }
const ucOne = id => SIMR.ucOne[id] ?? ((COSTS[id]||{}).one || 0);
const ucMo  = id => SIMR.ucMo[id]  ?? ((COSTS[id]||{}).mo  || 0);
function unitsOf5(id){ return unitsAdded(id, valueOf5(id)); }
function autoTot(id){ return Math.round(unitsOf5(id) * (ucOne(id) + ucMo(id) * SIMR.D)); }
function totOf(id){ return valueOf5(id) === null ? 0 : (SIMR.tot[id] ?? autoTot(id)); }
function cost5(id){ if (valueOf5(id) === null) return { one:0, mo:0, tot:0 }; const mo = unitsOf5(id) * ucMo(id), tot = totOf(id); return { one: tot - mo*SIMR.D, mo, tot }; }
const rs = r => `₹${Math.round(r).toLocaleString("en-IN")}`;
const parseRs = s => { const n = parseFloat(String(s).replace(/[^0-9.]/g, "")); return isNaN(n) ? null : n; };
const L_ = r => r/100000;   /* rupees to lakh */
function money(l){ if (Math.abs(l) > 0 && Math.abs(l) < 1) return `₹${Math.round(l*100000).toLocaleString("en-IN")}`; if (Math.abs(l) >= 100) return `₹${(l/100).toLocaleString("en-IN",{maximumFractionDigits:2})} Cr`; return `₹${l.toLocaleString("en-IN",{maximumFractionDigits:1})} L`; }
function ebitdaL(m){ const eb = val5("EBITDA", m), rv = val5("REV", m); return eb/100*rv; }
function summary5(){ const ids = approved5(); let one = 0, mo = 0, tot = 0; ids.forEach(id => { const c = cost5(id); one += L_(c.one); mo += L_(c.mo); tot += L_(c.tot); });
  const base = ITEMS.EBITDA.t/100*ITEMS.REV.t;
  let cum = 0, be = null; const start1 = {}; ids.forEach(id => start1[id] = startOf5(id));
  for (let m = 1; m <= 60; m++){ const gain = ebitdaL(m) - base; const oneNow = ids.filter(id => start1[id] === m).reduce((s,id)=>s+L_(cost5(id).one),0); const moNow = ids.filter(id => start1[id] <= m).reduce((s,id)=>s+L_(cost5(id).mo),0);
    cum += gain - moNow - oneNow; if (be === null && m > 1 && cum >= 0) be = m; }
  const full = ids.length ? Math.max(...ids.map(id => startOf5(id) + RAMP5[leverKind(ITEMS[id])] - 1)) : 0;
  let reach = null; for (let m = 1; m <= 24; m++){ if (S3.sel.every(k => onGoal5(k, m))) { reach = m; break; } }
  const gainFull = ebitdaL(24) - base;
  return { one, mo, tot, D: SIMR.D, gainFull, net: gainFull - mo, be, full, reach, n: ids.length, hit: S3.sel.filter(k => onGoal5(k, 24)).length }; }
let GOALMODE = "ach";
function onGoal5(k, m = 24, mode = GOALMODE){ return fr5(m)(k) >= need5(k, mode) - 0.02; }
const p5listeners = []; const changed5 = () => p5listeners.forEach(fn=>fn());

/* ---------- shared parts ---------- */
function kpiPanel5(){ return `<aside class="kp5" aria-label="Selected KPIs"><div class="kp5-top"><h2>Selected KPIs</h2>
    <div class="seg" role="group" aria-label="Compare with"><button type="button" data-goal="ach">Achievable</button><button type="button" data-goal="drm">Dream</button></div></div>
    <ul>${S3.sel.map(k => `<li class="k5" data-k5="${k}"><div class="k5-h">${nameBtn(k)}<span class="k5-s" data-k5s="${k}"></span></div>
      <div class="k5-v"><b data-k5v="${k}"></b><small>${esc(unitOf(ITEMS[k]))}</small><em data-k5d="${k}"></em></div>
      <div class="k5-line"><i class="tr"></i><i class="fill" data-k5f="${k}"></i><i class="mk a" data-k5a="${k}" title="Achievable"></i><i class="mk d" data-k5dr="${k}" title="Dream"></i></div>
      <div class="k5-n"><span>Today <b>${esc(fmtV(k, ITEMS[k].t))}</b></span><span class="a">Achievable <b>${esc(fmtV(k, ITEMS[k].r))}</b></span><span class="d">Dream <b>${esc(fmtV(k))}</b></span></div></li>`).join("")}</ul>
    <div class="kp5-key"><span><i class="kf"></i>With approved changes</span><span><i class="ka"></i>Achievable</span><span><i class="kd"></i>Dream</span></div></aside>`; }
function topStrip5(){ return `<section class="top5" aria-label="Plan summary">
    <div class="t5" data-ref="sim:cost"><span>Total cost</span><b data-v="t5tot"></b><small data-noopen>over <input class="dur" type="number" min="1" max="60" step="1" data-dur aria-label="Project length in months"> months · <em data-v="t5totS" style="font-style:normal"></em></small></div>
    <div class="t5" data-ref="sim:mo"><span>Monthly cost</span><b data-v="t5mo"></b><small>once all changes are in place</small></div>
    <div class="t5" data-ref="sim:gain"><span>Extra EBITDA</span><b data-v="t5gain"></b><small data-v="t5gainS"></small></div>
    <div class="t5" data-ref="sim:be"><span>Break-even</span><b data-v="t5be"></b><small data-v="t5beS"></small></div>
    <div class="t5" data-ref="sim:time"><span>Full results in</span><b data-v="t5full"></b><small data-v="t5fullS"></small></div>
    <div class="t5 hl" data-ref="sim:hit"><span>KPIs on target</span><b data-v="t5hit"></b><small data-v="t5hitS"></small></div></section>`; }
function bulk5(){ return `<div class="bulk5"><span>Approve all at:</span><button type="button" class="act" data-all5="ach">Achievable</button><button type="button" class="act" data-all5="drm">Dream</button><button type="button" class="act ghost" data-all5="off">Clear all</button><button type="button" class="go ready frz" data-freeze>Freeze this plan</button></div>`; }
const lvLabel = (id, v) => v === ITEMS[id].t ? "Not needed" : fmtV(id, v);
function choiceHTML(id){ const it = ITEMS[id], L = LV[id], cnt = isCount(id) || isSwitch(it);
  return `<div class="ch5 sw3" role="group" aria-label="Level for ${esc(it.n)}">
    <button type="button" data-pick5="${id}:off"><small>Not approved</small><b>Today ${esc(fmtV(id,it.t))}</b></button>
    <button type="button" data-pick5="${id}:ach" class="a"><small>Achievable</small><b>${esc(lvLabel(id,L.ach))}</b></button>
    <button type="button" data-pick5="${id}:drm" class="d"><small>Dream</small><b>${esc(lvLabel(id,L.drm))}</b></button></div>
    <div class="ac5" data-ac5="${id}" data-noopen role="group" aria-label="Approve the cost of ${esc(it.n)}"><div class="ac5-h">Approve the Cost<button type="button" class="ac5-r" data-acr="${id}" hidden>Use formula</button></div>
      <label><small>${cnt ? (isSwitch(it) ? "Units (1 = on)" : `Units added`) : ITEMS[id].u==="time" ? "New time (9.5 = 9:30)" : "New level"}</small><input class="num" type="number" min="0" step="${cnt?(isSwitch(it)?1:stepOf(it)):stepOf(it)}" ${isSwitch(it)?'max="1"':""} data-acu="${id}" aria-label="${cnt?"Units":"New level"} for ${esc(it.n)}"></label>
      <label><small>Total cost</small><input class="num tot" type="text" inputmode="numeric" data-actot="${id}" aria-label="Total cost for ${esc(it.n)}"></label>
      <label><small>One-time, each</small><input class="num" type="text" inputmode="numeric" data-acc1="${id}" aria-label="One-time cost per unit for ${esc(it.n)}"></label>
      <label><small>Monthly, each</small><input class="num" type="text" inputmode="numeric" data-accm="${id}" aria-label="Monthly cost per unit for ${esc(it.n)}"></label></div>`; }
function costLine5(id){ return `<span class="cl" data-cl="${id}"></span>`; }
function wire5(root){
  root.querySelectorAll("[data-goal]").forEach(b => b.addEventListener("click", () => { GOALMODE = b.dataset.goal; changed5(); }));
  root.querySelectorAll("[data-all5]").forEach(b => b.addEventListener("click", () => setAll5(b.dataset.all5)));
  root.querySelectorAll("[data-pick5]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); const [id,c] = b.dataset.pick5.split(":"); SIMR.lvl[id] = c; resetCost5(id); changed5(); }));
  root.querySelectorAll("[data-acu]").forEach(n => n.addEventListener("change", () => { const id = n.dataset.acu, it = ITEMS[id];
    if (n.value === "") { SIMR.lvl[id] = "off"; } else { const u = +n.value; SIMR.own[id] = (isCount(id) || isSwitch(it)) ? Math.min(isSwitch(it) ? 1 : 1e9, it.t + u) : u; SIMR.lvl[id] = "own"; }
    delete SIMR.tot[id]; changed5(); }));
  [["acc1","ucOne"],["accm","ucMo"]].forEach(([a,k]) => root.querySelectorAll(`[data-${a}]`).forEach(n => n.addEventListener("change", () => { const id = n.dataset[a], v = parseRs(n.value); if (v === null) delete SIMR[k][id]; else SIMR[k][id] = v; delete SIMR.tot[id]; changed5(); })));
  root.querySelectorAll("[data-dur]").forEach(n => { n.addEventListener("click", e => e.stopPropagation()); n.addEventListener("change", () => { const v = Math.round(+n.value); if (v >= 1 && v <= 60) SIMR.D = v; changed5(); }); });
  root.querySelectorAll("[data-actot]").forEach(n => n.addEventListener("change", () => { const id = n.dataset.actot, v = parseRs(n.value);
    if (v === null) delete SIMR.tot[id]; else { SIMR.tot[id] = v; if (valueOf5(id) === null) SIMR.lvl[id] = GOALMODE; } changed5(); }));
  root.querySelectorAll("[data-acr]").forEach(b => b.addEventListener("click", () => { delete SIMR.tot[b.dataset.acr]; changed5(); }));
  root.querySelectorAll("[data-freeze]").forEach(b => b.addEventListener("click", () => openFreeze5()));
}
function sync5(root){ const s = summary5(); const set = (k,v) => root.querySelectorAll(`[data-v="${k}"]`).forEach(e => e.innerHTML = v);
  set("t5tot", money(s.tot)); set("t5totS", `${s.n} change${s.n===1?"":"s"}`);
  root.querySelectorAll("[data-dur]").forEach(n => { if (document.activeElement !== n) n.value = SIMR.D; });
  set("t5mo", money(s.mo)); set("t5gain", `${money(s.gainFull)}<i> a month</i>`); set("t5gainS", s.net >= 0 ? `${money(s.net)} after monthly costs` : `${money(-s.net)} less than monthly costs`);
  set("t5be", s.be ? `Month ${s.be}` : "Over 5 years"); set("t5beS", s.be ? "when the plan has paid for itself" : "the plan costs more than it earns");
  set("t5full", s.full ? `${s.full} months` : "—"); set("t5fullS", s.reach ? `all KPIs on target by month ${s.reach}` : "not all KPIs reach target");
  set("t5hit", `${s.hit}<i>/${S3.sel.length}</i>`); set("t5hitS", GOALMODE==="ach" ? "compared with Achievable" : "compared with Dream");
  root.querySelectorAll("[data-goal]").forEach(b => b.setAttribute("aria-pressed", b.dataset.goal === GOALMODE));
  const f = fr5(24);
  S3.sel.forEach(k => { const it = ITEMS[k], v = val5(k, 24), ok = onGoal5(k);
    root.querySelectorAll(`[data-k5v="${k}"]`).forEach(e => e.textContent = fmtV(k, v));
    const dlt = v - it.t; root.querySelectorAll(`[data-k5d="${k}"]`).forEach(e => { e.textContent = Math.abs(dlt) < 1e-6 ? "No change" : `${dlt>0?"+":"−"}${fmtV(k, Math.abs(dlt))} from today`; });
    root.querySelectorAll(`[data-k5s="${k}"]`).forEach(e => { e.textContent = ok ? "On target" : f(k) >= need5(k, GOALMODE)*0.6 ? "Close" : "Short"; e.dataset.state = ok ? "hit" : f(k) >= need5(k, GOALMODE)*0.6 ? "near" : "far"; });
    const P = x => (Math.max(0,Math.min(1,x))*100).toFixed(1)+"%";
    root.querySelectorAll(`[data-k5f="${k}"]`).forEach(e => e.style.width = P(f(k)));
    root.querySelectorAll(`[data-k5a="${k}"]`).forEach(e => e.style.left = P(need5(k,"ach")));
    root.querySelectorAll(`[data-k5dr="${k}"]`).forEach(e => e.style.left = P(need5(k,"drm"))); });
  root.querySelectorAll("[data-pick5]").forEach(b => { const [id,c] = b.dataset.pick5.split(":"); const cur = SIMR.lvl[id] || "off"; b.setAttribute("aria-pressed", cur === c); });
  const put = (n, v) => { if (document.activeElement !== n) n.value = v; };
  root.querySelectorAll("[data-ac5]").forEach(box => { const id = box.dataset.ac5, it = ITEMS[id], v = valueOf5(id), on = v !== null;
    box.classList.toggle("own", SIMR.lvl[id] === "own"); box.classList.toggle("set", on);
    const u = box.querySelector("[data-acu]"), t = box.querySelector("[data-actot]");
    put(u, !on ? "" : (isCount(id) || isSwitch(it)) ? +unitsOf5(id).toFixed(2) : v);
    put(box.querySelector("[data-acc1]"), rs(ucOne(id))); put(box.querySelector("[data-accm]"), rs(ucMo(id))); put(t, on ? rs(totOf(id)) : "");
    const edited = on && SIMR.tot[id] !== undefined && SIMR.tot[id] !== autoTot(id); t.classList.toggle("ed", edited);
    box.querySelector("[data-acr]").hidden = !edited; });
  root.querySelectorAll("[data-row5]").forEach(r => { const id = r.dataset.row5; r.classList.toggle("off", valueOf5(id) === null); });
  root.querySelectorAll("[data-cl]").forEach(e => { const id = e.dataset.cl, c = cost5(id), k = leverKind(ITEMS[id]), v = valueOf5(id);
    e.textContent = v === null ? "Not approved. No cost." : v === ITEMS[id].t ? "Not needed for this target. No cost." :
      `${c.tot?money(L_(c.tot))+" over "+SIMR.D+" months":"No cost"}${c.mo?" ("+money(L_(c.mo))+" a month)":""} · full result by month ${startOf5(id)+RAMP5[k]-1}`; }); }
function mount5(stage, inner){ levels5(); ch5().forEach(id => { if (!(id in SIMR.lvl)) SIMR.lvl[id] = "ach"; });
  stage.innerHTML = `<div class="lk lk-web">${journeyHTML(3)}${inner}</div><div class="frz5" data-v="frz" hidden></div>`; wire5(stage);
  const top = stage.querySelector(".top5"); if (top && window.ResizeObserver) { const ro = new ResizeObserver(() => stage.querySelector(".lk").style.setProperty("--t5h", top.offsetHeight + "px")); ro.observe(top); } }
function openFreeze5(){ const box = document.querySelector('[data-v="frz"]'); const s = summary5(); const ids = approved5();
  box.innerHTML = `<div class="frz5-in" role="dialog" aria-modal="true" aria-label="Freeze this plan"><h2>Freeze this plan?</h2>
    <p>This plan will set the budget, the timeline and the tasks for your team. On the next page you check it once more and confirm it.</p>
    <div class="frz5-g"><div><span>Changes approved</span><b>${ids.length}</b></div><div><span>Total cost (${s.D} months)</span><b>${money(s.tot)}</b></div><div><span>Monthly cost</span><b>${money(s.mo)}</b></div><div><span>Break-even</span><b>${s.be?"Month "+s.be:"Over 5 years"}</b></div><div><span>Full results in</span><b>${s.full} months</b></div><div><span>KPIs on target</span><b>${s.hit} of ${S3.sel.length}</b></div></div>
    <ul>${S3.sel.map(k => `<li><b>${esc(ITEMS[k].n)}</b>: ${esc(withU(k, val5(k)))} <small>(today ${esc(withU(k, ITEMS[k].t))}, ${GOALMODE==="ach"?"achievable":"dream"} ${esc(withU(k, goal5(k, GOALMODE)))})</small></li>`).join("")}</ul>
    <div class="frz5-b"><button type="button" class="act ghost" data-frz="no">Go back</button><button type="button" class="go ready" data-frz="yes">Freeze and confirm</button></div></div>`;
  box.hidden = false; box.querySelector('[data-frz="yes"]').focus();
  box.querySelectorAll("[data-frz]").forEach(b => b.onclick = () => { box.hidden = true; if (b.dataset.frz === "yes") { freezeNow5(); goStep(4, "Plan frozen. Next: confirm it."); } }); }
function freezeNow5(){ SIMR.frozen = { at: new Date(), lvl:{...SIMR.lvl}, own:{...SIMR.own}, ucOne:{...SIMR.ucOne}, ucMo:{...SIMR.ucMo}, tot:{...SIMR.tot}, D: SIMR.D, mode: GOALMODE, sel: [...S3.sel] }; }
/* run fn as if the frozen plan were on screen, then put the live plan back */
function withFrozen(fn){ const F = SIMR.frozen; if (!F) return fn(); const keep = { lvl:SIMR.lvl, own:SIMR.own, ucOne:SIMR.ucOne, ucMo:SIMR.ucMo, tot:SIMR.tot, D:SIMR.D, mode:GOALMODE };
  Object.assign(SIMR, { lvl:F.lvl, own:F.own, ucOne:F.ucOne, ucMo:F.ucMo, tot:F.tot, D:F.D }); GOALMODE = F.mode;
  try { return fn(); } finally { Object.assign(SIMR, { lvl:keep.lvl, own:keep.own, ucOne:keep.ucOne, ucMo:keep.ucMo, tot:keep.tot, D:keep.D }); GOALMODE = keep.mode; } }

/* ---------- details and chat ---------- */
function sim_detailFor(ref){ const [t,id] = ref.split(":");
  if (t==="it") { const it = ITEMS[id];
    if (isLever(it)) { const L = LV[id], k = leverKind(it), c = COSTS[id]||{}; const hits = S3.sel.filter(s => leversOf(s).includes(id));
      return [`<div class="d-eyebrow">A change · ${esc(KINDNAME[k])}</div><div class="d-title">${esc(it.n)}</div>
        <div class="d-four"><div><span>Today</span><b>${fmtV(id,it.t)}</b></div><div><span>Achievable</span><b>${fmtV(id,L.ach)}</b></div><div><span>Dream</span><b>${fmtV(id,L.drm)}</b></div><div class="now"><span>Approved</span><b>${valueOf5(id)===null?"No":fmtV(id,valueOf5(id))}</b></div></div>
        <div class="d-why"><span>How we look at it</span>${esc(it.why)}</div>
        <div class="d-sec"><h4>How we set these levels</h4><p style="margin:0">Achievable: what ${esc(hits.map(h=>ITEMS[h].n).join(", "))} need to reach their achievable values, but no more than this change can realistically do in 12 months. Dream: what they need to reach the targets you set on page 2.</p></div>
        <div class="d-sec"><h4>Cost</h4><p style="margin:0">${money(L_(ucOne(id)))} one-time and ${money(L_(ucMo(id)))} a month for each unit. Total cost = units × (one-time + monthly × ${SIMR.D} months). Change the units or unit costs under Approve the Cost and the total recalculates; you can also type the total yourself. Full result in about ${RAMP5[k]} month${RAMP5[k]>1?"s":""}.</p></div>
        <div class="d-sec"><h4>What it affects downstream</h4><ul class="d-ms">${(OUTPUTS[id]||[]).map(o=>`<li><span class="src src-yours">affects</span><span><b>${esc(ITEMS[o].n)}</b></span></li>`).join("")}</ul></div>`, "ahead"]; }
    const [h,st] = p2_detailFor(ref); return [h, st]; }
  if (t==="sim") { const s = summary5(); const T = {
      cost:["Total cost", `${money(s.tot)} over ${s.D} months: ${money(s.one)} one-time plus ${money(s.mo)} a month for ${s.D} months. Only approved changes count. Change the project length in this box.`],
      mo:["Monthly cost", `${money(s.mo)} a month once all approved changes are in place: salaries, licences and running costs. One-time costs are not included here.`],
      gain:["Extra EBITDA", `When all approved changes are working fully, EBITDA goes up by about ${money(s.gainFull)} a month compared with today. After monthly costs, that is ${money(s.net)} a month.`],
      be:["Break-even", s.be ? `Month ${s.be}. By then the extra EBITDA has paid back all the money spent.` : "The extra EBITDA does not pay back the cost within 5 years. Approve fewer expensive changes."],
      time:["Full results in", `${s.full} months, when the slowest approved change is fully working. Staff take about 3 months, equipment 6, process changes 1, automations 2 after go-live.`],
      hit:["KPIs on target", `${s.hit} of ${S3.sel.length} KPIs reach their ${GOALMODE==="ach"?"achievable":"dream"} value. Switch between Achievable and Dream at the top of the Selected KPIs panel.`] }[id];
    return [`<div class="d-eyebrow">Plan summary</div><div class="d-title">${T[0]}</div><p style="margin:0">${T[1]}</p>
      <div class="d-sec"><h4>Approved changes and cost</h4><ul class="d-list">${approved5().map(c=>{ const x = cost5(c); return `<li><span class="ck y">✓</span><span>${esc(ITEMS[c].n)} · ${esc(withU(c, valueOf5(c)))}</span><em>${x.one?money(L_(x.one)):""}${x.one&&x.mo?" + ":""}${x.mo?money(L_(x.mo))+"/mo":""}${!x.one&&!x.mo?"no cost":""}</em></li>`; }).join("") || "<li>None approved.</li>"}</ul></div>`, "watch"]; }
  return ["",""]; }
function sim_peekFor(ref){ const [t,id] = ref.split(":"); if (t==="it") { const it = ITEMS[id];
    if (isLever(it)) return `<div class="pk-t">${esc(it.n)}</div><div class="pk-m">Today ${esc(withU(id,it.t))} · achievable ${esc(withU(id,LV[id].ach))} · dream ${esc(withU(id,LV[id].drm))}</div><div class="pk-m"><b>${valueOf5(id)===null?"Not approved":"Approved at "+esc(withU(id, valueOf5(id)))}</b></div>`;
    return `<div class="pk-t">${esc(it.n)}</div><div class="pk-n">${esc(fmtV(id, val5(id)))}</div><div class="pk-m">Today ${esc(fmtV(id,it.t))} · achievable ${esc(fmtV(id,it.r))} · dream ${esc(fmtV(id))}</div>`; }
  return `<div class="pk-hint">Click for the detail</div>`; }
function sim_contextFor(ref){ const [t,id] = ref.split(":"); if (t==="it") { const it = ITEMS[id]; return { kind: isLever(it)?"Change":"KPI", point:`${it.n} in this plan`, title:it.n, lines:[isLever(it)?(valueOf5(id)===null?"Not approved":`Approved at ${withU(id, valueOf5(id))}`):`With this plan ${withU(id, val5(id))} · dream ${withU(id)}`] }; } return { kind:"Plan", point:"this plan", title:"The plan", lines:[] }; }
function sim_chatOpening(){ const s = summary5(); const miss = S3.sel.filter(k => !onGoal5(k));
  return { msg:[ `I have approved every change at the Achievable level. It costs ${money(s.tot)} over ${s.D} months, of which ${money(s.mo)} is monthly cost. It adds about ${money(s.gainFull)} a month to EBITDA and breaks even ${s.be?`in month ${s.be}`:"after more than 5 years"}.`,
      miss.length ? `${miss.map(k=>ITEMS[k].n).join(", ")} ${miss.length>1?"are":"is"} short of the ${GOALMODE==="ach"?"Achievable":"Dream"} value. Click "Dream" to see what your page 2 targets need.` : `All KPIs reach their ${GOALMODE==="ach"?"Achievable":"Dream"} values.`,
      "Change any approval or cost on the left. The KPIs on the right and the costs at the top update straight away. When it looks right, freeze the plan." ],
    note: s.be ? `Pays for itself in month ${s.be}.` : "Costs more than it earns.",
    points: [ `${money(s.tot)} over ${s.D} months`, `Break-even ${s.be?"month "+s.be:"after 5 years"}`, ...miss.slice(0,2).map(k=>`${ITEMS[k].n} short of target`) ],
    asks: [ "Which changes give the best value?", "What does the dream plan cost?", "Why are some KPIs short?" ] }; }
function sim_fillChat(){ const c = sim_chatOpening();
  document.getElementById("chatSub").textContent = "Simulation · step 4 of 7 · Simulate";
  chatBody.innerHTML = `<div class="msg">${c.msg.map(m=>`<p>${esc(m)}</p>`).join("")}</div><div class="lbl">Tojo's note</div><div class="note">${esc(c.note)}</div>
  <div class="lbl">Add to a point — pick one or more</div>${c.points.map((t,i)=>`<button class="pt" type="button" aria-pressed="false"><b>P${i+1}</b> ${esc(t)}</button>`).join("")}
  <div class="lbl">Or ask next</div>${c.asks.map(t=>`<button class="ask" type="button">${esc(t)}</button>`).join("")}`;
  chatBody.querySelectorAll(".pt").forEach(b => b.onclick = () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")==="true"?"false":"true"));
  chatBody.querySelectorAll(".ask").forEach(b => b.onclick = () => { chatIn.value = b.textContent; chatIn.focus(); }); }
function valueRank5(){ const base = summary5().gainFull; return approved5().map(id => { const keep = SIMR.lvl[id]; SIMR.lvl[id] = "off"; const g = summary5().gainFull; SIMR.lvl[id] = keep; const c = cost5(id); const cost12 = L_(c.one) + 12*L_(c.mo); return [id, base - g, cost12]; }).sort((a,b)=> (b[1]*12 - b[2]) - (a[1]*12 - a[2])); }
function sim_replyFor(text, ctx){ const q = text.toLowerCase();
  if (q.includes("best value")) { const r = valueRank5().slice(0,4); return [ `Best value in the first year: ${r.map(([id,g,c]) => `${ITEMS[id].n} (adds about ${money(g)} a month, costs ${money(c)} in year one)`).join("; ")}.`, "I checked each one by removing it from the plan and seeing how much EBITDA drops." ]; }
  if (q.includes("dream plan")) { const keep = {...SIMR.lvl}; ch5().forEach(id => SIMR.lvl[id] = "drm"); const s = summary5(); SIMR.lvl = keep;
    return [ `The Dream plan costs ${money(s.tot)} over ${s.D} months (${money(s.mo)} a month). It adds about ${money(s.gainFull)} a month to EBITDA and breaks even ${s.be?`in month ${s.be}`:"after more than 5 years"}.`, "Click \"Dream\" next to Approve all at, to see it on the page." ]; }
  if (q.includes("short")) { const miss = S3.sel.filter(k => !onGoal5(k)); return miss.length ? [ `${miss.map(k => `${ITEMS[k].n} can only get ${Math.round(reach5(k)*100)}% of the way to best practice with the changes on this page`).join("; ")}.`, "The rest depends on things none of these changes affect, such as staff leaving or infections. Picking one of those as a KPI on page 3 adds more changes." ] : ["All KPIs are on target."]; }
  if (ctx && ctx.ref) { const [,id] = ctx.ref.split(":"); const it = ITEMS[id]; if (it) return [ isLever(it) ? `${it.n}: ${valueOf5(id)===null?"not approved":`approved at ${withU(id, valueOf5(id))}`}. Achievable ${withU(id, LV[id].ach)}, dream ${withU(id, LV[id].drm)}.` : `${it.n}: ${withU(id, val5(id))} with this plan. Target: ${withU(id, goal5(id, GOALMODE))}.`, it.why ]; }
  const s = summary5(); return [ `${s.n} changes approved. ${money(s.tot)} over ${s.D} months. Break-even ${s.be?"in month "+s.be:"after 5 years"}.`, "Ask about any change or KPI." ]; }
function sim_fillCommon(){}
