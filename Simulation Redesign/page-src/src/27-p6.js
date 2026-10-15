/* ===== Page 6 · Your team: who leads each approved change =====
   Built from the frozen plan (page 5). Each change has a lead department and helping departments, taken from the
   old simulation's task map (which departments do the work, by count of tasks). The hospital names the head of each
   department involved, with a mobile number; Tojo then sends each head their own daily tasks (page 7).
   The lead of a change can be moved to another department. Each selected KPI also has an owner. */
const DEPTS = {
  owner:["Hospital owner / CEO","Leadership"], medical_dir:["Medical Director","Clinical"], nursing:["Chief Nursing Officer","Clinical"],
  icu:["ICU in-charge","Clinical"], pharmacy:["Pharmacy head","Clinical"], coo:["COO / Operations head","Operations"],
  biomedical:["Biomedical engineering head","Operations"], housekeeping:["Housekeeping supervisor","Operations"], cssd:["CSSD in-charge","Operations"],
  finance:["CFO / Finance head","Business"], procurement:["Procurement head","Business"], marketing:["Marketing head","Business"],
  hr:["HR head","Business"], it:["IT head","Business"] };
const DEPT_ORDER = Object.keys(DEPTS);
/* lead first, then helpers */
const CHANGE_DEPTS = {
  icunurse:["nursing","hr","icu"], wardnurse:["nursing","hr","coo"], icubeds:["biomedical","coo","procurement","nursing","icu"],
  ventk:["biomedical","icu","procurement","finance"], autoclave:["biomedical","cssd","procurement"], carm:["biomedical","procurement","coo"],
  lap:["biomedical","procurement","nursing"], echo:["biomedical","procurement","medical_dir"], usg:["biomedical","procurement","coo"],
  ct:["biomedical","procurement","medical_dir","finance"], mri:["biomedical","coo","procurement","finance","medical_dir"],
  biomed:["biomedical","hr"], hk:["housekeeping","coo","hr"], linenpar:["housekeeping","coo","procurement"],
  billexec:["finance","hr"], preauthstaff:["finance","hr","coo"], dccoord:["coo","medical_dir","nursing","hr"],
  coun:["marketing","coo","hr"], incentive:["finance","marketing","owner","hr"], icupar:["pharmacy","icu","procurement"],
  generic:["pharmacy","medical_dir","procurement"], cssdtech:["cssd","hr","biomedical"], round8:["medical_dir","coo","nursing"],
  implant:["procurement","finance","medical_dir"],
  s_dis:["coo","nursing","it"], s_bill:["finance","it"], s_adm:["coo","finance","it"], s_diag:["coo","medical_dir","it"], s_proc:["procurement","finance","it"] };
const KPI_DEPT = { fin:"finance", ops:"coo", clin:"medical_dir", mkt:"marketing", adm:"hr", up:"coo" };
const TEAM = { people:{}, lead:{}, kpi:{}, done:null };
function deptsOf(id){ return CHANGE_DEPTS[id] || ["coo"]; }
function leadOf(id){ return TEAM.lead[id] || deptsOf(id)[0]; }
function helpersOf(id){ const l = leadOf(id); return deptsOf(id).filter(d => d !== l); }
/* KPI owner: the department answerable for it. EBITDA sits with the owner; claims and billing KPIs with finance; otherwise by group. */
const KPI_OWNER = { EBITDA:"owner", sublag:"finance", RECV:"finance", denial:"finance", preauth:"finance" };
function kpiOwner(k){ return TEAM.kpi[k] || KPI_OWNER[k] || KPI_DEPT[ITEMS[k].g] || "coo"; }
function p6Data(){ const d = p5Data(); const used = new Set(["owner"]);
  d.changes.forEach(c => { used.add(leadOf(c.id)); helpersOf(c.id).forEach(h => used.add(h)); });
  d.kpis.forEach(x => used.add(kpiOwner(x.k)));
  const depts = DEPT_ORDER.filter(k => used.has(k)).map(k => { const leads = d.changes.filter(c => leadOf(c.id) === k), helps = d.changes.filter(c => helpersOf(c.id).includes(k));
    const all = [...leads, ...helps], from = all.length ? Math.min(...all.map(c=>c.start)) : null, to = all.length ? Math.max(...all.map(c=>c.full)) : null;
    return { k, role: DEPTS[k][0], area: DEPTS[k][1], leads, helps, kpis: d.kpis.filter(x => kpiOwner(x.k) === k), from, to, cost: leads.reduce((a,c)=>a+c.tot,0) }; });
  return { ...d, depts }; }
