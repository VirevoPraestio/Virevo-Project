/* ===== Admission Process, option 1: the signal line (slate and coral on mist) ===== */
SCHEMES.push({
  key:"signal", letter:"1", name:"Slate and coral",
  note:"<b>Option 1 · slate and coral.</b> The admission is a line with five stops, from arrival to the patient in bed. Each link is a signal beside the stop it speeds up, and tomorrow's bed map sits above the line.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#172A3A","--sh-mute":"#52606D","--sh-line":"#D3DCDD","--sh-card":"#F4F7F7","--c-ok":"#16825A","--c-warn":"#A86E00","--c-bad":"#C7372B","--pk-bg":"#172A3A","--pk-fg":"#FFFFFF","--pk-line":"#EE5A43","--pk-r":"10px","--sh-r":"18px" },
  fab:18,
  blocks:{ nav:".levers", pulse:".heads", watch:".closures", countdown:".stub", hero:".line", kpis:".pairs", team:".shift", money:".profile" },
  css:`
.s9{--bg:#EDF2F1;--ink:#172A3A;--mute:#52606D;--coral:#EE5A43;--coral2:#FFD3CB;--rail:#3B4A57;--ok:#16825A;--warn:#A86E00;--bad:#C7372B;--line:#D3DCDD;
  background:var(--bg);color:var(--ink);padding:18px 16px 90px;overflow-x:clip}
.s9 .wrap{max-width:1240px;margin:0 auto}
.s9 .levers{display:flex;flex-wrap:wrap;align-items:flex-end;gap:12px 16px;background:var(--ink);border-radius:12px;padding:12px 16px 10px;box-shadow:0 12px 24px rgba(23,42,58,.2)}
.s9 .dm{align-self:center;background:#0B141C;border-radius:6px;padding:6px 12px;color:var(--coral);font-family:var(--f-num);font-size:24px;letter-spacing:.12em;line-height:1;text-shadow:0 0 6px rgba(238,90,67,.7);
  background-image:radial-gradient(rgba(238,90,67,.12) 1px,transparent 1.3px);background-size:4px 4px;min-width:180px}
.s9 .dm small{display:block;font-family:var(--f-body);font-size:9.5px;letter-spacing:.16em;color:#8FA0AE;text-shadow:none}
.s9 .lv{display:flex;flex-direction:column;align-items:center;gap:6px;background:transparent;border:0;padding:0;color:#DCE4E8;font-size:12px;font-weight:600;min-height:56px}
.s9 .lv i{position:relative;width:10px;height:30px;border-radius:5px;background:linear-gradient(90deg,#8FA0AE,#DCE4E8,#8FA0AE);transform-origin:50% 100%;transform:rotate(-14deg);transition:transform .2s}
.s9 .lv i::before{content:"";position:absolute;top:-8px;left:50%;width:16px;height:12px;margin-left:-8px;border-radius:5px;background:#DCE4E8}
.s9 .lv:hover i{transform:rotate(-4deg)}
.s9 .lv.on i{transform:rotate(14deg)} .s9 .lv.on i::before{background:var(--coral)} .s9 .lv.on{color:#fff}
.s9 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:22px 0 14px}
.s9 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--coral)}
.s9 h2{font-family:var(--f-num);font-weight:400;font-size:72px;line-height:.9;margin:4px 0 0;letter-spacing:.01em}
.s9 .heads{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}
.s9 .sh{display:grid;grid-template-columns:30px minmax(0,1fr);gap:10px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:8px 12px 8px 8px;text-align:left;color:inherit;min-width:150px}
.s9 .sh svg{width:30px;height:62px}
.s9 .sh span{display:block;font-size:10.5px;letter-spacing:.1em;font-weight:600;color:var(--mute)}
.s9 .sh b{display:block;font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1}
.s9 .sh em{font-style:normal;font-size:11px;color:var(--coral)}
.s9 .closures{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.9fr);gap:12px;margin-bottom:14px}
.s9 .cl{position:relative;background:#fff;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px 10px 26px;text-align:left;color:inherit;font-size:12.5px;font-weight:600;overflow:hidden}
.s9 .cl::before{content:"";position:absolute;left:0;top:0;bottom:0;width:14px;background:repeating-linear-gradient(-45deg,var(--coral) 0 6px,#fff 6px 12px)}
.s9 .cl small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s9 .stub{position:relative;display:grid;grid-template-columns:auto minmax(0,1fr);background:var(--coral);color:#fff;border:0;border-radius:10px;text-align:left;padding:0;overflow:hidden}
.s9 .stub b{font-family:var(--f-num);font-weight:400;font-size:44px;line-height:1;padding:8px 14px;border-right:2px dashed rgba(255,255,255,.7);display:grid;place-items:center}
.s9 .stub span{padding:8px 12px;font-size:12px;font-weight:700;letter-spacing:.04em}
.s9 .stub small{display:block;font-weight:400;letter-spacing:0;font-size:11.5px;color:#FFE5E0}
.s9 .stub::before,.s9 .stub::after{content:"";position:absolute;left:62px;width:14px;height:14px;border-radius:50%;background:var(--bg)}
.s9 .stub::before{top:-7px} .s9 .stub::after{bottom:-7px}
.s9 .line{border-radius:18px;background:#fff;border:1.5px solid var(--line);overflow-x:auto;box-shadow:0 14px 30px rgba(23,42,58,.06)}
.s9 .line svg{display:block;width:100%;min-width:900px;height:auto}
.s9 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--coral)}
.s9 .sg{cursor:pointer}
.s9 .sg:focus{outline:none} .s9 .sg:focus .cd{stroke:#F2B705;stroke-width:3}
.s9 .sg:hover .cd{stroke:var(--coral)}
.s9 .sg.ping .cd{animation:s9ping .9s ease}
@keyframes s9ping{0%{fill:#FFE3DD}100%{fill:#FFFFFF}}
.s9 .blink{animation:s9blink 1.2s steps(2) infinite}
@keyframes s9blink{50%{opacity:.25}}
.s9 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:8px}
.s9 .legend i{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-1px;margin-right:6px}
.s9 .zone{margin-top:40px;scroll-margin-top:20px;border-radius:18px}
.s9 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:14px}
.s9 .zh h3{font-family:var(--f-num);font-weight:400;font-size:38px;margin:0;line-height:1;display:flex;align-items:center;gap:12px}
.s9 .zh h3::before{content:"";width:34px;height:8px;background:repeating-linear-gradient(90deg,var(--rail) 0 3px,transparent 3px 8px);border-top:2px solid var(--rail);border-bottom:2px solid var(--rail)}
.s9 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s9 .pairs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.s9 .pr{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:12px 14px;text-align:left;color:inherit;display:grid;gap:8px;transition:transform .15s,border-color .15s}
.s9 .pr:hover,.s9 .pr:focus-visible{transform:translateY(-2px);border-color:var(--coral)}
.s9 .pr .top{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.s9 .pr .top span{font-size:13px;font-weight:600;line-height:1.3}
.s9 .pr .top b{font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1;white-space:nowrap}
.s9 .bars2{position:relative;display:grid;gap:4px;padding-right:10px}
.s9 .bars2 .r{display:grid;grid-template-columns:38px minmax(0,1fr);gap:8px;align-items:center;font-size:10.5px;font-weight:600;color:var(--mute)}
.s9 .bars2 .t{position:relative;height:12px;border-radius:6px;background:#EEF2F2}
.s9 .bars2 .t i{position:absolute;left:0;top:0;bottom:0;border-radius:6px}
.s9 .bars2 .t.pl i{background:repeating-linear-gradient(-45deg,#9AA8B3 0 4px,#D5DDE2 4px 8px)}
.s9 .bars2 .flag{position:absolute;right:0;top:-6px;bottom:-4px;border-left:2px solid var(--ink)}
.s9 .bars2 .flag::after{content:"";position:absolute;top:0;left:0;border-left:9px solid var(--ink);border-top:5px solid transparent;border-bottom:5px solid transparent}
.s9 .pr .lg{display:flex;justify-content:space-between;gap:6px;font-size:11px;color:var(--mute)}
.s9 .pr .sw{font-size:11.5px;font-weight:700;letter-spacing:.04em}
.s9 .ahead{color:var(--ok)} .s9 .watch{color:var(--warn)} .s9 .off{color:var(--bad)}
.s9 .shift{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s9 .sc{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:12px 14px;text-align:left;color:inherit;display:grid;gap:8px;transition:transform .15s}
.s9 .sc:hover,.s9 .sc:focus-visible{transform:translateY(-3px);border-color:var(--coral)}
.s9 .sc .hd{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.s9 .sc .nm{font-weight:700;font-size:13.5px;line-height:1.2} .s9 .sc .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s9 .sc .chip{font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:999px;white-space:nowrap;color:#fff}
.s9 .slp{display:flex;flex-wrap:wrap;gap:3px;padding:4px 0;border-top:2px solid var(--rail);border-bottom:2px solid var(--rail)}
.s9 .slp i{width:10px;height:16px;border-radius:2px;background:#E3E9EA}
.s9 .slp i.y{background:var(--rail)} .s9 .slp i.l{background:var(--coral)}
.s9 .sc .meta{font-size:12px} .s9 .sc .meta b{font-family:var(--f-num);font-weight:400;font-size:18px}
.s9 .sc .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s9 .sc .nx{font-size:11.5px;color:var(--mute)}
.s9 .sc ul{list-style:none;margin:0;padding:0;font-size:12px;display:grid;gap:3px}
.s9 .sc li::before{content:"○ ";color:var(--mute)} .s9 .sc li.y::before{content:"● ";color:var(--rail)} .s9 .sc li.l{color:var(--bad);font-weight:600} .s9 .sc li.l::before{content:"● ";color:var(--coral)}
.s9 .vt{display:inline-flex;background:var(--ink);border-radius:999px;padding:3px}
.s9 .vt button{border:0;background:transparent;border-radius:999px;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:#DCE4E8}
.s9 .vt button[aria-pressed="true"]{background:var(--coral);color:#fff}
.s9 .profile{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s9 .chart{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:12px;overflow-x:auto}
.s9 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s9 .mlist{display:grid;gap:10px}
.s9 .mlist button{display:flex;justify-content:space-between;gap:12px;align-items:baseline;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12.5px}
.s9 .mlist b{font-family:var(--f-num);font-weight:400;font-size:24px;color:var(--ink);white-space:nowrap}
.s9 .mlist .why{background:var(--coral);border-color:var(--coral);color:#FFE5E0} .s9 .mlist .why b{color:#fff}
@media (max-width:1000px){ .s9 .head{grid-template-columns:1fr} .s9 .heads{justify-content:flex-start} .s9 .closures{grid-template-columns:1fr 1fr} .s9 .pairs,.s9 .shift{grid-template-columns:1fr 1fr} .s9 .profile{grid-template-columns:1fr} }
@media (max-width:600px){ .s9 .swipe{display:block} .s9 h2{font-size:52px} .s9 .closures,.s9 .pairs,.s9 .shift{grid-template-columns:1fr} .s9 .sh{flex:1 1 150px} .s9 .lv{font-size:11px} .s9 .dm{min-width:0;width:100%} }
`,
  render(){
    const C = { live:"#16825A", testing:"#E3A008", building:"#9AA8B3", blocked:"#C7372B", notstarted:"#C7CFD6" };
    const live = countParts("live");
    const head3 = (lit, n, lab, sub, attr) => { const cols = ["#C7372B","#E3A008","#16825A"]; return `<button class="sh" type="button" ${attr}><svg viewBox="0 0 30 62" aria-hidden="true"><rect x="3" y="1" width="24" height="60" rx="8" fill="#172A3A"/>${cols.map((c,i)=>`<circle cx="15" cy="${13+i*18}" r="6.5" fill="${i===lit?c:"#33424F"}" ${i===lit?`style="filter:drop-shadow(0 0 4px ${c})"`:""}/>`).join("")}</svg><span><span>${lab}</span><b>${n}</b><em>${sub}</em></span></button>`; };
    const heads = head3(1, `${live} / 12`, "PARTS LIVE", "plan 5", `data-tab="links"`) + head3(2, `${onCourse} / 9`, "KPIs ON COURSE", "plan 8", `data-tab="measures"`)
      + head3(1, `${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}`, "EBITDA BACK / OUT", "₹ lakh · plan 3.0 back", `data-ref="health:0"`) + head3(1, "JAN 2027", "BREAK-EVEN", "plan Dec 2026", `data-ref="health:0"`);

    /* --- the line --- */
    const W = 1000, H = 760, ty = 400, x0 = 40, x1 = 960;
    const sx = [130, 315, 500, 685, 870];
    let g = `<defs><path id="s9track" d="M${x0},${ty} L${x1},${ty}"/></defs>`;
    /* tomorrow's bed map board */
    const T = D.tomorrow;
    g += `<g aria-label="Tomorrow's bed map: ${T.mapped} of ${T.planned} planned admissions placed"><rect x="20" y="16" width="${W-40}" height="104" rx="12" fill="#172A3A"/>
      <text x="40" y="44" font-size="11" font-weight="700" letter-spacing="1.6" fill="#8FA0AE">TOMORROW'S BED MAP</text>
      <text x="40" y="78" font-family="Bebas Neue, sans-serif" font-size="40" fill="#FFFFFF">${T.mapped} of ${T.planned}</text><text x="40" y="100" font-size="11.5" fill="#DCE4E8">planned admissions placed in a bed</text>
      ${Array.from({length:T.planned},(_,i)=>{ const c = i%23, r = Math.floor(i/23); const st = i < T.mapped ? "#EE5A43" : "transparent"; return `<rect x="${270 + c*15}" y="${42 + r*30}" width="11" height="22" rx="3" fill="${st}" stroke="${i<T.mapped?"#EE5A43":"#8FA0AE"}" stroke-width="1.5" ${i>=T.mapped?'stroke-dasharray="3 2"':""}/>`; }).join("")}
      <text x="640" y="50" font-size="11.5" fill="#DCE4E8"><tspan font-weight="700" fill="#FFB4A6">${T.unmapped} not yet placed</tspan> (${T.icuUnmapped} need ICU)</text>
      <text x="640" y="72" font-size="11.5" fill="#DCE4E8">${T.reserve} beds held for emergencies</text>
      <text x="640" y="94" font-size="11.5" fill="#DCE4E8">First pass ${T.firstPass} · final freeze ${T.freeze}</text>
      <text x="${W-40}" y="50" text-anchor="end" font-size="10" letter-spacing="1.4" fill="#8FA0AE">ADMITTED TODAY</text>
      <text id="s9amt" x="${W-40}" y="80" text-anchor="end" font-family="Bebas Neue, sans-serif" font-size="32" fill="#FFFFFF">${D.today.admitted}</text>
      <text id="s9last" x="${W-40}" y="100" text-anchor="end" font-size="11" fill="#FFB4A6">last: ${esc(D.today.last)}</text></g>`;
    /* rails and sleepers */
    g += "<!--POLES-->";
    for (let x = x0; x <= x1; x += 18) g += `<rect x="${x}" y="${ty-12}" width="8" height="24" rx="1" fill="#C9B9A6"/>`;
    g += `<line x1="${x0}" x2="${x1}" y1="${ty-7}" y2="${ty-7}" stroke="#3B4A57" stroke-width="4"/><line x1="${x0}" x2="${x1}" y1="${ty+7}" y2="${ty+7}" stroke="#3B4A57" stroke-width="4"/>`;
    /* stage platforms */
    D.stages.forEach((s,i) => { const x = sx[i]; const pw = 150;
      g += `<polygon points="${x-pw/2},${ty+20} ${x+pw/2},${ty+20} ${x+pw/2+10},${ty+12} ${x-pw/2+10},${ty+12}" fill="#DCE4E8"/><rect x="${x-pw/2}" y="${ty+20}" width="${pw}" height="16" fill="#9AA8B3"/>
        <circle cx="${x}" cy="${ty}" r="15" fill="#FFFFFF" stroke="#172A3A" stroke-width="3"/><text x="${x}" y="${ty+6}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="18" fill="#172A3A">${i+1}</text>
        <foreignObject x="${x-pw/2}" y="${ty+40}" width="${pw}" height="58"><div xmlns="http://www.w3.org/1999/xhtml" style="font:700 11.5px/1.25 Poppins,sans-serif;color:#172A3A;text-align:center">${esc(s.name)}<div style="font-weight:600;font-size:10.5px;color:#C7372B">now ${s.now} min · was ${s.base}</div><div style="font-weight:400;font-size:10px;color:#52606D">can come down to ${s.floor} min</div></div></foreignObject>`; });
    /* signals for each part, above or below the line by stage */
    const slots = { above:[150,256], below:[520,600] };
    const byStage = [1,2,3,4,5].map(n => D.parts.filter(p=>p.stage===n));
    const SLOTS = i => i===2 ? [[500,180],[500,272],[500,555],[500,635],[500,715]] : [[sx[i],180],[sx[i],555],[sx[i],272],[sx[i],635],[sx[i],715]];
    let poles = "", cards = "";
    byStage.forEach((list,i) => { list.forEach((p,j) => {
      const [cx, cy] = SLOTS(i)[j]; const up = cy < ty; const cw = 160, ch = 66;
      const col = C[p.st]; const poleTop = up ? cy+ch/2 : ty+20, poleBot = up ? ty-14 : cy-ch/2;
      poles += `<line x1="${cx}" x2="${cx}" y1="${poleTop}" y2="${poleBot}" stroke="#52606D" stroke-width="2.5"/>`;
      cards += `<g class="sg" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}">
        <rect class="cd" x="${cx-cw/2}" y="${cy-ch/2}" width="${cw}" height="${ch}" rx="8" fill="#FFFFFF" stroke="#172A3A" stroke-width="1.5"/>
        <rect x="${cx-cw/2+6}" y="${cy-ch/2+6}" width="18" height="${ch-12}" rx="5" fill="#172A3A"/>
        <circle cx="${cx-cw/2+15}" cy="${cy-8}" r="5" fill="${col}" class="${p.st==="blocked"?"blink":""}"/><circle cx="${cx-cw/2+15}" cy="${cy+8}" r="5" fill="#33424F"/>
        <foreignObject x="${cx-cw/2+28}" y="${cy-ch/2+3}" width="${cw-32}" height="${ch-6}"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 10.5px/1.2 Poppins,sans-serif;color:#172A3A;height:${ch-6}px;display:flex;flex-direction:column;justify-content:center"><span><b style="font-family:'Bebas Neue';font-size:13px;font-weight:400;color:#EE5A43">${p.id}</b> ${esc(p.name)}</span><span style="font-weight:400;font-size:9.5px;color:${p.st==="notstarted"||p.st==="building"?"#52606D":col}">${PART_WORD[p.st]} · ${esc(p.when.replace(/^Live since /,"since ").replace(/^Goes live /,"live "))}</span></div></foreignObject></g>`;
    }); });
    g = g.replace("<!--POLES-->", poles) + cards;
    /* the patient carriage */
    g += `<g><rect x="-22" y="-12" width="44" height="18" rx="7" fill="#EE5A43" stroke="#172A3A" stroke-width="1.5"/><rect x="-14" y="-8" width="10" height="7" rx="1.5" fill="#FFE3DD"/><rect x="2" y="-8" width="10" height="7" rx="1.5" fill="#FFE3DD"/><animateMotion dur="9s" repeatCount="indefinite"><mpath href="#s9track"/></animateMotion></g>`;
    g += `<text x="${x0}" y="${ty-26}" font-size="11" font-weight="700" letter-spacing="1.4" fill="#EE5A43">ARRIVAL</text><text x="${x1}" y="${ty-26}" text-anchor="end" font-size="11" font-weight="700" letter-spacing="1.4" fill="#EE5A43">IN BED</text>`;
    const line = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="The five admission stages from arrival to the patient in bed, with each link shown beside the stage it speeds up, and tomorrow's bed map above.">${g}</svg>`;

    /* --- KPI pairs --- */
    const pr = k => { const n = Math.min(1,prog(k,k.now))*100, p = Math.min(1,prog(k,k.plan))*100; const col = k.state==="ahead"?"#16825A":k.state==="watch"?"#E3A008":"#C7372B";
      return `<button class="pr" type="button" data-ref="kpi:${k.id}"><span class="top"><span>${esc(k.name)}</span><b class="${k.state}">${fmtv(k,k.now)}</b></span>
        <span class="bars2" aria-hidden="true"><span class="r"><span>PLAN</span><span class="t pl"><i style="width:${p}%"></i></span></span><span class="r"><span>NOW</span><span class="t"><i style="width:${n}%;background:${col}"></i></span></span><span class="flag"></span></span>
        <span class="lg"><span>From ${fmtv(k,k.base)}</span><span class="sw ${k.state}">${STATE_WORD[k.state].toUpperCase()} · ${gapText(k)}</span><span>Target ${fmtv(k,k.target)}</span></span></button>`; };

    /* --- shift cards --- */
    const sc = p => { const cc = p.state==="ahead"?"#16825A":p.state==="watch"?"#A86E00":"#C7372B"; let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}">${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const b = []; for (let i=0;i<p.due;i++) b.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":""}"></i>`); body = `<span class="slp" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span><span class="meta"><b>${p.done}</b> of ${p.due} done${p.late?` · <b style="color:var(--bad)">${p.late}</b> late`:""}</span>`; }
      return `<button class="sc" type="button" data-ref="per:${p.key}"><span class="hd"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="chip" style="background:${cc}">${PERSON_WORD[p.state]}</span></span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</button>`; };

    /* --- money: net position profile --- */
    const CW = 760, CH = 300, cx0 = 50, cx1 = 740, n = D.cumMonths.length; const net = D.cumFore.map((v,i)=>v-D.cumSpend[i]), pnet = D.cumPlan.map((v,i)=>v-D.cumSpend[i]);
    const vmin = -10, vmax = 20, y0 = 26, y1 = 240; const bx = i => cx0 + (cx1-cx0)*i/(n-1), by = v => y1 - (y1-y0)*(v-vmin)/(vmax-vmin);
    const pts = a => a.map((v,i)=>`${bx(i).toFixed(1)},${by(v).toFixed(1)}`);
    let c = `<defs><clipPath id="s9neg"><rect x="0" y="${by(0)}" width="${CW}" height="${CH}"/></clipPath><clipPath id="s9pos"><rect x="0" y="0" width="${CW}" height="${by(0)}"/></clipPath></defs>`;
    [-10,0,10,20].forEach(v => c += `<line x1="${cx0}" x2="${cx1}" y1="${by(v)}" y2="${by(v)}" stroke="${v===0?"#172A3A":"#EEF2F2"}" stroke-width="${v===0?2:1}"/><text x="${cx0-8}" y="${by(v)+4}" text-anchor="end" font-size="10" fill="#52606D">${v>0?"+":""}${v}</text>`);
    const area = `M${bx(0)},${by(0)} L${pts(net).join(" L")} L${bx(n-1)},${by(0)} Z`;
    c += `<path d="${area}" fill="#EE5A43" fill-opacity=".25" clip-path="url(#s9neg)"/><path d="${area}" fill="#16825A" fill-opacity=".22" clip-path="url(#s9pos)"/>
      <polyline points="${pts(pnet).join(" ")}" fill="none" stroke="#52606D" stroke-width="1.5" stroke-dasharray="4 4"/>
      <polyline points="${pts(net).slice(0,D.actualTo+1).join(" ")}" fill="none" stroke="#172A3A" stroke-width="3"/><polyline points="${pts(net).slice(D.actualTo).join(" ")}" fill="none" stroke="#172A3A" stroke-width="2.5" stroke-dasharray="3 4"/>`;
    D.cumMonths.forEach((m,i) => c += `<text x="${bx(i)}" y="${y1+18}" text-anchor="middle" font-size="11" font-weight="600" fill="${i>D.actualTo?"#52606D":"#172A3A"}">${m}</text><rect data-ref="month:${i}" data-nopen x="${bx(i)-34}" y="${y0}" width="68" height="${y1-y0}" fill="transparent" style="cursor:help"/>`);
    const fi = D.breakeven.foreIdx, pi = D.breakeven.planIdx;
    c += `<g transform="translate(${bx(fi)},${by(0)})"><circle r="7" fill="#fff" stroke="#EE5A43" stroke-width="3"/><text x="10" y="-12" font-size="11.5" font-weight="700" fill="#C7372B">break-even, ${D.cumMonths[fi]}</text></g><g transform="translate(${bx(pi)},${by(0)})"><circle r="5" fill="#fff" stroke="#52606D" stroke-width="2" stroke-dasharray="2 2"/><text x="0" y="22" text-anchor="middle" font-size="10.5" fill="#52606D">plan</text></g>
      <text x="${cx0+6}" y="${by(-10)-6}" font-size="10.5" fill="#C7372B">still paying back</text><text x="${cx0+6}" y="${by(20)+12}" font-size="10.5" fill="#16825A">ahead of the money spent</text>
      <text x="${cx0}" y="${CH-12}" font-size="11" fill="#172A3A">Line: EBITDA back minus money out, to date (dashed: forecast) · grey dashed: plan · ₹ lakh</text>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="EBITDA back minus money out, to date. It crosses zero in ${D.cumMonths[fi]}; the plan crossed in ${D.cumMonths[pi]}.">${c}</svg>`;
    const mt = sum(D.spend.map(s=>s.v[1]));
    return `<div class="s9"><div class="wrap">
      <nav class="levers" aria-label="Suite sections"><div class="dm" aria-hidden="true"><small>YOU ARE ON</small><span id="s9at">OVERVIEW</span></div>
        ${TABS.map((t,i)=>`<button class="lv ${i?"":"on"}" type="button" data-tab="${t[0]}"><i></i>${t[1]}</button>`).join("")}</nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="heads" aria-label="Pulse strip">${heads}</div></div>
      <div class="closures" aria-label="Watch list and next go-live">${D.watch.map(w=>`<button class="cl" type="button" data-ref="${w.ref}">${esc(w.t)}<small>${esc(P[w.who].name)}</small></button>`).join("")}
        <button class="stub" type="button" data-ref="part:${D.milestone.part}"><b>${D.milestone.days}</b><span>DAYS TO THE NEXT GO-LIVE<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to see every stage →</p><div class="line">${line}</div>
        <div class="legend"><span><i style="background:#16825A"></i>Live</span><span><i style="background:#E3A008"></i>Testing</span><span><i style="background:#9AA8B3"></i>Being built</span><span><i style="background:#C7372B"></i>Late</span><span><i style="background:#C7CFD6"></i>Not started</span><span>· Data as of ${esc(D.asOf)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3><p>Hatched bar is the plan for this week · solid bar is today · the flag is the target</p></div><div class="pairs">${D.kpis.map(pr).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="shift">${D.people.map(sc).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="profile"><div class="chart">${chart}</div>
          <div class="mlist">
            <button type="button" data-ref="month:1"><span>Subscription, each month</span><b>${L(D.spend[0].v[1])}</b></button>
            <button type="button" data-ref="month:1"><span>Salaries of the Bed Manager and Admissions Executive we recommended, each month</span><b>${L(D.spend[1].v[1])}</b></button>
            <button type="button" data-ref="month:1"><span>One-time so far (messaging set-up, bed board screens)</span><b>${L(sum(D.spend[2].v))}</b></button>
            <button type="button" data-ref="health:0"><span>Extra revenue so far, from billing that starts earlier</span><b>${L(revTotal)}</b></button>
            <button type="button" data-ref="health:0"><span>EBITDA now, and at full run, each month</span><b>${L(D.ebitda[1])} → ${L(D.runRate.ebitda)}</b></button>
            <button type="button" class="why" data-ref="health:0"><span>Break-even ${D.breakeven.fore}, ${D.breakeven.late} late. See why</span><b>›</b></button>
          </div></div></section>
    </div></div>`;
  },
  after(){
    document.querySelectorAll(".s9 .lv").forEach(b => b.addEventListener("click", () => { const at = document.getElementById("s9at"); if (at) at.textContent = b.textContent.trim().toUpperCase(); }));
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { document.querySelectorAll(".s9 animateMotion").forEach(a => a.remove()); return; }
    admitTicker("s9", ".s9 .sg");
  }
});
