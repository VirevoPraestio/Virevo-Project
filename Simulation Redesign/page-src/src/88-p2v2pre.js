/* page 2 (revised): example targets, refresh on change, and review-only buttons to change which files are in */
Object.assign(TS.user, EXAMPLE_SET2);
p2listeners.push(() => refresh(null));
(function(){ const box = document.querySelector(".rvtools"); if (!box) return;
  box.insertAdjacentHTML("beforeend", `<span>Files in:</span><button type="button" data-rvd="p1">As on page 1 (38)</button><button type="button" data-rvd="all">All 51</button><button type="button" data-rvd="req">Only the 15 the formula needs</button>`);
  box.querySelectorAll("[data-rvd]").forEach(b => b.onclick = () => { const m = b.dataset.rvd; ST.files = {};
    if (m==="all") sampleFiles(ALL_FILES); else if (m==="req") sampleFiles(REQUIRED.concat(["dim_procedures","dim_beds","dim_equipment","dim_drugs"]).filter((v,i,a)=>a.indexOf(v)===i)); else sampleFiles(ALL_FILES.filter(f => !HELD_BACK.includes(f)));
    mountLook(LOOKS.indexOf(CUR)); toast(`${Object.keys(ST.files).length} files in. The page now shows ${counts().all} parameters.`); }); })();
