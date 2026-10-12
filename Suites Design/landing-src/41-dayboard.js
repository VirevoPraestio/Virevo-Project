/* ===== Diagnostic Scheduling, option 1: the day board (magenta and sky on blush) ===== */
SCHEMES.push({
  key:"dayboard", letter:"1", name:"Magenta and sky",
  note:"<b>Option 1 · magenta and sky.</b> Today's test rooms as a day board, hour by hour: booked, walk-ins slotted, slots held for emergencies, and gaps. Prescriptions come in at the top; what the suite sends out sits below.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#24202F","--sh-mute":"#5E5869","--sh-line":"#E2DCE6","--sh-card":"#FAF7FB","--c-ok":"#16845C","--c-warn":"#A86B05","--c-bad":"#C62D3A","--pk-bg":"#24202F","--pk-fg":"#FFFFFF","--pk-line":"#C2185B","--pk-r":"10px","--sh-r":"16px" },
  fab:18,
  blocks:{ nav:".folders", pulse:".appts", watch:".clashes", countdown:".note", hero:".board", kpis:".waffles", team:".cals", money:".diverge" },
  css:`
.s11{--bg:#F5F2F6;--ink:#24202F;--mute:#5E5869;--mag:#C2185B;--mag2:#F8D7E6;--sky:#2F7FE0;--sky2:#D9E8FB;--ok:#16845C;--warn:#A86B05;--bad:#C62D3A;--line:#E2DCE6;
  background:var(--bg);color:var(--ink);padding:18px 16px 90px;overflow-x:clip}
.s11 .wrap{max-width:1240px;margin:0 auto}
.s11 .folders{display:flex;flex-wrap:wrap;align-items:flex-end;gap:4px 4px;border-bottom:3px solid var(--ink);padding-left:4px}
.s11 .chipd{display:flex;align-items:center;gap:10px;margin:0 12px 6px 0}
.s11 .chipd b{display:grid;place-items:center;width:46px;height:50px;border-radius:8px;background:#fff;border:2px solid var(--ink);font-family:var(--f-num);font-weight:400;font-size:24px;line-height:.9;text-align:center}
.s11 .chipd b small{display:block;font-family:var(--f-body);font-size:9px;font-weight:700;letter-spacing:.1em;background:var(--mag);color:#fff;width:100%;border-radius:5px 5px 0 0;margin-bottom:2px}
.s11 .chipd span{font-size:10px;letter-spacing:.14em;color:var(--mute);font-weight:600} .s11 .chipd em{display:block;font-style:normal;font-family:var(--f-num);font-size:22px;letter-spacing:.04em;color:var(--ink)}
.s11 .fd{background:#EBE5EE;border:1.5px solid #D3CAD8;border-bottom:0;border-radius:10px 10px 0 0;padding:10px 16px;font-size:12.5px;font-weight:600;color:var(--ink);min-height:44px}
.s11 .fd:hover{background:#fff}
.s11 .fd.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.s11 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:22px 0 14px}
.s11 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--mag)}
.s11 h2{font-family:var(--f-num);font-weight:400;font-size:72px;line-height:.9;margin:4px 0 0;letter-spacing:.01em}
.s11 .appts{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}
.s11 .ap{display:grid;grid-template-columns:8px minmax(0,1fr);background:#fff;border:1.5px solid var(--line);border-radius:10px;overflow:hidden;text-align:left;color:inherit;padding:0;min-width:150px}
.s11 .ap i{background:var(--c)}
.s11 .ap span{padding:8px 12px}
.s11 .ap span span{display:block;padding:0;font-size:10.5px;letter-spacing:.1em;font-weight:600;color:var(--mute)}
.s11 .ap b{display:block;font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1}
.s11 .ap em{font-style:normal;font-size:11px;color:var(--mag)}
.s11 .clashes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.8fr);gap:12px;margin-bottom:14px;align-items:stretch}
.s11 .cs{display:grid;grid-template-columns:34px minmax(0,1fr);gap:10px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:10px 12px;text-align:left;color:inherit;font-size:12.5px;font-weight:600}
.s11 .cs i{position:relative;width:30px;height:26px}
.s11 .cs i::before,.s11 .cs i::after{content:"";position:absolute;width:20px;height:14px;border-radius:3px;border:2px solid var(--mag)}
.s11 .cs i::before{left:0;top:0;background:var(--mag2)} .s11 .cs i::after{left:9px;top:9px;background:#fff}
.s11 .cs small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s11 .note{position:relative;background:#FFF0F6;border:0;border-radius:4px;padding:16px 14px 10px;text-align:left;color:var(--ink);transform:rotate(1.5deg);box-shadow:0 8px 14px rgba(36,32,47,.12)}
.s11 .note::before{content:"";position:absolute;top:-7px;left:50%;width:14px;height:14px;margin-left:-7px;border-radius:50%;background:var(--mag);box-shadow:0 2px 3px rgba(0,0,0,.3)}
.s11 .note b{font-family:var(--f-num);font-weight:400;font-size:40px;line-height:.9;color:var(--mag)}
.s11 .note span{display:block;font-size:12px;font-weight:700} .s11 .note small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s11 .board{border-radius:16px;background:#fff;border:1.5px solid var(--line);overflow-x:auto;box-shadow:0 14px 30px rgba(36,32,47,.06)}
.s11 .board svg{display:block;width:100%;min-width:920px;height:auto}
.s11 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--mag)}
.s11 .pc{cursor:pointer}
.s11 .pc:focus{outline:none} .s11 .pc:focus .cd{stroke:#F2B705;stroke-width:3}
.s11 .pc:hover .cd{stroke:var(--mag)}
.s11 .pc.ping .cd{animation:s11ping .9s ease}
@keyframes s11ping{0%{fill:#FCE3EE}100%{fill:#FFFFFF}}
.s11 .newc{animation:s11pop .8s ease}
@keyframes s11pop{0%{opacity:0}100%{opacity:1}}
.s11 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:8px}
.s11 .legend i{display:inline-block;width:14px;height:12px;border-radius:3px;vertical-align:-1px;margin-right:6px}
.s11 .zone{margin-top:40px;scroll-margin-top:20px;border-radius:16px}
.s11 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:14px;border-bottom:3px solid var(--ink);padding-bottom:8px}
.s11 .zh h3{font-family:var(--f-num);font-weight:400;font-size:38px;margin:0;line-height:1}
.s11 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s11 .waffles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.s11 .wf{display:grid;grid-template-columns:96px minmax(0,1fr);gap:12px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:12px;text-align:left;color:inherit;transition:transform .15s}
.s11 .wf:hover,.s11 .wf:focus-visible{transform:translateY(-2px);border-color:var(--mag)}
.s11 .grid10{display:grid;grid-template-columns:repeat(10,1fr);gap:2px;width:96px}
.s11 .grid10 i{aspect-ratio:1;border-radius:2px;background:#EEE9F1}
.s11 .grid10 i.on{background:var(--c)} .s11 .grid10 i.pl{outline:1.5px solid var(--ink);outline-offset:0}
.s11 .wf .nm{font-size:13px;font-weight:600;line-height:1.3}
.s11 .wf b{display:block;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1;margin-top:4px}
.s11 .wf .st{display:block;font-size:11px;font-weight:700;letter-spacing:.05em;margin-top:4px}
.s11 .wf .rg{display:block;font-size:11px;color:var(--mute);margin-top:2px}
.s11 .ahead{color:var(--ok)} .s11 .watch{color:var(--warn)} .s11 .off{color:var(--bad)}
.s11 .cals{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s11 .cl{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:0;text-align:left;color:inherit;overflow:hidden;display:flex;flex-direction:column;transition:transform .15s}
.s11 .cl:hover,.s11 .cl:focus-visible{transform:translateY(-3px);border-color:var(--mag)}
.s11 .cl .top{display:flex;justify-content:space-between;gap:8px;align-items:center;padding:10px 12px;border-bottom:1.5px dashed var(--line)}
.s11 .cl .nm{font-weight:700;font-size:13.5px;line-height:1.2} .s11 .cl .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s11 .cl .chip{font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:4px;white-space:nowrap;color:#fff}
.s11 .cl .bd2{padding:10px 12px;display:grid;gap:7px}
.s11 .sq{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}
.s11 .sq i{aspect-ratio:1.4;border-radius:3px;background:#F1ECF3;border:1px solid #E2DCE6}
.s11 .sq i.y{background:var(--mag);border-color:var(--mag)} .s11 .sq i.l{background:#fff;border:2px solid var(--bad);background-image:linear-gradient(45deg,transparent 45%,var(--bad) 45% 55%,transparent 55%)}
.s11 .cl .meta{font-size:12px} .s11 .cl .meta b{font-family:var(--f-num);font-weight:400;font-size:18px}
.s11 .cl .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s11 .cl .nx{font-size:11.5px;color:var(--mute)}
.s11 .cl ul{list-style:none;margin:0;padding:0;font-size:12px;display:grid;gap:3px}
.s11 .cl li::before{content:"▢ ";color:var(--mute)} .s11 .cl li.y::before{content:"■ ";color:var(--mag)} .s11 .cl li.l{color:var(--bad);font-weight:600} .s11 .cl li.l::before{content:"▣ "}
.s11 .vt{display:inline-flex;border:2px solid var(--ink);border-radius:8px;overflow:hidden}
.s11 .vt button{border:0;background:#fff;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:var(--ink)}
.s11 .vt button[aria-pressed="true"]{background:var(--ink);color:#fff}
.s11 .diverge{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s11 .chart{background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:12px;overflow-x:auto}
.s11 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s11 .mlist{display:grid;gap:10px}
.s11 .mlist button{display:flex;justify-content:space-between;gap:12px;align-items:baseline;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12.5px}
.s11 .mlist b{font-family:var(--f-num);font-weight:400;font-size:24px;color:var(--ink);white-space:nowrap}
.s11 .mlist .why{background:var(--mag);border-color:var(--mag);color:#FCE3EE} .s11 .mlist .why b{color:#fff}
@media (max-width:1000px){ .s11 .head{grid-template-columns:1fr} .s11 .appts{justify-content:flex-start} .s11 .clashes{grid-template-columns:1fr 1fr} .s11 .waffles,.s11 .cals{grid-template-columns:1fr 1fr} .s11 .diverge{grid-template-columns:1fr} }
@media (max-width:600px){ .s11 .swipe{display:block} .s11 h2{font-size:52px} .s11 .clashes,.s11 .waffles,.s11 .cals{grid-template-columns:1fr} .s11 .ap{flex:1 1 150px} .s11 .fd{padding:8px 10px;font-size:12px} .s11 .chipd{width:100%} }
`,
  render(){
    const C = { live:"#16845C", testing:"#D9940A", building:"#A69DB0", blocked:"#C62D3A", notstarted:"#D8D2DE" };
    const live = countParts("live"), O = D.opd;
    const ap = (c, lab, val, sub, attr) => `<button class="ap" type="button" ${attr} style="--c:${c}"><i></i><span><span>${lab}</span><b>${val}</b><em>${sub}</em></span></button>`;
    const appts = ap("#16845C","PARTS LIVE",`${live} / 12`,"plan 4",`data-tab="links"`) + ap("#D9940A","KPIs ON COURSE",`${onCourse} / 9`,"plan 8",`data-tab="measures"`)
      + ap("#2F7FE0","EBITDA BACK / OUT",`${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}`,"₹ lakh · plan 7.0 back",`data-ref="health:0"`) + ap("#C62D3A","BREAK-EVEN","DEC 2026","plan Nov 2026",`data-ref="health:0"`);
    const P_ = id => D.parts.find(p=>p.id===id);
    const card = (p, x, y, w, h, small) => `<g class="pc" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}">
      <rect class="cd" x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="#FFFFFF" stroke="#24202F" stroke-width="1.5" ${p.st==="building"||p.st==="notstarted"?'stroke-dasharray="5 3"':""}/>
      <rect x="${x}" y="${y}" width="6" height="${h}" rx="3" fill="${C[p.st]}"/>
      <foreignObject x="${x+12}" y="${y+4}" width="${w-16}" height="${h-8}"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 ${small?10:10.5}px/1.2 Poppins,sans-serif;color:#24202F;height:${h-8}px;display:flex;flex-direction:column;justify-content:center"><span><b style="font-family:'Bebas Neue';font-weight:400;font-size:14px;color:#C2185B">${p.id}</b> ${esc(p.name)}</span><span style="font-weight:400;font-size:9.5px;color:${p.st==="notstarted"||p.st==="building"?"#5E5869":C[p.st]}">${PART_WORD[p.st]} · ${esc(p.when.replace(/^Live since /,"since ").replace(/^Goes live /,"live "))}</span></div></foreignObject></g>`;

    /* --- the day board --- */
    const W = 1000, H = 640; let g = "";
    /* intake */
    g += `<text x="20" y="30" font-size="11" font-weight="700" letter-spacing="1.4" fill="#C2185B">PRESCRIPTIONS COMING IN · OPD TODAY: ${O.newPts} NEW, ${O.returning} RETURNING</text>`;
    [1,2,3].forEach((id,i) => { const x = 20 + i*210; g += card(P_(id), x, 42, 190, 58) + (i<2?`<path d="M${x+192},71 L${x+208},71" stroke="#24202F" stroke-width="2" marker-end="url(#s11ar)"/>`:""); });
    g += `<defs><marker id="s11ar" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#24202F"/></marker><pattern id="s11hold" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#FFFFFF"/><line x1="0" y1="0" x2="0" y2="6" stroke="#C2185B" stroke-width="2"/></pattern><pattern id="s11nofeed" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#F3EFF5"/><line x1="0" y1="0" x2="0" y2="8" stroke="#D8D2DE" stroke-width="3"/></pattern></defs>`;
    const pct = Math.round(O.doneHere/O.prescribedToday*100);
    g += `<g aria-label="Prescribed today against done here"><rect x="660" y="42" width="320" height="58" rx="10" fill="#24202F"/>
      <text x="676" y="62" font-size="9.5" font-weight="700" letter-spacing="1.3" fill="#D3CAD8">PRESCRIBED TODAY · DONE HERE</text>
      <text x="676" y="90" font-family="Bebas Neue, sans-serif" font-size="26" fill="#FFFFFF">₹${O.prescribedToday} L</text><text id="s11amt" x="760" y="90" font-family="Bebas Neue, sans-serif" font-size="26" fill="#F8D7E6">₹${O.doneHere} L</text>
      <rect x="850" y="72" width="116" height="12" rx="6" fill="#4A4357"/><rect id="s11bar" x="850" y="72" width="${(116*pct/100).toFixed(1)}" height="12" rx="6" fill="#C2185B"/><text id="s11pct" x="966" y="64" text-anchor="end" font-size="10" fill="#F8D7E6">${pct}% done here</text></g>`;
    /* board grid */
    const bx0 = 240, bx1 = 840, by0 = 150, rh = 42, hours = 12, cw = (bx1-bx0)/hours; const rooms = D.rooms;
    g += `<text x="${bx0}" y="${by0-14}" font-size="11" font-weight="700" letter-spacing="1.4" fill="#C2185B">TODAY'S TEST ROOMS, HOUR BY HOUR</text>`;
    g += `<rect x="${bx0+cw*1}" y="${by0}" width="${cw*4}" height="${rooms.length*rh}" fill="#FCE3EE" opacity=".55"/><text x="${bx0+cw*5+6}" y="${by0+rooms.length*rh+16}" font-size="10" fill="#C2185B">◂ morning peak: 80% of patients</text>`;
    for (let hIdx=0; hIdx<=hours; hIdx++){ const x = bx0 + hIdx*cw; g += `<line x1="${x}" x2="${x}" y1="${by0}" y2="${by0+rooms.length*rh}" stroke="#EEE9F1"/>`; if (hIdx<hours) g += `<text x="${x+cw/2}" y="${by0-2}" text-anchor="middle" font-size="9.5" fill="#5E5869" dy="-1">${(8+hIdx)>12?(8+hIdx-12)+" PM":(8+hIdx)+(8+hIdx===12?" PM":" AM")}</text>`; }
    let seed = 11; const rnd = () => (seed = (seed*9301 + 49297) % 233280) / 233280;
    const nowCol = 2 + 40/60;
    rooms.forEach((r,ri) => { const y = by0 + ri*rh; const p = P_(r.part);
      g += `<g class="pc" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="${esc(r.name)}: part ${p.id}, ${PART_WORD[r.st]}"><rect class="cd" x="20" y="${y+4}" width="${bx0-30}" height="${rh-8}" rx="6" fill="#FFFFFF" stroke="#E2DCE6"/>
        <circle cx="36" cy="${y+rh/2}" r="6" fill="${C[r.st]}"/><text x="50" y="${y+rh/2+4}" font-size="12" font-weight="700" fill="#24202F">${esc(r.name)}</text><text x="${bx0-16}" y="${y+rh/2+4}" text-anchor="end" font-size="10" fill="#5E5869">part ${p.id}</text></g>`;
      for (let c=0;c<hours;c++){ const x = bx0 + c*cw + 2, w = cw-4, yy = y + 6, hh = rh-12; const peak = c>=1 && c<=4; const past = c < Math.floor(nowCol);
        if (r.st==="blocked") { g += `<rect x="${x}" y="${yy}" width="${w}" height="${hh}" rx="4" fill="url(#s11nofeed)"/>`; continue; }
        if (r.st==="building") { g += `<rect x="${x}" y="${yy}" width="${w}" height="${hh}" rx="4" fill="none" stroke="#A69DB0" stroke-dasharray="4 3"/>`; continue; }
        const held = (r.name==="MRI 1"||r.name==="CT") && (c%3===1);
        const v = rnd(); let fill;
        if (held) fill = "url(#s11hold)"; else if (v < (peak?.62:.35)) fill = "#C2185B"; else if (v < (peak?.85:.55)) fill = "#2F7FE0"; else fill = "#FFFFFF";
        g += `<rect x="${x}" y="${yy}" width="${w}" height="${hh}" rx="4" fill="${fill}" stroke="${fill==="#FFFFFF"?"#E2DCE6":"none"}" ${held?'stroke="#C2185B"':""} opacity="${past?.55:1}"/>`; }
      if (r.st==="blocked") g += `<text x="${(bx0+bx1)/2}" y="${y+rh/2+4}" text-anchor="middle" font-size="11" font-weight="700" fill="#C62D3A">No feed: bookings kept in a register</text>`;
      if (r.st==="building") g += `<text x="${(bx0+bx1)/2}" y="${y+rh/2+4}" text-anchor="middle" font-size="11" fill="#5E5869">Not on the schedule yet · due 3 Nov</text>`;
    });
    const nx = bx0 + nowCol*cw; g += `<line x1="${nx}" x2="${nx}" y1="${by0-6}" y2="${by0+rooms.length*rh+4}" stroke="#24202F" stroke-width="2"/><rect x="${nx-22}" y="${by0+rooms.length*rh+4}" width="44" height="16" rx="8" fill="#24202F"/><text x="${nx}" y="${by0+rooms.length*rh+16}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">10:40</text>`;
    /* engine column */
    g += `<text x="860" y="${by0-14}" font-size="11" font-weight="700" letter-spacing="1.4" fill="#C2185B">RULES</text>` + card(P_(4), 856, by0, 128, 92) + card(P_(5), 856, by0+104, 128, 92)
      + `<text x="920" y="${by0+218}" text-anchor="middle" font-size="10" fill="#5E5869">slots booked for</text><text x="920" y="${by0+232}" text-anchor="middle" font-size="10" fill="#5E5869">inpatients never move</text>`;
    /* outputs */
    const oy = by0 + rooms.length*rh + 52;
    g += `<text x="20" y="${oy-10}" font-size="11" font-weight="700" letter-spacing="1.4" fill="#C2185B">WHAT THE SUITE SENDS OUT</text>`;
    [9,10,11,12].forEach((id,i) => g += card(P_(id), 20 + i*245, oy, 225, 58));
    g += `<text x="${W-20}" y="${H-10}" text-anchor="end" font-size="10.5" fill="#5E5869">Findings that lead to admission go to the Admission Process suite</text>`;
    const board = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Today's test rooms hour by hour, with prescriptions coming in above and what the suite sends out below.">${g}</svg>`;

    /* --- KPI waffles --- */
    const wf = k => { const n = Math.round(Math.min(1,prog(k,k.now))*100), pl = Math.max(1,Math.round(Math.min(1,prog(k,k.plan))*100)); const col = k.state==="ahead"?"#16845C":k.state==="watch"?"#D9940A":"#C62D3A";
      return `<button class="wf" type="button" data-ref="kpi:${k.id}"><span class="grid10" style="--c:${col}" aria-hidden="true">${Array.from({length:100},(_,i)=>`<i class="${i<n?"on":""} ${i===pl-1?"pl":""}"></i>`).join("")}</span>
        <span><span class="nm">${esc(k.name)}</span><b class="${k.state}">${fmtv(k,k.now)}</b><span class="st ${k.state}">${STATE_WORD[k.state].toUpperCase()} · ${gapText(k)}</span><span class="rg">From ${fmtv(k,k.base)} · target ${fmtv(k,k.target)}</span></span></button>`; };

    /* --- people --- */
    const cl = p => { const cc = p.state==="ahead"?"#16845C":p.state==="watch"?"#A86B05":"#C62D3A"; let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}">${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const b = []; for (let i=0;i<p.due;i++) b.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":""}"></i>`); body = `<span class="sq" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span><span class="meta"><b>${p.done}</b> of ${p.due} done${p.late?` · <b style="color:var(--bad)">${p.late}</b> late`:""}</span>`; }
      return `<button class="cl" type="button" data-ref="per:${p.key}"><span class="top"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="chip" style="background:${cc}">${PERSON_WORD[p.state]}</span></span><span class="bd2">${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</span></button>`; };

    /* --- money: out below the line, back above, net line --- */
    const CW = 760, CH = 310, cx0 = 50, cx1 = 740, n = D.cumMonths.length, bw = (cx1-cx0)/n; const vmax = 70, mid = 150, sc = 120/vmax;
    let c = ""; [-60,-30,0,30,60].forEach(v => c += `<line x1="${cx0}" x2="${cx1}" y1="${mid - v*sc}" y2="${mid - v*sc}" stroke="${v===0?"#24202F":"#EEE9F1"}" stroke-width="${v===0?2:1}"/><text x="${cx0-8}" y="${mid - v*sc + 4}" text-anchor="end" font-size="10" fill="#5E5869">${Math.abs(v)}</text>`);
    D.cumMonths.forEach((m,i) => { const x = cx0 + i*bw + 10, w = bw-20, fore = i > D.actualTo;
      c += `<g data-ref="month:${i}" data-nopen style="cursor:help"><rect x="${x}" y="${mid - D.cumFore[i]*sc}" width="${w}" height="${D.cumFore[i]*sc}" rx="3" fill="#2F7FE0" fill-opacity="${fore?.3:.9}"/><rect x="${x}" y="${mid}" width="${w}" height="${D.cumSpend[i]*sc}" rx="3" fill="#C2185B" fill-opacity="${fore?.3:.9}"/>
        <text x="${x+w/2}" y="${CH-34}" text-anchor="middle" font-size="11" font-weight="600" fill="${fore?"#5E5869":"#24202F"}">${m}</text><rect x="${x-10}" y="10" width="${bw}" height="${CH-50}" fill="transparent"/></g>`; });
    const net = D.cumFore.map((v,i)=>v-D.cumSpend[i]);
    c += `<polyline points="${net.map((v,i)=>`${cx0+i*bw+bw/2},${mid - v*sc}`).join(" ")}" fill="none" stroke="#24202F" stroke-width="2.5"/>${net.map((v,i)=>`<circle cx="${cx0+i*bw+bw/2}" cy="${mid - v*sc}" r="3.5" fill="${v>=0?"#16845C":"#C62D3A"}"/>`).join("")}`;
    const fi = D.breakeven.foreIdx; c += `<text x="${cx0+fi*bw+bw/2}" y="${mid - net[fi]*sc - 10}" text-anchor="middle" font-size="11" font-weight="700" fill="#16845C">break-even</text>
      <text x="${cx0}" y="${CH-10}" font-size="11" fill="#24202F">Above: EBITDA back to date · below: money out to date · line: the difference · faded: forecast · ₹ lakh</text>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="EBITDA back above the line and money out below it, by month; the difference turns positive in ${D.cumMonths[fi]}.">${c}</svg>`;
    return `<div class="s11"><div class="wrap">
      <nav class="folders" aria-label="Suite sections"><div class="chipd" aria-hidden="true"><b><small>OCT</small>12</b><span>YOU ARE ON<em id="s11at">OVERVIEW</em></span></div>
        ${TABS.map((t,i)=>`<button class="fd ${i?"":"on"}" type="button" data-tab="${t[0]}">${t[1]}</button>`).join("")}</nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="appts" aria-label="Pulse strip">${appts}</div></div>
      <div class="clashes" aria-label="Watch list and next go-live">${D.watch.map(w=>`<button class="cs" type="button" data-ref="${w.ref}"><i aria-hidden="true"></i><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}
        <button class="note" type="button" data-ref="part:${D.milestone.part}"><b>${D.milestone.days}</b><span>days to the next go-live<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to see the whole day →</p><div class="board">${board}</div>
        <div class="legend"><span><i style="background:#C2185B"></i>Booked</span><span><i style="background:#2F7FE0"></i>Walk-in slotted today</span><span><i style="background:repeating-linear-gradient(45deg,#fff 0 2px,#C2185B 2px 4px)"></i>Held for emergencies</span><span><i style="background:#fff;border:1px solid #E2DCE6"></i>Free</span><span><i style="background:#16845C;border-radius:50%"></i>Live</span><span><i style="background:#D9940A;border-radius:50%"></i>Testing</span><span><i style="background:#A69DB0;border-radius:50%"></i>Being built</span><span><i style="background:#C62D3A;border-radius:50%"></i>Late</span><span>· Data as of ${esc(D.asOf)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3><p>Filled squares are how far from the start to the target we are today · the outlined square is the plan for this week</p></div><div class="waffles">${D.kpis.map(wf).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="cals">${D.people.map(cl).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="diverge"><div class="chart">${chart}</div>
          <div class="mlist">
            <button type="button" data-ref="month:1"><span>Subscription, each month</span><b>${L(D.spend[0].v[1])}</b></button>
            <button type="button" data-ref="month:1"><span>Salaries of the Scheduling Manager and guest-service executives we recommended, each month</span><b>${L(D.spend[1].v[1])}</b></button>
            <button type="button" data-ref="month:1"><span>One-time so far (prescription scanners, patient guide)</span><b>${L(sum(D.spend[2].v))}</b></button>
            <button type="button" data-ref="health:0"><span>Extra revenue so far, from tests done here</span><b>${L(revTotal)}</b></button>
            <button type="button" data-ref="health:0"><span>EBITDA now, and at full run, each month</span><b>${L(D.ebitda[1])} → ${L(D.runRate.ebitda)}</b></button>
            <button type="button" class="why" data-ref="health:0"><span>Break-even ${D.breakeven.fore}, ${D.breakeven.late} late. See why</span><b>›</b></button>
          </div></div></section>
    </div></div>`;
  },
  after(){
    document.querySelectorAll(".s11 .fd").forEach(b => b.addEventListener("click", () => { const at = document.getElementById("s11at"); if (at) at.textContent = b.textContent.trim().toUpperCase(); }));
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    testTicker("s11", ".s11 .pc");
  }
});
