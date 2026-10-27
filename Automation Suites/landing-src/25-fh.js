/* ===== Financial Health runtime: day and since-start checks, the two chosen measures, causes, actions, CEO decisions.
   Loaded after 20-shared.js. Only acts when the suite's data has fh:true; every other suite is untouched. ===== */
const FH_ST = { done:"Done by the suite", advised:"Advised", awaiting:"Awaiting the CEO", approved:"Approved by the CEO", held:"Held by the CEO" };
const FH_STC = { done:"ahead", advised:"watch", awaiting:"off", approved:"ahead", held:"watch" };
{ const _f = fmtv; fmtv = function(k, v){ if (k.unit === "d") return (Math.round(v*100)/100) + " days"; if (k.unit === "k") return "₹" + Math.round(v*1000).toLocaleString("en-IN"); if (k.unit === "L" && Math.abs(v) >= 100) return "₹" + Math.round(v).toLocaleString("en-IN") + " lakh"; return _f(k, v); }; }

function fhBuild(data){
  try { const s = JSON.parse(localStorage.getItem("fhChosen")||"null"); if (Array.isArray(s) && s.length===2 && s.every(id=>data.pool.some(k=>k.id===id) && !data.core.includes(id)) && s[0]!==s[1]) data.chosen = s; } catch(_){}
  data.kpis = data.core.concat(data.chosen).map(id => data.pool.find(k=>k.id===id));
}
function fhGap(k, exp, act){ const d = act - exp; const good = k.dir==="up" ? d >= 0 : d <= 0; const g = Math.round(Math.abs(d)*100)/100;
  const amt = k.unit==="%" ? `${g} point${g===1?"":"s"}` : fmtv(k, g);
  if (Math.abs(d) < 1e-9) return "exactly as expected"; return good ? `${amt} better than expected` : k.dir==="up" ? `${amt} short of expected` : `${amt} over expected`; }
function fhRatio(k){ const [e,a] = k.td; return k.dir==="up" ? (a-e)/e : (e-a)/e; }
function fhStates(){
  const rank = { ahead:0, watch:1, off:2 };
  D.kpis.forEach(k => { k.plan = k.day[0]; k.now = k.day[1];
    k.dayState = kstate(k); const r = fhRatio(k); k.tdState = r >= 0 ? "ahead" : r > -0.03 ? "watch" : "off";
    k.state = rank[k.dayState] >= rank[k.tdState] ? k.dayState : k.tdState; });
  KP = Object.fromEntries(D.kpis.map(k => [k.id, k]));
  onCourse = D.kpis.filter(k=>k.state!=="off").length;
}
{ const _s = setSuite; setSuite = function(key){ const s = SUITES.find(x=>x.key===key); if (s && s.data.fh && !s.data.kpis) fhBuild(s.data); _s(key); if (D && D.fh) fhStates(); }; }
function fhPick(slot, id){ const c = D.chosen.slice(); const other = 1 - slot; if (c[other] === id) c[other] = c[slot]; c[slot] = id; D.chosen = c;
  try { localStorage.setItem("fhChosen", JSON.stringify(c)); } catch(_){}
  fhBuild(D); fhStates(); fillChat(); const y = scrollY; render(); scrollTo(0, y); }
document.addEventListener("change", e => { const s = e.target.closest("select[data-pick]"); if (s) fhPick(+s.dataset.pick, s.value); });

/* text helpers */
const fhDay = k => `${fmtv(k,k.day[1])} on ${D.dayLabel}, against ${fmtv(k,k.day[0])} expected`;
function fhTd(k){ const [e,a] = k.td; const p = Math.abs(fhRatio(k)*100); const pct = (Math.round(p*10)/10) + "%";
  const pre = k.tdKind==="total" ? "" : "average ";
  return `${pre}${fmtv(k,a)} ${D.sinceLabel}, against ${fmtv(k,e)} expected (${pct} ${fhRatio(k)>=0?"better":"worse"})`; }
const fhPct = k => { const p = fhRatio(k)*100; return (p>=0?"+":"−") + (Math.round(Math.abs(p)*10)/10) + "%"; };
const fhDrivers = id => D.drivers.filter(d => d.kpis.includes(id));
const fhActs = drvIds => D.actions.filter(a => a.drv.some(d => drvIds.includes(d)));
const fhWho = k => k && P[k] ? P[k].name : "the suite";
const fhCost = a => !a.cost ? "" : /^No /.test(a.cost) ? a.cost.toLowerCase() : "cost " + a.cost.replace(/^About/,"about");
const fhL = v => (v>=0?"+":"−") + "₹" + Math.abs(v).toFixed(2) + " lakh";

