/* ===== Option C · The records room: a steel cabinet, one drawer per data family, a folder per file, a stamp per measure ===== */
LOOKS.push({ key:"records", letter:"C", name:"Records room", note:"<b>C · Records room.</b> A register and a steel cabinet. Each drawer is a data family; each folder standing in it is a file that has arrived, and each empty slot one still to come. Every measure carries a stamp: Your data, Reference, On paper or Not recorded. Flat frame, heavy rules, ledger lines.",
css:`
.lk-records{--r-ground:#E2E4DE;--r-paper:#F7F6F1;--r-ink:#151515;--r-mute:#4F534C;--r-steel:#5B6658;--r-steel2:#46503F;--r-manila:#E2C27C;--r-manila2:#C9A65A;--r-yours:#17633F;--r-ref:#5B3E9C;--r-paper2:#8E2433;--r-none:#6B6B6B;--r-hl:#F2C230;
  --pk-bg:#151515;--pk-fg:#F7F6F1;--pk-line:#3A3A3A;--pk-r:0;--sh-bg:#F7F6F1;--sh-fg:#151515;--sh-mute:#4F534C;--sh-line:#CFCFC6;--sh-card:#fff;--sh-r:0;--c-ok:#17633F;--c-warn:#8A5B00;--c-bad:#8E2433;
  background:var(--r-ground);color:var(--r-ink);padding:18px clamp(16px,3vw,40px) 120px;min-height:100vh}
.lk-records .jr ol{list-style:none;margin:0;padding:0;display:flex;gap:4px;overflow:auto;border-bottom:3px solid var(--r-ink);scrollbar-width:none}
.lk-records .jr li{flex:0 0 auto}
.lk-records .jr button{display:flex;align-items:center;gap:8px;border:2px solid var(--r-ink);border-bottom:0;background:var(--r-paper);color:var(--r-mute);padding:6px 12px;min-height:44px;margin-top:6px}
.lk-records .jr button b{font-family:var(--f-num);font-weight:400;font-size:22px;color:var(--r-ink)}
.lk-records .jr button span{display:flex;flex-direction:column;align-items:flex-start;font-size:12.5px;font-weight:600;line-height:1.15}
.lk-records .jr button small{font-weight:400;font-size:11px}
.lk-records .jr .now button{background:var(--r-ink);color:var(--r-paper);margin-top:0;padding-top:12px}
.lk-records .jr .now button b{color:var(--r-hl)}
.lk-records .jr button[aria-disabled]{cursor:default}
.lk-records .mast{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px 30px;align-items:end;padding:22px 0 14px;border-bottom:1.5px solid var(--r-ink)}
.lk-records .eb{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--r-mute)}
.lk-records h1{font-family:var(--f-num);font-weight:400;font-size:clamp(46px,6vw,66px);line-height:.9;margin:6px 0 0;text-wrap:balance}
.lk-records .regno{font-family:var(--f-num);font-size:22px;letter-spacing:.06em;border:3px solid var(--r-ink);padding:4px 12px;transform:rotate(-2deg);background:var(--r-paper)}
.lk-records .lede{margin:12px 0 0;max-width:68ch;color:var(--r-mute)}
.lk-records .pulse{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-bottom:4px double var(--r-ink);margin-bottom:22px}
.lk-records .pz{text-align:left;border:0;border-right:1.5px solid var(--r-ink);background:transparent;color:var(--r-ink);padding:12px 14px;min-height:44px}
.lk-records .pz:last-child{border-right:0}
.lk-records .pz:hover{background:rgba(242,194,48,.25)}
.lk-records .pz .pl{display:block;font-size:10.5px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--r-mute)}
.lk-records .pz b{display:block;font-family:var(--f-num);font-weight:400;font-size:40px;line-height:1;font-variant-numeric:tabular-nums}
.lk-records .pz b i{font-style:normal;font-size:22px;color:var(--r-mute)}
.lk-records .pz small{display:block;font-size:11.5px;color:var(--r-mute)}
.lk-records .sec{display:grid;grid-template-columns:44px minmax(0,1fr);gap:0 14px;margin-bottom:22px}
.lk-records .sec>.no{font-family:var(--f-num);font-size:40px;line-height:.9;border-top:3px solid var(--r-ink);padding-top:6px}
.lk-records .sec>div{border-top:1.5px solid var(--r-ink);padding-top:8px;min-width:0}
.lk-records .sec h2{margin:0 0 10px;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.lk-records .two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px}
.lk-records .intake{display:grid;gap:8px}
.lk-records .drop{display:flex;flex-direction:column;gap:2px;border:2px solid var(--r-ink);padding:16px;cursor:pointer;background:repeating-linear-gradient(0deg,var(--r-paper) 0 27px,#E5E3D8 27px 28px)}
.lk-records .drop:hover,.lk-records .drop:focus-within{background:repeating-linear-gradient(0deg,#FFFDF4 0 27px,#E5E3D8 27px 28px);box-shadow:6px 6px 0 var(--r-ink)}
.lk-records .dz-big{font-family:var(--f-num);font-size:30px;line-height:1}
.lk-records .dz-sub{font-size:13px;color:var(--r-mute)}
.lk-records .acts{display:flex;flex-wrap:wrap;gap:8px}
.lk-records .act{border:2px solid var(--r-ink);background:var(--r-ink);color:var(--r-paper);padding:8px 14px;font-weight:600;font-size:13.5px;min-height:44px}
.lk-records .act.ghost{background:transparent;color:var(--r-ink)}
.lk-records .intake-note{margin:0;font-size:12.5px;color:var(--r-mute)}
.lk-records .receipt{background:var(--r-paper);padding:12px 14px 18px;position:relative;--z:linear-gradient(135deg,var(--r-ground) 6px,transparent 0) 0 100%/12px 12px repeat-x,linear-gradient(-135deg,var(--r-ground) 6px,transparent 0) 0 100%/12px 12px repeat-x;background:var(--z),var(--r-paper)}
.lk-records .watch{list-style:none;margin:0;padding:0;display:grid}
.lk-records .wi{width:100%;display:grid;grid-template-columns:24px minmax(0,1fr);gap:10px;text-align:left;border:0;border-bottom:1.5px dashed #B9B7AC;background:transparent;color:var(--r-ink);padding:9px 0;min-height:44px}
.lk-records .wi i{font-style:normal;font-family:var(--f-num);font-size:20px;color:var(--r-paper2)}
.lk-records .wi b{display:flex;gap:6px;font-size:13.5px}
.lk-records .wi b::after{content:"";flex:1;border-bottom:2px dotted #8C8A80;transform:translateY(-4px)}
.lk-records .wi small{display:block;font-size:12px;color:var(--r-mute)}
.lk-records .wi:hover b{text-decoration:underline}
.lk-records .cab{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;background:var(--r-steel2);padding:10px;border:3px solid var(--r-ink)}
.lk-records .drw{display:flex;flex-direction:column;background:linear-gradient(180deg,var(--r-steel) 0%,#525D4F 100%);border:2px solid #2E352B;min-width:0}
.lk-records .folders{display:flex;gap:3px;align-items:flex-end;height:46px;padding:0 10px;background:#2E352B;border-bottom:3px solid #20261E}
.lk-records .fo{flex:1;min-width:0;height:28px;border:0;padding:0;background:transparent;position:relative;cursor:pointer}
.lk-records .fo::before{content:"";position:absolute;inset:0;border:1.5px dashed #7D8775;border-bottom:0}
.lk-records .fo.in::before{border:0;background:linear-gradient(180deg,var(--r-manila) 0%,var(--r-manila2) 100%);clip-path:polygon(0 30%,35% 30%,45% 0,100% 0,100% 100%,0 100%)}
.lk-records .fo.in{height:38px}
.lk-records .fo.need:not(.in)::before{border-color:#E89A9A}
.lk-records .fo.drop-in{animation:rdrop .5s cubic-bezier(.3,1.4,.6,1)}
@keyframes rdrop{0%{transform:translateY(-30px);opacity:0}100%{transform:none;opacity:1}}
.lk-records .front{padding:10px 10px 12px;display:flex;flex-direction:column;gap:8px;flex:1}
.lk-records .holder{display:block;width:100%;text-align:left;border:2px solid #20261E;background:var(--r-paper);color:var(--r-ink);padding:6px 8px;cursor:pointer}
.lk-records .holder:hover,.lk-records .holder:focus{background:#fff;outline:3px solid var(--r-hl)}
.lk-records .holder b{display:block;font-family:var(--f-num);font-weight:400;font-size:22px;line-height:1;letter-spacing:.02em}
.lk-records .holder small{display:block;font-size:11.5px;color:var(--r-mute);font-variant-numeric:tabular-nums}
.lk-records .handle{height:9px;margin:0 auto;width:46%;border:3px solid #20261E;border-top:0;border-radius:0 0 6px 6px}
.lk-records .slips{list-style:none;margin:0;padding:0;display:grid;gap:4px}
.lk-records .slip{width:100%;display:grid;grid-template-columns:minmax(0,1fr);text-align:left;border:0;background:#EDEBE2;color:var(--r-ink);padding:5px 7px 6px;font-size:12px;line-height:1.25;cursor:pointer;position:relative}
.lk-records .slip:hover,.lk-records .slip:focus{background:#fff}
.lk-records .slip .st{justify-self:start;margin-top:3px;font-size:9.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;border:1.5px solid currentColor;padding:0 4px;transform:rotate(-2deg)}
.lk-records .slip.yours .st{color:var(--r-yours)} .lk-records .slip.ref .st{color:var(--r-ref);border-style:dashed}
.lk-records .slip.manual .st{color:var(--r-paper2)} .lk-records .slip.none .st{color:var(--r-none)} .lk-records .slip.none span{text-decoration:line-through;text-decoration-color:#9A9A9A}
.lk-records .lg{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:10px;font-size:12.5px;color:var(--r-mute)}
.lk-records .cta{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;margin-top:6px}
.lk-records .go{border:3px solid var(--r-ink);background:transparent;color:var(--r-mute);padding:10px 22px;font-weight:700;font-size:15px;min-height:52px;letter-spacing:.02em}
.lk-records .go.ready{background:var(--r-hl);color:var(--r-ink);box-shadow:6px 6px 0 var(--r-ink)}
.lk-records .cta-note{font-size:13px;color:var(--r-mute);max-width:56ch}
@media (max-width:1100px){.lk-records .cab{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:820px){.lk-records .two{grid-template-columns:1fr}.lk-records .mast{grid-template-columns:1fr}.lk-records .regno{justify-self:start}}
@media (max-width:700px){.lk-records .cab{grid-template-columns:repeat(2,minmax(0,1fr))}.lk-records .pulse{grid-template-columns:1fr 1fr}.lk-records .pz:nth-child(2){border-right:0}.lk-records .pz:nth-child(-n+2){border-bottom:1.5px solid var(--r-ink)}.lk-records .sec{grid-template-columns:30px minmax(0,1fr);gap:0 10px}.lk-records .sec>.no{font-size:30px}.lk-records .go{width:100%}}
@media (max-width:420px){.lk-records .cab{grid-template-columns:1fr}}
`,
mount(stage){
  const drawers = DOMAINS.map(d => `<div class="drw" data-dom="${d.id}">
    <div class="folders">${d.files.map(f=>`<button type="button" class="fo${REQUIRED.includes(f)?" need":""}" data-file="${f}" data-ref="file:${f}" aria-label="${esc(FILE_NAME[f])}"></button>`).join("")}</div>
    <div class="front"><button type="button" class="holder" data-ref="dom:${d.id}"><b>${esc(d.name)}</b><small data-v="rc-${d.id}"></small></button><div class="handle" aria-hidden="true"></div>
      <ul class="slips">${d.ms.map(m=>`<li><button type="button" class="slip" data-ms="${m.id}" data-ref="ms:${m.id}"><span>${esc(m.n)}</span><em class="st"></em></button></li>`).join("")}</ul></div></div>`).join("");
  stage.innerHTML = `<div class="lk lk-records">${journeyHTML()}
    <div class="mast"><div><div class="eb">Simulation · register of records · ${esc(HOSPITAL.name)}, ${HOSPITAL.beds} beds</div><h1>Your hospital's data</h1><p class="lede">Every number the formula uses is filed here with where it came from. A folder for each file you send; a stamp on each measure saying whether it is your data, a reference value, kept on paper, or not recorded at all.</p></div><div class="regno">Step 1 of 8</div></div>
    ${pulseHTML()}
    <div class="sec"><div class="no">1</div><div><h2>Send your files</h2><div class="two">${intakeHTML()}<div class="receipt"><h2>Outstanding, by weight on your KPIs</h2>${watchHTML()}</div></div></div></div>
    <div class="sec"><div class="no">2</div><div><h2>The cabinet: ten drawers, one per data family</h2><div class="cab">${drawers}</div>
      <div class="lg"><span><b style="color:var(--r-manila2)">▮</b> Folder: file in</span><span><b style="color:#7D8775">▯</b> Empty slot: not sent</span><span><b style="color:#E89A9A">▯</b> Needed to run</span><span style="color:var(--r-yours);font-weight:600">YOUR DATA</span><span style="color:var(--r-ref);font-weight:600">REFERENCE</span><span style="color:var(--r-paper2);font-weight:600">ON PAPER</span><span style="color:var(--r-none);font-weight:600">NOT RECORDED</span></div></div></div>
    <div class="sec"><div class="no">3</div><div><h2>Build the formula</h2>${ctaHTML()}</div></div>
  </div>`;
  wireIntake(stage);
},
update(root, arrived){
  root.querySelectorAll(".fo").forEach(b => { const on = !!ST.files[b.dataset.file]; b.classList.toggle("in", on); if (arrived && b.dataset.file===arrived){ b.classList.remove("drop-in"); void b.offsetWidth; b.classList.add("drop-in"); } });
  root.querySelectorAll(".slip").forEach(b => { const s = msState(MS[b.dataset.ms]); b.className = "slip " + s; b.querySelector(".st").textContent = SRC_SHORT[s]; });
  DOMAINS.forEach(d => { const s = domStats(d); root.querySelectorAll(`[data-v="rc-${d.id}"]`).forEach(t => t.textContent = `${s.inn} of ${s.of} files · ${s.yours} of ${s.msN} measures yours`); });
}});
