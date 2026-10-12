/* ===== Suite block library: every block of the approved suite landings, by suite and by section ===== */
const LIB_CSS = `
.lib{background:#F7F7F5;color:#1D1F22;padding:24px 16px 120px;font-family:var(--f-body)}
.lib .in{max-width:1240px;margin:0 auto}
.lib h2{font-family:var(--f-num);font-weight:400;font-size:44px;line-height:1;margin:44px 0 6px;letter-spacing:.01em}
.lib h3{font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1;margin:30px 0 10px}
.lib p.lede{max-width:72ch;color:#4A4E55;margin:0 0 14px}
.lib .toc{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 0}
.lib .toc a{border:1.5px solid #D9DADC;background:#fff;border-radius:999px;padding:7px 13px;font-size:13px;font-weight:600;color:#1D1F22;text-decoration:none}
.lib .how{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.lib .how div,.lib .card{background:#fff;border:1.5px solid #E3E3E0;border-radius:14px;padding:14px}
.lib .how b{display:block;font-size:14px;margin-bottom:4px}
.lib .how p{margin:0;font-size:13px;color:#4A4E55}
.lib table{width:100%;border-collapse:collapse;font-size:13px;background:#fff}
.lib th,.lib td{border-bottom:1px solid #E3E3E0;padding:8px 10px;text-align:left;vertical-align:top}
.lib th{font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:#5E636A}
.lib .tw{overflow-x:auto;border:1.5px solid #E3E3E0;border-radius:14px}
.lib .suite-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 16px;border-top:4px solid #1D1F22;padding-top:12px;margin-top:56px}
.lib .suite-h h2{margin:0}
.lib .suite-h span{font-size:13px;color:#5E636A}
.lib .sw{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 4px}
.lib .sw i{display:flex;align-items:center;gap:8px;font-style:normal;font-size:12px;background:#fff;border:1.5px solid #E3E3E0;border-radius:999px;padding:4px 10px 4px 4px}
.lib .sw i::before{content:"";width:22px;height:22px;border-radius:50%;background:var(--c);border:1px solid rgba(0,0,0,.12)}
.lib .blk{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:16px;align-items:start;margin:18px 0 26px}
.lib .blk .tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:#1D1F22;color:#fff;border-radius:4px;padding:2px 7px;margin-bottom:6px}
.lib .blk .tag.u{background:#E8E8E4;color:#1D1F22}
.lib .use h4{margin:0 0 6px;font-size:15px}
.lib .use dl{margin:0;display:grid;gap:8px;font-size:12.5px}
.lib .use dt{font-weight:700;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#5E636A}
.lib .use dd{margin:0;color:#2E3136}
.lib .use code{font-size:11.5px;background:#F1F1EE;border-radius:4px;padding:1px 4px}
.lib .canvas{border-radius:16px;overflow:hidden;border:1.5px solid #E3E3E0;min-width:0}
.lib .canvas > div{padding:16px!important;min-height:0!important}
.lib .canvas .wrap{max-width:none!important}
.lib .canvas .zone{margin-top:0!important}
.lib .canvas .warn,.lib .canvas .hoard{position:static!important;max-width:none!important}
.lib .demo{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.lib .demo button{border:1.5px solid #1D1F22;background:#fff;border-radius:999px;padding:8px 14px;font-size:13px;font-weight:600;min-height:40px}
@media (max-width:900px){ .lib .blk{grid-template-columns:1fr} }
`;
const BLOCK_INFO = {
  nav:{ name:"Section bar", section:"Every section", shows:"The seven sections of the suite (Overview, Integrations, KPIs, Taskboards, Project Status, Resources, Chat) and a display of the one you are on.",
    data:"Fixed list <code>TABS</code>; nothing from the suite's data.", act:"Overview scrolls to the top; Integrations, KPIs, Taskboards and Project Status jump to their section; Resources opens the resources panel; Chat opens the chat. The display updates on every press.", phone:"Wraps onto two or three rows; nothing hidden." },
  pulse:{ name:"Pulse strip", section:"Overview", shows:"Universal element 1: parts live, KPIs on course, EBITDA back against money out, and the break-even month, each with its plan figure (universal element 2, the plan ghost).",
    data:"<code>parts[].st</code>, <code>kpis[]</code> (state worked out from base, plan, now, target), <code>spend</code>, <code>ebitda</code>, <code>breakeven</code>.", act:"Parts and KPIs jump to their section; the two money readings open the Project Status story. Each carries a hover peek.", phone:"Two across." },
  watch:{ name:"Watch list", section:"Overview", shows:"Universal element 3: the three items furthest off course, each with its owner.",
    data:"<code>watch[]</code>: text, owner key, and a reference to a part, KPI or person.", act:"Hover peek; click opens the full story with Ask Tojo about this.", phone:"Stacked, full width." },
  countdown:{ name:"Next go-live", section:"Overview", shows:"Universal element 5: days to the next part switching on, and what it is.",
    data:"<code>milestone</code>: what, date, days, part.", act:"Opens that part's story.", phone:"Full width under the watch list." },
  hero:{ name:"Integrations drawing", section:"Integrations", shows:"Every part (integration) of the suite and how far each has got: live, testing, being built, late, not started. Freshness marks (universal element 6) on each part, and the suite's live counter.",
    data:"<code>parts[]</code>: id, name, source system, status, when, freshness, owner, volume, note; for a late part also <code>delay</code> and <code>fixes</code>. Hand-offs to other suites in <code>handoffs[]</code>.", act:"Every part has a hover peek and opens its story. Live lines move; a late line shows a stop mark. The counter ticks and lights the part that sent the latest entry.", phone:"Scrolls sideways inside its frame, with a line saying so; the page itself never scrolls sideways." },
  kpis:{ name:"KPIs", section:"KPIs", shows:"Each KPI's start, plan for this week, today's value and target, and whether it is on track, slightly behind or off track.",
    data:"<code>kpis[]</code>: id, name, short name, unit (min, %, h), direction, base, plan, now, target; <code>why</code> when on track; <code>factors</code>, <code>fixes</code>, <code>back</code> when not.", act:"Hover peek; click opens the gap, its causes with their share, the recovery actions with owner and date, and when it is back on plan.", phone:"One or two across." },
  team:{ name:"Taskboards", section:"Taskboards", shows:"Each key person's tasks: this week (done, late, still to do) or today, who is doing well or lagging, and what a delay costs.",
    data:"<code>people[]</code>: key, name, role, where from, done, due, late, today's tasks, impact, critical tasks coming up.", act:"Today / This week switch; click opens today's tasks and the 3–5 critical tasks coming up.", phone:"One across." },
  money:{ name:"Project Status", section:"Project Status", shows:"Money out against EBITDA back by month, the plan, and the break-even month; monthly subscription, salaries of the roles we recommended, one-time costs, extra revenue and EBITDA.",
    data:"<code>months</code>, <code>spend[]</code>, <code>revenue</code>, <code>ebitda</code>, <code>runRate</code>, <code>cumMonths</code>, <code>cumSpend</code>, <code>cumPlan</code>, <code>cumFore</code>, <code>breakeven</code>, <code>healthFactors</code>, <code>healthFixes</code>.", act:"Each month has a hover peek; the reasons button opens why break-even moved and the recovery plan.", phone:"The chart scrolls sideways inside its frame; the cost list stacks under it." }
};
const DRAWN = {
  diorama:{ nav:"A lift panel: round floor buttons and an orange LED display.", pulse:"Green and blue highway signs.", watch:"Yellow diamond road signs.", countdown:"A construction hoarding with yellow and black stripes.", hero:"An isometric model of the hospital: each department is a building piped to the summary engine; numbered beacons on the roofs.", kpis:"Lift shafts: the car is today, the dashed car is the plan, the top floor is the target.", team:"Site crew cards with hard-hat progress rings.", money:"A bridge to break-even, one span a month: solid is built, scaffold is forecast." },
  sorter:{ nav:"Shipping tags hanging from a rail, with an olive 'you are on' plate.", pulse:"Wooden crates with stencilled numbers.", watch:"Cards stamped HELD.", countdown:"A shipping label.", hero:"A sorting floor: events and the charge list drop from the top into the billing engine, which sends bills down to the family and the insurers; moving parcels on live belts.", kpis:"Scale dials: needle is today, dashed tick is the plan, the end of the scale is the target.", team:"Parcel labels with bar marks: thick is done, red is late, thin is still to do.", money:"An area chart of money out against EBITDA back, with a flag at break-even." },
  signal:{ nav:"Signal levers with a dot-matrix display.", pulse:"Three-lamp signal heads.", watch:"Cards with a striped closure edge.", countdown:"A ticket stub.", hero:"The admission line: five stops from arrival to the patient in bed, each link a signal beside the stop it speeds up, tomorrow's bed map above.", kpis:"Plan and today as two bars, with a flag at the target.", team:"Cards with a row of sleepers.", money:"EBITDA back minus money out as a profile crossing zero at break-even." },
  dayboard:{ nav:"Folder tabs with a tear-off calendar date and a 'you are on' line.", pulse:"Appointment cards with a coloured edge.", watch:"Cards marked with two overlapping slots.", countdown:"A pinned sticky note.", hero:"A day board of today's test rooms hour by hour (booked, walk-ins slotted, held for emergencies, free) with a now line; prescriptions coming in above, rules at the side, what the suite sends out below.", kpis:"Grids of 100 squares: filled is today, the outlined square is this week's plan.", team:"Task calendars: a square for each task, filled when done, crossed when late.", money:"Monthly bars: EBITDA back above the line, money out below, the difference as a line." },
  lines:{ nav:"Round numbered section badges.", pulse:"Status pills with a ringed dot.", watch:"Alert cards with a warning triangle.", countdown:"A countdown ring on a dark card.", hero:"Three supply lines (buying, the store, the wards) meeting at the main store; each part is a stop marked with its status, trains run on working lines, and a line is cut where a late part stops supplies getting through; links to other suites as pills.", kpis:"Arc dials: the arc is today, the black tick is this week's plan, the end of the arc is the target.", team:"Journey strips: a stop for each task, filled when done, coral when late.", money:"Paired monthly bars of money out and EBITDA back to date, with the plan line and a break-even stop." },
  radar:{ nav:"A dark capsule bar with a sweeping radar mark.", pulse:"Progress rings.", watch:"Alert cards.", countdown:"A sunflower card.", hero:"A radar of tomorrow's planned admissions closing on the bed map at the centre; the links round the rim.", kpis:"Bullseyes: the centre is the target, the dot is today, the dashed ring is the plan.", team:"Dot timelines.", money:"Monthly steps of the net position." }
};
const SECTIONS = [
  ["Overview","The landing page itself: section bar, title, pulse strip, watch list, next go-live, then a short view of every other section in the order below.","Approved for Discharge Summary and Billing & Insurance."],
  ["Integrations","Every part of the suite on one drawing, with status, freshness, owner and hand-offs.","On the landing page; its own page is next."],
  ["KPIs","Start, plan, today and target for each KPI, with the gap, causes and recovery behind each.","On the landing page; its own page is next."],
  ["Taskboards","Today and this week for each key person, with what delays cost and what is coming up.","On the landing page; its own page is next."],
  ["Project Status","Money out, EBITDA back, monthly costs and break-even, with causes and recovery.","On the landing page; its own page is next."],
  ["Resources","Files for the suite: plan, process flow, specifications, training, review notes, agreement.","Opens as a panel from the section bar."],
  ["Chat","Tojo's chat, hidden behind the floating button; opens at the side in the tools' look. Every popup's Ask Tojo about this opens it with the item attached.","Approved 12 Oct."]
];
function libBlock(scheme, suiteKey, bkey){
  const tmp = document.createElement("div"); tmp.innerHTML = scheme.render(); const root = tmp.firstElementChild;
  const sel = scheme.blocks[bkey]; const el = root.querySelector(sel); if (!el) return "";
  const info = BLOCK_INFO[bkey];
  return `<div class="blk" id="b-${suiteKey}-${bkey}"><div class="canvas"><div class="${root.className}" data-suite="${suiteKey}"><div class="wrap">${el.outerHTML}</div></div></div>
    <div class="card use"><span class="tag">${esc(D.suite)}</span> <span class="tag u">${esc(info.section)}</span><h4>${esc(info.name)}</h4><dl>
      <dt>Drawn as</dt><dd>${esc(DRAWN[scheme.key][bkey])}</dd><dt>What it shows</dt><dd>${info.shows}</dd><dt>Data it needs</dt><dd>${info.data}</dd><dt>What you can do</dt><dd>${info.act}</dd><dt>On a phone</dt><dd>${info.phone}</dd></dl></div></div>`;
}
function onSuite(key){ if (typeof PAGE === "undefined" || PAGE.mode !== "library") return; const a = APPROVED.find(x=>x[0]===key); const sc = a && byKey(a[1]); if (sc) Object.entries(sc.vars).forEach(([k,v]) => document.documentElement.style.setProperty(k, v)); }
function renderLibrary(){
  if (!document.getElementById("libcss")) { const st = document.createElement("style"); st.id = "libcss"; st.textContent = LIB_CSS; document.head.appendChild(st); }
  const approved = APPROVED.filter(a=>byKey(a[1]) && SUITES.find(s=>s.key===a[0]));
  document.getElementById("rvNote").innerHTML = `<b>${approved.length} approved suites</b> · ${approved.map(a=>SUITES.find(s=>s.key===a[0]).data.suite).join(" · ")}. Blocks are live: hover, click, Ask Tojo and the chat all work.`;
  const tok = { diorama:[["Sky","#CFE5F6"],["Lawn","#E3EEDD"],["Ink","#1B2635"],["Live","#1B8A4B"],["Testing","#B47610"],["Late","#C93A30"],["LED","#FF8A1F"]],
    sorter:[["Stone","#F2F1E6"],["Olive","#3B4512"],["Marigold","#F2A900"],["Ink","#23280F"],["Live","#2F7D32"],["Testing","#D49400"],["Late","#B93A12"]],
    signal:[["Mist","#EDF2F1"],["Slate","#172A3A"],["Coral","#EE5A43"],["Live","#16825A"],["Testing","#E3A008"],["Late","#C7372B"]],
    radar:[["Mist","#F4F5FA"],["Indigo","#14123A"],["Sunflower","#F5B700"],["Live","#0F8A61"],["Testing","#E0A500"],["Late","#C93636"]],
    dayboard:[["Blush","#F5F2F6"],["Magenta","#C2185B"],["Sky","#2F7FE0"],["Ink","#24202F"],["Live","#16845C"],["Testing","#D9940A"],["Late","#C62D3A"]],
    lines:[["Mist","#F1F6F4"],["Teal","#0E7C72"],["Coral","#EF6A4C"],["Slate","#33557D"],["Ink","#12302D"],["Live","#1D8A5B"],["Testing","#E39B12"],["Late","#D9472B"]] };
  let h = `<div class="lib"><div class="in">
    <h2 style="margin-top:4px">How to use this library</h2>
    <p class="lede">Every block of the approved automation-suite landing pages, drawn live from the same runtime the pages use. The layout is the same in every suite; the look, colours and drawn elements belong to each suite alone.</p>
    <div class="how">
      <div><b>One layout</b><p>Section bar · title and pulse strip · watch list and next go-live · Integrations drawing · KPIs · Taskboards · Project Status. Never reorder.</p></div>
      <div><b>One look per suite</b><p>A suite's blocks use only its own colours and drawn elements. Never borrow another suite's look, and never reuse a tool's look.</p></div>
      <div><b>Type</b><p>The Virevo type scale everywhere: Bebas Neue for titles and big numbers, Poppins for everything else, Caveat only for handwritten notes and Tojo's Note.</p></div>
      <div><b>Words on the page</b><p>Section headings are just KPIs, Taskboards, Project Status. Hints say what the marks mean; the drawing is never named.</p></div>
      <div><b>Every popup asks Tojo</b><p>Hover peeks and detail panels carry Ask Tojo about this beside the close button. It opens the chat with the item attached and the question written; the user sends, edits or clears it.</p></div>
      <div><b>One data model</b><p>Each suite is one data object (see the data model below). A new suite needs a data file and a look file; the runtime does the rest.</p></div>
    </div>
    <div class="toc">${approved.map(a=>`<a href="#s-${a[0]}">${esc(SUITES.find(s=>s.key===a[0]).data.suite)}</a>`).join("")}<a href="#sections">Sections</a><a href="#universal">Universal elements</a><a href="#model">Data model</a><a href="#index">Index</a></div>
    <h2 id="sections">Sections of every suite</h2>
    <div class="tw"><table><thead><tr><th>Section</th><th>What it holds</th><th>Status</th></tr></thead><tbody>${SECTIONS.map(s=>`<tr><td><b>${s[0]}</b></td><td>${s[1]}</td><td>${s[2]}</td></tr>`).join("")}</tbody></table></div>
    <h2 id="universal">Universal elements</h2>
    <p class="lede">Shared by every suite, redrawn in each suite's look. The pulse strip, plan ghost, watch list, next go-live and freshness marks appear in each suite's blocks below. The three below are the same in every suite.</p>
    <div class="how">${UNIVERSAL.map((u,i)=>`<div><b>${i+1}. ${u[0]}</b><p>${u[1]}</p></div>`).join("")}
      <div><b>Detail panel</b><p>Opens on a click from any part, KPI, person, month or the money readings. Shows the full story; Ask Tojo about this and the close button sit together at the top.</p></div>
      <div><b>Chat panel</b><p>Hidden behind the floating Ask Tojo button; opens at the side in the tools' look (forest, cream, gold, Tojo's Note in Caveat). On a phone it takes the whole screen.</p></div></div>
    <div class="demo">${approved.map(a=>`<button type="button" data-libdemo="${a[0]}">Open a KPI story · ${esc(SUITES.find(s=>s.key===a[0]).data.suite)}</button>`).join("")}<button type="button" data-libchat="1">Open the chat</button></div>`;
  const index = [];
  approved.forEach(([su,k]) => { const sc = byKey(k); setSuite(su);
    h += `<div class="suite-h" id="s-${su}"><h2>${esc(D.suite)}</h2><span>Approved look: ${esc(sc.name.toLowerCase())} · ${esc(D.family)} · ${D.parts.length} parts · ${D.kpis.length} KPIs · ${D.people.length} people</span></div>
      <div class="sw">${(tok[k]||[]).map(t=>`<i style="--c:${t[1]}">${t[0]} <code>${t[1]}</code></i>`).join("")}</div>`;
    Object.keys(BLOCK_INFO).forEach(b => { h += libBlock(sc, su, b); index.push([D.suite, BLOCK_INFO[b].name, BLOCK_INFO[b].section, DRAWN[k][b], `b-${su}-${b}`]); });
  });
  setSuite(approved[0][0]);
  h += `<h2 id="model">Data model of a suite</h2><p class="lede">One object per suite. Statuses: <code>live</code>, <code>testing</code>, <code>building</code>, <code>blocked</code> (late), <code>notstarted</code>. KPI state (on track, slightly behind, off track) is worked out from base, plan, now and target; a person's state from done, due and late.</p>
    <div class="tw"><table><thead><tr><th>Field</th><th>Holds</th></tr></thead><tbody>${[
      ["suite, family, hospital, started, week, weeksPlanned, asOf","Name, the tool it comes from, the hospital, timing and data freshness"],
      ["chat","Tojo's opening message, note, four points and three prompts"],
      ["milestone","Next go-live: what, date, days, part"],
      ["parts[]","id, name, src, status (st), when, fresh, owner, vol, note; delay and fixes when late; suite-specific placing (dept, side, stage, room or bay)"],
      ["handoffs[]","Lines to and from other suites"],
      ["kpis[]","id, name, short, unit, dir, base, plan, now, target; why, or factors, fixes and back"],
      ["people[]","key, name, role, from, done, due, late, today[], impact, next[]"],
      ["months, spend[], revenue, ebitda, runRate","Monthly money so far and at full run (₹ lakh)"],
      ["cumMonths, cumSpend, cumPlan, cumFore, actualTo, breakeven","Cumulative money out, plan and forecast EBITDA back, break-even plan and forecast"],
      ["healthFactors, healthFixes, recoverLine","Why break-even moved and how it recovers"],
      ["watch[]","Three items with owner and reference"],
      ["resources[]","Files for the Resources panel"]].map(r=>`<tr><td><code>${r[0]}</code></td><td>${r[1]}</td></tr>`).join("")}</tbody></table></div>
    <h2 id="index">Index of blocks</h2><div class="tw"><table><thead><tr><th>Suite</th><th>Block</th><th>Section</th><th>Drawn as</th></tr></thead><tbody>${index.map(r=>`<tr><td>${esc(r[0])}</td><td><a href="#${r[4]}">${esc(r[1])}</a></td><td>${esc(r[2])}</td><td>${esc(r[3])}</td></tr>`).join("")}</tbody></table></div>
    </div></div>`;
  stage.innerHTML = h;
  stage.querySelectorAll("[data-libdemo]").forEach(b => b.onclick = () => { setSuite(b.dataset.libdemo); openSheet("kpi:" + D.kpis.find(k=>k.state==="off").id); });
  stage.querySelector("[data-libchat]").onclick = () => openChat();
}
