/* ===== Procurement, option 2: teal and coral, the supply lines ===== */
SCHEMES.push({
  key:"lines", letter:"2", name:"Teal and coral",
  note:"<b>Option 2 · teal and coral.</b> The suite as three lines that meet at the main store: buying from 41 suppliers, the store itself, and the wards. Each part is a stop on its line, marked with where it stands; where a line is cut, supplies are not getting through.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#12302D","--sh-mute":"#56706C","--sh-line":"#D5E2DF","--sh-card":"#F3F8F7","--c-ok":"#1D8A5B","--c-warn":"#B26B00","--c-bad":"#D9472B","--pk-bg":"#12302D","--pk-fg":"#FFFFFF","--pk-line":"#EF6A4C","--pk-r":"14px","--sh-r":"22px" },
  fab:18,
  blocks:{ nav:".badges", pulse:".status", watch:".alerts", countdown:".ring", hero:".map", kpis:".dials", team:".journeys", money:".pairs" },
  css:`
.s14{--bg:#F1F6F4;--ink:#12302D;--mute:#56706C;--teal:#0E7C72;--teal2:#D3ECE8;--coral:#EF6A4C;--coral2:#FDE3DC;--slate:#33557D;--ok:#1D8A5B;--warn:#B26B00;--bad:#D9472B;--line:#D5E2DF;
  background:var(--bg);color:var(--ink);padding:18px 16px 90px;overflow-x:clip}
.s14 .wrap{max-width:1240px;margin:0 auto}
.s14 .badges{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.s14 .bd{display:flex;align-items:center;gap:8px;background:#fff;border:2px solid var(--line);border-radius:999px;padding:6px 14px 6px 6px;font-size:12.5px;font-weight:600;color:var(--ink);min-height:44px}
.s14 .bd i{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--c);color:#fff;font-style:normal;font-family:var(--f-num);font-size:15px;line-height:1}
.s14 .bd:hover{border-color:var(--c)}
.s14 .bd.on{background:var(--ink);border-color:var(--ink);color:#fff}
.s14 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px;align-items:end;margin:26px 0 16px}
.s14 .head small{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--teal)}
.s14 .head small::before{content:"";width:38px;height:6px;border-radius:3px;background:linear-gradient(90deg,var(--teal) 0 33%,var(--coral) 33% 66%,var(--slate) 66%)}
.s14 h2{font-family:var(--f-num);font-weight:400;font-size:78px;line-height:.88;margin:6px 0 0;letter-spacing:.01em}
.s14 .status{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;min-width:420px}
.s14 .sb{display:grid;grid-template-columns:14px minmax(0,1fr) auto;gap:10px;align-items:center;background:#fff;border:0;border-radius:14px;padding:8px 14px 8px 12px;text-align:left;color:inherit;box-shadow:0 1px 0 var(--line),0 6px 16px rgba(18,48,45,.05)}
.s14 .sb i{width:14px;height:14px;border-radius:50%;border:4px solid var(--c);background:#fff}
.s14 .sb span{font-size:10.5px;letter-spacing:.1em;font-weight:700;color:var(--mute)} .s14 .sb span em{display:block;font-style:normal;letter-spacing:0;font-weight:400;font-size:11px;color:var(--teal)}
.s14 .sb b{font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1;white-space:nowrap}
.s14 .alerts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.75fr);gap:12px;margin-bottom:16px;align-items:stretch}
.s14 .al{display:grid;grid-template-columns:30px minmax(0,1fr);gap:10px;align-items:center;background:#fff;border:0;border-left:5px solid var(--coral);border-radius:14px;padding:10px 12px;text-align:left;color:inherit;font-size:12.5px;font-weight:600;box-shadow:0 6px 16px rgba(18,48,45,.05)}
.s14 .al i{width:0;height:0;border-left:13px solid transparent;border-right:13px solid transparent;border-bottom:22px solid var(--coral);position:relative}
.s14 .al i::after{content:"!";position:absolute;left:-3px;top:5px;color:#fff;font-style:normal;font-weight:700;font-size:13px}
.s14 .al small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s14 .al:hover{box-shadow:0 0 0 2px var(--coral)}
.s14 .ring{display:grid;grid-template-columns:62px minmax(0,1fr);gap:10px;align-items:center;background:var(--ink);border:0;border-radius:14px;padding:10px 12px;text-align:left;color:#fff}
.s14 .ring svg{width:62px;height:62px}
.s14 .ring span{font-size:12px;font-weight:700} .s14 .ring small{display:block;font-weight:400;font-size:11px;color:#A9C8C3}
.s14 .map{border-radius:22px;background:#fff;overflow-x:auto;box-shadow:0 1px 0 var(--line),0 18px 40px rgba(18,48,45,.08)}
.s14 .map svg{display:block;width:100%;min-width:980px;height:auto}
.s14 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--teal)}
.s14 .pc{cursor:pointer}
.s14 .pc:focus{outline:none} .s14 .pc:focus .fr{stroke:#F2B705}
.s14 .pc:hover .fr{stroke-width:7}
.s14 .pc.ping .dot{animation:s14ping 1s ease}
@keyframes s14ping{0%{r:12}100%{}}
.s14 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:10px}
.s14 .legend i{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-1px;margin-right:6px}
.s14 .zone{margin-top:44px;scroll-margin-top:20px;border-radius:22px}
.s14 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:16px}
.s14 .zh h3{font-family:var(--f-num);font-weight:400;font-size:40px;margin:0;line-height:1;display:flex;align-items:center;gap:12px}
.s14 .zh h3::before{content:"";width:16px;height:16px;border-radius:50%;border:5px solid var(--teal);background:#fff}
.s14 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s14 .dials{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.s14 .dl{display:grid;grid-template-columns:118px minmax(0,1fr);gap:12px;align-items:center;background:#fff;border:0;border-radius:18px;padding:12px 14px 12px 10px;text-align:left;color:inherit;box-shadow:0 6px 16px rgba(18,48,45,.05);transition:transform .15s}
.s14 .dl:hover,.s14 .dl:focus-visible{transform:translateY(-3px);box-shadow:0 0 0 2px var(--teal),0 10px 20px rgba(18,48,45,.08)}
.s14 .dl svg{width:118px;height:72px}
.s14 .dl .nm{display:block;font-size:12.5px;font-weight:600;line-height:1.3}
.s14 .dl b{display:block;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1;margin-top:4px}
.s14 .dl .sw{display:block;font-size:11px;font-weight:700;letter-spacing:.04em;margin-top:3px}
.s14 .dl .rg{display:block;font-size:10.5px;color:var(--mute);margin-top:2px}
.s14 .ahead{color:var(--ok)} .s14 .watch{color:var(--warn)} .s14 .off{color:var(--bad)}
.s14 .journeys{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s14 .jr{background:#fff;border:0;border-radius:18px;padding:12px 14px;text-align:left;color:inherit;display:flex;flex-direction:column;gap:9px;box-shadow:0 6px 16px rgba(18,48,45,.05);transition:transform .15s}
.s14 .jr:hover,.s14 .jr:focus-visible{transform:translateY(-3px);box-shadow:0 0 0 2px var(--teal),0 10px 20px rgba(18,48,45,.08)}
.s14 .jr .top{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.s14 .jr .av{flex:none;display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--teal2);color:var(--teal);font-family:var(--f-num);font-size:16px;margin-right:8px}
.s14 .jr .nm{display:flex;align-items:center;font-weight:700;font-size:13.5px;line-height:1.2} .s14 .jr .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s14 .jr .chip{font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:999px;white-space:nowrap}
.s14 .stops{position:relative;display:flex;justify-content:space-between;align-items:center;height:22px;margin:2px 4px}
.s14 .stops::before{content:"";position:absolute;left:0;right:0;top:50%;height:4px;margin-top:-2px;border-radius:2px;background:var(--line)}
.s14 .stops i{position:relative;width:14px;height:14px;border-radius:50%;background:#fff;border:3px solid var(--line)}
.s14 .stops i.y{border-color:var(--teal);background:var(--teal)} .s14 .stops i.l{border-color:var(--coral);background:var(--coral2)}
.s14 .jr .meta{font-size:12px} .s14 .jr .meta b{font-family:var(--f-num);font-weight:400;font-size:18px}
.s14 .jr .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s14 .jr .nx{font-size:11.5px;color:var(--mute)}
.s14 .jr ul{list-style:none;margin:0;padding:0 0 0 12px;font-size:12px;display:grid;gap:5px;border-left:4px solid var(--teal2)}
.s14 .jr li{position:relative} .s14 .jr li::before{content:"";position:absolute;left:-20px;top:3px;width:12px;height:12px;border-radius:50%;background:#fff;border:3px solid var(--line);box-sizing:border-box}
.s14 .jr li.y::before{background:var(--teal);border-color:var(--teal)} .s14 .jr li.l{color:var(--bad);font-weight:600} .s14 .jr li.l::before{border-color:var(--coral);background:var(--coral2)}
.s14 .vt{display:inline-flex;background:#fff;border-radius:999px;padding:3px;box-shadow:0 0 0 2px var(--line)}
.s14 .vt button{border:0;background:transparent;border-radius:999px;padding:6px 16px;font-size:12px;font-weight:600;min-height:36px;color:var(--ink)}
.s14 .vt button[aria-pressed="true"]{background:var(--teal);color:#fff}
.s14 .pairs{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s14 .chart{background:#fff;border-radius:22px;padding:14px;overflow-x:auto;box-shadow:0 6px 16px rgba(18,48,45,.05)}
.s14 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s14 .mlist{display:grid;gap:8px}
.s14 .mlist button{display:flex;justify-content:space-between;gap:12px;align-items:baseline;background:#fff;border:0;border-radius:14px;padding:10px 14px;text-align:left;color:var(--mute);font-size:12.5px;box-shadow:0 6px 16px rgba(18,48,45,.05)}
.s14 .mlist b{font-family:var(--f-num);font-weight:400;font-size:24px;color:var(--ink);white-space:nowrap}
.s14 .mlist .why{background:var(--coral);color:#FFF1EC} .s14 .mlist .why b{color:#fff}
@media (max-width:1000px){ .s14 .head{grid-template-columns:1fr} .s14 .status{min-width:0} .s14 .alerts{grid-template-columns:1fr 1fr} .s14 .dials,.s14 .journeys{grid-template-columns:1fr 1fr} .s14 .pairs{grid-template-columns:1fr} }
@media (max-width:600px){ .s14 .swipe{display:block} .s14 h2{font-size:56px} .s14 .status,.s14 .alerts,.s14 .dials,.s14 .journeys{grid-template-columns:1fr} .s14 .bd{padding:4px 12px 4px 4px;font-size:12px} }
`,
  render(){
    const SC = { live:"#1D8A5B", testing:"#E39B12", building:"#9AAFAB", blocked:"#D9472B", notstarted:"#C9D6D3" };
    const LC = { buying:"#0E7C72", stores:"#EF6A4C", wards:"#33557D" };
    const live = countParts("live"), M = D.month, P_ = id => D.parts.find(p=>p.id===id);
    const sb = (c, lab, val, sub, attr) => `<button class="sb" type="button" ${attr} style="--c:${c}"><i></i><span>${lab}<em>${sub}</em></span><b>${val}</b></button>`;
    const status = sb("#1D8A5B","PARTS LIVE",`${live} / 12`,"plan 4",`data-tab="links"`) + sb("#E39B12","KPIS ON COURSE",`${onCourse} / 9`,"plan 8",`data-tab="measures"`)
      + sb("#0E7C72","EBITDA BACK / OUT",`${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}`,`₹ lakh · plan ${D.cumPlan[D.actualTo].toFixed(1)} back`,`data-ref="health:0"`) + sb("#D9472B","BREAK-EVEN",D.breakeven.fore.toUpperCase(),`plan ${D.breakeven.plan}`,`data-ref="health:0"`);

    /* --- stops --- */
    const stop = (id, x, y, lab) => { const p = P_(id), s = p.st, lc = LC[p.bay], soft = s==="building"||s==="notstarted";
      const lx = x - 66, ly = lab==="up" ? y - 64 : y + 18;
      return `<g class="pc" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[s]}">
        <circle class="fr" cx="${x}" cy="${y}" r="13" fill="#fff" stroke="${s==="blocked"?"#D9472B":soft?"#9AAFAB":lc}" stroke-width="5" ${soft?'stroke-dasharray="4 3"':""}/>
        <circle class="dot" cx="${x}" cy="${y}" r="5.5" fill="${SC[s]}"/>
        ${s==="blocked"?`<text x="${x}" y="${y+4}" text-anchor="middle" font-size="11" font-weight="800" fill="#fff">!</text>`:""}
        <foreignObject x="${lx}" y="${ly}" width="132" height="48"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 9.8px/1.2 Poppins,sans-serif;color:#12302D;text-align:center;height:48px;display:flex;flex-direction:column;justify-content:${lab==="up"?"flex-end":"flex-start"}"><span><b style="font-family:'Bebas Neue';font-weight:400;font-size:13px;color:${lc}">${p.id}</b> ${esc(p.name)}</span><span style="font-weight:700;font-size:9px;letter-spacing:.04em;color:${soft?"#56706C":SC[s]}">${PART_WORD[s].toUpperCase()}</span></div></foreignObject></g>`; };

    const W = 1100, H = 560; let g = "";
    const hub = [580, 270];
    /* lines */
    const tealP = `M30,130 L480,130 L${hub[0]-12},${hub[1]-28}`, branchP = `M390,130 L470,50 L840,50`, coralP = `M170,270 L960,270`, slateP = `M${hub[0]},${hub[1]+20} L690,400 L890,400`, slateCut = `M905,400 L1070,400`;
    g += `<path d="${branchP}" stroke="#0E7C72" stroke-width="9" fill="none" stroke-linejoin="round" stroke-linecap="round" opacity=".55"/>
      <path d="${tealP}" stroke="#0E7C72" stroke-width="12" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
      <path d="${coralP}" stroke="#EF6A4C" stroke-width="12" fill="none" stroke-linecap="round"/>
      <path d="${slateP}" stroke="#33557D" stroke-width="12" fill="none" stroke-linejoin="round" stroke-linecap="round"/>
      <path d="${slateCut}" stroke="#33557D" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="2 14" opacity=".55"/>
      <path d="M938,388 l14,24 M952,388 l-14,24" stroke="#D9472B" stroke-width="4" stroke-linecap="round"/>`;
    /* trains */
    const train = (path, dur, begin, col) => `<g><rect x="-13" y="-6" width="26" height="12" rx="6" fill="${col}" stroke="#fff" stroke-width="2"/><rect x="-7" y="-2" width="4" height="4" fill="#fff"/><rect x="2" y="-2" width="4" height="4" fill="#fff"/><animateMotion dur="${dur}s" begin="${begin}s" repeatCount="indefinite" rotate="auto" path="${path}"/></g>`;
    g += train(tealP, 9, 0, "#0B5F57") + train(tealP, 9, -4.5, "#0B5F57") + train(coralP, 12, 0, "#C24E33") + train(coralP, 12, -6, "#C24E33") + train(`M${hub[0]},${hub[1]+20} L690,400 L860,400`, 6, -2, "#23405F");
    /* ends */
    g += `<text x="30" y="96" font-size="10.5" font-weight="700" letter-spacing="1.2" fill="#0E7C72">FROM 41 SUPPLIERS ▸</text><text x="30" y="110" font-size="9.5" fill="#56706C">about 90 bills a day</text>
      <text x="850" y="54" font-size="10.5" font-weight="700" letter-spacing="1.2" fill="#0E7C72">▸ ACCOUNTS</text>
      <text x="170" y="236" font-size="10.5" font-weight="700" letter-spacing="1.2" fill="#EF6A4C">ON THE SHELVES</text><text x="170" y="250" font-size="9.5" fill="#56706C">about 2,600 batches</text>
      <text x="970" y="266" font-size="10.5" font-weight="700" letter-spacing="1.2" fill="#EF6A4C">▸ TOP-UPS</text>
      <text x="676" y="440" text-anchor="end" font-size="10.5" font-weight="700" letter-spacing="1.2" fill="#33557D">TO 9 WARDS · THEATRES · ICU ▸</text>`;
    /* hub */
    g += `<rect x="${hub[0]-70}" y="${hub[1]-22}" width="140" height="44" rx="22" fill="#12302D"/><rect x="${hub[0]-70}" y="${hub[1]-22}" width="140" height="44" rx="22" fill="none" stroke="#fff" stroke-width="4"/>
      <text x="${hub[0]}" y="${hub[1]-2}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="19" letter-spacing="1" fill="#fff">MAIN STORE</text><text x="${hub[0]}" y="${hub[1]+12}" text-anchor="middle" font-size="9" fill="#A9C8C3">1,900 items · 41 suppliers</text>`;
    /* stops */
    g += stop(1,110,130,"down") + stop(2,250,130,"down") + stop(3,390,130,"down") + stop(12,590,50,"down") + stop(10,740,50,"down")
      + stop(9,290,270,"down") + stop(7,420,270,"down") + stop(4,730,270,"up") + stop(5,860,270,"up")
      + stop(6,770,400,"down") + stop(8,890,400,"down") + stop(11,1010,400,"down");
    /* connections to other suites */
    D.handoffs.forEach((h,i) => { const x = i ? 1020 : 880, c = SC[h.st], tx = i ? "◂ Admission suite" : "↔ Billing suite";
      g += `<path d="M${i?1010:890},${386} L${x},${342}" stroke="${c}" stroke-width="2.5" stroke-dasharray="3 4"/><rect x="${x-58}" y="318" width="116" height="24" rx="12" fill="#fff" stroke="${c}" stroke-width="2"/><text x="${x}" y="334" text-anchor="middle" font-size="9.5" font-weight="700" fill="${c}">${tx}</text>`; });
    /* bottom band: bought today */
    const by = 480; g += `<rect x="0" y="${by}" width="${W}" height="${H-by}" fill="#12302D"/>
      <text x="30" y="${by+28}" font-size="10" font-weight="700" letter-spacing="1.4" fill="#A9C8C3">BOUGHT TODAY</text><text id="s14amt" x="30" y="${by+60}" font-family="Bebas Neue, sans-serif" font-size="28" fill="#fff">₹${M.boughtToday.toFixed(2)} L</text>
      <text x="190" y="${by+28}" font-size="10" font-weight="700" letter-spacing="1.4" fill="#A9C8C3">FLAGGED BY THE PRICE WATCH</text><text id="s14above" x="190" y="${by+60}" font-family="Bebas Neue, sans-serif" font-size="28" fill="#FFB4A1">₹${M.aboveToday.toFixed(2)} L above price</text>
      <text x="470" y="${by+28}" font-size="10" font-weight="700" letter-spacing="1.4" fill="#A9C8C3">THIS MONTH</text><text x="470" y="${by+60}" font-family="Bebas Neue, sans-serif" font-size="28" fill="#fff">₹${M.bought} CR BOUGHT · ₹${M.lost} L LOST</text>
      <text id="s14last" x="${W-30}" y="${by+46}" text-anchor="end" font-size="11" fill="#D3ECE8">last: ${esc(M.last)}</text>`;
    const map = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Three supply lines meeting at the main store: buying, the store, and the wards. Each part is a stop marked live, testing, being built, late or not started. The wards line is cut after the bill matcher.">${g}</svg>`;

    /* --- KPI dials --- */
    const arc = (f) => { const a = Math.PI*(1-f), x = 59 + 46*Math.cos(a), y = 62 - 46*Math.sin(a); return `M13,62 A46,46 0 0 1 ${x.toFixed(1)},${y.toFixed(1)}`; };
    const dl = k => { const col = k.state==="ahead"?"#1D8A5B":k.state==="watch"?"#E39B12":"#D9472B"; const f = Math.max(.01,Math.min(1,prog(k,k.now))), pf = Math.min(1,prog(k,k.plan)); const pa = Math.PI*(1-pf);
      return `<button class="dl" type="button" data-ref="kpi:${k.id}"><svg viewBox="0 0 118 72" aria-hidden="true"><path d="M13,62 A46,46 0 0 1 105,62" fill="none" stroke="#E4EEEC" stroke-width="12" stroke-linecap="round"/><path d="${arc(f)}" fill="none" stroke="${col}" stroke-width="12" stroke-linecap="round"/>
        <line x1="${(59+34*Math.cos(pa)).toFixed(1)}" y1="${(62-34*Math.sin(pa)).toFixed(1)}" x2="${(59+58*Math.cos(pa)).toFixed(1)}" y2="${(62-58*Math.sin(pa)).toFixed(1)}" stroke="#12302D" stroke-width="3" stroke-linecap="round"/><text x="59" y="66" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="18" fill="#12302D">${Math.round(f*100)}%</text></svg>
        <span><span class="nm">${esc(k.name)}</span><b class="${k.state}">${fmtv(k,k.now)}</b><span class="sw ${k.state}">${STATE_WORD[k.state].toUpperCase()} · ${gapText(k)}</span><span class="rg">From ${fmtv(k,k.base)} · target ${fmtv(k,k.target)}</span></span></button>`; };

    /* --- people as journeys --- */
    const jr = p => { const cc = p.state==="ahead"?["#1D8A5B","#DDF2E7"]:p.state==="watch"?["#B26B00","#FBEBCB"]:["#D9472B","#FDE3DC"]; let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}">${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const b = []; for (let i=0;i<p.due;i++) b.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":""}"></i>`); body = `<span class="stops" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span><span class="meta"><b>${p.done}</b> of ${p.due} done${p.late?` · <b style="color:var(--bad)">${p.late}</b> late`:""}</span>`; }
      return `<button class="jr" type="button" data-ref="per:${p.key}"><span class="top"><span class="nm"><span class="av">${esc(initials(p.name))}</span><span>${esc(p.name)}<small>${esc(p.role)}</small></span></span><span class="chip" style="color:${cc[0]};background:${cc[1]}">${PERSON_WORD[p.state]}</span></span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</button>`; };

    /* --- money: out and back, month by month to date --- */
    const CW = 760, CH = 320, x0 = 50, x1 = 740, y0 = 30, y1 = 260, n = D.cumMonths.length, vmax = 70, bw = (x1-x0)/n;
    const Y = v => y1 - (y1-y0)*v/vmax;
    let c = ""; [0,10,20,30,40,50,60,70].forEach(v => c += `<line x1="${x0}" x2="${x1}" y1="${Y(v)}" y2="${Y(v)}" stroke="${v?"#EAF1EF":"#12302D"}" stroke-width="${v?1:2}"/><text x="${x0-8}" y="${Y(v)+4}" text-anchor="end" font-size="10" fill="#56706C">${v}</text>`);
    const fi = D.breakeven.foreIdx;
    D.cumMonths.forEach((m,i) => { const cx = x0 + i*bw + bw/2, fore = i > D.actualTo, w = 16;
      c += `<g data-ref="month:${i}" data-nopen style="cursor:help"><rect x="${cx-bw/2}" y="${y0-10}" width="${bw}" height="${y1-y0+40}" fill="${i===fi?"#F1F6F4":"transparent"}"/>
        <rect x="${cx-w-2}" y="${Y(D.cumSpend[i])}" width="${w}" height="${y1-Y(D.cumSpend[i])}" rx="8" fill="#EF6A4C" fill-opacity="${fore?.35:1}"/>
        <rect x="${cx+2}" y="${Y(D.cumFore[i])}" width="${w}" height="${y1-Y(D.cumFore[i])}" rx="8" fill="#0E7C72" fill-opacity="${fore?.35:1}"/>
        <text x="${cx}" y="${y1+18}" text-anchor="middle" font-size="11" font-weight="600" fill="${fore?"#56706C":"#12302D"}">${m}</text></g>`; });
    c += `<path d="${D.cumPlan.map((v,i)=>(i?"L":"M")+(x0+i*bw+bw/2)+","+Y(v)).join(" ")}" fill="none" stroke="#12302D" stroke-width="1.6" stroke-dasharray="5 4"/>`;
    const bx = x0 + fi*bw + bw/2; c += `<circle cx="${bx}" cy="${Y(D.cumFore[fi])-22}" r="11" fill="#fff" stroke="#1D8A5B" stroke-width="5"/><text x="${bx+18}" y="${Y(D.cumFore[fi])-18}" font-size="11" font-weight="700" fill="#1D8A5B">break-even, ${D.breakeven.fore}</text>`;
    const pi = D.breakeven.planIdx; c += `<text x="${x0+pi*bw+bw/2}" y="${Y(D.cumPlan[pi])-10}" text-anchor="middle" font-size="10" fill="#12302D">plan: ${D.breakeven.plan}</text>`;
    c += `<g font-size="11" fill="#12302D"><rect x="${x0}" y="${CH-24}" width="12" height="12" rx="6" fill="#EF6A4C"/><text x="${x0+18}" y="${CH-14}">Money out to date</text><rect x="${x0+150}" y="${CH-24}" width="12" height="12" rx="6" fill="#0E7C72"/><text x="${x0+168}" y="${CH-14}">EBITDA back to date</text><line x1="${x0+320}" x2="${x0+342}" y1="${CH-18}" y2="${CH-18}" stroke="#12302D" stroke-dasharray="5 4"/><text x="${x0+348}" y="${CH-14}">Plan · ₹ lakh · faded: forecast</text></g>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="Money out and EBITDA back to date, side by side for each month; EBITDA back passes money out in ${D.breakeven.fore}.">${c}</svg>`;

    /* countdown ring */
    const ringF = Math.max(.05, 1 - D.milestone.days/30), ra = 2*Math.PI*24;
    const ring = `<svg viewBox="0 0 62 62" aria-hidden="true"><circle cx="31" cy="31" r="24" fill="none" stroke="#24504B" stroke-width="7"/><circle cx="31" cy="31" r="24" fill="none" stroke="#EF6A4C" stroke-width="7" stroke-linecap="round" stroke-dasharray="${(ra*ringF).toFixed(1)} ${ra.toFixed(1)}" transform="rotate(-90 31 31)"/><text x="31" y="38" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="22" fill="#fff">${D.milestone.days}</text></svg>`;
    const BC = ["#12302D","#0E7C72","#E39B12","#33557D","#1D8A5B","#56706C","#EF6A4C"];
    return `<div class="s14"><div class="wrap">
      <nav class="badges" aria-label="Suite sections">${TABS.map((t,i)=>`<button class="bd ${i?"":"on"}" type="button" data-tab="${t[0]}" style="--c:${BC[i]}"><i aria-hidden="true">${i+1}</i>${t[1]}</button>`).join("")}</nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="status" aria-label="Pulse strip">${status}</div></div>
      <div class="alerts" aria-label="Watch list and next go-live">${D.watch.map(w=>`<button class="al" type="button" data-ref="${w.ref}"><i aria-hidden="true"></i><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}
        <button class="ring" type="button" data-ref="part:${D.milestone.part}">${ring}<span>days to the next go-live<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to see every line →</p><div class="map">${map}</div>
        <div class="legend"><span><i style="background:#0E7C72"></i>Buying</span><span><i style="background:#EF6A4C"></i>The store</span><span><i style="background:#33557D"></i>The wards</span><span>· Stops:</span><span><i style="background:#1D8A5B"></i>Live</span><span><i style="background:#E39B12"></i>Testing</span><span><i style="background:#fff;border:2px dashed #9AAFAB"></i>Being built or not started</span><span><i style="background:#D9472B"></i>Late</span><span>· Data as of ${esc(D.asOf)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3><p>Arc: how far from the start to the target we are today · black tick: this week's plan</p></div><div class="dials">${D.kpis.map(dl).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="journeys">${D.people.map(jr).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="pairs"><div class="chart">${chart}</div>
          <div class="mlist">
            <button type="button" data-ref="month:1"><span>Subscription, each month</span><b>${L(D.spend[0].v[1])}</b></button>
            <button type="button" data-ref="month:1"><span>Salary of the Stores Lead we recommended, each month</span><b>${L(D.spend[1].v[1])}</b></button>
            <button type="button" data-ref="month:1"><span>One-time so far (barcode scanners, ward phones)</span><b>${L(sum(D.spend[2].v))}</b></button>
            <button type="button" data-ref="health:0"><span>Extra revenue so far, from items now billed</span><b>${L(revTotal)}</b></button>
            <button type="button" data-ref="health:0"><span>EBITDA now, and at full run, each month</span><b>${L(D.ebitda[1])} → ${L(D.runRate.ebitda)}</b></button>
            <button type="button" class="why" data-ref="health:0"><span>Break-even ${D.breakeven.fore}, ${D.breakeven.late} late. See why</span><b>›</b></button>
          </div></div></section>
    </div></div>`;
  },
  after(){
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { document.querySelectorAll(".s14 animateMotion").forEach(a=>a.remove()); return; }
    buyTicker("s14", ".s14 .pc");
  }
});
