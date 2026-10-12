/* ===== shared: details, peek, sheet, tabs, chat ===== */
const SCHEMES = [];
const UI = { view:"week", scheme:0 };
const TABS = [
  ["overview","Overview"],["links","Integrations"],["measures","KPIs"],["team","Taskboards"],["health","Project Status"],["files","Resources"],["chat","Chat"]
];
const UNIVERSAL = [
  ["Pulse strip","Four readings that never leave the top of the suite: parts live, KPIs on course, money out against money back, and the break-even month."],
  ["Plan ghost","Every number carries a faint mark of where the plan said it would be today, so ahead or behind shows without a click."],
  ["Watch list","The three items furthest off course right now, each with its owner. It re-ranks itself every night."],
  ["Hover peek","Rest the pointer on any part, KPI, person or month (or press and hold on a phone) and its facts appear. A click opens the full story. Every peek and popup carries Ask Tojo about this, which opens the chat with the item and a question already written."],
  ["Next go-live countdown","The next part due to switch on, and the days left."],
  ["Freshness marks","Each link and figure says how old its data is: a minute, today, or no feed yet."]
];

function personChip(key){ const p = P[key]; return p ? `<span class="d-av" title="${esc(p.name)}">${esc(p.name)}</span>` : ""; }

function kpiDetail(k){
  const scale = v => (prog(k,v)/1.0)*100;
  let h = `<div class="d-eyebrow">KPI · ${k.id}</div><div class="d-title">${esc(k.name)}</div>
  <p class="d-sub"><span class="d-pill ${k.state}">${STATE_WORD[k.state]}</span> &nbsp;${gapText(k)} · week ${D.week} of ${D.weeksPlanned}</p>
  <div class="d-four"><div><span>At the start</span><b>${fmtv(k,k.base)}</b></div><div><span>Plan for this week</span><b>${fmtv(k,k.plan)}</b></div><div class="now"><span>Now</span><b>${fmtv(k,k.now)}</b></div><div><span>Target</span><b>${fmtv(k,k.target)}</b></div></div>
  <div class="d-glide" aria-label="From the start to the target: now at ${Math.round(prog(k,k.now)*100)}% of the way, plan says ${Math.round(prog(k,k.plan)*100)}%">
    <div class="rail"></div><div class="fill" style="width:${Math.min(100,scale(k.now))}%"></div>
    <div class="mk" style="left:0"><i>Start</i></div><div class="mk plan" style="left:${scale(k.plan)}%"><i>Plan</i></div><div class="mk" style="left:100%"><i>Target</i></div>
  </div>`;
  if (k.state === "ahead") h += `<div class="d-sec"><h4>What is driving it</h4><p style="margin:0">${esc(k.why)}</p></div>`;
  else {
    h += `<div class="d-sec"><h4>Where the gap comes from</h4><div class="d-fac">${k.factors.map(f=>`<span>${esc(f[0])}</span><span class="bar" aria-label="${f[1]}% of the gap"><i style="width:${f[1]}%"></i></span>`).join("")}</div></div>
    <div class="d-sec"><h4>Already planned to recover</h4><ul class="d-fix">${k.fixes.map(f=>`<li><span class="av">${initials(P[f[1]].name)}</span><span>${esc(f[0])}<br><small style="color:var(--sh-mute)">${esc(P[f[1]].name)}</small></span><time>${esc(f[2])}</time></li>`).join("")}</ul></div>
    <div class="d-back">${esc(k.back)}</div>`;
  }
  return h;
}
function personDetail(p){
  const today = p.today.map(t=>{ const done = t[1]===1; const late = typeof t[1]==="string" && t[1].startsWith("late");
    return `<li><span class="ck ${done?"y":late?"late":""}">${done?"✓":late?"!":""}</span><span>${esc(t[0])}</span><em class="${late?"late":""}">${done?"done":esc(t[1])}</em></li>`; }).join("");
  return `<div class="d-eyebrow">${esc(p.role)}</div><div class="d-title">${esc(p.name)}</div>
  <p class="d-sub"><span class="d-pill ${p.state}">${PERSON_WORD[p.state]}</span> &nbsp;${esc(p.from)}</p>
  <div class="d-four"><div><span>Due this week</span><b>${p.due}</b></div><div><span>Done</span><b>${p.done}</b></div><div><span>Late</span><b style="color:${p.late?"var(--c-bad)":"inherit"}">${p.late}</b></div><div><span>Done on time</span><b>${Math.round((p.done)/p.due*100)}%</b></div></div>
  ${p.impact?`<div class="d-sec"><h4>What the delay costs</h4><div class="d-impact">${esc(p.impact)}</div></div>`:""}
  <div class="d-sec"><h4>Today</h4><ul class="d-list">${today}</ul></div>
  <div class="d-sec"><h4>Critical tasks coming up</h4><ul class="d-fix">${p.next.map(n=>`<li><span class="av">→</span><span>${esc(n[0])}</span><time>${esc(n[1])}</time></li>`).join("")}</ul></div>`;
}
function partDetail(x){
  return `<div class="d-eyebrow">Part ${x.id} of ${D.parts.length} · Integration</div><div class="d-title">${esc(x.name)}</div>
  <p class="d-sub"><span class="d-pill ${x.st==="live"?"ahead":x.st==="blocked"?"off":"watch"}">${PART_WORD[x.st]}</span> &nbsp;${esc(x.when)}</p>
  <div class="d-grid"><div><span>Reads from</span><b>${esc(x.src)}</b></div><div><span>Data freshness</span><b>${esc(x.fresh)}</b></div><div><span>Owner</span><b>${esc(P[x.owner].name)}</b></div><div><span>Volume</span><b>${esc(x.vol)}</b></div></div>
  <div class="d-sec"><h4>What it does</h4><p style="margin:0">${esc(x.note)}</p></div>`;
}
function healthDetail(){
  const rows = D.spend.map(s=>`<tr><td>${esc(s.cat)}${s.note?`<br><small style="color:var(--sh-mute)">${esc(s.note)}</small>`:""}</td>${s.v.map(v=>`<td>${v.toFixed(2)}</td>`).join("")}<td>${sum(s.v).toFixed(2)}</td></tr>`).join("");
  const mt = D.months.map((m,i)=>sum(D.spend.map(s=>s.v[i])));
  return `<div class="d-eyebrow">Project Status · suite health</div><div class="d-title">Break-even in ${D.breakeven.fore}, ${D.breakeven.late} after plan</div>
  <p class="d-sub"><span class="d-pill watch">Off track by ${D.breakeven.late}</span> &nbsp;Plan said ${D.breakeven.plan}.</p>
  <div class="d-four"><div><span>Spent so far</span><b>${L(spendTotal)}</b></div><div><span>Extra revenue so far</span><b>${L(revTotal)}</b></div><div class="now"><span>EBITDA added so far</span><b>${L(ebitdaTotal)}</b></div><div><span>Monthly at full run</span><b>${L(D.runRate.ebitda)}</b></div></div>
  <div class="d-sec"><h4>Monthly outlay (₹ lakh)</h4><div class="d-wrap"><table class="d-money"><thead><tr><th>What</th>${D.months.map(m=>`<th>${m}</th>`).join("")}<th>Total</th></tr></thead><tbody>${rows}</tbody>
  <tfoot><tr><td>Total spent</td>${mt.map(v=>`<td>${v.toFixed(2)}</td>`).join("")}<td>${spendTotal.toFixed(2)}</td></tr><tr><td>Extra revenue from freed bed-days</td>${D.revenue.map(v=>`<td>${v.toFixed(1)}</td>`).join("")}<td>${revTotal.toFixed(1)}</td></tr><tr><td>EBITDA added</td>${D.ebitda.map(v=>`<td>${v.toFixed(1)}</td>`).join("")}<td>${ebitdaTotal.toFixed(1)}</td></tr></tfoot></table></div></div>
  <div class="d-sec"><h4>Where the delay comes from</h4><div class="d-fac">${D.healthFactors.map(f=>`<span>${esc(f[0])}</span><span class="bar"><i style="width:${f[1]}%"></i></span>`).join("")}</div></div>
  <div class="d-sec"><h4>Already planned to recover</h4><ul class="d-fix">${D.healthFixes.map(f=>`<li><span class="av">${initials(P[f[1]].name)}</span><span>${esc(f[0])}<br><small style="color:var(--sh-mute)">${esc(P[f[1]].name)}</small></span><time>${esc(f[2])}</time></li>`).join("")}</ul></div>
  <div class="d-back">${esc(D.recoverLine)}</div>`;
}
function monthDetail(i){
  const t = sum(D.spend.map(s=>s.v[i]));
  return `<div class="d-eyebrow">Project Status · ${D.months[i]} 2026</div><div class="d-title">${L(t)} spent, ${L(D.ebitda[i])} EBITDA added</div>
  <div class="d-grid">${D.spend.map(s=>`<div><span>${esc(s.cat)}</span><b>${L(s.v[i])}</b></div>`).join("")}<div><span>Extra revenue</span><b>${L(D.revenue[i])}</b></div></div>`;
}
function resourcesDetail(){
  return `<div class="d-eyebrow">Resources</div><div class="d-title">Everything filed for this suite</div>
  <ul class="d-fix">${D.resources.map(r=>`<li><span class="av">▤</span><span>${esc(r[0])}</span><time>${esc(r[1])}</time></li>`).join("")}</ul>`;
}
function universalDetail(){
  return `<div class="d-eyebrow">Proposed for every suite</div><div class="d-title">Six universal elements</div>
  <p class="d-sub">Each one gives a fact without a click or a typed question. Every scheme draws all six in its own look, plus the floating chat button.</p>
  <div class="d-uni">${UNIVERSAL.map((u,i)=>`<div><b>${i+1}. ${u[0]}</b><p>${u[1]}</p></div>`).join("")}</div>`;
}
function detailFor(ref){
  const [t,id] = ref.split(":");
  if (t==="kpi") return [kpiDetail(KP[id]), KP[id].state];
  if (t==="per") return [personDetail(P[id]), P[id].state];
  if (t==="part") { const x = D.parts.find(p=>p.id==id); return [partDetail(x), x.st==="live"?"ahead":x.st==="blocked"?"off":"watch"]; }
  if (t==="health") return [healthDetail(),"watch"];
  if (t==="month") return [monthDetail(+id),"ahead"];
  if (t==="files") return [resourcesDetail(),"ahead"];
  if (t==="uni") return [universalDetail(),"ahead"];
  return ["",""];
}
function peekFor(ref){
  const [t,id] = ref.split(":");
  if (t==="kpi"){ const k = KP[id]; return `<div class="pk-t">${esc(k.name)}</div><div class="pk-n">${fmtv(k,k.now)}</div><div class="pk-m">Start ${fmtv(k,k.base)} · plan ${fmtv(k,k.plan)} · target ${fmtv(k,k.target)}</div><div class="pk-m"><b>${STATE_WORD[k.state]}</b>: ${gapText(k)}</div><div class="pk-hint">Click to see why and the recovery plan</div>`; }
  if (t==="per"){ const p = P[id]; return `<div class="pk-t">${esc(p.name)} · ${esc(p.role)}</div><div class="pk-m">${p.done} of ${p.due} done this week${p.late?`, ${p.late} late`:""}</div>${p.impact?`<div class="pk-m" style="margin-top:4px">${esc(p.impact)}</div>`:""}<div class="pk-m" style="margin-top:4px">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</div><div class="pk-hint">Click for today's tasks and what is coming up</div>`; }
  if (t==="part"){ const x = D.parts.find(p=>p.id==id); return `<div class="pk-t">${x.id}. ${esc(x.name)}</div><div class="pk-m"><b>${PART_WORD[x.st]}</b> · ${esc(x.when)}</div><div class="pk-m">From ${esc(x.src)} · ${esc(x.fresh)}</div><div class="pk-hint">Owner: ${esc(P[x.owner].name)}</div>`; }
  if (t==="health") return `<div class="pk-t">Break-even</div><div class="pk-n">${D.breakeven.fore}</div><div class="pk-m">Plan ${D.breakeven.plan} · ${D.breakeven.late} late · spent ${L(spendTotal)}, EBITDA added ${L(ebitdaTotal)}</div><div class="pk-hint">Click for causes and recovery</div>`;
  if (t==="month"){ const i=+id, s=sum(D.spend.map(x=>x.v[i])); return `<div class="pk-t">${D.cumMonths[i]}</div><div class="pk-m">Spent ${L(D.cumSpend[i])} to date · EBITDA back ${L(D.cumFore[i])}${i>D.actualTo?" (forecast)":""}</div>`; }
  if (t==="files") return `<div class="pk-t">Resources</div><div class="pk-m">${D.resources.length} items · latest: weekly review, 9 Oct</div>`;
  return "";
}

