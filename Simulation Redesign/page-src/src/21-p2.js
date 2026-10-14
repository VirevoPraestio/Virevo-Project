/* ===== Page 2 · Targets: shared runtime (overrides the page-1 readings, details and chat) ===== */
const ITEMS = {};
KPIS.forEach(k => ITEMS[k.id] = { id:k.id, kind:"kpi", n:k.n, s:k.s, ...TGT[k.id] });
DOMAINS.forEach(d => d.ms.forEach(m => { const x = TGT[m.id]; if (!x || x.same || x.none) return; ITEMS[m.id] = { id:m.id, kind:"ms", n:m.n, fam:d.id, ...x }; }));
LEVERS.forEach(l => ITEMS[l.id] = { kind:"lever", d:l.d ?? Math.sign(l.b - l.t || 1), ...l });
const resolve = id => { const x = TGT[id]; if (x && x.same) return x.same.startsWith("L:") ? x.same.slice(2) : x.same; return id; };
/* inputs of each target: measures and KPIs from LINKS, levers from LEVERS */
const INPUTS = {};
const addIn = (to, from, w) => { to = resolve(to); from = resolve(from); if (!ITEMS[to] || !ITEMS[from] || to===from) return; const L = (INPUTS[to] ||= []); const ex = L.find(x=>x[0]===from); if (ex) ex[1] = Math.max(ex[1], w); else L.push([from, w]); };
LINKS.forEach(([s,t,w]) => addIn(t, s, w));
LEVERS.forEach(l => l.m.forEach(([to,w]) => addIn(to, l.id, w)));
const TS = { user:{}, go:{} };
LEVERS.filter(l=>l.k==="auto").forEach(l => TS.go[l.id] = l.go);

const isSwitch = it => it.u === "switch";
function valOf(id){ const it = ITEMS[id]; return TS.user[id] ?? it.r; }
function fracOf(id, v = valOf(id)){ const it = ITEMS[id]; if (it.b === it.t) return v === it.b ? 1 : 0; return Math.max(0, Math.min(1, (v - it.t) / (it.b - it.t))); }
function backed(id){ const ins = INPUTS[id]; if (!ins || !ins.length) return null; const tw = ins.reduce((s,x)=>s+x[1],0); return ins.reduce((s,[f,w])=>s + w*fracOf(f),0) / tw; }
function tension(id){ const a = fracOf(id), b = backed(id); if (b===null) return 0; return a - b; }
function fmtV(id, v = valOf(id)){ const it = ITEMS[id];
  if (isSwitch(it)) return v >= 0.5 ? "On" : "Off";
  if (it.u === "time"){ const h = Math.floor(v), m = Math.round((v-h)*60); return `${h}:${String(m).padStart(2,"0")}${h<12?" am":" pm"}`; }
  const dp = it.dp || 0; return (+v).toLocaleString("en-IN", {minimumFractionDigits:dp, maximumFractionDigits:dp}); }
const unitOf = it => (it.u==="switch"||it.u==="time") ? "" : it.u;
function srcOfItem(id){ const it = ITEMS[id]; if (it.kind==="ms") return msState(MS[id]); if (it.kind==="kpi") { const sh = kpiShare(id); return sh && sh.pct >= 50 ? "yours" : "ref"; } return "plan"; }
function stepOf(it){ if (isSwitch(it)) return 1; if (it.u==="time") return 0.25; return it.dp ? Math.pow(10,-it.dp) : 1; }
function rangeOf(it){ const lo = Math.min(it.t,it.b), hi = Math.max(it.t,it.b), pad = (hi-lo)*0.18 || 1; const st = stepOf(it);
  let mn = lo - pad, mx = hi + pad; if (lo >= 0 && mn < 0) mn = 0; if (it.u.startsWith("%") && mx > 100) mx = 100;
  return [Math.floor(mn/st)*st, Math.ceil(mx/st)*st]; }
