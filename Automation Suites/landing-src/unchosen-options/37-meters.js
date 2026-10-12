/* ===== Billing & Insurance, option 2: the meter wall (wine and champagne) ===== */
SCHEMES.push({
  key:"meters", letter:"2", name:"Wine and champagne",
  note:"<b>Option 2 · wine and champagne.</b> Every charge line is a meter on one wall, all wired to a central totaliser that counts what is posted today and sends bills on.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#2E0F1A","--sh-mute":"#6E5560","--sh-line":"#EAD9DC","--sh-card":"#FBF6F6","--c-ok":"#1E7F54","--c-warn":"#A9690A","--c-bad":"#C0263B","--pk-bg":"#2E0F1A","--pk-fg":"#FFF7EE","--pk-line":"#C8A24A","--pk-r":"8px","--sh-r":"14px" },
  fab:18,
  css:`
.s7{--bg:#F7F0EE;--ink:#2E0F1A;--mute:#6E5560;--wine:#8A1538;--wine2:#4A0C20;--champ:#C8A24A;--champ2:#E9D29A;--ok:#1E7F54;--warn:#A9690A;--bad:#C0263B;--line:#EAD9DC;
  background:var(--bg);color:var(--ink);padding:18px 16px 90px;overflow-x:clip}
.s7 .wrap{max-width:1240px;margin:0 auto}
.s7 .keys{display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;background:linear-gradient(180deg,#4A0C20,#33081A);border-radius:14px;padding:10px 14px;box-shadow:0 12px 26px rgba(74,12,32,.25)}
.s7 .odo{display:flex;gap:2px;align-items:center}
.s7 .odo small{font-size:9.5px;letter-spacing:.16em;color:var(--champ2);font-weight:600;margin-right:8px}
.s7 .wh{display:inline-grid;place-items:center;min-width:.7em;height:1.25em;padding:0 .06em;background:linear-gradient(180deg,#000 0%,#2a2a2a 30%,#2a2a2a 70%,#000 100%);color:var(--champ2);font-family:var(--f-num);border-radius:2px;line-height:1}
.s7 .odo .wh{font-size:24px}
.s7 .ks{display:flex;flex-wrap:wrap;gap:6px}
.s7 .key{display:flex;flex-direction:column;align-items:center;gap:5px;background:transparent;border:0;padding:0;color:#F3DDE3;min-height:52px}
.s7 .key i{width:8px;height:8px;border-radius:50%;background:#6E2A3E}
.s7 .key span{background:linear-gradient(180deg,#FFF8F0,#EAD6C8);color:var(--ink);border-radius:6px;padding:6px 12px;font-size:12.5px;font-weight:600;box-shadow:0 3px 0 #1E0510}
.s7 .key:hover span{background:#fff}
.s7 .key.on i{background:var(--champ2);box-shadow:0 0 8px var(--champ2)} .s7 .key.on span{background:linear-gradient(180deg,var(--champ2),var(--champ));transform:translateY(2px);box-shadow:0 1px 0 #1E0510}
.s7 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:22px 0 14px}
.s7 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--wine)}
.s7 h2{font-family:var(--f-num);font-weight:400;font-size:72px;line-height:.9;margin:4px 0 0;letter-spacing:.01em;color:var(--wine2)}
.s7 .counters{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}
.s7 .ct{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:8px 12px;text-align:left;color:inherit;min-width:140px}
.s7 .ct > span:first-child{display:block;font-size:10.5px;letter-spacing:.1em;font-weight:600;color:var(--mute);margin-bottom:5px}
.s7 .ct .wh{font-size:24px}
.s7 .ct em{display:block;font-style:normal;font-size:11px;color:var(--wine);margin-top:5px}
.s7 .strip{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.9fr);gap:12px;margin-bottom:14px;align-items:stretch}
.s7 .tag{position:relative;background:var(--wine);color:#FFF4F6;border:0;border-radius:4px 14px 14px 4px;padding:10px 12px 10px 30px;text-align:left;font-size:12.5px;font-weight:600;clip-path:polygon(16px 0,100% 0,100% 100%,16px 100%,0 50%)}
.s7 .tag::before{content:"";position:absolute;left:12px;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:var(--bg)}
.s7 .tag small{display:block;font-weight:400;color:#F1C2CF;font-size:11.5px}
.s7 .cal{display:grid;grid-template-columns:auto minmax(0,1fr);gap:12px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:8px 12px;text-align:left;color:inherit}
.s7 .cal .pg{width:58px;border-radius:6px;overflow:hidden;box-shadow:0 3px 0 var(--line);text-align:center}
.s7 .cal .pg i{display:block;background:var(--wine);color:#fff;font-style:normal;font-size:10.5px;font-weight:700;letter-spacing:.1em;padding:2px 0}
.s7 .cal .pg b{display:block;font-family:var(--f-num);font-weight:400;font-size:34px;line-height:1.1;background:#FFFBF4}
.s7 .cal span{font-size:12.5px;font-weight:600} .s7 .cal small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s7 .wall{border-radius:18px;background:linear-gradient(180deg,#FFFFFF,#FBF4F2);border:1.5px solid var(--line);overflow-x:auto;box-shadow:0 16px 34px rgba(74,12,32,.08)}
.s7 .wall svg{display:block;width:100%;min-width:900px;height:auto}
.s7 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--wine)}
.s7 .mt{cursor:pointer}
.s7 .mt:focus{outline:none} .s7 .mt:focus .bz{stroke:#F2B705;stroke-width:4}
.s7 .mt:hover .bz{stroke:var(--wine)}
.s7 .mt.ping .fc{animation:s7ping .9s ease}
@keyframes s7ping{0%{fill:#FFF0C8}100%{fill:#FFFFFF}}
.s7 .wire{animation:s7wire 1.2s linear infinite}
.s7 .wire.slow{animation-duration:3.5s}
@keyframes s7wire{to{stroke-dashoffset:-20}}
.s7 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:8px}
.s7 .legend i{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-1px;margin-right:6px;border:2.5px solid}
.s7 .zone{margin-top:40px;scroll-margin-top:20px;border-radius:18px}
.s7 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:14px}
.s7 .zh h3{font-family:var(--f-num);font-weight:400;font-size:38px;margin:0;line-height:1;color:var(--wine2);display:flex;align-items:center;gap:10px}
.s7 .zh h3::before{content:"";width:14px;height:14px;border-radius:50%;border:3px solid var(--champ);background:var(--wine)}
.s7 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s7 .levels{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:10px;background:linear-gradient(180deg,#4A0C20,#33081A);border-radius:18px;padding:18px 14px 14px}
.s7 .lv{display:flex;flex-direction:column;align-items:center;gap:6px;background:transparent;border:0;padding:0;color:#FFF4F6;text-align:center}
.s7 .lv .tg{font-size:10.5px;color:var(--champ2);font-weight:600}
.s7 .seg{display:flex;flex-direction:column-reverse;gap:3px;width:44px;padding:5px;border-radius:8px;background:#1E0510}
.s7 .seg i{height:7px;border-radius:2px;background:#4E1A2A}
.s7 .seg i.on{background:var(--c)}
.s7 .seg i.pl{outline:2px solid var(--champ2);outline-offset:1px}
.s7 .lv b{font-family:var(--f-num);font-weight:400;font-size:24px;line-height:1}
.s7 .lv .nm{font-size:11.5px;font-weight:600;line-height:1.25;min-height:30px;color:#FFE9EE}
.s7 .lv .st{font-size:10.5px;font-weight:700;letter-spacing:.05em}
.s7 .lv:hover .seg,.s7 .lv:focus-visible .seg{box-shadow:0 0 0 2px var(--champ)}
.s7 .ahead{color:#5FD39B} .s7 .watch{color:#F5C063} .s7 .off{color:#FF8A9A}
.s7 .people{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s7 .pp{background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:12px 14px;text-align:left;color:inherit;display:grid;gap:8px;transition:transform .15s}
.s7 .pp:hover,.s7 .pp:focus-visible{transform:translateY(-3px);border-color:var(--wine)}
.s7 .pp .hd{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.s7 .pp .nm{font-weight:700;font-size:13.5px;line-height:1.2}
.s7 .pp .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s7 .pp .chip{font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:999px;white-space:nowrap;border:1.5px solid currentColor}
.s7 .pp .chip.ahead{color:var(--ok)} .s7 .pp .chip.watch{color:var(--warn)} .s7 .pp .chip.off{color:var(--bad)}
.s7 .bar10{display:flex;gap:3px}
.s7 .bar10 i{flex:1;height:12px;border-radius:3px;background:#F1E4E7}
.s7 .bar10 i.y{background:var(--wine)} .s7 .bar10 i.l{background:var(--bad);background:repeating-linear-gradient(45deg,var(--bad) 0 3px,#F6B6C0 3px 6px)}
.s7 .pp .meta{font-size:12px} .s7 .pp .meta b{font-family:var(--f-num);font-weight:400;font-size:18px}
.s7 .pp .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s7 .pp .nx{font-size:11.5px;color:var(--mute)}
.s7 .pp ul{list-style:none;margin:0;padding:0;font-size:12px;display:grid;gap:3px}
.s7 .pp li::before{content:"○ ";color:var(--mute)} .s7 .pp li.y::before{content:"● ";color:var(--wine)} .s7 .pp li.l{color:var(--bad);font-weight:600} .s7 .pp li.l::before{content:"◆ ";color:var(--bad)}
.s7 .vt{display:inline-flex;background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:3px}
.s7 .vt button{border:0;background:transparent;border-radius:999px;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:var(--ink)}
.s7 .vt button[aria-pressed="true"]{background:var(--wine);color:#fff}
.s7 .money{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s7 .chart{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:12px;overflow-x:auto}
.s7 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s7 .mlist{display:grid;gap:10px}
.s7 .mlist button{display:flex;justify-content:space-between;gap:12px;align-items:baseline;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12.5px}
.s7 .mlist b{font-family:var(--f-num);font-weight:400;font-size:24px;color:var(--ink);white-space:nowrap}
.s7 .mlist .why{background:var(--wine);border-color:var(--wine);color:#FBDDE5} .s7 .mlist .why b{color:#fff}
@media (max-width:1000px){ .s7 .head{grid-template-columns:1fr} .s7 .counters{justify-content:flex-start} .s7 .strip{grid-template-columns:1fr 1fr} .s7 .levels{grid-template-columns:repeat(5,minmax(0,1fr))} .s7 .people{grid-template-columns:1fr 1fr} .s7 .money{grid-template-columns:1fr} }
@media (max-width:600px){ .s7 .swipe{display:block} .s7 h2{font-size:52px} .s7 .strip,.s7 .people{grid-template-columns:1fr} .s7 .levels{grid-template-columns:repeat(3,minmax(0,1fr))} .s7 .ct{flex:1 1 140px} .s7 .key span{padding:6px 9px;font-size:12px} }
`,
  render(){
    const C = { live:"#1E7F54", testing:"#C98A12", building:"#B9A3AA", blocked:"#C0263B", notstarted:"#E2D3D7" };
    const wheels = (t) => [...String(t)].map(c=>`<span class="wh" aria-hidden="true">${c===" "?"&nbsp;":esc(c)}</span>`).join("");
    const live = countParts("live");
    const counters = `
      <button class="ct" type="button" data-tab="links"><span>CHARGE LINES LIVE</span>${wheels(String(live).padStart(2,"0")+"/12")}<em>plan for this week: 4</em></button>
      <button class="ct" type="button" data-tab="measures"><span>KPIs ON COURSE</span>${wheels(onCourse+"/9")}<em>plan for this week: 8</em></button>
      <button class="ct" type="button" data-ref="health:0"><span>EBITDA BACK / OUT · ₹ LAKH</span>${wheels(ebitdaTotal.toFixed(1)+"/"+spendTotal.toFixed(1))}<em>plan: 3.4 back</em></button>
      <button class="ct" type="button" data-ref="health:0"><span>BREAK-EVEN</span>${wheels("MAR 27")}<em>plan Jan 2027 · 8 weeks late</em></button>`;

    /* --- the meter wall --- */
    const W = 1000, H = 680; let wires = "", meters = "", defs = "";
    const tot = { x: 520, y: 340, r: 104 };
    const meter = (p, x, y, r) => { const col = C[p.st], sx = x, sy = y; const live = p.st==="live", test = p.st==="testing";
      const ring = p.st==="building"||p.st==="notstarted" ? `stroke-dasharray="5 4"` : "";
      const reading = live ? (p.vol.match(/[\d,]+/)||["—"])[0] : test ? "TEST" : p.st==="blocked" ? "LATE" : "—";
      const disc = live || test ? `<g transform="translate(${sx},${sy+10})"><ellipse rx="${r*.55}" ry="4" fill="#EAD9DC"/><line x1="0" y1="0" x2="${r*.5}" y2="0" stroke="#4A0C20" stroke-width="2"><animateTransform attributeName="transform" type="scale" values="1 1;-1 1;1 1" dur="${live?1.6:4.5}s" repeatCount="indefinite"/></line></g>` : "";
      return `<g class="mt" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}">
        <circle cx="${sx}" cy="${sy}" r="${r+7}" fill="#F3E6C4" class="bz" stroke="#C8A24A" stroke-width="3"/>
        <circle class="fc" cx="${sx}" cy="${sy}" r="${r}" fill="#FFFFFF" stroke="${col}" stroke-width="4" ${ring}/>
        <rect x="${sx-r*.62}" y="${sy-r*.42}" width="${r*1.24}" height="${r*.42}" rx="3" fill="#1A0710"/>
        <text x="${sx}" y="${sy-r*.12}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="${r*.36}" fill="${p.st==="blocked"?"#FF8A9A":"#E9D29A"}" letter-spacing="1">${reading}</text>
        ${disc}
        <circle cx="${sx-r*.78}" cy="${sy-r*.78}" r="11" fill="${p.st==="building"||p.st==="notstarted"?"#fff":col}" stroke="${col==="#E2D3D7"?"#B9A3AA":col}" stroke-width="2"/><text x="${sx-r*.78}" y="${sy-r*.78+4}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="13" fill="${p.st==="building"||p.st==="notstarted"?"#2E0F1A":"#fff"}">${p.id}</text>
        <foreignObject x="${sx-74}" y="${sy+r+10}" width="148" height="46"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 11px/1.25 Poppins,sans-serif;color:#2E0F1A;text-align:center">${esc(p.name)}<div style="font-weight:400;font-size:10px;color:${p.st==="notstarted"||p.st==="building"?"#6E5560":col}">${PART_WORD[p.st]} · ${esc(p.when.replace(/^Live since /,"since "))}</div></div></foreignObject></g>`; };
    const wire = (x1,y1,x2,y2,st) => { const d = `M${x1},${y1} C${(x1+x2)/2},${y1} ${(x1+x2)/2},${y2} ${x2},${y2}`;
      if (st==="live") return `<path d="${d}" fill="none" stroke="#EAD9DC" stroke-width="7" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#8A1538" stroke-width="3" stroke-dasharray="7 5" class="wire"/>`;
      if (st==="testing") return `<path d="${d}" fill="none" stroke="#EAD9DC" stroke-width="7" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#C98A12" stroke-width="3" stroke-dasharray="7 5" class="wire slow"/>`;
      if (st==="blocked") return `<path d="${d}" fill="none" stroke="#C0263B" stroke-width="3"/><g transform="translate(${(x1+x2)/2},${(y1+y2)/2})"><circle r="10" fill="#fff" stroke="#C0263B" stroke-width="2"/><path d="M-4,-4 L4,4 M4,-4 L-4,4" stroke="#C0263B" stroke-width="2.5"/></g>`;
      return `<path d="${d}" fill="none" stroke="#D9C3C9" stroke-width="2.5" stroke-dasharray="${st==="building"?"6 5":"2 6"}"/>`; };
    const ins = D.parts.filter(p=>p.side==="in"), outs = D.parts.filter(p=>p.side==="out"), rule = D.parts.find(p=>p.side==="rules");
    const mr = 34;
    ins.forEach((p,i) => { const col = i%2, row = Math.floor(i/2); const x = 80 + col*175, y = 80 + row*150 + (col?75:0);
      wires += wire(x+mr+7, y, tot.x-tot.r-6, tot.y-60+i*20, p.st); meters += meter(p, x, y, mr); });
    { const x = tot.x, y = 62; wires += wire(x, y+mr+7, x, tot.y-tot.r-8, rule.st).replace(/C[^"]+"/g, `L${x},${tot.y-tot.r-8}"`); meters += meter(rule, x, y, mr); }
    outs.forEach((p,i) => { const x = 880, y = 80 + i*150; wires += wire(tot.x+tot.r+6, tot.y-45+i*30, x-mr-7, y, p.st); meters += meter(p, x, y, mr); });
    const totaliser = `<g aria-label="The totaliser">
      <circle cx="${tot.x}" cy="${tot.y}" r="${tot.r+14}" fill="#F3E6C4" stroke="#C8A24A" stroke-width="4"/>
      <circle cx="${tot.x}" cy="${tot.y}" r="${tot.r}" fill="#4A0C20"/>
      ${Array.from({length:40},(_,i)=>{ const a = i/40*Math.PI*2; const r1 = tot.r-6, r2 = tot.r-(i%5?12:18); return `<line x1="${tot.x+r1*Math.cos(a)}" y1="${tot.y+r1*Math.sin(a)}" x2="${tot.x+r2*Math.cos(a)}" y2="${tot.y+r2*Math.sin(a)}" stroke="#C8A24A" stroke-width="${i%5?1:2}"/>`; }).join("")}
      <text x="${tot.x}" y="${tot.y-40}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="22" fill="#E9D29A" letter-spacing="1.5">BILLING ENGINE</text>
      <rect x="${tot.x-74}" y="${tot.y-24}" width="148" height="40" rx="5" fill="#120309" stroke="#C8A24A"/>
      <text id="s7amt" x="${tot.x}" y="${tot.y+5}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="28" fill="#E9D29A" letter-spacing="1">₹18,42,300</text>
      <text x="${tot.x}" y="${tot.y+34}" text-anchor="middle" font-size="9.5" fill="#F1C2CF" letter-spacing="1.2">POSTED TODAY</text>
      <text id="s7cnt" x="${tot.x}" y="${tot.y+50}" text-anchor="middle" font-size="10" fill="#F1C2CF">1,284 charges</text>
      <text id="s7last" x="${tot.x}" y="${tot.y+66}" text-anchor="middle" font-size="9" fill="#E9D29A">Lab · CBC · ₹450 · Bed 214</text></g>`;
    const heads = `<text x="40" y="24" font-size="11" font-weight="700" letter-spacing="1.5" fill="#8A1538">EVENTS IN THE STAY</text><text x="${W-40}" y="24" text-anchor="end" font-size="11" font-weight="700" letter-spacing="1.5" fill="#8A1538">BILLS GOING OUT</text>
      <text x="${W-40}" y="${H-14}" text-anchor="end" font-size="10.5" fill="#6E5560">The signed summary for claims comes from the Discharge Summary suite</text>`;
    const wall = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Seven kinds of event and the charge list each feed the billing engine, which sends bills to the family and the insurers.">${heads}${wires}${totaliser}${meters}</svg>`;

    /* --- KPI level bars --- */
    const lv = k => { const N = 20, n = Math.round(Math.min(1,prog(k,k.now))*N), pl = Math.max(1,Math.round(Math.min(1,prog(k,k.plan))*N)); const col = k.state==="ahead"?"#5FD39B":k.state==="watch"?"#F5C063":"#FF8A9A";
      const segs = Array.from({length:N},(_,i)=>`<i class="${i<n?"on":""} ${i===pl-1?"pl":""}"></i>`).join("");
      return `<button class="lv" type="button" data-ref="kpi:${k.id}" aria-label="${esc(k.name)}: ${fmtv(k,k.now)}, ${STATE_WORD[k.state]}"><span class="tg">${fmtv(k,k.target)}</span><span class="seg" style="--c:${col}">${segs}</span><b class="${k.state}">${fmtv(k,k.now)}</b><span class="nm">${esc(k.short)}</span><span class="st ${k.state}">${STATE_WORD[k.state].toUpperCase()}</span></button>`; };

    /* --- people --- */
    const pp = p => { let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}">${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const b = []; for (let i=0;i<p.due;i++) b.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":""}"></i>`); body = `<span class="bar10" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span><span class="meta"><b>${p.done}</b> of ${p.due} done${p.late?` · <b style="color:var(--bad)">${p.late}</b> late`:""}</span>`; }
      return `<button class="pp" type="button" data-ref="per:${p.key}"><span class="hd"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="chip ${p.state}">${PERSON_WORD[p.state]}</span></span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</button>`; };

    /* --- money: paired columns --- */
    const CW = 760, CH = 300, x0 = 46, x1 = 740, y0 = 20, y1 = 250, vmax = 45, n = D.cumMonths.length, bw = (x1-x0)/n;
    const by = v => y1 - (y1-y0)*v/vmax;
    let cols = `<defs><pattern id="s7hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#F3E6C4"/><line x1="0" y1="0" x2="0" y2="6" stroke="#C8A24A" stroke-width="2"/></pattern><pattern id="s7hatchw" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#F6E4E9"/><line x1="0" y1="0" x2="0" y2="6" stroke="#B98A97" stroke-width="2"/></pattern></defs>`;
    [0,10,20,30,40].forEach(v => cols += `<line x1="${x0}" x2="${x1}" y1="${by(v)}" y2="${by(v)}" stroke="#F1E4E7"/><text x="${x0-8}" y="${by(v)+4}" text-anchor="end" font-size="10" fill="#6E5560">${v}</text>`);
    D.cumMonths.forEach((m,i) => { const x = x0 + i*bw + 6, w = (bw-16)/2, fore = i > D.actualTo;
      cols += `<g data-ref="month:${i}" data-nopen style="cursor:help"><rect x="${x}" y="${by(D.cumSpend[i])}" width="${w}" height="${y1-by(D.cumSpend[i])}" rx="3" fill="${fore?"url(#s7hatchw)":"#8A1538"}"/><rect x="${x+w+4}" y="${by(D.cumFore[i])}" width="${w}" height="${y1-by(D.cumFore[i])}" rx="3" fill="${fore?"url(#s7hatch)":"#C8A24A"}"/>
        <text x="${x+w+2}" y="${y1+16}" text-anchor="middle" font-size="11" font-weight="600" fill="${fore?"#6E5560":"#2E0F1A"}">${m}</text><rect x="${x-4}" y="${y0}" width="${bw}" height="${y1-y0}" fill="transparent"/></g>`; });
    const pl = D.cumPlan.map((v,i)=>`${i?"L":"M"}${x0+i*bw+bw/2},${by(v)}`).join(" ");
    const mx = x0 + 6*bw + bw/2, jx = x0 + 4*bw + bw/2;
    cols += `<path d="${pl}" fill="none" stroke="#6E5560" stroke-width="1.5" stroke-dasharray="4 4"/><text x="${x0+9*bw+bw/2}" y="${by(D.cumPlan[9])-8}" text-anchor="end" font-size="10.5" fill="#6E5560">plan, back</text>
      <line x1="${jx}" x2="${jx}" y1="${y0}" y2="${y1}" stroke="#6E5560" stroke-dasharray="3 3"/><text x="${jx}" y="${y0-6}" text-anchor="middle" font-size="10.5" fill="#6E5560">plan break-even</text>
      <line x1="${mx}" x2="${mx}" y1="${y0}" y2="${y1}" stroke="#C0263B" stroke-width="2"/><text x="${mx+6}" y="${y0+10}" font-size="11" font-weight="700" fill="#C0263B">break-even, Mar</text>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="Money out and EBITDA back to date, by month. EBITDA back passes money out in March; the plan said January.">${cols}
      <rect x="${x0}" y="${CH-22}" width="12" height="12" rx="2" fill="#8A1538"/><text x="${x0+18}" y="${CH-12}" font-size="11" fill="#2E0F1A">Money out to date</text><rect x="${x0+150}" y="${CH-22}" width="12" height="12" rx="2" fill="#C8A24A"/><text x="${x0+168}" y="${CH-12}" font-size="11" fill="#2E0F1A">EBITDA back to date</text><text x="${x0+320}" y="${CH-12}" font-size="11" fill="#6E5560">Hatched: forecast · ₹ lakh</text></svg>`;

    return `<div class="s7"><div class="wrap">
      <nav class="keys" aria-label="Suite sections"><div class="odo" aria-hidden="true"><small>YOU ARE ON</small><span id="s7at">${wheels("OVERVIEW")}</span></div>
        <div class="ks">${TABS.map((t,i)=>`<button class="key ${i?"":"on"}" type="button" data-tab="${t[0]}"><i></i><span>${t[1]}</span></button>`).join("")}</div></nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="counters" aria-label="Pulse strip">${counters}</div></div>
      <div class="strip" aria-label="Watch list and next go-live">${D.watch.map(w=>`<button class="tag" type="button" data-ref="${w.ref}">${esc(w.t)}<small>${esc(P[w.who].name)}</small></button>`).join("")}
        <button class="cal" type="button" data-ref="part:${D.milestone.part}"><span class="pg"><i>OCT</i><b>${D.milestone.date.split(" ")[0]}</b></span><span>Next go-live in ${D.milestone.days} days<small>${esc(D.milestone.what)}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to see every line →</p><div class="wall">${wall}</div>
        <div class="legend"><span><i style="border-color:#1E7F54"></i>Live</span><span><i style="border-color:#C98A12"></i>Testing</span><span><i style="border-color:#B9A3AA;border-style:dashed"></i>Being built</span><span><i style="border-color:#C0263B"></i>Late</span><span><i style="border-color:#E2D3D7;border-style:dotted"></i>Not started</span><span>· Data as of ${esc(D.asOf)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3><p>Lit bars are today · the outlined bar is the plan for this week · the top is the target</p></div>
        <div class="levels">${D.kpis.map(lv).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="people">${D.people.map(pp).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="money"><div class="chart">${chart}</div>
          <div class="mlist">
            <button type="button" data-ref="month:1"><span>Subscription, each month</span><b>${L(2.0)}</b></button>
            <button type="button" data-ref="month:1"><span>Salary of the night insurance coordinator we recommended, each month</span><b>${L(0.25)}</b></button>
            <button type="button" data-ref="month:1"><span>One-time so far (charge list, insurer connectors)</span><b>${L(3.0)}</b></button>
            <button type="button" data-ref="health:0"><span>Extra revenue so far, from charges no longer missed</span><b>${L(revTotal)}</b></button>
            <button type="button" data-ref="health:0"><span>EBITDA now, and at full run, each month</span><b>${L(D.ebitda[1])} → ${L(D.runRate.ebitda)}</b></button>
            <button type="button" class="why" data-ref="health:0"><span>Break-even ${D.breakeven.fore}, ${D.breakeven.late} late. See why</span><b>›</b></button>
          </div></div></section>
    </div></div>`;
  },
  after(){
    document.querySelectorAll(".s7 .key").forEach(b => b.addEventListener("click", () => { const at = document.getElementById("s7at"); if (at) at.innerHTML = [...b.textContent.trim().toUpperCase()].map(c=>`<span class="wh">${c===" "?"&nbsp;":c}</span>`).join(""); }));
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { document.querySelectorAll(".s7 animateTransform").forEach(a => a.remove()); return; }
    tickEngine("s7", ".s7 .mt");
  }
});
