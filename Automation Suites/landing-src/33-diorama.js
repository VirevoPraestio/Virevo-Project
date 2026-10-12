/* ===== Scheme C: the hospital diorama ===== */
SCHEMES.push({
  key:"diorama", letter:"C", name:"Hospital diorama",
  note:"<b>C · Hospital diorama.</b> The suite is a model of the hospital. Every department that feeds the summary is a building piped to the summary engine; the pipe flows, ticks or stands empty by how far its link has got. KPIs are lift shafts, the team is the site crew, and break-even is a bridge still being built. Sections are floors on a lift panel; the watch list is road signs. <b>New:</b> every peek and popup has <b>Ask Tojo about this</b>; it opens the chat with the item attached and the question written. Send it, edit it, or clear it.",
  vars:{ "--sh-bg":"#F7FAFD","--sh-fg":"#1B2635","--sh-mute":"#566275","--sh-line":"#D3DCE6","--sh-card":"#FFFFFF","--c-ok":"#1B8A4B","--c-warn":"#B47610","--c-bad":"#C93A30","--pk-bg":"#1B2635","--pk-fg":"#F7FAFD","--pk-line":"#1B2635","--pk-r":"12px","--sh-r":"22px" },
  fab:18,
  blocks:{ nav:".lift", pulse:".signs", watch:".warn", countdown:".hoard", hero:".sv", kpis:".shafts", team:".crew", money:".bridge" },
  css:`
.s3{--sky1:#CFE5F6;--sky2:#F1F7FC;--ink:#1B2635;--mute:#566275;--line:#D3DCE6;--ok:#1B8A4B;--warn:#B47610;--bad:#C93A30;--grey:#8E9AAB;--steel1:#D7DCE2;--steel2:#A7B0BA;--led:#FF8A1F;--sign:#0F6B45;
  background:linear-gradient(180deg,var(--sky1),var(--sky2) 520px,#F4F7FA 520px);color:var(--ink);padding:18px 16px 90px}
.s3 .wrap{max-width:1240px;margin:0 auto}
.s3 .lift{display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px;background:linear-gradient(135deg,#E9EDF1,var(--steel1) 40%,#C4CBD3);border:1px solid #AEB6C0;border-radius:18px;padding:12px 16px;box-shadow:0 2px 0 #fff inset,0 10px 24px rgba(27,38,53,.15)}
.s3 .disp{background:#1A1110;border-radius:8px;padding:6px 12px;min-width:150px;color:var(--led);font-family:var(--f-num);font-size:30px;line-height:1;letter-spacing:.06em;text-shadow:0 0 8px rgba(255,138,31,.6);box-shadow:inset 0 2px 6px #000}
.s3 .disp small{display:block;font-family:var(--f-body);font-size:10px;letter-spacing:.14em;color:#B86A22;text-shadow:none}
.s3 .btns{display:flex;flex-wrap:wrap;gap:10px}
.s3 .fl{display:flex;align-items:center;gap:8px;background:transparent;border:0;padding:0;font-size:12.5px;font-weight:600;color:var(--ink);min-height:48px}
.s3 .fl i{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-family:var(--f-num);font-size:20px;background:radial-gradient(circle at 35% 30%,#fff,#C9D0D8 60%,#9AA3AD);border:2px solid #8B949E;box-shadow:0 3px 0 #7D868F;transition:box-shadow .15s}
.s3 .fl.on i,.s3 .fl:hover i{box-shadow:0 0 0 3px var(--led),0 0 14px rgba(255,138,31,.7);color:#9A4A06}
.s3 .fl:active i{transform:translateY(2px);box-shadow:0 1px 0 #7D868F}
.s3 .head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:end;margin:22px 0 6px}
.s3 .head small{font-size:12px;font-weight:600;letter-spacing:.14em;color:var(--mute)}
.s3 h2{font-family:var(--f-num);font-weight:400;font-size:72px;line-height:.9;margin:4px 0 0;letter-spacing:.01em}
.s3 .signs{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}
.s3 .rs{background:var(--sign);color:#fff;border:3px solid #fff;outline:2px solid var(--sign);border-radius:10px;padding:6px 12px;text-align:left;min-width:128px}
.s3 .rs small{display:block;font-size:10.5px;letter-spacing:.1em;font-weight:600;color:#fff}
.s3 .rs b{font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1;letter-spacing:.03em}
.s3 .rs em{font-style:normal;font-size:11px;color:#E4F2EA}
.s3 .rs.blue{background:#1F4FA8;outline-color:#1F4FA8}
.s3 .scene{position:relative;margin-top:6px}
.s3 .scene svg{width:100%;height:auto;display:block;overflow:visible}
.s3 .sv{overflow-x:auto}
.s3 .flow{animation:s3flow 1.2s linear infinite}
.s3 .flow.slow{animation-duration:3.2s}
@keyframes s3flow{to{stroke-dashoffset:-24}}
.s3 .bc{cursor:pointer}
.s3 .bc:focus{outline:none} .s3 .bc:focus circle{stroke:#F2B705;stroke-width:3}
.s3 .warn{position:absolute;left:0;top:0;display:grid;gap:10px;max-width:260px}
.s3 .wd{display:grid;grid-template-columns:44px minmax(0,1fr);gap:10px;align-items:center;background:rgba(255,255,255,.85);border:0;border-radius:10px;padding:6px 10px 6px 6px;text-align:left;font-size:12.5px;font-weight:600;color:var(--ink);box-shadow:0 4px 10px rgba(27,38,53,.12)}
.s3 .wd i{width:34px;height:34px;margin:5px;background:#FFC93C;border:2.5px solid #1B2635;transform:rotate(45deg);display:grid;place-items:center}
.s3 .wd i b{transform:rotate(-45deg);font-family:var(--f-num);font-size:20px;font-style:normal}
.s3 .wd small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s3 .hoard{position:absolute;right:0;top:0;background:repeating-linear-gradient(-45deg,#FFC93C 0 12px,#1B2635 12px 24px);padding:6px;border-radius:6px;box-shadow:0 4px 10px rgba(27,38,53,.15)}
.s3 .hoard div{background:#fff;padding:8px 12px;border-radius:3px;text-align:center}
.s3 .hoard b{display:block;font-family:var(--f-num);font-weight:400;font-size:40px;line-height:.9}
.s3 .hoard small{font-size:11.5px}
.s3 .legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12px;color:var(--mute);justify-content:center;margin-top:4px}
.s3 .legend i{display:inline-block;width:22px;height:0;border-top:3px solid;vertical-align:middle;margin-right:6px}
.s3 .zone{margin-top:40px;scroll-margin-top:20px;border-radius:18px}
.s3 .zh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 16px;margin-bottom:14px}
.s3 .zh h3{font-family:var(--f-num);font-weight:400;font-size:38px;margin:0;line-height:1;display:flex;align-items:center;gap:12px}
.s3 .zh h3 span{font-size:15px;width:30px;height:30px;border-radius:50%;display:inline-grid;place-items:center;background:radial-gradient(circle at 35% 30%,#fff,#C9D0D8 60%,#9AA3AD);border:2px solid #8B949E}
.s3 .zh p{margin:0;font-size:13px;color:var(--mute)}
.s3 .shafts{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:10px}
.s3 .shaft{display:flex;flex-direction:column;align-items:center;gap:6px;background:transparent;border:0;padding:0;color:inherit;text-align:center}
.s3 .tube{position:relative;width:58px;height:220px;border-radius:12px;background:linear-gradient(90deg,#E8EEF4,#fff 40%,#DDE5EE);border:2px solid #B8C3CF;overflow:hidden;box-shadow:inset 0 0 0 4px rgba(255,255,255,.6)}
.s3 .tube .fln{position:absolute;left:6px;right:6px;border-top:1px solid #C8D2DD}
.s3 .tube .car{position:absolute;left:7px;right:7px;height:26px;border-radius:5px;transform:translateY(50%);display:grid;place-items:center;color:#fff;font-size:10px;font-weight:700;box-shadow:0 3px 6px rgba(0,0,0,.25);transition:bottom .6s}
.s3 .tube .ghost{position:absolute;left:5px;right:5px;height:26px;border-radius:5px;border:2px dashed var(--mute);transform:translateY(50%)}
.s3 .tube .tgt{position:absolute;top:8px;left:0;right:0;font-size:10px;font-weight:700;color:var(--mute)}
.s3 .shaft b{font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1}
.s3 .shaft .nm{font-size:11.5px;font-weight:600;line-height:1.25;min-height:30px}
.s3 .shaft .st{font-size:10.5px;font-weight:700;letter-spacing:.05em}
.s3 .ahead{color:var(--ok)} .s3 .watch{color:var(--warn)} .s3 .off{color:var(--bad)}
.s3 .shaft:hover .tube,.s3 .shaft:focus-visible .tube{border-color:var(--ink)}
.s3 .crew{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.s3 .mate{display:grid;grid-template-columns:56px minmax(0,1fr);gap:12px;align-items:start;background:#fff;border:1px solid var(--line);border-radius:16px;padding:12px;text-align:left;color:inherit;box-shadow:0 6px 0 #E3E9EF;transition:transform .15s}
.s3 .mate:hover,.s3 .mate:focus-visible{transform:translateY(-3px)}
.s3 .mate svg{width:56px;height:56px}
.s3 .mate .nm{font-weight:700;font-size:13.5px;line-height:1.2}
.s3 .mate .nm small{display:block;font-weight:400;color:var(--mute);font-size:11.5px}
.s3 .mate ul{list-style:none;margin:6px 0 0;padding:0;font-size:12px;display:grid;gap:2px}
.s3 .mate ul li.y{color:var(--ok)} .s3 .mate ul li.l{color:var(--bad);font-weight:600}
.s3 .mate .imp{font-size:11.5px;color:var(--bad);margin-top:6px;line-height:1.35}
.s3 .mate .nx{font-size:11.5px;color:var(--mute);margin-top:6px}
.s3 .vt{display:inline-flex;gap:6px}
.s3 .vt button{border:2px solid var(--ink);background:#fff;border-radius:999px;padding:5px 14px;font-size:12px;font-weight:600;min-height:38px}
.s3 .vt button[aria-pressed="true"]{background:var(--ink);color:#fff}
.s3 .bridge{background:linear-gradient(180deg,#DCEBF6,#F1F7FC);border-radius:18px;padding:10px;border:1px solid var(--line);overflow-x:auto}
.s3 .bridge svg{display:block;width:100%;min-width:620px;height:auto}
.s3 .costs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin-top:14px}
.s3 .costs button{background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px 12px;text-align:left;color:inherit;font-size:12px}
.s3 .costs b{display:block;font-family:var(--f-num);font-weight:400;font-size:26px;line-height:1.1;color:var(--ink)}
.s3 .costs .bad{border-color:var(--bad);color:var(--bad)}
@media (max-width:1000px){ .s3 .shafts{grid-template-columns:repeat(5,minmax(0,1fr))} .s3 .crew{grid-template-columns:repeat(2,minmax(0,1fr))} .s3 .costs{grid-template-columns:repeat(2,minmax(0,1fr))} .s3 .head{grid-template-columns:1fr} .s3 .signs{justify-content:flex-start}
  .s3 .warn,.s3 .hoard{position:static;max-width:none} .s3 .scene{display:grid;gap:10px} }
@media (max-width:600px){ .s3 .sv svg{min-width:700px} .s3 h2{font-size:52px} .s3 .shafts{grid-template-columns:repeat(3,minmax(0,1fr))} .s3 .crew{grid-template-columns:1fr} .s3 .fl span{display:none} .s3 .btns{gap:6px} .s3 .disp{min-width:0;width:100%} .s3 .rs{min-width:0;flex:1 1 140px} }
`,
  render(){
    /* ---- isometric scene ---- */
    const S = 30, OX = 430, OY = 70, C = 0.866, Sn = 0.5;
    const pt = (x,y,z=0) => [OX + (x - y)*C*S, OY + (x + y)*Sn*S - z*S];
    const poly = (pts, fill, extra="") => `<polygon points="${pts.map(p=>p.map(v=>v.toFixed(1)).join(",")).join(" ")}" fill="${fill}" ${extra}/>`;
    const box = (x,y,w,d,h,roof,ghost) => {
      const st = ghost ? `stroke="#8E9AAB" stroke-dasharray="4 3" stroke-width="1.2"` : `stroke="#1B2635" stroke-opacity=".18"`;
      const f = ghost ? ["none","none","none"] : ["#FFFFFF","#E4EAF1","#C9D3DF"];
      const top = poly([pt(x,y,h),pt(x+w,y,h),pt(x+w,y+d,h),pt(x,y+d,h)], f[0], st);
      const left = poly([pt(x,y+d,0),pt(x+w,y+d,0),pt(x+w,y+d,h),pt(x,y+d,h)], f[1], st);
      const right = poly([pt(x+w,y,0),pt(x+w,y+d,0),pt(x+w,y+d,h),pt(x+w,y,h)], f[2], st);
      let win = "";
      if (!ghost) { for (let i=0.35;i<w-0.2;i+=0.55) for (let z=0.45; z<h-0.3; z+=0.6) win += poly([pt(x+i,y+d,z),pt(x+i+0.3,y+d,z),pt(x+i+0.3,y+d,z+0.3),pt(x+i,y+d,z+0.3)],"#B7C9DD"); }
      const band = ghost ? "" : poly([pt(x,y,h),pt(x+w,y,h),pt(x+w,y+0.22,h),pt(x,y+0.22,h)], roof);
      return left + right + top + win + band;
    };
    const B = {
      ward:  {x:0.6,y:0.6,w:3.2,d:2.0,h:2.4,roof:"#5B8DEF",label:"Wards"},
      lab:   {x:5.0,y:0.2,w:2.0,d:1.6,h:1.6,roof:"#9B6BDF",label:"Laboratory"},
      radio: {x:8.6,y:0.6,w:2.2,d:2.0,h:1.9,roof:"#E0663A",label:"Radiology"},
      ot:    {x:9.0,y:4.4,w:2.0,d:2.4,h:1.5,roof:"#2AA6A0",label:"Theatres"},
      pharm: {x:8.4,y:8.6,w:2.2,d:1.8,h:1.4,roof:"#E2A72E",label:"Pharmacy"},
      stores:{x:4.6,y:9.4,w:2.4,d:1.6,h:1.2,roof:"#8C6B4F",label:"Stores"},
      nurse: {x:0.6,y:8.6,w:2.2,d:1.8,h:1.3,roof:"#D45A8C",label:"Nursing station"},
      phone: {x:0.8,y:4.6,w:1.4,d:1.4,h:3.0,roof:"#3D4F66",label:"Doctors' phones"},
      engine:{x:4.6,y:4.4,w:2.6,d:2.6,h:4.4,roof:"#1B2635",label:"Summary engine"}
    };
    const order = { live:4, testing:3, building:2, blocked:1, notstarted:0 };
    const pipeCol = { live:"#1B8A4B", testing:"#E09B1A", building:"#8E9AAB", blocked:"#C93A30", notstarted:"#B9C3CF" };
    const ec = [B.engine.x + B.engine.w/2, B.engine.y + B.engine.d/2];
    let pipes = "", builds = "", beacons = "";
    const drawOrder = Object.keys(B).sort((a,b)=>(B[a].x+B[a].w/2+B[a].y+B[a].d/2)-(B[b].x+B[b].w/2+B[b].y+B[b].d/2));
    Object.entries(B).forEach(([k,b]) => { if (k==="engine") return;
      const parts = D.parts.filter(p=>p.dept===k); if (!parts.length) return;
      const best = parts.reduce((a,p)=>order[p.st]>order[a.st]?p:a, parts[0]).st;
      const c = [b.x + b.w/2, b.y + b.d/2]; const a = pt(c[0],c[1],0.15), e = pt(ec[0],ec[1],0.15);
      pipes += `<line x1="${a[0]}" y1="${a[1]}" x2="${e[0]}" y2="${e[1]}" stroke="#1B2635" stroke-opacity=".12" stroke-width="9" stroke-linecap="round"/>`;
      const dash = best==="live" ? `stroke-dasharray="8 4" class="flow"` : best==="testing" ? `stroke-dasharray="8 4" class="flow slow"` : best==="notstarted" ? `stroke-dasharray="2 6"` : `stroke-dasharray="4 4"`;
      pipes += `<line x1="${a[0]}" y1="${a[1]}" x2="${e[0]}" y2="${e[1]}" stroke="${pipeCol[best]}" stroke-width="4" stroke-linecap="round" ${dash}/>`;
      if (best==="blocked") { const m = [(a[0]+e[0])/2,(a[1]+e[1])/2]; pipes += `<g transform="translate(${m[0]},${m[1]})"><circle r="10" fill="#fff" stroke="#C93A30" stroke-width="2"/><path d="M-4,-4 L4,4 M4,-4 L-4,4" stroke="#C93A30" stroke-width="2.5"/></g>`; }
    });
    drawOrder.forEach(k => { const b = B[k]; builds += box(b.x,b.y,b.w,b.d,b.h,b.roof,false);
      const lp = pt(b.x + b.w/2, b.y + b.d/2, b.h); builds += `<text x="${lp[0]}" y="${lp[1]-30}" text-anchor="middle" font-size="12" font-weight="700" fill="#1B2635" paint-order="stroke" stroke="#F1F7FC" stroke-width="4">${b.label}</text>`;
      const parts = D.parts.filter(p=>p.dept===k);
      parts.forEach((p,i) => { const bx = lp[0] + (i - (parts.length-1)/2)*24, by = lp[1]-12;
        const col = pipeCol[p.st]; beacons += `<g class="bc" data-ref="part:${p.id}" tabindex="0" role="button" aria-label="Part ${p.id}: ${esc(p.name)}, ${PART_WORD[p.st]}"><line x1="${bx}" y1="${by}" x2="${bx}" y2="${lp[1]}" stroke="#1B2635" stroke-width="1.5"/><circle cx="${bx}" cy="${by}" r="10" fill="${p.st==="notstarted"||p.st==="building"?"#fff":col}" stroke="${col}" stroke-width="2" ${p.st==="building"?'stroke-dasharray="3 2"':""}/><text x="${bx}" y="${by+4}" text-anchor="middle" font-size="10.5" font-weight="700" fill="${p.st==="notstarted"||p.st==="building"?"#1B2635":"#fff"}">${p.id}</text></g>`; });
    });
    const bill = box(12.8,3.4,1.8,1.8,1.6,"",true); const bl = pt(13.7,4.3,1.6);
    const bp1 = pt(ec[0],ec[1],0.15), bp2 = pt(13.7,4.3,0.15);
    const ground = poly([pt(-0.6,-0.8),pt(14.8,-0.8),pt(14.8,11.6),pt(-0.6,11.6)], "#E3EEDD", `stroke="#C9DAC2" stroke-width="2"`);
    let grid = ""; for (let i=0;i<=14.8;i+=1.5){ const a=pt(i,-0.8),b=pt(i,11.6); grid += `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="#D2E2CB"/>`; } for (let j=-0.8;j<=11.6;j+=1.55){ const a=pt(-0.6,j),b=pt(14.8,j); grid += `<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="#D2E2CB"/>`; }
    const slab = poly([pt(-0.6,11.6),pt(14.8,11.6),pt(14.8,11.6,-0.5),pt(-0.6,11.6,-0.5)],"#C7D8C0") + poly([pt(14.8,-0.8),pt(14.8,11.6),pt(14.8,11.6,-0.5),pt(14.8,-0.8,-0.5)],"#B5C9AE");
    const scene = `<svg viewBox="0 -30 900 530" role="img" aria-label="Model of the hospital: each department that feeds the summary is piped to the summary engine.">${slab}${ground}${grid}${pipes}
      <line x1="${bp1[0]}" y1="${bp1[1]}" x2="${bp2[0]}" y2="${bp2[1]}" stroke="#8E9AAB" stroke-width="3" stroke-dasharray="2 6"/>
      ${builds}${bill}<text x="${bl[0]}" y="${bl[1]-14}" text-anchor="middle" font-size="11.5" font-weight="600" fill="#566275">Billing & Insurance</text><text x="${bl[0]}" y="${bl[1]}" text-anchor="middle" font-size="10.5" fill="#566275">next suite · 2 hand-offs</text>${beacons}</svg>`;

    /* ---- lift shafts ---- */
    const shaft = k => { const n = Math.min(1,prog(k,k.now)), p = prog(k,k.plan); const col = k.state==="ahead"?"#1B8A4B":k.state==="watch"?"#E09B1A":"#C93A30"; const H=220, pad=30;
      const y = v => pad/2 + v*(H-pad*1.6);
      return `<button class="shaft" type="button" data-ref="kpi:${k.id}"><span class="tube" aria-hidden="true"><span class="tgt">${fmtv(k,k.target)}</span>${[0,.25,.5,.75,1].map(f=>`<span class="fln" style="bottom:${y(f)}px"></span>`).join("")}
        <span class="ghost" style="bottom:${y(p)}px"></span><span class="car" style="bottom:${y(n)}px;background:${col}">NOW</span></span>
        <b class="${k.state}">${fmtv(k,k.now)}</b><span class="nm">${esc(k.short)}</span><span class="st ${k.state}">${STATE_WORD[k.state].toUpperCase()}</span></button>`; };

    /* ---- crew ---- */
    const mate = p => { const pc = p.done/p.due; const hat = p.state==="ahead"?"#1B8A4B":p.state==="watch"?"#E09B1A":"#C93A30"; const R=24, Cc=2*Math.PI*R;
      const ring = `<svg viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="${R}" fill="none" stroke="#E3E9EF" stroke-width="5"/><circle cx="28" cy="28" r="${R}" fill="none" stroke="${hat}" stroke-width="5" stroke-dasharray="${(Cc*pc).toFixed(1)} ${Cc}" transform="rotate(-90 28 28)" stroke-linecap="round"/><circle cx="28" cy="31" r="11" fill="#F2D2B6"/><path d="M15,27 a13,11 0 0 1 26,0 z" fill="${hat}"/><rect x="13" y="26" width="30" height="3.5" rx="1.5" fill="${hat}"/><text x="28" y="38" text-anchor="middle" font-size="8" font-weight="700" fill="#1B2635">${initials(p.name)}</text></svg>`;
      const body = UI.view==="day" ? `<ul>${p.today.map(t=>`<li class="${t[1]===1?"y":String(t[1]).startsWith("late")?"l":""}">${t[1]===1?"✓":String(t[1]).startsWith("late")?"!":"○"} ${esc(t[0])}${t[1]!==1?` <span style="color:var(--mute)">· ${esc(t[1])}</span>`:""}</li>`).join("")}</ul>`
        : `<div style="font-size:12px;margin-top:4px"><b>${p.done}</b> of ${p.due} done${p.late?` · <b class="off">${p.late} late</b>`:""}</div>${p.impact?`<div class="imp">${esc(p.impact)}</div>`:`<div class="nx">Next: ${esc(p.next[0][0])} · ${esc(p.next[0][1])}</div>`}`;
      return `<button class="mate" type="button" data-ref="per:${p.key}">${ring}<span style="min-width:0"><span class="nm">${esc(p.name)}<small>${esc(p.role)}</small></span>${body}</span></button>`; };

    /* ---- bridge ---- */
    const BW = 960, x0 = 150, x1 = 790, segs = 7, sw = (x1-x0)/segs, deck = 150;
    let deckSvg = "";
    for (let i=0;i<segs;i++){ const x = x0 + i*sw; const built = i <= D.actualTo;
      deckSvg += `<g data-ref="month:${i}" data-nopen style="cursor:help">${built
        ? `<rect x="${x+1}" y="${deck}" width="${sw-2}" height="14" fill="#1B2635"/><path d="M${x+1},${deck+14} L${x+sw/2},${deck+48} L${x+sw-1},${deck+14}" fill="none" stroke="#1B2635" stroke-width="3"/>`
        : `<rect x="${x+1}" y="${deck}" width="${sw-2}" height="14" fill="none" stroke="#566275" stroke-dasharray="5 4" stroke-width="2"/><path d="M${x+6},${deck+16} L${x+sw-6},${deck+60} M${x+sw-6},${deck+16} L${x+6},${deck+60}" stroke="#B47610" stroke-width="1.5" stroke-dasharray="3 3"/>`}
        <text x="${x+sw/2}" y="${deck-10}" text-anchor="middle" font-size="12" font-weight="600" fill="${built?"#1B2635":"#566275"}">${D.cumMonths[i]}</text><rect x="${x}" y="${deck-30}" width="${sw}" height="100" fill="transparent"/></g>`; }
    const planX = x0 + 6*sw;
    const bridge = `<svg viewBox="0 0 ${BW} 260" role="img" aria-label="Bridge to break-even: three months built, four more to cross. The plan reached the far bank after six months, in January; the forecast reaches it after seven, in February.">
      <path d="M0,260 L0,${deck} L${x0},${deck} L${x0+30},260 Z" fill="#9FB4C8"/><path d="M${BW},260 L${BW},${deck} L${x1},${deck} L${x1-30},260 Z" fill="#7FA88A"/>
      <path d="M${x0+20},236 Q${(x0+x1)/2},216 ${x1-20},236 L${x1-20},260 L${x0+20},260 Z" fill="#8EC3E6"/><path d="M${x0+60},242 q20,-6 40,0 t40,0 M${x0+260},246 q20,-6 40,0 t40,0 M${x0+470},242 q20,-6 40,0 t40,0" stroke="#fff" stroke-width="2" fill="none" opacity=".7"/>
      ${deckSvg}
      <line x1="${planX}" x2="${planX}" y1="40" y2="${deck}" stroke="#566275" stroke-dasharray="4 4"/><text x="${planX}" y="32" text-anchor="middle" font-size="11.5" fill="#566275">plan: across by Jan</text>
      <text x="${x0-10}" y="${deck-40}" text-anchor="end" font-family="Bebas Neue, sans-serif" font-size="26" fill="#1B2635">MONEY OUT</text><text x="${x0-10}" y="${deck-20}" text-anchor="end" font-size="12" fill="#1B2635">${L(spendTotal)} so far</text>
      <text x="${BW-12}" y="${deck-40}" text-anchor="end" font-family="Bebas Neue, sans-serif" font-size="26" fill="#1B2635">BREAK-EVEN</text><text x="${BW-12}" y="${deck-20}" text-anchor="end" font-size="12" fill="#C93A30" font-weight="600">reached Feb · 4 weeks late</text>
      <g transform="translate(${x1-8},${deck-62})"><line x1="0" y1="0" x2="0" y2="62" stroke="#1B2635" stroke-width="2"/><path d="M0,0 L26,8 L0,16 Z" fill="#C93A30"/></g>
    </svg>`;

    return `<div class="s3"><div class="wrap">
      <nav class="lift" aria-label="Suite sections"><div class="disp" aria-hidden="true"><small>YOU ARE ON</small><span id="s3floor">G · OVERVIEW</span></div>
        <div class="btns">${TABS.map((t,i)=>`<button class="fl ${i?"":"on"}" type="button" data-tab="${t[0]}"><i>${t[0]==="chat"?"☎":i===0?"G":i}</i><span>${t[1]}</span></button>`).join("")}</div></nav>
      <div class="head"><div><small>AUTOMATION SUITE · ${esc(D.family.toUpperCase())} · ${esc(D.hospital.toUpperCase())}</small><h2>${esc(D.suite)}</h2></div>
        <div class="signs" aria-label="Pulse strip">
          <button class="rs" type="button" data-tab="links"><small>PARTS LIVE →</small><b>${countParts("live")} / 12</b> <em>plan 6</em></button>
          <button class="rs" type="button" data-tab="measures"><small>KPIs ON COURSE →</small><b>${onCourse} / 9</b> <em>plan 8</em></button>
          <button class="rs blue" type="button" data-ref="health:0"><small>OUT · EBITDA BACK</small><b>${spendTotal.toFixed(1)} · ${ebitdaTotal.toFixed(1)}</b> <em>₹ lakh</em></button>
          <button class="rs blue" type="button" data-ref="health:0"><small>BREAK-EVEN</small><b>FEB 2027</b> <em>plan Jan</em></button>
        </div></div>
      <section class="scene zone" data-zone="links" style="margin-top:4px">
        <div class="warn" aria-label="Watch list">${D.watch.map((w,i)=>`<button class="wd" type="button" data-ref="${w.ref}"><i><b>!</b></i><span>${esc(w.t)}<small>${esc(P[w.who].name)}</small></span></button>`).join("")}</div>
        <div class="hoard" data-ref="part:${D.milestone.part}" role="button" tabindex="0"><div><small>OPENING IN</small><b>${D.milestone.days} DAYS</b><small>${esc(D.milestone.what)}<br>${D.milestone.date}</small></div></div>
        <div class="sv">${scene}</div>
        <div class="legend"><span><i style="border-color:#1B8A4B"></i>Live, data flowing</span><span><i style="border-color:#E09B1A;border-top-style:dashed"></i>Testing</span><span><i style="border-color:#8E9AAB;border-top-style:dashed"></i>Being built</span><span><i style="border-color:#C93A30"></i>Late</span><span><i style="border-color:#B9C3CF;border-top-style:dotted"></i>Not started</span><span>· Data as of ${esc(D.asOf)}</span></div>
      </section>
      <section class="zone" data-zone="measures"><div class="zh"><h3><span>2</span>KPIs · lift shafts</h3><p>The car is now · the dashed car is where the plan says we should be · the top floor is the target</p></div>
        <div class="shafts">${D.kpis.map(shaft).join("")}</div></section>
      <section class="zone" data-zone="team"><div class="zh"><h3><span>3</span>Taskboards · site crew</h3>${viewToggle("vt")}</div><div class="crew">${D.people.map(mate).join("")}</div></section>
      <section class="zone" data-zone="health"><div class="zh"><h3><span>4</span>Project Status · the bridge to break-even</h3><p>One span a month · solid is built, scaffold is forecast</p></div>
        <div class="bridge">${bridge}</div>
        <div class="costs">
          <button type="button" data-ref="month:2">Subscription<b>${L(2.4)}/mo</b></button>
          <button type="button" data-ref="month:2">Salaries, roles we recommended<b>${L(0.92)}/mo</b></button>
          <button type="button" data-ref="month:2">One-time so far<b>${L(8.2)}</b></button>
          <button type="button" data-ref="health:0">EBITDA added so far<b>${L(ebitdaTotal)}</b></button>
          <button type="button" class="bad" data-ref="health:0">Why 4 weeks late<b>3 causes ›</b></button>
        </div></section>
    </div></div>`;
  }
});
/* lift display follows the floor */
document.addEventListener("click", e => { const b = e.target.closest(".s3 .fl"); if (!b) return; const d = document.getElementById("s3floor"); if (d) d.textContent = b.querySelector("i").textContent + " · " + b.textContent.replace(b.querySelector("i").textContent,"").trim().toUpperCase(); });
