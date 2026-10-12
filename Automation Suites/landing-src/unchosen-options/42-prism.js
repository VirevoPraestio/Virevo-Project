/* ===== Diagnostic Scheduling, option 2: the prism (ink and spectrum on cool white) ===== */
SCHEMES.push({
  key:"prism", letter:"2", name:"Ink and spectrum",
  note:"<b>Option 2 · ink and spectrum.</b> Each OPD prescription enters as one beam and the scheduling rules split it into its tests, each beam running to the room or service that delivers it.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#12141C","--sh-mute":"#565B68","--sh-line":"#DDE1E7","--sh-card":"#F6F7F9","--c-ok":"#0E8A62","--c-warn":"#A86B05","--c-bad":"#C92F38","--pk-bg":"#12141C","--pk-fg":"#FFFFFF","--pk-line":"#0891B2","--pk-r":"12px","--sh-r":"20px" },
  fab:18,
  blocks:{ nav:".spec", pulse:".lenses", watch:".refr", countdown:".focus", hero:".bench", kpis:".sliders", team:".bands", money:".glow" },
  css:`
.s12{--bg:#F6F7F9;--ink:#12141C;--mute:#565B68;--cyan:#0891B2;--orange:#EA580C;--ok:#0E8A62;--warn:#A86B05;--bad:#C92F38;--line:#DDE1E7;
  background:var(--bg);color:var(--ink);padding:18px 16px 90px;overflow-x:clip}
.s12 .wrap{max-width:1240px;margin:0 auto}
.s12 .spec{display:flex;flex-wrap:wrap;align-items:stretch;gap:0;background:#fff;border:1.5px solid var(--line);border-radius:14px;overflow:hidden}
.s12 .vw{display:flex;flex-direction:column;justify-content:center;padding:8px 16px;background:var(--ink);color:#fff;font-family:var(--f-num);font-size:22px;letter-spacing:.06em;line-height:1;min-width:150px}
.s12 .vw small{font-family:var(--f-body);font-size:9.5px;letter-spacing:.16em;color:#9AA1B0}
.s12 .sg{flex:1 1 auto;background:#fff;border:0;border-top:4px solid var(--h);padding:10px 12px;font-size:12.5px;font-weight:600;color:var(--ink);min-height:48px}
.s12 .sg:hover{background:color-mix(in srgb,var(--h) 10%,#fff)}
.s12 .sg.on{background:var(--h);color:#fff}
.s12 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:22px 0 14px}
.s12 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--cyan)}
.s12 h2{font-family:var(--f-num);font-weight:400;font-size:72px;line-height:.9;margin:4px 0 0;letter-spacing:.01em;background:linear-gradient(90deg,#12141C 55%,#2563EB 75%,#0891B2 85%,#059669 95%);-webkit-background-clip:text;background-clip:text;color:transparent}
.s12 .lenses{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}
.s12 .ln{display:grid;grid-template-columns:52px minmax(0,1fr);gap:10px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:6px 16px 6px 6px;text-align:left;color:inherit;min-width:170px}
.s12 .ln i{width:52px;height:52px;border-radius:50%;background:conic-gradient(var(--h) var(--f),#ECEEF2 0);display:grid;place-items:center}
.s12 .ln i::after{content:"";width:34px;height:34px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#E8F6FA)}
.s12 .ln span{display:block;font-size:10.5px;letter-spacing:.1em;font-weight:600;color:var(--mute)}
.s12 .ln b{display:block;font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1}
.s12 .ln em{font-style:normal;font-size:11px;color:var(--cyan)}
.s12 .refr{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.9fr);gap:12px;margin-bottom:14px}
.s12 .rf{position:relative;display:grid;grid-template-columns:30px minmax(0,1fr);gap:10px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:10px 12px;text-align:left;color:inherit;font-size:12.5px;font-weight:600}
.s12 .rf i{width:0;height:0;border-left:13px solid transparent;border-right:13px solid transparent;border-bottom:22px solid var(--bad)}
.s12 .rf small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s12 .focus{display:flex;align-items:center;gap:12px;border:0;border-radius:14px;padding:8px 14px;text-align:left;color:#fff;background:linear-gradient(120deg,#2563EB,#0891B2 55%,#059669)}
.s12 .focus b{font-family:var(--f-num);font-weight:400;font-size:44px;line-height:.9}
.s12 .focus span{font-size:12px;font-weight:700;letter-spacing:.04em} .s12 .focus small{display:block;font-weight:400;letter-spacing:0;font-size:11.5px;color:#E6F7FB}
.s12 .bench{border-radius:20px;background:#0E1018;border:1.5px solid #222636;overflow-x:auto;box-shadow:0 16px 34px rgba(18,20,28,.18)}
.s12 .bench svg{display:block;width:100%;min-width:920px;height:auto}
.s12 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--cyan)}
.s12 .st{cursor:pointer}
.s12 .st:focus{outline:none} .s12 .st:focus .cd{stroke:#F2B705;stroke-width:3}
.s12 .st:hover .cd{stroke:#7DD3FC}
.s12 .st.ping .cd{animation:s12ping .9s ease}
@keyframes s12ping{0%{fill:#23304A}100%{fill:#171A26}}
.s12 .beam{animation:s12beam 1.4s linear infinite} .s12 .beam.slow{animation-duration:4s}
@keyframes s12beam{to{stroke-dashoffset:-30}}
.s12 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:8px}
.s12 .legend i{display:inline-block;width:24px;height:0;border-top:3px solid;vertical-align:middle;margin-right:6px}
.s12 .zone{margin-top:40px;scroll-margin-top:20px;border-radius:20px}
.s12 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:14px}
.s12 .zh h3{font-family:var(--f-num);font-weight:400;font-size:38px;margin:0;line-height:1;display:flex;align-items:center;gap:12px}
.s12 .zh h3::before{content:"";width:40px;height:6px;border-radius:3px;background:linear-gradient(90deg,#7C3AED,#2563EB,#0891B2,#059669,#D97706,#DC2626)}
.s12 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s12 .sliders{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.s12 .sl{background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:12px 14px 14px;text-align:left;color:inherit;display:grid;gap:10px;transition:transform .15s}
.s12 .sl:hover,.s12 .sl:focus-visible{transform:translateY(-2px);border-color:var(--cyan)}
.s12 .sl .top{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.s12 .sl .top span{font-size:13px;font-weight:600;line-height:1.3}
.s12 .sl .top b{font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1;white-space:nowrap}
.s12 .trk{position:relative;height:10px;border-radius:5px;background:linear-gradient(90deg,#ECEEF2,var(--h));margin:6px 8px}
.s12 .trk .kn{position:absolute;top:50%;width:20px;height:20px;border-radius:50%;background:#fff;border:4px solid var(--c);transform:translate(-50%,-50%);box-shadow:0 2px 6px rgba(0,0,0,.2)}
.s12 .trk .gh{position:absolute;top:50%;width:18px;height:18px;border-radius:50%;border:2px dashed var(--ink);transform:translate(-50%,-50%)}
.s12 .trk .tg{position:absolute;right:-6px;top:-7px;width:3px;height:24px;background:var(--ink);border-radius:2px}
.s12 .sl .lg{display:flex;justify-content:space-between;gap:6px;font-size:11px;color:var(--mute)}
.s12 .sl .sw{font-size:11.5px;font-weight:700;letter-spacing:.04em}
.s12 .ahead{color:var(--ok)} .s12 .watch{color:var(--warn)} .s12 .off{color:var(--bad)}
.s12 .bands{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s12 .bd{background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:12px 14px;text-align:left;color:inherit;display:grid;gap:8px;transition:transform .15s}
.s12 .bd:hover,.s12 .bd:focus-visible{transform:translateY(-3px);border-color:var(--cyan)}
.s12 .bd .hd{display:flex;justify-content:space-between;gap:8px;align-items:flex-start}
.s12 .bd .nm{font-weight:700;font-size:13.5px;line-height:1.2} .s12 .bd .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s12 .bd .chip{font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:999px;white-space:nowrap;border:1.5px solid currentColor}
.s12 .rb{display:flex;height:12px;border-radius:6px;overflow:hidden;gap:2px}
.s12 .rb i{flex:1;background:#ECEEF2}
.s12 .rb i.y{background:var(--h)} .s12 .rb i.l{background:repeating-linear-gradient(45deg,var(--bad) 0 3px,#F7C8CB 3px 6px)}
.s12 .bd .meta{font-size:12px} .s12 .bd .meta b{font-family:var(--f-num);font-weight:400;font-size:18px}
.s12 .bd .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s12 .bd .nx{font-size:11.5px;color:var(--mute)}
.s12 .bd ul{list-style:none;margin:0;padding:0;font-size:12px;display:grid;gap:3px}
.s12 .bd li::before{content:"○ ";color:var(--mute)} .s12 .bd li.y::before{content:"● ";color:var(--cyan)} .s12 .bd li.l{color:var(--bad);font-weight:600} .s12 .bd li.l::before{content:"◆ "}
.s12 .vt{display:inline-flex;background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:3px}
.s12 .vt button{border:0;background:transparent;border-radius:999px;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:var(--ink)}
.s12 .vt button[aria-pressed="true"]{background:var(--ink);color:#fff}
.s12 .glow{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s12 .chart{background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:12px;overflow-x:auto}
.s12 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s12 .mlist{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.s12 .mlist button{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12px}
.s12 .mlist b{display:block;font-family:var(--f-num);font-weight:400;font-size:24px;line-height:1.1;color:var(--ink)}
.s12 .mlist .why{grid-column:1/-1;background:var(--ink);border-color:var(--ink);color:#C9CED8} .s12 .mlist .why b{color:#7DD3FC}
@media (max-width:1000px){ .s12 .head{grid-template-columns:1fr} .s12 .lenses{justify-content:flex-start} .s12 .refr{grid-template-columns:1fr 1fr} .s12 .sliders,.s12 .bands{grid-template-columns:1fr 1fr} .s12 .glow{grid-template-columns:1fr} }
@media (max-width:600px){ .s12 .swipe{display:block} .s12 h2{font-size:52px} .s12 .refr,.s12 .sliders,.s12 .bands{grid-template-columns:1fr} .s12 .ln{flex:1 1 160px} .s12 .vw{width:100%} }
`,
  render(){
    const HUE = ["#7C3AED","#2563EB","#0891B2","#059669","#65A30D","#D97706","#EA580C","#DC2626","#DB2777"];
    const LAMP = { live:"#22C58B", testing:"#F5B321", building:"#8A90A2", blocked:"#FF5A64", notstarted:"#4A5064" };
    const live = countParts("live"), O = D.opd;
    const ln = (h, f, lab, val, sub, attr) => `<button class="ln" type="button" ${attr} style="--h:${h};--f:${Math.round(Math.min(1,f)*100)}%"><i aria-hidden="true"></i><span><span>${lab}</span><b>${val}</b><em>${sub}</em></span></button>`;
    const lenses = ln("#059669", live/12, "PARTS LIVE", `${live} / 12`, "plan 4", `data-tab="links"`) + ln("#D97706", onCourse/9, "KPIs ON COURSE", `${onCourse} / 9`, "plan 8", `data-tab="measures"`)
      + ln("#0891B2", ebitdaTotal/spendTotal, "EBITDA BACK / OUT", `${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}`, "₹ lakh · plan 7.0 back", `data-ref="health:0"`) + ln("#DC2626", .6, "BREAK-EVEN", "DEC 2026", "plan Nov 2026", `data-ref="health:0"`);
    const P_ = id => D.parts.find(p=>p.id===id);
    const W = 1000, H = 660; let g = `<defs><linearGradient id="s12glass" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#E0F2FE" stop-opacity=".9"/><stop offset=".5" stop-color="#93C5FD" stop-opacity=".35"/><stop offset="1" stop-color="#C4B5FD" stop-opacity=".7"/></linearGradient><filter id="s12g"><feGaussianBlur stdDeviation="3"/></filter></defs>`;
    const card = (p, x, y, w, h, hue) => `<g class="st" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}">
      <rect class="cd" x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="#171A26" stroke="${hue||"#3A3F55"}" stroke-width="1.5" ${p.st==="building"||p.st==="notstarted"?'stroke-dasharray="5 3"':""}/>
      <circle cx="${x+18}" cy="${y+h/2}" r="7" fill="${LAMP[p.st]}" ${p.st==="live"?`style="filter:drop-shadow(0 0 4px ${LAMP.live})"`:""}/>
      <foreignObject x="${x+32}" y="${y+4}" width="${w-38}" height="${h-8}"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 10.5px/1.2 Poppins,sans-serif;color:#F1F3F8;height:${h-8}px;display:flex;flex-direction:column;justify-content:center"><span><b style="font-family:'Bebas Neue';font-weight:400;font-size:14px;color:${hue||"#7DD3FC"}">${p.id}</b> ${esc(p.name)}</span><span style="font-weight:400;font-size:9.5px;color:#9AA1B0">${PART_WORD[p.st]} · ${esc(p.when.replace(/^Live since /,"since ").replace(/^Goes live /,"live "))}</span></div></foreignObject></g>`;
    /* incoming: three stations on one white beam */
    const ix = 24, iw = 210, ih = 62;
    g += `<text x="${ix}" y="34" font-size="11" font-weight="700" letter-spacing="1.4" fill="#7DD3FC">PRESCRIPTIONS IN · OPD TODAY ${O.newPts + O.returning}</text>`;
    const pr = { a:[380,520], b:[560,520], c:[470,180] }; /* prism corners: bottom-left, bottom-right, apex */
    const entry = [ (pr.a[0]+pr.c[0])/2 - 4, (pr.a[1]+pr.c[1])/2 ];
    [1,2,3].forEach((id,i) => { const y = 120 + i*120; g += `<path d="M${ix+iw},${y+ih/2} C${ix+iw+60},${y+ih/2} ${entry[0]-80},${entry[1]} ${entry[0]},${entry[1]}" fill="none" stroke="#F1F3F8" stroke-opacity=".5" stroke-width="${i===1?5:3}"/>` + card(P_(id), ix, y, iw, ih); });
    g += `<line x1="${ix+iw}" y1="${entry[1]}" x2="${entry[0]}" y2="${entry[1]}" stroke="#FFFFFF" stroke-width="6" filter="url(#s12g)" opacity=".5"/>`;
    /* outgoing beams to the services */
    const outs = [6,7,8,9,10,11,12]; const ox = 700, ow = 276, oh = 58; const exitPt = i => [ (pr.b[0]+pr.c[0])/2 + 6 + i*1.2, pr.c[1] + 120 + i*28 ];
    outs.forEach((id,i) => { const p = P_(id), hue = HUE[i+1], y = 48 + i*84; const [ex,ey] = exitPt(i); const d = `M${ex},${ey} C${ex+70},${ey} ${ox-70},${y+oh/2} ${ox},${y+oh/2}`;
      if (p.st==="live") g += `<path d="${d}" fill="none" stroke="${hue}" stroke-width="7" opacity=".35" filter="url(#s12g)"/><path d="${d}" fill="none" stroke="${hue}" stroke-width="3"/><path d="${d}" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="6 24" class="beam"/>`;
      else if (p.st==="testing") g += `<path d="${d}" fill="none" stroke="${hue}" stroke-width="2.5" stroke-dasharray="10 6" class="beam slow"/>`;
      else if (p.st==="blocked") { g += `<path d="${d}" fill="none" stroke="${hue}" stroke-width="3" stroke-dasharray="80 900"/><g transform="translate(${(ex+ox)/2},${(ey+y+oh/2)/2})"><circle r="11" fill="#0E1018" stroke="#FF5A64" stroke-width="2"/><path d="M-4,-4 L4,4 M4,-4 L-4,4" stroke="#FF5A64" stroke-width="2.5"/></g>`; }
      else g += `<path d="${d}" fill="none" stroke="${hue}" stroke-opacity="${p.st==="building"?.6:.3}" stroke-width="1.5" stroke-dasharray="${p.st==="building"?"6 5":"2 6"}"/>`;
      g += card(p, ox, y, ow, oh, hue); });
    /* the prism: scheduling rules */
    g += `<polygon points="${pr.a.join(",")} ${pr.b.join(",")} ${pr.c.join(",")}" fill="url(#s12glass)" stroke="#E0F2FE" stroke-width="2"/><polygon points="${pr.c.join(",")} ${pr.b.join(",")} ${pr.b[0]+18},${pr.b[1]-12} ${pr.c[0]+18},${pr.c[1]-12}" fill="#93C5FD" opacity=".25"/>`;
    const r4 = P_(4), r5 = P_(5);
    g += `<g class="st" data-ref="part:4" data-part="4" tabindex="0" role="button" aria-label="Part 4: ${esc(r4.name)}, ${PART_WORD[r4.st]}"><rect class="cd" x="${pr.c[0]-80}" y="${pr.a[1]-150}" width="160" height="48" rx="10" fill="#171A26" stroke="#7DD3FC" stroke-width="1.5"/><circle cx="${pr.c[0]-62}" cy="${pr.a[1]-126}" r="6" fill="${LAMP[r4.st]}"/><text x="${pr.c[0]-50}" y="${pr.a[1]-130}" font-size="10.5" font-weight="700" fill="#F1F3F8">4 Scheduling engine</text><text x="${pr.c[0]-50}" y="${pr.a[1]-115}" font-size="9.5" fill="#9AA1B0">${PART_WORD[r4.st]} · live 20 Oct</text></g>
      <g class="st" data-ref="part:5" data-part="5" tabindex="0" role="button" aria-label="Part 5: ${esc(r5.name)}, ${PART_WORD[r5.st]}"><rect class="cd" x="${pr.c[0]-80}" y="${pr.a[1]-94}" width="160" height="48" rx="10" fill="#171A26" stroke="#7DD3FC" stroke-width="1.5"/><circle cx="${pr.c[0]-62}" cy="${pr.a[1]-70}" r="6" fill="${LAMP[r5.st]}"/><text x="${pr.c[0]-50}" y="${pr.a[1]-74}" font-size="10.5" font-weight="700" fill="#F1F3F8">5 Held emergency slots</text><text x="${pr.c[0]-50}" y="${pr.a[1]-59}" font-size="9.5" fill="#9AA1B0">${PART_WORD[r5.st]} · live 20 Oct</text></g>`;
    /* counters */
    const pct = Math.round(O.doneHere/O.prescribedToday*100);
    g += `<text x="${ix}" y="${H-86}" font-size="10" font-weight="700" letter-spacing="1.3" fill="#9AA1B0">PRESCRIBED TODAY</text><text x="${ix}" y="${H-56}" font-family="Bebas Neue, sans-serif" font-size="34" fill="#F1F3F8">₹${O.prescribedToday} LAKH</text>
      <text x="${ix+190}" y="${H-86}" font-size="10" font-weight="700" letter-spacing="1.3" fill="#9AA1B0">DONE HERE</text><text id="s12amt" x="${ix+190}" y="${H-56}" font-family="Bebas Neue, sans-serif" font-size="34" fill="#7DD3FC">₹${O.doneHere} L</text>
      <rect x="${ix}" y="${H-44}" width="330" height="10" rx="5" fill="#2A2F42"/><rect id="s12bar" data-full="330" x="${ix}" y="${H-44}" width="${(330*pct/100).toFixed(1)}" height="10" rx="5" fill="url(#s12spec)"/>
      <defs><linearGradient id="s12spec"><stop offset="0" stop-color="#7C3AED"/><stop offset=".5" stop-color="#0891B2"/><stop offset="1" stop-color="#059669"/></linearGradient></defs>
      <text id="s12pct" x="${ix+340}" y="${H-35}" font-size="10.5" fill="#F1F3F8">${pct}% done here</text><text id="s12last" x="${ix}" y="${H-14}" font-size="10.5" fill="#F5B321">last: ${esc(O.last)}</text>`;
    const bench = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Prescriptions come in on one beam, the scheduling rules split them into tests, and each beam runs to the room or service that delivers it.">${g}</svg>`;

    /* --- KPI sliders --- */
    const sl = (k,i) => { const n = Math.min(1,prog(k,k.now))*100, p = Math.min(1,prog(k,k.plan))*100; const col = k.state==="ahead"?"#0E8A62":k.state==="watch"?"#D99A0A":"#C92F38";
      return `<button class="sl" type="button" data-ref="kpi:${k.id}"><span class="top"><span>${esc(k.name)}</span><b class="${k.state}">${fmtv(k,k.now)}</b></span>
        <span class="trk" style="--h:${HUE[i%HUE.length]}88;--c:${col}" aria-hidden="true"><span class="gh" style="left:${p}%"></span><span class="kn" style="left:${n}%"></span><span class="tg"></span></span>
        <span class="lg"><span>From ${fmtv(k,k.base)}</span><span class="sw ${k.state}">${STATE_WORD[k.state].toUpperCase()} · ${gapText(k)}</span><span>Target ${fmtv(k,k.target)}</span></span></button>`; };

    /* --- people --- */
    const bd = (p,i) => { const cc = p.state==="ahead"?"#0E8A62":p.state==="watch"?"#A86B05":"#C92F38"; let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}">${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const b = []; for (let j=0;j<p.due;j++) b.push(`<i class="${j<p.done?"y":j<p.done+p.late?"l":""}"></i>`); body = `<span class="rb" style="--h:${HUE[i%HUE.length]}" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span><span class="meta"><b>${p.done}</b> of ${p.due} done${p.late?` · <b style="color:var(--bad)">${p.late}</b> late`:""}</span>`; }
      return `<button class="bd" type="button" data-ref="per:${p.key}"><span class="hd"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="chip" style="color:${cc}">${PERSON_WORD[p.state]}</span></span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</button>`; };

    /* --- money: glowing lines --- */
    const CW = 760, CH = 300, cx0 = 50, cx1 = 740, n = D.cumMonths.length, y0 = 24, y1 = 240, vmax = 70;
    const bx = i => cx0 + (cx1-cx0)*i/(n-1), by = v => y1 - (y1-y0)*v/vmax; const pts = (a,f,t) => a.slice(f,t+1).map((v,j)=>`${bx(f+j).toFixed(1)},${by(v).toFixed(1)}`).join(" ");
    let c = `<defs><linearGradient id="s12ar" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#0891B2" stop-opacity=".35"/><stop offset="1" stop-color="#0891B2" stop-opacity="0"/></linearGradient></defs>`;
    [0,20,40,60].forEach(v => c += `<line x1="${cx0}" x2="${cx1}" y1="${by(v)}" y2="${by(v)}" stroke="#ECEEF2"/><text x="${cx0-8}" y="${by(v)+4}" text-anchor="end" font-size="10" fill="#565B68">${v}</text>`);
    D.cumMonths.forEach((m,i) => c += `<text x="${bx(i)}" y="${y1+18}" text-anchor="middle" font-size="11" font-weight="600" fill="${i>D.actualTo?"#565B68":"#12141C"}">${m}</text><rect data-ref="month:${i}" data-nopen x="${bx(i)-34}" y="${y0}" width="68" height="${y1-y0}" fill="transparent" style="cursor:help"/>`);
    c += `<polygon points="${bx(0)},${y1} ${pts(D.cumFore,0,n-1)} ${bx(n-1)},${y1}" fill="url(#s12ar)"/><polyline points="${pts(D.cumPlan,0,n-1)}" fill="none" stroke="#7C3AED" stroke-width="1.5" stroke-dasharray="4 4"/>
      <polyline points="${pts(D.cumSpend,0,n-1)}" fill="none" stroke="#12141C" stroke-width="2.5"/><polyline points="${pts(D.cumFore,0,D.actualTo)}" fill="none" stroke="#0891B2" stroke-width="3.5"/><polyline points="${pts(D.cumFore,D.actualTo,n-1)}" fill="none" stroke="#0891B2" stroke-width="2.5" stroke-dasharray="3 4"/>`;
    const fi = D.breakeven.foreIdx; c += `<circle cx="${bx(fi)}" cy="${by(D.cumFore[fi])}" r="8" fill="none" stroke="#EA580C" stroke-width="2.5"/><text x="${bx(fi)+10}" y="${by(D.cumFore[fi])+20}" font-size="11" font-weight="700" fill="#EA580C">break-even, ${D.cumMonths[fi]}</text>
      <text x="${cx0}" y="${CH-12}" font-size="11" fill="#12141C">Black: money out to date · blue: EBITDA back to date (dotted: forecast) · violet dashed: plan · ₹ lakh</text>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="Money out and EBITDA back to date; EBITDA back passes money out in ${D.cumMonths[fi]}.">${c}</svg>`;
    const SH = ["#7C3AED","#2563EB","#0891B2","#059669","#65A30D","#D97706","#DC2626"];
    return `<div class="s12"><div class="wrap">
      <nav class="spec" aria-label="Suite sections"><div class="vw" aria-hidden="true"><small>YOU ARE ON</small><span id="s12at">OVERVIEW</span></div>
        ${TABS.map((t,i)=>`<button class="sg ${i?"":"on"}" type="button" data-tab="${t[0]}" style="--h:${SH[i]}">${t[1]}</button>`).join("")}</nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="lenses" aria-label="Pulse strip">${lenses}</div></div>
      <div class="refr" aria-label="Watch list and next go-live">${D.watch.map(w=>`<button class="rf" type="button" data-ref="${w.ref}"><i aria-hidden="true"></i><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}
        <button class="focus" type="button" data-ref="part:${D.milestone.part}"><b>${D.milestone.days}</b><span>DAYS TO THE NEXT GO-LIVE<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to follow every beam →</p><div class="bench">${bench}</div>
        <div class="legend"><span><i style="border-color:#0891B2"></i>Live</span><span><i style="border-color:#D97706;border-top-style:dashed"></i>Testing</span><span><i style="border-color:#8A90A2;border-top-style:dashed"></i>Being built</span><span><i style="border-color:#C92F38"></i>Late, beam stops</span><span><i style="border-color:#C9CED8;border-top-style:dotted"></i>Not started</span><span>· the dot on each card is its status · Data as of ${esc(D.asOf)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3><p>The solid knob is today · the dashed ring is the plan for this week · the bar at the end is the target</p></div><div class="sliders">${D.kpis.map(sl).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="bands">${D.people.map(bd).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="glow"><div class="chart">${chart}</div>
          <div class="mlist">
            <button type="button" data-ref="month:1">Subscription<b>${L(D.spend[0].v[1])}/mo</b></button>
            <button type="button" data-ref="month:1">Scheduling Manager and guest services we recommended<b>${L(D.spend[1].v[1])}/mo</b></button>
            <button type="button" data-ref="month:1">One-time so far<b>${L(sum(D.spend[2].v))}</b></button>
            <button type="button" data-ref="health:0">Extra revenue so far<b>${L(revTotal)}</b></button>
            <button type="button" data-ref="health:0">EBITDA now<b>${L(D.ebitda[1])}/mo</b></button>
            <button type="button" data-ref="health:0">EBITDA at full run<b>${L(D.runRate.ebitda)}/mo</b></button>
            <button type="button" class="why" data-ref="health:0">Break-even ${D.breakeven.fore}, ${D.breakeven.late} late<b>See why and the recovery plan ›</b></button>
          </div></div></section>
    </div></div>`;
  },
  after(){
    document.querySelectorAll(".s12 .sg").forEach(b => b.addEventListener("click", () => { const at = document.getElementById("s12at"); if (at) at.textContent = b.textContent.trim().toUpperCase(); }));
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    testTicker("s12", ".s12 .st");
  }
});
