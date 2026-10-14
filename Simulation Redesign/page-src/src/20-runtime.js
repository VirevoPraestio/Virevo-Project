/* ===== Simulation · shared runtime: intake, readings, peek, sheet, chat ===== */
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const ALL_FILES = DOMAINS.flatMap(d => d.files);
const FILE_DOM = {}; DOMAINS.forEach(d => d.files.forEach(f => FILE_DOM[f] = d.id));
const MS = {}; DOMAINS.forEach(d => d.ms.forEach(m => { m.dom = d.id; MS[m.id] = m; }));
const DOM = {}; DOMAINS.forEach(d => DOM[d.id] = d);
const KP = {}; KPIS.forEach(k => KP[k.id] = k);
const ST = { files:{}, unknown:[], busy:false };
const SRC_WORD = { yours:"From your data", ref:"From reference until it arrives", manual:"Kept on paper", none:"Not recorded today" };
const SRC_SHORT = { yours:"Your data", ref:"Reference", manual:"On paper", none:"Not recorded" };

/* ---------- state ---------- */
function msState(m){
  if (m.src === "none") return "none";
  if (m.src === "manual") return "manual";
  return m.f.every(f => ST.files[f]) ? "yours" : "ref";
}
function domStats(d){
  const inn = d.files.filter(f => ST.files[f]).length;
  const ms = d.ms.map(msState);
  return { inn, of:d.files.length, cov: inn/d.files.length, yours: ms.filter(s=>s==="yours").length, msN: d.ms.length,
           state: inn===d.files.length ? "full" : inn===0 ? "empty" : "part", req: d.files.filter(f=>REQUIRED.includes(f) && !ST.files[f]) };
}
function stats(){
  const filesIn = ALL_FILES.filter(f => ST.files[f]).length;
  const reqIn = REQUIRED.filter(f => ST.files[f]).length;
  const all = Object.values(MS); const yours = all.filter(m => msState(m)==="yours").length;
  const mLinks = LINKS.filter(l => MS[l[0]]); const linkYours = mLinks.filter(l => msState(MS[l[0]])==="yours").length;
  const spans = Object.values(ST.files).filter(x => x.from).map(x => monthsBetween(x.from, x.to));
  const months = spans.length ? mode(spans) : 0;
  const rows = Object.values(ST.files).reduce((s,x)=>s+(x.rows||0),0);
  return { filesIn, filesOf:ALL_FILES.length, reqIn, reqOf:REQUIRED.length, yours, msOf:all.length, ref:all.length-yours,
           linkYours, linkOf:mLinks.length, months, rows, ready: reqIn===REQUIRED.length };
}
function monthsBetween(a,b){ const [y1,m1]=a.split("-").map(Number), [y2,m2]=(b||a).split("-").map(Number); return (y2-y1)*12+(m2-m1)+1; }
function mode(arr){ const c={}; arr.forEach(v=>c[v]=(c[v]||0)+1); return +Object.entries(c).sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0]; }
function weightOf(mid){ return LINKS.filter(l=>l[0]===mid).reduce((s,l)=>s+l[2],0); }
function gaps(n=3){
  return Object.values(MS).filter(m => msState(m)!=="yours").sort((a,b)=>weightOf(b.id)-weightOf(a.id)).slice(0,n);
}
function gapLine(m){
  const s = msState(m);
  if (s==="ref"){ const miss = m.f.filter(f=>!ST.files[f]).map(f=>FILE_NAME[f]); return `${miss.join(", ")} not sent yet`; }
  if (s==="manual") return "Kept on paper: a register is needed";
  return "Not recorded today: start a register";
}
function kpiShare(kid){
  const ls = LINKS.filter(l => l[1]===kid && MS[l[0]]); if (!ls.length) return null;
  const tot = ls.reduce((s,l)=>s+l[2],0), y = ls.filter(l=>msState(MS[l[0]])==="yours").reduce((s,l)=>s+l[2],0);
  return { pct: Math.round(y/tot*100), n: ls.length, yours: ls.filter(l=>msState(MS[l[0]])==="yours").length };
}
const fmtN = n => n.toLocaleString("en-IN");

