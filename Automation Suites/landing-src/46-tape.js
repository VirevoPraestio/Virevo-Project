/* ===== Financial Health, option 2: cobalt and tangerine, thirty closed days for every measure, the causes on the same dates, the feeds below ===== */
SCHEMES.push({
  key:"tape", letter:"2", name:"Cobalt and tangerine",
  note:"<b>Option 2 · cobalt and tangerine.</b> The last thirty closed days for every measure, each day marked against what was expected that day, with the total since the start at the end of the row. Below them, the causes laid on the same dates, so you can see which one started when a measure turned.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#142040","--sh-mute":"#58627C","--sh-line":"#DCE2EF","--sh-card":"#F5F7FC","--c-ok":"#14845A","--c-warn":"#B26B00","--c-bad":"#D13A2A","--pk-bg":"#142040","--pk-fg":"#FFFFFF","--pk-line":"#F2711C","--pk-r":"6px","--sh-r":"12px" },
  fab:18,
  blocks:{ nav:".topbar", pulse:".tiles", watch:".alerts", countdown:".flip", hero:".tape", kpis:".twins", recovery:".inbox", team:".roster", money:".net" },
  css:`
.s16{--bg:#F4F6FB;--ink:#142040;--mute:#58627C;--co:#1F4FD1;--co2:#DCE5FB;--ta:#F2711C;--ta2:#FDE4D2;--ok:#14845A;--warn:#B26B00;--bad:#D13A2A;--line:#DCE2EF;
  background:var(--bg);color:var(--ink);padding:0 0 90px;overflow-x:clip}
.s16 .wrap{max-width:1240px;margin:0 auto;padding:0 16px}
.s16 .topbar{background:var(--co);position:sticky;top:0;z-index:5}
.s16 .topbar .wrap{display:flex;flex-wrap:wrap;gap:2px;align-items:stretch}
.s16 .tb{border:0;background:transparent;color:#DCE5FB;font-size:12.5px;font-weight:600;padding:12px 14px;min-height:48px;border-bottom:4px solid transparent}
.s16 .tb:hover{color:#fff;background:rgba(255,255,255,.08)}
.s16 .tb.on{color:#fff;border-bottom-color:var(--ta)}
.s16 .tb em{font-style:normal;background:var(--ta);color:#fff;border-radius:999px;padding:1px 7px;margin-left:6px;font-size:11px}
.s16 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:22px 0 16px}
.s16 .head small{font-size:12px;font-weight:700;letter-spacing:.14em;color:var(--co)}
.s16 h2{font-family:var(--f-num);font-weight:400;font-size:80px;line-height:.86;margin:6px 0 0;letter-spacing:.01em}
.s16 h2 span{color:var(--ta)}
.s16 .head p{margin:8px 0 0;font-size:13px;color:var(--mute)}
.s16 .tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.s16 .tl{position:relative;background:#fff;border:0;border-radius:10px;padding:10px 14px;text-align:left;color:inherit;min-width:132px;box-shadow:0 1px 0 var(--line),0 8px 18px rgba(20,32,64,.06);overflow:hidden}
.s16 .tl::after{content:"";position:absolute;right:0;top:0;border-style:solid;border-width:0 22px 22px 0;border-color:transparent var(--c) transparent transparent}
.s16 .tl span{display:block;font-size:10.5px;letter-spacing:.12em;font-weight:700;color:var(--mute)}
.s16 .tl b{display:block;font-family:var(--f-num);font-weight:400;font-size:32px;line-height:1}
.s16 .tl em{font-style:normal;font-size:11px;color:var(--co)}
.s16 .alerts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.7fr);gap:12px;margin-bottom:16px}
.s16 .al{display:grid;grid-template-columns:34px minmax(0,1fr) 14px;gap:10px;align-items:center;background:#fff;border:0;border-radius:10px;padding:10px 12px;text-align:left;color:inherit;font-size:12.5px;font-weight:600;box-shadow:0 1px 0 var(--line)}
.s16 .al i{display:grid;place-items:center;width:30px;height:30px;border-radius:8px;background:var(--ta);color:#fff;font-style:normal;font-family:var(--f-num);font-size:18px}
.s16 .al small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s16 .al::after{content:"›";color:var(--ta);font-size:20px}
.s16 .al:hover{box-shadow:0 0 0 2px var(--ta)}
.s16 .flip{display:grid;grid-template-columns:auto minmax(0,1fr);gap:12px;align-items:center;background:var(--ink);color:#fff;border:0;border-radius:10px;padding:10px 14px;text-align:left}
.s16 .flip b{position:relative;display:grid;place-items:center;width:52px;height:56px;border-radius:6px;background:linear-gradient(#26345E 50%,#1B2850 50%);font-family:var(--f-num);font-weight:400;font-size:40px;color:var(--ta)}
.s16 .flip b::after{content:"";position:absolute;left:0;right:0;top:50%;height:1px;background:#0D1631}
.s16 .flip span{font-size:12px;font-weight:700} .s16 .flip small{display:block;font-weight:400;font-size:11px;color:#A9B6D8}
.s16 .tape{border-radius:12px;background:#fff;overflow-x:auto;box-shadow:0 1px 0 var(--line),0 14px 30px rgba(20,32,64,.07)}
.s16 .tape svg{display:block;width:100%;min-width:980px;height:auto}
.s16 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--co)}
.s16 .rw{cursor:pointer} .s16 .rw:focus{outline:none} .s16 .rw:focus .hl,.s16 .rw:hover .hl{opacity:1}
.s16 .hl{opacity:0;transition:opacity .12s}
.s16 .cell{transition:transform .12s;transform-box:fill-box;transform-origin:center} .s16 .rw:hover .cell{transform:scaleY(1.12)}
.s16 .pc{cursor:pointer} .s16 .pc:hover .fc,.s16 .pc:focus .fc{stroke:var(--ta);stroke-width:2.5} .s16 .pc:focus{outline:none}
.s16 .live{animation:s16b 1.6s ease-in-out infinite}
@keyframes s16b{50%{opacity:.35}}
.s16 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:10px}
.s16 .legend i{display:inline-block;width:14px;height:12px;border-radius:2px;vertical-align:-1px;margin-right:6px}
.s16 .zone{margin-top:44px;scroll-margin-top:70px;border-radius:12px}
.s16 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px 16px;margin-bottom:14px}
.s16 .zh h3{font-family:var(--f-num);font-weight:400;font-size:40px;margin:0;line-height:1;padding-left:14px;border-left:8px solid var(--ta)}
.s16 .zh p{margin:0;font-size:12.5px;color:var(--mute)}
.s16 .pick{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:12px;font-weight:700;color:var(--co)}
.s16 .pick select{font:inherit;font-weight:500;font-size:12.5px;padding:8px 10px;border:0;border-radius:8px;background:var(--co2);color:var(--ink);min-height:40px;max-width:270px}
.s16 .twins{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px}
.s16 .tw{background:#fff;border:0;border-radius:12px;padding:12px 14px;text-align:left;color:inherit;box-shadow:0 1px 0 var(--line),0 6px 14px rgba(20,32,64,.05);transition:transform .15s;position:relative}
.s16 .tw:hover,.s16 .tw:focus-visible{transform:translateY(-2px);box-shadow:0 0 0 2px var(--co)}
.s16 .tw.ch::before{content:"YOUR MEASURE";position:absolute;right:12px;top:12px;font-size:9.5px;font-weight:700;letter-spacing:.08em;color:var(--ta)}
.s16 .tw .nm{display:block;font-size:13px;font-weight:600;padding-right:90px}
.s16 .tw .st{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.05em;margin:4px 0 8px}
.s16 .tb2{display:grid;grid-template-columns:72px minmax(0,1fr) auto;gap:8px;align-items:center;font-size:11px;color:var(--mute);margin-top:6px}
.s16 .tb2 b{font-family:var(--f-num);font-weight:400;font-size:20px;color:var(--ink)}
.s16 .trk{position:relative;height:12px;border-radius:6px;background:var(--co2)}
.s16 .trk i{position:absolute;left:0;top:0;bottom:0;border-radius:6px;background:var(--c)}
.s16 .trk u{position:absolute;top:-4px;bottom:-4px;width:3px;margin-left:-1.5px;background:var(--ink);border-radius:2px}
.s16 .ahead{color:var(--ok)} .s16 .watch{color:var(--warn)} .s16 .off{color:var(--bad)}
.s16 .inbox{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:18px;align-items:start}
.s16 .q h4,.s16 .tline h4{margin:0 0 10px;font-size:12px;letter-spacing:.1em;font-weight:700;color:var(--co)}
.s16 .dc{display:block;background:#fff;border:0;border-radius:12px;padding:14px;margin-bottom:12px;text-align:left;color:inherit;cursor:pointer;box-shadow:0 0 0 2px var(--ta),0 10px 20px rgba(242,113,28,.12)}
.s16 .dc.approved{box-shadow:0 0 0 2px var(--ok)} .s16 .dc.held{box-shadow:0 0 0 2px var(--line);opacity:.8}
.s16 .dc .tp{display:flex;justify-content:space-between;gap:10px;font-size:10.5px;font-weight:700;letter-spacing:.06em;color:var(--ta)}
.s16 .dc.approved .tp{color:var(--ok)} .s16 .dc.held .tp{color:var(--mute)}
.s16 .dc .t{display:block;font-size:14px;font-weight:600;margin:4px 0 8px}
.s16 .dc .nums{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;font-size:11px;color:var(--mute)}
.s16 .dc .nums b{display:block;font-family:var(--f-num);font-weight:400;font-size:19px;color:var(--ink);line-height:1.1}
.s16 .fh-dec{display:flex;gap:8px;margin-top:12px}
.s16 .fh-dec button{flex:1;min-height:42px;border-radius:999px;font-weight:700;font-size:13px;border:0}
.s16 .fh-dec button:first-child{background:var(--ta);color:#fff} .s16 .fh-dec button:last-child{background:var(--co2);color:var(--co)}
.s16 .tline{position:relative;padding-left:22px}
.s16 .tline::before{content:"";position:absolute;left:7px;top:28px;bottom:6px;width:3px;background:var(--co2);border-radius:2px}
.s16 .ti{position:relative;display:block;background:#fff;border:0;border-radius:10px;padding:9px 12px;margin-bottom:9px;text-align:left;color:inherit;font-size:12.5px;font-weight:600;box-shadow:0 1px 0 var(--line);cursor:pointer}
.s16 .ti::before{content:"";position:absolute;left:-21px;top:12px;width:11px;height:11px;border-radius:50%;background:var(--c);box-shadow:0 0 0 3px var(--bg)}
.s16 .ti small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s16 .ti .k{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.05em;color:var(--c);margin-right:6px}
.s16 .ti.log{background:transparent;box-shadow:none;padding:2px 12px;font-weight:400;color:var(--mute);cursor:default}
.s16 .roster{background:#fff;border-radius:12px;box-shadow:0 1px 0 var(--line);overflow:hidden}
.s16 .rr{display:grid;grid-template-columns:minmax(0,1.2fr) 110px minmax(0,1.4fr) minmax(0,1.4fr);gap:12px;align-items:center;width:100%;border:0;border-bottom:1px solid var(--line);background:transparent;padding:10px 14px;text-align:left;color:inherit;font-size:12.5px}
.s16 .rr:hover,.s16 .rr:focus-visible{background:var(--co2)}
.s16 .rr .nm{font-weight:700} .s16 .rr .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s16 .rr .chip{justify-self:start;font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:999px}
.s16 .sq{display:flex;gap:3px;flex-wrap:wrap} .s16 .sq i{width:14px;height:14px;border-radius:3px;background:var(--co2)} .s16 .sq i.y{background:var(--co)} .s16 .sq i.l{background:var(--ta)}
.s16 .rr ul{list-style:none;margin:0;padding:0;display:grid;gap:2px;font-size:12px}
.s16 .rr li::before{content:"· ";color:var(--mute)} .s16 .rr li.y{color:var(--mute);text-decoration:line-through} .s16 .rr li.l{color:var(--bad);font-weight:600}
.s16 .rr .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s16 .rr .nx{font-size:11.5px;color:var(--mute)}
.s16 .vt{display:inline-flex;background:#fff;border-radius:8px;padding:3px;box-shadow:0 0 0 1px var(--line)}
.s16 .vt button{border:0;background:transparent;border-radius:6px;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:var(--ink)}
.s16 .vt button[aria-pressed="true"]{background:var(--co);color:#fff}
.s16 .net{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s16 .chart{background:#fff;border-radius:12px;padding:12px;overflow-x:auto;box-shadow:0 1px 0 var(--line)}
.s16 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s16 .mlist{display:grid;gap:8px}
.s16 .mlist button{display:flex;justify-content:space-between;gap:12px;align-items:baseline;background:#fff;border:0;border-radius:10px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12.5px;box-shadow:0 1px 0 var(--line)}
.s16 .mlist b{font-family:var(--f-num);font-weight:400;font-size:23px;color:var(--ink);white-space:nowrap}
.s16 .mlist .why{background:var(--ta);color:#FFF1E6} .s16 .mlist .why b{color:#fff}
@media (max-width:1000px){ .s16 .head{grid-template-columns:1fr} .s16 .alerts{grid-template-columns:1fr 1fr} .s16 .inbox,.s16 .net{grid-template-columns:1fr} .s16 .rr{grid-template-columns:minmax(0,1fr) auto} .s16 .rr>span:nth-child(n+3){grid-column:1/-1} }
@media (max-width:600px){ .s16 .swipe{display:block} .s16 h2{font-size:56px} .s16 .tiles{grid-template-columns:1fr 1fr} .s16 .alerts{grid-template-columns:1fr} .s16 .tb{padding:10px 9px;font-size:12px} .s16 .topbar{position:static} }
`,
  render(){
    const PC = { live:"#14845A", testing:"#E39B12", building:"#9AA6C2", blocked:"#D13A2A", notstarted:"#C8D0E2" };
    const live = countParts("live"), wait = D.actions.filter(a=>a.st==="awaiting").length;
    const tl = (c, lab, val, sub, attr) => `<button class="tl" type="button" ${attr} style="--c:${c}"><span>${lab}</span><b>${val}</b><em>${sub}</em></button>`;
    const tiles = tl("#14845A","PARTS LIVE",`${live} / 12`,"plan 7",`data-tab="links"`) + tl("#E39B12","KPIS ON COURSE",`${onCourse} / ${D.kpis.length}`,`plan ${D.kpis.length}`,`data-tab="measures"`)
      + tl("#1F4FD1","EBITDA BACK / OUT",`${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}`,`₹ lakh · plan ${D.cumPlan[D.actualTo].toFixed(1)} back`,`data-ref="health:0"`) + tl("#D13A2A","BREAK-EVEN",D.breakeven.fore.toUpperCase(),`plan ${D.breakeven.plan}`,`data-ref="health:0"`);

    /* --- thirty days --- */
    const N = 30, dates = fhDates(N), W = 1100, lx = 20, cx0 = 230, cx1 = 900, cw = (cx1-cx0)/N, rh = 34, top = 64;
    const colr = v => v >= 0.02 ? "#1F4FD1" : v >= 0 ? "#8FA9EC" : v > -0.03 ? "#F9B98C" : v > -0.08 ? "#F2711C" : "#D13A2A";
    let g = `<text x="${lx}" y="24" font-size="11" font-weight="700" letter-spacing="1.4" fill="#1F4FD1">THE LAST ${N} CLOSED DAYS, EACH AGAINST WHAT WAS EXPECTED THAT DAY</text>`;
    dates.forEach((d,i) => { if (i % 5 === 4 || i === N-1) g += `<text x="${cx0 + i*cw + cw/2}" y="${top-10}" text-anchor="middle" font-size="9.5" fill="${i===N-1?"#F2711C":"#58627C"}" font-weight="${i===N-1?700:400}">${d}</text>`; });
    g += `<text x="${cx1+20}" y="${top-10}" font-size="9.5" font-weight="700" letter-spacing=".8" fill="#58627C">${esc(D.sinceLabel.toUpperCase())}</text>`;
    D.kpis.forEach((k,r) => { const y = top + r*rh, s = fhSeries(k, N), c = k.state==="ahead"?"#14845A":k.state==="watch"?"#B26B00":"#D13A2A";
      g += `<g class="rw" data-ref="kpi:${k.id}" tabindex="0" role="button" aria-label="${esc(k.name)}: ${fmtv(k,k.day[1])} on ${esc(D.dayLabel)} against ${fmtv(k,k.day[0])} expected; ${fhPct(k)} ${esc(D.sinceLabel)}">
        <rect class="hl" x="8" y="${y}" width="${W-16}" height="${rh-4}" rx="6" fill="#EEF2FC"/>
        <circle cx="${lx+6}" cy="${y+rh/2-2}" r="5" fill="${c}"/><text x="${lx+18}" y="${y+rh/2+2}" font-size="12" font-weight="600" fill="#142040">${esc(k.short)}</text>${D.core.includes(k.id)?"":`<text x="${cx0-10}" y="${y+rh/2+2}" text-anchor="end" font-size="9" font-weight="700" fill="#F2711C">YOURS</text>`}
        ${s.map((v,i)=>`<rect class="cell" x="${cx0 + i*cw + 1}" y="${y+3}" width="${cw-2}" height="${rh-10}" rx="3" fill="${colr(v)}"/>`).join("")}
        <rect x="${cx0 + (N-1)*cw - 1}" y="${y+1}" width="${cw+2}" height="${rh-6}" rx="4" fill="none" stroke="#142040" stroke-width="1.5"/>
        <text x="${cx1+20}" y="${y+rh/2+3}" font-family="Bebas Neue, sans-serif" font-size="19" fill="${k.tdState==="ahead"?"#14845A":k.tdState==="watch"?"#B26B00":"#D13A2A"}">${fhPct(k)}</text><text x="${cx1+76}" y="${y+rh/2+2}" font-size="10" fill="#58627C">${fmtv(k,k.td[1])}</text></g>`; });
    /* causes on the same dates */
    const cy = top + D.kpis.length*rh + 34, ch = 22, start = new Date(2026, 8, 24);
    const idxOf = d => { const m = /(\d+) (Sep|Oct)/.exec(d.since); if (!m) return 0; const dt = new Date(2026, m[2]==="Sep"?8:9, +m[1]); return Math.max(0, Math.round((dt - start)/864e5)); };
    g += `<text x="${lx}" y="${cy-12}" font-size="11" font-weight="700" letter-spacing="1.4" fill="#1F4FD1">CAUSES, ON THE DATES THEY WERE ACTIVE</text>`;
    D.drivers.forEach((d,r) => { const y = cy + r*ch, i0 = idxOf(d), col = d.lift ? "#14845A" : d.e ? "#F2711C" : "#9AA6C2";
      g += `<g class="pc" data-ref="drv:${d.id}" tabindex="0" role="button" aria-label="Cause: ${esc(d.name)}, ${esc(d.since)}">
        <text x="${lx}" y="${y+14}" font-size="10.5" fill="#142040">${esc(d.name.length > 34 ? d.name.slice(0,33)+"…" : d.name)}</text>
        <rect class="fc" x="${cx0 + i0*cw + 1}" y="${y+3}" width="${(N-i0)*cw - 2}" height="${ch-8}" rx="7" fill="${col}" fill-opacity="${d.lift?.75:.85}" stroke="${col}"/>
        <text x="${cx1+20}" y="${y+14}" font-size="10.5" font-weight="700" fill="${col}">${d.e?fhL(d.e)+" a day":"no direct effect"}</text>
        ${i0>0?`<line x1="${cx0 + i0*cw}" x2="${cx0 + i0*cw}" y1="${top}" y2="${y+3}" stroke="${col}" stroke-dasharray="2 3" opacity=".6"/>`:""}</g>`; });
    /* feeds */
    const fy = cy + D.drivers.length*ch + 40, fw = 82, fg = 6, fx0 = (W - (12*fw + 11*fg))/2;
    g += `<text x="${fx0}" y="${fy-12}" font-size="11" font-weight="700" letter-spacing="1.4" fill="#1F4FD1">FEEDS READ EVERY MORNING AT 6 AM</text>`;
    D.parts.forEach((p,i) => { const x = fx0 + i*(fw+fg), c = PC[p.st], soft = p.st==="building"||p.st==="notstarted";
      g += `<g class="pc" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}"><rect class="fc" x="${x}" y="${fy}" width="${fw}" height="58" rx="8" fill="${soft?"#F4F6FB":"#fff"}" stroke="${c}" stroke-width="1.5" ${soft?'stroke-dasharray="4 3"':""}/><rect x="${x}" y="${fy}" width="${fw}" height="5" rx="2" fill="${c}"/>
        ${p.st==="live"?`<circle class="live" cx="${x+fw-9}" cy="${fy+13}" r="3.5" fill="#14845A"/>`:""}
        <foreignObject x="${x+5}" y="${fy+7}" width="${fw-12}" height="50"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 9px/1.2 Poppins,sans-serif;color:#142040;height:48px;display:flex;flex-direction:column;justify-content:space-between"><span><b style="font-family:'Bebas Neue';font-weight:400;font-size:13px;color:#1F4FD1">${p.id}</b> ${esc(p.short)}</span><span style="font-size:8.5px;font-weight:700;color:${c}">${PART_WORD[p.st].toUpperCase()}</span></div></foreignObject></g>`; });
    const H = fy + 74;
    const tape = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Thirty closed days for each measure against what was expected, the total since the start at the end of each row, the causes on the dates they were active, and the twelve feeds.">${g}</svg>`;

    /* --- KPI twins --- */
    const bar = (k, e, a, lab, st) => { const mx = Math.max(e, a) * 1.15, w = Math.min(100, a/mx*100), p = e/mx*100; const col = st==="ahead"?"#14845A":st==="watch"?"#E39B12":"#D13A2A";
      return `<span class="tb2"><span>${lab}</span><span class="trk" style="--c:${col}"><i style="width:${w.toFixed(1)}%"></i><u style="left:${p.toFixed(1)}%"></u></span><b class="${st}">${fmtv(k,a)}</b></span>`; };
    const tw = k => `<button class="tw ${D.core.includes(k.id)?"":"ch"}" type="button" data-ref="kpi:${k.id}"><span class="nm">${esc(k.name)}</span><span class="st ${k.state}">${STATE_WORD[k.state].toUpperCase()} · ${fhGap(k,k.day[0],k.day[1])} on ${esc(D.dayLabel)}</span>
      ${bar(k,k.day[0],k.day[1],esc(D.dayLabel),k.dayState)}${bar(k,k.td[0],k.td[1],esc(D.sinceLabel.replace("since ","Since ")),k.tdState)}</button>`;

    /* --- recovery: the CEO's queue, then everything else in time order --- */
    const dc = a => `<div class="dc ${a.st}" role="button" tabindex="0" data-ref="act:${a.id}"><span class="tp"><span>${esc(FH_ST[a.st].toUpperCase())}</span><span>${esc(a.st==="awaiting"?a.wait:"")}</span></span><span class="t">${esc(a.t)}</span>
      <span class="nums"><span>Gain<b>${fhL(a.gain)}/day</b></span><span>Cost<b>${esc(/^No /.test(a.cost)?"None":a.cost.replace(/ for 10 days| a day of discount/,"").replace("About ",""))}</b></span><span>Net<b>${esc(a.net.split(";")[0].replace(" over 10 days","/10 days").replace(" a month","/month").replace(" over 30 days","/30 days"))}</b></span></span>${fhDecideBtns(a)}</div>`;
    const ceo = D.actions.filter(a=>["awaiting","approved","held"].includes(a.st));
    const other = D.actions.filter(a=>["done","advised"].includes(a.st));
    const ti = a => `<div class="ti" role="button" tabindex="0" data-ref="act:${a.id}" style="--c:${a.st==="done"?"#1F4FD1":"#F2711C"}"><span class="k">${a.st==="done"?"DONE":"ADVISED"}</span>${esc(a.t)}<small>${esc(a.when)}${a.st==="advised"?` · ${esc(fhWho(a.who))}: ${esc(a.reply)}`:""}${a.gain?` · ${fhL(a.gain)} a day`:""}</small></div>`;
    const inbox = `<div class="q"><h4>FOR THE CEO TO CONFIRM · ${wait} WAITING</h4>${ceo.map(dc).join("")}</div>
      <div class="tline"><h4>DONE AND ADVISED BY THE SUITE</h4>${D.runLog.slice(0,4).map(r=>`<div class="ti log" style="--c:#C8D0E2"><b>${r[0]}</b> ${esc(r[1])}</div>`).join("")}${other.map(ti).join("")}</div>`;

    /* --- roster --- */
    const rr = p => { const cc = p.state==="ahead"?["#14845A","#DDF2E8"]:p.state==="watch"?["#B26B00","#FBEBCB"]:["#D13A2A","#FBE1DD"]; let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":/^(late|waiting)/.test(String(t[1]))?"l":""}">${esc(t[0])}${t[1]!==1?` · ${esc(t[1])}`:""}</li>`).join("")}</ul>`;
      else { const b = []; for (let i=0;i<p.due;i++) b.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":""}"></i>`); body = `<span class="sq" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span>`; }
      return `<button class="rr" type="button" data-ref="per:${p.key}"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="chip" style="color:${cc[0]};background:${cc[1]}">${PERSON_WORD[p.state]}</span><span>${body}</span>${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</button>`; };

    /* --- money: net position to date --- */
    const CW = 760, CH = 300, x0 = 50, x1 = 740, mid = 140, n = D.cumMonths.length, bw = (x1-x0)/n, sc = 2.2;
    let c = ""; [-20,0,20,40].forEach(v => c += `<line x1="${x0}" x2="${x1}" y1="${mid - v*sc}" y2="${mid - v*sc}" stroke="${v?"#EEF2FA":"#142040"}" stroke-width="${v?1:2}"/><text x="${x0-8}" y="${mid - v*sc + 4}" text-anchor="end" font-size="10" fill="#58627C">${v}</text>`);
    const net = D.cumFore.map((v,i)=>Math.round((v-D.cumSpend[i])*10)/10);
    net.forEach((v,i) => { const x = x0 + i*bw + 12, w = bw - 24, fore = i > D.actualTo, h = Math.abs(v)*sc;
      c += `<g data-ref="month:${i}" data-nopen style="cursor:help"><rect x="${x-12}" y="10" width="${bw}" height="${CH-40}" fill="transparent"/><rect x="${x}" y="${v>=0?mid-h:mid}" width="${w}" height="${Math.max(2,h)}" rx="4" fill="${v>=0?"#1F4FD1":"#F2711C"}" fill-opacity="${fore?.4:1}"/>
        <text x="${x+w/2}" y="${v>=0?mid-h-6:mid+h+14}" text-anchor="middle" font-size="10" font-weight="600" fill="${v>=0?"#1F4FD1":"#C8580F"}">${v>0?"+":""}${v}</text><text x="${x+w/2}" y="${CH-18}" text-anchor="middle" font-size="11" font-weight="600" fill="${fore?"#58627C":"#142040"}">${D.cumMonths[i]}</text></g>`; });
    c += `<text x="${x0}" y="${CH-2}" font-size="11" fill="#142040">EBITDA back less money out, to date · orange: still short · blue: paid for itself · faded: forecast · ₹ lakh</text>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="Net position to date by month; it turns positive in ${D.breakeven.fore}.">${c}</svg>`;

    const name = D.suite.split(" ");
    return `<div class="s16"><nav class="topbar" aria-label="Suite sections"><div class="wrap">${D.tabs.map((t,i)=>`<button class="tb ${i?"":"on"}" type="button" data-tab="${t[0]}">${t[1]}${t[0]==="recovery"&&wait?`<em>${wait}</em>`:""}</button>`).join("")}</div></nav><div class="wrap">
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(name[0])} <span>${esc(name.slice(1).join(" "))}</span></h2><p>Every measure checked at 6 AM against the day and ${esc(D.sinceLabel)} · data as of ${esc(D.asOf)}</p></div>
        <div class="tiles" aria-label="Pulse strip">${tiles}</div></div>
      <div class="alerts" aria-label="Watch list and next go-live">${D.watch.map((w,i)=>`<button class="al" type="button" data-ref="${w.ref}"><i aria-hidden="true">${i+1}</i><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}
        <button class="flip" type="button" data-ref="part:${D.milestone.part}"><b>${D.milestone.days}</b><span>days to the next go-live<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to see all thirty days →</p><div class="tape">${tape}</div>
        <div class="legend"><span><i style="background:#1F4FD1"></i>2% or more better than expected</span><span><i style="background:#8FA9EC"></i>On expected</span><span><i style="background:#F9B98C"></i>Up to 3% short</span><span><i style="background:#F2711C"></i>3 to 8% short</span><span><i style="background:#D13A2A"></i>More than 8% short</span><span>· Outlined: ${esc(D.dayLabel)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3>${fhChooser("pick")}</div><div class="twins">${D.kpis.map(tw).join("")}</div><p style="font-size:12px;color:var(--mute);margin:10px 0 0">Bar: actual · black tick: expected · top bar ${esc(D.dayLabel)}, lower bar ${esc(D.sinceLabel)}</p></section>
      <section class="zone" data-zone="recovery"><div class="zh"><h3>Recovery</h3><p>Decisions first, then what the suite has already done and advised</p></div><div class="inbox">${inbox}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="roster">${D.people.map(rr).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="net"><div class="chart">${chart}</div>
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
  after(){}
});