const p2listeners = [];
function setTarget(id, v){ const it = ITEMS[id]; if (v === null || v === undefined || v === "") delete TS.user[id]; else { const st = stepOf(it); TS.user[id] = Math.round(v/st)*st; } p2listeners.forEach(fn=>fn(id)); }
function resetAll(){ TS.user = {}; p2listeners.forEach(fn=>fn(null)); }
function backSolve(kid){ const a = fracOf(kid); const touched = [];
  (INPUTS[kid]||[]).forEach(([f]) => { if (TS.user[f] !== undefined || ITEMS[f].kind==="kpi") return; const it = ITEMS[f]; let v = it.t + a*(it.b - it.t); if (isSwitch(it)) v = a >= 0.5 ? 1 : 0; const st = stepOf(it); TS.user[f] = Math.round(v/st)*st; touched.push(f); });
  p2listeners.forEach(fn=>fn(null)); return touched; }
function counts(){ const all = Object.keys(ITEMS); const set = all.filter(id => TS.user[id] !== undefined);
  const tens = KPIS.filter(k => tension(k.id) > 0.15); return { all:all.length, set:set.length, tens, ebA:fracOf("EBITDA"), ebB:backed("EBITDA") }; }
const pct = x => Math.round((x||0)*100) + "%";

/* ---------- a ruler: today, Tojo's realistic, best practice, and your pin. Right is always better. ---------- */
function rulerHTML(id, cls=""){
  const it = ITEMS[id]; const [mn,mx] = rangeOf(it);
  const P = v => { let p = (v-mn)/(mx-mn); if (it.d < 0) p = 1-p; return (Math.max(0,Math.min(1,p))*100).toFixed(2); };
  return `<div class="rl ${cls}" data-rl="${id}" style="--pt:${P(it.t)}%;--pr:${P(it.r)}%;--pb:${P(it.b)}%">
    <div class="rl-track"><i class="rl-gap"></i><i class="rl-mk rl-t" title="Today ${fmtV(id,it.t)}"></i><i class="rl-mk rl-r" title="Tojo's realistic ${fmtV(id,it.r)}"></i><i class="rl-mk rl-b" title="Best practice ${fmtV(id,it.b)}"></i></div>
    <input type="range" id="rg-${id}" aria-label="Your target for ${esc(it.n)}" min="${mn}" max="${mx}" step="${stepOf(it)}" value="${valOf(id)}" ${it.d<0?'dir="rtl"':''} data-rg="${id}">
  </div>`; }
