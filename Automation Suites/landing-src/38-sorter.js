/* ===== Billing & Insurance, option 3: the sorting floor (olive and marigold) ===== */
SCHEMES.push({
  key:"sorter", letter:"3", name:"Olive and marigold",
  note:"<b>Option 3 · olive and marigold.</b> Events drop from the top into the billing engine, which sorts each charge onto the right bill and sends it down to the family or the insurer.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#23280F","--sh-mute":"#5F6449","--sh-line":"#DEDCC8","--sh-card":"#FAF9F2","--c-ok":"#2F7D32","--c-warn":"#A86B00","--c-bad":"#B93A12","--pk-bg":"#23280F","--pk-fg":"#FFF8E1","--pk-line":"#F2A900","--pk-r":"6px","--sh-r":"12px" },
  fab:18,
  blocks:{ nav:".rail", pulse:".crates", watch:".strip", countdown:".label", hero:".floor", kpis:".dials", team:".labels", money:".money" },
  css:`
.s8{--bg:#F2F1E6;--ink:#23280F;--mute:#5F6449;--olive:#5C6B1E;--olive2:#3B4512;--mari:#F2A900;--mari2:#FFD466;--ok:#2F7D32;--warn:#A86B00;--bad:#B93A12;--line:#DEDCC8;
  background:var(--bg);color:var(--ink);padding:0 16px 90px;overflow-x:clip}
.s8 .wrap{max-width:1240px;margin:0 auto}
.s8 .rail{position:relative;display:flex;flex-wrap:wrap;align-items:flex-start;gap:6px 14px;padding:20px 0 6px}
.s8 .rail::before{content:"";position:absolute;left:0;right:0;top:12px;height:3px;background:var(--olive2);border-radius:2px}
.s8 .now{position:relative;background:var(--olive2);color:var(--mari2);padding:6px 14px;font-family:var(--f-num);font-size:24px;letter-spacing:.08em;line-height:1;border-radius:3px;margin-top:6px}
.s8 .now small{display:block;font-family:var(--f-body);font-size:9.5px;letter-spacing:.16em;color:#CFD3B0;font-weight:600}
.s8 .tg{position:relative;background:transparent;border:0;padding:16px 0 0;color:var(--ink);min-height:52px}
.s8 .tg::before{content:"";position:absolute;left:50%;top:-8px;height:24px;border-left:1.5px solid var(--olive2)}
.s8 .tg span{display:block;position:relative;background:#FFF8E1;border:1.5px solid #D7CFA5;padding:7px 14px 7px 22px;font-size:12.5px;font-weight:600;clip-path:polygon(10px 0,100% 0,100% 100%,10px 100%,0 50%);transform-origin:50% 0;transition:transform .2s}
.s8 .tg span::before{content:"";position:absolute;left:10px;top:50%;width:6px;height:6px;margin-top:-3px;border-radius:50%;background:var(--bg);border:1px solid #B9AF7E}
.s8 .tg:hover span{transform:rotate(-4deg)}
.s8 .tg.on span{background:var(--mari);border-color:#C78B00}
.s8 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:18px 0 14px}
.s8 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--olive)}
.s8 h2{font-family:var(--f-num);font-weight:400;font-size:72px;line-height:.9;margin:4px 0 0;letter-spacing:.01em;color:var(--olive2)}
.s8 .crates{display:flex;flex-wrap:wrap;gap:12px;justify-content:flex-end}
.s8 .crate{position:relative;background:#D9B97A;border:0;color:#2A1F05;padding:10px 14px 8px;min-width:132px;text-align:left;box-shadow:inset 0 0 0 3px #B8944F,6px 6px 0 rgba(59,69,18,.25);
  background-image:repeating-linear-gradient(0deg,transparent 0 13px,rgba(120,86,30,.25) 13px 14px)}
.s8 .crate::before,.s8 .crate::after{content:"";position:absolute;left:0;right:0;height:3px;background:#8A6A2E}
.s8 .crate::before{top:0} .s8 .crate::after{bottom:0}
.s8 .crate span{display:block;font-size:10px;letter-spacing:.12em;font-weight:700}
.s8 .crate b{display:block;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1;letter-spacing:.06em}
.s8 .crate em{font-style:normal;font-size:10.5px;font-weight:600}
.s8 .strip{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.9fr);gap:12px;margin-bottom:14px}
.s8 .held{position:relative;background:#fff;border:1.5px solid var(--line);border-radius:8px;padding:10px 70px 10px 12px;text-align:left;color:var(--ink);font-size:12.5px;font-weight:600;overflow:hidden}
.s8 .held small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s8 .held::after{content:"HELD";position:absolute;right:8px;top:50%;transform:translateY(-50%) rotate(-14deg);font-family:var(--f-num);font-size:22px;letter-spacing:.08em;color:var(--bad);border:2.5px solid var(--bad);padding:1px 7px;border-radius:4px;opacity:.85}
.s8 .label{display:grid;grid-template-columns:auto minmax(0,1fr);gap:0;background:#fff;border:2px solid var(--ink);border-radius:4px;text-align:left;color:var(--ink);padding:0;overflow:hidden}
.s8 .label b{background:var(--ink);color:var(--mari2);font-family:var(--f-num);font-weight:400;font-size:40px;line-height:1;padding:8px 12px;display:grid;place-items:center}
.s8 .label span{padding:8px 12px;font-size:12px;font-weight:700;letter-spacing:.04em}
.s8 .label small{display:block;font-weight:400;letter-spacing:0;font-size:11.5px;color:var(--mute)}
.s8 .floor{border-radius:16px;background:#FBFAF3;border:1.5px solid var(--line);overflow-x:auto;
  background-image:linear-gradient(90deg,rgba(92,107,30,.06) 1px,transparent 1px);background-size:56px 100%}
.s8 .floor svg{display:block;width:100%;min-width:900px;height:auto}
.s8 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--olive)}
.s8 .hp{cursor:pointer}
.s8 .hp:focus{outline:none} .s8 .hp:focus .bd{stroke:#F2B705;stroke-width:3}
.s8 .hp:hover .bd{stroke:var(--mari)}
.s8 .hp.ping .bd{animation:s8ping .9s ease}
@keyframes s8ping{0%{fill:#FFF0BF}100%{fill:#FFFFFF}}
.s8 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:8px}
.s8 .legend i{display:inline-block;width:12px;height:12px;vertical-align:-1px;margin-right:6px;border-radius:2px}
.s8 .zone{margin-top:40px;scroll-margin-top:20px;border-radius:16px}
.s8 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:14px;border-top:3px solid var(--olive2);padding-top:10px}
.s8 .zh h3{font-family:var(--f-num);font-weight:400;font-size:38px;margin:0;line-height:1;color:var(--olive2)}
.s8 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s8 .dials{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.s8 .dl{display:grid;grid-template-columns:120px minmax(0,1fr);gap:12px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:10px 12px;text-align:left;color:inherit;transition:transform .15s}
.s8 .dl:hover,.s8 .dl:focus-visible{transform:translateY(-2px);border-color:var(--olive)}
.s8 .dl svg{width:120px;height:104px}
.s8 .dl .nm{font-size:13px;font-weight:600;line-height:1.3}
.s8 .dl b{display:block;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1;margin-top:4px}
.s8 .dl .st{display:block;font-size:11px;font-weight:700;letter-spacing:.05em;margin-top:4px}
.s8 .dl .rg{display:block;font-size:11px;color:var(--mute);margin-top:2px}
.s8 .ahead{color:var(--ok)} .s8 .watch{color:var(--warn)} .s8 .off{color:var(--bad)}
.s8 .labels{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s8 .pl{background:#fff;border:2px solid var(--ink);border-radius:6px;padding:0;text-align:left;color:inherit;overflow:hidden;display:flex;flex-direction:column;transition:transform .15s}
.s8 .pl:hover,.s8 .pl:focus-visible{transform:translateY(-3px);box-shadow:5px 5px 0 rgba(35,40,15,.18)}
.s8 .pl .top{display:flex;justify-content:space-between;align-items:center;gap:8px;background:var(--olive2);color:#FFF8E1;padding:7px 10px}
.s8 .pl .top b{font-size:13px} .s8 .pl .top em{font-style:normal;font-size:10px;font-weight:700;letter-spacing:.06em;padding:2px 7px;border-radius:3px}
.s8 .pl .bd2{padding:10px;display:grid;gap:7px}
.s8 .pl .role{font-size:11.5px;color:var(--mute)}
.s8 .bars{display:flex;align-items:flex-end;gap:2px;height:30px}
.s8 .bars i{width:5px;height:100%;background:var(--ink)}
.s8 .bars i.l{background:var(--bad);width:7px} .s8 .bars i.p{width:2px;background:#C9C6AE}
.s8 .pl .meta{font-size:12px} .s8 .pl .meta b{font-family:var(--f-num);font-weight:400;font-size:18px}
.s8 .pl .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s8 .pl .nx{font-size:11.5px;color:var(--mute)}
.s8 .pl ul{list-style:none;margin:0;padding:0;font-size:12px;display:grid;gap:3px}
.s8 .pl li::before{content:"□ "} .s8 .pl li.y::before{content:"■ ";color:var(--olive)} .s8 .pl li.l{color:var(--bad);font-weight:600} .s8 .pl li.l::before{content:"▣ "}
.s8 .vt{display:inline-flex;border:2px solid var(--ink);border-radius:4px;overflow:hidden}
.s8 .vt button{border:0;background:#fff;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:var(--ink)}
.s8 .vt button[aria-pressed="true"]{background:var(--mari)}
.s8 .money{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s8 .chart{background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:12px;overflow-x:auto}
.s8 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s8 .mlist{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.s8 .mlist button{background:#fff;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12px}
.s8 .mlist b{display:block;font-family:var(--f-num);font-weight:400;font-size:24px;line-height:1.1;color:var(--ink)}
.s8 .mlist .why{grid-column:1/-1;background:var(--olive2);border-color:var(--olive2);color:#E9ECCF} .s8 .mlist .why b{color:var(--mari2)}
@media (max-width:1000px){ .s8 .head{grid-template-columns:1fr} .s8 .crates{justify-content:flex-start} .s8 .strip{grid-template-columns:1fr 1fr} .s8 .dials{grid-template-columns:1fr 1fr} .s8 .labels{grid-template-columns:1fr 1fr} .s8 .money{grid-template-columns:1fr} }
@media (max-width:600px){ .s8 .swipe{display:block} .s8 h2{font-size:52px} .s8 .strip,.s8 .dials,.s8 .labels{grid-template-columns:1fr} .s8 .crate{flex:1 1 140px} .s8 .tg span{padding:6px 10px 6px 20px;font-size:12px} }
`,
  render(){
    const C = { live:"#2F7D32", testing:"#D49400", building:"#A9A88F", blocked:"#B93A12", notstarted:"#D6D4C2" };
    const live = countParts("live");
    const crates = `
      <button class="crate" type="button" data-tab="links"><span>CHARGE LINES LIVE</span><b>${live} / 12</b><em>plan 4</em></button>
      <button class="crate" type="button" data-tab="measures"><span>KPIs ON COURSE</span><b>${onCourse} / 9</b><em>plan 8</em></button>
      <button class="crate" type="button" data-ref="health:0"><span>EBITDA BACK / OUT</span><b>${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}</b><em>₹ lakh · plan 3.4 back</em></button>
      <button class="crate" type="button" data-ref="health:0"><span>BREAK-EVEN</span><b>MAR 2027</b><em>plan Jan 2027</em></button>`;

    /* --- the sorting floor: top to bottom --- */
    const W = 1000, H = 680; let belts = "", parcels = "", boards = "", defs = "";
    const sx = 330, sw = 340, sy = 330, sh = 120; /* engine */
    const top = D.parts.filter(p=>p.side!=="out"), outs = D.parts.filter(p=>p.side==="out");
    const bw = 112, gap = (W - 30 - top.length*bw)/(top.length-1);
    const belt = (id, d, st) => { defs += `<path id="bp${id}" d="${d}"/>`;
      if (st==="building"||st==="notstarted") return `<path d="${d}" fill="none" stroke="${st==="building"?"#A9A88F":"#D6D4C2"}" stroke-width="12" stroke-dasharray="${st==="building"?"8 6":"2 8"}"/>`;
      const edge = st==="blocked" ? "#B93A12" : "#23280F";
      return `<path d="${d}" fill="none" stroke="${edge}" stroke-width="16" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#4A4F38" stroke-width="11" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#8B8F72" stroke-width="1.5" stroke-dasharray="3 7"/>`; };
    const parcel = (id, st, i) => { const box = `<rect x="-7" y="-7" width="14" height="14" rx="2" fill="#F2A900" stroke="#8A6200"/><line x1="-7" x2="7" y1="0" y2="0" stroke="#C78B00" stroke-width="2"/>`;
      if (st==="live") return [0,1].map(k=>`<g>${box}<animateMotion dur="3s" begin="${(k*1.5+i*.25).toFixed(2)}s" repeatCount="indefinite"><mpath href="#bp${id}"/></animateMotion></g>`).join("");
      if (st==="testing") return `<g>${box}<animateMotion dur="7.5s" begin="${i*.5}s" repeatCount="indefinite"><mpath href="#bp${id}"/></animateMotion></g>`;
      if (st==="blocked") return `<g>${box.replace(/#F2A900/,"#F7B9A3")}<animateMotion dur="1s" fill="freeze" keyPoints=".45;.45" keyTimes="0;1" calcMode="linear"><mpath href="#bp${id}"/></animateMotion></g>`;
      return ""; };
    const board = (p, x, y, w, h) => `<g class="hp" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}">
      <rect class="bd" x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#FFFFFF" stroke="#23280F" stroke-width="1.8"/>
      <rect x="${x}" y="${y}" width="${w}" height="7" rx="3" fill="${C[p.st]}"/>
      <text x="${x+10}" y="${y+30}" font-family="Bebas Neue, sans-serif" font-size="22" fill="${p.st==="notstarted"||p.st==="building"?"#8B8F72":C[p.st]}">${String(p.id).padStart(2,"0")}</text>
      <foreignObject x="${x+34}" y="${y+10}" width="${w-38}" height="${h-12}"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 10.5px/1.25 Poppins,sans-serif;color:#23280F">${esc(p.name)}<div style="font-weight:400;font-size:9.5px;color:${p.st==="notstarted"||p.st==="building"?"#5F6449":C[p.st]}">${PART_WORD[p.st]} · ${esc(p.when.replace(/^Live since /,"since ").replace(/^Goes live /,"live "))}</div></div></foreignObject></g>`;
    top.forEach((p,i) => { const x = 15 + i*(bw+gap), y = 34, h = 100; const cx = x + bw/2; const tx = sx + 30 + i*(sw-60)/(top.length-1);
      const d = `M${cx},${y+h+4} L${cx},${y+h+40} L${tx},${sy-26} L${tx},${sy-4}`;
      belts += belt(p.id, d, p.st) + `<path d="M${cx-18},${y+h+4} L${cx+18},${y+h+4} L${cx+8},${y+h+18} L${cx-8},${y+h+18} Z" fill="#5C6B1E"/>`;
      parcels += parcel(p.id, p.st, i);
      if (p.st==="blocked") { const mx = (cx+tx)/2, my = (y+h+40+sy-26)/2; parcels += `<g transform="translate(${mx+16},${my})"><circle r="10" fill="#fff" stroke="#B93A12" stroke-width="2"/><text y="4" text-anchor="middle" font-size="12" font-weight="700" fill="#B93A12">!</text></g>`; }
      boards += board(p, x, y, bw, h); });
    const ow = 190, og = (W - 30 - outs.length*ow)/(outs.length-1);
    outs.forEach((p,i) => { const x = 15 + i*(ow+og), y = 580, h = 70; const cx = x + ow/2; const fx = sx + 40 + i*(sw-80)/(outs.length-1);
      const d = `M${fx},${sy+sh+4} L${fx},${sy+sh+24} L${cx},${y-34} L${cx},${y-6}`;
      belts += belt(p.id, d, p.st); parcels += parcel(p.id, p.st, i+8);
      boards += `<path d="M${x+10},${y-4} L${x+ow-10},${y-4} L${x+ow-24},${y+h} L${x+24},${y+h} Z" fill="#E7E3CB"/>` + board(p, x, y, ow, h); });
    const engine = `<g aria-label="The billing engine">
      <polygon points="${sx},${sy} ${sx+18},${sy-18} ${sx+sw+18},${sy-18} ${sx+sw},${sy}" fill="#7A8A2E"/>
      <polygon points="${sx+sw},${sy} ${sx+sw+18},${sy-18} ${sx+sw+18},${sy+sh-18} ${sx+sw},${sy+sh}" fill="#2C3410"/>
      <rect x="${sx}" y="${sy}" width="${sw}" height="${sh}" rx="4" fill="#3B4512"/>
      ${Array.from({length:12},(_,i)=>`<line x1="${sx+12+i*28}" x2="${sx+26+i*28}" y1="${sy+sh-10}" y2="${sy+sh-10}" stroke="#F2A900" stroke-width="4"/>`).join("")}
      <text x="${sx+18}" y="${sy+30}" font-family="Bebas Neue, sans-serif" font-size="24" fill="#FFD466" letter-spacing="1.5">BILLING ENGINE</text>
      <text x="${sx+18}" y="${sy+48}" font-size="10" fill="#CFD3B0">prices each charge and sorts it onto the right bill</text>
      <rect x="${sx+18}" y="${sy+58}" width="${sw-36}" height="40" rx="4" fill="#1A1F08"/>
      <text x="${sx+30}" y="${sy+76}" font-size="9" fill="#CFD3B0" letter-spacing="1.2">POSTED TODAY</text>
      <text id="s8amt" x="${sx+30}" y="${sy+93}" font-family="Bebas Neue, sans-serif" font-size="20" fill="#FFD466">₹18,42,300</text>
      <text id="s8cnt" x="${sx+170}" y="${sy+76}" font-size="9.5" fill="#CFD3B0">1,284 charges</text>
      <text id="s8last" x="${sx+170}" y="${sy+92}" font-size="10" fill="#FFD466">Lab · CBC · ₹450 · Bed 214</text></g>`;
    const heads = `<text x="15" y="22" font-size="11" font-weight="700" letter-spacing="1.5" fill="#5C6B1E">EVENTS IN THE STAY, AND THE CHARGE LIST</text><text x="15" y="${H-6}" font-size="11" font-weight="700" letter-spacing="1.5" fill="#5C6B1E">BILLS GOING OUT</text>
      <text x="${W-15}" y="${H-6}" text-anchor="end" font-size="10.5" fill="#5F6449">The signed summary for claims comes from the Discharge Summary suite</text>`;
    const floor = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Seven kinds of event and the charge list drop into the billing engine, which sends bills down to the family and the insurers."><defs>${defs}</defs>${heads}${belts}${engine}${parcels}${boards}</svg>`;

    /* --- KPI dials --- */
    const dl = k => { const n = Math.min(1,prog(k,k.now)), p = Math.min(1,prog(k,k.plan)); const col = k.state==="ahead"?"#2F7D32":k.state==="watch"?"#D49400":"#B93A12";
      const a0 = Math.PI*0.75, sweep = Math.PI*1.5, cx = 60, cy = 58, r = 44; const at = (f,rr=r) => [cx + rr*Math.cos(a0+f*sweep), cy + rr*Math.sin(a0+f*sweep)];
      const arc = (f1,f2,rr) => { const [x1,y1] = at(f1,rr), [x2,y2] = at(f2,rr); return `M${x1.toFixed(1)},${y1.toFixed(1)} A${rr},${rr} 0 ${(f2-f1)*sweep>Math.PI?1:0} 1 ${x2.toFixed(1)},${y2.toFixed(1)}`; };
      const [nx,ny] = at(n, r-12), [p1x,p1y] = at(p, r+5), [p2x,p2y] = at(p, r-8);
      const ticks = Array.from({length:11},(_,i)=>{ const [a,b]=at(i/10,r-2),[c,d]=at(i/10,r-(i%5?6:10)); return `<line x1="${a.toFixed(1)}" y1="${b.toFixed(1)}" x2="${c.toFixed(1)}" y2="${d.toFixed(1)}" stroke="#5F6449" stroke-width="${i%5?1:2}"/>`; }).join("");
      return `<button class="dl" type="button" data-ref="kpi:${k.id}"><svg viewBox="0 0 120 104" aria-hidden="true"><circle cx="${cx}" cy="${cy}" r="${r+8}" fill="#F7F4E2" stroke="#23280F" stroke-width="2"/><path d="${arc(0,1,r)}" fill="none" stroke="#E5E1C8" stroke-width="7"/><path d="${arc(0,Math.max(.01,n),r)}" fill="none" stroke="${col}" stroke-width="7"/>${ticks}
        <line x1="${p1x.toFixed(1)}" y1="${p1y.toFixed(1)}" x2="${p2x.toFixed(1)}" y2="${p2y.toFixed(1)}" stroke="#23280F" stroke-width="2" stroke-dasharray="2 2"/><line x1="${cx}" y1="${cy}" x2="${nx.toFixed(1)}" y2="${ny.toFixed(1)}" stroke="#23280F" stroke-width="3" stroke-linecap="round"/><circle cx="${cx}" cy="${cy}" r="5" fill="#F2A900" stroke="#23280F"/>
        <text x="${cx}" y="${cy+30}" text-anchor="middle" font-size="9" fill="#5F6449">target ${fmtv(k,k.target)}</text></svg>
        <span><span class="nm">${esc(k.name)}</span><b class="${k.state}">${fmtv(k,k.now)}</b><span class="st ${k.state}">${STATE_WORD[k.state].toUpperCase()} · ${gapText(k)}</span><span class="rg">From ${fmtv(k,k.base)} · plan now ${fmtv(k,k.plan)}</span></span></button>`; };

    /* --- people --- */
    const pl = p => { const tgc = p.state==="ahead"?"#2F7D32":p.state==="watch"?"#A86B00":"#B93A12"; let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}">${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const b = []; for (let i=0;i<p.due;i++) b.push(`<i class="${i<p.done?"":i<p.done+p.late?"l":"p"}"></i>`); body = `<span class="bars" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span><span class="meta"><b>${p.done}</b> of ${p.due} done${p.late?` · <b style="color:var(--bad)">${p.late}</b> late`:""}</span>`; }
      return `<button class="pl" type="button" data-ref="per:${p.key}"><span class="top"><b>${esc(p.name)}</b><em style="background:${tgc}">${PERSON_WORD[p.state].toUpperCase()}</em></span><span class="bd2"><span class="role">${esc(p.role)}</span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</span></button>`; };

    /* --- money: area chart --- */
    const CW = 760, CH = 290, x0 = 46, x1 = 740, y0 = 24, y1 = 240, vmax = 45, n = D.cumMonths.length;
    const bx = i => x0 + (x1-x0)*i/(n-1), by = v => y1 - (y1-y0)*v/vmax;
    const line = (a,f,t) => a.slice(f,t+1).map((v,j)=>`${j?"L":"M"}${bx(f+j).toFixed(1)},${by(v).toFixed(1)}`).join(" ");
    let g = ""; [0,10,20,30,40].forEach(v => g += `<line x1="${x0}" x2="${x1}" y1="${by(v)}" y2="${by(v)}" stroke="#EFEDDD"/><text x="${x0-8}" y="${by(v)+4}" text-anchor="end" font-size="10" fill="#5F6449">${v}</text>`);
    D.cumMonths.forEach((m,i) => g += `<text x="${bx(i)}" y="${y1+18}" text-anchor="middle" font-size="11" font-weight="600" fill="${i>D.actualTo?"#5F6449":"#23280F"}">${m}</text><rect data-ref="month:${i}" data-nopen x="${bx(i)-34}" y="${y0}" width="68" height="${y1-y0}" fill="transparent" style="cursor:help"/>`);
    const area = line(D.cumFore,0,n-1) + ` L${bx(n-1)},${y1} L${bx(0)},${y1} Z`;
    g += `<path d="${area}" fill="#F2A900" fill-opacity=".25"/><path d="${line(D.cumFore,0,D.actualTo)}" fill="none" stroke="#C78B00" stroke-width="3"/><path d="${line(D.cumFore,D.actualTo,n-1)}" fill="none" stroke="#C78B00" stroke-width="2.5" stroke-dasharray="4 4"/>
      <path d="${line(D.cumPlan,0,n-1)}" fill="none" stroke="#5F6449" stroke-width="1.5" stroke-dasharray="2 4"/><path d="${line(D.cumSpend,0,n-1)}" fill="none" stroke="#3B4512" stroke-width="3"/>
      <line x1="${bx(4)}" x2="${bx(4)}" y1="${y0}" y2="${y1}" stroke="#5F6449" stroke-dasharray="3 3"/><text x="${bx(4)}" y="${y0-8}" text-anchor="middle" font-size="10.5" fill="#5F6449">plan break-even</text>
      <g transform="translate(${bx(6)},${by(D.cumFore[6])})"><line x1="0" y1="0" x2="0" y2="-46" stroke="#B93A12" stroke-width="2"/><path d="M0,-46 L24,-39 L0,-32 Z" fill="#B93A12"/><text x="28" y="-36" font-size="11" font-weight="700" fill="#B93A12">Mar</text></g>
      <rect x="${x0}" y="${CH-20}" width="14" height="4" fill="#3B4512"/><text x="${x0+20}" y="${CH-14}" font-size="11" fill="#23280F">Money out to date</text><rect x="${x0+150}" y="${CH-24}" width="14" height="12" fill="#F2A900" fill-opacity=".5" stroke="#C78B00"/><text x="${x0+170}" y="${CH-14}" font-size="11" fill="#23280F">EBITDA back to date (dashed: forecast)</text><text x="${x0+430}" y="${CH-14}" font-size="11" fill="#5F6449">dotted: plan · ₹ lakh</text>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="Money out and EBITDA back to date. EBITDA back passes money out in March; the plan said January.">${g}</svg>`;

    return `<div class="s8"><div class="wrap">
      <nav class="rail" aria-label="Suite sections"><div class="now" aria-hidden="true"><small>YOU ARE ON</small><span id="s8at">OVERVIEW</span></div>
        ${TABS.map((t,i)=>`<button class="tg ${i?"":"on"}" type="button" data-tab="${t[0]}"><span>${t[1]}</span></button>`).join("")}</nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="crates" aria-label="Pulse strip">${crates}</div></div>
      <div class="strip" aria-label="Watch list and next go-live">${D.watch.map(w=>`<button class="held" type="button" data-ref="${w.ref}">${esc(w.t)}<small>${esc(P[w.who].name)}</small></button>`).join("")}
        <button class="label" type="button" data-ref="part:${D.milestone.part}"><b>${D.milestone.days}</b><span>DAYS TO THE NEXT GO-LIVE<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0;border:0;padding:0"><p class="swipe">Swipe sideways to see every line →</p><div class="floor">${floor}</div>
        <div class="legend"><span><i style="background:#2F7D32"></i>Live</span><span><i style="background:#D49400"></i>Testing</span><span><i style="background:repeating-linear-gradient(90deg,#A9A88F 0 3px,transparent 3px 5px)"></i>Being built</span><span><i style="background:#B93A12"></i>Late</span><span><i style="background:#D6D4C2"></i>Not started</span><span>· Data as of ${esc(D.asOf)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3><p>Needle is today · dashed tick is the plan for this week · the end of the scale is the target</p></div>
        <div class="dials">${D.kpis.map(dl).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="labels">${D.people.map(pl).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="money"><div class="chart">${chart}</div>
          <div class="mlist">
            <button type="button" data-ref="month:1">Subscription<b>${L(2.0)}/mo</b></button>
            <button type="button" data-ref="month:1">Night insurance coordinator we recommended<b>${L(0.25)}/mo</b></button>
            <button type="button" data-ref="month:1">One-time so far<b>${L(3.0)}</b></button>
            <button type="button" data-ref="health:0">Extra revenue so far<b>${L(revTotal)}</b></button>
            <button type="button" data-ref="health:0">EBITDA now<b>${L(D.ebitda[1])}/mo</b></button>
            <button type="button" data-ref="health:0">EBITDA at full run<b>${L(D.runRate.ebitda)}/mo</b></button>
            <button type="button" class="why" data-ref="health:0">Break-even ${D.breakeven.fore}, ${D.breakeven.late} late<b>See why and the recovery plan ›</b></button>
          </div></div></section>
    </div></div>`;
  },
  after(){
    document.querySelectorAll(".s8 .tg").forEach(b => b.addEventListener("click", () => { const at = document.getElementById("s8at"); if (at) at.textContent = b.textContent.trim().toUpperCase(); }));
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { document.querySelectorAll(".s8 animateMotion").forEach(a => a.remove()); return; }
    tickEngine("s8", ".s8 .hp");
  }
});