/* ---------- intake ---------- */
const listeners = [];
function changed(arrivedFile){ listeners.forEach(fn => fn(arrivedFile)); }
function addFile(key, rows, from, to, own){ ST.files[key] = { rows, from, to, own:!!own }; }
function stemOf(name){ return name.toLowerCase().replace(/\.csv$/,"").replace(/\s*\(\d+\)$/,"").replace(/[^a-z0-9_]/g,"_").replace(/^_+|_+$/g,""); }
async function readFiles(list){
  for (const file of list){
    const key = stemOf(file.name);
    if (!FILE_DOM[key]) { if (!ST.unknown.includes(file.name)) ST.unknown.push(file.name); continue; }
    let text = ""; try { text = await file.text(); } catch(e) {}
    const lines = text.split(/\r?\n/).filter(l=>l.trim()); const rows = Math.max(0, lines.length-1);
    const ms = text.match(/\b(19|20)\d{2}-[01]\d(?=-[0-3]\d)/g) || [];
    const recent = ms.filter(x => x >= "2000-01").sort();
    addFile(key, rows, recent[0]||"", recent[recent.length-1]||"", true);
    changed(key);
    await new Promise(r=>setTimeout(r,60));
  }
  changed(null);
  if (ST.unknown.length) toast(`${ST.unknown.length} file${ST.unknown.length>1?"s":""} not recognised: ${ST.unknown.slice(0,3).join(", ")}${ST.unknown.length>3?"…":""}. Tojo will ask what ${ST.unknown.length>1?"they hold":"it holds"}.`);
}
function sampleFiles(keys){ keys.forEach(k => { const s = SAMPLE[k]; addFile(k, s[0], s[1], s[2]); }); }
function openingState(){ ST.files = {}; ST.unknown = []; sampleFiles(ALL_FILES.filter(f => !HELD_BACK.includes(f))); }
async function playSample(){
  if (ST.busy) return; ST.busy = true; ST.files = {}; ST.unknown = []; changed(null);
  const order = [...REQUIRED, ...ALL_FILES.filter(f=>!REQUIRED.includes(f))];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  for (const k of order){ sampleFiles([k]); changed(k); if (!reduce) await new Promise(r=>setTimeout(r,70)); }
  ST.busy = false; changed(null);
}
function clearAll(){ if (ST.busy) return; ST.files = {}; ST.unknown = []; changed(null); }
function wireIntake(root){
  const inp = root.querySelector('input[type=file]');
  if (inp) inp.addEventListener("change", e => { readFiles([...e.target.files]); e.target.value = ""; });
  root.querySelectorAll("[data-act]").forEach(b => b.addEventListener("click", () => {
    const a = b.dataset.act;
    if (a==="sample") playSample(); else if (a==="clear") clearAll(); else if (a==="go") goNext(); else if (a==="chat") openChat();
  }));
}
/* drag and drop anywhere on the stage */
addEventListener("dragover", e => { if ([...(e.dataTransfer?.types||[])].includes("Files")) { e.preventDefault(); document.body.classList.add("dropping"); } });
addEventListener("dragleave", e => { if (e.target === document.documentElement || !e.relatedTarget) document.body.classList.remove("dropping"); });
addEventListener("drop", e => { if (!e.dataTransfer?.files?.length) return; e.preventDefault(); document.body.classList.remove("dropping");
  /* page 1 reads data files; other pages handle a drop only if they say so (page 6 reads a team list) */
  const h = pageAlt("dropFiles"); if (h) return h([...e.dataTransfer.files]); if (!CUR || !CUR.page || CUR.page === "p1") readFiles([...e.dataTransfer.files]); });

function goNext(){
  const s = stats();
  if (!s.ready) { const miss = REQUIRED.filter(f=>!ST.files[f]).map(f=>FILE_NAME[f]); toast(`Still needed before the formula can run: ${miss.slice(0,4).join(", ")}${miss.length>4?` and ${miss.length-4} more`:""}.`); return; }
  toast(`The formula is built from ${s.linkYours} links in your data and ${s.linkOf-s.linkYours} from reference. `); goStep(1);
}
/* move to another step of the journey: on the joined review page it opens that page; otherwise it says so */
function goStep(step, msg){ if (PAGE.byPage) { const i = LOOKS.findIndex(l => l.step === step); if (i >= 0) { REACHED = Math.max(REACHED, step); mountLook(i); if (msg) toast(msg); return; } }
  toast((msg ? msg + " " : "") + (step >= JOURNEY.length - 1 || PAGE.product ? `The ${JOURNEY[step][0]} page comes in the next round.` : `The ${JOURNEY[step][0]} page is shown on its own review page.`)); }
let REACHED = 0;   /* the furthest step reached by its own button; the step bar can go back, and forward only this far */
let toastT;
function toast(msg){ const t = document.getElementById("toast"); t.textContent = msg; t.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(()=>t.classList.remove("on"), 5200); }

