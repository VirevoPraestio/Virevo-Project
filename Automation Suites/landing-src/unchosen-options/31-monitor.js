/* ===== Scheme A: the bedside monitor ===== */
SCHEMES.push({
  key:"monitor", letter:"A", name:"Bedside monitor",
  note:"<b>A · Bedside monitor.</b> The suite is a patient on a monitor. KPIs run as live traces against a dashed plan line, the twelve links are leads with their own rhythm, the team is telemetry, and money is a crossing trace. Navigation lives on hardware keys along the bezel. Dark, phosphor colours.",
  vars:{ "--sh-bg":"#0B1114","--sh-fg":"#E6F2EE","--sh-mute":"#93ABA3","--sh-line":"#21343A","--sh-card":"#101A1E","--c-ok":"#3BE58A","--c-warn":"#FFC447","--c-bad":"#FF6464","--pk-bg":"#03080A","--pk-fg":"#E6F2EE","--pk-line":"#2BE08A55","--pk-r":"6px","--sh-r":"16px" },
  fab:96,
  css:`
.s1{--bg:#0D1013;--bez:#262B31;--bez2:#1A1E22;--scr:#03080A;--grid:#0C2620;--fg:#E6F2EE;--mute:#8FA9A0;--ok:#3BE58A;--warn:#FFC447;--bad:#FF6464;--cyan:#55D6FF;
  background:radial-gradient(1200px 600px at 50% -10%,#1D252B 0%,var(--bg) 60%);color:var(--fg);padding:22px 16px 0;min-height:100vh}
.s1 .mon{max-width:1240px;margin:0 auto;background:linear-gradient(180deg,#30363D,var(--bez) 30%,var(--bez2));border-radius:30px;padding:18px 18px 0;
  box-shadow:0 1px 0 #4A525B inset,0 -2px 0 #111 inset,0 40px 80px rgba(0,0,0,.55),0 8px 0 #121518}
.s1 .brand{display:flex;justify-content:space-between;align-items:center;padding:0 8px 10px;font-size:11px;letter-spacing:.2em;color:#8E989F;font-weight:600}
.s1 .brand i{width:9px;height:9px;border-radius:50%;background:var(--ok);display:inline-block;box-shadow:0 0 10px var(--ok);margin-right:8px;vertical-align:middle}
.s1 .scr{background:var(--scr);border-radius:14px;padding:16px;position:relative;overflow:hidden;
  box-shadow:inset 0 0 0 2px #0A0F11,inset 0 0 60px rgba(59,229,138,.06);
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:24px 24px;background-position:-1px -1px}
.s1 .scr::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,.035),transparent 25%);pointer-events:none}
.s1 .top{display:flex;flex-wrap:wrap;gap:12px 22px;align-items:flex-end;justify-content:space-between;border-bottom:1px solid #12312A;padding-bottom:12px}
.s1 .top h2{font-family:var(--f-num);font-weight:400;font-size:52px;line-height:.9;margin:0;letter-spacing:.02em}
.s1 .top h2 small{display:block;font-family:var(--f-body);font-size:12px;letter-spacing:.16em;color:var(--mute);font-weight:600;margin-bottom:6px}
.s1 .beds{display:flex;flex-wrap:wrap;gap:6px}
.s1 .beds span{font-size:11px;border:1px solid #1E3B33;border-radius:4px;padding:3px 7px;color:var(--mute)}
.s1 .beds span.on{border-color:var(--ok);color:var(--ok)}
.s1 .clock{text-align:right;font-variant-numeric:tabular-nums}
.s1 .clock b{font-family:var(--f-num);font-weight:400;font-size:40px;line-height:1;color:var(--cyan);letter-spacing:.04em}
.s1 .clock small{display:block;font-size:11px;color:var(--mute);letter-spacing:.08em}
.s1 .alarms{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px}
.s1 .alarm{display:flex;align-items:center;gap:8px;background:#1A0A0B;border:1px solid #5A1E22;color:#FFB3B3;border-radius:6px;padding:7px 11px;font-size:12.5px;font-weight:500;text-align:left;min-height:40px}
.s1 .alarm:nth-child(2){background:#1A1405;border-color:#5C4612;color:#FFE1A0}
.s1 .alarm .tri{width:0;height:0;border-left:7px solid transparent;border-right:7px solid transparent;border-bottom:12px solid currentColor;animation:s1blink 1.2s steps(2) infinite}
.s1 .alarm em{font-style:normal;opacity:.7;font-size:11.5px}
@keyframes s1blink{50%{opacity:.15}}
.s1 .grid{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:16px;margin-top:12px}
.s1 .zh{display:flex;justify-content:space-between;align-items:baseline;margin:0 0 8px;font-size:11.5px;letter-spacing:.14em;color:var(--mute);font-weight:600;text-transform:uppercase}
.s1 .zh b{color:var(--fg)}
.s1 .ch{display:grid;grid-template-columns:150px minmax(0,1fr) 112px;gap:10px;align-items:center;width:100%;background:transparent;border:0;border-bottom:1px solid #0F2721;padding:6px 0;text-align:left;color:inherit;min-height:52px}
.s1 .ch:hover,.s1 .ch:focus-visible{background:rgba(85,214,255,.05)}
.s1 .ch .nm{font-size:12.5px;font-weight:600;line-height:1.25}
.s1 .ch .nm small{display:block;font-weight:400;color:var(--mute);font-size:11px}
.s1 .ch svg{width:100%;height:44px;display:block;overflow:visible}
.s1 .ch .v{text-align:right;font-variant-numeric:tabular-nums}
.s1 .ch .v b{font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1;letter-spacing:.02em}
.s1 .ch .v small{display:block;font-size:10.5px;letter-spacing:.06em;font-weight:600}
.s1 .ahead{color:var(--ok)} .s1 .watch{color:var(--warn)} .s1 .off{color:var(--bad)}
.s1 .sweep{animation:s1sweep 4s linear infinite}
@keyframes s1sweep{from{transform:translateX(-30px)}to{transform:translateX(330px)}}
.s1 .vit{display:grid;gap:10px}
.s1 .vbox{border:1px solid #173A31;border-radius:8px;padding:10px 12px;text-align:left;background:rgba(0,0,0,.25);color:inherit;width:100%}
.s1 .vbox span{display:flex;justify-content:space-between;font-size:11px;letter-spacing:.12em;font-weight:600}
.s1 .vbox b{display:block;font-family:var(--f-num);font-weight:400;font-size:46px;line-height:1;letter-spacing:.02em;font-variant-numeric:tabular-nums}
.s1 .vbox b sub{font-size:22px;vertical-align:baseline;color:var(--mute);margin-left:3px}
.s1 .vbox small{display:block;color:var(--mute);font-size:11.5px}
.s1 .vbox .gh{color:var(--cyan)}
.s1 .count{border:1px dashed var(--cyan);border-radius:8px;padding:10px 12px;color:var(--cyan)}
.s1 .count b{font-family:var(--f-num);font-weight:400;font-size:38px;line-height:1}
.s1 .count small{display:block;font-size:11.5px;color:var(--fg)}
.s1 .zone{margin-top:18px;border-top:1px solid #12312A;padding-top:12px;border-radius:6px}
.s1 .leads{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px}
.s1 .lead{border:1px solid #163128;border-radius:6px;padding:7px 8px;background:rgba(0,0,0,.3);text-align:left;color:inherit;min-height:92px;display:flex;flex-direction:column;gap:3px}
.s1 .lead .id{display:flex;justify-content:space-between;font-family:var(--f-num);font-size:18px;line-height:1;letter-spacing:.04em}
.s1 .lead .id em{font-style:normal;font-family:var(--f-body);font-size:10.5px;font-weight:600;letter-spacing:.05em}
.s1 .lead .nm{font-size:11.5px;line-height:1.25;color:var(--fg)}
.s1 .lead svg{width:100%;height:20px;margin-top:auto}
.s1 .lead .fr{font-size:10.5px;color:var(--mute)}
.s1 .lead.blocked{border-color:#5A1E22}
.s1 .hand{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;font-size:12px;color:var(--mute)}
.s1 .hand span{border:1px dashed #36514A;border-radius:4px;padding:3px 8px}
.s1 .two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}
.s1 .keysw{display:inline-flex;border:1px solid #1E3B33;border-radius:6px;overflow:hidden}
.s1 .keysw button{background:transparent;border:0;color:var(--mute);font-size:11px;padding:6px 10px;letter-spacing:.08em;font-weight:600;min-height:32px}
.s1 .keysw button[aria-pressed="true"]{background:#0F2C24;color:var(--ok)}
.s1 .tel{display:grid;grid-template-columns:34px minmax(0,1fr) 60px;gap:10px;align-items:center;width:100%;text-align:left;background:transparent;border:0;border-bottom:1px solid #0F2721;color:inherit;padding:7px 0;min-height:48px}
.s1 .tel .av{width:34px;height:34px;border-radius:50%;border:1.5px solid currentColor;display:grid;place-items:center;font-size:11px;font-weight:700}
.s1 .tel .nm{font-size:12.5px;font-weight:600;line-height:1.2}
.s1 .tel .nm small{font-weight:400;color:var(--mute);font-size:11px}
.s1 .tel .bar{display:block;height:6px;background:#0F2721;border-radius:3px;margin-top:5px;position:relative;overflow:hidden}
.s1 .tel .bar i{position:absolute;left:0;top:0;bottom:0;background:currentColor;border-radius:3px}
.s1 .tel .tk{font-size:11.5px;color:var(--fg);margin-top:3px;display:flex;flex-wrap:wrap;gap:4px 10px}
.s1 .tel .tk .y{color:var(--ok)} .s1 .tel .tk .l{color:var(--bad)} .s1 .tel .tk .p{color:var(--mute)}
.s1 .tel .pc{text-align:right;font-family:var(--f-num);font-size:28px;line-height:1}
.s1 .tel .pc small{display:block;font-family:var(--f-body);font-size:10px;letter-spacing:.06em;font-weight:600}
.s1 .be svg{width:100%;height:auto;display:block}
.s1 .be .reads{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:10px}
.s1 .be .reads div{border:1px solid #163128;border-radius:6px;padding:6px 9px;font-size:11.5px;color:var(--mute)}
.s1 .be .reads b{display:block;font-family:var(--f-num);font-weight:400;font-size:22px;color:var(--fg);line-height:1.1}
.s1 .bezel{position:sticky;bottom:0;z-index:5;margin:14px -18px 0;padding:10px 18px calc(12px + env(safe-area-inset-bottom,0px));background:linear-gradient(180deg,var(--bez),#1B1F23);border-radius:0 0 30px 30px;display:flex;gap:10px;overflow-x:auto;scrollbar-width:none}
.s1 .key{flex:1 0 96px;display:flex;flex-direction:column;align-items:center;gap:6px;background:transparent;border:0;color:#AEB7BD;font-size:11px;letter-spacing:.1em;font-weight:600;text-transform:uppercase;min-height:56px}
.s1 .key i{width:100%;height:24px;border-radius:7px;background:linear-gradient(180deg,#3B424A,#2A3036);box-shadow:0 3px 0 #111,0 1px 0 #5A636C inset;position:relative}
.s1 .key i::after{content:"";position:absolute;top:8px;left:50%;width:8px;height:8px;margin-left:-4px;border-radius:50%;background:#1A1E22}
.s1 .key.on{color:var(--ok)} .s1 .key.on i::after{background:var(--ok);box-shadow:0 0 8px var(--ok)}
.s1 .key:active i{transform:translateY(2px);box-shadow:0 1px 0 #111}
.s1 .foot{height:24px}
@media (max-width:980px){ .s1 .grid{grid-template-columns:1fr} .s1 .vit{order:-1} .s1 .vit{grid-template-columns:repeat(2,minmax(0,1fr))} .s1 .two{grid-template-columns:1fr} .s1 .leads{grid-template-columns:repeat(4,minmax(0,1fr))} }
@media (max-width:600px){ .s1{padding:12px 10px 0} .s1 .mon{padding:12px 10px 0;border-radius:22px} .s1 .scr{padding:12px} .s1 .top h2{font-size:40px}
  .s1 .ch{grid-template-columns:minmax(0,1fr) 92px;grid-template-areas:"n v" "t t"} .s1 .ch .nm{grid-area:n} .s1 .ch .v{grid-area:v} .s1 .ch svg{grid-area:t}
  .s1 .leads{grid-template-columns:repeat(2,minmax(0,1fr))} .s1 .vbox b{font-size:36px} .s1 .bezel{margin:12px -10px 0} .s1 .key{flex:0 0 76px} }
`,
  render(){
    const W = 300, H = 40;
    const chan = k => {
      const xs = w => (w/D.weeksPlanned)*W, ys = p => H - p*H*0.86 - 3;
      const pts = weekly(k).map((v,w)=>`${xs(w).toFixed(1)},${ys(prog(k,v)).toFixed(1)}`).join(" ");
      return `<button class="ch" type="button" data-ref="kpi:${k.id}" aria-label="${esc(k.name)}: ${fmtv(k,k.now)}, ${STATE_WORD[k.state]}">
        <span class="nm">${esc(k.short)}<small>${fmtv(k,k.base)} → ${fmtv(k,k.target)}</small></span>
        <svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true">
          <line x1="0" x2="${W}" y1="${ys(1)}" y2="${ys(1)}" stroke="#E6F2EE" stroke-opacity=".25" stroke-dasharray="1 4"/>
          <line x1="0" y1="${ys(0)}" x2="${W}" y2="${ys(1)}" stroke="#55D6FF" stroke-opacity=".55" stroke-dasharray="4 4" fill="none"/>
          <circle cx="${xs(D.week)}" cy="${ys(prog(k,k.plan))}" r="3" fill="none" stroke="#55D6FF"/>
          <polyline points="${pts}" fill="none" stroke="currentColor" class="${k.state}" stroke-width="2" style="filter:drop-shadow(0 0 3px currentColor)"/>
          <circle cx="${xs(D.week)}" cy="${ys(prog(k,k.now))}" r="3.5" class="${k.state}" fill="currentColor"/>
          <rect class="sweep" x="0" y="0" width="22" height="${H}" fill="#03080A" opacity=".85"/>
        </svg>
        <span class="v ${k.state}"><b>${fmtv(k,k.now)}</b><small>${STATE_WORD[k.state].toUpperCase()}</small></span></button>`;
    };
    const beat = st => {
      if (st==="live") return `<polyline points="0,12 12,12 15,4 18,18 21,12 34,12 46,12 49,4 52,18 55,12 68,12 80,12 83,4 86,18 89,12 100,12" fill="none" stroke="#3BE58A" stroke-width="1.6"/>`;
      if (st==="testing") return `<polyline points="0,12 10,12 13,7 16,15 19,12 34,12 40,9 44,14 60,12 66,6 70,16 74,12 100,12" fill="none" stroke="#FFC447" stroke-width="1.6"/>`;
      if (st==="building") return `<polyline points="0,12 100,12" fill="none" stroke="#8FA9A0" stroke-width="1.4" stroke-dasharray="3 3"/>`;
      if (st==="blocked") return `<polyline points="0,12 100,12" fill="none" stroke="#FF6464" stroke-width="1.8"/>`;
      return `<polyline points="0,12 100,12" fill="none" stroke="#2C4740" stroke-width="1.2"/>`;
    };
    const lead = x => `<button class="lead ${x.st}" type="button" data-ref="part:${x.id}"><span class="id">L${x.id}<em class="${x.st==="live"?"ahead":x.st==="blocked"?"off":x.st==="testing"?"watch":""}" style="${x.st==="building"||x.st==="notstarted"?"color:#8FA9A0":""}">${PART_WORD[x.st].toUpperCase()}</em></span><span class="nm">${esc(x.name)}</span><svg viewBox="0 0 100 24" preserveAspectRatio="none" aria-hidden="true">${beat(x.st)}</svg><span class="fr">${esc(x.fresh)}</span></button>`;
    const tel = p => {
      const pc = Math.round(p.done/p.due*100);
      const tasks = UI.view==="day" ? `<span class="tk">${p.today.map(t=>t[1]===1?`<span class="y">✓ ${esc(t[0])}</span>`:String(t[1]).startsWith("late")?`<span class="l">! ${esc(t[0])}</span>`:`<span class="p">○ ${esc(t[0])}</span>`).join("")}</span>`
        : `<span class="bar"><i style="width:${pc}%"></i></span>`;
      return `<button class="tel ${p.state}" type="button" data-ref="per:${p.key}"><span class="av">${initials(p.name)}</span><span style="min-width:0"><span class="nm">${esc(p.name)} <small>· ${esc(p.role)}</small></span>${tasks}</span><span class="pc">${UI.view==="day"?p.today.filter(t=>t[1]===1).length+"/"+p.today.length:pc}<small>${UI.view==="day"?"TODAY":"% DONE"}</small></span></button>`;
    };
    /* break-even trace */
    const BW=600, BH=190, x0=34, x1=590, y0=14, y1=160, vmax=65;
    const bx = i => x0 + (x1-x0)*i/(D.cumMonths.length-1), by = v => y1 - (y1-y0)*v/vmax;
    const pth = (a,from,to) => a.slice(from,to+1).map((v,j)=>(j?"L":"M")+bx(from+j).toFixed(1)+","+by(v).toFixed(1)).join(" ");
    const be = `<svg viewBox="0 0 ${BW} ${BH}" role="img" aria-label="Money out against EBITDA back, August to May. Plan crosses in January, forecast crosses in February.">
      ${[0,20,40,60].map(v=>`<line x1="${x0}" x2="${x1}" y1="${by(v)}" y2="${by(v)}" stroke="#12312A"/><text x="${x0-6}" y="${by(v)+4}" fill="#8FA9A0" font-size="10" text-anchor="end">${v}</text>`).join("")}
      ${D.cumMonths.map((m,i)=>`<text x="${bx(i)}" y="${BH-12}" fill="#8FA9A0" font-size="10" text-anchor="middle">${m}</text>`).join("")}
      <line x1="${bx(5)}" x2="${bx(5)}" y1="${y0}" y2="${y1}" stroke="#55D6FF" stroke-dasharray="3 3" opacity=".7"/><text x="${bx(5)-4}" y="${y0+8}" fill="#55D6FF" font-size="10" text-anchor="end">plan: Jan</text>
      <line x1="${bx(6)}" x2="${bx(6)}" y1="${y0}" y2="${y1}" stroke="#FFC447" stroke-dasharray="3 3"/><text x="${bx(6)+4}" y="${y0+8}" fill="#FFC447" font-size="10">forecast: Feb</text>
      <path d="${pth(D.cumPlan,0,9)}" fill="none" stroke="#55D6FF" stroke-opacity=".6" stroke-dasharray="5 4"/>
      <path d="${pth(D.cumSpend,0,9)}" fill="none" stroke="#E6F2EE" stroke-width="2"/>
      <path d="${pth(D.cumFore,0,D.actualTo)}" fill="none" stroke="#3BE58A" stroke-width="2.5" style="filter:drop-shadow(0 0 3px #3BE58A)"/>
      <path d="${pth(D.cumFore,D.actualTo,9)}" fill="none" stroke="#3BE58A" stroke-width="2" stroke-dasharray="2 4"/>
      <circle cx="${bx(6)}" cy="${by(31)}" r="5" fill="none" stroke="#FFC447" stroke-width="2"/>
      <text x="${bx(9)}" y="${by(41)+14}" fill="#E6F2EE" font-size="10" text-anchor="end">money out</text>
      <text x="${bx(9)-4}" y="${by(57.2)-6}" fill="#3BE58A" font-size="10" text-anchor="end">EBITDA back</text>
      ${D.cumMonths.map((m,i)=>`<rect data-ref="month:${i}" data-nopen x="${bx(i)-20}" y="${y0}" width="40" height="${y1-y0}" fill="transparent"/>`).join("")}
    </svg>`;
    const vit = `
      <button class="vbox" type="button" data-tab="links"><span>PARTS LIVE<em class="ahead">● ${countParts("testing")} TESTING</em></span><b class="ahead">${countParts("live")}<sub>/12</sub></b><small class="gh">plan for week ${D.week}: 6 live</small></button>
      <button class="vbox" type="button" data-tab="measures"><span>KPIs ON COURSE<em class="off">● ${D.kpis.filter(k=>k.state==="off").length} OFF</em></span><b class="watch">${onCourse}<sub>/9</sub></b><small class="gh">plan for week ${D.week}: 8 of 9</small></button>
      <button class="vbox" type="button" data-ref="health:0"><span>MONEY OUT · EBITDA BACK<em>₹ LAKH</em></span><b>${spendTotal.toFixed(1)}<sub>out</sub> <span class="ahead" style="display:inline;font:inherit">${ebitdaTotal.toFixed(1)}</span><sub>back</sub></b><small class="gh">plan: out 14.7 · back 7.5</small></button>
      <button class="vbox" type="button" data-ref="health:0"><span>BREAK-EVEN<em class="watch">+4 WK</em></span><b class="watch">FEB 27</b><small class="gh">plan: Jan 27</small></button>
      <div class="count" aria-label="Next go-live in ${D.milestone.days} days"><span style="font-size:11px;letter-spacing:.12em;font-weight:600">NEXT GO-LIVE</span><br><b>0${D.milestone.days} DAYS</b><small>${esc(D.milestone.what)} · ${D.milestone.date}</small></div>`;
    return `<div class="s1"><div class="mon">
      <div class="brand"><span><i></i>VIREVO · SUITE MONITOR</span><span>${esc(D.hospital.toUpperCase())}</span></div>
      <div class="scr">
        <div class="top">
          <h2><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())}</small>${esc(D.suite.toUpperCase())}</h2>
          <div class="beds" aria-label="Other suites">${D.siblings.map((s,i)=>`<span class="${i?"":"on"}">${i+1} · ${esc(s)}</span>`).join("")}</div>
          <div class="clock"><b id="s1clock">10:40</b><small>DATA ${esc(D.asOf.toUpperCase())} · WEEK ${D.week}/${D.weeksPlanned}</small></div>
        </div>
        <div class="alarms" aria-label="Watch list">${D.watch.map(w=>`<button class="alarm" type="button" data-ref="${w.ref.startsWith("part")?w.ref:w.ref}"><i class="tri" aria-hidden="true"></i>${esc(w.t)} <em>· ${esc(P[w.who].name)}</em></button>`).join("")}</div>
        <div class="grid">
          <section data-zone="measures" style="min-width:0"><div class="zh"><span>KPIs · trace against <b style="color:var(--cyan)">- - plan</b></span><span>start → target</span></div>${D.kpis.map(chan).join("")}</section>
          <aside class="vit" aria-label="Pulse strip">${vit}</aside>
        </div>
        <section class="zone" data-zone="links"><div class="zh"><span>Integrations · 12 leads</span><span><b>${countParts("live")}</b> live · <b>${countParts("testing")}</b> testing · <b>${countParts("building")+countParts("blocked")}</b> building · <b>${countParts("notstarted")}</b> not started</span></div>
          <div class="leads">${D.parts.map(lead).join("")}</div>
          <div class="hand">Hand-offs to the Billing & Insurance suite: ${D.handoffs.map(h=>`<span>${esc(h.name)} · ${esc(h.when)}</span>`).join("")}</div></section>
        <div class="two">
          <section class="zone" data-zone="team"><div class="zh"><span>Taskboards · staff telemetry</span>${viewToggle("keysw")}</div>${D.people.map(tel).join("")}</section>
          <section class="zone be" data-zone="health"><div class="zh"><span>Project Status · ₹ lakh, cumulative</span><button type="button" class="keysw" data-ref="health:0" style="padding:5px 9px;color:var(--warn);font-size:11px;letter-spacing:.08em;font-weight:600;background:transparent">WHY +4 WK ›</button></div>${be}
            <div class="reads"><div>Subscription<b>₹2.4 lakh / month</b></div><div>Salaries, roles we recommended<b>₹0.92 lakh / month</b></div><div>One-time so far<b>₹8.2 lakh</b></div><div>EBITDA now → full run<b>₹3.9 → ₹6.3 lakh / month</b></div></div></section>
        </div>
        <div class="foot"></div>
      </div>
      <nav class="bezel" aria-label="Suite sections">${TABS.map(t=>`<button class="key ${t[0]==="overview"?"on":""}" type="button" data-tab="${t[0]}"><i></i>${t[1]}</button>`).join("")}</nav>
    </div><div style="height:30px"></div></div>`;
  },
  after(){ const c = document.getElementById("s1clock"); const tick = () => { if (!c.isConnected) return clearInterval(t); const d = new Date(); c.textContent = d.toLocaleTimeString("en-IN",{hour:"2-digit",minute:"2-digit",hour12:false}); }; const t = setInterval(tick, 15000); tick(); }
});
