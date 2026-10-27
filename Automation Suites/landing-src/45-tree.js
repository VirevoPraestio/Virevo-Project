/* ===== Financial Health, option 1: burgundy and champagne, the measures as one tree from EBITDA down to the causes and the feeds ===== */
SCHEMES.push({
  key:"tree", letter:"1", name:"Burgundy and champagne",
  note:"<b>Option 1 · burgundy and champagne.</b> EBITDA at the top, the revenue streams and costs below it, your two measures beside them, then the causes that moved them and the feeds the numbers come from. Red lines pull down, green lines lift.",
  vars:{ "--sh-bg":"#FFFDF9","--sh-fg":"#2A1A1F","--sh-mute":"#6B5A5F","--sh-line":"#E8DDD3","--sh-card":"#FAF4EC","--c-ok":"#2F7D4F","--c-warn":"#A8720E","--c-bad":"#C2362F","--pk-bg":"#2A1A1F","--pk-fg":"#FFFFFF","--pk-line":"#B8955A","--pk-r":"8px","--sh-r":"14px" },
  fab:18,
  blocks:{ nav:".ribbons", pulse:".ledger", watch:".seals", countdown:".stub", hero:".tree", kpis:".book", recovery:".rec", team:".cheques", money:".mny" },
  css:`
.s15{--bg:#FBF7F0;--ink:#2A1A1F;--mute:#6B5A5F;--bur:#7A1F3D;--bur2:#F3DDE3;--ch:#E9D8B4;--chd:#B8955A;--ok:#2F7D4F;--warn:#A8720E;--bad:#C2362F;--line:#E8DDD3;
  background:var(--bg);color:var(--ink);padding:0 16px 90px;overflow-x:clip}
.s15 .wrap{max-width:1240px;margin:0 auto}
.s15 .ribbons{display:flex;flex-wrap:wrap;gap:6px;border-top:6px solid var(--bur);padding:0 4px;margin-bottom:6px}
.s15 .rb{position:relative;background:var(--ch);border:0;padding:12px 14px 16px;font-size:12.5px;font-weight:600;color:var(--ink);min-height:48px;clip-path:polygon(0 0,100% 0,100% 100%,50% 82%,0 100%);transition:padding .15s}
.s15 .rb:hover{padding-bottom:20px}
.s15 .rb.on{background:var(--bur);color:#fff;padding-bottom:22px}
.s15 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:18px 0 16px}
.s15 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--bur)}
.s15 h2{font-family:var(--f-num);font-weight:400;font-size:78px;line-height:.88;margin:4px 0 0;letter-spacing:.01em}
.s15 .head p{margin:8px 0 0;font-size:13px;color:var(--mute)}
.s15 .ledger{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1.5px solid var(--ink);background:#FFFDF9;min-width:560px}
.s15 .lg{border:0;border-right:1px solid var(--line);background:transparent;padding:10px 14px;text-align:left;color:inherit}
.s15 .lg:last-child{border-right:0} .s15 .lg:hover{background:var(--bur2)}
.s15 .lg span{display:block;font-size:10.5px;letter-spacing:.12em;font-weight:700;color:var(--mute)}
.s15 .lg b{display:inline-block;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1.05;border-bottom:3px double var(--ink);padding-bottom:1px}
.s15 .lg em{display:block;font-style:normal;font-size:11px;color:var(--bur);margin-top:3px}
.s15 .seals{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.8fr);gap:12px;margin-bottom:16px}
.s15 .sl{display:grid;grid-template-columns:40px minmax(0,1fr);gap:12px;align-items:center;background:#FFFDF9;border:1px solid var(--line);border-radius:10px;padding:10px 12px;text-align:left;color:inherit;font-size:12.5px;font-weight:600;box-shadow:0 2px 0 var(--line)}
.s15 .sl i{width:36px;height:36px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#A8475F,var(--bur) 60%,#5A142C);box-shadow:inset 0 0 0 4px rgba(255,255,255,.12),0 2px 3px rgba(0,0,0,.25);display:grid;place-items:center;color:#F3DDE3;font-style:normal;font-family:var(--f-num);font-size:18px}
.s15 .sl small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s15 .sl:hover{border-color:var(--bur)}
.s15 .stub{display:grid;grid-template-columns:auto minmax(0,1fr);gap:12px;align-items:center;background:var(--bur);color:#fff;border:0;border-radius:10px;padding:10px 14px;text-align:left;border-left:6px dotted var(--bg)}
.s15 .stub b{font-family:var(--f-num);font-weight:400;font-size:46px;line-height:.9;color:var(--ch)}
.s15 .stub span{font-size:12px;font-weight:700} .s15 .stub small{display:block;font-weight:400;font-size:11.5px;color:#F3DDE3}
.s15 .tree{border-radius:14px;background:#FFFDF9;border:1px solid var(--line);overflow-x:auto;box-shadow:0 16px 34px rgba(122,31,61,.07)}
.s15 .tree svg{display:block;width:100%;min-width:980px;height:auto}
.s15 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--bur)}
.s15 .nd{cursor:pointer} .s15 .nd:focus{outline:none} .s15 .nd:focus .fc{stroke:#F2B705;stroke-width:3}
.s15 .nd:hover .fc{stroke-width:2.5} .s15 .nd{transition:transform .15s} .s15 .nd:hover{transform:translateY(-3px)}
.s15 .flow{stroke-dasharray:6 8;animation:s15f 1.4s linear infinite}
@keyframes s15f{to{stroke-dashoffset:-28}}
.s15 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:10px}
.s15 .legend i{display:inline-block;width:18px;height:4px;border-radius:2px;vertical-align:3px;margin-right:6px}
.s15 .zone{margin-top:44px;scroll-margin-top:20px;border-radius:14px}
.s15 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:10px 16px;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid var(--ink);box-shadow:0 3px 0 -2px var(--ink)}
.s15 .zh h3{font-family:var(--f-num);font-weight:400;font-size:40px;margin:0;line-height:1;color:var(--bur)}
.s15 .zh p{margin:0;font-size:12.5px;color:var(--mute)}
.s15 .pick{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:12px;font-weight:600}
.s15 .pick>span{color:var(--bur);letter-spacing:.06em}
.s15 .pick select{font:inherit;font-weight:500;font-size:12.5px;padding:8px 10px;border:1.5px solid var(--bur);border-radius:8px;background:#FFFDF9;color:var(--ink);min-height:40px;max-width:260px}
.s15 .book{display:grid;gap:0;border:1.5px solid var(--ink);background:#FFFDF9}
.s15 .brow{display:grid;grid-template-columns:minmax(0,1.6fr) repeat(3,minmax(0,.8fr)) 10px repeat(3,minmax(0,.8fr)) minmax(0,.9fr);gap:0 10px;align-items:center;border:0;border-bottom:1px solid var(--line);background:transparent;padding:10px 14px;text-align:left;color:inherit;font-size:12.5px}
.s15 .brow:hover,.s15 .brow:focus-visible{background:var(--bur2)}
.s15 .brow.hd{font-size:10.5px;letter-spacing:.1em;font-weight:700;color:var(--mute);background:var(--ch);border-bottom:1.5px solid var(--ink);cursor:default}
.s15 .brow.hd:hover{background:var(--ch)}
.s15 .brow .nm{font-weight:600;font-size:13px} .s15 .brow .nm small{display:block;font-weight:400;font-size:11px;color:var(--bur)}
.s15 .brow .n{font-family:var(--f-num);font-size:20px;letter-spacing:.02em;text-align:right}
.s15 .brow .g{text-align:right;font-weight:600;font-size:12px}
.s15 .brow .sep{align-self:stretch;border-left:3px double var(--line)}
.s15 .brow .st{font-size:10.5px;font-weight:700;letter-spacing:.05em;text-align:right}
.s15 .brow.ch{background:linear-gradient(90deg,var(--bur2) 0 5px,transparent 5px)}
.s15 .ahead{color:var(--ok)} .s15 .watch{color:var(--warn)} .s15 .off{color:var(--bad)}
.s15 .runlog{display:flex;flex-wrap:wrap;gap:0;margin-bottom:14px;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#FFFDF9}
.s15 .runlog div{flex:1 1 150px;padding:8px 12px;border-right:1px dashed var(--line);font-size:12px}
.s15 .runlog b{display:block;font-family:var(--f-num);font-weight:400;font-size:18px;color:var(--bur)}
.s15 .rec{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;align-items:start}
.s15 .rcol h4{margin:0 0 8px;font-size:12px;letter-spacing:.1em;font-weight:700;display:flex;justify-content:space-between;align-items:center;padding:8px 12px;border-radius:8px;background:var(--ch);color:var(--ink)}
.s15 .rcol h4 b{font-family:var(--f-num);font-weight:400;font-size:22px}
.s15 .rcol.ceo h4{background:var(--bur);color:#fff}
.s15 .ac{display:block;width:100%;cursor:pointer;background:#FFFDF9;border:1px solid var(--line);border-radius:10px;padding:10px 12px;text-align:left;color:inherit;font-size:12.5px;font-weight:600;margin-bottom:10px;box-shadow:0 2px 0 var(--line);transition:transform .15s}
.s15 .ac:hover,.s15 .ac:focus-visible{transform:translateY(-2px);border-color:var(--bur)}
.s15 .ac small{display:block;font-weight:400;color:var(--mute);font-size:11.5px;margin-top:3px}
.s15 .ac .gn{display:inline-block;margin-top:6px;font-size:11px;font-weight:700;color:var(--ok)}
.s15 .ac.awaiting{border:2px solid var(--bur)} .s15 .ac.approved{border-color:var(--ok)} .s15 .ac.held{opacity:.75}
.s15 .ac .tag{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.06em;padding:2px 7px;border-radius:4px;margin-bottom:5px;background:var(--bur2);color:var(--bur)}
.s15 .ac.approved .tag{background:#DFF0E5;color:var(--ok)}
.s15 .fh-dec{display:flex;gap:8px;margin-top:10px}
.s15 .fh-dec button{flex:1;min-height:40px;border-radius:8px;font-weight:700;font-size:12.5px;border:1.5px solid var(--bur)}
.s15 .fh-dec button:first-child{background:var(--bur);color:#fff} .s15 .fh-dec button:last-child{background:#FFFDF9;color:var(--bur)}
.s15 .cheques{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s15 .cq{display:grid;grid-template-columns:56px minmax(0,1fr);background:#FFFDF9;border:1px solid var(--line);border-radius:10px;padding:0;text-align:left;color:inherit;overflow:hidden;transition:transform .15s}
.s15 .cq:hover,.s15 .cq:focus-visible{transform:translateY(-3px);border-color:var(--bur)}
.s15 .cq .stb{background:var(--ch);border-right:2px dashed #FFFDF9;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;padding:10px 4px}
.s15 .cq .stb b{font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1} .s15 .cq .stb span{font-size:10px;color:var(--mute)}
.s15 .cq .bd{padding:10px 12px;display:grid;gap:6px}
.s15 .cq .nm{font-weight:700;font-size:13px;line-height:1.2} .s15 .cq .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s15 .cq .chip{justify-self:start;font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:999px;color:#fff}
.s15 .cq .bar{display:flex;gap:2px;height:8px} .s15 .cq .bar i{flex:1;background:var(--line);border-radius:2px} .s15 .cq .bar i.y{background:var(--bur)} .s15 .cq .bar i.l{background:var(--bad)}
.s15 .cq ul{list-style:none;margin:0;padding:0;font-size:12px;display:grid;gap:3px}
.s15 .cq li::before{content:"○ ";color:var(--mute)} .s15 .cq li.y::before{content:"● ";color:var(--bur)} .s15 .cq li.l{color:var(--bad);font-weight:600} .s15 .cq li.l::before{content:"◐ "}
.s15 .cq .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s15 .cq .nx{font-size:11.5px;color:var(--mute)}
.s15 .vt{display:inline-flex;border:1.5px solid var(--bur);border-radius:8px;overflow:hidden}
.s15 .vt button{border:0;background:#FFFDF9;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:var(--bur)}
.s15 .vt button[aria-pressed="true"]{background:var(--bur);color:#fff}
.s15 .mny{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s15 .chart{background:#FFFDF9;border:1px solid var(--line);border-radius:14px;padding:12px;overflow-x:auto}
.s15 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s15 .mlist{display:grid;border:1.5px solid var(--ink);background:#FFFDF9}
.s15 .mlist button{display:flex;justify-content:space-between;gap:12px;align-items:baseline;background:transparent;border:0;border-bottom:1px solid var(--line);padding:10px 12px;text-align:left;color:var(--mute);font-size:12.5px}
.s15 .mlist b{font-family:var(--f-num);font-weight:400;font-size:22px;color:var(--ink);white-space:nowrap}
.s15 .mlist .why{background:var(--bur);color:#F3DDE3;border-bottom:0} .s15 .mlist .why b{color:#fff}
@media (max-width:1000px){ .s15 .head{grid-template-columns:1fr} .s15 .ledger{min-width:0} .s15 .seals{grid-template-columns:1fr 1fr} .s15 .rec{grid-template-columns:1fr} .s15 .cheques{grid-template-columns:1fr 1fr} .s15 .mny{grid-template-columns:1fr}
  .s15 .brow{grid-template-columns:minmax(0,1fr) auto auto;gap:4px 10px} .s15 .brow.hd{display:none} .s15 .brow .sep{display:none}
  .s15 .brow .nm{grid-column:1/-1} .s15 .brow .n,.s15 .brow .g{text-align:left} .s15 .brow .n::before{content:attr(data-l);display:block;font-family:var(--f-body);font-size:10px;color:var(--mute);letter-spacing:.06em} }
@media (max-width:600px){ .s15 .swipe{display:block} .s15 h2{font-size:54px} .s15 .ledger{grid-template-columns:1fr 1fr} .s15 .lg:nth-child(2){border-right:0} .s15 .lg:nth-child(-n+2){border-bottom:1px solid var(--line)} .s15 .seals,.s15 .cheques{grid-template-columns:1fr} .s15 .rb{padding:10px 10px 14px;font-size:12px} }
`,
  render(){
    const SC = { ahead:"#2F7D4F", watch:"#D9940A", off:"#C2362F" }, PC = { live:"#2F7D4F", testing:"#D9940A", building:"#9C8F93", blocked:"#C2362F", notstarted:"#D8CFC9" };
    const live = countParts("live"), wait = D.actions.filter(a=>a.st==="awaiting").length;
    const lg = (lab, val, sub, attr) => `<button class="lg" type="button" ${attr}><span>${lab}</span><b>${val}</b><em>${sub}</em></button>`;
    const ledger = lg("PARTS LIVE",`${live} / 12`,"plan 7",`data-tab="links"`) + lg("KPIS ON COURSE",`${onCourse} / ${D.kpis.length}`,`plan ${D.kpis.length}`,`data-tab="measures"`)
      + lg("EBITDA BACK / OUT",`${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}`,`₹ lakh · plan ${D.cumPlan[D.actualTo].toFixed(1)} back`,`data-ref="health:0"`) + lg("BREAK-EVEN",D.breakeven.fore.toUpperCase(),`plan ${D.breakeven.plan}`,`data-ref="health:0"`);

    /* --- the tree --- */
    const W = 1100, H = 660; let g = `<defs><filter id="s15sh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#7A1F3D" flood-opacity=".14"/></filter></defs>`;
    const node = (k, cx, cy, w, h, big) => { const c = SC[k.state]; const x = cx - w/2, y = cy - h/2;
      return `<g class="nd" data-ref="kpi:${k.id}" tabindex="0" role="button" aria-label="${esc(k.name)}: ${fmtv(k,k.day[1])} against ${fmtv(k,k.day[0])} expected, ${STATE_WORD[k.state]}">
        <rect x="${x+4}" y="${y+6}" width="${w}" height="${h}" rx="12" fill="#E9D8B4"/>
        <rect class="fc" x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="#FFFDF9" stroke="${c}" stroke-width="1.6" filter="url(#s15sh)"/>
        <rect x="${x}" y="${y}" width="${w}" height="6" rx="3" fill="${c}"/>
        <foreignObject x="${x+8}" y="${y+8}" width="${w-16}" height="${h-12}"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 ${big?12:10.5}px/1.2 Poppins,sans-serif;color:#2A1A1F;text-align:center">
          <div style="letter-spacing:.06em">${esc(big?k.name.toUpperCase():k.short)}${D.core.includes(k.id)?"":` <span style="color:#7A1F3D;font-weight:700">· yours</span>`}</div>
          <div style="font-family:'Bebas Neue';font-weight:400;font-size:${big?34:22}px;line-height:1.05;color:${c}">${fmtv(k,k.day[1])}</div>
          <div style="font-weight:400;font-size:${big?11:9.5}px;color:#6B5A5F">expected ${fmtv(k,k.day[0])} · ${D.sinceLabel} ${fhPct(k)}</div></div></foreignObject></g>`; };
    const K = id => KP[id];
    /* positions */
    const pos = { K1:[550,62], K2:[300,182], costs:[790,182], K3:[130,312], K4:[300,312], K5:[470,312] };
    D.chosen.forEach((id,i) => pos[id] = [700 + i*175, 312]);
    const cExp = K("K2").day[0] - K("K1").day[0], cAct = K("K2").day[1] - K("K1").day[1];
    /* edges up the tree */
    const up = (a, b, col) => `<path d="M${pos[a][0]},${pos[a][1]-34} C${pos[a][0]},${(pos[a][1]+pos[b][1])/2} ${pos[b][0]},${(pos[a][1]+pos[b][1])/2} ${pos[b][0]},${pos[b][1]+(b==="K1"?44:34)}" fill="none" stroke="${col}" stroke-width="2.4"/>`;
    g += up("K3","K2","#D8C9B9") + up("K4","K2","#D8C9B9") + up("K5","K2","#D8C9B9") + up("K2","K1","#D8C9B9") + up("costs","K1","#D8C9B9");
    g += `<text x="${pos.K2[0]-110}" y="${pos.K2[1]-58}" font-size="10" fill="#6B5A5F">revenue</text><text x="${pos.costs[0]+60}" y="${pos.costs[1]-58}" font-size="10" fill="#6B5A5F">less costs</text>`;
    /* drivers row */
    const dy = 448, dw = 122, dgap = 9.5, dx0 = (W - (D.drivers.length*dw + (D.drivers.length-1)*dgap))/2;
    const target = d => { const t = d.kpis.filter(id => ["K3","K4","K5"].includes(id) || D.chosen.includes(id)); if (t.length) return t; return d.e < 0 ? ["costs"] : []; };
    let edges = "", tags = "";
    D.drivers.forEach((d,i) => { const x = dx0 + i*(dw+dgap), cx = x + dw/2, col = d.lift ? "#2F7D4F" : d.e ? "#C2362F" : "#9C8F93";
      target(d).forEach(t => { const [tx,ty] = pos[t]; const ey = ty + 36; edges += `<path class="${d.e?"flow":""}" d="M${cx},${dy-4} C${cx},${dy-50} ${tx},${ey+40} ${tx},${ey}" fill="none" stroke="${col}" stroke-width="${1.2+Math.min(3,Math.abs(d.e)*5)}" opacity=".55"/>`; });
      tags += `<g class="nd" data-ref="drv:${d.id}" tabindex="0" role="button" aria-label="Cause: ${esc(d.name)}"><rect class="fc" x="${x}" y="${dy}" width="${dw}" height="66" rx="8" fill="${d.lift?"#EAF4EC":d.e?"#FBEDEE":"#F4EFEA"}" stroke="${col}" stroke-width="1.2"/>
        <foreignObject x="${x+6}" y="${dy+4}" width="${dw-12}" height="60"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 9.5px/1.2 Poppins,sans-serif;color:#2A1A1F;height:58px;display:flex;flex-direction:column;justify-content:space-between"><span>${esc(d.name)}</span><span style="font-family:'Bebas Neue';font-weight:400;font-size:15px;color:${col}">${d.e?fhL(d.e)+" A DAY":"NO DIRECT EFFECT"}</span></div></foreignObject></g>`; });
    g += edges;
    /* costs node (not a KPI: shows what was spent) */
    { const [cx,cy] = pos.costs, w = 170, h = 74, x = cx - w/2, y = cy - h/2, over = cAct > cExp;
      g += `<g aria-label="Costs on ${esc(D.dayLabel)}: ₹${cAct.toFixed(1)} lakh against ₹${cExp.toFixed(1)} lakh expected"><rect x="${x+4}" y="${y+6}" width="${w}" height="${h}" rx="12" fill="#E9D8B4"/><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="#FFFDF9" stroke="${over?"#C2362F":"#2F7D4F"}" stroke-width="1.6" stroke-dasharray="5 3"/>
        <text x="${cx}" y="${y+22}" text-anchor="middle" font-size="10.5" font-weight="600" letter-spacing=".6" fill="#2A1A1F">COSTS</text><text x="${cx}" y="${y+48}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="24" fill="${over?"#C2362F":"#2F7D4F"}">₹${cAct.toFixed(1)} lakh</text><text x="${cx}" y="${y+64}" text-anchor="middle" font-size="9.5" fill="#6B5A5F">expected ₹${cExp.toFixed(1)} lakh</text></g>`; }
    g += node(K("K1"), pos.K1[0], pos.K1[1], 260, 92, true) + node(K("K2"), pos.K2[0], pos.K2[1], 170, 74) + ["K3","K4","K5"].map(id => node(K(id), pos[id][0], pos[id][1], 156, 74)).join("") + D.chosen.map(id => node(K(id), pos[id][0], pos[id][1], 156, 74)).join("");
    g += `<rect x="612" y="262" width="350" height="104" rx="16" fill="none" stroke="#B8955A" stroke-dasharray="3 5"/><text x="626" y="258" font-size="10" font-weight="700" letter-spacing="1.2" fill="#B8955A">YOUR TWO MEASURES</text>`;
    g += `<text x="${dx0}" y="${dy-14}" font-size="10.5" font-weight="700" letter-spacing="1.4" fill="#7A1F3D">WHAT MOVED THEM ON ${esc(D.dayLabel.toUpperCase())}</text>` + tags;
    /* feeds */
    const fy = 566, fw = 82, fg = 6, fx0 = (W - (12*fw + 11*fg))/2;
    g += `<text x="${fx0}" y="${fy-12}" font-size="10.5" font-weight="700" letter-spacing="1.4" fill="#7A1F3D">WHERE THE NUMBERS COME FROM · READ EVERY MORNING AT 6 AM</text>`;
    D.parts.forEach((p,i) => { const x = fx0 + i*(fw+fg), c = PC[p.st], soft = p.st==="building"||p.st==="notstarted";
      g += `<g class="nd" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}"><rect class="fc" x="${x}" y="${fy}" width="${fw}" height="70" rx="8" fill="${soft?"#FBF7F0":"#FFFDF9"}" stroke="${c}" stroke-width="1.4" ${soft?'stroke-dasharray="4 3"':""}/>
        <foreignObject x="${x+5}" y="${fy+4}" width="${fw-10}" height="64"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 9px/1.2 Poppins,sans-serif;color:#2A1A1F;height:62px;display:flex;flex-direction:column;justify-content:space-between"><span><b style="font-family:'Bebas Neue';font-weight:400;font-size:13px;color:#7A1F3D">${p.id}</b> ${esc(p.short)}</span><span style="font-size:8.5px;font-weight:700;letter-spacing:.04em;color:${c}">${PART_WORD[p.st].toUpperCase()}</span></div></foreignObject></g>`; });
    const tree = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="EBITDA at the top, built from revenue less costs; the revenue streams and your two measures below; the causes that moved them on ${esc(D.dayLabel)}; and the twelve feeds the numbers come from.">${g}</svg>`;

    /* --- KPI book --- */
    const row = k => `<button class="brow ${D.core.includes(k.id)?"":"ch"}" type="button" data-ref="kpi:${k.id}"><span class="nm">${esc(k.name)}<small>${D.core.includes(k.id)?(k.unit==="L"?"₹ lakh a day":""):"your measure · "+esc(k.kind)}</small></span>
      <span class="n" data-l="EXPECTED ${esc(D.dayLabel.toUpperCase())}">${fmtv(k,k.day[0])}</span><span class="n ${k.dayState}" data-l="ACTUAL">${fmtv(k,k.day[1])}</span><span class="g ${k.dayState}">${fhGap(k,k.day[0],k.day[1]).replace(" than expected","").replace(" of expected","").replace(" expected","")}</span><span class="sep"></span>
      <span class="n" data-l="EXPECTED ${esc(D.sinceLabel.toUpperCase())}">${fmtv(k,k.td[0])}</span><span class="n ${k.tdState}" data-l="ACTUAL">${fmtv(k,k.td[1])}</span><span class="g ${k.tdState}">${fhPct(k)}</span><span class="st ${k.state}">${STATE_WORD[k.state].toUpperCase()}</span></button>`;
    const book = `<div class="brow hd" aria-hidden="true"><span>MEASURE</span><span style="text-align:right">EXPECTED</span><span style="text-align:right">${esc(D.dayLabel.toUpperCase())}</span><span style="text-align:right">GAP</span><span></span><span style="text-align:right">EXPECTED</span><span style="text-align:right">${esc(D.sinceLabel.toUpperCase())}</span><span style="text-align:right">GAP</span><span style="text-align:right">STATE</span></div>` + D.kpis.map(row).join("");

    /* --- recovery --- */
    const card = a => `<div class="ac ${a.st}" role="button" tabindex="0" data-ref="act:${a.id}"><span class="tag">${esc(FH_ST[a.st].toUpperCase())}</span><br>${esc(a.t)}<small>${esc(a.when)}${a.st==="advised"?` · to ${esc(fhWho(a.who))}: ${esc(a.reply)}`:""}${a.cost?` · ${esc(fhCost(a))}`:""}</small>${a.gain?`<span class="gn">${fhL(a.gain)} EBITDA a day</span>`:""}${fhDecideBtns(a)}</div>`;
    const col = (cls, title, list) => `<div class="rcol ${cls}"><h4><span>${title}</span><b>${list.length}</b></h4>${list.map(card).join("")}</div>`;
    const rec = col("", "DONE BY THE SUITE", D.actions.filter(a=>a.st==="done")) + col("", "ADVISED · WAITING ON THE OWNER", D.actions.filter(a=>a.st==="advised")) + col("ceo", "FOR THE CEO TO CONFIRM", D.actions.filter(a=>["awaiting","approved","held"].includes(a.st)));

    /* --- people --- */
    const cq = p => { const cc = p.state==="ahead"?"#2F7D4F":p.state==="watch"?"#A8720E":"#C2362F"; let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":/^(late|waiting)/.test(String(t[1]))?"l":""}">${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const b = []; for (let i=0;i<p.due;i++) b.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":""}"></i>`); body = `<span class="bar" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span>`; }
      return `<button class="cq" type="button" data-ref="per:${p.key}"><span class="stb"><b>${p.done}</b><span>of ${p.due}</span>${p.late?`<span style="color:var(--bad);font-weight:700">${p.late} late</span>`:""}</span><span class="bd"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="chip" style="background:${cc}">${PERSON_WORD[p.state]}</span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</span></button>`; };

    /* --- money --- */
    const CW = 760, CH = 320, x0 = 50, x1 = 740, y0 = 24, y1 = 260, n = D.cumMonths.length, vmax = 110;
    const X = i => x0 + (x1-x0)*i/(n-1), Y = v => y1 - (y1-y0)*v/vmax;
    let c = ""; [0,20,40,60,80,100].forEach(v => c += `<line x1="${x0}" x2="${x1}" y1="${Y(v)}" y2="${Y(v)}" stroke="${v?"#F1E9DF":"#2A1A1F"}"/><text x="${x0-8}" y="${Y(v)+4}" text-anchor="end" font-size="10" fill="#6B5A5F">${v}</text>`);
    c += `<path d="${linePath(D.cumFore,x0,x1,y0,y1,0,vmax)} L${x1},${y1} L${x0},${y1} Z" fill="#7A1F3D" opacity=".14"/>
      <path d="${linePath(D.cumPlan,x0,x1,y0,y1,0,vmax)}" fill="none" stroke="#2A1A1F" stroke-width="1.5" stroke-dasharray="5 4"/>
      <path d="${linePath(D.cumFore,x0,x1,y0,y1,0,vmax)}" fill="none" stroke="#7A1F3D" stroke-width="3"/>
      <path d="${linePath(D.cumSpend,x0,x1,y0,y1,0,vmax)}" fill="none" stroke="#B8955A" stroke-width="3"/>`;
    const fi = D.breakeven.foreIdx; c += `<circle cx="${X(fi)}" cy="${Y(D.cumFore[fi])}" r="13" fill="#7A1F3D"/><text x="${X(fi)}" y="${Y(D.cumFore[fi])+4}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="12" fill="#E9D8B4">B/E</text><text x="${X(fi)+18}" y="${Y(D.cumFore[fi])+20}" font-size="11" font-weight="700" fill="#7A1F3D">break-even ${D.breakeven.fore}</text>`;
    D.cumMonths.forEach((m,i) => c += `<text x="${X(i)}" y="${y1+18}" text-anchor="middle" font-size="11" font-weight="600" fill="${i>D.actualTo?"#6B5A5F":"#2A1A1F"}">${m}</text><rect data-ref="month:${i}" data-nopen x="${X(i)-34}" y="${y0}" width="68" height="${y1-y0+24}" fill="transparent" style="cursor:help"/>`);
    c += `<g font-size="11" fill="#2A1A1F"><line x1="${x0}" x2="${x0+22}" y1="${CH-16}" y2="${CH-16}" stroke="#7A1F3D" stroke-width="3"/><text x="${x0+28}" y="${CH-12}">EBITDA back to date</text><line x1="${x0+170}" x2="${x0+192}" y1="${CH-16}" y2="${CH-16}" stroke="#B8955A" stroke-width="3"/><text x="${x0+198}" y="${CH-12}">Money out to date</text><line x1="${x0+330}" x2="${x0+352}" y1="${CH-16}" y2="${CH-16}" stroke="#2A1A1F" stroke-dasharray="5 4"/><text x="${x0+358}" y="${CH-12}">Plan · ₹ lakh · after Oct is forecast</text></g>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="EBITDA back to date against money out to date; break-even ${D.breakeven.fore}, plan ${D.breakeven.plan}.">${c}</svg>`;

    return `<div class="s15"><div class="wrap">
      <nav class="ribbons" aria-label="Suite sections">${D.tabs.map((t,i)=>`<button class="rb ${i?"":"on"}" type="button" data-tab="${t[0]}">${t[1]}${t[0]==="recovery"&&wait?` · ${wait}`:""}</button>`).join("")}</nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2><p>Checked every morning at 6 AM against what was expected for the day and ${esc(D.sinceLabel)} · data as of ${esc(D.asOf)}</p></div>
        <div class="ledger" aria-label="Pulse strip">${ledger}</div></div>
      <div class="seals" aria-label="Watch list and next go-live">${D.watch.map((w,i)=>`<button class="sl" type="button" data-ref="${w.ref}"><i aria-hidden="true">${i+1}</i><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}
        <button class="stub" type="button" data-ref="part:${D.milestone.part}"><b>${D.milestone.days}</b><span>days to the next go-live<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to see the whole picture →</p><div class="tree">${tree}</div>
        <div class="legend"><span><i style="background:#C2362F"></i>Pulling down</span><span><i style="background:#2F7D4F"></i>Lifting</span><span><i style="background:#2F7D4F;height:10px;width:10px;border-radius:2px"></i>On track</span><span><i style="background:#D9940A;height:10px;width:10px;border-radius:2px"></i>Slightly behind</span><span><i style="background:#C2362F;height:10px;width:10px;border-radius:2px"></i>Off track</span><span>· Feeds: live, testing, being built, late, not started</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3>${fhChooser("pick")}</div><div class="book">${book}</div></section>
      <section class="zone" data-zone="recovery"><div class="zh"><h3>Recovery</h3><p>What the suite did on its own, what it advised, and what needs the CEO</p></div>
        <div class="runlog" aria-label="This morning's run">${D.runLog.map(r=>`<div><b>${r[0]}</b>${esc(r[1])}</div>`).join("")}</div><div class="rec">${rec}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="cheques">${D.people.map(cq).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="mny"><div class="chart">${chart}</div>
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
  after(){ const tr = document.querySelector(".s15 .tree"); if (tr) tr.scrollLeft = (tr.scrollWidth - tr.clientWidth)/2; if (matchMedia("(prefers-reduced-motion: reduce)").matches) document.querySelectorAll(".s15 .flow").forEach(p=>p.classList.remove("flow")); }
});