function wireTargets(root){
  root.querySelectorAll("[data-rg]").forEach(r => r.addEventListener("input", () => setTarget(r.dataset.rg, +r.value)));
  root.querySelectorAll("[data-num]").forEach(n => n.addEventListener("change", () => setTarget(n.dataset.num, n.value===""?null:+n.value)));
  root.querySelectorAll("[data-sw]").forEach(b => b.addEventListener("click", () => setTarget(b.dataset.sw, valOf(b.dataset.sw) >= 0.5 ? 0 : 1)));
  root.querySelectorAll("[data-go]").forEach(s => s.addEventListener("change", () => { TS.go[s.dataset.go] = +s.value; p2listeners.forEach(fn=>fn(s.dataset.go)); }));
  root.querySelectorAll("[data-p2]").forEach(b => b.addEventListener("click", () => { const a = b.dataset.p2;
    if (a==="reset") resetAll(); else if (a==="go") goNext2(); else if (a.startsWith("solve:")) { const t = backSolve(a.slice(6)); toast(t.length ? `Set ${t.length} feeding targets to match ${ITEMS[a.slice(6)].n}. Targets you typed were left alone.` : "Every feeding target is already yours; nothing changed."); }
    else if (a.startsWith("tier:")) { const [,id,tier] = a.split(":"); const it = ITEMS[id]; setTarget(id, tier==="t"?it.t:tier==="b"?it.b:null); } }));
}
function syncTargets(root){
  root.querySelectorAll("[data-rg]").forEach(r => { if (document.activeElement !== r) r.value = valOf(r.dataset.rg); r.closest(".rl")?.classList.toggle("mine", TS.user[r.dataset.rg] !== undefined); });
  root.querySelectorAll("[data-num]").forEach(n => { if (document.activeElement !== n) n.value = TS.user[n.dataset.num] ?? ""; n.placeholder = fmtV(n.dataset.num, ITEMS[n.dataset.num].r); });
  root.querySelectorAll("[data-tv]").forEach(e => e.textContent = fmtV(e.dataset.tv));
  root.querySelectorAll("[data-sw]").forEach(b => { const on = valOf(b.dataset.sw) >= 0.5; b.setAttribute("aria-pressed", on); b.textContent = ITEMS[b.dataset.sw].k==="auto" ? (on?"Switched on":"Off") : (on?"In place":"Not in place"); b.classList.toggle("mine", TS.user[b.dataset.sw] !== undefined); });
  root.querySelectorAll("[data-mine]").forEach(e => e.classList.toggle("mine", TS.user[e.dataset.mine] !== undefined));
  root.querySelectorAll("[data-tier]").forEach(b => { const [id,tier] = b.dataset.tier.split(":"); const v = valOf(id), it = ITEMS[id]; const cur = TS.user[id]===undefined ? "r" : v===it.t ? "t" : v===it.b ? "b" : "x"; b.setAttribute("aria-pressed", cur===tier); });
  root.querySelectorAll("[data-ask-bk]").forEach(e => { const id = e.dataset.askBk, a = fracOf(id), b = backed(id), t = tension(id);
    e.style.setProperty("--a", (a*100)+"%"); e.style.setProperty("--b", ((b??a)*100)+"%"); e.dataset.state = t > .15 ? "short" : t < -.15 ? "ahead" : "ok"; });
  const c = counts(); const set = (k,v) => root.querySelectorAll(`[data-v="${k}"]`).forEach(e => e.innerHTML = v);
  set("p2set", `${c.set}<i>/${c.all}</i>`); set("p2setSub", "typed in by you");
  set("p2real", `${c.all-c.set}`); set("p2realSub", "on Tojo's realistic value");
  set("p2eb", `${pct(c.ebA)}<i> / ${pct(c.ebB)}</i>`); set("p2ebSub", "of the gap asked / backed");
  set("p2tens", `${c.tens.length}<i>/9</i>`); set("p2tensSub", c.tens.length ? c.tens.slice(0,2).map(k=>k.n).join(", ") + (c.tens.length>2?"…":"") : "every outcome is backed");
  set("ctaNote2", c.tens.length ? `${c.tens.length} outcome${c.tens.length>1?"s ask":" asks"} more than the targets under ${c.tens.length>1?"them":"it"} back. You can still go on; the simulation will show the shortfall.` : "Every outcome is backed by the targets under it.");
}
function p2PulseHTML(){ return `<div class="pulse" role="group" aria-label="Readings">
  <button type="button" class="pz" data-ref="p2:set"><span class="pl">Targets you set</span><b data-v="p2set"></b><small data-v="p2setSub"></small></button>
  <button type="button" class="pz" data-ref="p2:real"><span class="pl">Left to Tojo</span><b data-v="p2real"></b><small data-v="p2realSub"></small></button>
  <button type="button" class="pz" data-ref="kpi2:EBITDA"><span class="pl">EBITDA</span><b data-v="p2eb"></b><small data-v="p2ebSub"></small></button>
  <button type="button" class="pz" data-ref="p2:tens"><span class="pl">Outcomes not backed</span><b data-v="p2tens"></b><small data-v="p2tensSub"></small></button></div>`; }
function p2CtaHTML(){ return `<div class="cta"><button type="button" class="go ready" data-p2="go">Confirm targets and pick six KPIs <span aria-hidden="true">→</span></button><span class="cta-note" data-v="ctaNote2"></span></div>`; }
function goNext2(){ const c = counts(); toast(`${c.set} targets of yours and ${c.all-c.set} of Tojo's are kept. The next page, Six KPIs, comes in the next round of options.`); }
const LEGEND2 = `<span><i class="lg-t"></i>Today</span><span><i class="lg-r"></i>Tojo's realistic, 12 months</span><span><i class="lg-b"></i>Best practice</span><span><i class="lg-y"></i>Your target</span>`;