const personOf = k => TEAM.people[k] || {};
const named = k => !!(personOf(k).name || "").trim();
const mobileOk = m => /^\+?[0-9 ]{10,15}$/.test((m||"").trim());
const whoLabel = k => named(k) ? `${personOf(k).name.trim()}` : DEPTS[k][0];
const titleOf = k => (personOf(k).title || "").trim();
function teamCount6(d){ const n = d.depts.filter(x => named(x.k) && mobileOk(personOf(x.k).mobile)).length; return { n, of: d.depts.length }; }

/* ---------- shared parts ---------- */
function p6Head(title, lede){ return `<div class="p2head" style="grid-template-columns:1fr"><div><div class="eb">Simulation · step 6 of 7 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>${title}</h1><p class="lede">${lede}</p></div></div>`; }
function p6Tiles(d){ return `<section class="top5 p5t" aria-label="Team summary">
  <div class="t5 hl"><span>Heads added</span><b data-v="p6n"></b><small>name and mobile number</small></div>
  <div class="t5"><span>Departments</span><b>${d.depts.length}</b><small>involved in this plan</small></div>
  <div class="t5"><span>Changes</span><b>${d.changes.length}</b><small>each with one lead</small></div>
  <div class="t5"><span>Selected KPIs</span><b>${d.kpis.length}</b><small>each with one owner</small></div>
  <div class="t5"><span>Plan length</span><b>${d.s.D} months</b><small>${money(d.s.tot)} in total</small></div>
  <div class="t5"><span>Busiest head</span><b data-v="p6busy"></b><small data-v="p6busyS"></small></div></section>`; }