/* peek: stays open while the pointer is on it, so its buttons can be used */
const peek = document.getElementById("peek"); let peekT, hideT, peekRef = null;
function showPeek(el){ suiteOf(el); const ref = el.dataset.ref; const h = ref && peekFor(ref); if (!h) return; clearTimeout(hideT); peekRef = ref;
  peek.innerHTML = `<div class="pk-bar"><button type="button" class="pk-ask" data-ask="${ref}"><i>T</i>Ask Tojo about this</button><button type="button" class="pk-x" aria-label="Close">×</button></div>${h}`;
  peek.classList.add("on");
  const r = el.getBoundingClientRect(); const pw = peek.offsetWidth, ph = peek.offsetHeight;
  let x = r.left + r.width/2 - pw/2; x = Math.max(8, Math.min(innerWidth - pw - 8 - (document.body.classList.contains("chat-open") && innerWidth > 900 ? 400 : 0), x));
  let y = r.top - ph - 8; if (y < 8) y = r.bottom + 8; peek.style.left = x+"px"; peek.style.top = y+"px"; }
function hidePeek(){ clearTimeout(hideT); peek.classList.remove("on"); peekRef = null; }
function laterHide(ms=260){ clearTimeout(hideT); hideT = setTimeout(()=>{ if (!peek.matches(":hover") && !peek.contains(document.activeElement)) hidePeek(); }, ms); }
document.addEventListener("pointerover", e => { if (e.pointerType==="touch") return; if (peek.contains(e.target)) { clearTimeout(hideT); return; } const el = e.target.closest("#stage [data-ref]"); if (!el) return; clearTimeout(peekT); peekT = setTimeout(()=>showPeek(el), 120); });
document.addEventListener("pointerout", e => { if (e.target.closest("#stage [data-ref]") || peek.contains(e.target)) { clearTimeout(peekT); laterHide(); } });
document.addEventListener("focusin", e => { if (peek.contains(e.target)) { clearTimeout(hideT); return; } const el = e.target.closest("#stage [data-ref]"); if (el) showPeek(el); });
document.addEventListener("focusout", () => laterHide(200));
let pressT; document.addEventListener("touchstart", e => { if (peek.contains(e.target)) return; const el = e.target.closest("#stage [data-ref]"); if (!el) return; pressT = setTimeout(()=>{ showPeek(el); el.dataset.peeked = "1"; }, 380); }, {passive:true});
document.addEventListener("touchend", () => clearTimeout(pressT));
addEventListener("scroll", () => { if (!peek.contains(document.activeElement)) hidePeek(); }, {passive:true});
peek.addEventListener("click", e => { e.stopPropagation(); if (e.target.closest(".pk-x")) return hidePeek(); const a = e.target.closest("[data-ask]"); if (a) { askTojo(a.dataset.ask); hidePeek(); } });