/* ---------- details, peek, chat for page 2 ---------- */
function inputsList(id){ return (INPUTS[id]||[]).slice().sort((a,b)=>b[1]-a[1]).map(([f,w]) => { const it = ITEMS[f];
  return `<li><span class="src src-${it.kind==="lever"?"yours":srcOfItem(f)}">${it.kind==="lever"?KIND[it.k][0].split(" ")[0]:it.kind==="kpi"?"Outcome":"Measure"}</span><span><b>${esc(it.n)}</b> · target ${esc(fmtV(f))} ${esc(unitOf(it))} · ${pct(fracOf(f))} of its gap${TS.user[f]!==undefined?" · yours":""}</span></li>`; }).join(""); }
function outputsList(id){ const outs = Object.entries(INPUTS).filter(([,ins]) => ins.some(x=>x[0]===id)).map(([to]) => to);
  return outs.map(to => `<li><span class="src src-yours">Moves</span><span><b>${esc(ITEMS[to].n)}</b></span></li>`).join(""); }
function itemDetail(id){
  const it = ITEMS[id], a = fracOf(id), b = backed(id), t = tension(id);
  const kindWord = it.kind==="kpi" ? "Outcome" : it.kind==="ms" ? `Measure · ${DOM[it.fam].name}` : `Lever · ${KIND[it.k][0]}`;
  const src = it.kind==="ms" ? `<p class="d-sub" style="margin-top:-6px">Today's value: ${SRC_WORD[msState(MS[id])].toLowerCase()}.</p>` : "";
  return `<div class="d-eyebrow">${kindWord}</div><div class="d-title">${esc(it.n)}</div>
  <p class="d-sub">${b!==null?`<span class="d-pill ${t>.15?"off":t<-.15?"ahead":"watch"}">${t>.15?"Asks more than its inputs back":t<-.15?"Inputs would carry it further":"Asked and backed match"}</span> &nbsp;`:""}${TS.user[id]!==undefined?"Your target":"Tojo's realistic value, until you change it"}</p>${src}
  <div class="d-four"><div><span>Today</span><b>${fmtV(id,it.t)}</b></div><div><span>Tojo's realistic</span><b>${fmtV(id,it.r)}</b></div><div class="now"><span>Your target</span><b>${fmtV(id)}</b></div><div><span>Best practice</span><b>${fmtV(id,it.b)}</b></div></div>
  <div class="d-glide" aria-label="Your target closes ${pct(a)} of the gap to best practice"><div class="rail"></div><div class="fill" style="width:${a*100}%"></div><div class="mk" style="left:0"><i>Today</i></div><div class="mk plan" style="left:${fracOf(id,it.r)*100}%"><i>Realistic</i></div><div class="mk" style="left:100%"><i>Best</i></div></div>
  ${b!==null?`<div class="d-sec"><h4>Asked and backed</h4><p style="margin:0">Your target asks for <b>${pct(a)}</b> of the way from today to best practice. The targets that feed it back <b>${pct(b)}</b>.</p></div>`:""}
  ${(INPUTS[id]||[]).length?`<div class="d-sec"><h4>What feeds it</h4><ul class="d-ms">${inputsList(id)}</ul></div>`:""}
  <div class="d-sec"><h4>What it moves</h4><ul class="d-ms">${outputsList(id)||"<li><span></span><span>Nothing further: this is an outcome.</span></li>"}</ul></div>
  ${it.kind==="lever"&&it.k==="auto"?`<div class="d-sec"><h4>Go-live</h4><p style="margin:0">Month ${TS.go[id]} of the project. Its effect starts then and builds over the following two months.</p></div>`:""}`;
}
function p2Detail(id){ const c = counts();
  const T = { set:["Targets you set", `${c.set} of ${c.all}`, "Everything you have not typed in uses Tojo's realistic value: what hospitals of your size and type reached in twelve months from a similar start."],
    real:["Left to Tojo", `${c.all-c.set}`, "These follow Tojo's realistic value. Change any of them by moving its pin or typing a number."],
    tens:["Outcomes not backed", `${c.tens.length} of 9`, "An outcome is not backed when its target asks for more of the gap than the targets feeding it deliver. Raise the feeding targets, or lower the outcome."] }[id];
  return `<div class="d-eyebrow">Reading</div><div class="d-title">${T[0]}: ${T[1]}</div><p style="margin:0">${T[2]}</p>
  <div class="d-sec"><h4>Outcomes, asked and backed</h4><ul class="d-list">${KPIS.map(k=>{ const t = tension(k.id); return `<li><span class="ck ${t>.15?"late":"y"}">${t>.15?"!":"✓"}</span><span>${esc(k.n)} · ${esc(fmtV(k.id))} ${esc(unitOf(ITEMS[k.id]))}</span><em class="${t>.15?"late":""}">${pct(fracOf(k.id))} asked · ${pct(backed(k.id))} backed</em></li>`; }).join("")}</ul></div>`; }
