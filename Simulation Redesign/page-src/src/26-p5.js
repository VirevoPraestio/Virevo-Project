/* ===== Page 5 · Freeze: check the frozen plan once more and confirm it =====
   Everything on this page is read from the frozen plan (SIMR.frozen), not from the live page 4.
   If page 4 has been changed since freezing, the page says so and offers to freeze the new version. */
const P5 = { by:"", role:"", ticks:{}, done:null };
function frozenSig(F){ return JSON.stringify([F.lvl, F.own, F.ucOne, F.ucMo, F.tot, F.D, F.sel]); }
function stale5(){ const F = SIMR.frozen; if (!F) return false; return frozenSig(F) !== frozenSig({ lvl:SIMR.lvl, own:SIMR.own, ucOne:SIMR.ucOne, ucMo:SIMR.ucMo, tot:SIMR.tot, D:SIMR.D, sel:S3.sel }); }
function withFrozenSel(fn){ const F = SIMR.frozen; if (!F) return fn(); const keep = [...S3.sel]; S3.sel.splice(0, S3.sel.length, ...F.sel); levels5();
  try { return withFrozen(fn); } finally { S3.sel.splice(0, S3.sel.length, ...keep); levels5(); } }
function p5Data(){ return withFrozenSel(() => {
  const s = summary5(), mode = GOALMODE;
  const kpis = S3.sel.map(k => { const it = ITEMS[k]; let m = null; for (let i = 1; i <= 24; i++) if (onGoal5(k, i)) { m = i; break; }
    return { k, n: it.n, t: it.t, v: val5(k), goal: goal5(k, mode), ok: onGoal5(k), month: m, close: fr5(24)(k) >= need5(k, mode)*0.6 }; });
  const changes = approved5().map(id => { const it = ITEMS[id], kind = leverKind(it), c = cost5(id);
    return { id, n: it.n, kind, from: it.t, to: valueOf5(id), units: unitsOf5(id), tot: c.tot, mo: c.mo, start: startOf5(id), full: startOf5(id) + RAMP5[kind] - 1 }; });
  const base = ITEMS.EBITDA.t/100*ITEMS.REV.t, N = Math.min(36, Math.max(18, (s.be || 24) + 6));
  let spent = 0, earned = 0; const cash = [];
  for (let m = 1; m <= N; m++){ changes.forEach(c => { if (c.start === m) spent += L_(cost5(c.id).one); if (c.start <= m) spent += L_(c.mo); });
    earned += ebitdaL(m) - base; cash.push({ m, spent, earned }); }
  return { s, mode, kpis, changes, cash, at: SIMR.frozen ? SIMR.frozen.at : null }; }); }
const fmtDate = d => d ? new Date(d).toLocaleString("en-IN", { day:"numeric", month:"short", year:"numeric", hour:"numeric", minute:"2-digit" }) : "";
const goalWord = m => m === "ach" ? "Achievable" : "Dream";
const kpiState = x => x.ok ? ["hit","On target"] : x.close ? ["near","Close"] : ["far","Short"];

/* ---------- shared parts ---------- */
function p5Head(title, lede){ return `<div class="p2head" style="grid-template-columns:1fr"><div><div class="eb">Simulation · step 5 of 7 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>${title}</h1><p class="lede">${lede}</p></div></div>`; }
function p5Stale(){ return `<div class="stale5" data-v="stale5" role="status"></div>`; }
function p5Tiles(d){ const s = d.s; return `<section class="top5 p5t" aria-label="Plan summary">
  <div class="t5" data-ref="p5:cost"><span>Total cost</span><b>${money(s.tot)}</b><small>over ${s.D} months · ${s.n} changes</small></div>
  <div class="t5" data-ref="p5:mo"><span>Monthly cost</span><b>${money(s.mo)}</b><small>once all changes are in place</small></div>
  <div class="t5" data-ref="p5:gain"><span>Extra EBITDA</span><b>${money(s.gainFull)}<i> a month</i></b><small>${s.net >= 0 ? money(s.net)+" after monthly costs" : money(-s.net)+" less than monthly costs"}</small></div>
  <div class="t5" data-ref="p5:be"><span>Break-even</span><b>${s.be ? "Month "+s.be : "Over 5 years"}</b><small>${s.be ? "when the plan has paid for itself" : "costs more than it earns"}</small></div>
  <div class="t5" data-ref="p5:time"><span>Full results in</span><b>${s.full} months</b><small>${s.reach ? "all KPIs on target by month "+s.reach : "not all KPIs reach target"}</small></div>
  <div class="t5 hl" data-ref="p5:hit"><span>KPIs on target</span><b>${s.hit}<i>/${d.kpis.length}</i></b><small>compared with ${goalWord(d.mode)}</small></div></section>`; }