/* sheet: the full story, with Ask Tojo beside the close button */
const sheet = document.getElementById("sheet"), scrim = document.getElementById("scrim"), sheetBody = document.getElementById("sheetBody");
function openSheet(ref){ const [h,st] = detailFor(ref); if (!h) return; hidePeek(); sheet.dataset.ref = ref;
  sheet.style.setProperty("--sh-state", st==="off"?"var(--c-bad)":st==="watch"?"var(--c-warn)":"var(--c-ok)");
  const canAsk = !ref.startsWith("uni");
  sheet.querySelector(".sh-ask").hidden = !canAsk;
  sheetBody.innerHTML = h; sheet.classList.add("on"); scrim.classList.add("on"); sheet.scrollTop = 0; sheet.querySelector(canAsk ? ".sh-ask" : ".x").focus(); }
function closeSheet(){ sheet.classList.remove("on"); scrim.classList.remove("on"); }
sheet.querySelector(".x").onclick = closeSheet; scrim.onclick = closeSheet;
sheet.querySelector(".sh-ask").onclick = () => askTojo(sheet.dataset.ref);
addEventListener("keydown", e => { if (e.key==="Escape") { if (sheet.classList.contains("on")) closeSheet(); else if (peek.classList.contains("on")) hidePeek(); else closeChat(); } });

