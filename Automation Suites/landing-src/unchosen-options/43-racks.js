/* ===== Procurement, option 1: rust and steel, the store racks ===== */
SCHEMES.push({
  key:"racks", letter:"1", name:"Rust and steel",
  note:"<b>Option 1 · rust and steel.</b> The suite as three bays of store racks: buying, the store, and the wards. Each part is a carton on the shelf, stamped with where it stands. Supplies come in at the left and go out to the wards at the right.",
  vars:{ "--sh-bg":"#FFFFFF","--sh-fg":"#23272B","--sh-mute":"#5B6168","--sh-line":"#DDD7CF","--sh-card":"#F7F4F0","--c-ok":"#2E7D4F","--c-warn":"#A86B05","--c-bad":"#C0392B","--pk-bg":"#23272B","--pk-fg":"#FFFFFF","--pk-line":"#B4532A","--pk-r":"4px","--sh-r":"6px" },
  fab:18,
  blocks:{ nav:".bins", pulse:".stags", watch:".shorts", countdown:".docket", hero:".racks", kpis:".tags", team:".picks", money:".gapc" },
  css:`
.s13{--bg:#ECE8E2;--ink:#23272B;--mute:#5B6168;--rust:#B4532A;--rust2:#F4DDD1;--steel:#4F6D86;--steel2:#DCE5EC;--ok:#2E7D4F;--warn:#A86B05;--bad:#C0392B;--line:#D6CFC6;
  background:var(--bg);background-image:radial-gradient(rgba(35,39,43,.05) 1px,transparent 1.2px);background-size:7px 7px;color:var(--ink);padding:18px 16px 90px;overflow-x:clip}
.s13 .wrap{max-width:1240px;margin:0 auto}
.s13 .bins{display:flex;flex-wrap:wrap;gap:8px;padding:10px;background:var(--steel);border-radius:4px;box-shadow:inset 0 -4px 0 rgba(0,0,0,.18)}
.s13 .bn{display:flex;align-items:center;gap:8px;background:#FBFAF7;border:0;border-radius:2px;padding:8px 12px 8px 8px;font-size:12.5px;font-weight:600;color:var(--ink);min-height:44px;box-shadow:0 2px 0 rgba(0,0,0,.2)}
.s13 .bn i{width:16px;height:24px;background:repeating-linear-gradient(90deg,var(--ink) 0 1px,transparent 1px 3px,var(--ink) 3px 5px,transparent 5px 6px)}
.s13 .bn:hover{background:#fff;transform:translateY(-1px)}
.s13 .bn.on{background:var(--rust);color:#fff} .s13 .bn.on i{background:repeating-linear-gradient(90deg,#fff 0 1px,transparent 1px 3px,#fff 3px 5px,transparent 5px 6px)}
.s13 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:24px 0 16px}
.s13 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--rust)}
.s13 h2{font-family:var(--f-num);font-weight:400;font-size:76px;line-height:.88;margin:4px 0 0;letter-spacing:.02em}
.s13 h2::after{content:"";display:block;height:8px;width:180px;margin-top:8px;background:repeating-linear-gradient(-45deg,var(--rust) 0 10px,var(--ink) 10px 20px)}
.s13 .stags{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}
.s13 .st{position:relative;background:#FFFDF8;border:0;border-top:5px solid var(--c);padding:8px 12px 8px;text-align:left;color:inherit;min-width:140px;box-shadow:0 3px 0 rgba(35,39,43,.15);border-radius:0 0 3px 3px}
.s13 .st span{display:block;font-size:10.5px;letter-spacing:.12em;font-weight:700;color:var(--mute)}
.s13 .st b{display:block;font-family:var(--f-num);font-weight:400;font-size:30px;line-height:1}
.s13 .st em{display:block;font-style:normal;font-size:11px;color:var(--rust)}
.s13 .st::after{content:"";position:absolute;right:10px;bottom:10px;width:26px;height:14px;background:repeating-linear-gradient(90deg,var(--ink) 0 1px,transparent 1px 2px,var(--ink) 2px 4px,transparent 4px 5px);opacity:.5}
.s13 .shorts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,.8fr);gap:12px;margin-bottom:16px;align-items:stretch}
.s13 .sh{display:grid;grid-template-columns:12px minmax(0,1fr);gap:12px;align-items:center;background:#fff;border:0;border-radius:3px;padding:10px 12px 10px 0;text-align:left;color:inherit;font-size:12.5px;font-weight:600;box-shadow:0 2px 0 rgba(35,39,43,.12);overflow:hidden}
.s13 .sh i{align-self:stretch;margin:-10px 0;background:repeating-linear-gradient(-45deg,#F2B705 0 6px,var(--ink) 6px 12px)}
.s13 .sh small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s13 .sh:hover{box-shadow:0 0 0 2px var(--rust)}
.s13 .docket{position:relative;background:#FFFDF8;border:0;padding:12px 14px 18px;text-align:left;color:var(--ink);box-shadow:0 3px 0 rgba(35,39,43,.15);
  -webkit-mask:conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) 50%/12px 100%;mask:conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) 50%/12px 100%}
.s13 .docket span.k{display:block;font-size:10px;font-weight:700;letter-spacing:.14em;color:var(--mute);border-bottom:1px dashed var(--line);padding-bottom:4px;margin-bottom:4px}
.s13 .docket b{font-family:var(--f-num);font-weight:400;font-size:42px;line-height:.9;color:var(--rust)}
.s13 .docket span.w{display:block;font-size:12px;font-weight:700} .s13 .docket small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s13 .racks{border-radius:6px;background:#F7F4EF;border:2px solid var(--ink);overflow-x:auto;box-shadow:6px 6px 0 rgba(35,39,43,.12)}
.s13 .racks svg{display:block;width:100%;min-width:960px;height:auto}
.s13 .swipe{display:none;margin:0 0 6px;font-size:12px;color:var(--rust)}
.s13 .pc{cursor:pointer}
.s13 .pc:focus{outline:none} .s13 .pc:focus .fr{stroke:#F2B705;stroke-width:3}
.s13 .pc:hover .fr{stroke:var(--rust);stroke-width:2.5}
.s13 .pc{transition:transform .2s} .s13 .pc:hover{transform:translateY(-4px)}
.s13 .pc.ping .fr{animation:s13ping 1s ease}
@keyframes s13ping{0%{fill:#FFE7A8}100%{}}
.s13 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;font-size:12px;color:var(--mute);margin-top:10px}
.s13 .legend i{display:inline-block;width:14px;height:12px;border-radius:2px;vertical-align:-1px;margin-right:6px}
.s13 .zone{margin-top:42px;scroll-margin-top:20px;border-radius:6px}
.s13 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px 16px;margin-bottom:16px;padding:8px 12px;background:var(--ink);color:#fff;border-radius:3px}
.s13 .zh h3{font-family:var(--f-num);font-weight:400;font-size:34px;margin:0;line-height:1;letter-spacing:.03em}
.s13 .zh p{margin:0;font-size:12.5px;color:#C9CED3}
.s13 .tags{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px 16px}
.s13 .tg{position:relative;display:block;background:#FFFDF8;border:0;padding:12px 14px 12px 30px;text-align:left;color:inherit;
  clip-path:polygon(18px 0,100% 0,100% 100%,18px 100%,0 50%);filter:drop-shadow(0 2px 0 rgba(35,39,43,.18));transition:transform .15s}
.s13 .tg::before{content:"";position:absolute;left:10px;top:50%;width:9px;height:9px;margin-top:-4.5px;border-radius:50%;background:var(--bg);box-shadow:inset 0 0 0 2px var(--steel)}
.s13 .tg:hover,.s13 .tg:focus-visible{transform:rotate(-1deg) translateY(-2px)}
.s13 .tg .nm{display:block;font-size:12.5px;font-weight:600;line-height:1.3;padding-right:56px}
.s13 .tg .pr{position:absolute;right:12px;top:10px;font-family:var(--f-num);font-size:12px;letter-spacing:.06em;color:#fff;padding:1px 6px;border-radius:2px}
.s13 .tg b{display:block;font-family:var(--f-num);font-weight:400;font-size:34px;line-height:1;margin-top:6px}
.s13 .tg .sw{display:block;font-size:11px;font-weight:700;letter-spacing:.04em;margin-top:2px}
.s13 .rng{position:relative;display:block;height:10px;margin:10px 0 4px;background:repeating-linear-gradient(90deg,#E7E1D8 0 6px,#F0EBE3 6px 8px);border-radius:1px}
.s13 .rng i{position:absolute;left:0;top:0;bottom:0;background:var(--c)}
.s13 .rng u{position:absolute;top:-4px;bottom:-4px;width:3px;margin-left:-1.5px;background:var(--ink)}
.s13 .tg .rg{display:flex;justify-content:space-between;font-size:10.5px;color:var(--mute)}
.s13 .ahead{color:var(--ok)} .s13 .watch{color:var(--warn)} .s13 .off{color:var(--bad)}
.s13 .picks{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.s13 .pk{position:relative;background:#FFFDF8;border:0;padding:16px 12px 12px;text-align:left;color:inherit;display:flex;flex-direction:column;gap:8px;box-shadow:0 3px 0 rgba(35,39,43,.14);transition:transform .15s}
.s13 .pk::before{content:"";position:absolute;left:0;right:0;top:0;height:6px;background:radial-gradient(circle at 5px 0,var(--bg) 3px,transparent 3.5px) 0 0/10px 6px repeat-x}
.s13 .pk:hover,.s13 .pk:focus-visible{transform:translateY(-3px);box-shadow:0 3px 0 rgba(35,39,43,.14),0 0 0 2px var(--rust)}
.s13 .pk .top{display:flex;justify-content:space-between;gap:8px;align-items:flex-start;border-bottom:2px solid var(--ink);padding-bottom:6px}
.s13 .pk .nm{font-weight:700;font-size:13.5px;line-height:1.2} .s13 .pk .nm small{display:block;font-weight:400;font-size:11.5px;color:var(--mute)}
.s13 .pk .chip{font-size:10px;font-weight:700;letter-spacing:.06em;padding:3px 7px;border:2px solid currentColor;border-radius:2px;white-space:nowrap;transform:rotate(-4deg)}
.s13 .bc{display:flex;align-items:flex-end;gap:3px;height:34px}
.s13 .bc i{flex:1;height:100%;background:#E3DDD3} .s13 .bc i.y{background:var(--ink)} .s13 .bc i.l{background:var(--bad);height:70%}
.s13 .pk .meta{font-size:12px} .s13 .pk .meta b{font-family:var(--f-num);font-weight:400;font-size:18px}
.s13 .pk .imp{font-size:11.5px;color:var(--bad);line-height:1.35} .s13 .pk .nx{font-size:11.5px;color:var(--mute)}
.s13 .pk ul{list-style:none;margin:0;padding:0;font-size:12px;display:grid;gap:4px}
.s13 .pk li{display:grid;grid-template-columns:16px minmax(0,1fr);gap:4px}
.s13 .pk li::before{content:"";width:11px;height:11px;margin-top:2px;border:1.5px solid var(--mute)}
.s13 .pk li.y::before{background:var(--ink);border-color:var(--ink);box-shadow:inset 0 0 0 2px #FFFDF8} .s13 .pk li.l{color:var(--bad);font-weight:600} .s13 .pk li.l::before{border-color:var(--bad);background:var(--rust2)}
.s13 .vt{display:inline-flex;border:2px solid #fff;border-radius:2px;overflow:hidden}
.s13 .vt button{border:0;background:transparent;padding:6px 14px;font-size:12px;font-weight:600;min-height:36px;color:#fff}
.s13 .vt button[aria-pressed="true"]{background:#fff;color:var(--ink)}
.s13 .gapc{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:20px;align-items:start}
.s13 .chart{background:#FFFDF8;border:2px solid var(--ink);border-radius:4px;padding:12px;overflow-x:auto}
.s13 .chart svg{display:block;width:100%;min-width:560px;height:auto}
.s13 .mlist{display:grid;gap:8px}
.s13 .mlist button{display:flex;justify-content:space-between;gap:12px;align-items:baseline;background:#FFFDF8;border:0;border-left:6px solid var(--steel);border-radius:2px;padding:10px 12px;text-align:left;color:var(--mute);font-size:12.5px;box-shadow:0 2px 0 rgba(35,39,43,.12)}
.s13 .mlist b{font-family:var(--f-num);font-weight:400;font-size:24px;color:var(--ink);white-space:nowrap}
.s13 .mlist .why{background:var(--rust);border-left-color:var(--ink);color:#FBE6DC} .s13 .mlist .why b{color:#fff}
@media (max-width:1000px){ .s13 .head{grid-template-columns:1fr} .s13 .stags{justify-content:flex-start} .s13 .shorts{grid-template-columns:1fr 1fr} .s13 .tags,.s13 .picks{grid-template-columns:1fr 1fr} .s13 .gapc{grid-template-columns:1fr} }
@media (max-width:600px){ .s13 .swipe{display:block} .s13 h2{font-size:54px} .s13 .shorts,.s13 .tags,.s13 .picks{grid-template-columns:1fr} .s13 .st{flex:1 1 150px} .s13 .bn{padding:6px 10px 6px 6px;font-size:12px} }
`,
  render(){
    const SC = { live:"#2E7D4F", testing:"#D9940A", building:"#7D8A96", blocked:"#C0392B", notstarted:"#A7A097" };
    const live = countParts("live"), M = D.month, P_ = id => D.parts.find(p=>p.id===id);
    const st = (c, lab, val, sub, attr) => `<button class="st" type="button" ${attr} style="--c:${c}"><span>${lab}</span><b>${val}</b><em>${sub}</em></button>`;
    const stags = st("#2E7D4F","PARTS LIVE",`${live} / 12`,"plan 4",`data-tab="links"`) + st("#D9940A","KPIS ON COURSE",`${onCourse} / 9`,"plan 8",`data-tab="measures"`)
      + st("#4F6D86","EBITDA BACK / OUT",`${ebitdaTotal.toFixed(1)} / ${spendTotal.toFixed(1)}`,`₹ lakh · plan ${D.cumPlan[D.actualTo].toFixed(1)} back`,`data-ref="health:0"`) + st("#C0392B","BREAK-EVEN",D.breakeven.fore.toUpperCase(),`plan ${D.breakeven.plan}`,`data-ref="health:0"`);

    /* --- a carton on a pallet, drawn in three faces --- */
    const BW = 96, BH = 92, DX = 14, DY = -10;
    const box = (p, x, y) => { const s = p.st, empty = s==="building"||s==="notstarted";
      const F = { live:["#D7B68A","#E7CCA6","#B9966A"], testing:["#D7B68A","#E7CCA6","#B9966A"], blocked:["#D7B68A","#E7CCA6","#B9966A"], building:["#EEF2F5","#F6F8FA","#D8E0E7"], notstarted:["#F7F4EF","#F7F4EF","#EFEAE3"] }[s];
      let g = `<g class="pc" data-ref="part:${p.id}" data-part="${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[s]}">`;
      g += `<rect x="${x-4}" y="${y+BH}" width="${BW+8}" height="6" fill="#A0784C"/><rect x="${x+4}" y="${y+BH+6}" width="10" height="4" fill="#7E5C38"/><rect x="${x+BW/2-5}" y="${y+BH+6}" width="10" height="4" fill="#7E5C38"/><rect x="${x+BW-14}" y="${y+BH+6}" width="10" height="4" fill="#7E5C38"/>`;
      const dash = empty ? `stroke-dasharray="5 3"` : "";
      g += `<polygon points="${x},${y} ${x+DX},${y+DY} ${x+BW+DX},${y+DY} ${x+BW},${y}" fill="${F[1]}" stroke="#23272B" stroke-width="1.2" ${dash}/>`;
      g += `<polygon points="${x+BW},${y} ${x+BW+DX},${y+DY} ${x+BW+DX},${y+BH+DY} ${x+BW},${y+BH}" fill="${F[2]}" stroke="#23272B" stroke-width="1.2" ${dash}/>`;
      g += `<rect class="fr" x="${x}" y="${y}" width="${BW}" height="${BH}" fill="${F[0]}" stroke="#23272B" stroke-width="1.2" ${dash}/>`;
      if (s==="testing") g += `<rect x="${x+BW/2-7}" y="${y}" width="14" height="5" fill="#E9B949"/><polygon points="${x+BW/2-7},${y} ${x+BW/2-7+DX},${y+DY} ${x+BW/2+7+DX},${y+DY} ${x+BW/2+7},${y}" fill="#F2CB66"/>`;
      if (s==="blocked") g += `<rect x="${x}" y="${y}" width="${BW}" height="${BH}" fill="none" stroke="#C0392B" stroke-width="3"/><path d="M${x+BW+2},${y-1} L${x+BW+DX-2},${y+BH+DY-6} M${x+BW+DX-2},${y+DY+2} L${x+BW+2},${y+BH-6}" stroke="#C0392B" stroke-width="4"/><polygon points="${x+18},${y} ${x+18+DX},${y+DY} ${x+30+DX},${y+DY} ${x+30},${y}" fill="#C0392B"/><polygon points="${x+BW-30},${y} ${x+BW-30+DX},${y+DY} ${x+BW-18+DX},${y+DY} ${x+BW-18},${y}" fill="#C0392B"/>`;
      const tc = empty ? "#5B6168" : "#23272B";
      g += `<foreignObject x="${x+5}" y="${y+4}" width="${BW-10}" height="${BH-26}"><div xmlns="http://www.w3.org/1999/xhtml" style="font:600 9.5px/1.18 Poppins,sans-serif;color:${tc}"><b style="font-family:'Bebas Neue';font-weight:400;font-size:17px;line-height:1;color:#B4532A;display:block">${String(p.id).padStart(2,"0")}</b>${esc(p.name)}</div></foreignObject>`;
      g += `<rect x="${x+5}" y="${y+BH-19}" width="${BW-10}" height="15" rx="2" fill="${empty?"none":"#FFFDF8"}" stroke="${SC[s]}" stroke-width="1.6" ${empty?'stroke-dasharray="3 2"':""}/><text x="${x+BW/2}" y="${y+BH-8}" text-anchor="middle" font-size="9" font-weight="700" letter-spacing=".6" fill="${SC[s]}">${PART_WORD[s].toUpperCase()}</text>`;
      return g + `</g>`; };

    const W = 1100, H = 560; let g = `<defs><pattern id="s13floor" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#E4DED5"/><path d="M0,0 L40,0 M0,0 L0,40" stroke="#D6CFC4" stroke-width="1"/></pattern></defs>`;
    /* top strip: bought today */
    g += `<rect x="0" y="0" width="${W}" height="60" fill="#23272B"/>
      <text x="24" y="24" font-size="10" font-weight="700" letter-spacing="1.4" fill="#C9CED3">BOUGHT TODAY</text><text id="s13amt" x="24" y="50" font-family="Bebas Neue, sans-serif" font-size="26" fill="#FFFFFF">₹${M.boughtToday.toFixed(2)} L</text>
      <text x="170" y="24" font-size="10" font-weight="700" letter-spacing="1.4" fill="#C9CED3">ABOVE THE AGREED PRICE</text><text id="s13above" x="170" y="50" font-family="Bebas Neue, sans-serif" font-size="26" fill="#F4A07B">₹${M.aboveToday.toFixed(2)} L above price</text>
      <text x="420" y="24" font-size="10" font-weight="700" letter-spacing="1.4" fill="#C9CED3">THIS MONTH</text><text x="420" y="50" font-family="Bebas Neue, sans-serif" font-size="26" fill="#FFFFFF">₹${M.bought} CR BOUGHT · ₹${M.lost} L LOST</text>
      <text id="s13last" x="${W-24}" y="38" text-anchor="end" font-size="11" fill="#E7CCA6">last: ${esc(M.last)}</text>`;
    /* floor */
    const FY = 408; g += `<polygon points="0,${FY} ${W},${FY} ${W},${H} 0,${H}" fill="url(#s13floor)"/><line x1="0" x2="${W}" y1="${FY}" y2="${FY}" stroke="#23272B" stroke-width="2"/>`;
    g += `<path id="s13lane" d="M20,${FY+46} L${W-20},${FY+46}" stroke="#E9B949" stroke-width="3" stroke-dasharray="18 10" fill="none"/>`;
    /* racks */
    const bays = [["A","BUYING","buying",[1,2,3,12,10]],["B","THE STORE","stores",[4,7,9,5]],["C","THE WARDS","wards",[6,8,11]]];
    bays.forEach(([L_,name,bay,ids],bi) => { const bx = 80 + bi*340, bw = 330, top = 120, b1 = 262, b2 = FY - 6;
      const n = ids.length, nl = ids.filter(id=>P_(id).st==="live").length;
      g += `<rect x="${bx+bw/2-80}" y="74" width="160" height="34" rx="2" fill="#FFFDF8" stroke="#23272B" stroke-width="1.5"/><line x1="${bx+bw/2-50}" x2="${bx+bw/2-50}" y1="${top}" y2="108" stroke="#5B6168"/><line x1="${bx+bw/2+50}" x2="${bx+bw/2+50}" y1="${top}" y2="108" stroke="#5B6168"/>
        <text x="${bx+bw/2-70}" y="99" font-family="Bebas Neue, sans-serif" font-size="22" fill="#B4532A">${L_}</text><text x="${bx+bw/2-54}" y="91" font-size="10.5" font-weight="700" letter-spacing="1" fill="#23272B">${name}</text><text x="${bx+bw/2-54}" y="103" font-size="9.5" fill="#5B6168">${nl} of ${n} parts live</text>`;
      /* uprights + beams (beams in front of nothing; boxes drawn after) */
      [bx, bx+bw].forEach(x => g += `<rect x="${x-5}" y="${top}" width="10" height="${FY-top}" fill="#4F6D86"/><g fill="#3B5468">${Array.from({length:12},(_,k)=>`<rect x="${x-2}" y="${top+8+k*23}" width="4" height="8"/>`).join("")}</g>`);
      [top+4, b1, b2].forEach(y => g += `<rect x="${bx-5}" y="${y}" width="${bw+10}" height="9" fill="#C0602F"/><rect x="${bx-5}" y="${y+9}" width="${bw+10}" height="3" fill="#8F4220"/>`);
      ids.forEach((id,i) => { const lvl = i < 3 ? 0 : 1, col = i < 3 ? i : i - 3; const x = bx + 12 + col*106, y = (lvl ? b2 : b1) - 10 - BH; g += box(P_(id), x, y); });
      if (n < 6) g += `<text x="${bx + 12 + (n-3)*106 + 50}" y="${b2-50}" text-anchor="middle" font-size="10" fill="#9A938A" font-style="italic">${n===5?"":"room for more"}</text>`;
    });
    /* moving pallet trucks */
    const truck = (dur, begin, label) => `<g><rect x="-24" y="-14" width="34" height="20" rx="2" fill="#D7B68A" stroke="#23272B"/><rect x="10" y="-4" width="16" height="10" rx="2" fill="#B4532A"/><circle cx="-16" cy="8" r="3.5" fill="#23272B"/><circle cx="18" cy="8" r="3.5" fill="#23272B"/><animateMotion dur="${dur}s" begin="${begin}s" repeatCount="indefinite" path="M20,${FY+44} L${W-20},${FY+44}"/></g>`;
    g += truck(16, 0) + truck(16, -6) + truck(16, -11);
    g += `<text x="24" y="${FY+24}" font-size="10.5" font-weight="700" letter-spacing="1.2" fill="#23272B">IN ▸ 41 SUPPLIERS · ABOUT 90 BILLS A DAY</text><text x="${W-24}" y="${FY+24}" text-anchor="end" font-size="10.5" font-weight="700" letter-spacing="1.2" fill="#23272B">OUT ▸ 9 WARDS · THEATRES · ICU</text>`;
    /* handoffs */
    D.handoffs.forEach((h,i) => { const x = 24 + i*540, y = FY + 78; const c = SC[h.st];
      g += `<rect x="${x}" y="${y}" width="520" height="44" rx="2" fill="#FFFDF8" stroke="#23272B"/><rect x="${x}" y="${y}" width="8" height="44" fill="${c}"/>
        <text x="${x+20}" y="${y+18}" font-size="10" font-weight="700" letter-spacing="1" fill="#5B6168">${i?"FROM":"SHARED WITH"} THE ${esc(h.to.toUpperCase())} SUITE</text>
        <text x="${x+20}" y="${y+35}" font-size="12" font-weight="600" fill="#23272B">${esc(h.name)} · <tspan fill="${c}" font-weight="700">${PART_WORD[h.st]}</tspan> · ${esc(h.when)}</text>`; });
    const racks = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Three bays of racks: buying, the store and the wards, with each part as a carton marked live, testing, being built, late or not started.">${g}</svg>`;

    /* --- KPI price tags --- */
    const tg = k => { const col = k.state==="ahead"?"#2E7D4F":k.state==="watch"?"#D9940A":"#C0392B"; const n = Math.min(100,prog(k,k.now)*100), pl = Math.min(100,prog(k,k.plan)*100);
      return `<button class="tg" type="button" data-ref="kpi:${k.id}"><span class="nm">${esc(k.name)}</span><span class="pr" style="background:${col}">${k.id}</span>
        <b class="${k.state}">${fmtv(k,k.now)}</b><span class="sw ${k.state}">${STATE_WORD[k.state].toUpperCase()} · ${gapText(k)}</span>
        <span class="rng" style="--c:${col}" aria-hidden="true"><i style="width:${n.toFixed(0)}%"></i><u style="left:${pl.toFixed(0)}%"></u></span>
        <span class="rg"><span>Start ${fmtv(k,k.base)}</span><span>Plan ${fmtv(k,k.plan)}</span><span>Target ${fmtv(k,k.target)}</span></span></button>`; };

    /* --- picking lists --- */
    const pk = p => { const cc = p.state==="ahead"?"#2E7D4F":p.state==="watch"?"#A86B05":"#C0392B"; let body;
      if (UI.view==="day") body = `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}"><span>${esc(t[0])}${t[1]!==1?` · <span style="font-weight:400">${esc(t[1])}</span>`:""}</span></li>`).join("")}</ul>`;
      else { const b = []; for (let i=0;i<p.due;i++) b.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":""}"></i>`); body = `<span class="bc" aria-label="${p.done} of ${p.due} done, ${p.late} late">${b.join("")}</span><span class="meta"><b>${p.done}</b> of ${p.due} done${p.late?` · <b style="color:var(--bad)">${p.late}</b> late`:""}</span>`; }
      return `<button class="pk" type="button" data-ref="per:${p.key}"><span class="top"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="chip" style="color:${cc}">${PERSON_WORD[p.state].toUpperCase()}</span></span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</button>`; };

    /* --- money: out and back to date, gap shaded --- */
    const CW = 760, CH = 320, x0 = 50, x1 = 740, y0 = 20, y1 = 260, n = D.cumMonths.length, vmax = 70;
    const X = i => x0 + (x1-x0)*i/(n-1), Y = v => y1 - (y1-y0)*v/vmax;
    let c = ""; [0,10,20,30,40,50,60,70].forEach(v => c += `<line x1="${x0}" x2="${x1}" y1="${Y(v)}" y2="${Y(v)}" stroke="${v?"#EEE8E0":"#23272B"}"/><text x="${x0-8}" y="${Y(v)+4}" text-anchor="end" font-size="10" fill="#5B6168">${v}</text>`);
    /* crossing point */
    let xi = n-1; for (let i=1;i<n;i++){ if (D.cumFore[i] >= D.cumSpend[i] && D.cumFore[i-1] < D.cumSpend[i-1]) { const a = D.cumSpend[i-1]-D.cumFore[i-1], b = D.cumFore[i]-D.cumSpend[i]; xi = i-1 + a/(a+b); break; } }
    const xb = x0 + (x1-x0)*xi/(n-1);
    const area = D.cumFore.map((v,i)=>`${X(i)},${Y(v)}`).join(" ") + " " + D.cumSpend.map((v,i)=>`${X(i)},${Y(v)}`).reverse().join(" ");
    c += `<defs><clipPath id="s13l"><rect x="0" y="0" width="${xb}" height="${CH}"/></clipPath><clipPath id="s13r"><rect x="${xb}" y="0" width="${CW}" height="${CH}"/></clipPath></defs>
      <polygon points="${area}" fill="#C0392B" opacity=".18" clip-path="url(#s13l)"/><polygon points="${area}" fill="#2E7D4F" opacity=".18" clip-path="url(#s13r)"/>
      <rect x="${X(D.actualTo)}" y="${y0}" width="${x1-X(D.actualTo)}" height="${y1-y0}" fill="#F7F4EF" opacity=".5"/>
      <path d="${linePath(D.cumPlan,x0,x1,y0,y1,0,vmax)}" fill="none" stroke="#23272B" stroke-width="1.6" stroke-dasharray="6 4"/>
      <path d="${linePath(D.cumSpend,x0,x1,y0,y1,0,vmax)}" fill="none" stroke="#4F6D86" stroke-width="3"/>
      <path d="${linePath(D.cumFore,x0,x1,y0,y1,0,vmax)}" fill="none" stroke="#B4532A" stroke-width="3.5"/>
      ${D.cumFore.map((v,i)=>`<circle cx="${X(i)}" cy="${Y(v)}" r="4" fill="${i<=D.actualTo?"#B4532A":"#FFFDF8"}" stroke="#B4532A" stroke-width="2"/>`).join("")}
      <line x1="${xb}" x2="${xb}" y1="${y0}" y2="${y1}" stroke="#2E7D4F" stroke-width="2" stroke-dasharray="3 3"/><rect x="${xb-42}" y="${y0}" width="84" height="18" rx="2" fill="#2E7D4F"/><text x="${xb}" y="${y0+13}" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">BREAK-EVEN</text>
      <text x="${X(D.breakeven.planIdx)-8}" y="${Y(D.cumPlan[D.breakeven.planIdx])-12}" text-anchor="end" font-size="10" fill="#23272B">plan: ${D.breakeven.plan}</text>`;
    D.cumMonths.forEach((m,i) => c += `<text x="${X(i)}" y="${y1+18}" text-anchor="middle" font-size="11" font-weight="600" fill="${i>D.actualTo?"#5B6168":"#23272B"}">${m}</text><rect data-ref="month:${i}" data-nopen x="${X(i)-34}" y="${y0}" width="68" height="${y1-y0+24}" fill="transparent" style="cursor:help"/>`);
    c += `<g font-size="11" fill="#23272B"><line x1="${x0}" x2="${x0+22}" y1="${CH-16}" y2="${CH-16}" stroke="#B4532A" stroke-width="3.5"/><text x="${x0+28}" y="${CH-12}">EBITDA back to date</text>
      <line x1="${x0+170}" x2="${x0+192}" y1="${CH-16}" y2="${CH-16}" stroke="#4F6D86" stroke-width="3"/><text x="${x0+198}" y="${CH-12}">Money out to date</text>
      <line x1="${x0+330}" x2="${x0+352}" y1="${CH-16}" y2="${CH-16}" stroke="#23272B" stroke-dasharray="6 4"/><text x="${x0+358}" y="${CH-12}">Plan · ₹ lakh · after Oct is forecast</text></g>`;
    const chart = `<svg viewBox="0 0 ${CW} ${CH}" role="img" aria-label="Money out and EBITDA back to date, by month; they cross in ${D.breakeven.fore} against a plan of ${D.breakeven.plan}.">${c}</svg>`;

    return `<div class="s13"><div class="wrap">
      <nav class="bins" aria-label="Suite sections">${TABS.map((t,i)=>`<button class="bn ${i?"":"on"}" type="button" data-tab="${t[0]}"><i aria-hidden="true"></i>${t[1]}</button>`).join("")}</nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="stags" aria-label="Pulse strip">${stags}</div></div>
      <div class="shorts" aria-label="Watch list and next go-live">${D.watch.map(w=>`<button class="sh" type="button" data-ref="${w.ref}"><i aria-hidden="true"></i><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}
        <button class="docket" type="button" data-ref="part:${D.milestone.part}"><span class="k">NEXT GO-LIVE · ${D.milestone.date.toUpperCase()}</span><b>${D.milestone.days} DAYS</b><span class="w">${esc(D.milestone.what)}</span></button></div>
      <section class="zone" data-zone="links" style="margin-top:0"><p class="swipe">Swipe sideways to see every bay →</p><div class="racks">${racks}</div>
        <div class="legend"><span><i style="background:#2E7D4F"></i>Live</span><span><i style="background:#E9B949"></i>Testing</span><span><i style="background:#EEF2F5;border:1px dashed #7D8A96"></i>Being built</span><span><i style="background:#C0392B"></i>Late</span><span><i style="background:#F7F4EF;border:1px dashed #A7A097"></i>Not started</span><span>· Data as of ${esc(D.asOf)}</span></div></section>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs</h3><p>Bar: start to target · black tick: this week's plan</p></div><div class="tags">${D.kpis.map(tg).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards</h3>${viewToggle("vt")}</div><div class="picks">${D.people.map(pk).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status</h3><p>₹ lakh to date, by month</p></div>
        <div class="gapc"><div class="chart">${chart}</div>
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
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { document.querySelectorAll(".s13 animateMotion").forEach(a=>a.remove()); return; }
    buyTicker("s13", ".s13 .pc");
  }
});
