/* ===== Scheme E: the dispensary ===== */
SCHEMES.push({
  key:"dispensary", letter:"E", name:"The dispensary",
  note:"<b>E · The dispensary.</b> The suite is a course of treatment. The prescription label carries the pulse readings, refill date and warnings; the twelve links are drip bags feeding one chamber; KPIs are bottles filled toward the line; each person has a pill organiser; and money is two blister packs that meet at break-even. Sections are capsules.",
  vars:{ "--sh-bg":"#FBFAFE","--sh-fg":"#231B3A","--sh-mute":"#5F5873","--sh-line":"#E1DCEE","--sh-card":"#FFFFFF","--c-ok":"#18825A","--c-warn":"#B06D05","--c-bad":"#C93C31","--pk-bg":"#FFFFFF","--pk-fg":"#231B3A","--pk-line":"#5B3FD0","--pk-r":"16px","--sh-r":"28px" },
  fab:18,
  css:`
.s5{--wall:#EFEDF6;--ink:#231B3A;--mute:#5F5873;--vio:#5B3FD0;--vio2:#8C7AE6;--ok:#18825A;--okf:#3CC48B;--warn:#B06D05;--warnf:#F0A732;--bad:#C93C31;--badf:#EE6A5E;--glass:#FFFFFF;
  background:var(--wall);color:var(--ink);padding:20px 16px 90px;
  background-image:linear-gradient(#E6E3F0 1px,transparent 1px),linear-gradient(90deg,#E6E3F0 1px,transparent 1px);background-size:64px 32px}
.s5 .wrap{max-width:1240px;margin:0 auto}
.s5 .caps{display:flex;flex-wrap:wrap;gap:10px}
.s5 .cap{display:flex;align-items:stretch;border:0;padding:0;background:transparent;border-radius:999px;box-shadow:0 4px 0 rgba(35,27,58,.15);transition:transform .15s,box-shadow .15s;min-height:44px}
.s5 .cap i{width:30px;border-radius:999px 0 0 999px;background:var(--c)}
.s5 .cap span{background:#fff;border-radius:0 999px 999px 0;padding:10px 16px 10px 10px;font-size:13px;font-weight:600;border:1.5px solid var(--c);border-left:0;display:flex;align-items:center}
.s5 .cap:hover{transform:translateY(-2px) rotate(-1.5deg)}
.s5 .cap.on{transform:translateY(-3px);box-shadow:0 8px 0 rgba(35,27,58,.18)} .s5 .cap.on span{background:var(--c);color:#fff}
.s5 .hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);gap:26px;margin-top:22px;align-items:start}
.s5 .rx{background:#fff;border-radius:6px;box-shadow:0 18px 40px rgba(35,27,58,.14);overflow:hidden;transform:rotate(-.6deg)}
.s5 .rx .rh{display:flex;justify-content:space-between;align-items:center;background:var(--vio);color:#fff;padding:10px 16px}
.s5 .rx .rh b{font-family:var(--f-num);font-weight:400;font-size:44px;line-height:.9}
.s5 .rx .rh small{font-size:11px;letter-spacing:.14em;font-weight:600;text-align:right}
.s5 .rx .rb{padding:14px 16px;display:grid;gap:10px}
.s5 .rx h2{font-family:var(--f-num);font-weight:400;font-size:64px;line-height:.88;margin:0;letter-spacing:.01em}
.s5 .rx .meta{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;font-size:12px;border-top:1px dashed #CFC8E3;border-bottom:1px dashed #CFC8E3;padding:8px 0}
.s5 .rx .meta span{color:var(--mute)} .s5 .rx .meta b{display:block;color:var(--ink);font-size:13px}
.s5 .dose{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:10px;align-items:center;background:transparent;border:0;border-bottom:1px solid #EEEAF6;padding:6px 0;text-align:left;color:inherit;width:100%;min-height:44px}
.s5 .dose .pl{width:30px;height:14px;border-radius:7px;background:linear-gradient(90deg,var(--c) 50%,#fff 50%);border:1.5px solid var(--c)}
.s5 .dose span{font-size:13px}
.s5 .dose b{font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1}
.s5 .dose b small{font-family:var(--f-body);font-size:11px;color:var(--mute);margin-left:4px}
.s5 .refill{display:flex;gap:12px;align-items:center;background:#F3F0FE;border-radius:10px;padding:10px 12px;border:0;text-align:left;color:inherit;width:100%}
.s5 .refill b{font-family:var(--f-num);font-weight:400;font-size:42px;line-height:.9;color:var(--vio)}
.s5 .refill span{font-size:13px} .s5 .refill small{display:block;color:var(--mute);font-size:11.5px}
.s5 .warnbox{border:2px solid var(--bad);border-radius:10px;padding:8px 12px}
.s5 .warnbox > b{font-size:11px;letter-spacing:.14em;color:var(--bad)}
.s5 .warnbox button{display:block;width:100%;text-align:left;background:transparent;border:0;padding:5px 0;font-size:13px;color:var(--ink);min-height:36px}
.s5 .warnbox button::before{content:"⚠ ";color:var(--bad)}
.s5 .warnbox small{color:var(--mute)}
.s5 .hand{font-family:var(--f-hand);font-weight:700;font-size:24px;color:var(--vio);line-height:1}
.s5 .stand{background:linear-gradient(180deg,rgba(255,255,255,.65),rgba(255,255,255,.3));border:1px solid #DCD6EC;border-radius:24px;padding:14px;scroll-margin-top:20px}
.s5 .stand{overflow-x:auto}
.s5 .stand svg{width:100%;height:auto;display:block}
.s5 .bag{cursor:pointer}
.s5 .bag:focus{outline:none} .s5 .bag:focus rect.body{stroke:#F2B705;stroke-width:3}
.s5 .drop{animation:s5drop 1.6s ease-in infinite}
@keyframes s5drop{0%{transform:translateY(0);opacity:1}80%{opacity:1}100%{transform:translateY(14px);opacity:0}}
.s5 .flowl{animation:s5flow 1.4s linear infinite}
@keyframes s5flow{to{stroke-dashoffset:-20}}
.s5 .zone{margin-top:40px;scroll-margin-top:20px;border-radius:24px}
.s5 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:12px}
.s5 .zh h3{font-family:var(--f-num);font-weight:400;font-size:40px;margin:0;line-height:1}
.s5 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s5 .shelf{position:relative;display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:8px;padding:0 14px}
.s5 .shelf::after{content:"";position:absolute;left:0;right:0;bottom:-14px;height:18px;border-radius:4px;background:linear-gradient(180deg,#fff,#D9D3EA);box-shadow:0 10px 18px rgba(35,27,58,.14)}
.s5 .btl{background:transparent;border:0;padding:0;display:flex;flex-direction:column;align-items:center;gap:4px;color:inherit;position:relative;z-index:1;transition:transform .2s}
.s5 .btl:hover,.s5 .btl:focus-visible{transform:translateY(-6px) rotate(-2deg)}
.s5 .btl svg{width:100%;max-width:96px;height:auto}
.s5 .under{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:8px;padding:24px 14px 0;text-align:center}
.s5 .under button{background:transparent;border:0;color:inherit;padding:0;font-size:11.5px;font-weight:600;line-height:1.25}
.s5 .under small{display:block;font-weight:700;font-size:10.5px;letter-spacing:.04em;margin-top:2px}
.s5 .ahead{color:var(--ok)} .s5 .watch{color:var(--warn)} .s5 .off{color:var(--bad)}
.s5 .orgs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.s5 .org{background:#fff;border-radius:18px;padding:12px 14px;border:1.5px solid #E1DCEE;text-align:left;color:inherit;display:grid;gap:8px;box-shadow:0 5px 0 #E1DCEE;transition:transform .15s}
.s5 .org:hover,.s5 .org:focus-visible{transform:translateY(-3px)}
.s5 .org .hd{display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.s5 .org .nm{font-weight:700;font-size:14px} .s5 .org .nm small{font-weight:400;color:var(--mute);font-size:12px;margin-left:6px}
.s5 .org .tag{font-size:11px;font-weight:700;letter-spacing:.05em;border-radius:999px;padding:2px 9px;border:1.5px solid currentColor;white-space:nowrap}
.s5 .comp{display:flex;flex-wrap:wrap;gap:5px}
.s5 .comp i{width:34px;height:30px;border-radius:7px;background:#F4F2FA;border:1.5px solid #D4CDE6;display:grid;place-items:center;position:relative}
.s5 .comp i::after{content:"";width:18px;height:9px;border-radius:5px}
.s5 .comp i.y::after{background:linear-gradient(90deg,var(--vio) 50%,#C9BEF6 50%)}
.s5 .comp i.l{border-color:var(--bad)} .s5 .comp i.l::after{background:linear-gradient(90deg,var(--bad) 50%,#F6C3BE 50%);transform:rotate(25deg)}
.s5 .comp i.e::after{border:1.5px dashed #B6ADCF}
.s5 .tlist{display:grid;gap:5px;margin:0;padding:0;list-style:none;font-size:12.5px}
.s5 .tlist li{display:flex;gap:8px;align-items:center}
.s5 .tlist li::before{content:"";flex:0 0 22px;height:10px;border-radius:5px;border:1.5px dashed #B6ADCF}
.s5 .tlist li.y::before{background:linear-gradient(90deg,var(--vio) 50%,#C9BEF6 50%);border:0}
.s5 .tlist li.l{color:var(--bad);font-weight:600} .s5 .tlist li.l::before{background:linear-gradient(90deg,var(--bad) 50%,#F6C3BE 50%);border:0}
.s5 .org .imp{font-size:12px;color:var(--bad)} .s5 .org .nx{font-size:12px;color:var(--mute)}
.s5 .vt{display:inline-flex;background:#fff;border-radius:999px;padding:3px;border:1.5px solid #D4CDE6}
.s5 .vt button{border:0;background:transparent;border-radius:999px;padding:6px 14px;font-size:12.5px;font-weight:600;min-height:36px}
.s5 .vt button[aria-pressed="true"]{background:var(--vio);color:#fff}
.s5 .packs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr)) minmax(0,.9fr);gap:18px;align-items:start}
.s5 .pack{background:linear-gradient(135deg,#F6F5FA,#DCD8E8);border-radius:14px;padding:12px;box-shadow:inset 0 0 0 1px #C9C3DA,0 10px 20px rgba(35,27,58,.12)}
.s5 .pack h4{margin:0 0 8px;font-size:13px;display:flex;justify-content:space-between}
.s5 .pack h4 b{font-family:var(--f-num);font-weight:400;font-size:22px}
.s5 .bl{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:5px}
.s5 .bl i{aspect-ratio:1;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#E7E3F1 70%);box-shadow:inset 0 -2px 3px rgba(35,27,58,.15)}
.s5 .bl i.f{background:radial-gradient(circle at 35% 30%,#fff 0 12%,var(--c) 40%)}
.s5 .bl i.g{background:radial-gradient(circle at 35% 30%,#fff 0 12%,var(--c) 40%);opacity:.35}
.s5 .bl i.mk{outline:2.5px solid var(--bad);outline-offset:1px}
.s5 .key{display:flex;flex-wrap:wrap;gap:6px 12px;margin-top:8px;font-size:11.5px;color:var(--mute)}
.s5 .key span::before{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--c);margin-right:5px;vertical-align:-1px}
.s5 .verdict{display:grid;gap:10px}
.s5 .verdict button{background:#fff;border:1.5px solid #E1DCEE;border-radius:14px;padding:10px 12px;text-align:left;color:inherit;font-size:12.5px}
.s5 .verdict b{display:block;font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1.05}
.s5 .verdict .bad{border-color:var(--bad);color:var(--bad)}
@media (max-width:1000px){ .s5 .hero{grid-template-columns:1fr} .s5 .packs{grid-template-columns:1fr 1fr} .s5 .verdict{grid-column:1/-1;grid-template-columns:repeat(2,minmax(0,1fr))}
  .s5 .shelf,.s5 .under{grid-template-columns:repeat(5,minmax(0,1fr))} .s5 .shelf::after{display:none} .s5 .btl{border-bottom:10px solid #E7E2F2;padding-bottom:4px} .s5 .under{display:none} .s5 .btl .cap2{display:block} }
.s5 .btl .cap2{display:none;font-size:11px;font-weight:600;line-height:1.2;text-align:center}
.s5 .btl .cap2 small{display:block;font-size:10.5px;font-weight:700}
@media (max-width:600px){ .s5 .stand svg{min-width:640px} .s5 .btl svg{max-width:78px} .s5 .orgs{grid-template-columns:1fr} .s5 .packs{grid-template-columns:1fr} .s5 .verdict{grid-template-columns:1fr} .s5 .shelf{grid-template-columns:repeat(3,minmax(0,1fr))} .s5 .rx h2{font-size:48px} .s5 .rx .meta{grid-template-columns:1fr 1fr} .s5 .cap span{padding:8px 12px 8px 8px;font-size:12px} .s5 .cap i{width:22px} }
`,
  render(){
    const capCol = ["#5B3FD0","#2E8FD6","#E0702E","#18825A","#C93C31","#8C7AE6","#231B3A"];
    /* IV stand */
    const W = 760, bw = 82, gapx = (W - 40 - 6*bw)/5;
    const lvl = { live:1, testing:.6, building:.25, blocked:.25, notstarted:0 };
    const col = { live:"#3CC48B", testing:"#F0A732", building:"#B6ADCF", blocked:"#EE6A5E", notstarted:"#FFFFFF" };
    let bags = "", tubes = "";
    const cx = W/2, cy = 520;
    D.parts.forEach((x,i) => { const r = Math.floor(i/6), c = i%6; const bx = 20 + c*(bw+gapx), by = 30 + r*200; const bh = 96, f = lvl[x.st];
      const tx = bx + bw/2, ty = by + bh + 18;
      tubes += `<path d="M${tx},${ty} C${tx},${ty+60} ${cx + (tx-cx)*.2},${cy-90} ${cx + (tx-cx)*.08},${cy-30}" fill="none" stroke="${x.st==="notstarted"?"#D4CDE6":x.st==="blocked"?"#EE6A5E":"#B9AEDC"}" stroke-width="2" ${x.st==="live"?'stroke-dasharray="6 4" class="flowl"':x.st==="notstarted"?'stroke-dasharray="2 5"':""}/>`;
      bags += `<g class="bag" data-ref="part:${x.id}" tabindex="0" role="button" aria-label="Part ${x.id}: ${esc(x.name)}, ${PART_WORD[x.st]}">
        <line x1="${tx}" y1="${by-14}" x2="${tx}" y2="${by}" stroke="#8C84A3" stroke-width="2"/>
        <rect class="body" x="${bx}" y="${by}" width="${bw}" height="${bh}" rx="16" fill="rgba(255,255,255,.9)" stroke="${x.st==="notstarted"?"#B6ADCF":"#9D93BD"}" stroke-width="1.6" ${x.st==="notstarted"||x.st==="building"?'stroke-dasharray="5 4"':""}/>
        ${f?`<clipPath id="bg${x.id}"><rect x="${bx}" y="${by}" width="${bw}" height="${bh}" rx="16"/></clipPath><rect x="${bx}" y="${by+bh*(1-f*.86)}" width="${bw}" height="${bh}" fill="${col[x.st]}" opacity=".85" clip-path="url(#bg${x.id})"/>`:""}
        <rect x="${bx+10}" y="${by+12}" width="${bw-20}" height="30" rx="4" fill="#fff" stroke="#E1DCEE"/>
        <text x="${tx}" y="${by+33}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="22" fill="#231B3A">${String(x.id).padStart(2,"0")}</text>
        <text x="${tx}" y="${by+bh-10}" text-anchor="middle" font-size="10.5" font-weight="700" fill="#231B3A">${PART_WORD[x.st].toUpperCase()}</text>
        <path d="M${tx-6},${by+bh} L${tx+6},${by+bh} L${tx+4},${ty} L${tx-4},${ty} Z" fill="#E1DCEE"/>
        ${x.st==="live"?`<circle class="drop" cx="${tx}" cy="${ty+3}" r="3" fill="#3CC48B"/>`:""}
        <foreignObject x="${bx-8}" y="${ty+12}" width="${bw+16}" height="44"><div xmlns="http://www.w3.org/1999/xhtml" style="font:500 10.5px/1.25 Poppins,sans-serif;color:#5F5873;text-align:center">${esc(x.name)}</div></foreignObject></g>`; });
    const stand = `<svg viewBox="0 0 ${W} 600" role="img" aria-label="Twelve drip bags, one for each link, feeding the summary chamber.">
      <line x1="10" x2="${W-10}" y1="16" y2="16" stroke="#8C84A3" stroke-width="4" stroke-linecap="round"/><line x1="10" x2="${W-10}" y1="216" y2="216" stroke="#8C84A3" stroke-width="4" stroke-linecap="round"/>
      ${tubes}${bags}
      <rect x="${cx-115}" y="${cy-34}" width="230" height="62" rx="20" fill="#fff" stroke="#5B3FD0" stroke-width="2"/>
      <rect x="${cx-111}" y="${cy-30+54*(1-.62)}" width="222" height="${54*.62}" rx="16" fill="#5B3FD0" opacity=".22"/>
      <text x="${cx}" y="${cy-6}" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="24" fill="#231B3A">THE SUMMARY</text>
      <text x="${cx}" y="${cy+14}" text-anchor="middle" font-size="11.5" fill="#5F5873">filled ${KP.K3.now}% without typing · plan ${KP.K3.plan}%</text>
      <path d="M${cx+115},${cy} L${W-30},${cy}" stroke="#B6ADCF" stroke-width="2" stroke-dasharray="2 5"/><text x="${W-30}" y="${cy+22}" text-anchor="end" font-size="11" fill="#5F5873">to Billing & Insurance · not started</text>
    </svg>`;
    /* bottles */
    const bottle = k => { const n = Math.min(1,prog(k,k.now)), p = Math.min(1,prog(k,k.plan)); const fc = k.state==="ahead"?"#3CC48B":k.state==="watch"?"#F0A732":"#EE6A5E"; const cc = k.state==="ahead"?"#18825A":k.state==="watch"?"#B06D05":"#C93C31";
      const top = 52, bot = 186, Hh = bot-top, y = v => bot - v*Hh*.92;
      return `<button class="btl" type="button" data-ref="kpi:${k.id}" aria-label="${esc(k.name)}: ${fmtv(k,k.now)}, ${STATE_WORD[k.state]}"><svg viewBox="0 0 100 200" aria-hidden="true">
        <rect x="34" y="6" width="32" height="18" rx="3" fill="${cc}"/><rect x="38" y="24" width="24" height="16" fill="#fff" stroke="#BFB6D6"/>
        <clipPath id="bt${k.id}"><path d="M38,40 L62,40 L62,48 Q86,54 86,72 L86,180 Q86,192 74,192 L26,192 Q14,192 14,180 L14,72 Q14,54 38,48 Z"/></clipPath>
        <rect x="0" y="${y(n)}" width="100" height="200" fill="${fc}" opacity=".8" clip-path="url(#bt${k.id})"/>
        <path d="M38,40 L62,40 L62,48 Q86,54 86,72 L86,180 Q86,192 74,192 L26,192 Q14,192 14,180 L14,72 Q14,54 38,48 Z" fill="rgba(255,255,255,.25)" stroke="#9D93BD" stroke-width="2"/>
        <line x1="14" x2="86" y1="${y(1)}" y2="${y(1)}" stroke="#231B3A" stroke-width="1.5"/><text x="84" y="${y(1)-3}" text-anchor="end" font-size="8.5" font-weight="700" fill="#231B3A">FILL TO</text>
        <line x1="10" x2="90" y1="${y(p)}" y2="${y(p)}" stroke="#231B3A" stroke-width="1.5" stroke-dasharray="4 3"/>
        <rect x="22" y="104" width="56" height="44" rx="4" fill="#fff" stroke="#E1DCEE"/>
        <text x="50" y="128" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="${fmtv(k,k.now).length>7?14:20}" fill="${cc}">${fmtv(k,k.now)}</text>
        <text x="50" y="141" text-anchor="middle" font-size="7.5" font-weight="700" fill="#5F5873">${k.id}</text>
        <path d="M22,62 Q20,120 24,176" stroke="#fff" stroke-width="4" fill="none" opacity=".7" stroke-linecap="round"/>
      </svg><span class="cap2">${esc(k.short)}<small class="${k.state}">${STATE_WORD[k.state]}</small></span></button>`; };
    /* organisers */
    const org = p => { const tg = p.state==="ahead"?"ahead":p.state==="watch"?"watch":"off";
      let body;
      if (UI.view==="day") body = `<ul class="tlist">${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}">${esc(t[0])}${t[1]!==1?` <span style="color:var(--mute);font-weight:400">· ${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`;
      else { const c = []; for (let i=0;i<p.due;i++) c.push(`<i class="${i<p.done?"y":i<p.done+p.late?"l":"e"}"></i>`); body = `<span class="comp" aria-label="${p.done} of ${p.due} done, ${p.late} late">${c.join("")}</span>`; }
      return `<button class="org" type="button" data-ref="per:${p.key}"><span class="hd"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span><span class="tag ${tg}">${PERSON_WORD[p.state]} · ${p.done}/${p.due}</span></span>${body}${p.impact?`<span class="imp">${esc(p.impact)}</span>`:`<span class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</span>`}</button>`; };
    /* blister packs: one blister = ₹1 lakh, 50 per pack, to Feb */
    const spendCells = []; const cats = [["#5B3FD0",sum(D.spend[0].v)],["#2E8FD6",sum(D.spend[1].v)],["#B9AEDC",sum(D.spend[2].v)-2.5],["#C93C31",2.5]];
    cats.forEach(c => { for (let i=0;i<Math.round(c[1]);i++) spendCells.push(`<i class="f" style="--c:${c[0]}"></i>`); });
    while (spendCells.length < Math.round(D.cumSpend[6])) spendCells.push(`<i class="g" style="--c:#5B3FD0"></i>`);
    const be = Math.round(D.cumSpend[6]) - 1; spendCells[be] = spendCells[be].replace('class="g"','class="g mk"');
    while (spendCells.length < 50) spendCells.push(`<i></i>`);
    const backCells = []; for (let i=0;i<Math.round(ebitdaTotal);i++) backCells.push(`<i class="f" style="--c:#18825A"></i>`);
    while (backCells.length < Math.round(D.cumFore[6])) backCells.push(`<i class="g" style="--c:#18825A"></i>`);
    backCells[backCells.length-1] = backCells[backCells.length-1].replace('class="g"','class="g mk"');
    while (backCells.length < 50) backCells.push(`<i></i>`);
    return `<div class="s5"><div class="wrap">
      <nav class="caps" aria-label="Suite sections">${TABS.map((t,i)=>`<button class="cap ${i?"":"on"}" type="button" data-tab="${t[0]}" style="--c:${capCol[i]}"><i></i><span>${t[1]}</span></button>`).join("")}</nav>
      <div class="hero">
        <div class="rx">
          <div class="rh"><b>Rx</b><small>VIREVO · AUTOMATION SUITE<br>${esc(D.family.toUpperCase())}</small></div>
          <div class="rb">
            <h2>${esc(D.suite)}</h2>
            <div class="meta"><div><span>For</span><b>${esc(D.hospital)}</b></div><div><span>Started</span><b>${D.started}</b></div><div><span>Course</span><b>Week ${D.week} of ${D.weeksPlanned}</b></div></div>
            <div aria-label="Pulse strip">
              <button class="dose" type="button" data-tab="links" style="--c:#2E8FD6"><i class="pl"></i><span>Parts live</span><b>${countParts("live")} / 12<small>plan 6</small></b></button>
              <button class="dose" type="button" data-tab="measures" style="--c:#E0702E"><i class="pl"></i><span>KPIs on course</span><b>${onCourse} / 9<small>plan 8</small></b></button>
              <button class="dose" type="button" data-ref="health:0" style="--c:#5B3FD0"><i class="pl"></i><span>Money out · EBITDA back</span><b>${L(spendTotal)} · ${L(ebitdaTotal)}</b></button>
              <button class="dose" type="button" data-ref="health:0" style="--c:#C93C31"><i class="pl"></i><span>Break-even</span><b>Feb 2027<small>plan Jan</small></b></button>
            </div>
            <button class="refill" type="button" data-ref="part:${D.milestone.part}"><b>${D.milestone.days}</b><span>days to the next go-live<small>${esc(D.milestone.what)} · ${D.milestone.date}</small></span></button>
            <div class="warnbox"><b>WARNINGS</b>${D.watch.map(w=>`<button type="button" data-ref="${w.ref}">${esc(w.t)} <small>· ${esc(P[w.who].name)}</small></button>`).join("")}</div>
            <div class="hand">Readings as of ${esc(D.asOf)}</div>
          </div>
        </div>
        <section class="stand" data-zone="links" aria-label="Integrations">${stand}</section>
      </div>
      <section class="zone" data-zone="measures"><div class="zh"><h3>KPIs · the shelf</h3><p>Filled to now · dashed line is the plan for this week · solid line is the target</p></div>
        <div class="shelf">${D.kpis.map(bottle).join("")}</div>
        <div class="under">${D.kpis.map(k=>`<button type="button" data-ref="kpi:${k.id}">${esc(k.short)}<small class="${k.state}">${STATE_WORD[k.state].toUpperCase()}</small></button>`).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3>Taskboards · pill organisers</h3>${viewToggle("vt")}</div><div class="orgs">${D.people.map(org).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3>Project Status · two blister packs</h3><p>One blister is ₹1 lakh · faded is forecast to February · ringed blisters are where the two packs meet</p></div>
        <div class="packs">
          <div class="pack"><h4>Money out <b>${L(spendTotal)}</b></h4><div class="bl">${spendCells.join("")}</div>
            <div class="key"><span style="--c:#5B3FD0">Subscription</span><span style="--c:#2E8FD6">Salaries, roles we recommended</span><span style="--c:#B9AEDC">One-time</span><span style="--c:#C93C31">Imaging fee, not in plan</span></div></div>
          <div class="pack"><h4>EBITDA back <b>${L(ebitdaTotal)}</b></h4><div class="bl">${backCells.join("")}</div>
            <div class="key"><span style="--c:#18825A">From freed bed-days</span><span style="--c:#9FD9BE">Forecast</span></div></div>
          <div class="verdict">
            <button type="button" data-ref="health:0">Break-even<b>Feb 2027</b>plan said Jan 2027</button>
            <button type="button" data-ref="month:2">Each month now<b>₹3.32 lakh out</b>subscription ₹2.4 · salaries ₹0.92</button>
            <button type="button" data-ref="health:0">EBITDA each month<b>₹3.9 → ₹6.3 lakh</b>now, and at full run</button>
            <button type="button" class="bad" data-ref="health:0">4 weeks late<b>See causes ›</b>and the recovery plan</button>
          </div>
        </div></section>
    </div></div>`;
  }
});