/* ---------- shared parts (each look styles them) ---------- */
function journeyHTML(cur=0){ const top = PAGE.product ? Math.max(cur, REACHED) : cur;
  return `<nav class="jr" aria-label="Simulation steps"><ol>${JOURNEY.map((j,i)=>`<li class="${i===cur?"now":i<cur?"done":""}"><button type="button" ${i===cur?'aria-current="step"':i>top?'aria-disabled="true"':''} data-step="${i}"><b>${i<cur?"✓":i+1}</b><span>${esc(j[0])}<small>${esc(j[1])}</small></span></button></li>`).join("")}</ol></nav>`;
}
function pulseHTML(){
  return `<div class="pulse" role="group" aria-label="Readings">
    <button type="button" class="pz" data-ref="pulse:files"><span class="pl">Files in</span><b data-v="files"></b><small data-v="filesSub"></small></button>
    <button type="button" class="pz" data-ref="pulse:measures"><span class="pl">Measures from your data</span><b data-v="ms"></b><small data-v="msSub"></small></button>
    <button type="button" class="pz" data-ref="pulse:links"><span class="pl">Formula links</span><b data-v="links"></b><small data-v="linksSub"></small></button>
    <button type="button" class="pz" data-ref="pulse:months"><span class="pl">History</span><b data-v="months"></b><small data-v="monthsSub"></small></button>
  </div>`;
}
function intakeHTML(){
  return `<div class="intake">
    <label class="drop" for="fileIn"><input id="fileIn" type="file" multiple accept=".csv,text/csv"><span class="dz-big">Drop your files here</span><span class="dz-sub">or choose them: CSV exports from your HIS, ERP, roster and registers</span></label>
    <p class="intake-note" data-v="intakeNote"></p>
  </div>`;
}
function watchHTML(){ return `<ul class="watch" data-v="watch" aria-label="Biggest gaps"></ul>`; }
function ctaHTML(){ return `<div class="cta"><button type="button" class="go" data-act="go">Build the formula <span aria-hidden="true">→</span></button><span class="cta-note" data-v="ctaNote"></span></div>`; }

function fillCommon(root){ { const _a = pageAlt("fillCommon"); if (_a) return _a(...arguments); }
  const s = stats();
  const set = (k,v) => root.querySelectorAll(`[data-v="${k}"]`).forEach(e => e.innerHTML = v);
  set("files", `${s.filesIn}<i>/${s.filesOf}</i>`); set("filesSub", `${s.reqIn} of ${s.reqOf} the formula needs`);
  set("ms", `${s.yours}<i>/${s.msOf}</i>`); set("msSub", `${s.ref} come from reference`);
  set("links", `${s.linkYours}<i>/${s.linkOf}</i>`); set("linksSub", "set by your own data");
  set("months", s.months ? `${s.months}<i> month${s.months>1?"s":""}</i>` : "—"); set("monthsSub", s.months ? (s.months<12 ? "12 needed to learn from you" : "enough to learn from") : "no dated files yet");
  set("intakeNote", ST.busy ? "Reading files…" : s.filesIn ? `${fmtN(s.rows)} rows read from ${s.filesIn} files.${ST.unknown.length?` ${ST.unknown.length} not recognised.`:""}` : "Nothing in yet. Drop the exports from your systems and registers; the formula below already runs on reference weights until they arrive.");
  set("ctaNote", s.ready ? `Ready. ${s.ref} measures will use reference weights until their data arrives.` : `${s.reqOf-s.reqIn} of the files the formula needs are still missing.`);
  root.querySelectorAll('[data-act="go"]').forEach(b => b.classList.toggle("ready", s.ready));
  const w = root.querySelector('[data-v="watch"]');
  if (w) w.innerHTML = gaps(3).map(m => `<li><button type="button" data-ref="ms:${m.id}" class="wi wi-${msState(m)}"><i aria-hidden="true">${msState(m)==="ref"?"⧗":msState(m)==="manual"?"✎":"?"}</i><span><b>${esc(m.n)}</b><small>${esc(gapLine(m))} · ${esc(DOM[m.dom].short)}</small></span></button></li>`).join("");
}

