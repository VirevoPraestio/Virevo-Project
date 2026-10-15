/* ===== Page 3 · Six KPIs: pick the six numbers to steer by ===== */
const P3G = ["fin","ops","clin","mkt","adm"];
const isLever = it => it.g === "up" || it.x === "p";
function poolIds(){ return shownIds().filter(id => { const it = ITEMS[id]; return it.x === "m" && P3G.includes(it.g); }); }
const _lv = {};
function leversOf(id){ if (_lv[id]) return _lv[id]; const out = new Set(), seen = new Set([id]);
  const walk = (x, d) => (INPUTS[x]||[]).forEach(([f]) => { if (seen.has(f)) return; seen.add(f); if (isLever(ITEMS[f])) out.add(f); else if (d < 2) walk(f, d+1); });
  walk(id, 0); return (_lv[id] = [...out]); }
function measuresOf(id){ const out = new Set(), seen = new Set([id]); const walk = x => (INPUTS[x]||[]).forEach(([f]) => { if (seen.has(f)) return; seen.add(f); if (!isLever(ITEMS[f])) { out.add(f); walk(f); } }); walk(id); return [...out]; }
const S3 = { sel:[] };
const MAX3 = 6;
function toggle3(id){ const i = S3.sel.indexOf(id); if (i >= 0) S3.sel.splice(i,1); else if (S3.sel.length < MAX3) S3.sel.push(id); else { toast("Six are already picked. Remove one to add another."); return; } p2listeners.forEach(fn=>fn(null)); }
function setSel3(ids){ S3.sel = ids.slice(0, MAX3); p2listeners.forEach(fn=>fn(null)); }
function cover3(ids = S3.sel){ const lev = {}; ids.forEach(id => leversOf(id).forEach(l => lev[l] = (lev[l]||0) + 1));
  const depts = new Set(ids.map(id => ITEMS[id].g)); const nodata = ids.filter(id => !hasData(id));
  return { lev, levN: Object.keys(lev).length, shared: Object.values(lev).filter(n=>n>1).length, depts, nodata, short: ids.filter(id => addsUp(id)==="short") }; }
function suggest3(){ const pool = poolIds(); const pick = [];
  const score = (id, cur) => { const it = ITEMS[id], c = cover3(cur); const fresh = leversOf(id).filter(l => !c.lev[l]).length;
    return fresh*1.0 + Math.min(1,fracOf(id))*2 + (hasData(id)?1.2:0) + (c.depts.has(it.g)?0:1.6) + (id==="EBITDA"?5:0); };
  while (pick.length < MAX3){ let best = null, bs = -1; pool.forEach(id => { if (pick.includes(id)) return; const s = score(id, pick); if (s > bs) { bs = s; best = id; } }); if (!best) break; pick.push(best); }
  return pick; }
const SETS3 = [
  { key:"tojo", n:"Tojo's balanced six", why:"Chosen to reach the most changes across the most departments, with data behind as many as possible.", ids:null },
  { key:"margin", n:"Margin first", why:"For a hospital whose first worry is profit: cost lines and the rate per bed.", ids:["EBITDA","DRUG","AGENCY","ARPOB","otuse","agency"] },
  { key:"flow", n:"Faster beds", why:"For a hospital that is full and turning patients away: every hour a bed waits.", ids:["REV","occ","los","turn","icul","clean"] },
  { key:"cash", n:"Cash in sooner", why:"For a hospital short of cash: the claim desk, the insurer, and the services that bring money in quickly.", ids:["RECV","sublag","instat","DIAGREV","OPDREV","conv"] }
];
function setIds(s){ return (s.ids || suggest3()).filter(id => ITEMS[id] && isShown(id)); }
const KINDNAME = { a:"Automations", k:"Beds and equipment", w:"Process and role changes", p:"Staff numbers" };
const leverKind = it => it.x === "p" ? "p" : subOf(it);
function goNext3(){ if (S3.sel.length < MAX3) { toast(`Pick ${MAX3 - S3.sel.length} more to go on.`); return; } goStep(3, `KPIs confirmed: ${S3.sel.map(id=>ITEMS[id].n).join(", ")}.`); }

/* ---------- shared parts ---------- */
function p3Head(title, lede){ return `<div class="p2head"><div><div class="eb">Simulation · step 3 of 7 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>${title}</h1><p class="lede">${lede}</p></div>
  <div class="pulse" role="group" aria-label="Readings">
    <button type="button" class="pz" data-ref="p3:sel"><span class="pl">Picked</span><b data-v="p3n"></b><small data-v="p3nSub"></small></button>
    <button type="button" class="pz" data-ref="p3:lev"><span class="pl">Changes they bring in</span><b data-v="p3lev"></b><small data-v="p3levSub"></small></button>
    <button type="button" class="pz" data-ref="p3:dep"><span class="pl">Departments covered</span><b data-v="p3dep"></b><small data-v="p3depSub"></small></button>
    <button type="button" class="pz" data-ref="p3:nd"><span class="pl">Picked without data</span><b data-v="p3nd"></b><small data-v="p3ndSub"></small></button></div></div>`; }
