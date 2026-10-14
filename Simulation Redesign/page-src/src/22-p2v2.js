/* ===== Page 2 · Targets (revised 13 Oct): catalogue-driven, plain English ===== */
["dccoord","icupar","linenpar"].forEach(id => { const c = CATALOGUE.find(x=>x.id===id); if (c) c.f = ["sim_parameters"]; });
const ITEMS = {}; CATALOGUE.forEach(c => ITEMS[c.id] = { ...c, d: Math.sign(c.b - c.t) || 1 });
const INPUTS = {}; CATALOGUE.forEach(c => { INPUTS[c.id] = (c.by||[]).filter(([f]) => ITEMS[f]); });
const OUTPUTS = {}; CATALOGUE.forEach(c => (c.by||[]).forEach(([f]) => { (OUTPUTS[f] ||= []).push(c.id); }));
const TS = { user:{}, go:{} }; CATALOGUE.filter(c=>c.x==="a").forEach(c => TS.go[c.id] = c.go);
const GNAME = Object.fromEntries(GROUPS.map(g=>[g[0],g[1]]));

const isSwitch = it => it.u === "switch";
function hasData(id){ const it = ITEMS[id]; if (it.x==="a" || (it.g==="up" && isSwitch(it))) return true; if (!it.f.length) return false; return it.f.every(f => ST.files[f]); }
function isShown(id){ const it = ITEMS[id]; return it.core || hasData(id); }
function noDataWhy(id){ const it = ITEMS[id]; if (!it.f.length) return "Not recorded today"; return `Needs ${it.f.filter(f=>!ST.files[f]).map(f=>FILE_NAME[f]||f).join(" and ")}`; }
function valOf(id){ return TS.user[id] ?? ITEMS[id].r; }
function fracOf(id, v = valOf(id)){ const it = ITEMS[id]; if (it.b === it.t) return v === it.b ? 1 : 0; return Math.max(0, Math.min(1.3, (v - it.t) / (it.b - it.t))); }
function supportFrac(id){ const ins = INPUTS[id]; if (!ins || !ins.length) return null; const tw = ins.reduce((s,x)=>s+x[1],0); return ins.reduce((s,[f,w])=>s + w*Math.min(1,fracOf(f)),0) / tw; }
function likelyOf(id){ const s = supportFrac(id); if (s===null) return null; const it = ITEMS[id]; return it.t + s*(it.b - it.t); }
function addsUp(id){ const s = supportFrac(id); if (s===null) return null; const g = Math.min(1,fracOf(id)) - s; return g > .12 ? "short" : g < -.2 ? "room" : "ok"; }
function helpers(id, n=3){ return (INPUTS[id]||[]).map(([f,w]) => [f, w*(1-Math.min(1,fracOf(f)))]).filter(x=>x[1]>0.01).sort((a,b)=>b[1]-a[1]).slice(0,n).map(x=>x[0]); }
function fmtV(id, v = valOf(id)){ const it = ITEMS[id];
  if (v === null || v === undefined) return "—";
  if (isSwitch(it)) return v >= 0.5 ? (it.x==="a"?"On":"Yes") : (it.x==="a"?"Off":"No");
  if (it.u === "time"){ const h = Math.floor(v), m = Math.round((v-h)*60); return `${h > 12 ? h-12 : h}:${String(m).padStart(2,"0")} ${h<12?"am":"pm"}`; }
  const dp = it.dp || 0; return (+v).toLocaleString("en-IN", {minimumFractionDigits:dp, maximumFractionDigits:dp}); }
const unitOf = it => (it.u==="switch"||it.u==="time") ? "" : it.u;
const withU = (id, v) => { const u = unitOf(ITEMS[id]), x = fmtV(id, v); if (!u) return x; if (u.startsWith("%")) return x + u; if (u === "₹") return "₹" + x; if (u.startsWith("₹ ")) return "₹" + x + " " + u.slice(2); return x + " " + u; };
function gapWords(id, a, b){ const it = ITEMS[id], d = Math.abs(a-b); const dp = it.dp || 0; const n = d.toLocaleString("en-IN",{maximumFractionDigits:Math.max(dp,1)});
  return it.u.startsWith("%") ? `${n} points` : `${n} ${unitOf(it) || ""}`.trim(); }