/* ---------- detail texts ---------- */
function fileRow(f){ const x = ST.files[f]; return `<li><span class="ck ${x?"y":""}">${x?"✓":""}</span><span>${esc(FILE_NAME[f])}<br><small style="color:var(--sh-mute)">${f}.csv${REQUIRED.includes(f)?" · needed to run":""}</small></span><em>${x?`${fmtN(x.rows)} rows${x.from?` · ${x.from}${x.to&&x.to!==x.from?` to ${x.to}`:""}`:""}`:"not sent"}</em></li>`; }
function msChip(m){ const s = msState(m); return `<li><span class="src src-${s}">${SRC_SHORT[s]}</span><span><b>${esc(m.n)}</b>${m.note?`<br><small style="color:var(--sh-mute)">${esc(m.note)}</small>`:""}</span></li>`; }
function domDetail(d){
  const s = domStats(d);
  return `<div class="d-eyebrow">Data family · ${d.files.length} files · ${d.ms.length} measures</div><div class="d-title">${esc(d.name)}</div>
  <p class="d-sub"><span class="d-pill ${s.state==="full"?"ahead":s.state==="part"?"watch":"off"}">${s.state==="full"?"All files in":s.state==="part"?`${s.inn} of ${s.of} files in`:"Nothing in yet"}</span>${s.req.length?` &nbsp;Needed to run: ${s.req.map(f=>esc(FILE_NAME[f])).join(", ")}`:""}</p>
  <div class="d-four"><div><span>Files in</span><b>${s.inn}/${s.of}</b></div><div><span>Rows read</span><b>${fmtN(d.files.reduce((a,f)=>a+(ST.files[f]?.rows||0),0))}</b></div><div class="now"><span>Measures from your data</span><b>${s.yours}/${s.msN}</b></div><div><span>From reference</span><b>${s.msN-s.yours}</b></div></div>
  <div class="d-sec"><h4>Measures the formula takes from here</h4><ul class="d-ms">${d.ms.map(msChip).join("")}</ul></div>
  <div class="d-sec"><h4>Files</h4><ul class="d-list">${d.files.map(fileRow).join("")}</ul></div>
  <div class="d-sec"><h4>For your IT team</h4><div class="d-impact">${esc(d.it)} Twelve months, one CSV per table.</div></div>`;
}
function msDetail(m){
  const s = msState(m), d = DOM[m.dom]; const ks = LINKS.filter(l=>l[0]===m.id);
  const how = s==="yours" ? "The formula reads this from your files and sets its links from your own numbers."
    : s==="ref" ? "Until the file arrives, the formula uses the reference value and the reference weights for a hospital of your size."
    : s==="manual" ? "This is written on paper today. The formula uses reference weights now; a simple register kept for two weeks lets your numbers replace them."
    : "Nobody records this today. The formula uses reference weights; Tojo will set up a short register so your numbers can replace them.";
  return `<div class="d-eyebrow">Measure · ${esc(d.name)}</div><div class="d-title">${esc(m.n)}</div>
  <p class="d-sub"><span class="d-pill ${s==="yours"?"ahead":s==="ref"?"watch":"off"}">${SRC_WORD[s]}</span></p>
  <div class="d-sec"><h4>How the formula gets it</h4><p style="margin:0">${how}</p>${m.note?`<p style="margin:8px 0 0;color:var(--sh-mute)">${esc(m.note)}</p>`:""}</div>
  <div class="d-sec"><h4>What it moves</h4><div class="d-fac">${ks.map(l=>`<span>${esc(KP[l[1]]?.n||l[1])}</span><span class="bar" aria-label="weight ${l[2]}"><i style="width:${l[2]*100}%;background:var(--sh-state)"></i></span>`).join("")}</div></div>
  ${m.f.length?`<div class="d-sec"><h4>Comes from</h4><ul class="d-list">${m.f.map(fileRow).join("")}</ul></div>`:""}`;
}
function kpiDetail(k){
  const ls = LINKS.filter(l=>l[1]===k.id); const sh = kpiShare(k.id);
  return `<div class="d-eyebrow">KPI the formula drives</div><div class="d-title">${esc(k.n)}</div>
  <p class="d-sub">${sh?`<span class="d-pill ${sh.pct>=70?"ahead":sh.pct>=40?"watch":"off"}">${sh.pct}% of its pull set by your data</span>`:""}</p>
  <div class="d-sec"><h4>What feeds it</h4><ul class="d-ms">${ls.map(l=>{ const m = MS[l[0]]; if (!m) return `<li><span class="src src-yours">KPI</span><span><b>${esc(KP[l[0]].n)}</b> · weight ${l[2]}</span></li>`; return `<li><span class="src src-${msState(m)}">${SRC_SHORT[msState(m)]}</span><span><b>${esc(m.n)}</b> · weight ${l[2]}</span></li>`; }).join("")}</ul></div>`;
}
function fileDetail(f){ const d = DOM[FILE_DOM[f]]; return domDetail(d); }
function pulseDetail(id){
  const s = stats();
  const T = {
    files:["Files in", `${s.filesIn} of ${s.filesOf}`, `The formula needs ${s.reqOf} of them to run; ${s.reqIn} are in. The rest sharpen it.`],
    measures:["Measures from your data", `${s.yours} of ${s.msOf}`, `${s.ref} measures come from the reference files for now: some because a file has not been sent, some because they are kept on paper, and some because nobody records them.`],
    links:["Formula links", `${s.linkYours} of ${s.linkOf}`, `Each link says how much one measure moves a KPI. ${s.linkYours} are set from your data; the rest use reference weights, marked as such everywhere they appear.`],
    months:["History", s.months?`${s.months} month${s.months>1?"s":""}`:"—", "One month shows where you stand. Twelve months show how your measures move together, so the formula can learn its links from you instead of from reference."]
  }[id];
  return `<div class="d-eyebrow">Reading</div><div class="d-title">${T[0]}: ${T[1]}</div><p style="margin:0">${T[2]}</p>
  <div class="d-sec"><h4>Data families</h4><ul class="d-list">${DOMAINS.map(d=>{ const x = domStats(d); return `<li><span class="ck ${x.state==="full"?"y":x.state==="empty"?"late":""}">${x.state==="full"?"✓":x.state==="empty"?"!":"·"}</span><span>${esc(d.name)}</span><em>${x.inn}/${x.of} files · ${x.yours}/${x.msN} measures</em></li>`; }).join("")}</ul></div>`;
}
function detailFor(ref){ { const _a = pageAlt("detailFor"); if (_a) return _a(...arguments); }
  const [t,id] = ref.split(":");
  if (t==="dom") { const s = domStats(DOM[id]); return [domDetail(DOM[id]), s.state==="full"?"ahead":s.state==="part"?"watch":"off"]; }
  if (t==="file") { const s = domStats(DOM[FILE_DOM[id]]); return [fileDetail(id), s.state==="full"?"ahead":"watch"]; }
  if (t==="ms") { const s = msState(MS[id]); return [msDetail(MS[id]), s==="yours"?"ahead":s==="ref"?"watch":"off"]; }
  if (t==="kpi") return [kpiDetail(KP[id]), "ahead"];
  if (t==="pulse") return [pulseDetail(id), "ahead"];
  return ["",""];
}
function peekFor(ref){ { const _a = pageAlt("peekFor"); if (_a) return _a(...arguments); }
  const [t,id] = ref.split(":");
  if (t==="dom"){ const d = DOM[id], s = domStats(d); return `<div class="pk-t">${esc(d.name)}</div><div class="pk-n">${s.inn}/${s.of} files</div><div class="pk-m">${s.yours} of ${s.msN} measures from your data${s.req.length?` · needed to run: ${s.req.map(f=>FILE_NAME[f]).join(", ")}`:""}</div><div class="pk-hint">Click for files, measures and what to ask IT for</div>`; }
  if (t==="file"){ const x = ST.files[id]; return `<div class="pk-t">${esc(FILE_NAME[id])}</div><div class="pk-m">${id}.csv · ${esc(DOM[FILE_DOM[id]].name)}</div><div class="pk-n">${x?`${fmtN(x.rows)} rows`:"Not sent"}</div>${x&&x.from?`<div class="pk-m">${x.from}${x.to!==x.from?` to ${x.to}`:""}</div>`:""}<div class="pk-hint">${REQUIRED.includes(id)?"Needed to run the formula":"Sharpens the formula"}</div>`; }
  if (t==="ms"){ const m = MS[id], s = msState(m); return `<div class="pk-t">${esc(m.n)}</div><div class="pk-m"><b>${SRC_WORD[s]}</b></div><div class="pk-m">${esc(s==="yours"?`Read from ${m.f.map(f=>FILE_NAME[f]).join(" and ")}`:gapLine(m))}</div><div class="pk-hint">Moves ${LINKS.filter(l=>l[0]===id).map(l=>KP[l[1]]?.n).join(", ")}</div>`; }
  if (t==="kpi"){ const k = KP[id], sh = kpiShare(id); return `<div class="pk-t">${esc(k.n)}</div>${sh?`<div class="pk-n">${sh.pct}%</div><div class="pk-m">of its pull set by your data · ${sh.yours} of ${sh.n} inputs</div>`:""}<div class="pk-hint">Click to see what feeds it</div>`; }
  if (t==="pulse"){ return `<div class="pk-t">${{files:"Files in",measures:"Measures from your data",links:"Formula links",months:"History"}[id]}</div><div class="pk-hint">Click for the full count by data family</div>`; }
  return "";
}
function contextFor(ref){ { const _a = pageAlt("contextFor"); if (_a) return _a(...arguments); }
  const [t,id] = ref.split(":");
  if (t==="dom"){ const d = DOM[id], s = domStats(d); return { kind:"Data family", point:`the ${d.name} data`, title:d.name, lines:[`${s.inn} of ${s.of} files in · ${s.yours} of ${s.msN} measures from our data`] }; }
  if (t==="file"){ const x = ST.files[id]; return { kind:"File", point:`the ${FILE_NAME[id]} file`, title:FILE_NAME[id], lines:[x?`${fmtN(x.rows)} rows`:"Not sent yet"] }; }
  if (t==="ms"){ const m = MS[id]; return { kind:"Measure", point:`the measure "${m.n}"`, title:m.n, lines:[SRC_WORD[msState(m)]] }; }
  if (t==="kpi"){ const k = KP[id], sh = kpiShare(id); return { kind:"KPI", point:`what feeds ${k.n}`, title:k.n, lines:sh?[`${sh.pct}% of its pull set by our data`]:[] }; }
  if (t==="pulse"){ return { kind:"Reading", point:`the ${id} reading`, title:{files:"Files in",measures:"Measures from your data",links:"Formula links",months:"History"}[id], lines:[] }; }
  return { kind:"Item", point:"this", title:"This item", lines:[] };
}

