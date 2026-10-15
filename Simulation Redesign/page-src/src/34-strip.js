/* ===== Option D · The trace: a printed ECG strip, one lead per data family; every file sent is a beat, every missing one a flat line ===== */
LOOKS.push({ key:"strip", letter:"D", name:"The trace", note:"<b>D · The trace.</b> A printed ECG strip on pink grid paper. Each lead is a data family. Every file that arrives prints a beat; a file not sent is a flat dashed line. At the end of each lead, its measures: a full square pulse from your data, a dashed one from reference, a short orange one kept on paper, a ring where nothing is recorded. The interpretation box reads it like the machine would.",
css:`
.lk-strip{--s-paper:#FFF3F1;--s-minor:#F5CFCB;--s-major:#EBA39C;--s-ink:#1B1B1F;--s-mute:#5C4D4D;--s-red:#C21F32;--s-ref:#6447A8;--s-paper2:#D86B0E;--s-sheet:#FFFCFB;
  --pk-bg:#1B1B1F;--pk-fg:#FFF3F1;--pk-line:#4A3A3A;--sh-bg:#FFFCFB;--sh-fg:#1B1B1F;--sh-mute:#5C4D4D;--sh-line:#EBCFCB;--sh-card:#fff;--c-ok:#1E6B45;--c-warn:#8A5A00;--c-bad:#C21F32;
  background-color:var(--s-paper);background-image:linear-gradient(var(--s-major) 1px,transparent 1px),linear-gradient(90deg,var(--s-major) 1px,transparent 1px),linear-gradient(var(--s-minor) 1px,transparent 1px),linear-gradient(90deg,var(--s-minor) 1px,transparent 1px);
  background-size:40px 40px,40px 40px,8px 8px,8px 8px;color:var(--s-ink);padding:18px clamp(16px,3vw,40px) 120px;min-height:100vh}
.lk-strip .jr ol{list-style:none;margin:0;padding:0;display:flex;gap:6px;overflow:auto;scrollbar-width:none}
.lk-strip .jr li{flex:0 0 auto}
.lk-strip .jr button{display:flex;align-items:center;gap:8px;border:1.5px solid var(--s-ink);background:var(--s-sheet);color:var(--s-mute);border-radius:4px;padding:5px 12px 5px 8px;min-height:44px}
.lk-strip .jr button b{font-family:var(--f-num);font-weight:400;font-size:22px;color:var(--s-ink)}
.lk-strip .jr button span{display:flex;flex-direction:column;align-items:flex-start;font-size:12.5px;font-weight:600;line-height:1.15}
.lk-strip .jr button small{font-weight:400;font-size:11px}
.lk-strip .jr .now button{border:2.5px solid var(--s-red);box-shadow:0 0 0 3px rgba(194,31,50,.15);color:var(--s-ink)}
.lk-strip .jr .now button b{color:var(--s-red)}
.lk-strip .jr button[aria-disabled]{cursor:default}
.lk-strip .hdr{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,560px);gap:16px 30px;align-items:end;margin:22px 0 14px}
.lk-strip .eb{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--s-mute)}
.lk-strip h1{font-family:var(--f-num);font-weight:400;font-size:clamp(46px,6vw,66px);line-height:.9;margin:6px 0 8px;text-wrap:balance}
.lk-strip h1 em{font-style:normal;color:var(--s-red)}
.lk-strip .lede{margin:0;max-width:60ch;color:var(--s-mute)}
.lk-strip .pulse{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:1.5px solid var(--s-ink);background:var(--s-sheet)}
.lk-strip .pz{text-align:left;border:0;border-right:1px solid var(--s-major);background:transparent;color:var(--s-ink);padding:8px 10px;min-height:44px}
.lk-strip .pz:last-child{border-right:0} .lk-strip .pz:hover{background:#FFE9E6}
.lk-strip .pz .pl{display:block;font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--s-mute)}
.lk-strip .pz b{display:block;font-family:var(--f-num);font-weight:400;font-size:32px;line-height:1;font-variant-numeric:tabular-nums}
.lk-strip .pz b i{font-style:normal;font-size:18px;color:var(--s-mute)}
.lk-strip .pz small{display:block;font-size:11px;color:var(--s-mute);line-height:1.3}
.lk-strip .row2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;margin-bottom:16px}
.lk-strip .intake{display:grid;gap:8px}
.lk-strip .drop{display:flex;flex-direction:column;gap:2px;border:2px dashed var(--s-red);border-radius:4px;padding:14px 16px;cursor:pointer;background:var(--s-sheet)}
.lk-strip .drop:hover,.lk-strip .drop:focus-within{background:#fff;box-shadow:0 0 0 4px rgba(194,31,50,.12)}
.lk-strip .dz-big{font-family:var(--f-num);font-size:28px;line-height:1;color:var(--s-red)}
.lk-strip .dz-sub{font-size:13px;color:var(--s-mute)}
.lk-strip .acts{display:flex;flex-wrap:wrap;gap:8px}
.lk-strip .act{border:1.5px solid var(--s-ink);background:var(--s-ink);color:var(--s-paper);border-radius:4px;padding:8px 14px;font-weight:600;font-size:13.5px;min-height:44px}
.lk-strip .act.ghost{background:var(--s-sheet);color:var(--s-ink)}
.lk-strip .intake-note{margin:0;font-size:12.5px;color:var(--s-mute)}
.lk-strip .interp{border:1.5px solid var(--s-ink);background:var(--s-sheet);padding:10px 14px}
.lk-strip .interp h2{margin:0 0 6px;font-size:11.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.lk-strip .interp .rhythm{margin:0 0 6px;font-size:13.5px;font-weight:600}
.lk-strip .watch{list-style:none;margin:0;padding:0;display:grid;gap:2px}
.lk-strip .wi{width:100%;display:grid;grid-template-columns:20px minmax(0,1fr);gap:8px;text-align:left;border:0;background:transparent;color:var(--s-ink);padding:6px 0;min-height:44px;border-top:1px dotted var(--s-major)}
.lk-strip .wi i{font-style:normal;font-weight:700;color:var(--s-red)}
.lk-strip .wi b{font-size:13.5px} .lk-strip .wi small{display:block;font-size:12px;color:var(--s-mute)}
.lk-strip .wi:hover b{text-decoration:underline}
.lk-strip .strip{position:relative;border:1.5px solid var(--s-ink);background:transparent;overflow:hidden}
.lk-strip .strip>svg{display:block;width:100%;height:auto}
.lk-strip .tr{fill:none;stroke:var(--s-ink);stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}
.lk-strip .flat{fill:none;stroke:var(--s-mute);stroke-width:1.6;stroke-dasharray:5 5}
.lk-strip .need .flat{stroke:var(--s-red)}
.lk-strip .bt{cursor:pointer}
.lk-strip .bt .hit{fill:transparent}
.lk-strip .bt:hover .hit,.lk-strip .bt:focus .hit{fill:rgba(194,31,50,.08)}
.lk-strip .bt .tr{display:none} .lk-strip .bt.in .tr{display:inline} .lk-strip .bt.in .flat{display:none}
.lk-strip .bt.draw .tr{stroke-dasharray:420;stroke-dashoffset:420;animation:sdraw .7s ease-out forwards}
@keyframes sdraw{to{stroke-dashoffset:0}}
.lk-strip .ld{cursor:pointer}
.lk-strip .ld rect{fill:var(--s-sheet);stroke:var(--s-ink);stroke-width:1.5}
.lk-strip .ld:hover rect,.lk-strip .ld:focus rect{fill:#fff;stroke:var(--s-red)}
.lk-strip .ld text.n{font-family:var(--f-num);font-size:22px;fill:var(--s-ink)}
.lk-strip .ld text.c{font-size:11px;fill:var(--s-mute)}
.lk-strip .cal{cursor:pointer}
.lk-strip .cal .hit{fill:transparent}
.lk-strip .cal path{fill:none;stroke-width:2.2}
.lk-strip .cal.yours path{stroke:var(--s-ink)} .lk-strip .cal.ref path{stroke:var(--s-ref);stroke-dasharray:4 3}
.lk-strip .cal.manual path{stroke:var(--s-paper2)} .lk-strip .cal.none path{stroke:var(--s-red)}
.lk-strip .cal .q{fill:none;stroke:var(--s-red);stroke-width:1.8;display:none} .lk-strip .cal.none .q{display:inline}
.lk-strip .cal:hover .hit,.lk-strip .cal:focus .hit{fill:rgba(194,31,50,.08)}
.lk-strip .sweep{fill:rgba(194,31,50,.10)}
.lk-strip .note{position:absolute;font-family:var(--f-hand);font-weight:700;font-size:24px;color:var(--s-red);line-height:1;pointer-events:none;transform:rotate(-3deg);white-space:nowrap}
.lk-strip .lg{display:flex;flex-wrap:wrap;gap:6px 18px;padding:8px 12px;border-top:1.5px solid var(--s-ink);background:var(--s-sheet);font-size:12.5px;color:var(--s-mute)}
.lk-strip .lg span{display:inline-flex;align-items:center;gap:6px}
.lk-strip .fam{display:none;list-style:none;margin:12px 0 0;padding:0;gap:6px}
.lk-strip .fam button{width:100%;display:grid;grid-template-columns:1fr auto;gap:2px 10px;text-align:left;border:1.5px solid var(--s-ink);border-radius:4px;padding:10px 12px;background:var(--s-sheet);color:var(--s-ink);min-height:44px}
.lk-strip .fam small{color:var(--s-mute);font-size:12px}
.lk-strip .cta{display:flex;flex-wrap:wrap;align-items:center;justify-content:flex-end;gap:10px 16px;margin-top:16px}
.lk-strip .go{border:2px solid var(--s-mute);background:var(--s-sheet);color:var(--s-mute);border-radius:4px;padding:10px 22px;font-weight:700;font-size:15px;min-height:52px}
.lk-strip .go.ready{background:var(--s-red);border-color:var(--s-red);color:#fff}
.lk-strip .cta-note{font-size:13px;color:var(--s-mute);max-width:52ch;background:var(--s-sheet);padding:2px 6px}
@media (prefers-reduced-motion:reduce){.lk-strip .sweep{display:none}}
@media (max-width:980px){.lk-strip .hdr{grid-template-columns:1fr}.lk-strip .row2{grid-template-columns:1fr}}
@media (max-width:700px){.lk-strip .pulse{grid-template-columns:1fr 1fr}.lk-strip .pz:nth-child(2){border-right:0}.lk-strip .pz:nth-child(-n+2){border-bottom:1px solid var(--s-major)}.lk-strip .fam{display:grid}.lk-strip .note{display:none}.lk-strip .go{width:100%}}
`,
mount(stage){
  const W = 1240, LH = 74, TOP = 14, X0 = 176, X1 = 980, M0 = 1004, M1 = W - 14, ROM = ["I","II","III","IV","V","VI","VII","VIII","IX","X"];
  const beat = (x, w, y) => { const u = w/40; // a P-QRS-T complex scaled to the segment
    const p = [[0,0],[5,0],[7,-3],[9,0],[13,0],[14,2],[16,-26],[18,8],[19.5,0],[24,0],[27,-6],[30,0],[40,0]];
    return "M" + p.map(([a,b]) => `${(x+a*u).toFixed(1)} ${(y+b*(LH/74)).toFixed(1)}`).join(" L"); };
  const rows = DOMAINS.map((d,i) => { const y0 = TOP + i*LH, base = y0 + LH*0.62, sw = (X1-X0)/d.files.length;
    const beats = d.files.map((f,j) => { const x = X0 + j*sw;
      return `<g class="bt${REQUIRED.includes(f)?" need":""}" data-file="${f}" data-ref="file:${f}" tabindex="0" role="button" aria-label="${esc(FILE_NAME[f])}"><rect class="hit" x="${x.toFixed(1)}" y="${y0+4}" width="${sw.toFixed(1)}" height="${LH-8}"/><path class="tr" d="${beat(x,Math.min(sw,150),base)}${sw>150?` L${(x+sw).toFixed(1)} ${base.toFixed(1)}`:""}"/><path class="flat" d="M${x.toFixed(1)} ${base.toFixed(1)} L${(x+sw).toFixed(1)} ${base.toFixed(1)}"/></g>`; }).join("");
    const mw = (M1-M0)/d.ms.length;
    const cals = d.ms.map((m,j) => { const x = M0 + j*mw;
      return `<g class="cal" data-ms="${m.id}" data-ref="ms:${m.id}" tabindex="0" role="button" aria-label="${esc(m.n)}"><rect class="hit" x="${x.toFixed(1)}" y="${y0+4}" width="${mw.toFixed(1)}" height="${LH-8}"/><path data-x="${x.toFixed(1)}" data-w="${mw.toFixed(1)}" data-b="${base.toFixed(1)}" d=""/><circle class="q" cx="${(x+mw/2).toFixed(1)}" cy="${(base-14).toFixed(1)}" r="6"/></g>`; }).join("");
    return `<g data-dom="${d.id}"><line x1="0" y1="${y0+LH}" x2="${W}" y2="${y0+LH}" stroke="var(--s-major)" stroke-width="1"/>
      <g class="ld" data-ref="dom:${d.id}" tabindex="0" role="button" aria-label="${esc(d.name)}"><rect x="10" y="${y0+10}" width="152" height="${LH-20}" rx="3"/><text class="n" x="20" y="${y0+36}">${ROM[i]} · ${esc(d.short)}</text><text class="c" data-v="sl-${d.id}" x="20" y="${y0+54}"></text></g>
      <line x1="${X0-6}" y1="${base}" x2="${X0}" y2="${base}" class="tr"/>${beats}<line x1="${X1}" y1="${base}" x2="${M0}" y2="${base}" class="tr" style="stroke-width:1.4"/>${cals}</g>`; }).join("");
  const H = TOP*2 + DOMAINS.length*LH;
  stage.innerHTML = `<div class="lk lk-strip">${journeyHTML()}
    <div class="hdr"><div><div class="eb">Simulation · step 1 of 8 · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>Your hospital's data, <em>read like a trace</em></h1><p class="lede">Ten leads, one per data family. A beat for every file that has arrived; a flat line for every one still to come. The formula runs on the beats and fills the flat lines from our reference files.</p></div>${pulseHTML()}</div>
    <div class="row2">${intakeHTML()}<div class="interp"><h2>Interpretation</h2><p class="rhythm" data-v="rhythm"></p>${watchHTML()}</div></div>
    <div class="strip"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Ten leads, one per data family">${rows}<line x1="${X1+12}" y1="0" x2="${X1+12}" y2="${H}" stroke="var(--s-ink)" stroke-width="1" stroke-dasharray="2 4"/><text x="${M0}" y="12" font-size="10.5" font-weight="600" fill="var(--s-mute)" letter-spacing="1.2">MEASURES</text><text x="${X0}" y="12" font-size="10.5" font-weight="600" fill="var(--s-mute)" letter-spacing="1.2">FILES</text><rect class="sweep" x="0" y="0" width="40" height="${H}"><animate attributeName="x" from="${X0}" to="${M1}" dur="9s" repeatCount="indefinite"/></rect></svg>
      <div class="note" aria-hidden="true"></div>
      <div class="lg"><span><svg width="30" height="14"><path d="M1 10 L9 10 L11 2 L13 12 L15 10 L29 10" fill="none" stroke="#1B1B1F" stroke-width="2"/></svg>File in</span><span><svg width="30" height="14"><path d="M1 7 L29 7" stroke="#5C4D4D" stroke-width="1.6" stroke-dasharray="5 5"/></svg>Not sent</span><span><svg width="30" height="14"><path d="M1 7 L29 7" stroke="#C21F32" stroke-width="1.6" stroke-dasharray="5 5"/></svg>Needed to run</span><span><svg width="22" height="14"><path d="M1 12 L5 12 L5 2 L15 2 L15 12 L21 12" fill="none" stroke="#1B1B1F" stroke-width="2"/></svg>Your data</span><span><svg width="22" height="14"><path d="M1 12 L5 12 L5 2 L15 2 L15 12 L21 12" fill="none" stroke="#6447A8" stroke-width="2" stroke-dasharray="4 3"/></svg>Reference</span><span><svg width="22" height="14"><path d="M1 12 L5 12 L5 8 L15 8 L15 12 L21 12" fill="none" stroke="#D86B0E" stroke-width="2"/></svg>On paper</span><span><svg width="22" height="14"><circle cx="11" cy="7" r="5" fill="none" stroke="#C21F32" stroke-width="1.8"/></svg>Not recorded</span></div></div>
    <ul class="fam" aria-label="Data families">${DOMAINS.map(d=>`<li><button type="button" data-ref="dom:${d.id}"><b>${esc(d.name)}</b><small data-v="sf-${d.id}"></small></button></li>`).join("")}</ul>
    ${ctaHTML()}</div>`;
  this._geo = { W, H, X0, X1 };
  wireIntake(stage);
},
update(root, arrived){
  root.querySelectorAll(".bt").forEach(g => { const on = !!ST.files[g.dataset.file]; g.classList.toggle("in", on); if (arrived && g.dataset.file===arrived){ g.classList.remove("draw"); void g.getBBox; g.classList.add("draw"); } });
  root.querySelectorAll(".cal").forEach(g => { const s = msState(MS[g.dataset.ms]); g.setAttribute("class", "cal " + s); const p = g.querySelector("path");
    const x = +p.dataset.x, w = +p.dataset.w, b = +p.dataset.b, h = s==="yours"||s==="ref" ? 26 : s==="manual" ? 12 : 0;
    p.setAttribute("d", `M${x} ${b} L${x+w*0.25} ${b} L${x+w*0.25} ${b-h} L${x+w*0.72} ${b-h} L${x+w*0.72} ${b} L${x+w} ${b}`); });
  DOMAINS.forEach(d => { const s = domStats(d); root.querySelectorAll(`[data-v="sl-${d.id}"],[data-v="sf-${d.id}"]`).forEach(t => t.textContent = `${s.inn}/${s.of} files · ${s.yours}/${s.msN} measures`); });
  const st = stats(); const flatFams = DOMAINS.filter(d => domStats(d).state!=="full").length;
  root.querySelector('[data-v="rhythm"]').textContent = st.filesIn===0 ? "No signal. Nothing has arrived yet." : flatFams ? `Regular beats on ${10-flatFams} of 10 leads; flat segments on ${flatFams}. ${st.months && st.months<12 ? `Short strip: ${st.months} month${st.months>1?"s":""} recorded.` : ""}` : `Beats on all ten leads.${st.months && st.months<12 ? ` Short strip: ${st.months} month${st.months>1?"s":""} recorded.` : ""}`;
  const note = root.querySelector(".note"), svg = root.querySelector(".strip svg"), first = root.querySelector(".bt:not(.in)");
  if (first && svg.clientWidth){ const sc = svg.clientWidth / this._geo.W, b = first.getBBox(); note.style.left = Math.min(svg.clientWidth-220, (b.x + 6)*sc) + "px"; note.style.top = Math.max(0, (b.y - 2)*sc) + "px"; note.textContent = "flat line: not sent yet"; note.hidden = false; }
  else note.hidden = true;
}});
