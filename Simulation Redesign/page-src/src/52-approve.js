/* ===== Page 4 · Option A · Approval list: each change with its achievable and dream level, approve one, see the six on the right ===== */
LOOKS.push({ key:"apprlist", page:"sim", step:3, letter:"A", name:"Approval list", note:"<b>A · Approval list (revised 14 Oct).</b> The plan summary at the top and the Selected KPIs on the right both stay in view while you scroll. Each change has Not approved, Achievable, Dream, and Approve the Cost: units, unit cost and total cost. Picking Achievable or Dream fills these in. You can change any of them; the plan uses the total cost.",
css: SIM_CSS + `
.lk-web .grp5{border:2px solid var(--w-ink);border-radius:14px;background:var(--w-sheet);margin-bottom:14px;overflow:hidden}
.lk-web .grp5>h2{margin:0;padding:10px 16px;border-bottom:1.5px solid var(--w-line);background:#F3F5F8;font-family:var(--f-num);font-weight:400;font-size:24px;line-height:1}
.lk-web .grp5>h2 small{font-family:var(--f-body);font-size:12.5px;color:var(--w-mute);margin-left:8px}
.lk-web .r5{display:grid;grid-template-columns:minmax(150px,1fr) minmax(220px,1.1fr) minmax(250px,1.3fr);gap:8px 16px;align-items:center;padding:10px 16px;border-top:1px solid #E6EAF0}
.lk-web .grp5>h2+.r5{border-top:0}
.lk-web .r5.off .nm5 .linkbtn b{color:var(--w-mute)}
.lk-web .nm5{min-width:0;display:grid;gap:2px}
.lk-web .nm5 small{font-size:11.5px;color:var(--w-mute)}
@media (max-width:1300px){.lk-web .r5{grid-template-columns:1fr 1fr}.lk-web .r5 .nm5{grid-column:1/-1}}
@media (max-width:640px){.lk-web .r5{grid-template-columns:1fr}}
`,
mount(stage){ levels5(); ch5().forEach(id => { if (!(id in SIMR.lvl)) SIMR.lvl[id] = "ach"; });
  const row = id => { const c3 = cover3(); return `<div class="r5" data-row5="${id}"><div class="nm5">${nameBtn(id)}<small>Affects ${c3.lev[id]} selected KPI${c3.lev[id]>1?"s":""}</small>${costLine5(id)}</div>${choiceHTML(id)}</div>`; };
  const groups = ["a","k","w","p"].map(k => { const ids = ch5().filter(id => leverKind(ITEMS[id])===k); return ids.length ? `<section class="grp5"><h2>${KINDNAME[k]}<small>${ids.length}</small></h2>${ids.map(row).join("")}</section>` : ""; }).join("");
  mount5(stage, `${simHead("Simulate your plan", "Choose what to approve for each change. The KPIs on the right and the costs at the top update straight away.")}
    ${topStrip5()}${bulk5()}<div class="sim5"><div>${groups}</div>${kpiPanel5()}</div>`);
},
update(root){ sync5(root); }
});
