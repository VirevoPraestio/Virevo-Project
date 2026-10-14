/* ===== Page 4 · Option B · The plan table: the old page's table, made plain ===== */
LOOKS.push({ key:"plantable", page:"sim", step:3, letter:"B", name:"Plan table", note:"<b>B · Plan table.</b> Closest to the old page. One row per change, with its today, achievable and dream levels side by side; click the level you want to approve, or type your own. Cost and time sit on the same row. Your six stay frozen on the right; the plan's numbers sit across the top.",
css: SIM_CSS + `
.lk-web .tbl5{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);overflow-x:auto}
.lk-web .tbl5 table{width:100%;border-collapse:collapse;font-size:13px;min-width:720px}
.lk-web .tbl5 th{position:sticky;top:0;background:#F3F5F8;text-align:left;font-size:10.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--w-mute);padding:8px 10px;border-bottom:1.5px solid var(--w-line);z-index:1}
.lk-web .tbl5 td{padding:7px 10px;border-top:1px solid #E6EAF0;vertical-align:middle}
.lk-web .tbl5 tr.kh td{background:#F8FAFC;font-family:var(--f-num);font-size:20px;padding:8px 10px 4px}
.lk-web .tbl5 tr.off td.nmc .linkbtn b{color:var(--w-mute)}
.lk-web .tbl5 td.num5{font-family:var(--f-num);font-size:18px;white-space:nowrap}
.lk-web .lvb{border:1.5px solid var(--w-line);background:#fff;border-radius:8px;padding:4px 10px;min-height:38px;min-width:76px;font-family:var(--f-num);font-size:17px;white-space:nowrap;color:var(--w-ink)}
.lk-web .lvb[aria-pressed="true"]{background:var(--w-ink);border-color:var(--w-ink);color:#fff}
.lk-web .lvb.a[aria-pressed="true"]{background:var(--w-gold);border-color:var(--w-ink);color:var(--w-ink)}
.lk-web .lvb.o{min-width:0;font-family:var(--f-body);font-size:12px}
.lk-web .tbl5 .num{width:80px;min-height:38px}
.lk-web .tbl5 .own.on .num{border-color:var(--w-ink);background:#FFF7E3}
.lk-web .tbl5 .cl{display:block;max-width:220px}
`,
mount(stage){ levels5(); if (!Object.keys(SIMR.lvl).length) ch5().forEach(id => SIMR.lvl[id] = "ach");
  const row = id => { const it = ITEMS[id], L = LV[id];
    return `<tr data-row5="${id}"><td class="nmc">${nameBtn(id)}<br><small style="color:var(--w-mute);font-size:11.5px">${esc(unitOf(it)||(isSwitch(it)?"yes or no":""))}</small></td>
      <td class="num5">${esc(fmtV(id,it.t))}</td>
      <td><button type="button" class="lvb a" data-pick5="${id}:ach">${esc(lvLabel(id,L.ach))}</button></td>
      <td><button type="button" class="lvb" data-pick5="${id}:drm">${esc(lvLabel(id,L.drm))}</button></td>
      <td>${isSwitch(it)?"":`<span class="own"><input class="num" type="number" step="${stepOf(it)}" data-own5="${id}" aria-label="Your own level for ${esc(it.n)}"></span>`}</td>
      <td><button type="button" class="lvb o" data-pick5="${id}:off">Leave out</button></td>
      <td>${costLine5(id)}</td></tr>`; };
  const body = ["a","k","w","p"].map(k => { const ids = ch5().filter(id => leverKind(ITEMS[id])===k); return ids.length ? `<tr class="kh"><td colspan="7">${KINDNAME[k]}</td></tr>${ids.map(row).join("")}` : ""; }).join("");
  mount5(stage, `${simHead("Simulate your plan", "One row per change. Click the achievable or the dream level to approve it, type your own, or leave it out. The six on the right and the numbers at the top update as you go.")}
    ${topStrip5()}${bulk5()}<div class="sim5"><div class="tbl5"><table><thead><tr><th>Change</th><th>Today</th><th>Achievable</th><th>Dream</th><th>Your own</th><th></th><th>Cost and time</th></tr></thead><tbody>${body}</tbody></table></div>${kpiPanel5()}</div>`);
},
update(root){ sync5(root); root.querySelectorAll("tr[data-row5]").forEach(r => { const id = r.dataset.row5; r.querySelector(".own")?.classList.toggle("on", SIMR.lvl[id]==="own"); }); }
});