/* ---------- peek ---------- */
const peek = document.getElementById("peek"); let peekT, hideT;
function showPeek(el){ const ref = el.dataset.ref; const h = ref && peekFor(ref); if (!h) return; clearTimeout(hideT);
  peek.innerHTML = `<div class="pk-bar"><button type="button" class="pk-ask" data-ask="${ref}"><i>T</i>Ask Tojo about this</button><button type="button" class="pk-x" aria-label="Close">×</button></div>${h}`;
  peek.classList.add("on");
  const r = el.getBoundingClientRect(); const pw = peek.offsetWidth, ph = peek.offsetHeight;
  let x = r.left + r.width/2 - pw/2; x = Math.max(8, Math.min(innerWidth - pw - 8 - (document.body.classList.contains("chat-open") && innerWidth > 900 ? 400 : 0), x));
  let y = r.top - ph - 8; if (y < 8) y = r.bottom + 8; peek.style.left = x+"px"; peek.style.top = y+"px"; }
function hidePeek(){ clearTimeout(hideT); peek.classList.remove("on"); }
function laterHide(ms=260){ clearTimeout(hideT); hideT = setTimeout(()=>{ if (!peek.matches(":hover") && !peek.contains(document.activeElement)) hidePeek(); }, ms); }
document.addEventListener("pointerover", e => { if (e.pointerType==="touch") return; if (peek.contains(e.target)) { clearTimeout(hideT); return; } const el = e.target.closest("#stage [data-ref]"); if (!el) return; clearTimeout(peekT); peekT = setTimeout(()=>showPeek(el), 120); });
document.addEventListener("pointerout", e => { if (e.target.closest("#stage [data-ref]") || peek.contains(e.target)) { clearTimeout(peekT); laterHide(); } });
let pressT; document.addEventListener("touchstart", e => { if (peek.contains(e.target)) return; const el = e.target.closest("#stage [data-ref]"); if (!el) return; pressT = setTimeout(()=>showPeek(el), 380); }, {passive:true});
document.addEventListener("touchend", () => clearTimeout(pressT));
addEventListener("scroll", () => { if (!peek.contains(document.activeElement)) hidePeek(); }, {passive:true});
peek.addEventListener("click", e => { e.stopPropagation(); if (e.target.closest(".pk-x")) return hidePeek(); const a = e.target.closest("[data-ask]"); if (a) { askTojo(a.dataset.ask); hidePeek(); } });
document.addEventListener("click", e => { const el = e.target.closest("#stage [data-ref]"); if (el && !el.closest("[data-noopen]")) openSheet(el.dataset.ref); });

