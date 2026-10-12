/* ===== Scheme D: the departures hall ===== */
SCHEMES.push({
  key:"departures", letter:"D", name:"Departures hall",
  note:"<b>D · Departures hall.</b> Discharge is a departure, so the suite reads like a station. Parts going live are departures with their gate and remarks, KPIs are arrivals that come in early or delayed, the team is the crew roster, and break-even is a scheduled arrival running late. Split-flap boards, a service-alert ticker and yellow wayfinding signs for the sections.",
  vars:{ "--sh-bg":"#15181B","--sh-fg":"#F2F2EE","--sh-mute":"#A3A9AF","--sh-line":"#2C3136","--sh-card":"#1C2024","--c-ok":"#39D98A","--c-warn":"#FFB547","--c-bad":"#FF6A5E","--pk-bg":"#FFD21F","--pk-fg":"#111","--pk-line":"#111","--pk-r":"4px","--sh-r":"8px" },
  fab:18,
  css:`
.s4{--hall:#2A2E33;--board:#0E1012;--flap:#24282C;--flap2:#1B1E21;--txt:#F2F2EE;--mute:#A3A9AF;--yel:#FFD21F;--ok:#39D98A;--warn:#FFB547;--bad:#FF6A5E;
  background:linear-gradient(180deg,#3A3F45,var(--hall) 300px,#23272B);color:var(--txt);padding:0 0 90px;overflow-x:clip}
.s4 .way{background:var(--yel);color:#111;display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;border-bottom:4px solid #111}
.s4 .ws{display:flex;align-items:center;gap:10px;background:transparent;border:0;border-right:2px solid #111;padding:10px 18px;font-family:var(--f-num);font-size:24px;letter-spacing:.04em;white-space:nowrap;color:#111;min-height:56px}
.s4 .ws i{width:32px;height:32px;background:#111;color:var(--yel);display:grid;place-items:center;font-style:normal;font-family:var(--f-body);font-size:18px;font-weight:700;border-radius:3px}
.s4 .ws.on{background:#111;color:var(--yel)} .s4 .ws.on i{background:var(--yel);color:#111}
.s4 .ws:hover{background:#FFE36B}
.s4 .wrap{max-width:1240px;margin:0 auto;padding:0 16px}
.s4 .hero{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px;align-items:end;padding:26px 0 14px}
.s4 .hero small{font-size:12px;letter-spacing:.16em;color:var(--yel);font-weight:600}
.s4 .hero h2{font-family:var(--f-num);font-weight:400;font-size:80px;line-height:.88;margin:6px 0 0;letter-spacing:.02em}
.s4 .clk{text-align:right}
.s4 .clk b{font-family:var(--f-num);font-weight:400;font-size:64px;line-height:.9;color:var(--yel);font-variant-numeric:tabular-nums}
.s4 .clk small{display:block;color:var(--mute);letter-spacing:.06em}
.s4 .fl{display:inline-flex;flex-wrap:wrap;gap:3px}
.s4 .fc{position:relative;display:inline-grid;place-items:center;min-width:.72em;padding:0 .08em;height:1.18em;background:linear-gradient(180deg,var(--flap) 50%,var(--flap2) 50%);border-radius:3px;font-family:var(--f-num);line-height:1;box-shadow:0 2px 0 #000,inset 0 1px 0 rgba(255,255,255,.06)}
.s4 .fc::after{content:"";position:absolute;left:0;right:0;top:50%;height:1px;background:#000;opacity:.85}
.s4 .fc.sp{background:transparent;box-shadow:none;min-width:.35em}
.s4 .fc.sp::after{display:none}
.s4 .counters{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:8px 0 14px}
.s4 .cnt{background:var(--board);border:1px solid #000;border-radius:8px;padding:10px 12px;text-align:left;color:inherit;box-shadow:0 10px 24px rgba(0,0,0,.35)}
.s4 .cnt > span{display:block;font-size:11px;letter-spacing:.14em;color:var(--mute);font-weight:600;margin-bottom:6px}
.s4 .cnt .fl{font-size:34px}
.s4 .cnt em{display:block;font-style:normal;font-size:11.5px;color:var(--mute);margin-top:6px}
.s4 .ticker{display:flex;align-items:stretch;background:#111;border:2px solid var(--bad);border-radius:6px;overflow:hidden;margin-bottom:12px}
.s4 .ticker > b{background:var(--bad);color:#111;font-family:var(--f-num);font-weight:400;font-size:20px;letter-spacing:.06em;padding:8px 12px;white-space:nowrap;display:grid;place-items:center}
.s4 .tk{overflow:hidden;flex:1;position:relative;display:flex;align-items:center}
.s4 .tk .run{display:flex;gap:48px;white-space:nowrap;padding-left:20px;animation:s4tick 32s linear infinite}
.s4 .tk:hover .run,.s4 .tk:focus-within .run{animation-play-state:paused}
.s4 .tk button{background:transparent;border:0;color:#FFD3CF;font-size:14px;font-weight:500;white-space:nowrap;min-height:40px}
.s4 .tk button b{color:var(--yel);font-weight:600}
@keyframes s4tick{to{transform:translateX(-50%)}}
.s4 .next{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;background:#0B2A1C;border:1px solid #145E3B;border-radius:8px;padding:10px 14px;margin-bottom:20px;color:inherit;width:100%;text-align:left}
.s4 .next .fl{font-size:30px}
.s4 .next > span:not(.fl){font-size:13px}
.s4 .next > span b{color:var(--ok);letter-spacing:.1em;font-size:11.5px;display:block}
.s4 .board{position:relative;background:var(--board);border:10px solid #3B4148;border-radius:10px;box-shadow:0 22px 40px rgba(0,0,0,.45),inset 0 0 0 1px #000;margin-top:44px;scroll-margin-top:30px}
.s4 .board::before,.s4 .board::after{content:"";position:absolute;top:-46px;width:6px;height:36px;background:linear-gradient(90deg,#666,#bbb,#666)}
.s4 .board::before{left:14%} .s4 .board::after{right:14%}
.s4 .bh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px 16px;padding:12px 16px;border-bottom:2px solid #000;background:#14171A}
.s4 .bh h3{margin:0;font-family:var(--f-num);font-weight:400;font-size:34px;letter-spacing:.06em;line-height:1;color:var(--yel);display:flex;align-items:center;gap:12px}
.s4 .bh h3 i{font-style:normal;font-family:var(--f-body);font-size:22px;color:var(--yel)}
.s4 .bh p{margin:0;font-size:12.5px;color:var(--mute)}
.s4 .cols,.s4 .row{display:grid;gap:12px;align-items:center;padding:8px 16px}
.s4 .cols{font-size:10.5px;letter-spacing:.14em;color:var(--mute);font-weight:600;border-bottom:1px solid #22262A}
.s4 .row{width:100%;background:transparent;border:0;border-bottom:1px solid #1D2125;color:inherit;text-align:left;min-height:52px}
.s4 .row:nth-of-type(even){background:rgba(255,255,255,.015)}
.s4 .row:hover,.s4 .row:focus-visible{background:rgba(255,210,31,.07)}
.s4 .row .fl{font-size:19px}
.s4 .row .dst{font-size:14.5px;font-weight:600;line-height:1.25}
.s4 .row .dst small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s4 .gate{font-family:var(--f-num);font-size:22px;color:var(--yel);letter-spacing:.04em}
.s4 .rm .fc{color:currentColor}
.s4 .ok{color:var(--ok)} .s4 .warn{color:var(--warn)} .s4 .bad{color:var(--bad)} .s4 .dim{color:var(--mute)}
.s4 .blink{animation:s4b 1.4s steps(2) infinite}
@keyframes s4b{50%{opacity:.35}}
.s4 .dep .cols,.s4 .dep .row{grid-template-columns:110px minmax(0,1.6fr) minmax(0,1fr) 70px 200px}
.s4 .arr .cols,.s4 .arr .row{grid-template-columns:minmax(0,1.5fr) 100px 100px 110px 100px 250px}
.s4 .crw .cols,.s4 .crw .row{grid-template-columns:minmax(0,1.3fr) minmax(0,1.6fr) 90px 100px 160px}
.s4 .num{font-family:var(--f-num);font-size:22px;letter-spacing:.03em;font-variant-numeric:tabular-nums}
.s4 .num.dim{font-size:20px}
.s4 .crw .row .imp{font-size:11.5px;color:#FFB3AC;display:block;font-weight:400;margin-top:2px}
.s4 .crw .row .tdy{font-size:11.5px;color:var(--mute);display:block;font-weight:400;margin-top:2px}
.s4 .vt{display:inline-flex;border:2px solid var(--yel);border-radius:4px;overflow:hidden}
.s4 .vt button{background:transparent;border:0;color:var(--yel);padding:6px 12px;font-size:12px;font-weight:600;letter-spacing:.06em;min-height:36px}
.s4 .vt button[aria-pressed="true"]{background:var(--yel);color:#111}
.s4 .fare{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0}
.s4 .fare > div{padding:14px 16px}
.s4 .fare > div + div{border-left:1px solid #22262A}
.s4 .mrow{display:grid;grid-template-columns:70px repeat(3,minmax(0,1fr));gap:8px;align-items:center;padding:6px 0;border-bottom:1px solid #1D2125;font-size:12px;color:var(--mute)}
.s4 .mrow .num{color:var(--txt);font-size:22px}
.s4 .mrow button{background:transparent;border:0;color:inherit;text-align:left;padding:0}
.s4 .sched{display:grid;gap:10px}
.s4 .sched button{display:grid;grid-template-columns:120px minmax(0,1fr);gap:12px;align-items:center;background:transparent;border:0;border-bottom:1px solid #1D2125;color:inherit;text-align:left;padding:6px 0}
.s4 .sched small{font-size:10.5px;letter-spacing:.14em;color:var(--mute);font-weight:600}
.s4 .sched .fl{font-size:28px}
.s4 .runway{margin-top:12px;position:relative;height:46px}
.s4 .runway svg{width:100%;height:46px;display:block}
.s4 .hand{padding:10px 16px;font-size:12.5px;color:var(--mute);border-top:1px solid #22262A}
.s4 .hand b{color:var(--txt)}
@media (max-width:1000px){ .s4 .counters{grid-template-columns:repeat(2,minmax(0,1fr))} .s4 .fare{grid-template-columns:1fr} .s4 .fare > div + div{border-left:0;border-top:1px solid #22262A}
  .s4 .cols{display:none}
  .s4 .dep .row{grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"d r" "t g"} .s4 .dep .row .c1{grid-area:t} .s4 .dep .row .c2{grid-area:d} .s4 .dep .row .c3{display:none} .s4 .dep .row .c4{grid-area:g;text-align:right} .s4 .dep .row .c5{grid-area:r;text-align:right}
  .s4 .arr .row{grid-template-columns:repeat(4,minmax(0,1fr));grid-template-areas:"n n n n" "a b c d" "r r r r"} .s4 .arr .row .c1{grid-area:n} .s4 .arr .row .c2{grid-area:a} .s4 .arr .row .c3{grid-area:b} .s4 .arr .row .c4{grid-area:c} .s4 .arr .row .c5{grid-area:d} .s4 .arr .row .c6{grid-area:r}
  .s4 .arr .row .lab{display:block;font-size:10px;letter-spacing:.12em;color:var(--mute);font-weight:600}
  .s4 .crw .row{grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"n s" "i i"} .s4 .crw .row .c1{grid-area:n} .s4 .crw .row .c2{grid-area:i} .s4 .crw .row .c3,.s4 .crw .row .c4{display:none} .s4 .crw .row .c5{grid-area:s;text-align:right} }
.s4 .lab{display:none}
@media (max-width:600px){ .s4 .next .fl{font-size:20px} .s4 .hero{grid-template-columns:1fr} .s4 .clk{text-align:left} .s4 .hero h2{font-size:54px} .s4 .clk b{font-size:44px} .s4 .cnt .fl{font-size:24px} .s4 .row .fl{font-size:17px} .s4 .num{font-size:19px} .s4 .bh h3{font-size:26px} .s4 .board{border-width:6px} .s4 .ws{font-size:20px;padding:8px 12px} .s4 .sched button{grid-template-columns:1fr} .s4 .sched .fl{font-size:22px} .s4 .mrow .num{font-size:18px} }
`,
  render(){
    const flap = (t, cls="") => `<span class="fl ${cls}" aria-label="${esc(t)}">${[...String(t).toUpperCase()].map(c=>`<span class="fc ${c===" "?"sp":""}" aria-hidden="true">${c===" "?"&nbsp;":esc(c)}</span>`).join("")}</span>`;
    const remark = { live:["DEPARTED","ok"], testing:["BOARDING","warn"], building:["ON SCHEDULE","dim"], blocked:["DELAYED 9D","bad blink"], notstarted:["SCHEDULED","dim"] };
    const goDate = x => { const m = [...x.when.matchAll(/(\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))/g)]; if (m.length) return m[m.length-1][1]; const w = x.when.match(/(\d) of (\d)/); return w ? `${w[1]}/${w[2]} WD` : "—"; };
    const dep = x => `<button class="row" type="button" data-ref="part:${x.id}"><span class="c1">${flap(goDate(x).toUpperCase())}</span><span class="c2 dst">${String(x.id).padStart(2,"0")} · ${esc(x.name)}<small>${esc(x.when)} · ${esc(x.fresh)}</small></span><span class="c3 dst" style="font-weight:400;color:var(--mute);font-size:13px">via ${esc(x.src)}</span><span class="c4 gate">${initials(P[x.owner].name)}</span><span class="c5 rm ${remark[x.st][1]}">${flap(remark[x.st][0])}</span></button>`;
    const rem = k => { if (k.state==="ahead") return k.unit==="%" ? `AHEAD ${Math.abs(k.now-k.plan)} PTS` : `EARLY ${Math.abs(k.now-k.plan)} MIN`; return k.unit==="%" ? `LATE ${Math.abs(k.now-k.plan)} PTS` : `DELAYED ${Math.abs(k.now-k.plan)} MIN`; };
    const cls = k => k.state==="ahead"?"ok":k.state==="watch"?"warn":"bad";
    const arr = k => `<button class="row" type="button" data-ref="kpi:${k.id}"><span class="c1 dst">${esc(k.name)}<small>${k.id} · ${STATE_WORD[k.state]}</small></span><span class="c2"><span class="lab">FROM</span><span class="num dim">${fmtv(k,k.base)}</span></span><span class="c3"><span class="lab">DUE NOW</span><span class="num dim">${fmtv(k,k.plan)}</span></span><span class="c4"><span class="lab">ARRIVED</span><span class="num ${cls(k)}">${fmtv(k,k.now)}</span></span><span class="c5"><span class="lab">FINAL</span><span class="num dim">${fmtv(k,k.target)}</span></span><span class="c6 rm ${cls(k)} ${k.state==="off"?"blink":""}">${flap(rem(k))}</span></button>`;
    const pstat = p => p.state==="ahead" ? ["ON TIME","ok"] : p.state==="watch" ? ["SLIPPING","warn"] : ["DELAYED","bad"];
    const crw = p => { const st = pstat(p); const sub = UI.view==="day" ? `<span class="tdy">Today: ${p.today.map(t=>(t[1]===1?"✓ ":String(t[1]).startsWith("late")?"! ":"○ ")+esc(t[0])).join(" · ")}</span>` : (p.impact ? `<span class="imp">${esc(p.impact)}</span>` : `<span class="tdy">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`);
      return `<button class="row" type="button" data-ref="per:${p.key}"><span class="c1 dst">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="c2 dst" style="font-weight:400;font-size:12.5px">${sub}</span><span class="c3 num">${p.today.filter(t=>t[1]===1).length}/${p.today.length}</span><span class="c4 num">${p.done}/${p.due}</span><span class="c5 rm ${st[1]}">${flap(st[0])}</span></button>`; };
    const mt = D.months.map((m,i)=>sum(D.spend.map(s=>s.v[i])));
    const alerts = D.watch.map(w=>`<button type="button" data-ref="${w.ref}"><b>▲</b> ${esc(w.t)} · ${esc(P[w.who].name)}</button>`).join("");
    /* runway: cumulative back vs out, small */
    const rw = (()=>{ const n = D.cumMonths.length; let s = ""; D.cumMonths.forEach((m,i)=>{ const x = 4 + i*(992/n); const ok = D.cumFore[i] >= D.cumSpend[i]; const fore = i > D.actualTo;
      s += `<g data-ref="month:${i}" data-nopen><rect x="${x}" y="8" width="${992/n-6}" height="18" rx="2" fill="${ok?"#39D98A":fore?"#24282C":"#3A3F45"}" ${fore&&!ok?'stroke="#555" stroke-dasharray="3 2"':""}/><text x="${x+(992/n-6)/2}" y="40" text-anchor="middle" font-size="11" fill="#A3A9AF">${m}</text></g>`; });
      return `<svg viewBox="0 0 1000 46" preserveAspectRatio="none" role="img" aria-label="Months until EBITDA back passes money out: green from February">${s}<line x1="${4+5*(992/n)}" x2="${4+5*(992/n)}" y1="2" y2="30" stroke="#FFD21F" stroke-width="2" stroke-dasharray="3 2"/></svg>`; })();
    return `<div class="s4">
      <nav class="way" aria-label="Suite sections">${TABS.map((t,i)=>`<button class="ws ${i?"":"on"}" type="button" data-tab="${t[0]}"><i aria-hidden="true">${["⌂","⇄","↗","☰","₹","▤","✉"][i]}</i>${t[1]}</button>`).join("")}</nav>
      <div class="wrap">
        <div class="hero"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
          <div class="clk"><b id="s4clock">10:40</b><small>MON 12 OCT · BOARD UPDATED 10:40 AM · WEEK ${D.week} OF ${D.weeksPlanned}</small></div></div>
        <div class="counters" aria-label="Pulse strip">
          <button class="cnt" type="button" data-tab="links"><span>PARTS DEPARTED</span>${flap(`${String(countParts("live")).padStart(2,"0")}/12`,"ok")}<em>Plan for this week: 06</em></button>
          <button class="cnt" type="button" data-tab="measures"><span>KPIs ARRIVING ON TIME</span>${flap(`${onCourse}/9`,"warn")}<em>Plan for this week: 8</em></button>
          <button class="cnt" type="button" data-ref="health:0"><span>OUT · EBITDA BACK, ₹ LAKH</span>${flap(`${spendTotal.toFixed(1)} ${ebitdaTotal.toFixed(1)}`)}<em>Plan: 14.7 out · 7.5 back</em></button>
          <button class="cnt" type="button" data-ref="health:0"><span>BREAK-EVEN ARRIVES</span>${flap("FEB 27","bad")}<em>Scheduled Jan 27 · 4 weeks late</em></button>
        </div>
        <div class="ticker"><b>SERVICE ALERTS</b><div class="tk"><div class="run">${alerts}${alerts.replace(/<button /g,'<button tabindex="-1" aria-hidden="true" ')}</div></div></div>
        <button class="next" type="button" data-ref="part:${D.milestone.part}"><span><b>NEXT DEPARTURE</b>${esc(D.milestone.what)} · ${D.milestone.date}</span>${flap(`BOARDING IN 0${D.milestone.days} DAYS`,"ok")}</button>

        <section class="board dep" data-zone="links"><div class="bh"><h3><i>⇄</i>DEPARTURES · INTEGRATIONS</h3><p>${countParts("live")} departed · ${countParts("testing")} boarding · ${countParts("building")} on schedule · 1 delayed · ${countParts("notstarted")} scheduled</p></div>
          <div class="cols"><span>GO-LIVE</span><span>PART</span><span>VIA</span><span>GATE</span><span>REMARKS</span></div>
          ${D.parts.map(dep).join("")}
          <div class="hand">Connecting services to the <b>Billing & Insurance</b> suite: ${D.handoffs.map(h=>esc(h.name)+" ("+esc(h.when)+")").join(" · ")}</div></section>

        <section class="board arr" data-zone="measures"><div class="bh"><h3><i>↗</i>ARRIVALS · KPIs</h3><p>Due now is where the plan says we should be in week ${D.week}</p></div>
          <div class="cols"><span>MEASURE</span><span>FROM</span><span>DUE NOW</span><span>ARRIVED</span><span>FINAL</span><span>REMARKS</span></div>
          ${D.kpis.map(arr).join("")}</section>

        <section class="board crw" data-zone="team"><div class="bh"><h3><i>☰</i>CREW ROSTER · TASKBOARDS</h3>${viewToggle("vt")}</div>
          <div class="cols"><span>CREW</span><span>${UI.view==="day"?"TODAY'S TASKS":"WHAT IT COSTS / NEXT"}</span><span>TODAY</span><span>WEEK</span><span>STATUS</span></div>
          ${D.people.map(crw).join("")}</section>

        <section class="board" data-zone="health"><div class="bh"><h3><i>₹</i>FARES · PROJECT STATUS</h3><p>₹ lakh</p></div>
          <div class="fare"><div>
            <div class="mrow" style="color:var(--mute);font-size:10.5px;letter-spacing:.12em;font-weight:600"><span>MONTH</span><span>OUT</span><span>REVENUE</span><span>EBITDA</span></div>
            ${D.months.map((m,i)=>`<div class="mrow"><button type="button" data-ref="month:${i}" class="num" style="color:var(--yel)">${m.toUpperCase()}</button><span class="num">${mt[i].toFixed(2)}</span><span class="num">${D.revenue[i].toFixed(1)}</span><span class="num ok">${D.ebitda[i].toFixed(1)}</span></div>`).join("")}
            <div class="mrow"><span style="font-weight:600;color:var(--txt)">TOTAL</span><span class="num">${spendTotal.toFixed(2)}</span><span class="num">${revTotal.toFixed(1)}</span><span class="num ok">${ebitdaTotal.toFixed(1)}</span></div>
            <p style="font-size:12px;color:var(--mute);margin:10px 0 0">Each month: subscription ₹2.4 lakh · salaries of the three roles we recommended ₹0.92 lakh. One-time so far ₹8.2 lakh, of which the ₹2.5 lakh imaging fee was not in plan.</p>
          </div><div class="sched">
            <button type="button" data-ref="health:0"><small>SCHEDULED</small>${flap("JAN 2027","dim")}</button>
            <button type="button" data-ref="health:0"><small>EXPECTED</small>${flap("FEB 2027","warn")}</button>
            <button type="button" data-ref="health:0"><small>REMARKS</small>${flap("DELAYED 4 WK","bad blink")}</button>
            <button type="button" data-ref="health:0"><small>FULL RUN EBITDA</small>${flap("6.3/MO","ok")}</button>
            <div class="runway">${rw}</div>
          </div></div></section>
      </div></div>`;
  },
  after(){
    const c = document.getElementById("s4clock"); const tick = () => { if (!c.isConnected) return clearInterval(t); c.textContent = new Date().toLocaleTimeString("en-IN",{hour:"2-digit",minute:"2-digit",hour12:false}); }; const t = setInterval(tick, 15000); tick();
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const A = "ABCDEFGHIJKLMNOPRSTUVWXYZ0123456789";
    document.querySelectorAll(".s4 .rm .fc:not(.sp), .s4 .cnt .fc:not(.sp)").forEach((el,i) => { const real = el.textContent; let n = 4 + (i % 7); const iv = setInterval(() => { if (--n <= 0) { el.textContent = real; clearInterval(iv); } else el.textContent = A[Math.floor(Math.random()*A.length)]; }, 70); });
  }
});
