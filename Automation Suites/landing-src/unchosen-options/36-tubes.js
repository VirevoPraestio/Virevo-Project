/* ===== Billing & Insurance: the pneumatic tube room ===== */
SCHEMES.push({
  key:"tubes", letter:"1", name:"Cobalt and tangerine",
  note:"<b>Option 1 · cobalt and tangerine.</b> Same tube layout as before, redrawn on white with cobalt lines and orange capsules.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#15233F","--sh-mute":"#5A6782","--sh-line":"#D8DFEE","--sh-card":"#F5F7FC","--c-ok":"#0E8A5B","--c-warn":"#B06F00","--c-bad":"#D93A40","--pk-bg":"#15233F","--pk-fg":"#FFFFFF","--pk-line":"#3B5BE6","--pk-r":"10px","--sh-r":"16px" },
  fab:18,
  css:`
.s6{--bg:#F3F5F9;--ink:#15233F;--mute:#5A6782;--acc:#2D4EDB;--acc2:#1F3AAE;--tang:#FF7A1A;--mint:#0E8A5B;--amber:#B06F00;--coral:#D93A40;--line:#D8DFEE;
  background:var(--bg);color:var(--ink);padding:18px 16px 90px;overflow-x:clip;background-image:radial-gradient(#DCE2EE 1px,transparent 1.2px);background-size:22px 22px}
.s6 .wrap{max-width:1240px;margin:0 auto}
.s6 .disp-panel{display:flex;flex-wrap:wrap;align-items:center;gap:12px 16px;background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:10px 14px;box-shadow:0 10px 24px rgba(21,35,63,.08)}
.s6 .nix{display:flex;align-items:center;gap:10px;padding:6px 14px;border-radius:10px;background:var(--ink);min-width:200px}
.s6 .nix small{font-size:9.5px;letter-spacing:.16em;color:#A9BAFF;font-weight:600}
.s6 .nix b{font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1;color:#FFB067;letter-spacing:.06em}
.s6 .caps{display:flex;flex-wrap:wrap;gap:8px}
.s6 .capb{display:flex;align-items:center;background:transparent;border:0;padding:0;min-height:46px;color:var(--ink)}
.s6 .capb i{width:12px;height:32px;background:var(--acc);border-radius:16px 3px 3px 16px}
.s6 .capb span{height:32px;display:flex;align-items:center;padding:0 12px;font-size:12.5px;font-weight:600;background:#EEF2FB;border-top:1.5px solid #C9D3EA;border-bottom:1.5px solid #C9D3EA}
.s6 .capb em{width:12px;height:32px;background:var(--acc);border-radius:3px 16px 16px 3px}
.s6 .capb:hover span{background:#DFE6FA}
.s6 .capb.on i,.s6 .capb.on em{background:var(--tang)} .s6 .capb.on span{background:#FFE8D6;border-color:#FFB98A;color:#7A2E00}
.s6 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:22px 0 14px}
.s6 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--acc)}
.s6 h2{font-family:var(--f-num);font-weight:400;font-size:72px;line-height:.9;margin:4px 0 0;letter-spacing:.01em}
.s6 .gauges{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}
.s6 .gg{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:8px 4px;color:inherit;display:flex;flex-direction:column;align-items:center;gap:2px;width:124px}
.s6 .gg svg{width:112px;height:76px}
.s6 .gg b{font-family:var(--f-num);font-weight:400;font-size:22px;line-height:1;letter-spacing:.03em}
.s6 .gg span{font-size:10.5px;letter-spacing:.1em;color:var(--mute);font-weight:600;text-align:center}
.s6 .gg em{font-style:normal;font-size:10.5px;color:var(--acc)}
.s6 .strip{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,1.1fr);gap:10px;margin-bottom:12px}
.s6 .jam{display:grid;grid-template-columns:34px minmax(0,1fr);gap:10px;align-items:center;background:#FFF3F3;border:1.5px solid #F2B8BA;border-radius:12px;padding:8px 10px;color:var(--ink);text-align:left;font-size:12.5px;font-weight:600}
.s6 .jam small{display:block;font-weight:400;color:#8C3A3E;font-size:11.5px}
.s6 .jam i{width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#FFD0D0,#E5484D 55%,#9A1C22);box-shadow:0 0 10px rgba(229,72,77,.5);animation:s6beacon 1.6s ease-in-out infinite}
@keyframes s6beacon{50%{box-shadow:0 0 2px rgba(229,72,77,.2);filter:brightness(.8)}}
.s6 .plate{display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,#FFB067,#FF7A1A);color:#fff;border-radius:12px;padding:8px 14px;border:0;text-align:left;box-shadow:0 8px 18px rgba(255,122,26,.3)}
.s6 .plate b{font-family:var(--f-num);font-weight:400;font-size:46px;line-height:.9}
.s6 .plate span{font-size:12.5px;font-weight:600} .s6 .plate small{display:block;font-weight:400;font-size:11.5px}
.s6 .room{position:relative;border-radius:16px;background:#fff;border:1.5px solid var(--line);overflow-x:auto;box-shadow:0 14px 30px rgba(21,35,63,.07);
  background-image:linear-gradient(#F0F3F9 1px,transparent 1px),linear-gradient(90deg,#F0F3F9 1px,transparent 1px);background-size:40px 40px}
.s6 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--acc)}
.s6 .room svg{display:block;width:100%;min-width:900px;height:auto}
.s6 .st{cursor:pointer}
.s6 .st:focus{outline:none} .s6 .st:focus .fr{stroke:#F2B705;stroke-width:3}
.s6 .st:hover .fr{stroke:var(--tang)}
.s6 .st.ping .fr{animation:s6ping .9s ease}
@keyframes s6ping{0%{fill:#FFE8D6}100%{fill:#FFFFFF}}
.s6 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:8px}
.s6 .legend i{display:inline-block;width:24px;height:8px;border-radius:4px;vertical-align:middle;margin-right:6px}
.s6 .zone{margin-top:40px;scroll-margin-top:20px;border-radius:16px}
.s6 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:14px;border-bottom:2px solid var(--ink);padding-bottom:8px}
.s6 .zh h3{font-family:var(--f-num);font-weight:400;font-size:38px;margin:0;line-height:1;display:flex;align-items:center;gap:12px}
.s6 .zh h3 i{width:28px;height:12px;border-radius:6px;background:linear-gradient(90deg,var(--acc) 50%,var(--tang) 50%)}
.s6 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s6 .tubes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.s6 .kt{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:12px 14px 14px;text-align:left;color:inherit;display:grid;gap:10px;transition:transform .15s,border-color .15s}
.s6 .kt:hover,.s6 .kt:focus-visible{transform:translateY(-2px);border-color:var(--acc)}
.s6 .kt .top{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.s6 .kt .top span{font-size:13px;font-weight:600;line-height:1.3}
.s6 .kt .top b{font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1;white-space:nowrap}
.s6 .glass{position:relative;height:24px;border-radius:12px;background:#EEF2FB;border:1.5px solid #C9D3EA;margin:0 14px}
.s6 .glass::before,.s6 .glass::after{content:"";position:absolute;top:-4px;width:10px;height:30px;border-radius:4px;background:var(--acc)}
.s6 .glass::before{left:-12px} .s6 .glass::after{right:-12px}
.s6 .glass .cp{position:absolute;top:2px;height:17px;width:38px;border-radius:9px;transform:translateX(-50%)}
.s6 .glass .gh{position:absolute;top:1px;height:19px;width:38px;border-radius:10px;border:2px dashed var(--mute);transform:translateX(-50%)}
.s6 .kt .lg{display:flex;justify-content:space-between;gap:6px;font-size:11px;color:var(--mute)}
.s6 .kt .sw{font-size:11.5px;font-weight:700;letter-spacing:.05em}
.s6 .ahead{color:var(--mint)} .s6 .watch{color:var(--amber)} .s6 .off{color:var(--coral)}
.s6 .cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s6 .pc{position:relative;background:#fff;color:var(--ink);border:1.5px solid var(--line);border-radius:14px;padding:12px 12px 12px 14px;text-align:left;display:grid;gap:8px;transition:transform .15s}
.s6 .pc:hover,.s6 .pc:focus-visible{transform:translateY(-3px);border-color:var(--acc)}
.s6 .pc .nm{font-weight:700;font-size:13.5px;line-height:1.2;padding-right:70px}
.s6 .pc .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s6 .holes{display:flex;flex-wrap:wrap;gap:5px}
.s6 .holes i{width:14px;height:22px;border-radius:4px;border:1.5px solid #C3CCDF;display:grid;place-items:center;font-style:normal;font-size:9px;color:var(--mute)}
.s6 .holes i.y{background:var(--acc);border-color:var(--acc)}
.s6 .holes i.l{background:#FFE3E4;border:2px solid var(--coral)}
.s6 .pc .meta{font-size:11.5px;display:flex;gap:10px;flex-wrap:wrap}
.s6 .pc .meta b{font-family:var(--f-num);font-weight:400;font-size:18px}
.s6 .pc .imp{font-size:11.5px;color:#B3262C;line-height:1.35}
.s6 .pc .nx{font-size:11.5px;color:var(--mute)}
.s6 .pc ul{list-style:none;margin:0;padding:0;font-size:12px;display:grid;gap:3px}
.s6 .pc li.y::before{content:"● ";color:var(--acc)} .s6 .pc li.l{color:#B3262C;font-weight:600} .s6 .pc li.l::before{content:"◍ "} .s6 .pc li.p::before{content:"○ "}
.s6 .pc .tg{position:absolute;top:10px;right:10px;font-size:10px;font-weight:700;letter-spacing:.06em;padding:2px 7px;border-radius:999px;color:#fff}
.s6 .vt{display:inline-flex;border:1.5px solid var(--acc);border-radius:999px;overflow:hidden}
.s6 .vt button{background:transparent;border:0;color:var(--acc);padding:6px 14px;font-size:12px;font-weight:600;min-height:36px}
.s6 .vt button[aria-pressed="true"]{background:var(--acc);color:#fff}
.s6 .rec{display:grid;grid-template-columns:minmax(0,420px) minmax(0,1fr);gap:24px;align-items:center}
.s6 .disc{background:#fff;border-radius:50%;padding:12px;box-shadow:0 18px 40px rgba(21,35,63,.12),inset 0 0 0 6px var(--acc)}
.s6 .disc svg{display:block;width:100%;height:auto}
.s6 .plates{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.s6 .plates button{display:block;width:100%;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12px}
.s6 .plates b{display:block;font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1.1;color:var(--ink)}
.s6 .plates .why{border-color:#F2B8BA;background:#FFF3F3;color:#8C3A3E} .s6 .plates .why b{color:var(--coral)}
@media (max-width:1000px){ .s6 .head{grid-template-columns:1fr} .s6 .gauges{justify-content:flex-start} .s6 .strip{grid-template-columns:1fr 1fr} .s6 .tubes{grid-template-columns:1fr 1fr} .s6 .cards{grid-template-columns:1fr 1fr} .s6 .rec{grid-template-columns:1fr} .s6 .disc{max-width:420px;margin:0 auto} }
@media (max-width:600px){ .s6 .swipe{display:block} .s6 h2{font-size:52px} .s6 .strip,.s6 .tubes,.s6 .cards,.s6 .plates{grid-template-columns:1fr} .s6 .gg{width:calc(50% - 5px)} .s6 .capb span{padding:0 8px;font-size:12px} .s6 .nix{min-width:0;width:100%} }
`,
  render(){
    const C = { live:"#12A06A", testing:"#E08A00", building:"#9AA6BF", blocked:"#E5484D", notstarted:"#C3CCDF" };
    /* --- gauges (pulse strip) --- */
    const gauge = (frac, plan, col, val, lab, sub, attr) => { const a0 = Math.PI, ang = f => a0 + f*Math.PI; const cx=56, cy=62, r=46;
      const pt = (f,rr=r) => [cx + rr*Math.cos(ang(f)), cy + rr*Math.sin(ang(f))];
      const [ex,ey] = pt(Math.min(1,frac)); const [nx,ny] = pt(Math.min(1,frac), r-10); const [px1,py1] = pt(plan, r+3), [px2,py2] = pt(plan, r-9);
      return `<button class="gg" type="button" ${attr}><svg viewBox="0 0 112 76" aria-hidden="true"><path d="M10,62 A46,46 0 0 1 102,62" fill="none" stroke="#E3E9F7" stroke-width="8" stroke-linecap="round"/><path d="M10,62 A46,46 0 0 1 ${ex.toFixed(1)},${ey.toFixed(1)}" fill="none" stroke="${col}" stroke-width="8" stroke-linecap="round"/>
        <line x1="${px1.toFixed(1)}" y1="${py1.toFixed(1)}" x2="${px2.toFixed(1)}" y2="${py2.toFixed(1)}" stroke="#15233F" stroke-width="2" stroke-dasharray="2 2"/><line x1="${cx}" y1="${cy}" x2="${nx.toFixed(1)}" y2="${ny.toFixed(1)}" stroke="#2D4EDB" stroke-width="3" stroke-linecap="round"/><circle cx="${cx}" cy="${cy}" r="6" fill="#2D4EDB"/></svg>
        <b style="color:${col}">${val}</b><span>${lab}</span><em>${sub}</em></button>`; };
    const live = countParts("live");
    const gauges = gauge(live/12, 4/12, "#12A06A", `${live} / 12`, "CHARGE LINES LIVE", "plan 4", `data-tab="links"`)
      + gauge(onCourse/9, 8/9, "#E08A00", `${onCourse} / 9`, "KPIs ON COURSE", "plan 8", `data-tab="measures"`)
      + gauge(ebitdaTotal/spendTotal, D.cumPlan[1]/D.cumSpend[1], "#12A06A", `${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}`, "EBITDA BACK / OUT", "₹ lakh · plan 3.4 back", `data-ref="health:0"`)
      + gauge(0.62, 0.42, "#E5484D", "MAR 2027", "BREAK-EVEN", "plan Jan 2027", `data-ref="health:0"`);

    /* --- the tube room --- */
    const W = 1000, H = 600;
    const box = (x,y,w,h,d) => `<polygon points="${x},${y} ${x+d},${y-d} ${x+w+d},${y-d} ${x+w},${y}" fill="#E3E9F7"/><polygon points="${x+w},${y} ${x+w+d},${y-d} ${x+w+d},${y+h-d} ${x+w},${y+h}" fill="#C9D3EA"/><rect class="fr" x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="#FFFFFF" stroke="#2D4EDB" stroke-width="1.5"/>`;
    const ins = D.parts.filter(p=>p.side==="in"), outs = D.parts.filter(p=>p.side==="out"), rule = D.parts.find(p=>p.side==="rules");
    const ex = 420, ew = 170, ey = 200, eh = 210; /* engine */
    let defs = "", tubes = "", caps = "", stations = "";
    const tube = (id, d, st) => {
      defs += `<path id="tp${id}" d="${d}"/>`;
      if (st==="building" || st==="notstarted") return `<path d="${d}" fill="none" stroke="${st==="building"?"#9AA6BF":"#C3CCDF"}" stroke-width="12" stroke-linecap="round" stroke-dasharray="${st==="building"?"10 7":"2 9"}" opacity=".9"/><path d="${d}" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>`;
      const glow = C[st];
      return `<path d="${d}" fill="none" stroke="#1F3AAE" stroke-width="16" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#FFFFFF" stroke-width="11" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${glow}" stroke-opacity=".28" stroke-width="9" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="2" transform="translate(0,-3)" stroke-linecap="round"/>`;
    };
    const capsule = (id, st, i) => { if (st==="live") return [0,1,2].map(k=>`<rect x="-9" y="-4.5" width="18" height="9" rx="4.5" fill="#FF7A1A" stroke="#B34E00"><animateMotion dur="3.2s" begin="${(k*1.07 + i*.3).toFixed(2)}s" repeatCount="indefinite" rotate="auto"><mpath href="#tp${id}"/></animateMotion></rect>`).join("");
      if (st==="testing") return `<rect x="-9" y="-4.5" width="18" height="9" rx="4.5" fill="#E08A00" stroke="#1F3AAE"><animateMotion dur="8s" begin="${i*.6}s" repeatCount="indefinite" rotate="auto"><mpath href="#tp${id}"/></animateMotion></rect>`;
      if (st==="blocked") return `<rect x="-9" y="-4.5" width="18" height="9" rx="4.5" fill="#E5484D" stroke="#6B1A1A"><animateMotion dur="1s" fill="freeze" keyPoints="0.5;0.5" keyTimes="0;1" calcMode="linear" rotate="auto"><mpath href="#tp${id}"/></animateMotion></rect>`;
      return ""; };
    const label = (x,y,w,h,p,align) => `<foreignObject x="${x+38}" y="${y+5}" width="${w-44}" height="${h-8}"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 11.5px/1.25 Poppins,sans-serif;color:#15233F;height:${h-10}px;display:flex;flex-direction:column;justify-content:center">${esc(p.name)}<span style="font-weight:400;font-size:10px;color:${C[p.st]==="#C3CCDF"?"#5A6782":C[p.st]}">${PART_WORD[p.st]} · ${esc(p.when.replace(/^Live since /,"since "))}</span></div></foreignObject>`;
    const badge = (x,y,p) => `<circle cx="${x+19}" cy="${y}" r="13" fill="${p.st==="notstarted"||p.st==="building"?"#FFFFFF":C[p.st]}" stroke="${C[p.st]==="#C3CCDF"?"#9AA6BF":C[p.st]}" stroke-width="2" ${p.st==="building"||p.st==="notstarted"?'stroke-dasharray="3 2"':""}/><text x="${x+19}" y="${y+4}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="15" fill="${p.st==="notstarted"||p.st==="building"?"#15233F":"#15233F"}">${p.id}</text>`;
    const sw = 230, sh = 56, gap = 72;
    ins.forEach((p,i) => { const x = 24, y = 40 + i*gap; const ty = ey + 30 + i*(eh-60)/(ins.length-1);
      const d = `M${x+sw+8},${y+sh/2} C${x+sw+90},${y+sh/2} ${ex-90},${ty} ${ex},${ty}`;
      tubes += tube(p.id, d, p.st); caps += capsule(p.id, p.st, i);
      if (p.st==="blocked") { const mx = (x+sw+ex)/2, my = (y+sh/2+ty)/2; caps += `<g transform="translate(${mx},${my - 16})"><path d="M0,-12 L11,8 L-11,8 Z" fill="#E5484D" stroke="#15233F"/><text y="6" text-anchor="middle" font-size="11" font-weight="700" fill="#15233F">!</text></g>`; }
      stations += `<g class="st" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}">${box(x,y,sw,sh,8)}${badge(x,y+sh/2,p)}${label(x,y,sw,sh,p)}<rect x="${x+sw}" y="${y+sh/2-9}" width="10" height="18" rx="2" fill="#2D4EDB"/></g>`; });
    outs.forEach((p,i) => { const x = W - 24 - sw, y = 90 + i*(gap+42); const ty = ey + 40 + i*(eh-80)/(outs.length-1);
      const d = `M${ex+ew},${ty} C${ex+ew+90},${ty} ${x-90},${y+sh/2} ${x-8},${y+sh/2}`;
      tubes += tube(p.id, d, p.st); caps += capsule(p.id, p.st, i+7);
      stations += `<g class="st" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}">${box(x,y,sw,sh,8)}${badge(x,y+sh/2,p)}${label(x,y,sw,sh,p)}<rect x="${x-10}" y="${y+sh/2-9}" width="10" height="18" rx="2" fill="#2D4EDB"/></g>`; });
    /* rules feed from the top */
    { const p = rule, x = ex + ew/2 - sw/2, y = 30; const d = `M${ex+ew/2},${y+sh+6} L${ex+ew/2},${ey-16}`;
      tubes += tube(p.id, d, p.st); caps += capsule(p.id, p.st, 3);
      stations += `<g class="st" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}">${box(x,y,sw,sh,8)}${badge(x,y+sh/2,p)}${label(x,y,sw,sh,p)}</g>`; }
    /* engine: a brass drum */
    const engine = `<g aria-label="The billing engine">
      <ellipse cx="${ex+ew/2}" cy="${ey+eh}" rx="${ew/2+6}" ry="18" fill="#15233F" opacity=".6"/>
      <rect x="${ex}" y="${ey}" width="${ew}" height="${eh}" fill="url(#drum)"/>
      <ellipse cx="${ex+ew/2}" cy="${ey+eh}" rx="${ew/2}" ry="16" fill="#1F3AAE"/>
      <ellipse cx="${ex+ew/2}" cy="${ey}" rx="${ew/2}" ry="16" fill="#C9D4FF" stroke="#2D4EDB" stroke-width="2"/>
      <ellipse cx="${ex+ew/2}" cy="${ey}" rx="${ew/2-18}" ry="9" fill="#0F1B3D"/>
      ${[0.25,0.75].map(f=>`<line x1="${ex}" x2="${ex+ew}" y1="${ey+eh*f}" y2="${ey+eh*f}" stroke="#1F3AAE" stroke-width="2"/>`).join("")}
      <rect x="${ex+14}" y="${ey+64}" width="${ew-28}" height="84" rx="6" fill="#0B0F18" stroke="#0F1B3D" stroke-width="2"/>
      <text x="${ex+ew/2}" y="${ey+44}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="22" fill="#FFFFFF">BILLING ENGINE</text>
      <text x="${ex+ew/2}" y="${ey+82}" text-anchor="middle" font-size="9" letter-spacing="1.4" fill="#A9BAFF">POSTED TODAY</text>
      <text id="s6amt" class="ticker" x="${ex+ew/2}" y="${ey+108}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="26" fill="#5BE3A4">₹18,42,300</text>
      <text id="s6cnt" x="${ex+ew/2}" y="${ey+124}" text-anchor="middle" font-size="9.5" fill="#A9BAFF">1,284 charges</text>
      <text id="s6last" x="${ex+ew/2}" y="${ey+140}" text-anchor="middle" font-size="9.5" fill="#FFB067">Lab · CBC · ₹450 · Bed 214</text>
      <text x="${ex+ew/2}" y="${ey+eh-14}" text-anchor="middle" font-size="9.5" fill="#FFFFFF" font-weight="700">priced from the charge list</text></g>`;
    defs += `<linearGradient id="drum" x1="0" x2="1"><stop offset="0" stop-color="#1F3AAE"/><stop offset=".35" stop-color="#7E96FF"/><stop offset=".55" stop-color="#A9BAFF"/><stop offset="1" stop-color="#1F3AAE"/></linearGradient>`;
    const headers = `<text x="24" y="22" font-size="11" font-weight="700" letter-spacing="1.5" fill="#2D4EDB">EVENTS IN THE STAY</text><text x="${W-24}" y="72" text-anchor="end" font-size="11" font-weight="700" letter-spacing="1.5" fill="#2D4EDB">BILLS GOING OUT</text>
      <text x="${W-24}" y="${H-28}" text-anchor="end" font-size="10.5" fill="#5A6782">The signed summary for claims arrives from the Discharge Summary suite</text>`;
    const room = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Seven kinds of event and the charge list feed the billing engine, which sends bills to the family and the insurers."><defs>${defs}</defs>${headers}${tubes}${engine}${caps}${stations}</svg>`;

    /* --- KPI glass tubes --- */
    const kt = k => { const n = Math.min(1,prog(k,k.now))*100, p = Math.min(1,prog(k,k.plan))*100; const col = k.state==="ahead"?"#12A06A":k.state==="watch"?"#E08A00":"#E5484D";
      return `<button class="kt" type="button" data-ref="kpi:${k.id}"><span class="top"><span>${esc(k.name)}</span><b class="${k.state}">${fmtv(k,k.now)}</b></span>
        <span class="glass" aria-hidden="true"><span class="gh" style="left:calc(${p}% * .9 + 5%)"></span><span class="cp" style="left:calc(${n}% * .9 + 5%);background:${col};color:${col}"></span></span>
        <span class="lg"><span>${fmtv(k,k.base)}</span><span class="sw ${k.state}">${STATE_WORD[k.state].toUpperCase()} · ${gapText(k)}</span><span>${fmtv(k,k.target)}</span></span></button>`; };

    /* --- punch cards --- */
    const pc = p => { const tgc = p.state==="ahead"?"#12A06A":p.state==="watch"?"#B87000":"#D93A40";
      let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":"p"}">${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const h = []; for (let i=0;i<p.due;i++) h.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":""}">${i<p.done||i<p.done+p.late?"":i+1}</i>`); body = `<span class="holes" aria-label="${p.done} of ${p.due} done, ${p.late} late">${h.join("")}</span><span class="meta"><span><b>${p.done}</b>/${p.due} done</span>${p.late?`<span style="color:#C62F35"><b>${p.late}</b> late</span>`:""}</span>`; }
      return `<button class="pc" type="button" data-ref="per:${p.key}"><span class="tg" style="background:${tgc}">${PERSON_WORD[p.state].toUpperCase()}</span><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</button>`; };

    /* --- chart recorder --- */
    const R = 148, cx = 190, cy = 190, n = D.cumMonths.length, maxV = 45;
    const ang = i => -Math.PI/2 + (i/(n))*Math.PI*2*0.92 + 0.12;
    const P2 = (i,v) => { const r = 24 + (R-24)*v/maxV; return [cx + r*Math.cos(ang(i)), cy + r*Math.sin(ang(i))]; };
    const trace = (arr, from, to) => arr.slice(from,to+1).map((v,j)=>{ const [x,y]=P2(from+j,v); return (j?"L":"M")+x.toFixed(1)+","+y.toFixed(1); }).join(" ");
    let rings = ""; [10,20,30,40].forEach(v=>{ const r = 24+(R-24)*v/maxV; rings += `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#8A94AB" stroke-opacity=".35"/><text x="${cx+3}" y="${cy-r+11}" font-size="9" fill="#8A94AB">₹${v} L</text>`; });
    let spokes = ""; D.cumMonths.forEach((m,i)=>{ const [x1,y1]=P2(i,0),[x2,y2]=P2(i,maxV),[lx,ly]=P2(i,maxV+6);
      spokes += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#8A94AB" stroke-opacity=".3"/><text x="${lx}" y="${ly+4}" text-anchor="middle" font-size="11" font-weight="600" fill="${i<=D.actualTo?"#15233F":"#9AA6BF"}">${m}</text>
        <path data-ref="month:${i}" data-nopen d="M${cx},${cy} L${P2(i-.45,maxV)[0]},${P2(i-.45,maxV)[1]} L${P2(i+.45,maxV)[0]},${P2(i+.45,maxV)[1]} Z" fill="transparent" style="cursor:help"/>`; });
    const [bx,by] = P2(6, D.cumFore[6]); const [px,py] = P2(4, D.cumPlan[4]);
    const recorder = `<svg viewBox="0 0 380 380" role="img" aria-label="Money out against EBITDA back by month. The plan crossed in January; the forecast crosses in March.">
      <circle cx="${cx}" cy="${cy}" r="${R+36}" fill="#F7F9FD"/>${rings}${spokes}
      <path d="${trace(D.cumPlan,0,n-1)}" fill="none" stroke="#9AA6BF" stroke-width="1.5" stroke-dasharray="4 4"/>
      <path d="${trace(D.cumSpend,0,n-1)}" fill="none" stroke="#15233F" stroke-width="2.2"/>
      <path d="${trace(D.cumFore,0,D.actualTo)}" fill="none" stroke="#FF7A1A" stroke-width="3"/>
      <path d="${trace(D.cumFore,D.actualTo,n-1)}" fill="none" stroke="#FF7A1A" stroke-width="2" stroke-dasharray="2 4"/>
      <circle cx="${px}" cy="${py}" r="6" fill="none" stroke="#9AA6BF" stroke-width="1.5"/>
      <circle cx="${bx}" cy="${by}" r="8" fill="none" stroke="#FF7A1A" stroke-width="2.5"/>
      <circle cx="${cx}" cy="${cy}" r="16" fill="#2D4EDB"/><circle cx="${cx}" cy="${cy}" r="6" fill="#7E96FF"/>
      <line x1="${cx}" y1="${cy}" x2="${bx}" y2="${by}" stroke="#15233F" stroke-width="2"/>
    </svg>`;

    return `<div class="s6"><div class="wrap">
      <nav class="disp-panel" aria-label="Suite sections"><div class="nix" aria-hidden="true"><small>YOU ARE ON</small><b id="s6at">OVERVIEW</b></div>
        <div class="caps">${TABS.map((t,i)=>`<button class="capb ${i?"":"on"}" type="button" data-tab="${t[0]}"><i></i><span>${t[1]}</span><em></em></button>`).join("")}</div></nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="gauges" aria-label="Pulse strip">${gauges}</div></div>
      <div class="strip" aria-label="Watch list and next go-live">${D.watch.map(w=>`<button class="jam" type="button" data-ref="${w.ref}"><i aria-hidden="true"></i><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}
        <button class="plate" type="button" data-ref="part:${D.milestone.part}"><b>${D.milestone.days}</b><span>days to the next go-live<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to see every line →</p><div class="room">${room}</div>
        <div class="legend"><span><i style="background:#12A06A"></i>Live</span><span><i style="background:#E08A00"></i>Testing</span><span><i style="background:repeating-linear-gradient(90deg,#9AA6BF 0 6px,transparent 6px 10px)"></i>Being built</span><span><i style="background:#E5484D"></i>Late</span><span><i style="background:repeating-linear-gradient(90deg,#C3CCDF 0 2px,transparent 2px 8px)"></i>Not started</span><span>· Data as of ${esc(D.asOf)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3><i></i>KPIs</h3><p>Solid marker is today · dashed marker is the plan for this week · right end is the target</p></div>
        <div class="tubes">${D.kpis.map(kt).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3><i></i>Taskboards</h3>${viewToggle("vt")}</div>
        <div class="cards">${D.people.map(pc).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3><i></i>Project Status</h3><p>Dark line: money out to date · orange: EBITDA back (dotted is forecast) · grey dashed: plan · ₹ lakh</p></div>
        <div class="rec"><div class="disc">${recorder}</div>
          <div class="plates">
            <button type="button" data-ref="month:1">Subscription<b>${L(2.0)}/mo</b></button>
            <button type="button" data-ref="month:1">Salary, the night insurance coordinator we recommended<b>${L(0.25)}/mo</b></button>
            <button type="button" data-ref="month:1">One-time so far (charge list, insurer connectors)<b>${L(3.0)}</b></button>
            <button type="button" data-ref="health:0">Extra revenue so far, from charges no longer missed<b>${L(revTotal)}</b></button>
            <button type="button" data-ref="health:0">EBITDA now, and at full run<b>${L(D.ebitda[1])} → ${L(D.runRate.ebitda)}/mo</b></button>
            <button type="button" class="why" data-ref="health:0">Break-even ${D.breakeven.fore}, ${D.breakeven.late} late<b>See why ›</b></button>
          </div></div></section>
    </div></div>`;
  },
  after(){
    const at = document.getElementById("s6at");
    document.querySelectorAll(".s6 .capb").forEach(b => b.addEventListener("click", () => { at.textContent = b.textContent.trim().toUpperCase(); }));
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { document.querySelectorAll(".s6 animateMotion").forEach(a => a.remove()); return; }
    tickEngine("s6", ".s6 .st");
  }
});