/* chat */
function fillChat(){ const c = D.chat;
  document.getElementById("chatSub").textContent = c.sub;
  document.getElementById("chatBody").innerHTML = `<div class="msg">${c.msg.map(m=>`<p>${esc(m)}</p>`).join("")}</div><div class="lbl">Tojo's note</div><div class="note">${esc(c.note)}</div>
  <div class="lbl">Add to a point — pick one or more</div>${c.points.map((t,i)=>`<button class="pt" type="button" aria-pressed="false"><b>P${i+1}</b> ${esc(t)}</button>`).join("")}
  <div class="lbl">Or ask next</div>${c.asks.map(t=>`<button class="ask" type="button">${esc(t)}</button>`).join("")}`;
  document.querySelectorAll("#chat .pt").forEach(b => b.onclick = () => b.setAttribute("aria-pressed", b.getAttribute("aria-pressed")==="true"?"false":"true"));
  document.querySelectorAll("#chat .ask").forEach(b => b.onclick = () => { chatIn.value = b.textContent; chatIn.focus(); });
}
const chatIn = document.getElementById("chatIn"), chatBody = document.querySelector("#chat .body"), ctxBox = document.getElementById("chatCtx");
let chatCtx = null;
function openChat(){ document.body.classList.add("chat-open"); setTimeout(()=>chatIn.focus(), 300); markTab("chat"); }
function closeChat(){ document.body.classList.remove("chat-open"); markTab(lastTab); }
document.getElementById("chatFab").onclick = openChat;
document.getElementById("chatClose").onclick = closeChat;