function stepOf(it){ if (isSwitch(it)) return 1; if (it.u==="time") return 0.25; return it.dp ? Math.pow(10,-it.dp) : 1; }
function rangeOf(it){ const lo = Math.min(it.t,it.b), hi = Math.max(it.t,it.b), pad = (hi-lo)*0.18 || 1; const st = stepOf(it);
  let mn = lo - pad, mx = hi + pad; if (lo >= 0 && mn < 0) mn = 0; if (it.u.startsWith("%") && mx > 100) mx = 100; return [Math.floor(mn/st)*st, Math.ceil(mx/st)*st]; }
const p2listeners = [];
function setTarget(id, v){ const it = ITEMS[id]; if (v === null || v === undefined || v === "" || Number.isNaN(v)) delete TS.user[id]; else { const st = stepOf(it); TS.user[id] = Math.round(v/st)*st; } p2listeners.forEach(fn=>fn(id)); }
function resetAll(){ TS.user = {}; p2listeners.forEach(fn=>fn(null)); }
function fillSupport(id){ const a = Math.min(1, fracOf(id)); const touched = [];
  (INPUTS[id]||[]).forEach(([f]) => { if (TS.user[f] !== undefined) return; const it = ITEMS[f]; let v = it.t + a*(it.b - it.t); if (isSwitch(it)) v = a >= 0.5 ? 1 : 0; const st = stepOf(it); TS.user[f] = Math.round(v/st)*st; touched.push(f); });
  p2listeners.forEach(fn=>fn(null)); return touched; }
function shownIds(g){ return CATALOGUE.filter(c => (!g || c.g===g) && isShown(c.id)).map(c=>c.id); }
function counts(){ const ids = shownIds(); const set = ids.filter(id => TS.user[id] !== undefined); const fin = shownIds("fin");
  return { all:ids.length, set:set.length, nodata: ids.filter(id=>!hasData(id)), short: fin.filter(id=>addsUp(id)==="short"), fin, cat:CATALOGUE.length,
    extraShown: ids.filter(id=>!ITEMS[id].core).length, hidden: CATALOGUE.filter(c=>!isShown(c.id)) }; }

/* ---------- a ruler: today, realistic in 12 months, best practice, and your pin. Right is always better. ---------- */
function rulerHTML(id, cls=""){
  const it = ITEMS[id]; const [mn,mx] = rangeOf(it);
  const P = v => { let p = (v-mn)/(mx-mn); if (it.d < 0) p = 1-p; return (Math.max(0,Math.min(1,p))*100).toFixed(2); };
  return `<div class="rl ${cls}${hasData(id)?"":" nodata"}" data-rl="${id}" style="--pt:${P(it.t)}%;--pr:${P(it.r)}%;--pb:${P(it.b)}%">
    <div class="rl-track"><i class="rl-gap"></i><i class="rl-mk rl-t"></i><i class="rl-mk rl-r"></i><i class="rl-mk rl-b"></i></div>
    <input type="range" id="rg-${id}" aria-label="Your target for ${esc(it.n)}" min="${mn}" max="${mx}" step="${stepOf(it)}" value="${valOf(id)}" ${it.d<0?'dir="rtl"':''} data-rg="${id}">
  </div>`; }
