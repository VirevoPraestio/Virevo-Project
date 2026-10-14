/* ===== Option A · Lights on: the hospital at night lights up, floor by floor, as its data arrives ===== */

LOOKS.push({ key:"night", letter:"A", name:"Lights on", note:"<b>A · Lights on.</b> The hospital at night. Each building is a data family, each floor a file: a floor lights up the moment its file arrives. The lights on each roof are its measures: steady amber from your data, slow lilac from reference, orange kept on paper, hollow red not recorded.",
css:`
.lk-night{--n-sky:#0F1729;--n-sky2:#1A2742;--n-face:#24324D;--n-side:#18233A;--n-roof:#33456A;--n-off:#2F3D5B;--n-lit:#F6C35B;--n-ink:#F2EBDD;--n-mute:#A9B4CB;--n-line:#33446A;--n-ref:#B7A6EC;--n-paper:#F08A4B;--n-none:#F06B6B;
  --pk-bg:#0B1222;--pk-fg:#F2EBDD;--pk-line:#33446A;--sh-bg:#FBF8F1;--sh-fg:#14203A;--sh-mute:#55607A;--sh-line:#DDD8CC;--sh-card:#fff;--c-ok:#1E6B45;--c-warn:#9A6A00;--c-bad:#A23A3A;
  background:radial-gradient(1200px 520px at 70% -10%,#25365C 0%,transparent 60%),linear-gradient(180deg,var(--n-sky) 0%,var(--n-sky2) 100%);color:var(--n-ink);padding:18px clamp(16px,3vw,40px) 120px;min-height:100vh}
.lk-night .jr ol{list-style:none;margin:0;padding:6px;display:flex;gap:6px;overflow:auto;border:1px solid var(--n-line);border-radius:999px;background:rgba(10,16,30,.55);scrollbar-width:none}
.lk-night .jr li{flex:0 0 auto}
.lk-night .jr button{display:flex;align-items:center;gap:8px;border:0;background:transparent;color:var(--n-mute);border-radius:999px;padding:6px 14px 6px 6px;min-height:44px}
.lk-night .jr button b{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;border:1.5px solid var(--n-line);font-family:var(--f-num);font-weight:400;font-size:18px}
.lk-night .jr button span{display:flex;flex-direction:column;align-items:flex-start;font-size:13px;font-weight:600;line-height:1.15}
.lk-night .jr button small{font-weight:400;font-size:11px;opacity:.8}
.lk-night .jr .now button{background:var(--n-lit);color:#1B1406}
.lk-night .jr .now button b{border-color:#1B1406;background:#1B1406;color:var(--n-lit)}
.lk-night .jr button[aria-disabled]{cursor:default}
.lk-night .top{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px 28px;align-items:end;margin:26px 0 18px}
.lk-night .eb{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--n-mute)}
.lk-night h1{font-family:var(--f-num);font-weight:400;font-size:clamp(44px,6vw,64px);line-height:.92;margin:6px 0 8px;letter-spacing:.01em;text-wrap:balance}
.lk-night h1 em{font-style:normal;color:var(--n-lit)}
.lk-night .lede{margin:0;max-width:60ch;color:var(--n-mute)}
.lk-night .pulse{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.lk-night .pz{text-align:left;border:1.5px solid var(--n-line);background:rgba(10,16,30,.6);border-radius:12px;padding:10px 12px;color:var(--n-ink);min-width:132px;box-shadow:inset 0 0 0 1px rgba(246,195,91,.06)}
.lk-night .pz .pl{display:block;font-size:10.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--n-mute)}
.lk-night .pz b{display:block;font-family:var(--f-num);font-weight:400;font-size:34px;line-height:1;color:var(--n-lit);text-shadow:0 0 18px rgba(246,195,91,.35)}
.lk-night .pz b i{font-style:normal;font-size:20px;color:var(--n-mute);text-shadow:none}
.lk-night .pz small{display:block;font-size:11.5px;color:var(--n-mute)}
.lk-night .mid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:14px;margin-bottom:14px}
.lk-night .intake{display:grid;gap:8px}
.lk-night .drop{display:flex;flex-direction:column;gap:2px;border:2px dashed rgba(246,195,91,.6);border-radius:14px;padding:14px 16px;cursor:pointer;background:rgba(246,195,91,.05)}
.lk-night .drop:hover,.lk-night .drop:focus-within{background:rgba(246,195,91,.12)}
.lk-night .dz-big{font-family:var(--f-num);font-size:28px;letter-spacing:.02em;color:var(--n-lit);line-height:1}
.lk-night .dz-sub{font-size:13px;color:var(--n-mute)}
.lk-night .acts{display:flex;flex-wrap:wrap;gap:8px}
.lk-night .act{border:1.5px solid var(--n-lit);background:var(--n-lit);color:#1B1406;border-radius:999px;padding:8px 16px;font-weight:600;font-size:13.5px;min-height:44px}
.lk-night .act.ghost{background:transparent;color:var(--n-ink);border-color:var(--n-line)}
.lk-night .intake-note{margin:0;font-size:12.5px;color:var(--n-mute)}
.lk-night .watchbox{border:1px solid var(--n-line);border-radius:14px;padding:12px 14px;background:rgba(10,16,30,.45)}
.lk-night .watchbox h2{margin:0 0 8px;font-size:11.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--n-mute)}
.lk-night .watch{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.lk-night .wi{width:100%;display:flex;gap:12px;align-items:center;text-align:left;border:0;border-radius:10px;padding:8px 10px;background:rgba(255,255,255,.04);color:var(--n-ink);min-height:44px}
.lk-night .wi i{flex:0 0 30px;height:30px;border-radius:8px;display:grid;place-items:center;font-style:normal;font-weight:700;border:1.5px dashed var(--n-ref);color:var(--n-ref)}
.lk-night .wi-manual i{border:1.5px solid var(--n-paper);color:var(--n-paper)} .lk-night .wi-none i{border:1.5px dotted var(--n-none);color:var(--n-none)}
.lk-night .wi b{display:block;font-size:13.5px} .lk-night .wi small{display:block;font-size:12px;color:var(--n-mute)}
.lk-night .campus{position:relative;border:1px solid var(--n-line);border-radius:18px;overflow:hidden;background:linear-gradient(180deg,rgba(10,16,30,0) 0%,rgba(10,16,30,.5) 100%)}
.lk-night .campus svg{display:block;width:100%;height:auto}
.lk-night .campus .hint{position:absolute;left:18px;top:14px;font-family:var(--f-hand);font-weight:700;font-size:26px;color:var(--n-lit);transform:rotate(-2deg);max-width:300px;line-height:1.05}
.lk-night .fl{cursor:pointer}
.lk-night .fl rect.w{fill:var(--n-off);transition:fill .25s}
.lk-night .fl.in rect.w{fill:var(--n-lit);filter:url(#nglow)}
.lk-night .fl.need:not(.in) rect.w{stroke:var(--n-none);stroke-width:1.5}
.lk-night .fl:hover rect.band,.lk-night .fl:focus rect.band{fill:rgba(246,195,91,.18)}
.lk-night .fl rect.band{fill:transparent}
.lk-night .fl.flick rect.w{animation:nflick .7s steps(4) 1}
@keyframes nflick{0%{fill:var(--n-off)}30%{fill:#FFF3C8}55%{fill:var(--n-off)}100%{fill:var(--n-lit)}}
.lk-night .ml{cursor:pointer}
.lk-night .ml circle.dot{stroke-width:2}
.lk-night .ml.yours circle.dot{fill:var(--n-lit);stroke:var(--n-lit);filter:url(#nglow)}
.lk-night .ml.ref circle.dot{fill:rgba(183,166,236,.25);stroke:var(--n-ref);stroke-dasharray:3 2;animation:npulse 2.6s ease-in-out infinite}
.lk-night .ml.manual circle.dot{fill:var(--n-paper);stroke:var(--n-paper)}
.lk-night .ml.none circle.dot{fill:none;stroke:var(--n-none)}
@keyframes npulse{0%,100%{opacity:.45}50%{opacity:1}}
.lk-night .plaque{cursor:pointer}
.lk-night .plaque rect{fill:#0B1222;stroke:var(--n-line)}
.lk-night .plaque:hover rect,.lk-night .plaque:focus rect{stroke:var(--n-lit)}
.lk-night .plaque text{fill:var(--n-ink);font-family:var(--f-body);font-size:13px;font-weight:600}
.lk-night .plaque text.c{fill:var(--n-mute);font-weight:400;font-size:11.5px}
.lk-night .legend{display:flex;flex-wrap:wrap;gap:8px 18px;padding:12px 18px;border-top:1px solid var(--n-line);font-size:12.5px;color:var(--n-mute)}
.lk-night .legend span{display:inline-flex;align-items:center;gap:7px}
.lk-night .legend i{display:inline-block;width:14px;height:10px;border-radius:2px}
.lk-night .fam{display:none;list-style:none;margin:12px 0 0;padding:0;gap:6px}
.lk-night .fam button{width:100%;display:grid;grid-template-columns:1fr auto;gap:2px 10px;text-align:left;border:1px solid var(--n-line);border-radius:10px;padding:10px 12px;background:rgba(10,16,30,.5);color:var(--n-ink);min-height:44px}
.lk-night .fam small{color:var(--n-mute);font-size:12px}
.lk-night .fam .bar{grid-column:1/-1;height:6px;border-radius:3px;background:var(--n-off);overflow:hidden}
.lk-night .fam .bar i{display:block;height:100%;background:var(--n-lit)}
.lk-night .cta{display:flex;flex-wrap:wrap;align-items:center;justify-content:flex-end;gap:10px 16px;margin-top:18px}
.lk-night .go{border:2px solid var(--n-line);background:transparent;color:var(--n-mute);border-radius:999px;padding:10px 22px;font-weight:600;font-size:15px;min-height:52px}
.lk-night .go.ready{background:var(--n-lit);border-color:var(--n-lit);color:#1B1406;box-shadow:0 0 30px rgba(246,195,91,.35)}
.lk-night .cta-note{font-size:13px;color:var(--n-mute);max-width:52ch}
@media (max-width:980px){.lk-night .top{grid-template-columns:1fr}.lk-night .mid{grid-template-columns:1fr}}
@media (max-width:700px){.lk-night .pulse{grid-template-columns:repeat(2,minmax(0,1fr))}.lk-night .pz{min-width:0}.lk-night .fam{display:grid}.lk-night .campus .hint{display:none}.lk-night .cta{justify-content:stretch}.lk-night .go{width:100%}}
`,
mount(stage){
  const G = 452, FH = 34, BW = 86, SW = 14, gap = 22, W = 30*2 + DOMAINS.length*(BW+SW+gap) - gap;
  let x = 30; const star = [];
  for (let i=0;i<70;i++){ const sx = (i*137.5)%W, sy = (i*61.3)%170+116; star.push(`<circle cx="${sx.toFixed(1)}" cy="${sy.toFixed(1)}" r="${i%7?0.9:1.6}" fill="#DCE3F5" opacity="${(0.25+((i*13)%10)/20).toFixed(2)}"/>`); }
  const blds = DOMAINS.map((d,di) => {
    const n = d.files.length, H = Math.max(2,n)*FH + 12, top = G - H, bx = x; x += BW + SW + gap;
    const floors = d.files.map((f,i) => { const fy = G - 12 - (i+1)*FH + 6;
      const w = [0,1,2].map(k => `<rect class="w" x="${bx+12+k*25}" y="${fy+6}" width="18" height="${FH-16}" rx="1.5"/>`).join("");
      return `<g class="fl${REQUIRED.includes(f)?" need":""}" data-file="${f}" data-ref="file:${f}" tabindex="0" role="button" aria-label="${esc(FILE_NAME[f])}"><rect class="band" x="${bx+4}" y="${fy}" width="${BW-8}" height="${FH-2}" rx="3"/>${w}</g>`; }).join("");
    const lights = d.ms.map((m,i) => { const lx = bx + 12 + i*((BW-24)/Math.max(1,d.ms.length-1||1)); const cx = d.ms.length===1? bx+BW/2 : lx;
      return `<g class="ml" data-ms="${m.id}" data-ref="ms:${m.id}" tabindex="0" role="button" aria-label="${esc(m.n)}"><line x1="${cx}" y1="${top-2}" x2="${cx}" y2="${top-16}" stroke="#4A5C82" stroke-width="2"/><circle class="dot" cx="${cx}" cy="${top-21}" r="6"/><circle cx="${cx}" cy="${top-21}" r="13" fill="transparent"/></g>`; }).join("");
    return `<g class="bld" data-dom="${d.id}">
      <polygon points="${bx+BW},${top} ${bx+BW+SW},${top-10} ${bx+BW+SW},${G-10} ${bx+BW},${G}" fill="var(--n-side)"/>
      <polygon points="${bx},${top} ${bx+SW},${top-10} ${bx+BW+SW},${top-10} ${bx+BW},${top}" fill="var(--n-roof)"/>
      <rect x="${bx}" y="${top}" width="${BW}" height="${H}" fill="var(--n-face)"/>
      ${d.id==="icu"?`<path d="M${bx+BW/2-7} ${top+10}h14M${bx+BW/2} ${top+3}v14" stroke="#E85D5D" stroke-width="4"/>`:""}
      ${floors}${lights}
      <g class="plaque" data-ref="dom:${d.id}" tabindex="0" role="button" aria-label="${esc(d.name)}"><rect x="${bx-4}" y="${G+14}" width="${BW+SW+8}" height="40" rx="8"/><text x="${bx+(BW+SW)/2}" y="${G+31}" text-anchor="middle">${esc(d.short)}</text><text class="c" data-v="dc-${d.id}" x="${bx+(BW+SW)/2}" y="${G+47}" text-anchor="middle"></text></g>
    </g>`; }).join("");
  stage.innerHTML = `<div class="lk lk-night">${journeyHTML()}
    <div class="top"><div><div class="eb">Simulation · step 1 of 8 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>Your hospital's <em>data</em></h1><p class="lede">Send what your systems and registers hold. Every floor that lights up is a file the formula can learn from; every dark one is filled from our reference files until it arrives.</p></div>${pulseHTML()}</div>
    <div class="mid">${intakeHTML()}<div class="watchbox"><h2>Dark windows that matter most</h2>${watchHTML()}</div></div>
    <div class="campus"><div class="hint" aria-hidden="true">dark floors = files not sent yet</div>
      <svg viewBox="0 110 ${W} 410" role="img" aria-label="The hospital campus: ten buildings, one per data family">
        <defs><filter id="nglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
        ${star.join("")}
        <path d="M0 ${G-60} L60 ${G-60} L60 ${G-110} L130 ${G-110} L130 ${G-80} L210 ${G-80} L210 ${G-140} L260 ${G-140} L260 ${G-70} L380 ${G-70} L380 ${G-120} L470 ${G-120} L470 ${G-90} L600 ${G-90} L600 ${G-150} L660 ${G-150} L660 ${G-75} L800 ${G-75} L800 ${G-130} L880 ${G-130} L880 ${G-95} L1010 ${G-95} L1010 ${G-140} L1090 ${G-140} L1090 ${G-70} L${W} ${G-70} L${W} ${G} L0 ${G}Z" fill="#172238" opacity=".8"/>
        <rect x="0" y="${G}" width="${W}" height="68" fill="#0B1222"/>
        <line x1="0" y1="${G+62}" x2="${W}" y2="${G+62}" stroke="#2A3858" stroke-width="2" stroke-dasharray="18 14"/>
        ${blds}
      </svg>
      <div class="legend"><span><i style="background:var(--n-lit)"></i>File in</span><span><i style="background:var(--n-off)"></i>Not sent</span><span><i style="background:var(--n-off);outline:1.5px solid var(--n-none)"></i>Needed to run</span><span><i style="background:var(--n-lit);border-radius:50%;width:10px"></i>Measure from your data</span><span><i style="border:1.5px dashed var(--n-ref);border-radius:50%;width:10px"></i>From reference</span><span><i style="background:var(--n-paper);border-radius:50%;width:10px"></i>On paper</span><span><i style="border:1.5px solid var(--n-none);border-radius:50%;width:10px"></i>Not recorded</span></div>
    </div>
    <ul class="fam" aria-label="Data families">${DOMAINS.map(d=>`<li><button type="button" data-ref="dom:${d.id}"><b>${esc(d.name)}</b><small data-v="fm-${d.id}"></small><span class="bar"><i data-bar="${d.id}"></i></span></button></li>`).join("")}</ul>
    ${ctaHTML()}</div>`;
  wireIntake(stage);
},
update(root, arrived){
  root.querySelectorAll("[data-file]").forEach(g => { const on = !!ST.files[g.dataset.file]; g.classList.toggle("in", on); });
  if (arrived){ const g = root.querySelector(`[data-file="${arrived}"]`); if (g){ g.classList.remove("flick"); void g.getBBox; g.classList.add("flick"); } }
  root.querySelectorAll(".ml").forEach(g => { g.setAttribute("class", "ml " + msState(MS[g.dataset.ms])); });
  DOMAINS.forEach(d => { const s = domStats(d); root.querySelectorAll(`[data-v="dc-${d.id}"]`).forEach(t => t.textContent = `${s.inn} of ${s.of} files`);
    root.querySelectorAll(`[data-v="fm-${d.id}"]`).forEach(t => t.textContent = `${s.inn}/${s.of} files · ${s.yours}/${s.msN} measures`);
    root.querySelectorAll(`[data-bar="${d.id}"]`).forEach(b => b.style.width = (s.cov*100)+"%"); });
}});