function kpiRows5(d){ return `<ul class="kl5">${d.kpis.map(x => { const [st, w] = kpiState(x); return `<li><div class="kl5-n">${nameBtn(x.k)}<span class="k5-s" data-state="${st}">${w}</span></div>
  <div class="kl5-v"><span>Today <b>${esc(fmtV(x.k, x.t))}</b></span><span class="ar" aria-hidden="true">→</span><span>With plan <b>${esc(fmtV(x.k, x.v))}</b></span><span class="g">${goalWord(d.mode)} <b>${esc(fmtV(x.k, x.goal))}</b></span></div></li>`; }).join("")}</ul>`; }
function changeLevel5(c){ const it = ITEMS[c.id]; return isSwitch(it) ? "Switch on" : `${fmtV(c.id, c.from)} → ${fmtV(c.id, c.to)}${isCount(c.id) ? ` <small>(+${+c.units.toFixed(2)})</small>` : ""}`; }
function changeGroups5(d){ return ["a","k","w","p"].map(k => { const xs = d.changes.filter(c => c.kind === k); if (!xs.length) return "";
  const sum = xs.reduce((a,c)=>a+c.tot,0);
  return `<section class="cg5"><h3>${KINDNAME[k]}<small>${xs.length} · ${money(L_(sum))}</small></h3><ul>${xs.map(c => `<li>${nameBtn(c.id)}<span class="lv">${changeLevel5(c)}</span><span class="cs">${c.tot ? money(L_(c.tot)) : "No cost"}</span><span class="wh">month ${c.start}–${c.full}</span></li>`).join("")}</ul></section>`; }).join(""); }
function p5Confirm(ticks){ return `<section class="cf5" data-v="cf5" aria-label="Confirm the plan">
  <h2>Confirm this plan</h2>
  ${ticks ? `<div class="tk5">${[["cost","I have checked the total cost and the monthly cost."],["changes","I have checked every approved change and its cost."],["kpis","I have checked where each KPI will land."]].map(([k,t]) => `<label><input type="checkbox" data-tick="${k}"> ${t}</label>`).join("")}</div>` : ""}
  <div class="who5"><label><small>Confirmed by</small><input type="text" data-p5in="by" placeholder="Your name" autocomplete="name"></label><label><small>Role</small><input type="text" data-p5in="role" placeholder="e.g. CEO, COO"></label></div>
  <div class="cf5-b"><button type="button" class="act ghost" data-p5="back">Go back and change it</button><button type="button" class="go ready" data-p5="confirm">Confirm this plan</button></div>
  <p class="cf5-done" data-v="cf5done" hidden></p></section>`; }
function p5Mount(stage, inner){ if (!SIMR.frozen) { levels5(); ch5().forEach(id => { if (!(id in SIMR.lvl)) SIMR.lvl[id] = "ach"; }); }
  stage.innerHTML = `<div class="lk lk-web">${journeyHTML(4)}${SIMR.frozen ? inner : `<div class="empty5"><h1>No plan frozen yet</h1><p>Go to Simulate, approve the changes you want, and press Freeze this plan.</p><button type="button" class="go ready" data-p5="back">Go to Simulate</button></div>`}</div>`;
  wire5p(stage); }
function wire5p(root){
  root.querySelectorAll("[data-p5]").forEach(b => b.addEventListener("click", () => { const a = b.dataset.p5;
    if (a === "back") goStep(3);
    else if (a === "refreeze") { freezeNow5(); P5.done = null; mountLook(LOOKS.indexOf(CUR)); toast("The new plan is frozen."); }
    else if (a === "confirm") { const need = [...root.querySelectorAll("[data-tick]")].filter(t => !t.checked);
      if (need.length) { toast("Tick each check first."); need[0].focus(); return; }
      if (!P5.by.trim()) { toast("Add your name to confirm."); root.querySelector('[data-p5in="by"]').focus(); return; }
      P5.done = { by: P5.by.trim(), role: P5.role.trim(), at: new Date() }; refresh(null); }
    else if (a === "next") goStep(5, "Plan confirmed."); }));
  root.querySelectorAll("[data-p5in]").forEach(n => { n.value = P5[n.dataset.p5in] || ""; n.addEventListener("input", () => P5[n.dataset.p5in] = n.value); });
  root.querySelectorAll("[data-tick]").forEach(t => { t.checked = !!P5.ticks[t.dataset.tick]; t.addEventListener("change", () => P5.ticks[t.dataset.tick] = t.checked); });
}
function p5Sync(root){
  const st = root.querySelector('[data-v="stale5"]'); if (st) { const on = stale5(); st.hidden = !on;
    st.innerHTML = on ? `<span>Simulate has been changed since this plan was frozen. This page still shows the frozen plan${SIMR.frozen ? ", frozen "+esc(fmtDate(SIMR.frozen.at)) : ""}.</span><button type="button" class="act" data-p5="refreeze">Freeze the changed plan instead</button>` : "";
    st.querySelectorAll("[data-p5]").forEach(b => b.onclick = () => { freezeNow5(); P5.done = null; mountLook(LOOKS.indexOf(CUR)); toast("The new plan is frozen."); }); }
  const cf = root.querySelector('[data-v="cf5"]'); if (!cf) return; const done = P5.done;
  cf.classList.toggle("done", !!done); cf.querySelectorAll("input,[data-p5='confirm']").forEach(e => e.disabled = !!done);
  const p = cf.querySelector('[data-v="cf5done"]'); p.hidden = !done;
  if (done) { p.innerHTML = `<b>Confirmed</b> by ${esc(done.by)}${done.role ? ", "+esc(done.role) : ""}, ${esc(fmtDate(done.at))}. <button type="button" class="go ready" data-p5n>Go to Your team →</button>`;
    p.querySelector("[data-p5n]").onclick = () => goStep(5, "Plan confirmed."); }
}