function personInputs(k, compact, title){ return `<div class="pi6${compact?" c":""}${title?" t3":""}" data-noopen><label><small>Name</small><input type="text" data-pn="${k}" placeholder="Full name" autocomplete="off"></label>${title?`<label><small>Designation</small><input type="text" data-pt="${k}" placeholder="e.g. Chief Financial Officer" autocomplete="off"></label>`:""}<label><small>Mobile</small><input type="tel" data-pm="${k}" placeholder="10-digit mobile" inputmode="tel"></label></div>`; }
function leadSelect(id){ return `<select data-lead="${id}" aria-label="Lead for ${esc(ITEMS[id].n)}">${deptsOf(id).concat(DEPT_ORDER.filter(k => !deptsOf(id).includes(k))).map(k => `<option value="${k}">${esc(DEPTS[k][0])}</option>`).join("")}</select>`; }
function p6Actions(){ return `<div class="bulk5"><button type="button" class="act" data-p6="owner">Use the owner for every empty department</button><button type="button" class="act ghost" data-p6="clear">Clear all names</button><button type="button" class="go ready frz" data-p6="confirm">Confirm the team</button></div>`; }
function p6Done(){ return `<p class="cf6" data-v="cf6" hidden></p>`; }
function p6Mount(stage, inner){ stage.innerHTML = `<div class="lk lk-web">${journeyHTML(5)}${SIMR.frozen ? inner : `<div class="empty5"><h1>No plan frozen yet</h1><p>Freeze and confirm a plan first.</p><button type="button" class="go ready" data-p6="back">Go to Simulate</button></div>`}</div>`; wire6(stage); }
function wire6(root){
  root.querySelectorAll("[data-pn],[data-pm],[data-pt]").forEach(n => { const a = n.dataset.pn ? "pn" : n.dataset.pm ? "pm" : "pt", k = n.dataset[a], f = { pn:"name", pm:"mobile", pt:"title" }[a];
    n.addEventListener("input", () => { TEAM.people[k] = { ...personOf(k), [f]: n.value }; TEAM.done = null; root.querySelectorAll(`[data-${a}="${k}"]`).forEach(o => { if (o !== n) o.value = n.value; }); CUR.update(root); }); });
  root.querySelectorAll("[data-lead]").forEach(s => s.addEventListener("change", () => { TEAM.lead[s.dataset.lead] = s.value; TEAM.done = null; mountLook(LOOKS.indexOf(CUR)); }));
  root.querySelectorAll("[data-kown]").forEach(s => s.addEventListener("change", () => { TEAM.kpi[s.dataset.kown] = s.value; TEAM.done = null; mountLook(LOOKS.indexOf(CUR)); }));
  root.querySelectorAll("[data-p6]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); const a = b.dataset.p6, d = p6Data();
    if (a === "back") goStep(3);
    else if (a === "owner") { const o = personOf("owner"); if (!named("owner")) { toast("Add the owner's name and mobile first."); root.querySelector('[data-pn="owner"]')?.focus(); return; }
      d.depts.forEach(x => { if (!named(x.k)) TEAM.people[x.k] = { name:o.name, mobile:o.mobile }; }); mountLook(LOOKS.indexOf(CUR)); toast("The owner is now named for every department that was empty."); }
    else if (a === "clear") { TEAM.people = {}; TEAM.done = null; TFILE.last = null; TFILE.unmatched = []; mountLook(LOOKS.indexOf(CUR)); }
    else if (a === "confirm") { const miss = d.depts.filter(x => !named(x.k) || !mobileOk(personOf(x.k).mobile));
      if (miss.length) { toast(`Add a name and a valid mobile for ${miss.length} more: ${miss.slice(0,3).map(x=>x.role).join(", ")}${miss.length>3?"…":""}.`); const f = root.querySelector(`[data-pn="${miss[0].k}"]`); if (f) { f.scrollIntoView({block:"center"}); f.focus(); } return; }
      TEAM.done = new Date(); sync6(root); }
    else if (a === "next") goStep(6, "Team confirmed."); }));
}
function sync6(root, typing){ if (!SIMR.frozen) return; const d = p6Data(), c = teamCount6(d);
  const set = (k,v) => root.querySelectorAll(`[data-v="${k}"]`).forEach(e => e.innerHTML = v);
  set("p6n", `${c.n}<i>/${c.of}</i>`);
  const busy = [...d.depts].sort((a,b) => (b.leads.length*2+b.helps.length) - (a.leads.length*2+a.helps.length))[0];
  set("p6busy", esc(busy ? whoLabel(busy.k).split(" ")[0] : "—")); set("p6busyS", busy ? `${esc(busy.role)}: leads ${busy.leads.length}, helps ${busy.helps.length}` : "");
  if (!typing) { root.querySelectorAll("[data-pn]").forEach(n => { if (document.activeElement !== n) n.value = personOf(n.dataset.pn).name || ""; });
    root.querySelectorAll("[data-pm]").forEach(n => { if (document.activeElement !== n) n.value = personOf(n.dataset.pm).mobile || ""; });
    root.querySelectorAll("[data-pt]").forEach(n => { if (document.activeElement !== n) n.value = personOf(n.dataset.pt).title || ""; });
    root.querySelectorAll("[data-lead]").forEach(s => s.value = leadOf(s.dataset.lead)); root.querySelectorAll("[data-kown]").forEach(s => s.value = kpiOwner(s.dataset.kown)); }
  root.querySelectorAll("[data-pm]").forEach(n => n.classList.toggle("bad", !!n.value.trim() && !mobileOk(n.value)));
  root.querySelectorAll("[data-who]").forEach(e => { const k = e.dataset.who; e.textContent = named(k) ? whoLabel(k) : e.classList.contains("n") ? "Name not added" : whoLabel(k); e.classList.toggle("none", !named(k)); });
  root.querySelectorAll("[data-dstate]").forEach(e => { const k = e.dataset.dstate, ok = named(k) && mobileOk(personOf(k).mobile); e.dataset.ok = ok; e.textContent = ok ? "Added" : named(k) ? "Mobile needed" : "Not added"; });
  const p = root.querySelector('[data-v="cf6"]'); if (p) { p.hidden = !TEAM.done;
    if (TEAM.done) { p.innerHTML = `<b>Team confirmed</b>, ${esc(fmtDate(TEAM.done))}. Tojo will send each head their own tasks every morning. <button type="button" class="go ready" data-p6n>Go to Taskboards →</button>`; p.querySelector("[data-p6n]").onclick = () => goStep(6, "Team confirmed."); } }
}