function detailFor(ref){ const [t,id] = ref.split(":");
  if (t==="it" || t==="kpi2") { const x = tension(id); return [itemDetail(id), x>.15?"off":x<-.15?"ahead":"watch"]; }
  if (t==="p2") return [p2Detail(id), counts().tens.length?"watch":"ahead"];
  if (t==="dom") { const s = domStats(DOM[id]); return [domDetail(DOM[id]), s.state==="full"?"ahead":"watch"]; }
  return ["",""]; }
function peekFor(ref){ const [t,id] = ref.split(":");
  if (t==="it" || t==="kpi2") { const it = ITEMS[id], b = backed(id); return `<div class="pk-t">${esc(it.n)}</div><div class="pk-n">${esc(fmtV(id))} <small style="font-size:13px">${esc(unitOf(it))}</small></div><div class="pk-m">Today ${esc(fmtV(id,it.t))} · realistic ${esc(fmtV(id,it.r))} · best ${esc(fmtV(id,it.b))}</div>${b!==null?`<div class="pk-m">${pct(fracOf(id))} of the gap asked, ${pct(b)} backed</div>`:""}<div class="pk-hint">${TS.user[id]!==undefined?"Your target":"Tojo's realistic value"} · click for what feeds it</div>`; }
  if (t==="p2") return `<div class="pk-t">${{set:"Targets you set",real:"Left to Tojo",tens:"Outcomes not backed"}[id]}</div><div class="pk-hint">Click for every outcome, asked and backed</div>`;
  return ""; }
function contextFor(ref){ const [t,id] = ref.split(":");
  if (t==="it" || t==="kpi2") { const it = ITEMS[id], b = backed(id); return { kind: it.kind==="kpi"?"Outcome":it.kind==="ms"?"Measure":"Lever", point:`the target for ${it.n}`, title:it.n, lines:[`Target ${fmtV(id)} ${unitOf(it)} · today ${fmtV(id,it.t)}`].concat(b!==null?[`${pct(fracOf(id))} asked, ${pct(b)} backed`]:[]) }; }
  return { kind:"Reading", point:"the targets so far", title:"Targets", lines:[] }; }