/* ---------- details and chat ---------- */
function p5_detailFor(ref){ const [t,id] = ref.split(":");
  if (t === "p5") return withFrozenSel(() => sim_detailFor("sim:"+id));
  if (t === "it") return withFrozenSel(() => sim_detailFor(ref));
  return ["",""]; }
function p5_peekFor(ref){ const [t] = ref.split(":"); if (t === "it") return withFrozenSel(() => sim_peekFor(ref)); return `<div class="pk-hint">Click for the detail</div>`; }
function p5_contextFor(ref){ const [t,id] = ref.split(":"); if (t === "it") return withFrozenSel(() => sim_contextFor(ref)); return { kind:"Plan", point:"the frozen plan", title:"Frozen plan", lines:[] }; }
function p5_chatOpening(){ if (!SIMR.frozen) return { msg:["No plan is frozen yet. Go back to Simulate and freeze one."], note:"Freeze a plan first.", points:[], asks:["What does freezing do?"] };
  const d = p5Data(), s = d.s, miss = d.kpis.filter(x => !x.ok);
  return { msg:[ `This is the plan you froze: ${s.n} changes, ${money(s.tot)} over ${s.D} months, ${money(s.mo)} a month once everything is in place.`,
      `It adds about ${money(s.gainFull)} a month to EBITDA and breaks even ${s.be ? "in month "+s.be : "after more than 5 years"}. ${s.hit} of ${d.kpis.length} KPIs reach the ${goalWord(d.mode)} value${miss.length ? `; ${miss.map(x=>x.n).join(", ")} ${miss.length>1?"fall":"falls"} short` : ""}.`,
      "Check it, then confirm. Confirming sends this plan to Your team, where each change gets an owner." ],
    note: s.be ? `Pays for itself in month ${s.be}.` : "Costs more than it earns.",
    points: [ `${money(s.tot)} over ${s.D} months`, `Break-even ${s.be ? "month "+s.be : "after 5 years"}`, ...miss.slice(0,2).map(x => `${x.n} short of target`) ],
    asks: [ "What happens after I confirm?", "Which changes cost the most?", "Can I change it later?" ] }; }
function p5_fillChat(){ const c = p5_chatOpening();
  document.getElementById("chatSub").textContent = "Simulation · step 5 of 7 · Freeze";
  chatBody.innerHTML = `<div class="msg">${c.msg.map(m=>`<p>${esc(m)}</p>`).join("")}</div><div class="lbl">Tojo's note</div><div class="note">${esc(c.note)}</div>
  ${c.points.length ? `<div class="lbl">Add to a point — pick one or more</div>${c.points.map((t,i)=>`<button class="pt" type="button" aria-pressed="false"><b>P${i+1}</b> ${esc(t)}</button>`).join("")}` : ""}
  <div class="lbl">Or ask next</div>${c.asks.map(t=>`<button class="ask" type="button">${esc(t)}</button>`).join("")}`;
  chatBody.querySelectorAll(".pt").forEach(b => b.onclick = () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")==="true"?"false":"true"));
  chatBody.querySelectorAll(".ask").forEach(b => b.onclick = () => { chatIn.value = b.textContent; chatIn.focus(); }); }
function p5_replyFor(text, ctx){ const q = text.toLowerCase(); if (!SIMR.frozen) return ["Freeze a plan on Simulate first."];
  const d = p5Data();
  if (q.includes("after i confirm") || q.includes("happens")) return [ "Your team comes next: each approved change gets an owner and a start date. Then the taskboards are built week by week.", "Until you confirm, nothing is sent to anyone." ];
  if (q.includes("cost the most")) { const top = [...d.changes].sort((a,b)=>b.tot-a.tot).slice(0,4); return [ `Biggest costs over ${d.s.D} months: ${top.map(c => `${c.n} (${money(L_(c.tot))})`).join("; ")}.`, "Click any change to see how its cost is worked out." ]; }
  if (q.includes("change it later") || q.includes("later")) return [ "Yes. Go back to Simulate, change it, and freeze again. The team and taskboards are then rebuilt from the new plan.", "This page always shows the last frozen plan, and says so if Simulate has changed since." ];
  if (ctx && ctx.ref) return withFrozenSel(() => sim_replyFor(text, ctx));
  return [ `${d.s.n} changes, ${money(d.s.tot)} over ${d.s.D} months, break-even ${d.s.be ? "month "+d.s.be : "after 5 years"}.`, "Ask about any change or KPI." ]; }
function p5_fillCommon(){}