function p3Cta(){ return `<div class="cta"><button type="button" class="go" data-p3="go">Confirm and simulate <span aria-hidden="true">→</span></button><span class="cta-note" data-v="p3cta"></span></div>`; }
function p3Sync(root){ const c = cover3(), n = S3.sel.length; const set = (k,v) => root.querySelectorAll(`[data-v="${k}"]`).forEach(e => e.innerHTML = v);
  set("p3n", `${n}<i>/6</i>`); set("p3nSub", n<6 ? `${6-n} still to pick` : "ready to simulate");
  set("p3lev", `${c.levN}`); set("p3levSub", c.shared ? `${c.shared} shared by two or more` : "changes the simulation will move");
  set("p3dep", `${c.depts.size}<i>/5</i>`); set("p3depSub", c.depts.size < 3 && n ? "most are from one area" : "Financial, Operational, Clinical, Marketing, Admin");
  set("p3nd", `${c.nodata.length}`); set("p3ndSub", c.nodata.length ? "simulated from typical values" : "all have data");
  set("p3cta", n<6 ? `Pick ${6-n} more.` : c.nodata.length ? `${c.nodata.length} selected KPI${c.nodata.length>1?"s have":" has"} no data yet. The simulation will start from typical values.` : "All six have data. Ready.");
  root.querySelectorAll('[data-p3="go"]').forEach(b => b.classList.toggle("ready", n===6));
  root.querySelectorAll("[data-pick3]").forEach(b => { const on = S3.sel.includes(b.dataset.pick3); b.setAttribute("aria-pressed", on); b.classList.toggle("on", on); b.disabled = !on && n >= 6 && !b.dataset.keep; }); }