function contextFor(ref){
  const [t,id] = ref.split(":");
  if (t==="kpi"){ const k = KP[id]; return { kind:"KPI", point:`the KPI "${k.name}"`, title:k.name, lines:[`Now ${fmtv(k,k.now)} · plan for this week ${fmtv(k,k.plan)} · target ${fmtv(k,k.target)}`, `${STATE_WORD[k.state]}: ${gapText(k)}`] }; }
  if (t==="per"){ const p = P[id]; return { kind:"Person", point:`${p.name}'s tasks (${p.role})`, title:`${p.name} · ${p.role}`, lines:[`${p.done} of ${p.due} done this week${p.late?`, ${p.late} late`:""} · ${PERSON_WORD[p.state]}`].concat(p.impact?[p.impact]:[]) }; }
  if (t==="part"){ const x = D.parts.find(q=>q.id==id); return { kind:"Integration", point:`part ${x.id}, "${x.name}"`, title:`${x.id}. ${x.name}`, lines:[`${PART_WORD[x.st]} · ${x.when}`, `Reads from ${x.src} · ${x.fresh} · owner ${P[x.owner].name}`] }; }
  if (t==="health") return { kind:"Project Status", point:"the suite's break-even and costs", title:"Break-even and costs", lines:[`Break-even forecast ${D.breakeven.fore}, plan ${D.breakeven.plan} (${D.breakeven.late} late)`, `Spent ${L(spendTotal)} · EBITDA added ${L(ebitdaTotal)}`] };
  if (t==="month"){ const i=+id; return { kind:"Project Status", point:`the money for ${D.cumMonths[i]}`, title:`${D.cumMonths[i]}: money out and back`, lines:[`Out to date ${L(D.cumSpend[i])} · EBITDA back to date ${L(D.cumFore[i])}${i>D.actualTo?" (forecast)":""}`] }; }
  if (t==="files") return { kind:"Resources", point:"the suite's resources", title:"Resources", lines:[`${D.resources.length} items · latest: weekly review notes, 9 Oct`] };
  return null;
}
function promptFor(c){ return `Tell me more about ${c.point}: where this stands, whether there is any delay or overrun on it, who or what is responsible for it, whether we have any way to recover, and how we are planning to recover.`; }
function drawCtx(){ ctxBox.hidden = !chatCtx; if (!chatCtx) return;
  ctxBox.innerHTML = `<div><span>${esc(chatCtx.kind)} · added from the page</span><b>${esc(chatCtx.title)}</b>${chatCtx.lines.map(l=>`<small>${esc(l)}</small>`).join("")}</div><button type="button" aria-label="Remove this from the message">×</button>`;
  ctxBox.querySelector("button").onclick = () => { chatCtx = null; drawCtx(); chatIn.focus(); }; }
function askTojo(ref){ const c = contextFor(ref); if (!c) return; chatCtx = Object.assign({ref, suite:SUITE_KEY}, c); drawCtx(); chatIn.value = promptFor(c);
  openChat(); setTimeout(()=>{ chatIn.focus(); chatIn.setSelectionRange(chatIn.value.length, chatIn.value.length); chatBody.scrollTop = chatBody.scrollHeight; }, 320); }