/* ---------- sheet ---------- */
const sheet = document.getElementById("sheet"), scrim = document.getElementById("scrim"), sheetBody = document.getElementById("sheetBody");
function openSheet(ref){ const [h,st] = detailFor(ref); if (!h) return; hidePeek(); sheet.dataset.ref = ref;
  sheet.style.setProperty("--sh-state", st==="off"?"var(--c-bad)":st==="watch"?"var(--c-warn)":"var(--c-ok)");
  sheetBody.innerHTML = h; sheet.classList.add("on"); scrim.classList.add("on"); sheet.scrollTop = 0; sheet.querySelector(".sh-ask").focus(); }
function closeSheet(){ sheet.classList.remove("on"); scrim.classList.remove("on"); }
sheet.querySelector(".x").onclick = closeSheet; scrim.onclick = closeSheet;
sheet.querySelector(".sh-ask").onclick = () => askTojo(sheet.dataset.ref);
addEventListener("keydown", e => { if (e.key==="Escape") { if (sheet.classList.contains("on")) closeSheet(); else if (peek.classList.contains("on")) hidePeek(); else closeChat(); } });

/* ---------- chat (the tools' chat look) ---------- */
const chatIn = document.getElementById("chatIn"), chatBody = document.getElementById("chatBody"), ctxBox = document.getElementById("chatCtx");
let chatCtx = null;
function chatOpening(){ { const _a = pageAlt("chatOpening"); if (_a) return _a(...arguments); }
  const s = stats(); const g = gaps(4);
  return {
    msg:[ s.filesIn ? `${s.filesIn} of the ${s.filesOf} files are in. They give ${s.yours} of the ${s.msOf} measures the formula needs; the other ${s.ref} come from our reference files until your data arrives, and each one is marked so you can see it.` : "Nothing is in yet. The formula already runs on reference weights for a hospital of your size; every file you drop replaces some of them with your own numbers.",
          s.months && s.months < 12 ? `One thing matters more than the missing files: the files cover ${s.months} month${s.months>1?"s":""}. That shows where you stand today, but not how your measures move together, so most links in the formula still lean on reference weights.` : "Twelve months of history lets your own data set the links in the formula.",
          "Pick a point to add to it, or choose what to do next." ],
    note: s.months && s.months < 12 ? "Ask IT for twelve months, not one." : "Send what you have. I'll fill the rest.",
    points: [ s.months && s.months<12 ? `Only ${s.months} month${s.months>1?"s":""} of history` : "History is long enough", ...g.slice(0,3).map(m => `${m.n}: ${SRC_SHORT[msState(m)].toLowerCase()}`) ],
    asks: ["Which files should IT send first?", "What does the formula do with a missing measure?", "Write the request for our IT team"]
  };
}
function fillChat(){ { const _a = pageAlt("fillChat"); if (_a) return _a(...arguments); } const c = chatOpening();
  document.getElementById("chatSub").textContent = "Simulation · step 1 of 7 · your data";
  chatBody.innerHTML = `<div class="msg">${c.msg.map(m=>`<p>${esc(m)}</p>`).join("")}</div><div class="lbl">Tojo's note</div><div class="note">${esc(c.note)}</div>
  <div class="lbl">Add to a point — pick one or more</div>${c.points.map((t,i)=>`<button class="pt" type="button" aria-pressed="false"><b>P${i+1}</b> ${esc(t)}</button>`).join("")}
  <div class="lbl">Or ask next</div>${c.asks.map(t=>`<button class="ask" type="button">${esc(t)}</button>`).join("")}`;
  chatBody.querySelectorAll(".pt").forEach(b => b.onclick = () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")==="true"?"false":"true"));
  chatBody.querySelectorAll(".ask").forEach(b => b.onclick = () => { chatIn.value = b.textContent; chatIn.focus(); });
}
function openChat(){ document.body.classList.add("chat-open"); setTimeout(()=>chatIn.focus(), 300); }
function closeChat(){ document.body.classList.remove("chat-open"); }
document.getElementById("chatFab").onclick = openChat;
document.getElementById("chatClose").onclick = closeChat;
function askTojo(ref){
  const c = contextFor(ref); chatCtx = { ref, ...c };
  ctxBox.innerHTML = `<div><span>${esc(c.kind)}</span><b>${esc(c.title)}</b>${c.lines.map(l=>`<small>${esc(l)}</small>`).join("")}</div><button type="button" aria-label="Remove the attached item">×</button>`;
  ctxBox.hidden = false; ctxBox.querySelector("button").onclick = () => { chatCtx = null; ctxBox.hidden = true; };
  chatIn.value = `Tell me more about ${c.point}: where this stands, whether there is any delay or overrun on it, who or what is responsible for it, whether we have any way to recover, and how we are planning to recover.`;
  closeSheet(); hidePeek(); openChat();
}
function replyFor(text, ctx){ { const _a = pageAlt("replyFor"); if (_a) return _a(...arguments); }
  const s = stats(); const q = text.toLowerCase();
  if (ctx){ const [t,id] = ctx.ref.split(":");
    if (t==="ms"){ const m = MS[id], st = msState(m);
      if (st==="yours") return [`${m.n} comes from your own files, so its links are set from your numbers. Nothing is late on it.`, `It moves ${LINKS.filter(l=>l[0]===id).map(l=>KP[l[1]]?.n).join(" and ")}.`];
      if (st==="ref") return [`${m.n} is waiting on ${m.f.filter(f=>!ST.files[f]).map(f=>FILE_NAME[f]).join(" and ")}. Until it arrives the formula uses the reference value for a hospital of your size.`, `The IT team owns this. ${DOM[m.dom].it}`, "Once the file is in, the reference value is replaced on the next run. Nothing else has to change."];
      return [`${m.n} is ${st==="manual"?"kept on paper":"not recorded anywhere"} today, so the formula uses reference weights for it.`, m.note||"", "To recover: a short register kept for two weeks by the person on duty is enough. I can draft the register and name who should keep it once your team is in place (step 7)."]; }
    if (t==="dom"){ const d = DOM[id], x = domStats(d); return [`${d.name}: ${x.inn} of ${x.of} files in, ${x.yours} of ${x.msN} measures from your data.`, x.inn<x.of?`Missing: ${d.files.filter(f=>!ST.files[f]).map(f=>FILE_NAME[f]).join(", ")}. ${d.it}`:"Everything in this family is in.", "The IT team owns the exports; I'll mark each measure as yours as soon as its file lands."]; }
  }
  if (q.includes("first")) { const miss = REQUIRED.filter(f=>!ST.files[f]); return [ miss.length ? `First the ${miss.length} files the formula cannot run without: ${miss.map(f=>FILE_NAME[f]).join(", ")}.` : "Every file the formula needs is in.", `Then the ones with the most pull on your KPIs: ${gaps(3).filter(m=>msState(m)==="ref").map(m=>m.f.filter(f=>!ST.files[f]).map(f=>FILE_NAME[f])).flat().filter((v,i,a)=>a.indexOf(v)===i).join(", ")||"none left"}.`, "And twelve months of each, so the formula learns from your history." ]; }
  if (q.includes("missing")) return ["A missing measure never stops the formula. It takes the reference value and the reference weights for a hospital of your size and type, and marks the link as reference.", "When your data arrives, the link is re-learned from it and the mark changes to your data."];
  if (q.includes("request") || q.includes("it team")) return ["Here is the request for your IT team:", `Please export twelve months of the following, one CSV per table: ${DOMAINS.map(d=>d.name).join("; ")}. For each, the rows and columns listed on its card. Dates as YYYY-MM-DD, one row per event.`, "I can turn this into a full data guide with column names once you approve this page."];
  return [`Noted. ${s.filesIn} files are in and ${s.yours} of ${s.msOf} measures come from your data.`, "Pick a data family or a measure on the page and ask about it; I'll answer for that item."];
}
function sendChat(){
  const text = chatIn.value.trim(); if (!text) return;
  const ctx = chatCtx;
  chatBody.insertAdjacentHTML("beforeend", `<div class="you">${ctx?`<div class="att"><span>${esc(ctx.kind)}</span>${esc(ctx.title)}</div>`:""}<p>${esc(text)}</p></div><div class="typing" aria-label="Tojo is writing"><i></i><i></i><i></i></div>`);
  chatIn.value = ""; chatCtx = null; ctxBox.hidden = true; chatBody.scrollTop = chatBody.scrollHeight;
  setTimeout(() => { chatBody.querySelector(".typing")?.remove();
    chatBody.insertAdjacentHTML("beforeend", `<div class="msg">${replyFor(text, ctx).filter(Boolean).map(p=>`<p>${esc(p)}</p>`).join("")}</div>`);
    chatBody.scrollTop = chatBody.scrollHeight; }, 700);
}
document.querySelector("#chat .send").onclick = sendChat;
chatIn.addEventListener("keydown", e => { if (e.key==="Enter" && !e.shiftKey) { e.preventDefault(); sendChat(); } });
const LOOKS = [];
function pageAlt(name){ let m = "p1"; try { m = (CUR && CUR.page) || "p1"; } catch(e) {} return m === "p1" ? null : (globalThis[m + "_" + name] || null); }