function wireTargets(root){
  root.querySelectorAll("[data-rg]").forEach(r => r.addEventListener("input", () => setTarget(r.dataset.rg, +r.value)));
  root.querySelectorAll("[data-num]").forEach(n => n.addEventListener("change", () => setTarget(n.dataset.num, n.value===""?null:+n.value)));
  root.querySelectorAll("[data-sw]").forEach(b => b.addEventListener("click", () => setTarget(b.dataset.sw, valOf(b.dataset.sw) >= 0.5 ? 0 : 1)));
  root.querySelectorAll("[data-go]").forEach(s => s.addEventListener("change", () => { TS.go[s.dataset.go] = +s.value; p2listeners.forEach(fn=>fn(s.dataset.go)); }));
  root.querySelectorAll("[data-p2]").forEach(b => b.addEventListener("click", () => { const a = b.dataset.p2;
    if (a==="reset") resetAll(); else if (a==="go") goNext2();
    else if (a.startsWith("fill:")) { const id = a.slice(5), t = fillSupport(id); toast(t.length ? `Raised ${t.length} of the targets that affect ${ITEMS[id].n}, to match yours. Targets you typed yourself were not changed.` : `Every target that affects ${ITEMS[id].n} is already one you set, so nothing was changed.`); } }));
}
function syncTargets(root){
  root.querySelectorAll("[data-rg]").forEach(r => { if (document.activeElement !== r) r.value = valOf(r.dataset.rg); r.closest(".rl")?.classList.toggle("mine", TS.user[r.dataset.rg] !== undefined); });
  root.querySelectorAll("[data-num]").forEach(n => { if (document.activeElement !== n) n.value = TS.user[n.dataset.num] ?? ""; n.placeholder = fmtV(n.dataset.num, ITEMS[n.dataset.num].r); });
  root.querySelectorAll("[data-tv]").forEach(e => e.textContent = fmtV(e.dataset.tv));
  root.querySelectorAll("[data-sw]").forEach(b => { const id = b.dataset.sw, on = valOf(id) >= 0.5; b.setAttribute("aria-pressed", on); b.textContent = ITEMS[id].x==="a" ? (on?"Switched on":"Off") : (on?"Yes":"No"); b.classList.toggle("mine", TS.user[id] !== undefined); });
  root.querySelectorAll("[data-mine]").forEach(e => e.classList.toggle("mine", TS.user[e.dataset.mine] !== undefined));
}
function goNext2(){ const c = counts(); toast(`${c.set} targets of yours and ${c.all-c.set} at the realistic value are kept. `); goStep(2); }

/* ---------- card for each parameter ---------- */
function sourceLine(id){ const it = ITEMS[id];
  if (it.x==="a" || (it.g==="up" && isSwitch(it) && !it.f.length)) return "A decision, no data needed";
  if (hasData(id)) return `From ${it.f.map(f=>FILE_NAME[f]||f).join(" and ")}`;
  return `${noDataWhy(id)}. Until then we start from what is typical for hospitals like yours.`; }
function addsUpSentence(id){ const st = addsUp(id); if (!st) return ""; const it = ITEMS[id], L = likelyOf(id), tgt = valOf(id);
  const hs = helpers(id).map(h => ITEMS[h].n);
  if (st==="short") return `Your other targets would take this to about <b>${esc(withU(id, L))}</b>, not ${esc(withU(id, tgt))}: about ${esc(gapWords(id, tgt, L))} short. To close the gap, raise ${esc(hs.join(", ") || "the targets that affect it")}.`;
  if (st==="room") return `Your other targets would take this further than you have asked, to about <b>${esc(withU(id, L))}</b>. You could raise this target.`;
  return `Your other targets are enough to reach this, at about <b>${esc(withU(id, L))}</b>.`; }
