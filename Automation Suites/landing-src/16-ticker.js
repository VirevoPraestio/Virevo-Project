/* live "posted today" counter shared by the Billing & Insurance options */
function tickEngine(px, sel){
  const ev = [[2,"Lab · CBC",450,"Bed 214"],[1,"Bed-day · Twin room",4200,"Bed 118"],[7,"Visit · Cardiology",1200,"Bed 305"],[2,"Lab · Lipid profile",900,"Bed 221"],[7,"Visit · Gen Med",800,"Bed 112"],[1,"Transfer · ICU out",0,"Bed 402"],[2,"Lab · Culture",1450,"Bed 117"]];
  let amt = 1842300, cnt = 1284, i = 0; const fa = document.getElementById(px+"amt"), fc = document.getElementById(px+"cnt"), fl = document.getElementById(px+"last");
  if (!fa) return;
  const t = setInterval(() => { if (!fa.isConnected) return clearInterval(t); const e = ev[i++ % ev.length]; amt += e[2]; cnt += 1;
    fa.textContent = "₹" + amt.toLocaleString("en-IN"); if (fc) fc.textContent = cnt.toLocaleString("en-IN") + " charges"; if (fl) fl.textContent = `${e[1]} · ₹${e[2].toLocaleString("en-IN")} · ${e[3]}`;
    const g = document.querySelector(`${sel}[data-part="${e[0]}"]`); if (g) { g.classList.remove("ping"); void g.getBBox(); g.classList.add("ping"); } }, 2200);
}

/* admissions ticker for the Admission Process looks */
function admitTicker(px, sel){
  const ev = [["Bed 118",38,9],["Bed 305",52,12],["ICU 4",44,9],["Bed 221",29,12],["Bed 112",61,9]];
  let n = D.today.admitted, i = 0; const fa = document.getElementById(px+"amt"), fl = document.getElementById(px+"last");
  if (!fa) return;
  const t = setInterval(() => { if (!fa.isConnected) return clearInterval(t); const e = ev[i++ % ev.length]; n += 1;
    fa.textContent = n; if (fl) fl.textContent = `last: ${e[0]} · ${e[1]} min`;
    const g = document.querySelector(`${sel}[data-part="${e[2]}"]`); if (g) { g.classList.remove("ping"); void g.getBBox(); g.classList.add("ping"); } }, 6000);
}

/* tests-done-here ticker for the Diagnostic Scheduling looks */
function testTicker(px, sel){
  const ev = [["Ultrasound","OPD 7",3,4,0.012],["Lab samples","OPD 2",1,7,0.004],["CT","OPD 11",6,6,0.045],["X-ray","OPD 4",2,4,0.006],["MRI 1","OPD 9",9,6,0.06]];
  let done = D.opd.doneHere, i = 0; const fa = document.getElementById(px+"amt"), fp = document.getElementById(px+"pct"), fb = document.getElementById(px+"bar"), fl = document.getElementById(px+"last");
  if (!fa) return; const full = fb ? +fb.dataset.full || 116 : 0;
  const t = setInterval(() => { if (!fa.isConnected) return clearInterval(t); const e = ev[i++ % ev.length]; done = Math.round((done + e[4])*100)/100;
    fa.textContent = "₹" + done.toFixed(2) + " L"; const pc = Math.round(done / D.opd.prescribedToday * 100);
    if (fp) fp.textContent = pc + "% done here"; if (fb) fb.setAttribute("width", (full*pc/100).toFixed(1)); if (fl) fl.textContent = `last: ${e[0]} for ${e[1]} slotted in ${e[2]} min`;
    const g = document.querySelector(`${sel}[data-part="${e[3]}"]`); if (g) { g.classList.remove("ping"); void g.getBBox(); g.classList.add("ping"); } }, 4500);
}

/* bought-today ticker for the Procurement looks */
function buyTicker(px, sel){
  const ev = [["PO 7713 · syringes 5 ml",0.18,1,0],["Rushed buy · IV sets, Ward 4 (signed)",0.04,7,1],["PO 7714 · surgical gowns",0.31,1,0],["Bill 2290 · sutures, ₹1,800 above price",0.22,3,2],["Top-up · Ward 2 gloves",0.06,6,0],["PO 7715 · ceftriaxone",0.27,2,0]];
  let amt = D.month.boughtToday, above = D.month.aboveToday, i = 0; const fa = document.getElementById(px+"amt"), fb = document.getElementById(px+"above"), fl = document.getElementById(px+"last");
  if (!fa) return;
  const t = setInterval(() => { if (!fa.isConnected) return clearInterval(t); const e = ev[i++ % ev.length]; amt = Math.round((amt + e[1])*100)/100; if (e[3]===2) above = Math.round((above + 0.02)*100)/100;
    fa.textContent = "₹" + amt.toFixed(2) + " L"; if (fb) fb.textContent = "₹" + above.toFixed(2) + " L above price"; if (fl) fl.textContent = "last: " + e[0];
    const g = document.querySelector(`${sel}[data-part="${e[2]}"]`); if (g) { g.classList.remove("ping"); void g.getBBox(); g.classList.add("ping"); } }, 4000);
}