function wire3(root){ root.querySelectorAll("[data-pick3]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); toggle3(b.dataset.pick3); }));
  root.querySelectorAll("[data-p3]").forEach(b => b.addEventListener("click", () => { const a = b.dataset.p3;
    if (a==="go") goNext3(); else if (a==="clear") setSel3([]); else if (a==="suggest") { setSel3(suggest3()); toast("Tojo's balanced six are in. Swap any of them."); }
    else if (a.startsWith("set:")) { const s = SETS3.find(x=>x.key===a.slice(4)); setSel3(setIds(s)); toast(`${s.n} is in. Swap any of them below.`); } })); }
function p3Mount(stage, inner){ stage.innerHTML = `<div class="lk lk-web">${journeyHTML(2)}${inner}</div>`; wire3(stage); }
function kpiLine(id){ const it = ITEMS[id]; return `${hasData(id)?"Today":"Typical"} ${withU(id, it.t)} → target ${withU(id)}`; }

/* ---------- details and chat ---------- */
function p3_detailFor(ref){ const [t,id] = ref.split(":"); const c = cover3();
  if (t==="it") { const [h,st] = p2_detailFor(ref); const lv = leversOf(id);
    const extra = `<div class="d-sec"><h4>If you pick it, the simulation will move</h4><p style="margin:0 0 6px">${lv.length} changes with a direct or close effect on it.</p><ul class="d-ms">${lv.map(l=>`<li><span class="src src-${c.lev[l]?"yours":"ref"}">${esc(KINDNAME[leverKind(ITEMS[l])])}</span><span><b>${esc(ITEMS[l].n)}</b>${c.lev[l]?` · already in through ${c.lev[l]} of your picks`:""}</span></li>`).join("")}</ul></div>`;
    return [h + extra, st]; }
  if (t==="p3") { const T = { sel:"Selected KPIs", lev:"Changes the selected KPIs bring in", dep:"Departments covered", nd:"Picked without data" }[id];
    return [`<div class="d-eyebrow">Reading</div><div class="d-title">${T}</div>
      <div class="d-sec"><h4>Selected KPIs</h4><ul class="d-list">${S3.sel.map(s=>`<li><span class="ck ${hasData(s)?"y":"late"}">${hasData(s)?"✓":"!"}</span><span>${esc(ITEMS[s].n)} · ${esc(GNAME[ITEMS[s].g])}</span><em>${leversOf(s).length} changes</em></li>`).join("") || "<li>None picked yet.</li>"}</ul></div>
      <div class="d-sec"><h4>Changes the simulation will move</h4><ul class="d-list">${Object.entries(c.lev).sort((a,b)=>b[1]-a[1]).map(([l,n])=>`<li><span class="ck y">${n}</span><span>${esc(ITEMS[l].n)}</span><em>${esc(KINDNAME[leverKind(ITEMS[l])])}</em></li>`).join("") || "<li>Pick a KPI to see them.</li>"}</ul></div>`, "watch"]; }
  return ["",""]; }
function p3_peekFor(ref){ const [t,id] = ref.split(":"); if (t==="it") { const it = ITEMS[id];
  return `<div class="pk-t">${esc(it.n)}</div><div class="pk-m">${esc(kpiLine(id))}</div><div class="pk-m">Brings in ${leversOf(id).length} changes${hasData(id)?"":" · no data yet"}</div><div class="pk-hint">${S3.sel.includes(id)?"Picked":"Click for how we look at it"}</div>`; }
  if (t==="p3") return `<div class="pk-t">Selected KPIs</div><div class="pk-hint">Click for the list of changes they bring in</div>`; return ""; }
function p3_contextFor(ref){ const [t,id] = ref.split(":"); if (t==="it") return { kind:GNAME[ITEMS[id].g], point:`${ITEMS[id].n} as a selected KPI`, title:ITEMS[id].n, lines:[kpiLine(id)] }; return { kind:"KPIs", point:"my selected KPIs", title:"Six KPIs", lines:S3.sel.map(s=>ITEMS[s].n) }; }
function p3_chatOpening(){ const c = cover3(), n = S3.sel.length;
  return { msg:[ "Pick six KPIs to track. The next page simulates every change that affects them, so these six decide what goes into the plan.",
      n ? `So far ${n} picked, bringing in ${c.levN} changes across ${c.depts.size} department${c.depts.size===1?"":"s"}.${c.depts.size<3?" They lean on one area; a mix across departments gives a fuller plan.":""}` : "Nothing picked yet.",
      c.nodata.length ? `${c.nodata.map(id=>ITEMS[id].n).join(", ")} ${c.nodata.length>1?"have":"has"} no data yet. You can keep ${c.nodata.length>1?"them":"it"}; the simulation starts from typical values.` : "" ].filter(Boolean),
    note: c.depts.size < 3 && n ? "Mix departments, not just money." : "Six numbers, one plan.",
    points: [ `${c.levN} changes brought in`, c.shared ? `${c.shared} changes shared by two or more picks` : "No shared changes yet", c.nodata.length ? `${c.nodata.length} picks without data` : "All picks have data" ],
    asks: [ "Suggest a balanced six", "Why only six?", "What if a KPI has no data?" ] }; }
function p3_fillChat(){ const c = p3_chatOpening();
  document.getElementById("chatSub").textContent = "Simulation · step 3 of 7 · six KPIs";
  chatBody.innerHTML = `<div class="msg">${c.msg.map(m=>`<p>${esc(m)}</p>`).join("")}</div><div class="lbl">Tojo's note</div><div class="note">${esc(c.note)}</div>
  <div class="lbl">Add to a point — pick one or more</div>${c.points.map((t,i)=>`<button class="pt" type="button" aria-pressed="false"><b>P${i+1}</b> ${esc(t)}</button>`).join("")}
  <div class="lbl">Or ask next</div>${c.asks.map(t=>`<button class="ask" type="button">${esc(t)}</button>`).join("")}`;
  chatBody.querySelectorAll(".pt").forEach(b => b.onclick = () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")==="true"?"false":"true"));
  chatBody.querySelectorAll(".ask").forEach(b => b.onclick = () => { chatIn.value = b.textContent; chatIn.focus(); }); }
function p3_replyFor(text, ctx){ const q = text.toLowerCase();
  if (q.includes("suggest")) { const s = suggest3(); setSel3(s); return [`Done: ${s.map(id=>ITEMS[id].n).join(", ")}.`, `Together they bring in ${cover3().levN} changes across ${cover3().depts.size} departments. I started with EBITDA, then added the KPI that brought in the most new changes each time, preferring ones with data and ones from a department not yet covered.`]; }
  if (q.includes("only six")) return ["Six is enough to cover every department and few enough to keep the plan clear. Each KPI pulls in the changes that affect it, so six usually brings in most of the levers in the hospital.", "The other targets you set on page 2 still count; they are simply not the numbers the plan is steered by."];
  if (q.includes("no data")) return ["You can still pick it. The simulation starts it from the typical value for hospitals like yours and marks every result that depends on it.", "Its data then becomes the first thing to collect; it will show on the data guide for your IT team."];
  if (ctx && ctx.ref){ const [,id] = ctx.ref.split(":"); const it = ITEMS[id]; if (it) return [`${it.n}: ${kpiLine(id)}.`, `Picking it brings ${leversOf(id).length} changes into the simulation: ${leversOf(id).slice(0,4).map(l=>ITEMS[l].n).join(", ")}${leversOf(id).length>4?" and more":""}.`, it.why]; }
  return [`${S3.sel.length} of six picked, bringing in ${cover3().levN} changes.`, "Ask about any KPI on the page, or ask me to suggest a balanced six."]; }
function p3_fillCommon(){}