function replyFor(ref){
  const [t,id] = ref.split(":"); const who = k => P[k].name;
  const fixes = f => `<ul>${f.map(x=>`<li>${esc(x[0])} · <b>${esc(who(x[1]))}</b>, ${esc(x[2])}</li>`).join("")}</ul>`;
  if (t==="kpi"){ const k = KP[id];
    if (k.state==="ahead") return [`<p><b>${esc(k.name)}</b> is at ${fmtv(k,k.now)}. The plan for this week was ${fmtv(k,k.plan)}, so it is ${gapText(k)}. The target is ${fmtv(k,k.target)}.</p><p>There is no delay or overrun here. ${esc(k.why)}</p><p>Nothing to recover. ${esc(D.aheadRisk)}</p>`, "Ahead of plan. Keep it there."];
    return [`<p><b>${esc(k.name)}</b> is at ${fmtv(k,k.now)} against ${fmtv(k,k.plan)} planned for this week, so it is ${STATE_WORD[k.state].toLowerCase()}: ${gapText(k)}. The target is ${fmtv(k,k.target)}.</p><p><b>What is causing it:</b></p><ul>${k.factors.map(f=>`<li>${esc(f[0])} (${f[1]}% of the gap)</li>`).join("")}</ul><p><b>How we recover:</b></p>${fixes(k.fixes)}<p>${esc(k.back)}.</p>`, k.back + "."]; }
  if (t==="per"){ const p = P[id]; const late = p.today.filter(x=>String(x[1]).startsWith("late"));
    return [`<p><b>${esc(p.name)}</b> (${esc(p.role)}) has done ${p.done} of ${p.due} tasks this week${p.late?`, with ${p.late} late`:""}.</p>${p.impact?`<p><b>What the delay costs:</b> ${esc(p.impact)}</p>`:`<p>No delay on this person's tasks.</p>`}${late.length?`<p><b>Running late:</b></p><ul>${late.map(x=>`<li>${esc(x[0])} (${esc(x[1])})</li>`).join("")}</ul>`:""}<p><b>Coming up:</b></p><ul>${p.next.slice(0,3).map(n=>`<li>${esc(n[0])} · ${esc(n[1])}</li>`).join("")}</ul>`, p.late ? `${p.name.split(" ").slice(-2)[0]} needs help this week.` : "On top of the work."]; }
  if (t==="part"){ const x = D.parts.find(q=>q.id==id);
    if (x.delay) return [`<p><b>${esc(x.name)}</b> is ${PART_WORD[x.st].toLowerCase()}: ${esc(x.when)}. ${esc(x.delay)}</p><p><b>Responsible:</b> ${esc(who(x.owner))}, with the vendor.</p><p><b>How we recover:</b></p>${fixes(x.fixes)}`, "Chase the vendor this week."];
    return [`<p><b>${esc(x.name)}</b> is ${PART_WORD[x.st].toLowerCase()}: ${esc(x.when)}. It reads from ${esc(x.src)} and its data is ${esc(x.fresh)}.</p><p>${esc(x.note)}</p><p>${x.st==="live"?"No delay. It is running as planned.":x.st==="notstarted"?"It has not started, and it is not due to yet, so there is no overrun.":"It is on its planned date, so there is no overrun yet."} Owner: ${esc(who(x.owner))}.</p>`, x.st==="live" ? "Live and flowing." : "On its date so far."]; }
  if (t==="health") return [`<p>Break-even is forecast for <b>${D.breakeven.fore}</b>, ${D.breakeven.late} after the plan's ${D.breakeven.plan}. So far ${L(spendTotal)} has gone out and ${L(ebitdaTotal)} of EBITDA has come back.</p><p><b>What is causing it:</b></p><ul>${D.healthFactors.map(f=>`<li>${esc(f[0])} (${f[1]}%)</li>`).join("")}</ul><p><b>How we recover:</b></p>${fixes(D.healthFixes)}<p>${esc(D.recoverLine)}</p>`, "Three fixes bring January back."];
  if (t==="month"){ const i=+id; return [`<p>By the end of ${D.cumMonths[i]}, ${L(D.cumSpend[i])} will have gone out and ${L(D.cumFore[i])} of EBITDA will have come back${i>D.actualTo?" (forecast)":""}.</p><p>${D.cumFore[i] >= D.cumSpend[i] ? "The suite has paid for itself by this month." : `Still ${L(D.cumSpend[i]-D.cumFore[i])} short of break-even.`}</p>`, "Watch the gap close."]; }
  return [`<p>${D.resources.length} items are filed for this suite. The latest are the weekly review notes from 9 Oct.</p>`, "All filed."];
}
function sendChat(){
  const text = chatIn.value.trim(); if (!text) { chatIn.focus(); return; }
  const c = chatCtx;
  chatBody.insertAdjacentHTML("beforeend", `<div class="you">${c?`<div class="att"><span>${esc(c.kind)}</span><b>${esc(c.title)}</b></div>`:""}<p>${esc(text)}</p></div>`);
  chatIn.value = ""; chatCtx = null; drawCtx(); closeSheet(); hidePeek();
  const wait = document.createElement("div"); wait.className = "typing"; wait.innerHTML = "<i></i><i></i><i></i>"; chatBody.appendChild(wait); chatBody.scrollTop = chatBody.scrollHeight;
  setTimeout(() => { wait.remove();
    if (c && c.suite) setSuite(c.suite); const [h, note] = c ? replyFor(c.ref) : [`<p>In the working product I answer this from the suite's live records. In this mockup I can answer the questions raised from the page: use Ask Tojo about this on any item.</p>`, "Ask from the page."];
    chatBody.insertAdjacentHTML("beforeend", `<div class="msg">${h}</div><div class="lbl">Tojo's note</div><div class="note">${esc(note)}</div>`);
    chatBody.lastElementChild.previousElementSibling.previousElementSibling.scrollIntoView({block:"start", behavior:"smooth"}); }, 1100);
}
document.querySelector("#chat .send").onclick = sendChat;
chatIn.addEventListener("keydown", e => { if (e.key==="Enter" && !e.shiftKey) { e.preventDefault(); sendChat(); } });

/* tabs and clicks */
let lastTab = "overview";
function markTab(t){ document.querySelectorAll("#stage nav [data-tab]").forEach(b => { const on = b.dataset.tab===t; b.classList.toggle("on", on); b.setAttribute("aria-current", on?"page":"false"); }); }
function go(t){
  if (t==="chat") return openChat();
  if (t==="files") { markTab("files"); return openSheet("files:0"); }
  lastTab = t; markTab(t);
  if (t==="overview") return scrollTo({top:0, behavior:"smooth"});
  const z = document.querySelector(`#stage [data-zone="${t}"]`); if (!z) return;
  const y = z.getBoundingClientRect().top + scrollY - 70; scrollTo({top:y, behavior:"smooth"});
  z.classList.remove("flash"); void z.offsetWidth; z.classList.add("flash");
}
document.addEventListener("click", e => {
  const tb = e.target.closest("#stage [data-tab]"); if (tb) { e.preventDefault(); return go(tb.dataset.tab); }
  const vw = e.target.closest("[data-view]"); if (vw) { UI.view = vw.dataset.view; const y = scrollY; render(); scrollTo(0,y); return; }
  const op = e.target.closest("[data-ref]"); if (op && !op.matches("[data-nopen]")) { suiteOf(op); return openSheet(op.dataset.ref); }
});
document.getElementById("uniBtn").onclick = () => openSheet("uni:0");

/* small svg helpers */
function linePath(vals, x0, x1, y0, y1, vmin, vmax){ const n = vals.length; return vals.map((v,i)=>{ const x = x0 + (x1-x0)*i/(n-1); const y = y1 - (y1-y0)*(v - vmin)/(vmax - vmin); return (i?"L":"M")+x.toFixed(1)+","+y.toFixed(1); }).join(" "); }
function weekly(k){ /* 11 points, week 0..10, from base to now with gentle wobble */
  const out = []; for (let w=0; w<=D.week; w++){ const t = w/D.week; const ease = t<.3 ? t*.5 : .15 + (t-.3)/.7*.85; let v = k.base + (k.now-k.base)*ease; const wob = Math.sin(w*2.3 + k.id.charCodeAt(1))*Math.abs(k.target-k.base)*0.035*(w>0&&w<D.week?1:0); out.push(v + wob); } return out; }
function viewToggle(cls){ return `<div class="${cls}" role="group" aria-label="Show daily or weekly tasks"><button type="button" data-view="day" aria-pressed="${UI.view==="day"}">Today</button><button type="button" data-view="week" aria-pressed="${UI.view==="week"}">This week</button></div>`; }