function fhChooser(cls){
  const opt = slot => D.pool.filter(k => !D.core.includes(k.id)).map(k => `<option value="${k.id}" ${D.chosen[slot]===k.id?"selected":""}>${esc(k.name)} · ${esc(k.kind||"")}</option>`).join("");
  return `<div class="${cls}"><span>Your two measures</span><label><span class="sr">First chosen measure</span><select data-pick="0">${opt(0)}</select></label><label><span class="sr">Second chosen measure</span><select data-pick="1">${opt(1)}</select></label></div>`;
}
function fhDecideBtns(a, cls){ if (a.st !== "awaiting") return "";
  return `<span class="${cls||"fh-dec"}"><button type="button" data-decide="${a.id}:yes">Approve</button><button type="button" data-decide="${a.id}:no">Hold</button></span>`; }

/* details */
function fhActRow(a){ return `<li><span class="av">${a.st==="done"?"✓":a.st==="awaiting"?"?":a.st==="approved"?"✓":"→"}</span><span>${esc(a.t)}<br><small style="color:var(--sh-mute)">${esc(FH_ST[a.st])}${a.st==="advised"?` to ${esc(fhWho(a.who))} · ${esc(a.reply)}`:""} · ${a.gain?`${fhL(a.gain)} a day`:"no direct gain"}</small></span><time>${esc(a.when.replace(/^(Raised|Advised) /,""))}</time></li>`; }
function fhKpiDetail(k){
  const drv = fhDrivers(k.id).filter(d => k.state==="ahead" ? d.lift : true), acts = fhActs(drv.map(d=>d.id));
  let h = `<div class="d-eyebrow">KPI · ${k.id} · ${D.core.includes(k.id)?"core measure":"your chosen measure"}</div><div class="d-title">${esc(k.name)}</div>
  <p class="d-sub"><span class="d-pill ${k.state}">${STATE_WORD[k.state]}</span> &nbsp;checked every morning against the day and the total ${esc(D.sinceLabel)}</p>
  <div class="d-four"><div><span>Expected ${esc(D.dayLabel)}</span><b>${fmtv(k,k.day[0])}</b></div><div class="now"><span>Actual ${esc(D.dayLabel)}</span><b>${fmtv(k,k.day[1])}</b></div><div><span>Expected ${esc(D.sinceLabel)}</span><b>${fmtv(k,k.td[0])}</b></div><div class="now"><span>Actual ${esc(D.sinceLabel)}</span><b>${fmtv(k,k.td[1])}</b></div></div>
  <div class="d-grid"><div><span>For the day</span><b class="d-pill ${k.dayState}" style="border:0;padding:0">${fhGap(k,k.day[0],k.day[1])}</b></div><div><span>${k.tdKind==="total"?"Total":"Average"} ${esc(D.sinceLabel)}</span><b class="d-pill ${k.tdState}" style="border:0;padding:0">${fhPct(k)} against expected</b></div><div><span>Before the project</span><b>${fmtv(k,k.base)} a day</b></div><div><span>Target at full run</span><b>${fmtv(k,k.target)} a day</b></div></div>`;
  if (k.state === "ahead") h += `<div class="d-sec"><h4>What is driving it</h4><p style="margin:0">${esc(k.why || (drv[0] && drv[0].note) || "Running above what was expected.")}</p></div>`;
  if (drv.length) h += `<div class="d-sec"><h4>${k.state==="ahead"?"Lifting it":"What pulled it down"}</h4><ul class="d-fix">${drv.map(d=>`<li><span class="av">${d.lift?"↑":"↓"}</span><span>${esc(d.name)}<br><small style="color:var(--sh-mute)">${esc(d.src)} · ${esc(fhWho(d.owner))}</small></span><time>${d.e?fhL(d.e)+" EBITDA a day":"—"}</time></li>`).join("")}</ul></div>`;
  if (acts.length) h += `<div class="d-sec"><h4>What the suite has done, advised and is waiting on</h4><ul class="d-fix">${acts.map(fhActRow).join("")}</ul></div>`;
  if (k.state !== "ahead") { const g = sum(acts.filter(a=>a.st!=="held").map(a=>a.gain)); h += `<div class="d-back">${acts.length ? `All of this together brings back about ₹${g.toFixed(2)} lakh a day.` : "Watched every morning; no cause found yet."}</div>`; }
  return h;
}
function fhDrvDetail(d){
  const acts = fhActs([d.id]);
  return `<div class="d-eyebrow">Cause · ${d.lift?"lifting revenue":"pulling the measures down"}</div><div class="d-title">${esc(d.name)}</div>
  <p class="d-sub"><span class="d-pill ${d.lift?"ahead":"off"}">${d.e?fhL(d.e)+" EBITDA on "+esc(D.dayLabel):"No direct money effect"}</span> &nbsp;${esc(d.since)}</p>
  <div class="d-grid"><div><span>Effect ${esc(D.sinceLabel)}</span><b>${d.etd?fhL(d.etd)+" EBITDA":"—"}</b></div><div><span>Comes from</span><b>${esc(d.src)}</b></div><div><span>Owner</span><b>${esc(fhWho(d.owner))}</b></div><div><span>Measures it moves</span><b>${d.kpis.map(id=>{ const k = D.pool.find(x=>x.id===id); return esc(k.short); }).join(", ")}</b></div></div>
  <div class="d-sec"><h4>What is happening</h4><p style="margin:0">${esc(d.note)}</p></div>
  ${acts.length?`<div class="d-sec"><h4>Done, advised and waiting</h4><ul class="d-fix">${acts.map(fhActRow).join("")}</ul></div>`:""}`;
}
function fhActDetail(a){
  const drv = D.drivers.filter(d => a.drv.includes(d.id));
  return `<div class="d-eyebrow">Recovery · ${esc(FH_ST[a.st])}</div><div class="d-title">${esc(a.t)}</div>
  <p class="d-sub"><span class="d-pill ${FH_STC[a.st]}">${esc(FH_ST[a.st])}</span> &nbsp;${esc(a.when)}${a.wait&&a.st==="awaiting"?" · "+esc(a.wait):""}</p>
  <div class="d-grid"><div><span>Expected gain</span><b>${a.gain?fhL(a.gain)+" EBITDA a day":"Visibility, no direct gain"}</b></div>${a.cost?`<div><span>Cost</span><b>${esc(a.cost)}</b></div>`:""}${a.net?`<div><span>Net</span><b>${esc(a.net)}</b></div>`:""}<div><span>${a.st==="done"?"Owner informed":a.st==="advised"?"Advised to":"Then carried out by"}</span><b>${esc(fhWho(a.who))}</b></div>${a.reply?`<div><span>Reply</span><b>${esc(a.reply)}</b></div>`:""}</div>
  <div class="d-sec"><h4>Why</h4><p style="margin:0">${esc(a.note)}</p></div>
  <div class="d-sec"><h4>The cause it answers</h4><ul class="d-fix">${drv.map(d=>`<li><span class="av">${d.lift?"↑":"↓"}</span><span>${esc(d.name)}</span><time>${d.e?fhL(d.e)+" a day":"—"}</time></li>`).join("")}</ul></div>
  ${a.st==="awaiting"?`<div class="d-sec"><h4>Your decision</h4><div class="d-decide">${fhDecideBtns(a,"d-dec")}</div></div>`:""}`;
}
{ const _d = detailFor; detailFor = function(ref){ const [t,id] = ref.split(":");
  if (D && D.fh){ if (t==="kpi" && KP[id]) return [fhKpiDetail(KP[id]), KP[id].state];
    if (t==="drv") { const d = D.drivers.find(x=>x.id===id); return [fhDrvDetail(d), d.lift?"ahead":"off"]; }
    if (t==="act") { const a = D.actions.find(x=>x.id===id); return [fhActDetail(a), FH_STC[a.st]]; } }
  return _d(ref); }; }
{ const _p = peekFor; peekFor = function(ref){ const [t,id] = ref.split(":");
  if (D && D.fh){
    if (t==="kpi" && KP[id]){ const k = KP[id]; return `<div class="pk-t">${esc(k.name)}</div><div class="pk-n">${fmtv(k,k.day[1])}</div><div class="pk-m">${esc(D.dayLabel)}: expected ${fmtv(k,k.day[0])} · ${fhGap(k,k.day[0],k.day[1])}</div><div class="pk-m">${k.tdKind==="total"?"Total":"Average"} ${esc(D.sinceLabel)}: ${fmtv(k,k.td[1])} against ${fmtv(k,k.td[0])} (${fhPct(k)})</div><div class="pk-m"><b>${STATE_WORD[k.state]}</b></div><div class="pk-hint">Click for the causes and the recovery</div>`; }
    if (t==="drv"){ const d = D.drivers.find(x=>x.id===id); return `<div class="pk-t">${esc(d.name)}</div><div class="pk-m">${d.e?fhL(d.e)+" EBITDA on "+esc(D.dayLabel)+" · "+fhL(d.etd)+" "+esc(D.sinceLabel):"No direct money effect"}</div><div class="pk-m">${esc(d.src)} · ${esc(fhWho(d.owner))}</div><div class="pk-hint">Click for what the suite is doing about it</div>`; }
    if (t==="act"){ const a = D.actions.find(x=>x.id===id); return `<div class="pk-t">${esc(a.t)}</div><div class="pk-m"><b>${esc(FH_ST[a.st])}</b> · ${esc(a.when)}</div><div class="pk-m">${a.gain?fhL(a.gain)+" EBITDA a day":"Visibility"}${a.cost?" · "+esc(fhCost(a)):""}</div><div class="pk-hint">${a.st==="awaiting"?"Click to approve or hold":"Click for the full story"}</div>`; } }
  return _p(ref); }; }
{ const _c = contextFor; contextFor = function(ref){ const [t,id] = ref.split(":");
  if (D && D.fh){
    if (t==="kpi" && KP[id]){ const k = KP[id]; return { kind:"KPI", point:`the KPI "${k.name}"`, title:k.name, lines:[`${D.dayLabel}: ${fmtv(k,k.day[1])} against ${fmtv(k,k.day[0])} expected`, `${D.sinceLabel}: ${fmtv(k,k.td[1])} against ${fmtv(k,k.td[0])} (${fhPct(k)})`] }; }
    if (t==="drv"){ const d = D.drivers.find(x=>x.id===id); return { kind:"Cause", point:`the cause "${d.name}"`, title:d.name, lines:[d.e?`${fhL(d.e)} EBITDA a day · ${fhL(d.etd)} ${D.sinceLabel}`:"No direct money effect", `${d.src} · ${fhWho(d.owner)}`] }; }
    if (t==="act"){ const a = D.actions.find(x=>x.id===id); return { kind:"Recovery", point:`the recovery step "${a.t}"`, title:a.t, lines:[`${FH_ST[a.st]} · ${a.when}`, a.gain?`${fhL(a.gain)} EBITDA a day${a.cost?" · cost "+a.cost:""}`:"Visibility"] }; } }
  return _c(ref); }; }
{ const _r = replyFor; replyFor = function(ref){ const [t,id] = ref.split(":");
  if (D && D.fh){
    const actList = acts => `<ul>${acts.map(a=>`<li>${esc(a.t)} · <b>${esc(FH_ST[a.st])}</b>${a.st==="advised"?` (${esc(fhWho(a.who))}: ${esc(a.reply)})`:""}${a.gain?`, ${fhL(a.gain)} a day`:""}</li>`).join("")}</ul>`;
    if (t==="kpi" && KP[id]){ const k = KP[id]; const drv = fhDrivers(k.id).filter(d=>!d.lift), acts = fhActs(drv.map(d=>d.id));
      if (k.state==="ahead") return [`<p><b>${esc(k.name)}</b> was ${fhDay(k)}: ${fhGap(k,k.day[0],k.day[1])}. ${k.tdKind==="total"?"The total":"The average"} is ${fhTd(k)}.</p><p>No delay or overrun. ${esc(k.why||"")}</p><p>Nothing to recover. ${esc(D.aheadRisk)}</p>`, "Ahead. Keep it there."];
      const wait = acts.filter(a=>a.st==="awaiting");
      return [`<p><b>${esc(k.name)}</b> was ${fhDay(k)}: ${fhGap(k,k.day[0],k.day[1])}. ${k.tdKind==="total"?"The total":"The average"} is ${fhTd(k)}.</p><p><b>What is causing it:</b></p><ul>${drv.map(d=>`<li>${esc(d.name)}${d.e?` (${fhL(d.e)} EBITDA a day)`:""} · ${esc(fhWho(d.owner))}</li>`).join("")}</ul>${acts.length?`<p><b>How we recover:</b></p>${actList(acts)}`:""}${wait.length?`<p>${wait.length} of these need${wait.length===1?"s":""} your decision.</p>`:""}`, wait.length ? "Confirm the waiting decisions today." : "Recovery is under way."]; }
    if (t==="drv"){ const d = D.drivers.find(x=>x.id===id), acts = fhActs([d.id]);
      return [`<p><b>${esc(d.name)}</b> (${esc(d.since)}). ${esc(d.note)}</p><p>${d.e?`It moved yesterday's EBITDA by ${fhL(d.e)}, and ${fhL(d.etd)} ${esc(D.sinceLabel)}.`:"It has no direct money effect."} Responsible: ${esc(fhWho(d.owner))}, through the ${esc(d.src)}.</p>${acts.length?`<p><b>What is being done:</b></p>${actList(acts)}`:""}`, d.lift ? "Keep this one growing." : "Recovery is in hand."]; }
    if (t==="act"){ const a = D.actions.find(x=>x.id===id);
      return [`<p><b>${esc(a.t)}</b> is ${esc(FH_ST[a.st].toLowerCase())} (${esc(a.when)}).</p><p>${esc(a.note)}</p><p>${a.gain?`Expected gain ${fhL(a.gain)} of EBITDA a day.`:""} ${a.cost?`Cost: ${esc(a.cost)}. Net: ${esc(a.net)}.`:""}</p>${a.st==="awaiting"?`<p>It is waiting for your decision (${esc(a.wait)}). Approve or hold it from the Recovery section or from its panel.</p>`:""}`, a.st==="awaiting" ? "Your decision is the only thing it waits on." : "In hand."]; } }
  return _r(ref); }; }

/* CEO decisions */
function fhToast(msg){ let t = document.getElementById("fhToast"); if (!t){ t = document.createElement("div"); t.id = "fhToast"; t.setAttribute("role","status"); document.body.appendChild(t);
  const s = document.createElement("style"); s.textContent = "#fhToast{position:fixed;left:50%;bottom:90px;transform:translate(-50%,20px);opacity:0;z-index:90;background:#10241a;color:#F3EFE3;border:1.5px solid #d4a94f;border-radius:12px;padding:10px 16px;font:500 13.5px/1.4 Poppins,sans-serif;max-width:min(520px,calc(100% - 32px));transition:opacity .2s,transform .2s;pointer-events:none}#fhToast.on{opacity:1;transform:translate(-50%,0)}"; document.head.appendChild(s); }
  t.textContent = msg; t.classList.add("on"); clearTimeout(t._h); t._h = setTimeout(()=>t.classList.remove("on"), 3200); }
function fhDecide(id, yes){ const a = D.actions.find(x=>x.id===id); if (!a || a.st!=="awaiting") return;
  a.st = yes ? "approved" : "held"; a.when = yes ? "Approved by the CEO just now · the suite is carrying it out" : "Held by the CEO just now";
  const ceo = D.people.find(p=>p.key==="anil"); if (ceo && a.ceo !== undefined && ceo.today[a.ceo]) { const was = ceo.today[a.ceo][1]; ceo.today[a.ceo] = [ceo.today[a.ceo][0] + (yes?"":" (held)"), 1]; ceo.done += 1; if (String(was).startsWith("waiting 1")) ceo.late = Math.max(0, ceo.late-1); ceo.state = pstate(ceo); if (!ceo.today.some(x=>x[1]!==1)) ceo.impact = ""; }
  const y = scrollY; render(); scrollTo(0, y);
  if (sheet.classList.contains("on") && sheet.dataset.ref === "act:"+id) { const [h,st] = detailFor("act:"+id); sheetBody.innerHTML = h; sheet.style.setProperty("--sh-state", st==="off"?"var(--c-bad)":st==="watch"?"var(--c-warn)":"var(--c-ok)"); }
  fhToast(yes ? `Approved: ${a.t}. Expected ${fhL(a.gain)} EBITDA a day.` : `Held: ${a.t}. The suite will raise it again tomorrow with fresh numbers.`); }
document.addEventListener("click", e => { const b = e.target.closest("[data-decide]"); if (!b) return; e.preventDefault(); e.stopPropagation(); suiteOf(b.closest("[data-suite]") || document.querySelector("#stage [data-suite]")); const [id, v] = b.dataset.decide.split(":"); fhDecide(id, v==="yes"); }, true);

/* 30 closed days for the day strips: actual against expected, as a ratio where 1 is on expected (higher is better for every measure) */
function fhSeries(k, n){ n = n || 30; const r = fhRatio(k), seed = k.id.charCodeAt(1) + (k.id.charCodeAt(2)||0); const dayR = k.dir==="up" ? (k.day[1]-k.day[0])/k.day[0] : (k.day[0]-k.day[1])/k.day[0];
  const out = []; for (let i=0;i<n;i++){ let v = r + 0.035*Math.sin(i*1.7 + seed) + 0.02*Math.cos(i*0.9 + seed*2);
    if ((k.id==="K4"||k.id==="K1"||k.id==="K8") && i >= n-6) v -= k.id==="K4" ? 0.07 : 0.03; if (i===n-1) v = dayR; out.push(v); } return out; }
const fhDates = n => { const out = []; for (let i=n-1;i>=0;i--){ const d = new Date(2026, 9, 23 - i); out.push(d.getDate() + " " + ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][d.getMonth()]); } return out; };
document.addEventListener("keydown", e => { if ((e.key==="Enter"||e.key===" ") && e.target.matches && e.target.matches('#stage div[role="button"][data-ref]')) { e.preventDefault(); e.target.click(); } });
