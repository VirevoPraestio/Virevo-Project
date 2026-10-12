/* ===== Admission Process, option 2: the radar (indigo and sunflower) ===== */
SCHEMES.push({
  key:"radar", letter:"2", name:"Indigo and sunflower",
  note:"<b>Option 2 · indigo and sunflower.</b> Tomorrow's planned admissions show as points on a radar closing in on the bed map at the centre; the twelve links sit round the rim.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#16133A","--sh-mute":"#5B5878","--sh-line":"#DCDBEA","--sh-card":"#F6F6FB","--c-ok":"#0F8A61","--c-warn":"#A87400","--c-bad":"#C93636","--pk-bg":"#16133A","--pk-fg":"#FFFFFF","--pk-line":"#F5B700","--pk-r":"14px","--sh-r":"22px" },
  fab:18,
  blocks:{ nav:".bar", pulse:".rings", watch:".alerts", countdown:".eta", hero:".scope", kpis:".eyes", team:".dots", money:".fall" },
  css:`
.s10{--bg:#F4F5FA;--ink:#16133A;--mute:#5B5878;--sun:#F5B700;--sun2:#FFE08A;--deep:#14123A;--ok:#0F8A61;--warn:#A87400;--bad:#C93636;--line:#DCDBEA;
  background:var(--bg);color:var(--ink);padding:18px 16px 90px;overflow-x:clip}
.s10 .wrap{max-width:1240px;margin:0 auto}
.s10 .bar{display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;background:var(--deep);border-radius:999px;padding:8px 10px 8px 16px;box-shadow:0 12px 26px rgba(22,19,58,.22)}
.s10 .trk{display:flex;align-items:center;gap:10px;color:#fff;font-family:var(--f-num);font-size:22px;letter-spacing:.06em;line-height:1}
.s10 .trk small{display:block;font-family:var(--f-body);font-size:9.5px;letter-spacing:.16em;color:#A9A6D6}
.s10 .trk i{width:26px;height:26px;border-radius:50%;border:2px solid #3E3B7A;background:conic-gradient(from 0deg,rgba(245,183,0,.9),transparent 25%);animation:s10spin 3s linear infinite}
@keyframes s10spin{to{transform:rotate(360deg)}}
.s10 .pl{display:flex;flex-wrap:wrap;gap:4px}
.s10 .pb{background:transparent;border:0;border-radius:999px;padding:9px 14px;color:#DAD8F2;font-size:12.5px;font-weight:600;min-height:40px}
.s10 .pb:hover{background:#2A2760}
.s10 .pb.on{background:var(--sun);color:var(--deep)}
.s10 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:22px 0 14px}
.s10 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:#6E5A00}
.s10 h2{font-family:var(--f-num);font-weight:400;font-size:72px;line-height:.9;margin:4px 0 0;letter-spacing:.01em}
.s10 .rings{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}
.s10 .rg{display:grid;grid-template-columns:56px minmax(0,1fr);gap:10px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:8px 12px 8px 8px;text-align:left;color:inherit;min-width:160px}
.s10 .rg svg{width:56px;height:56px}
.s10 .rg span{display:block;font-size:10.5px;letter-spacing:.1em;font-weight:600;color:var(--mute)}
.s10 .rg b{display:block;font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1}
.s10 .rg em{font-style:normal;font-size:11px;color:#6E5A00}
.s10 .alerts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.9fr);gap:12px;margin-bottom:14px}
.s10 .al{display:grid;grid-template-columns:30px minmax(0,1fr);gap:10px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:10px 12px;text-align:left;color:inherit;font-size:12.5px;font-weight:600}
.s10 .al i{width:28px;height:28px;border-radius:50%;background:#FFF3C4;display:grid;place-items:center;font-style:normal;color:var(--bad);font-weight:800;box-shadow:0 0 0 3px #FFE08A}
.s10 .al small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s10 .eta{display:flex;align-items:center;gap:12px;background:var(--sun);color:var(--deep);border:0;border-radius:14px;padding:8px 14px;text-align:left}
.s10 .eta b{font-family:var(--f-num);font-weight:400;font-size:44px;line-height:.9}
.s10 .eta span{font-size:12px;font-weight:700;letter-spacing:.04em} .s10 .eta small{display:block;font-weight:400;letter-spacing:0;font-size:11.5px}
.s10 .scope{border-radius:24px;background:#fff;border:1.5px solid var(--line);overflow-x:auto;box-shadow:0 16px 34px rgba(22,19,58,.07)}
.s10 .scope svg{display:block;width:100%;min-width:900px;height:auto}
.s10 .swipe{display:none;margin:0 0 6px;font-size:12px;color:#6E5A00}
.s10 .stn{cursor:pointer}
.s10 .stn:focus{outline:none} .s10 .stn:focus .cd{stroke:#F2B705;stroke-width:3}
.s10 .stn:hover .cd{stroke:var(--sun)}
.s10 .stn.ping .cd{animation:s10ping .9s ease}
@keyframes s10ping{0%{fill:#FFF3C4}100%{fill:#FFFFFF}}
.s10 .flow{animation:s10flow 1.2s linear infinite} .s10 .flow.slow{animation-duration:3.4s}
@keyframes s10flow{to{stroke-dashoffset:-18}}
.s10 .pulse{animation:s10pulse 1.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes s10pulse{50%{transform:scale(1.6);opacity:.4}}
.s10 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:8px}
.s10 .legend i{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-1px;margin-right:6px}
.s10 .zone{margin-top:40px;scroll-margin-top:20px;border-radius:24px}
.s10 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:14px}
.s10 .zh h3{font-family:var(--f-num);font-weight:400;font-size:38px;margin:0;line-height:1;display:flex;align-items:center;gap:12px}
.s10 .zh h3::before{content:"";width:22px;height:22px;border-radius:50%;border:2px solid var(--ink);background:radial-gradient(circle,var(--sun) 0 3px,transparent 4px),radial-gradient(circle,transparent 0 6px,var(--ink) 6px 7px,transparent 8px)}
.s10 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s10 .eyes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.s10 .ey{display:grid;grid-template-columns:100px minmax(0,1fr);gap:12px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:10px 12px;text-align:left;color:inherit;transition:transform .15s}
.s10 .ey:hover,.s10 .ey:focus-visible{transform:translateY(-2px);border-color:var(--sun)}
.s10 .ey svg{width:100px;height:100px}
.s10 .ey .nm{font-size:13px;font-weight:600;line-height:1.3}
.s10 .ey b{display:block;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1;margin-top:4px}
.s10 .ey .st{display:block;font-size:11px;font-weight:700;letter-spacing:.05em;margin-top:4px}
.s10 .ey .rgx{display:block;font-size:11px;color:var(--mute);margin-top:2px}
.s10 .ahead{color:var(--ok)} .s10 .watch{color:var(--warn)} .s10 .off{color:var(--bad)}
.s10 .dots{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s10 .dc{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:12px 14px;text-align:left;color:inherit;display:grid;gap:8px;transition:transform .15s}
.s10 .dc:hover,.s10 .dc:focus-visible{transform:translateY(-3px);border-color:var(--sun)}
.s10 .dc .hd{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.s10 .dc .nm{font-weight:700;font-size:13.5px;line-height:1.2} .s10 .dc .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s10 .dc .chip{font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:999px;white-space:nowrap;border:1.5px solid currentColor}
.s10 .tl{position:relative;display:flex;flex-wrap:wrap;gap:6px;padding:4px 0}
.s10 .tl i{width:12px;height:12px;border-radius:50%;border:2px solid var(--ink);background:#fff}
.s10 .tl i.y{background:var(--ink)} .s10 .tl i.l{border-color:var(--bad);background:#FFD9D9}
.s10 .dc .meta{font-size:12px} .s10 .dc .meta b{font-family:var(--f-num);font-weight:400;font-size:18px}
.s10 .dc .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s10 .dc .nx{font-size:11.5px;color:var(--mute)}
.s10 .dc ul{list-style:none;margin:0;padding:0;font-size:12px;display:grid;gap:3px}
.s10 .dc li::before{content:"○ ";color:var(--mute)} .s10 .dc li.y::before{content:"● ";color:var(--ink)} .s10 .dc li.l{color:var(--bad);font-weight:600} .s10 .dc li.l::before{content:"◉ ";color:var(--bad)}
.s10 .vt{display:inline-flex;background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:3px}
.s10 .vt button{border:0;background:transparent;border-radius:999px;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:var(--ink)}
.s10 .vt button[aria-pressed="true"]{background:var(--deep);color:#fff}
.s10 .fall{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s10 .chart{background:#fff;border:1.5px solid var(--line);border-radius:22px;padding:12px;overflow-x:auto}
.s10 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s10 .mlist{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.s10 .mlist button{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12px}
.s10 .mlist b{display:block;font-family:var(--f-num);font-weight:400;font-size:24px;line-height:1.1;color:var(--ink)}
.s10 .mlist .why{grid-column:1/-1;background:var(--deep);border-color:var(--deep);color:#DAD8F2} .s10 .mlist .why b{color:var(--sun)}
@media (max-width:1000px){ .s10 .head{grid-template-columns:1fr} .s10 .rings{justify-content:flex-start} .s10 .alerts{grid-template-columns:1fr 1fr} .s10 .eyes,.s10 .dots{grid-template-columns:1fr 1fr} .s10 .fall{grid-template-columns:1fr} .s10 .bar{border-radius:20px} }
@media (max-width:600px){ .s10 .swipe{display:block} .s10 h2{font-size:52px} .s10 .alerts,.s10 .eyes,.s10 .dots{grid-template-columns:1fr} .s10 .rg{flex:1 1 150px} }
`,
  render(){
    const C = { live:"#0F8A61", testing:"#E0A500", building:"#9C99BF", blocked:"#C93636", notstarted:"#CFCDE3" };
    const live = countParts("live");
    const ring = (f, col, val, lab, sub, attr) => { const R = 22, Cc = 2*Math.PI*R; return `<button class="rg" type="button" ${attr}><svg viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="${R}" fill="none" stroke="#ECEBF5" stroke-width="7"/><circle cx="28" cy="28" r="${R}" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round" stroke-dasharray="${(Cc*Math.min(1,f)).toFixed(1)} ${Cc}" transform="rotate(-90 28 28)"/><circle cx="28" cy="28" r="4" fill="#16133A"/></svg><span><span>${lab}</span><b>${val}</b><em>${sub}</em></span></button>`; };
    const rings = ring(live/12, "#F5B700", `${live} / 12`, "PARTS LIVE", "plan 5", `data-tab="links"`) + ring(onCourse/9, "#F5B700", `${onCourse} / 9`, "KPIs ON COURSE", "plan 8", `data-tab="measures"`)
      + ring(ebitdaTotal/spendTotal, "#0F8A61", `${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}`, "EBITDA BACK / OUT", "₹ lakh · plan 3.0 back", `data-ref="health:0"`) + ring(.4, "#C93636", "JAN 2027", "BREAK-EVEN", "plan Dec 2026", `data-ref="health:0"`);

    /* --- the radar --- */
    const W = 1000, H = 720, cx = 500, cy = 360, R = 220; const T = D.tomorrow;
    let g = `<defs><radialGradient id="s10bg"><stop offset="0" stop-color="#232063"/><stop offset="1" stop-color="#14123A"/></radialGradient><linearGradient id="s10sw" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#F5B700" stop-opacity="0"/><stop offset="1" stop-color="#F5B700" stop-opacity=".45"/></linearGradient></defs>`;
    g += `<circle cx="${cx}" cy="${cy}" r="${R+14}" fill="#E9E8F4"/><circle cx="${cx}" cy="${cy}" r="${R}" fill="url(#s10bg)"/>`;
    [0.25,0.5,0.75,1].forEach(f => g += `<circle cx="${cx}" cy="${cy}" r="${R*f}" fill="none" stroke="#3E3B7A" stroke-width="1"/>`);
    for (let a=0;a<12;a++){ const t = a*Math.PI/6; g += `<line x1="${cx}" y1="${cy}" x2="${cx+R*Math.cos(t)}" y2="${cy+R*Math.sin(t)}" stroke="#2C2A5C"/>`; }
    g += `<g><path d="M${cx},${cy} L${cx+R},${cy} A${R},${R} 0 0 0 ${cx+R*Math.cos(-Math.PI/5)},${cy+R*Math.sin(-Math.PI/5)} Z" fill="url(#s10sw)"/><animateTransform attributeName="transform" type="rotate" from="0 ${cx} ${cy}" to="360 ${cx} ${cy}" dur="6s" repeatCount="indefinite"/></g>`;
    /* blips: tomorrow's planned admissions, placed between the rim and the centre */
    let seed = 7; const rnd = () => (seed = (seed*9301 + 49297) % 233280) / 233280;
    for (let i=0;i<T.planned;i++){ const a = rnd()*Math.PI*2, r = R*(0.36 + rnd()*0.58); const x = cx + r*Math.cos(a), y = cy + r*Math.sin(a);
      g += i < T.mapped ? `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="#F5B700"/>` : `<circle class="pulse" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="5" fill="none" stroke="#FF8A8A" stroke-width="2"/>`; }
    /* centre: the bed map */
    g += `<circle cx="${cx}" cy="${cy}" r="82" fill="#FFFFFF"/><text x="${cx}" y="${cy-26}" text-anchor="middle" font-size="9.5" font-weight="700" letter-spacing="1.3" fill="#5B5878">TOMORROW'S BED MAP</text>
      <text x="${cx}" y="${cy+8}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="36" fill="#16133A">${T.mapped} / ${T.planned}</text>
      <text x="${cx}" y="${cy+26}" text-anchor="middle" font-size="10" fill="#5B5878">placed in a bed</text><text x="${cx}" y="${cy+42}" text-anchor="middle" font-size="10" font-weight="700" fill="#C93636">${T.unmapped} not yet (${T.icuUnmapped} ICU)</text>`;
    g += `<text x="${cx}" y="${cy+R-26}" text-anchor="middle" font-size="10" fill="#A9A6D6">freeze ${T.freeze} · ${T.reserve} beds held for emergencies</text>`;
    /* stations round the rim */
    const cw = 176, ch = 60; let wires = "", stns = "";
    D.parts.forEach((p,i) => { const t = -Math.PI/2 + i*Math.PI/6; const sxp = cx + (R+150)*Math.cos(t)*1.06, syp = cy + (R+82)*Math.sin(t);
      const ex = cx + (R+2)*Math.cos(t), ey = cy + (R+2)*Math.sin(t); const col = C[p.st];
      const dash = p.st==="live" ? `stroke-dasharray="6 4" class="flow"` : p.st==="testing" ? `stroke-dasharray="6 4" class="flow slow"` : p.st==="blocked" ? "" : `stroke-dasharray="2 5"`;
      wires += `<line x1="${sxp}" y1="${syp}" x2="${ex}" y2="${ey}" stroke="${col}" stroke-width="${p.st==="notstarted"||p.st==="building"?2:3}" ${dash}/>`;
      stns += `<g class="stn" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}">
        <rect class="cd" x="${sxp-cw/2}" y="${syp-ch/2}" width="${cw}" height="${ch}" rx="${ch/2}" fill="#FFFFFF" stroke="#16133A" stroke-width="1.5"/>
        <circle cx="${sxp-cw/2+ch/2}" cy="${syp}" r="17" fill="${p.st==="notstarted"||p.st==="building"?"#fff":col}" stroke="${col==="#CFCDE3"?"#9C99BF":col}" stroke-width="2.5" ${p.st==="building"||p.st==="notstarted"?'stroke-dasharray="4 3"':""}/>
        <text x="${sxp-cw/2+ch/2}" y="${syp+6}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="17" fill="${p.st==="notstarted"||p.st==="building"?"#16133A":"#fff"}">${p.id}</text>
        <foreignObject x="${sxp-cw/2+ch-2}" y="${syp-ch/2+3}" width="${cw-ch-8}" height="${ch-6}"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 9.8px/1.18 Poppins,sans-serif;color:#16133A;height:${ch-6}px;display:flex;flex-direction:column;justify-content:center">${esc(p.name)}<span style="font-weight:400;font-size:9.3px;color:${p.st==="notstarted"||p.st==="building"?"#5B5878":col}">${PART_WORD[p.st]} · ${esc(p.when.replace(/^Live since /,"since ").replace(/^Goes live /,"live "))}</span></div></foreignObject></g>`; });
    g = g.replace(`<circle cx="${cx}" cy="${cy}" r="${R+14}"`, wires + `<circle cx="${cx}" cy="${cy}" r="${R+14}"`) + stns;
    g += `<text x="24" y="30" font-size="11" font-weight="700" letter-spacing="1.4" fill="#6E5A00">ADMITTED TODAY</text><text id="s10amt" x="24" y="66" font-family="Bebas Neue, sans-serif" font-size="40" fill="#16133A">${D.today.admitted}</text><text id="s10last" x="24" y="86" font-size="11" fill="#5B5878">last: ${esc(D.today.last)}</text>
      <text x="${W-24}" y="30" text-anchor="end" font-size="11" font-weight="700" letter-spacing="1.4" fill="#6E5A00">ARRIVAL TO BED, AVERAGE</text><text x="${W-24}" y="66" text-anchor="end" font-family="Bebas Neue, sans-serif" font-size="40" fill="#16133A">${esc(D.today.avgTat)}</text><text x="${W-24}" y="86" text-anchor="end" font-size="11" fill="#5B5878">was 3 h 20 min · floor 30 min</text>`;
    const scope = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Radar of tomorrow's planned admissions: ${T.mapped} of ${T.planned} placed in a bed. The twelve links sit round the rim.">${g}</svg>`;

    /* --- KPI bullseyes --- */
    const ey = k => { const n = Math.min(1,prog(k,k.now)), p = Math.min(1,prog(k,k.plan)); const col = k.state==="ahead"?"#0F8A61":k.state==="watch"?"#E0A500":"#C93636"; const Rr = 44, c0 = 50;
      const ang = (k.id.charCodeAt(1)*47 % 360) * Math.PI/180; const dx = c0 + (1-n)*Rr*Math.cos(ang), dy = c0 + (1-n)*Rr*Math.sin(ang);
      return `<button class="ey" type="button" data-ref="kpi:${k.id}"><svg viewBox="0 0 100 100" aria-hidden="true">${[1,.75,.5,.25].map((f,i)=>`<circle cx="${c0}" cy="${c0}" r="${Rr*f}" fill="${i%2?"#FFFFFF":"#F2F1FA"}" stroke="#DCDBEA"/>`).join("")}<circle cx="${c0}" cy="${c0}" r="5" fill="#F5B700" stroke="#16133A"/>
        <circle cx="${c0}" cy="${c0}" r="${Math.max(3,(1-p)*Rr)}" fill="none" stroke="#16133A" stroke-width="1.5" stroke-dasharray="3 3"/><circle cx="${dx.toFixed(1)}" cy="${dy.toFixed(1)}" r="6" fill="${col}" stroke="#fff" stroke-width="2"/></svg>
        <span><span class="nm">${esc(k.name)}</span><b class="${k.state}">${fmtv(k,k.now)}</b><span class="st ${k.state}">${STATE_WORD[k.state].toUpperCase()} · ${gapText(k)}</span><span class="rgx">From ${fmtv(k,k.base)} · target ${fmtv(k,k.target)}</span></span></button>`; };

    /* --- dot timelines --- */
    const dc = p => { const cc = p.state==="ahead"?"#0F8A61":p.state==="watch"?"#A87400":"#C93636"; let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}">${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const b = []; for (let i=0;i<p.due;i++) b.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":""}"></i>`); body = `<span class="tl" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span><span class="meta"><b>${p.done}</b> of ${p.due} done${p.late?` · <b style="color:var(--bad)">${p.late}</b> late`:""}</span>`; }
      return `<button class="dc" type="button" data-ref="per:${p.key}"><span class="hd"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="chip" style="color:${cc}">${PERSON_WORD[p.state]}</span></span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</button>`; };

    /* --- money: monthly steps of the net position --- */
    const CW = 760, CH = 300, cx0 = 50, cx1 = 740, n = D.cumMonths.length, bw = (cx1-cx0)/n;
    const net = D.cumFore.map((v,i)=>v-D.cumSpend[i]), pnet = D.cumPlan.map((v,i)=>v-D.cumSpend[i]);
    const vmin = -10, vmax = 20, y0 = 26, y1 = 240, by = v => y1 - (y1-y0)*(v-vmin)/(vmax-vmin);
    let c = ""; [-10,0,10,20].forEach(v => c += `<line x1="${cx0}" x2="${cx1}" y1="${by(v)}" y2="${by(v)}" stroke="${v===0?"#16133A":"#ECEBF5"}" stroke-width="${v===0?2:1}"/><text x="${cx0-8}" y="${by(v)+4}" text-anchor="end" font-size="10" fill="#5B5878">${v>0?"+":""}${v}</text>`);
    net.forEach((v,i) => { const prev = i ? net[i-1] : 0; const x = cx0 + i*bw + 8, w = bw-16; const top = Math.max(v,prev), bot = Math.min(v,prev); const fore = i > D.actualTo; const col = v >= 0 ? "#0F8A61" : "#C93636";
      c += `<g data-ref="month:${i}" data-nopen style="cursor:help"><rect x="${x}" y="${by(top)}" width="${w}" height="${Math.max(2,by(bot)-by(top))}" rx="3" fill="${col}" fill-opacity="${fore?.3:.85}" ${fore?`stroke="${col}" stroke-dasharray="3 3"`:""}/>
        ${i<n-1?`<line x1="${x+w}" x2="${x+bw+8}" y1="${by(v)}" y2="${by(v)}" stroke="#5B5878" stroke-dasharray="2 2"/>`:""}<text x="${x+w/2}" y="${y1+18}" text-anchor="middle" font-size="11" font-weight="600" fill="${fore?"#5B5878":"#16133A"}">${D.cumMonths[i]}</text><rect x="${x-8}" y="${y0}" width="${bw}" height="${y1-y0}" fill="transparent"/></g>`; });
    c += `<polyline points="${pnet.map((v,i)=>`${cx0+i*bw+bw/2},${by(v)}`).join(" ")}" fill="none" stroke="#F5B700" stroke-width="2" stroke-dasharray="5 4"/>`;
    const fi = D.breakeven.foreIdx; c += `<text x="${cx0+fi*bw+bw/2}" y="${by(net[fi])-10}" text-anchor="middle" font-size="11" font-weight="700" fill="#0F8A61">break-even</text>
      <text x="${cx0}" y="${CH-12}" font-size="11" fill="#16133A">Each step: what the month adds to EBITDA back minus money out (faded: forecast) · yellow dashed: plan · ₹ lakh</text>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="Month by month, the net position climbs from below zero and crosses it in ${D.cumMonths[fi]}.">${c}</svg>`;
    return `<div class="s10"><div class="wrap">
      <nav class="bar" aria-label="Suite sections"><div class="trk" aria-hidden="true"><i></i><span><small>YOU ARE ON</small><span id="s10at">OVERVIEW</span></span></div>
        <div class="pl">${TABS.map((t,i)=>`<button class="pb ${i?"":"on"}" type="button" data-tab="${t[0]}">${t[1]}</button>`).join("")}</div></nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="rings" aria-label="Pulse strip">${rings}</div></div>
      <div class="alerts" aria-label="Watch list and next go-live">${D.watch.map(w=>`<button class="al" type="button" data-ref="${w.ref}"><i aria-hidden="true">!</i><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}
        <button class="eta" type="button" data-ref="part:${D.milestone.part}"><b>${D.milestone.days}</b><span>DAYS TO THE NEXT GO-LIVE<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to see every link →</p><div class="scope">${scope}</div>
        <div class="legend"><span><i style="background:#F5B700"></i>Placed in a bed</span><span><i style="border:2px solid #FF8A8A"></i>Not yet placed</span><span><i style="background:#0F8A61"></i>Live</span><span><i style="background:#E0A500"></i>Testing</span><span><i style="background:#9C99BF"></i>Being built</span><span><i style="background:#C93636"></i>Late</span><span><i style="background:#CFCDE3"></i>Not started</span><span>· Data as of ${esc(D.asOf)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3><p>The centre is the target · the dot is today · the dashed ring is where the plan says we should be</p></div><div class="eyes">${D.kpis.map(ey).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="dots">${D.people.map(dc).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh, month by month</p></div>
        <div class="fall"><div class="chart">${chart}</div>
          <div class="mlist">
            <button type="button" data-ref="month:1">Subscription<b>${L(D.spend[0].v[1])}/mo</b></button>
            <button type="button" data-ref="month:1">Bed Manager and Admissions Executive we recommended<b>${L(D.spend[1].v[1])}/mo</b></button>
            <button type="button" data-ref="month:1">One-time so far<b>${L(sum(D.spend[2].v))}</b></button>
            <button type="button" data-ref="health:0">Extra revenue so far<b>${L(revTotal)}</b></button>
            <button type="button" data-ref="health:0">EBITDA now<b>${L(D.ebitda[1])}/mo</b></button>
            <button type="button" data-ref="health:0">EBITDA at full run<b>${L(D.runRate.ebitda)}/mo</b></button>
            <button type="button" class="why" data-ref="health:0">Break-even ${D.breakeven.fore}, ${D.breakeven.late} late<b>See why and the recovery plan ›</b></button>
          </div></div></section>
    </div></div>`;
  },
  after(){
    document.querySelectorAll(".s10 .pb").forEach(b => b.addEventListener("click", () => { const at = document.getElementById("s10at"); if (at) at.textContent = b.textContent.trim().toUpperCase(); }));
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { document.querySelectorAll(".s10 animateTransform").forEach(a => a.remove()); return; }
    admitTicker("s10", ".s10 .stn");
  }
});
