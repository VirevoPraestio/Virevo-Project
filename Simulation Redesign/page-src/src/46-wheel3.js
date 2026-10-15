/* ===== Page 3 · Option B · The wheel: KPIs on the inner ring, the changes on the outer ring; your six light their paths ===== */
LOOKS.push({ key:"wheel3", page:"p3", step:2, letter:"B", name:"The wheel", note:"<b>B · The wheel.</b> The page-1 wheel turned toward the plan. KPIs sit on the inner ring by department; the changes the hospital can make sit on the outer ring. Pick a KPI and gold lines run to every change that affects it. A change reached by several of your six grows larger, so you can see where your six overlap and which corners of the hospital they leave out.",
css: P3_CSS + `
.lk-web .w3{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:22px;align-items:start}
.lk-web .w3wheel{position:relative;border:2px solid var(--w-ink);border-radius:18px;background:var(--w-sheet);box-shadow:8px 8px 0 rgba(22,33,62,.12)}
.lk-web .w3wheel>svg{display:block;width:100%;height:auto}
.lk-web .w3wheel .hand{position:absolute;left:18px;top:14px;font-family:var(--f-hand);font-weight:700;font-size:24px;color:var(--w-gold-ink);transform:rotate(-2deg);max-width:220px;line-height:1.05}
.lk-web .w3e{fill:none;stroke:var(--w-gold);stroke-width:1.8;opacity:.85}
.lk-web .k3{cursor:pointer}
.lk-web .k3 circle.d{fill:#fff;stroke:var(--w-ink);stroke-width:2}
.lk-web .k3.on circle.d{fill:var(--w-ink);stroke:var(--w-gold);stroke-width:3}
.lk-web .k3.nod circle.d{stroke-dasharray:3 2.5}
.lk-web .k3 text{font-size:13px;fill:var(--w-ink);font-family:var(--f-body)}
.lk-web .k3.on text{font-weight:700}
.lk-web .l3{cursor:pointer}
.lk-web .l3 .s{fill:#fff;stroke:#9AA5B8;stroke-width:1.6}
.lk-web .l3.on .s{fill:var(--w-gold);stroke:var(--w-ink)}
.lk-web .l3 text{font-size:13px;fill:var(--w-mute);font-family:var(--f-body)}
.lk-web .l3.on text{fill:var(--w-ink);font-weight:600}
.lk-web .sec3 path{fill:none;stroke:#E3E8EF;stroke-width:26}
.lk-web .sec3 text{font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;fill:var(--w-ink)}
.lk-web .core3 circle{fill:var(--w-ink)} .lk-web .core3 text{fill:#fff;font-family:var(--f-num)}
.lk-web .six{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);padding:14px;position:sticky;top:calc(12px + env(safe-area-inset-top,0px))}
.lk-web .six h2{margin:0 0 8px;font-family:var(--f-num);font-weight:400;font-size:28px;line-height:1}
.lk-web .six ol{list-style:none;margin:0 0 10px;padding:0;display:grid;gap:6px}
.lk-web .six li{display:grid;grid-template-columns:30px minmax(0,1fr) 34px;gap:8px;align-items:center;border:1.5px dashed var(--w-line);border-radius:10px;padding:6px 8px;min-height:52px}
.lk-web .six li.full{border:1.5px solid var(--w-ink);background:#fff}
.lk-web .six li .n{font-family:var(--f-num);font-size:24px;color:#C9D0DA;text-align:center}
.lk-web .six li.full .n{color:var(--w-gold)}
.lk-web .six li small{display:block;font-size:11.5px;color:var(--w-mute)}
.lk-web .six li .x{width:32px;height:32px;border-radius:50%;border:1.5px solid var(--w-line);background:#fff;color:var(--w-ink)}
.lk-web .six .acts3{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.lk-web .six .kinds3{display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12.5px}
.lk-web .six .kinds3 div{border:1px solid var(--w-line);border-radius:8px;padding:6px 8px;background:#F6F8FA}
.lk-web .six .kinds3 b{display:block;font-family:var(--f-num);font-weight:400;font-size:22px;line-height:1}
.lk-web .fam3{display:none;margin-top:12px}
.lk-web .fam3 h3{margin:12px 0 6px;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.lk-web .fam3 .r{display:flex;justify-content:space-between;gap:8px;align-items:center;padding:6px 0;border-top:1px solid #E6EAF0}
@media (max-width:1100px){.lk-web .w3{grid-template-columns:1fr}.lk-web .six{position:static}}
@media (max-width:700px){.lk-web .fam3{display:block}.lk-web .k3 text,.lk-web .l3 text,.lk-web .w3wheel .hand{display:none}}
`,
mount(stage){
  const S = 1200, C = S/2, RK = 288, RL = 392, RS = 338;
  const pt = (r,a) => [C + r*Math.cos(a), C + r*Math.sin(a)];
  const pool = poolIds(); const byG = P3G.map(g => pool.filter(id => ITEMS[id].g===g));
  const gapA = 0.12, step = (2*Math.PI - gapA*P3G.length) / pool.length; let a = -Math.PI/2 + gapA/2; const KA = {}, secs = [];
  byG.forEach((ids,gi) => { const a0 = a; ids.forEach(id => { KA[id] = a + step/2; a += step; }); secs.push([P3G[gi], a0, a]); a += gapA; });
  const levs = CATALOGUE.filter(c => isLever(c) && isShown(c.id)).map(c=>c.id); const LA = {};
  levs.forEach((id,i) => LA[id] = -Math.PI/2 + (i+.5)*2*Math.PI/levs.length);
  this.geo = { pt, RK, RL, KA, LA };
  const sec = secs.map(([g,a0,a1]) => { const p0 = pt(RS,a0), p1 = pt(RS,a1), large = (a1-a0)>Math.PI?1:0, flip = Math.sin((a0+a1)/2) > .1; const t0 = pt(RS, flip?a1:a0), t1 = pt(RS, flip?a0:a1);
    return `<g class="sec3"><path d="M${p0[0].toFixed(1)} ${p0[1].toFixed(1)} A${RS} ${RS} 0 ${large} 1 ${p1[0].toFixed(1)} ${p1[1].toFixed(1)}"/><path id="s3-${g}" fill="none" stroke="none" d="M${t0[0].toFixed(1)} ${t0[1].toFixed(1)} A${RS} ${RS} 0 ${large} ${flip?0:1} ${t1[0].toFixed(1)} ${t1[1].toFixed(1)}"/><text dy="4.5"><textPath href="#s3-${g}" startOffset="50%" text-anchor="middle">${esc(GNAME[g])}</textPath></text></g>`; }).join("");
  const kn = pool.map(id => { const ang = KA[id], [x,y] = pt(RK, ang), right = Math.cos(ang) >= 0, [lx,ly] = pt(RK-14, ang), n = ITEMS[id].n;
    return `<g class="k3${hasData(id)?"":" nod"}" data-k3="${id}" data-ref="it:${id}" tabindex="0" role="button" aria-label="${esc(n)}"><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="15" fill="transparent"/><circle class="d" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="8"/>
      <text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" dy="4" text-anchor="${right?"end":"start"}" transform="rotate(${(right?ang:ang+Math.PI)*180/Math.PI} ${lx.toFixed(1)} ${ly.toFixed(1)})">${esc(n.length>26?n.slice(0,25)+"…":n)}</text></g>`; }).join("");
  const ln = levs.map(id => { const ang = LA[id], [x,y] = pt(RL, ang), right = Math.cos(ang) >= 0, [lx,ly] = pt(RL+16, ang), it = ITEMS[id], k = leverKind(it);
    const sh = k==="p" ? `<circle class="s" data-r cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="7"/>` : k==="k" ? `<rect class="s" x="${(x-7).toFixed(1)}" y="${(y-7).toFixed(1)}" width="14" height="14" rx="2"/>` : k==="w" ? `<rect class="s" x="${(x-6).toFixed(1)}" y="${(y-6).toFixed(1)}" width="12" height="12" transform="rotate(45 ${x.toFixed(1)} ${y.toFixed(1)})"/>` : `<rect class="s" x="${(x-10).toFixed(1)}" y="${(y-6).toFixed(1)}" width="20" height="12" rx="6" style="stroke:${it.c||"#9AA5B8"}"/>`;
    return `<g class="l3" data-l3="${id}" data-ref="it:${id}" tabindex="0" role="button" aria-label="${esc(it.n)}"><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="14" fill="transparent"/>${sh}<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" dy="4" text-anchor="${right?"start":"end"}" transform="rotate(${(right?ang:ang+Math.PI)*180/Math.PI} ${lx.toFixed(1)} ${ly.toFixed(1)})">${esc(it.n.length>26?it.n.slice(0,25)+"…":it.n)}</text></g>`; }).join("");
  const fam = P3G.map((g,gi) => byG[gi].length ? `<h3>${esc(GNAME[g])}</h3>${byG[gi].map(id => `<div class="r">${nameBtn(id)}<button type="button" class="pick3" data-pick3="${id}" aria-pressed="false">Pick</button></div>`).join("")}` : "").join("");
  p3Mount(stage, `${p3Head("Pick six KPIs to steer by", "Click a KPI on the inner ring to pick it. Gold lines show every change on the outer ring that affects it; those are the changes the simulation will move.")}
    <div class="w3"><div><div class="w3wheel"><div class="hand" aria-hidden="true">bigger = reached by more of your six</div>
      <svg viewBox="0 0 ${S} ${S}" role="img" aria-label="KPIs on the inner ring, the changes that affect them on the outer ring"><g data-v="e3"></g>${sec}${ln}${kn}<g class="core3"><circle cx="${C}" cy="${C}" r="56"/><text x="${C}" y="${C-4}" text-anchor="middle" font-size="20">YOUR SIX</text><text x="${C}" y="${C+22}" text-anchor="middle" font-size="26" data-v="core3"></text></g></svg></div>
      <div class="fam3">${fam}</div></div>
      <aside class="six" aria-label="Your six"><h2>Your six</h2><ol data-v="six"></ol>
        <div class="acts3"><button type="button" class="act" data-p3="suggest">Let Tojo suggest six</button><button type="button" class="act ghost" data-p3="clear">Clear</button></div>
        <div class="kinds3" data-v="kinds3"></div><div style="margin-top:12px">${p3Cta()}</div></aside></div>`);
  stage.querySelectorAll("[data-k3]").forEach(g => g.addEventListener("click", e => { if (e.target.closest("[data-k3]")) { e.stopPropagation(); toggle3(g.dataset.k3); } }));
  stage.querySelectorAll("[data-k3]").forEach(g => g.addEventListener("keydown", e => { if (e.key==="Enter"||e.key===" ") { e.preventDefault(); toggle3(g.dataset.k3); } }));
},
update(root){ p3Sync(root); const c = cover3(), { pt, RK, RL, KA, LA } = this.geo;
  root.querySelectorAll("[data-k3]").forEach(g => g.classList.toggle("on", S3.sel.includes(g.dataset.k3)));
  root.querySelectorAll("[data-l3]").forEach(g => { const n = c.lev[g.dataset.l3]||0; g.classList.toggle("on", n>0); const s = g.querySelector(".s"); s.style.transformOrigin = "center"; s.style.transformBox = "fill-box"; s.style.transform = `scale(${1 + Math.min(4,n)*0.22})`; });
  root.querySelector('[data-v="e3"]').innerHTML = S3.sel.flatMap(k => leversOf(k).filter(l=>LA[l]!==undefined).map(l => { const [x1,y1] = pt(RK, KA[k]), [x2,y2] = pt(RL, LA[l]), [cx,cy] = pt((RK+RL)/2*0.55, (KA[k]+LA[l])/2);
    return `<path class="w3e" d="M${x1.toFixed(1)} ${y1.toFixed(1)} Q${pt(RK*0.2,KA[k])[0].toFixed(1)} ${pt(RK*0.2,KA[k])[1].toFixed(1)} ${x2.toFixed(1)} ${y2.toFixed(1)}"/>`; })).join("");
  root.querySelector('[data-v="core3"]').textContent = `${S3.sel.length} / 6`;
  root.querySelector('[data-v="six"]').innerHTML = Array.from({length:6},(_,i) => { const id = S3.sel[i]; if (!id) return `<li><span class="n">${i+1}</span><span style="font-size:12.5px;color:var(--w-mute)">Pick a KPI on the wheel</span><span></span></li>`;
    return `<li class="full"><span class="n">${i+1}</span><span>${nameBtn(id)}<small>${esc(GNAME[ITEMS[id].g])} · ${leversOf(id).length} changes${hasData(id)?"":" · no data yet"}</small></span><button type="button" class="x" data-pick3="${id}" data-keep="1" aria-label="Remove ${esc(ITEMS[id].n)}">×</button></li>`; }).join("");
  root.querySelectorAll('[data-v="six"] [data-pick3]').forEach(b => b.addEventListener("click", e => { e.stopPropagation(); toggle3(b.dataset.pick3); }));
  const byK = { a:0, k:0, w:0, p:0 }; Object.keys(c.lev).forEach(l => byK[leverKind(ITEMS[l])]++);
  root.querySelector('[data-v="kinds3"]').innerHTML = Object.entries(byK).map(([k,n]) => `<div><b>${n}</b>${KINDNAME[k]}</div>`).join("");
  root.querySelectorAll(".fam3 .pick3").forEach(b => b.textContent = S3.sel.includes(b.dataset.pick3) ? "Picked ✓" : "Pick");
}});