/* ---------- details and chat ---------- */
function p6_detailFor(ref){ const [t,id] = ref.split(":");
  if (t === "dept") { const d = p6Data(), x = d.depts.find(y => y.k === id); if (!x) return ["",""];
    return [`<div class="d-eyebrow">${esc(x.area)}</div><div class="d-title">${esc(x.role)}</div>
      <div class="d-four"><div><span>Leads</span><b>${x.leads.length}</b></div><div><span>Helps with</span><b>${x.helps.length}</b></div><div><span>KPIs owned</span><b>${x.kpis.length}</b></div><div class="now"><span>Busy</span><b>${x.from ? `month ${x.from}–${x.to}` : "—"}</b></div></div>
      <div class="d-why"><span>How we chose the lead</span>The department that does most of the tasks for a change leads it; the others help. This comes from the task lists we use to build the taskboards. You can move a lead to another department.</div>
      <div class="d-sec"><h4>Leads</h4><ul class="d-list">${x.leads.map(c => `<li><span class="ck y">✓</span><span>${esc(c.n)}</span><em>month ${c.start}–${c.full}</em></li>`).join("") || "<li>None.</li>"}</ul></div>
      <div class="d-sec"><h4>Helps with</h4><ul class="d-list">${x.helps.map(c => `<li><span class="ck">·</span><span>${esc(c.n)}</span><em>led by ${esc(DEPTS[leadOf(c.id)][0])}</em></li>`).join("") || "<li>None.</li>"}</ul></div>`, "ahead"]; }
  if (t === "it") return withFrozenSel(() => sim_detailFor(ref));
  return ["",""]; }
function p6_peekFor(ref){ const [t,id] = ref.split(":"); if (t === "dept") { const x = p6Data().depts.find(y => y.k === id); return x ? `<div class="pk-t">${esc(x.role)}</div><div class="pk-m">Leads ${x.leads.length} · helps with ${x.helps.length}</div>` : ""; }
  if (t === "it") return withFrozenSel(() => sim_peekFor(ref)); return `<div class="pk-hint">Click for the detail</div>`; }
function p6_contextFor(ref){ const [t,id] = ref.split(":"); if (t === "dept") return { kind:"Department", point:DEPTS[id][0], title:DEPTS[id][0], lines:[] }; if (t === "it") return withFrozenSel(() => sim_contextFor(ref)); return { kind:"Team", point:"the team", title:"Your team", lines:[] }; }
function p6_chatOpening(){ if (!SIMR.frozen) return { msg:["Freeze and confirm a plan first."], note:"No plan yet.", points:[], asks:[] };
  const d = p6Data(), c = teamCount6(d), busy = [...d.depts].sort((a,b) => b.leads.length - a.leads.length)[0];
  return { msg:[ `Your plan needs ${d.depts.length} department heads. ${c.n} of them are added so far.`,
      `${busy.role} leads the most: ${busy.leads.length} changes. Each head will get their own list of tasks every morning, so I need a name and a mobile number for each.`,
      "If one person covers several departments, use the same name. You can also move the lead of any change to another department." ],
    note: c.n === c.of ? "Everyone is in. Confirm the team." : `${c.of - c.n} heads still to add.`,
    points: [ `${c.n} of ${c.of} heads added`, `${busy.role} leads ${busy.leads.length}` ],
    asks: [ "Why does this department lead?", "Can one person lead several departments?", "What will each head receive?" ] }; }
function p6_fillChat(){ const c = p6_chatOpening();
  document.getElementById("chatSub").textContent = "Simulation · step 6 of 7 · Your team";
  chatBody.innerHTML = `<div class="msg">${c.msg.map(m=>`<p>${esc(m)}</p>`).join("")}</div><div class="lbl">Tojo's note</div><div class="note">${esc(c.note)}</div>
  ${c.points.length ? `<div class="lbl">Add to a point — pick one or more</div>${c.points.map((t,i)=>`<button class="pt" type="button" aria-pressed="false"><b>P${i+1}</b> ${esc(t)}</button>`).join("")}` : ""}
  <div class="lbl">Or ask next</div>${c.asks.map(t=>`<button class="ask" type="button">${esc(t)}</button>`).join("")}`;
  chatBody.querySelectorAll(".pt").forEach(b => b.onclick = () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")==="true"?"false":"true"));
  chatBody.querySelectorAll(".ask").forEach(b => b.onclick = () => { chatIn.value = b.textContent; chatIn.focus(); }); }
function p6_replyFor(text, ctx){ const q = text.toLowerCase();
  if (q.includes("why does")) return [ "The department that does most of the tasks for a change leads it. For a new ventilator, biomedical engineering does the specification, installation and checks; procurement and finance help with the purchase.", "Change the lead with the drop-down next to any change." ];
  if (q.includes("one person") || q.includes("several")) return [ "Yes. Type the same name and mobile for each department they cover, or press \"Use the owner for every empty department\".", "Their tasks are then combined into one daily list." ];
  if (q.includes("receive")) return [ "Each head gets a short list every morning: what is due this week for the changes they lead or help with, and what is late.", "The owner gets one summary across every department." ];
  const d = p6Data(), c = teamCount6(d); return [ `${c.n} of ${c.of} heads added.`, "Ask about any department or change." ]; }
function p6_fillCommon(){}