function chatOpening(){ const c = counts(); const eb = ITEMS.EBITDA;
  const weak = (INPUTS.EBITDA||[]).map(([f,w])=>[f,w,fracOf(f)]).sort((a,b)=>(b[1]*(1-b[2]))-(a[1]*(1-a[2]))).slice(0,3).map(x=>ITEMS[x[0]].n);
  return { msg:[ `I've filled every target with Tojo's realistic value: what hospitals of your size reached in twelve months from a start like yours. You've typed in ${c.set} of your own.`,
      c.tens.length ? `${c.tens.map(k=>k.n).join(", ")} ${c.tens.length>1?"ask":"asks"} for more than the targets under ${c.tens.length>1?"them":"it"} back. EBITDA at ${fmtV("EBITDA")}% asks for ${pct(c.ebA)} of the way to best practice; the targets feeding it back ${pct(c.ebB)}. The biggest gaps are ${weak.join(", ")}.` : "Every outcome is backed by the targets that feed it.",
      "Move a pin, type a number, or ask me to fill what an outcome needs." ],
    note: c.tens.length ? `${c.tens[0].n} ${fmtV(c.tens[0].id)} needs more under it.` : "Targets and plans agree.",
    points: [ ...c.tens.slice(0,2).map(k => `${k.n}: ${pct(fracOf(k.id))} asked, ${pct(backed(k.id))} backed`), "Today's values that are reference estimates", "Automations and their go-live months" ],
    asks: [ "Fill what EBITDA needs", "Why these realistic values?", "Which targets cost the most?" ] }; }
function fillChat(){ const c = chatOpening();
  document.getElementById("chatSub").textContent = "Simulation · step 2 of 8 · targets";
  chatBody.innerHTML = `<div class="msg">${c.msg.map(m=>`<p>${esc(m)}</p>`).join("")}</div><div class="lbl">Tojo's note</div><div class="note">${esc(c.note)}</div>
  <div class="lbl">Add to a point — pick one or more</div>${c.points.map((t,i)=>`<button class="pt" type="button" aria-pressed="false"><b>P${i+1}</b> ${esc(t)}</button>`).join("")}
  <div class="lbl">Or ask next</div>${c.asks.map(t=>`<button class="ask" type="button">${esc(t)}</button>`).join("")}`;
  chatBody.querySelectorAll(".pt").forEach(b => b.onclick = () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")==="true"?"false":"true"));
  chatBody.querySelectorAll(".ask").forEach(b => b.onclick = () => { chatIn.value = b.textContent; chatIn.focus(); }); }
function replyFor(text, ctx){ const q = text.toLowerCase();
  if (q.includes("fill") && q.includes("ebitda")) { const t = backSolve("EBITDA"); return [ t.length ? `Done. I set ${t.length} targets that feed EBITDA to match the ${pct(fracOf("EBITDA"))} of the gap you asked for, and left your own targets alone.` : "Every input to EBITDA already carries your own target, so I changed nothing.", `EBITDA is now backed ${pct(backed("EBITDA"))}.` ]; }
  if (ctx && ctx.ref){ const [,id] = ctx.ref.split(":"); const it = ITEMS[id]; if (it){ const b = backed(id);
    return [`${it.n}: target ${fmtV(id)} ${unitOf(it)}, today ${fmtV(id,it.t)}. ${b!==null?`It asks for ${pct(fracOf(id))} of the gap; the targets feeding it back ${pct(b)}.`:""}`,
      (INPUTS[id]||[]).length ? `The inputs with the most room: ${(INPUTS[id]).map(([f,w])=>[f,w*(1-fracOf(f))]).sort((a,b)=>b[1]-a[1]).slice(0,3).map(x=>`${ITEMS[x[0]].n} (${fmtV(x[0])})`).join(", ")}.` : "It is a lever: it moves the measures listed on its card.",
      "Nothing is late here yet: these are targets, not progress. Once the plan is frozen I'll track each one against its owner."]; } }
  if (q.includes("realistic")) return ["Each realistic value is what hospitals of your size and type reached in twelve months from a similar starting point, taken from our reference files.", "Where your own history is long enough, the realistic value will come from your trend instead. With one month of data, it comes from reference for now."];
  if (q.includes("cost")) return ["Costs come on page 5, What's possible. There each lever gets its one-time and monthly cost, and you choose how far to fund it.", "On this page, levers that add people or equipment carry the largest costs: ICU nurses, ventilators and an own MRI."];
  const c = counts(); return [`${c.set} targets are yours and ${c.all-c.set} follow Tojo's realistic values. ${c.tens.length} outcome${c.tens.length===1?"":"s"} not yet backed.`, "Pick any target on the page and ask about it."]; }