const ST_WORD = { short:"Needs more from other targets", ok:"Your other targets are enough", room:"Could go further" };
function itemDetail(id){
  const it = ITEMS[id], has = hasData(id), st = addsUp(id);
  const grp = GNAME[it.g] + (it.g==="up" ? ` · ${UPSUB[it.x==="s"?"w":it.x] || ""}` : "");
  const pill = !has ? `<span class="d-pill off">No data yet</span>` : st ? `<span class="d-pill ${st==="short"?"off":st==="room"?"ahead":"ahead"}">${ST_WORD[st]}</span>` : "";
  const ins = (INPUTS[id]||[]).slice().sort((a,b)=>b[1]-a[1]), outs = OUTPUTS[id] || [];
  const strength = w => w >= .7 ? "strong" : w >= .4 ? "medium" : "light";
  return `<div class="d-eyebrow">${esc(grp)}</div><div class="d-title">${esc(it.n)}</div>
  <p class="d-sub">${pill} &nbsp;${TS.user[id]!==undefined?"You set this target.":"This is the realistic value until you change it."}</p>
  <div class="d-why"><span>How we look at it</span>${esc(it.why)}</div>
  <div class="d-four"><div><span>${has?"Today":"Typical start (no data yet)"}</span><b>${fmtV(id,it.t)}</b></div><div><span>Realistic in 12 months</span><b>${fmtV(id,it.r)}</b></div><div class="now"><span>Your target</span><b>${fmtV(id)}</b></div><div><span>Best practice</span><b>${fmtV(id,it.b)}</b></div></div>
  ${unitOf(it)?`<p class="d-sub" style="margin:-6px 0 8px">All figures in ${esc(unitOf(it))}.</p>`:""}
  ${st?`<div class="d-sec"><h4>Will your other targets get it there?</h4><p style="margin:0">${addsUpSentence(id)}</p>${st==="short"?`<p style="margin:8px 0 0"><button type="button" class="d-fill" data-fillsheet="${id}">Raise the targets that affect it to match</button></p>`:""}</div>`:""}
  ${ins.length?`<div class="d-sec"><h4>What it is affected by</h4><ul class="d-ms">${ins.map(([f,w])=>`<li><span class="src src-${w>=.7?"yours":w>=.4?"manual":"ref"}">${strength(w)} effect</span><span><b>${esc(ITEMS[f].n)}</b> · target ${esc(withU(f))}${TS.user[f]!==undefined?" (yours)":""}${hasData(f)?"":" · no data yet"}</span></li>`).join("")}</ul></div>`:""}
  ${outs.length?`<div class="d-sec"><h4>What it affects downstream</h4><ul class="d-ms">${outs.map(o=>`<li><span class="src src-yours">affects</span><span><b>${esc(ITEMS[o].n)}</b></span></li>`).join("")}</ul></div>`:""}
  <div class="d-sec"><h4>Where the figure comes from</h4><p style="margin:0">${esc(sourceLine(id))}</p></div>
  ${it.x==="a"?`<div class="d-sec"><h4>Go-live</h4><p style="margin:0">Month ${TS.go[id]} of the project. Its effect starts then and builds over the next two months.</p></div>`:""}`;
}
function p2Detail(key){ const c = counts();
  if (key==="nodata") return `<div class="d-eyebrow">Reading</div><div class="d-title">${c.nodata.length} parameters with no data yet</div><p style="margin:0">You can still set a target for each one. Until its data arrives we start from what is typical for hospitals like yours, and mark it on the page.</p>
    <div class="d-sec"><h4>What is missing</h4><ul class="d-list">${c.nodata.map(id=>`<li><span class="ck late">!</span><span>${esc(ITEMS[id].n)} <small style="color:var(--sh-mute)">· ${esc(GNAME[ITEMS[id].g])}</small></span><em>${esc(noDataWhy(id))}</em></li>`).join("")}</ul></div>`;
  if (key==="short") return `<div class="d-eyebrow">Reading</div><div class="d-title">Financial targets: will they add up?</div><p style="margin:0">For each financial target we check whether the other targets on this page are enough to get there.</p>
    <div class="d-sec"><ul class="d-list">${c.fin.map(id=>{ const st = addsUp(id); return `<li><span class="ck ${st==="short"?"late":"y"}">${st==="short"?"!":"✓"}</span><span>${esc(ITEMS[id].n)}: target ${esc(withU(id))}</span><em class="${st==="short"?"late":""}">${st?`likely ${esc(withU(id, likelyOf(id)))}`:""}</em></li>`; }).join("")}</ul></div>`;
  if (key==="shown") return `<div class="d-eyebrow">What is on this page</div><div class="d-title">${c.all} of ${c.cat} parameters shown</div>
    <p style="margin:0">${c.all - c.extraShown} are parameters we assess in every hospital; they always appear, with or without data. ${c.extraShown} more appear because your files contain them.</p>
    ${c.hidden.length?`<div class="d-sec"><h4>Would appear if you send</h4><ul class="d-list">${c.hidden.map(h=>`<li><span class="ck"></span><span>${esc(h.n)}</span><em>${esc(h.f.map(f=>FILE_NAME[f]||f).join(", "))}</em></li>`).join("")}</ul></div>`:""}`;
  return `<div class="d-eyebrow">Reading</div><div class="d-title">${c.set} targets set by you</div><p style="margin:0">Everything else stays at the realistic value: what hospitals of your size and type reached in twelve months from a similar start.</p>`; }
