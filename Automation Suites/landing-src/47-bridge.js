/* ===== Financial Health, option 3: graphite and lime, expected EBITDA stepped to actual EBITDA, one step per cause ===== */
SCHEMES.push({
  key:"bridge", letter:"3", name:"Graphite and lime",
  note:"<b>Option 3 · graphite and lime.</b> Expected EBITDA on the left, actual on the right, and one step for each cause in between, so the size of every loss and gain reads at a glance. Switch between the last closed day and the total since the start. The feeds sit underneath.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#1E2226","--sh-mute":"#5D646C","--sh-line":"#DDE0DA","--sh-card":"#F5F6F2","--c-ok":"#3E7F12","--c-warn":"#A86B05","--c-bad":"#C8342B","--pk-bg":"#1E2226","--pk-fg":"#FFFFFF","--pk-line":"#B7D433","--pk-r":"6px","--sh-r":"10px" },
  fab:18,
  blocks:{ nav:".keys", pulse:".odo", watch:".tix", countdown:".donut", hero:"[data-zone=links]", kpis:".bullets", recovery:"[data-zone=recovery]", team:".rings", money:".steps" },
  css:`
.s17{--bg:#F2F3EF;--ink:#1E2226;--mute:#5D646C;--gr:#2B3036;--lime:#B7D433;--limed:#4F6B00;--lime2:#EEF5D0;--ok:#3E7F12;--warn:#A86B05;--bad:#C8342B;--line:#DDE0DA;
  background:var(--bg);color:var(--ink);padding:18px 16px 90px;overflow-x:clip}
.s17 .wrap{max-width:1240px;margin:0 auto}
.s17 .frz{position:sticky;top:0;z-index:30;background:var(--bg);margin:-18px -16px 18px;padding:14px 16px 12px;transition:box-shadow .2s}
.s17 .frz.mini{box-shadow:0 10px 22px rgba(30,34,38,.13);border-bottom:3px solid var(--lime);padding:8px 16px 8px}
.s17 .frz.mini .ky{padding:5px 11px;min-height:34px;font-size:12px;box-shadow:0 2px 0 #C9CDC4}
.s17 .frz.mini .ky.on{box-shadow:0 2px 0 #111}
.s17 .frz.mini .head{margin:8px 0;grid-template-columns:auto minmax(0,1fr);align-items:center;gap:14px}
.s17 .frz.mini .head small,.s17 .frz.mini .head p{display:none}
.s17 .frz.mini h2{font-size:34px;white-space:nowrap} .s17 .frz.mini h2::before{width:8px;height:24px;margin-right:8px}
.s17 .frz.mini .odo{padding:5px;gap:5px;justify-self:end}
.s17 .frz.mini .od{padding:3px 10px;min-width:0} .s17 .frz.mini .od b{font-size:20px} .s17 .frz.mini .od span{font-size:9px} .s17 .frz.mini .od em{display:none}
.s17 .frz.mini .tix{margin-bottom:0;gap:8px}
.s17 .frz.mini .tk{padding:5px 12px 5px 16px;font-size:12px} .s17 .frz.mini .tk b{font-size:17px} .s17 .frz.mini .tk small{display:none}
.s17 .frz.mini .tk>span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.s17 .frz.mini .tk::before,.s17 .frz.mini .tk::after{width:10px;height:10px;margin-top:-5px}
.s17 .frz.mini .donut{grid-template-columns:34px minmax(0,1fr);padding:4px 10px} .s17 .frz.mini .donut svg{width:34px;height:34px} .s17 .frz.mini .donut small{display:none}
.s17 .keys{display:flex;flex-wrap:wrap;gap:8px}
.s17 .ky{border:1px solid #C9CDC4;background:linear-gradient(#FFFFFF,#ECEEE8);border-radius:8px;padding:9px 14px;font-size:12.5px;font-weight:600;color:var(--ink);min-height:44px;box-shadow:0 3px 0 #C9CDC4;transition:transform .08s,box-shadow .08s}
.s17 .ky:active{transform:translateY(2px);box-shadow:0 1px 0 #C9CDC4}
.s17 .ky.on{background:var(--gr);color:var(--lime);border-color:var(--gr);box-shadow:0 3px 0 #111,0 0 0 3px rgba(183,212,51,.35)}
.s17 .ky em{font-style:normal;background:var(--lime);color:var(--gr);border-radius:4px;padding:0 6px;margin-left:6px;font-size:11px;font-weight:700}
.s17 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:24px 0 16px}
.s17 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--limed)}
.s17 h2{font-family:var(--f-num);font-weight:400;font-size:78px;line-height:.88;margin:4px 0 0}
.s17 h2::before{content:"";display:inline-block;width:14px;height:56px;background:var(--lime);margin-right:12px;vertical-align:-2px;border-radius:3px}
.s17 .head p{margin:8px 0 0;font-size:13px;color:var(--mute)}
.s17 .odo{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;background:var(--gr);border-radius:12px;padding:8px}
.s17 .od{border:0;background:#353B42;border-radius:8px;padding:8px 12px;text-align:left;color:#fff;min-width:130px}
.s17 .od:hover{background:#3F464E}
.s17 .od span{display:block;font-size:10px;letter-spacing:.12em;font-weight:700;color:#AEB5BC}
.s17 .od b{display:block;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1.05;color:var(--lime);letter-spacing:.04em}
.s17 .od em{font-style:normal;font-size:11px;color:#D5DAD0}
.s17 .tix{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.8fr);gap:12px;margin-bottom:16px}
.s17 .tk{position:relative;display:grid;grid-template-columns:auto minmax(0,1fr);gap:10px;align-items:center;background:#fff;border:0;border-radius:10px;padding:10px 14px 10px 18px;text-align:left;color:inherit;font-size:12.5px;font-weight:600;box-shadow:0 1px 0 var(--line)}
.s17 .tk::before,.s17 .tk::after{content:"";position:absolute;left:-7px;top:50%;width:14px;height:14px;margin-top:-7px;border-radius:50%;background:var(--bg)}
.s17 .tk::after{left:auto;right:-7px}
.s17 .tk b{font-family:var(--f-num);font-weight:400;font-size:22px;color:var(--bad)}
.s17 .tk small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s17 .tk:hover{box-shadow:0 0 0 2px var(--lime)}
.s17 .donut{display:grid;grid-template-columns:58px minmax(0,1fr);gap:10px;align-items:center;background:var(--gr);border:0;border-radius:10px;padding:10px 12px;text-align:left;color:#fff}
.s17 .donut svg{width:58px;height:58px}
.s17 .donut span{font-size:12px;font-weight:700} .s17 .donut small{display:block;font-weight:400;font-size:11px;color:#AEB5BC}
.s17 .bridge{border-radius:12px;background:#fff;overflow-x:auto;box-shadow:0 1px 0 var(--line),0 16px 34px rgba(30,34,38,.07)}
.s17 .bridge svg{display:block;width:100%;min-width:980px;height:auto}
.s17 .bsw{display:inline-flex;background:var(--gr);border-radius:8px;padding:3px;margin-bottom:10px}
.s17 .bsw button{border:0;background:transparent;color:#D5DAD0;border-radius:6px;padding:7px 14px;font-size:12px;font-weight:600;min-height:38px}
.s17 .bsw button[aria-pressed="true"]{background:var(--lime);color:var(--gr)}
.s17 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--limed)}
.s17 .pc{cursor:pointer} .s17 .pc:focus{outline:none} .s17 .pc:hover .fc,.s17 .pc:focus .fc{stroke:#1E2226;stroke-width:2.5}
.s17 .grow{transform-box:fill-box;transform-origin:bottom;animation:s17g .7s ease both}
@keyframes s17g{from{transform:scaleY(0)}}
.s17 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:10px}
.s17 .legend i{display:inline-block;width:14px;height:12px;border-radius:2px;vertical-align:-1px;margin-right:6px}
.s17 .zone{margin-top:44px;scroll-margin-top:20px;border-radius:12px}
.s17 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px 16px;margin-bottom:14px}
.s17 .zh h3{font-family:var(--f-num);font-weight:400;font-size:40px;margin:0;line-height:1;background:linear-gradient(transparent 62%,var(--lime) 62% 92%,transparent 92%);padding:0 4px}
.s17 .zh p{margin:0;font-size:12.5px;color:var(--mute)}
.s17 .pick{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:12px;font-weight:700;color:var(--limed)}
.s17 .pick select{font:inherit;font-weight:500;font-size:12.5px;padding:8px 10px;border:1px solid #C9CDC4;border-radius:8px;background:#fff;color:var(--ink);min-height:40px;max-width:270px;box-shadow:0 2px 0 #C9CDC4}
.s17 .bullets{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.s17 .bl{background:#fff;border:0;border-radius:10px;padding:12px 14px;text-align:left;color:inherit;box-shadow:0 1px 0 var(--line);border-left:6px solid var(--c);transition:transform .15s}
.s17 .bl:hover,.s17 .bl:focus-visible{transform:translateX(3px);box-shadow:0 0 0 2px var(--lime)}
.s17 .bl .top{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.s17 .bl .nm{font-size:13px;font-weight:700} .s17 .bl .nm small{font-weight:600;font-size:10px;letter-spacing:.06em;color:var(--limed);margin-left:6px}
.s17 .bl .st{font-size:10.5px;font-weight:700;letter-spacing:.05em}
.s17 .bu{display:grid;grid-template-columns:70px minmax(0,1fr) 92px;gap:8px;align-items:center;font-size:11px;color:var(--mute);margin-top:8px}
.s17 .bu b{font-family:var(--f-num);font-weight:400;font-size:19px;text-align:right}
.s17 .band{position:relative;height:16px;border-radius:3px;background:linear-gradient(90deg,#E9ECE4 0 40%,#DCE0D6 40% 60%,#E9ECE4 60%)}
.s17 .band i{position:absolute;top:4px;height:8px;left:0;background:var(--gr);border-radius:2px}
.s17 .band u{position:absolute;top:-3px;bottom:-3px;width:3px;margin-left:-1.5px;background:var(--lime);box-shadow:0 0 0 1px var(--limed)}
.s17 .ahead{color:var(--ok)} .s17 .watch{color:var(--warn)} .s17 .off{color:var(--bad)}
.s17 .filt{display:flex;flex-wrap:wrap;gap:6px}
.s17 .filt button{border:1px solid #C9CDC4;background:#fff;border-radius:999px;padding:6px 12px;font-size:12px;font-weight:600;min-height:36px;color:var(--ink)}
.s17 .filt button[aria-pressed="true"]{background:var(--gr);color:var(--lime);border-color:var(--gr)}
.s17 .queue{background:#fff;border-radius:12px;box-shadow:0 1px 0 var(--line);overflow:hidden}
.s17 .qr{display:grid;grid-template-columns:130px minmax(0,1fr) 150px 210px;gap:12px;align-items:center;padding:12px 14px;border-bottom:1px solid var(--line);cursor:pointer;font-size:12.5px}
.s17 .qr:hover,.s17 .qr:focus-visible{background:#F7F9F1}
.s17 .qr .s{justify-self:start;font-size:10px;font-weight:700;letter-spacing:.06em;padding:3px 8px;border-radius:4px;background:#ECEEE8;color:var(--mute)}
.s17 .qr.awaiting{background:var(--lime2)} .s17 .qr.awaiting .s{background:var(--gr);color:var(--lime)}
.s17 .qr.approved .s{background:#DDEFD0;color:var(--ok)} .s17 .qr.done .s{background:#E2EAF0;color:#2E5B78}
.s17 .qr .t{font-weight:600} .s17 .qr .t small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s17 .qr .g{font-family:var(--f-num);font-size:19px;color:var(--ok)} .s17 .qr .g small{display:block;font-family:var(--f-body);font-size:10.5px;color:var(--mute)}
.s17 .fh-dec{display:flex;gap:6px}
.s17 .fh-dec button{flex:1;min-height:40px;border-radius:8px;font-weight:700;font-size:12.5px;border:1px solid var(--gr)}
.s17 .fh-dec button:first-child{background:var(--gr);color:var(--lime)} .s17 .fh-dec button:last-child{background:#fff;color:var(--gr)}
.s17 .runl{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:11.5px;color:var(--mute);padding:10px 14px;background:var(--gr);color:#D5DAD0}
.s17 .runl b{color:var(--lime);font-weight:700;margin-right:5px}
.s17 .rings{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.s17 .rg{display:grid;grid-template-columns:62px minmax(0,1fr);gap:10px;align-items:start;background:#fff;border:0;border-radius:10px;padding:12px;text-align:left;color:inherit;box-shadow:0 1px 0 var(--line);transition:transform .15s}
.s17 .rg:hover,.s17 .rg:focus-visible{transform:translateY(-3px);box-shadow:0 0 0 2px var(--lime)}
.s17 .rg svg{width:62px;height:62px}
.s17 .rg .nm{font-weight:700;font-size:13px;line-height:1.2} .s17 .rg .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s17 .rg .chip{display:inline-block;font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:4px;margin:5px 0}
.s17 .rg ul{list-style:none;margin:4px 0 0;padding:0;font-size:12px;display:grid;gap:3px}
.s17 .rg li::before{content:"▫ "} .s17 .rg li.y::before{content:"▪ ";color:var(--limed)} .s17 .rg li.l{color:var(--bad);font-weight:600}
.s17 .rg .imp{display:block;font-size:11.5px;color:var(--bad);line-height:1.35;margin-top:4px} .s17 .rg .nx{display:block;font-size:11.5px;color:var(--mute);margin-top:4px}
.s17 .vt{display:inline-flex;background:var(--gr);border-radius:8px;padding:3px}
.s17 .vt button{border:0;background:transparent;border-radius:6px;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:#D5DAD0}
.s17 .vt button[aria-pressed="true"]{background:var(--lime);color:var(--gr)}
.s17 .steps{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s17 .chart{background:#fff;border-radius:12px;padding:12px;overflow-x:auto;box-shadow:0 1px 0 var(--line)}
.s17 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s17 .mlist{display:grid;gap:8px}
.s17 .mlist button{display:flex;justify-content:space-between;gap:12px;align-items:baseline;background:#fff;border:0;border-radius:10px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12.5px;box-shadow:0 1px 0 var(--line)}
.s17 .mlist b{font-family:var(--f-num);font-weight:400;font-size:23px;color:var(--ink);white-space:nowrap}
.s17 .mlist .why{background:var(--gr);color:#D5DAD0} .s17 .mlist .why b{color:var(--lime)}
@media (max-width:1000px){ .s17 .head{grid-template-columns:1fr} .s17 .tix{grid-template-columns:1fr 1fr} .s17 .bullets{grid-template-columns:1fr} .s17 .rings{grid-template-columns:1fr 1fr} .s17 .steps{grid-template-columns:1fr} .s17 .qr{grid-template-columns:minmax(0,1fr) auto} .s17 .qr .t{grid-column:1/-1;grid-row:2} .s17 .qr .fh-dec,.s17 .qr .dash{grid-column:1/-1} }
@media (max-width:600px){ .s17 .frz.mini .keys{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none} .s17 .frz.mini .ky{flex:none} .s17 .frz.mini .head{grid-template-columns:1fr;gap:6px;margin:6px 0} .s17 .frz.mini h2{font-size:28px}
  .s17 .frz.mini .odo{grid-template-columns:repeat(4,minmax(0,1fr));justify-self:stretch} .s17 .frz.mini .od b{font-size:16px} .s17 .frz.mini .od span{font-size:8px;letter-spacing:.04em}
  .s17 .frz.mini .tix{display:flex;overflow-x:auto;scrollbar-width:none} .s17 .frz.mini .tk,.s17 .frz.mini .donut{flex:0 0 78%}
  .s17 .swipe{display:block} .s17 h2{font-size:54px} .s17 h2::before{height:40px} .s17 .odo{grid-template-columns:1fr 1fr} .s17 .tix,.s17 .rings{grid-template-columns:1fr} .s17 .ky{padding:8px 10px;font-size:12px} }
`,
  render(){
    const PC = { live:"#3E7F12", testing:"#D9940A", building:"#9AA0A6", blocked:"#C8342B", notstarted:"#C9CDC4" };
    const live = countParts("live"), wait = D.actions.filter(a=>a.st==="awaiting").length, mode = UI.fhBridge || "td";
    const od = (lab, val, sub, attr) => `<button class="od" type="button" ${attr}><span>${lab}</span><b>${val}</b><em>${sub}</em></button>`;
    const odo = od("PARTS LIVE",`${live}/12`,"plan 7",`data-tab="links"`) + od("KPIS ON COURSE",`${onCourse}/${D.kpis.length}`,`plan ${D.kpis.length}`,`data-tab="measures"`)
      + od("EBITDA BACK/OUT",`${ebitdaTotal.toFixed(1)}/${spendTotal.toFixed(1)}`,`₹ lakh · plan ${D.cumPlan[D.actualTo].toFixed(1)} back`,`data-ref="health:0"`) + od("BREAK-EVEN",D.breakeven.fore.toUpperCase(),`plan ${D.breakeven.plan}`,`data-ref="health:0"`);

    /* --- the bridge --- */
    const k1 = KP.K1, td = mode === "td";
    const exp = td ? k1.td[0] : k1.day[0], act = td ? k1.td[1] : k1.day[1];
    const steps = D.drivers.filter(d => d.e).map(d => ({ d, v: td ? d.etd : d.e })).sort((a,b) => a.v - b.v);
    const W = 1100, H = 530, x0 = 70, x1 = 1070, top = 60, bot = 330, n = steps.length + 2, sw = (x1-x0)/n, bwid = sw*0.62;
    const lo = Math.min(act, exp) - (exp-act)*0.9, hi = exp + (exp-act)*0.6; const Y = v => bot - (bot-top)*(v-lo)/(hi-lo);
    let g = `<defs><pattern id="s17hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#FBE6E4"/><line x1="0" y1="0" x2="0" y2="6" stroke="#C8342B" stroke-width="2"/></pattern></defs>`;
    for (let i=0;i<=4;i++){ const v = lo + (hi-lo)*i/4; g += `<line x1="${x0-10}" x2="${x1}" y1="${Y(v)}" y2="${Y(v)}" stroke="#EEF0EA"/><text x="${x0-14}" y="${Y(v)+4}" text-anchor="end" font-size="10" fill="#5D646C">${td?Math.round(v):v.toFixed(1)}</text>`; }
    g += `<text x="${x0-14}" y="${top-26}" font-size="11" font-weight="700" letter-spacing="1.3" fill="#4F6B00">EBITDA ${td?esc(D.sinceLabel.toUpperCase()):"ON "+esc(D.dayLabel.toUpperCase())} · ₹ LAKH · THE AXIS STARTS AT ${td?Math.round(lo):lo.toFixed(1)}</text>`;
    const total = (i, v, lab, c, ref) => { const x = x0 + i*sw + (sw-bwid)/2; return `<g ${ref?`class="pc" data-ref="${ref}" tabindex="0" role="button"`:""} aria-label="${lab}: ₹${v} lakh"><rect class="fc grow" x="${x}" y="${Y(v)}" width="${bwid}" height="${bot-Y(v)}" rx="4" fill="${c}"/><text x="${x+bwid/2}" y="${Y(v)-8}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="22" fill="#1E2226">₹${td?Math.round(v):v.toFixed(1)}</text><text x="${x+bwid/2}" y="${bot+18}" text-anchor="middle" font-size="11" font-weight="700" fill="#1E2226">${lab}</text></g>`; };
    g += total(0, exp, "EXPECTED", "#2B3036");
    let run = exp;
    steps.forEach((s,i) => { const a = run, b = run + s.v, x = x0 + (i+1)*sw + (sw-bwid)/2, up = s.v > 0, ya = Y(Math.max(a,b)), yb = Y(Math.min(a,b));
      g += `<line x1="${x - (sw-bwid)}" x2="${x}" y1="${Y(a)}" y2="${Y(a)}" stroke="#9AA0A6" stroke-dasharray="3 3"/>`;
      g += `<g class="pc" data-ref="drv:${s.d.id}" tabindex="0" role="button" aria-label="${esc(s.d.name)}: ${fhL(s.v)}"><rect class="fc" x="${x}" y="${ya}" width="${bwid}" height="${Math.max(3, yb-ya)}" rx="3" fill="${up?"#B7D433":"url(#s17hatch)"}" stroke="${up?"#4F6B00":"#C8342B"}" stroke-width="1.4"/>
        <text x="${x+bwid/2}" y="${up?ya-8:yb+16}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="17" fill="${up?"#3E7F12":"#C8342B"}">${up?"+":"−"}${Math.abs(s.v).toFixed(td?1:2)}</text>
        <foreignObject x="${x0 + (i+1)*sw + 2}" y="${bot+6}" width="${sw-4}" height="74"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 9.5px/1.2 Poppins,sans-serif;color:#1E2226;text-align:center">${esc(s.d.name)}<div style="font-weight:400;color:#5D646C;margin-top:2px">${esc(s.d.src.replace(" suite",""))}</div></div></foreignObject></g>`;
      run = b; });
    g += `<line x1="${x0 + (n-1)*sw - (sw-bwid)/2 - 2}" x2="${x0 + (n-1)*sw + (sw-bwid)/2}" y1="${Y(run)}" y2="${Y(run)}" stroke="#9AA0A6" stroke-dasharray="3 3"/>`;
    g += total(n-1, act, "ACTUAL", act < exp ? "#C8342B" : "#3E7F12", "kpi:K1");
    const gap = act - exp; g += `<text x="${x1}" y="${top-26}" text-anchor="end" font-size="11" font-weight="700" fill="${gap<0?"#C8342B":"#3E7F12"}">${gap<0?"SHORT BY":"AHEAD BY"} ₹${Math.abs(gap).toFixed(td?0:1)} LAKH (${gap<0?"−":"+"}${Math.abs(gap/exp*100).toFixed(1)}%)</text>`;
    /* feeds */
    const fy = 440, fw = 80, fg = 5.5, fx0 = (W - (12*fw + 11*fg))/2;
    g += `<rect x="0" y="${fy-36}" width="${W}" height="${H-fy+36}" fill="#2B3036"/><text x="${fx0}" y="${fy-14}" font-size="11" font-weight="700" letter-spacing="1.4" fill="#B7D433">WHERE THE NUMBERS COME FROM · READ AT 6 AM EVERY DAY</text>`;
    D.parts.forEach((p,i) => { const x = fx0 + i*(fw+fg), c = PC[p.st], soft = p.st==="building"||p.st==="notstarted";
      g += `<g class="pc" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}"><rect class="fc" x="${x}" y="${fy}" width="${fw}" height="74" rx="7" fill="#353B42" stroke="${c}" stroke-width="1.6" ${soft?'stroke-dasharray="4 3"':""}/>
        <foreignObject x="${x+5}" y="${fy+5}" width="${fw-10}" height="66"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 9px/1.2 Poppins,sans-serif;color:#F2F3EF;height:64px;display:flex;flex-direction:column;justify-content:space-between"><span><b style="font-family:'Bebas Neue';font-weight:400;font-size:13px;color:#B7D433">${p.id}</b> ${esc(p.short)}</span><span style="font-size:8.5px;font-weight:700;color:${c==="#3E7F12"?"#9BD267":c}">${PART_WORD[p.st].toUpperCase()}</span></div></foreignObject></g>`; });
    const bridge = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="EBITDA ${td?esc(D.sinceLabel):"on "+esc(D.dayLabel)}: expected ₹${exp} lakh, actual ₹${act} lakh, with one step for each cause, and the twelve feeds underneath.">${g}</svg>`;

    /* --- KPI bullets --- */
    const bu = (k, e, a, lab, st) => { const span = Math.max(Math.abs(a-e)*2.2, Math.abs(e)*0.06), lo2 = e - span, w = v => Math.max(0, Math.min(100, (v-lo2)/(2*span)*100));
      return `<span class="bu"><span>${lab}</span><span class="band"><i style="width:${w(a).toFixed(1)}%"></i><u style="left:50%"></u></span><b class="${st}">${fmtv(k,a)}</b></span>`; };
    const bl = k => { const c = k.state==="ahead"?"#3E7F12":k.state==="watch"?"#D9940A":"#C8342B";
      return `<button class="bl" type="button" data-ref="kpi:${k.id}" style="--c:${c}"><span class="top"><span class="nm">${esc(k.name)}${D.core.includes(k.id)?"":"<small>YOURS</small>"}</span><span class="st ${k.state}">${STATE_WORD[k.state].toUpperCase()}</span></span>
        ${bu(k,k.day[0],k.day[1],esc(D.dayLabel),k.dayState)}${bu(k,k.td[0],k.td[1],esc(D.sinceLabel.replace("since ","Since ")),k.tdState)}
        <span class="bu" style="margin-top:4px"><span></span><span style="font-size:10.5px">lime line: expected (${fmtv(k,k.day[0])} on the day, ${fmtv(k,k.td[0])} ${esc(D.sinceLabel)})</span><span style="text-align:right;font-weight:700" class="${k.tdState}">${fhPct(k)}</span></span></button>`; };

    /* --- recovery queue --- */
    const f = UI.fhFilter || "all";
    const order = { awaiting:0, approved:1, held:2, advised:3, done:4 };
    const list = D.actions.slice().sort((a,b)=>order[a.st]-order[b.st]).filter(a => f==="all" || (f==="ceo" ? ["awaiting","approved","held"].includes(a.st) : a.st===f));
    const qr = a => `<div class="qr ${a.st}" role="button" tabindex="0" data-ref="act:${a.id}"><span class="s">${esc(FH_ST[a.st].toUpperCase())}</span><span class="t">${esc(a.t)}<small>${esc(a.when)}${a.st==="advised"?` · ${esc(fhWho(a.who))}: ${esc(a.reply)}`:""}${a.cost?` · ${esc(fhCost(a))}`:""}</small></span><span class="g">${a.gain?fhL(a.gain):"—"}<small>EBITDA a day</small></span>${a.st==="awaiting"?fhDecideBtns(a):`<span class="dash" style="font-size:11.5px;color:var(--mute)">${a.st==="done"?"Done within its rules":a.st==="advised"?"Owner to act":a.st==="approved"?"Being carried out":"Raised again tomorrow"}</span>`}</div>`;
    const fb = (k, lab, cnt) => `<button type="button" data-fhf="${k}" aria-pressed="${f===k}">${lab} · ${cnt}</button>`;
    const filt = `<div class="filt" role="group" aria-label="Show recovery steps">${fb("all","All",D.actions.length)}${fb("ceo","For the CEO",D.actions.filter(a=>["awaiting","approved","held"].includes(a.st)).length)}${fb("done","Done by the suite",D.actions.filter(a=>a.st==="done").length)}${fb("advised","Advised",D.actions.filter(a=>a.st==="advised").length)}</div>`;

    /* --- people rings --- */
    const rg = p => { const cc = p.state==="ahead"?["#3E7F12","#E2F0D5"]:p.state==="watch"?["#A86B05","#FBEBCB"]:["#C8342B","#FBE1DD"]; const R = 24, C = 2*Math.PI*R, fd = p.done/p.due, fl = p.late/p.due;
      const ring = `<svg viewBox="0 0 62 62" aria-hidden="true"><circle cx="31" cy="31" r="${R}" fill="none" stroke="#ECEEE8" stroke-width="7"/><circle cx="31" cy="31" r="${R}" fill="none" stroke="#B7D433" stroke-width="7" stroke-dasharray="${(C*fd).toFixed(1)} ${C.toFixed(1)}" transform="rotate(-90 31 31)"/><circle cx="31" cy="31" r="${R}" fill="none" stroke="#C8342B" stroke-width="7" stroke-dasharray="${(C*fl).toFixed(1)} ${C.toFixed(1)}" stroke-dashoffset="${(-C*fd).toFixed(1)}" transform="rotate(-90 31 31)"/><text x="31" y="37" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="17" fill="#1E2226">${p.done}/${p.due}</text></svg>`;
      const body = UI.view==="day" ? `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":/^(late|waiting)/.test(String(t[1]))?"l":""}">${esc(t[0])}${t[1]!==1?` · ${esc(t[1])}`:""}</li>`).join("")}</ul>` : "";
      return `<button class="rg" type="button" data-ref="per:${p.key}">${ring}<span><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="chip" style="color:${cc[0]};background:${cc[1]}">${PERSON_WORD[p.state]}</span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</span></button>`; };

    /* --- money: steps --- */
    const CW = 760, CH = 300, cx0 = 50, cx1 = 740, cy0 = 20, cy1 = 250, nm = D.cumMonths.length, vmax = 110, X = i => cx0 + (cx1-cx0)*i/nm, YY = v => cy1 - (cy1-cy0)*v/vmax;
    const stepPath = arr => arr.map((v,i)=>`${i?"L":"M"}${X(i)},${YY(v)} L${X(i+1)},${YY(v)}`).join(" ");
    let c = ""; [0,25,50,75,100].forEach(v => c += `<line x1="${cx0}" x2="${cx1}" y1="${YY(v)}" y2="${YY(v)}" stroke="${v?"#EEF0EA":"#1E2226"}"/><text x="${cx0-8}" y="${YY(v)+4}" text-anchor="end" font-size="10" fill="#5D646C">${v}</text>`);
    c += `<path d="${stepPath(D.cumFore)} L${X(nm)},${cy1} L${X(0)},${cy1} Z" fill="#B7D433" opacity=".35"/><path d="${stepPath(D.cumFore)}" fill="none" stroke="#4F6B00" stroke-width="2.5"/><path d="${stepPath(D.cumSpend)}" fill="none" stroke="#2B3036" stroke-width="2.5"/><path d="${stepPath(D.cumPlan)}" fill="none" stroke="#2B3036" stroke-width="1.2" stroke-dasharray="4 4"/>`;
    D.cumMonths.forEach((m,i) => c += `<text x="${(X(i)+X(i+1))/2}" y="${cy1+18}" text-anchor="middle" font-size="11" font-weight="600" fill="${i>D.actualTo?"#5D646C":"#1E2226"}">${m}</text><rect data-ref="month:${i}" data-nopen x="${X(i)}" y="${cy0}" width="${X(1)-X(0)}" height="${cy1-cy0+24}" fill="transparent" style="cursor:help"/>`);
    const fi = D.breakeven.foreIdx; c += `<rect x="${X(fi)}" y="${cy0}" width="${X(1)-X(0)}" height="${cy1-cy0}" fill="#B7D433" opacity=".18"/><text x="${(X(fi)+X(fi+1))/2}" y="${cy0+14}" text-anchor="middle" font-size="10.5" font-weight="700" fill="#4F6B00">BREAK-EVEN</text>`;
    c += `<g font-size="11" fill="#1E2226"><rect x="${cx0}" y="${CH-22}" width="14" height="10" fill="#B7D433"/><text x="${cx0+20}" y="${CH-13}">EBITDA back to date</text><line x1="${cx0+160}" x2="${cx0+182}" y1="${CH-17}" y2="${CH-17}" stroke="#2B3036" stroke-width="2.5"/><text x="${cx0+188}" y="${CH-13}">Money out to date</text><line x1="${cx0+320}" x2="${cx0+342}" y1="${CH-17}" y2="${CH-17}" stroke="#2B3036" stroke-dasharray="4 4"/><text x="${cx0+348}" y="${CH-13}">Plan · ₹ lakh · after Oct is forecast</text></g>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="EBITDA back and money out to date by month; break-even ${D.breakeven.fore}.">${c}</svg>`;

    const R = 22, C = 2*Math.PI*R, rf = Math.max(.05, 1 - D.milestone.days/30);
    const donut = `<svg viewBox="0 0 58 58" aria-hidden="true"><circle cx="29" cy="29" r="${R}" fill="none" stroke="#3F464E" stroke-width="7"/><circle cx="29" cy="29" r="${R}" fill="none" stroke="#B7D433" stroke-width="7" stroke-linecap="round" stroke-dasharray="${(C*rf).toFixed(1)} ${C.toFixed(1)}" transform="rotate(-90 29 29)"/><text x="29" y="36" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="21" fill="#fff">${D.milestone.days}</text></svg>`;
    return `<div class="s17"><div class="wrap"><div class="frz" data-frz>
      <nav class="keys" aria-label="Suite sections">${D.tabs.map((t,i)=>`<button class="ky ${i?"":"on"}" type="button" data-tab="${t[0]}">${t[1]}${t[0]==="recovery"&&wait?`<em>${wait}</em>`:""}</button>`).join("")}</nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2><p>Checked at 6 AM every day against the day and ${esc(D.sinceLabel)} · data as of ${esc(D.asOf)}</p></div>
        <div class="odo" aria-label="Pulse strip">${odo}</div></div>
      <div class="tix" aria-label="Watch list and next go-live">${D.watch.map((w,i)=>`<button class="tk" type="button" data-ref="${w.ref}"><b>0${i+1}</b><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}
        <button class="donut" type="button" data-ref="part:${D.milestone.part}">${donut}<span>days to the next go-live<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div></div>
      <section class="zone" data-zone="links" style="margin-top:0"><div class="bsw" role="group" aria-label="Show EBITDA for"><button type="button" data-fhb="td" aria-pressed="${td}">${esc(D.sinceLabel.replace("since ","Since "))}</button><button type="button" data-fhb="day" aria-pressed="${!td}">${esc(D.dayLabel)}</button></div>
        <p class="swipe">Swipe sideways to see every step →</p><div class="bridge">${bridge}</div>
        <div class="legend"><span><i style="background:#2B3036"></i>Expected</span><span><i style="background:repeating-linear-gradient(45deg,#FBE6E4 0 2px,#C8342B 2px 4px)"></i>Cause pulling EBITDA down</span><span><i style="background:#B7D433"></i>Cause lifting it</span><span>· Feeds: live, testing, being built, late, not started</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3>${fhChooser("pick")}</div><div class="bullets">${D.kpis.map(bl).join("")}</div></section>
      <section class="zone" data-zone="recovery"><div class="zh"><h3>Recovery</h3>${filt}</div><div class="queue"><div class="runl">${D.runLog.map(r=>`<span><b>${r[0]}</b>${esc(r[1])}</span>`).join("")}</div>${list.map(qr).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="rings">${D.people.map(rg).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="steps"><div class="chart">${chart}</div>
          <div class="mlist">
            <button type="button" data-ref="month:1"><span>Subscription, each month</span><b>${L(D.spend[0].v[1])}</b></button>
            <button type="button" data-ref="month:1"><span>Salary of the Financial Health Analyst we recommended, each month</span><b>${L(D.spend[1].v[1])}</b></button>
            <button type="button" data-ref="month:1"><span>One-time so far (finance data set-up, CEO decision desk)</span><b>${L(sum(D.spend[2].v))}</b></button>
            <button type="button" data-ref="health:0"><span>Revenue recovered so far by the suite's actions</span><b>${L(revTotal)}</b></button>
            <button type="button" data-ref="health:0"><span>EBITDA added now, and at full run, each month</span><b>${L(D.ebitda[1])} → ${L(D.runRate.ebitda)}</b></button>
            <button type="button" class="why" data-ref="health:0"><span>Break-even ${D.breakeven.fore}, ${D.breakeven.late} late. See why</span><b>›</b></button>
          </div></div></section>
    </div></div>`;
  },
  after(){
    /* the header, down to the end of the overview, stays on screen; it tightens once the page scrolls */
    const fz = document.querySelector("#stage .s17 [data-frz]"); if (window.__s17frz) removeEventListener("scroll", window.__s17frz);
    if (!fz) return; const top0 = fz.parentElement.getBoundingClientRect().top + scrollY;
    const on = () => { const y = scrollY; if (!fz.classList.contains("mini") && y > top0 + 60) fz.classList.add("mini"); else if (fz.classList.contains("mini") && y < top0 + 4) fz.classList.remove("mini"); };
    window.__s17frz = on; addEventListener("scroll", on, {passive:true}); on();
  }
});
/* bridge switch and recovery filter: delegated so they also work in the block library */
document.addEventListener("click", e => { const b = e.target.closest(".s17 [data-fhb], .s17 [data-fhf]"); if (!b) return; suiteOf(b);
  if (b.dataset.fhb) UI.fhBridge = b.dataset.fhb; else UI.fhFilter = b.dataset.fhf; const y = scrollY; render(); scrollTo(0, y); });