function p2_detailFor(ref){ const [t,id] = ref.split(":");
  if (t==="it") { const st = addsUp(id); return [itemDetail(id), !hasData(id)||st==="short"?"off":"ahead"]; }
  if (t==="p2") return [p2Detail(id), "watch"];
  return ["",""]; }
function p2_peekFor(ref){ const [t,id] = ref.split(":");
  if (t==="it") { const it = ITEMS[id], st = addsUp(id);
    return `<div class="pk-t">${esc(it.n)}</div><div class="pk-n">${esc(fmtV(id))} <small style="font-size:13px">${esc(unitOf(it))}</small></div><div class="pk-m">${hasData(id)?"Today":"Typical (no data yet)"} ${esc(fmtV(id,it.t))} · realistic ${esc(fmtV(id,it.r))} · best ${esc(fmtV(id,it.b))}</div>${st?`<div class="pk-m"><b>${ST_WORD[st]}</b>${st!=="ok"?`: likely ${esc(withU(id, likelyOf(id)))}`:""}</div>`:""}<div class="pk-hint">Click for how we look at it, and what affects it</div>`; }
  if (t==="p2") return `<div class="pk-t">${{set:"Targets you set",nodata:"No data yet",short:"Financial targets that need more",shown:"What is on this page"}[id]}</div><div class="pk-hint">Click for the full list</div>`;
  return ""; }
function p2_contextFor(ref){ const [t,id] = ref.split(":");
  if (t==="it") { const it = ITEMS[id]; return { kind: GNAME[it.g], point:`the target for ${it.n}`, title:it.n, lines:[`Target ${withU(id)} · ${hasData(id)?"today":"typical"} ${withU(id, it.t)}`].concat(addsUp(id)?[`${ST_WORD[addsUp(id)]}`]:[]) }; }
  return { kind:"Targets", point:"the targets so far", title:"Targets", lines:[] }; }
document.addEventListener("click", e => { const b = e.target.closest("[data-fillsheet]"); if (!b) return; const id = b.dataset.fillsheet, t = fillSupport(id); closeSheet(); toast(t.length ? `Raised ${t.length} targets that affect ${ITEMS[id].n}. Yours were not changed.` : "Nothing to change: those targets are all yours."); });

/* ---------- chat, in plain English ---------- */
function p2_chatOpening(){ const c = counts();
  const sh = c.short.map(id => `${ITEMS[id].n} (target ${withU(id)}, likely ${withU(id, likelyOf(id))})`);
  return { msg:[ `Every target starts at the realistic value: what hospitals of your size reached in twelve months from a start like yours. You have set ${c.set} of your own.`,
      c.short.length ? `Some financial targets need more than your other targets give them: ${sh.join("; ")}. The biggest help would come from ${helpers(c.short[0]).map(h=>ITEMS[h].n).join(", ")}.` : "Your other targets are enough to reach every financial target.",
      c.nodata.length ? `${c.nodata.length} parameters have no data yet. You can still set targets for them; I start them from typical values and mark them.` : "",
      "Move a pin, type a number, or ask me to raise what a target needs." ].filter(Boolean),
    note: c.short.length ? `${ITEMS[c.short[0]].n} ${withU(c.short[0])} needs more support.` : "Your targets add up.",
    points: [ ...c.short.slice(0,2).map(id => `${ITEMS[id].n}: likely ${withU(id, likelyOf(id))}, target ${withU(id)}`), `${c.nodata.length} parameters with no data yet`, "Automations and when they go live" ],
    asks: [ `Raise what ${c.short.length ? ITEMS[c.short[0]].n : "EBITDA"} needs`, "Where do the realistic values come from?", "Which of these will cost the most?" ] }; }
function p2_fillChat(){ const c = p2_chatOpening();
  document.getElementById("chatSub").textContent = "Simulation · step 2 of 7 · targets";
  chatBody.innerHTML = `<div class="msg">${c.msg.map(m=>`<p>${esc(m)}</p>`).join("")}</div><div class="lbl">Tojo's note</div><div class="note">${esc(c.note)}</div>
  <div class="lbl">Add to a point — pick one or more</div>${c.points.map((t,i)=>`<button class="pt" type="button" aria-pressed="false"><b>P${i+1}</b> ${esc(t)}</button>`).join("")}
  <div class="lbl">Or ask next</div>${c.asks.map(t=>`<button class="ask" type="button">${esc(t)}</button>`).join("")}`;
  chatBody.querySelectorAll(".pt").forEach(b => b.onclick = () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")==="true"?"false":"true"));
  chatBody.querySelectorAll(".ask").forEach(b => b.onclick = () => { chatIn.value = b.textContent; chatIn.focus(); }); }
function p2_replyFor(text, ctx){ const q = text.toLowerCase();
  if (q.startsWith("raise what")) { const it = CATALOGUE.find(c => q.includes(c.n.toLowerCase())) || ITEMS.EBITDA; const t = fillSupport(it.id);
    return [ t.length ? `Done. I raised ${t.length} targets that affect ${it.n} so they match the target you set, and left your own targets alone.` : `Every target that affects ${it.n} is one you set, so I changed nothing.`, addsUp(it.id) ? addsUpSentence(it.id).replace(/<[^>]+>/g,"") : "" ]; }
  if (ctx && ctx.ref){ const [,id] = ctx.ref.split(":"); const it = ITEMS[id]; if (it){
    return [ `${it.n}: target ${withU(id)}, ${hasData(id)?"today":"typical start"} ${withU(id, it.t)}.`, addsUp(id) ? addsUpSentence(id).replace(/<[^>]+>/g,"") : "", it.why,
      hasData(id) ? "Nothing is late yet: these are targets. Once the plan is locked, each one gets an owner and I track it week by week." : `There is no data for it yet (${noDataWhy(id).toLowerCase()}). Your IT team or the department keeping the register is responsible for it.` ]; } }
  if (q.includes("realistic")) return ["Each realistic value is what hospitals of your size and type reached in twelve months from a similar start, taken from our reference files.", "Once you have twelve months of your own data, the realistic value comes from your own trend instead."];
  if (q.includes("cost")) return ["Costs come on page 5, What's possible, where each change gets its one-time and monthly cost.", "On this page the biggest costs are in staffing and equipment: ICU nurses, ventilators and an own MRI."];
  const c = counts(); return [`${c.set} targets are yours; ${c.all-c.set} are at the realistic value. ${c.short.length} financial target${c.short.length===1?" needs":"s need"} more from the others.`, "Pick any parameter on the page and ask me about it."]; }

function p2_fillCommon(){}
