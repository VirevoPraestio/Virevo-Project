/* ===== Page 6 · fill the team from a file =====
   Download a template (CSV or Excel), fill in each head's name, designation and mobile, upload it back.
   The file is read in the browser: CSV directly; Excel (.xlsx) by opening the workbook (a zip) and reading
   the first sheet. Each row is matched to a department by its Department column, else by its Designation.
   Rows that cannot be matched are listed so the user can pick a department for them. */
const TCOLS = ["Department", "Designation", "Name", "Mobile"];
function templateRows6(){ const d = p6Data(); return d.depts.map(x => { const p = personOf(x.k); return [x.role, p.title || "", p.name || "", p.mobile || ""]; }); }

/* --- save a file: the page's downloads capability when published, a plain link otherwise --- */
async function saveFile6(filename, data){
  try { if (window.claude && claude.use) { const dl = await claude.use("downloads"); if (dl) { await dl.save({ filename, data }); toast(`${filename} saved.`); return; } } }
  catch (e) { if (e && e.code === "declined") return; if (e && e.code && !["unavailable","not_granted","capability_disabled","capability_removed"].includes(e.code)) { toast("That file could not be saved here."); return; } }
  const blob = data instanceof Blob ? data : new Blob([data]); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = filename; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000); }

/* --- CSV --- */
const csvCell = v => /[",\n]/.test(v) ? `"${String(v).replace(/"/g, '""')}"` : String(v);
function templateCSV6(){ return "﻿" + [TCOLS, ...templateRows6()].map(r => r.map(csvCell).join(",")).join("\r\n") + "\r\n"; }
function parseCSV6(text){ const rows = []; let row = [], cell = "", q = false; text = text.replace(/^﻿/, "");
  for (let i = 0; i < text.length; i++){ const ch = text[i];
    if (q) { if (ch === '"') { if (text[i+1] === '"') { cell += '"'; i++; } else q = false; } else cell += ch; }
    else if (ch === '"') q = true; else if (ch === ",") { row.push(cell); cell = ""; } else if (ch === "\n" || ch === "\r") { if (ch === "\r" && text[i+1] === "\n") i++; row.push(cell); rows.push(row); row = []; cell = ""; } else cell += ch; }
  if (cell !== "" || row.length) { row.push(cell); rows.push(row); } return rows.filter(r => r.some(c => c.trim() !== "")); }

/* --- a small zip writer (stored, no compression) for the Excel template --- */
const CRC_T = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++){ let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
const crc32 = b => { let c = 0xFFFFFFFF; for (let i = 0; i < b.length; i++) c = CRC_T[(c ^ b[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
function zipStore(files){ const enc = new TextEncoder(), parts = [], cen = []; let off = 0;
  files.forEach(([name, text]) => { const nb = enc.encode(name), db = enc.encode(text), crc = crc32(db);
    const h = new DataView(new ArrayBuffer(30)); h.setUint32(0,0x04034b50,true); h.setUint16(4,20,true); h.setUint16(8,0,true); h.setUint16(10,0,true); h.setUint16(12,0x21,true); h.setUint32(14,crc,true); h.setUint32(18,db.length,true); h.setUint32(22,db.length,true); h.setUint16(26,nb.length,true);
    parts.push(new Uint8Array(h.buffer), nb, db);
    const c = new DataView(new ArrayBuffer(46)); c.setUint32(0,0x02014b50,true); c.setUint16(4,20,true); c.setUint16(6,20,true); c.setUint16(14,0x21,true); c.setUint32(16,crc,true); c.setUint32(20,db.length,true); c.setUint32(24,db.length,true); c.setUint16(28,nb.length,true); c.setUint32(42,off,true);
    cen.push(new Uint8Array(c.buffer), nb); off += 30 + nb.length + db.length; });
  const cenLen = cen.reduce((a,b)=>a+b.length,0), e = new DataView(new ArrayBuffer(22)); e.setUint32(0,0x06054b50,true); e.setUint16(8,files.length,true); e.setUint16(10,files.length,true); e.setUint32(12,cenLen,true); e.setUint32(16,off,true);
  return new Blob([...parts, ...cen, new Uint8Array(e.buffer)]); }
const xmlEsc = s => String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
function templateXLSX6(){ const rows = [TCOLS, ...templateRows6()], L = i => String.fromCharCode(65 + i);
  const sheet = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><cols><col min="1" max="1" width="32" customWidth="1"/><col min="2" max="2" width="30" customWidth="1"/><col min="3" max="3" width="28" customWidth="1"/><col min="4" max="4" width="18" customWidth="1"/></cols><sheetData>${rows.map((r,i) => `<row r="${i+1}">${r.map((v,j) => `<c r="${L(j)}${i+1}" t="inlineStr"${i===0?' s="1"':""}><is><t>${xmlEsc(v)}</t></is></c>`).join("")}</row>`).join("")}</sheetData></worksheet>`;
  return zipStore([
    ["[Content_Types].xml", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>`],
    ["_rels/.rels", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`],
    ["xl/workbook.xml", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Team" sheetId="1" r:id="rId1"/></sheets></workbook>`],
    ["xl/_rels/workbook.xml.rels", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`],
    ["xl/styles.xml", `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts><fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs></styleSheet>`],
    ["xl/worksheets/sheet1.xml", sheet] ]); }

/* --- read an Excel workbook: find the zip entries, inflate them, read the first sheet --- */
async function unzipEntries(buf){ const v = new DataView(buf), u8 = new Uint8Array(buf), dec = new TextDecoder(); let e = -1;
  for (let i = buf.byteLength - 22; i >= Math.max(0, buf.byteLength - 66000); i--) if (v.getUint32(i, true) === 0x06054b50) { e = i; break; }
  if (e < 0) throw new Error("not a zip"); const n = v.getUint16(e + 10, true); let p = v.getUint32(e + 16, true); const out = {};
  for (let k = 0; k < n; k++){ const method = v.getUint16(p + 10, true), csize = v.getUint32(p + 20, true), nl = v.getUint16(p + 28, true), xl = v.getUint16(p + 30, true), cl = v.getUint16(p + 32, true), lo = v.getUint32(p + 42, true);
    const name = dec.decode(u8.subarray(p + 46, p + 46 + nl)); out[name] = { method, csize, lo }; p += 46 + nl + xl + cl; }
  const read = async name => { const f = out[name]; if (!f) return null; const lnl = v.getUint16(f.lo + 26, true), lxl = v.getUint16(f.lo + 28, true), s = f.lo + 30 + lnl + lxl, raw = u8.slice(s, s + f.csize);
    if (f.method === 0) return dec.decode(raw);
    if (f.method !== 8 || typeof DecompressionStream === "undefined") throw new Error("cannot open");
    const ds = new Blob([raw]).stream().pipeThrough(new DecompressionStream("deflate-raw")); return await new Response(ds).text(); };
  return { names: Object.keys(out), read }; }
async function parseXLSX6(buf){ const z = await unzipEntries(buf), P = s => new DOMParser().parseFromString(s, "application/xml");
  const sheetName = z.names.filter(n => /^xl\/worksheets\/sheet\d+\.xml$/.test(n)).sort((a,b) => parseInt(a.match(/\d+/)) - parseInt(b.match(/\d+/)))[0]; if (!sheetName) throw new Error("no sheet");
  const ssx = await z.read("xl/sharedStrings.xml"), shared = ssx ? [...P(ssx).getElementsByTagName("si")].map(si => [...si.getElementsByTagName("t")].map(t => t.textContent).join("")) : [];
  const doc = P(await z.read(sheetName)), rows = [];
  [...doc.getElementsByTagName("row")].forEach(r => { const row = [];
    [...r.getElementsByTagName("c")].forEach(c => { const ref = c.getAttribute("r") || "", col = ref.replace(/\d+/g, "").split("").reduce((a,ch) => a*26 + ch.charCodeAt(0) - 64, 0) - 1, t = c.getAttribute("t");
      const vEl = c.getElementsByTagName("v")[0]; let val = "";
      if (t === "s") val = shared[+(vEl?.textContent || 0)] || ""; else if (t === "inlineStr") val = [...c.getElementsByTagName("t")].map(x => x.textContent).join(""); else val = vEl ? vEl.textContent : "";
      if (/^\d+(\.\d+)?E\+?\d+$/i.test(val)) val = String(Math.round(Number(val)));
      row[col >= 0 ? col : row.length] = val; });
    rows.push([...row].map(x => x ?? "")); });
  return rows.filter(r => r.some(c => String(c).trim() !== "")); }

/* --- match rows to departments --- */
const DEPT_WORDS = { owner:["owner","ceo","chief executive","managing director","chairman","founder","promoter","\\bmd\\b"], medical_dir:["medical director","medical superintendent","\\bms\\b","\\bcmo\\b","chief medical"],
  nursing:["nursing","\\bcno\\b","matron"], icu:["\\bicu\\b","critical care","intensiv"], pharmacy:["pharma"], coo:["\\bcoo\\b","operations","administrator","\\bgm\\b","general manager","hospital admin"],
  biomedical:["biomed","bio-med","bio med","clinical engineering"], housekeeping:["housekeep","\\bhk\\b"], cssd:["cssd","steril"], finance:["\\bcfo\\b","finance","accounts","\\bbilling\\b"],
  procurement:["procure","purchase","materials","\\bstores\\b","supply chain"], marketing:["marketing","business development","\\bbd\\b","sales"], hr:["\\bhr\\b","human resource","people"], it:["\\bit\\b","information tech","\\bcio\\b","\\bsystems\\b","\\bhis\\b"] };
function matchDept6(...texts){ for (const t0 of texts){ const t = String(t0 || "").toLowerCase().trim(); if (!t) continue;
    const exact = DEPT_ORDER.find(k => DEPTS[k][0].toLowerCase() === t || k === t); if (exact) return exact;
    for (const k of DEPT_ORDER) if (DEPT_WORDS[k].some(w => new RegExp(w, "i").test(t))) return k; } return null; }
function colIndex6(head){ const h = head.map(x => String(x).toLowerCase()), f = re => h.findIndex(x => re.test(x));
  return { dept: f(/dep(t|art)|function|unit/), desig: f(/design|title|role|position/), name: f(/name/), mobile: f(/mobile|phone|contact|cell|whatsapp/) }; }
const TFILE = { last:null, unmatched:[] };
function applyRows6(rows, fileName){ if (!rows.length) { toast("That file is empty."); return; }
  let head = rows[0], ix = colIndex6(head), body = rows.slice(1);
  if (ix.name < 0) { ix = { dept:0, desig:1, name:2, mobile:3 }; body = rows; }   /* no header row: assume the template's order */
  const d = p6Data(), needed = new Set(d.depts.map(x => x.k)), got = [], un = [], extra = [];
  body.forEach(r => { const g = i => i >= 0 ? String(r[i] ?? "").trim() : ""; const row = { dept:g(ix.dept), title:g(ix.desig), name:g(ix.name), mobile:g(ix.mobile).replace(/[^\d+ ]/g, "") };
    if (!row.name && !row.mobile) return; const k = matchDept6(row.dept, row.title);
    if (!k) { un.push(row); return; } TEAM.people[k] = { name: row.name || personOf(k).name || "", mobile: row.mobile || personOf(k).mobile || "", title: row.title || personOf(k).title || "" }; got.push(k); if (!needed.has(k)) extra.push(k); });
  TEAM.done = null; TFILE.unmatched = un;
  TFILE.last = { file: fileName, read: got.length + un.length, matched: got.length, extra: extra.length, missing: d.depts.filter(x => !named(x.k)).length };
  mountLook(LOOKS.indexOf(CUR)); }
async function readTeamFile6(file){ const name = file.name || "file", low = name.toLowerCase();
  try { if (low.endsWith(".csv") || low.endsWith(".txt")) applyRows6(parseCSV6(await file.text()), name);
    else if (low.endsWith(".xlsx")) applyRows6(await parseXLSX6(await file.arrayBuffer()), name);
    else if (low.endsWith(".xls")) toast("That is an old Excel file (.xls). Save it as .xlsx or .csv and upload again.");
    else toast("Upload a .csv or .xlsx file."); }
  catch (e) { toast("That file could not be read. Use the template, saved as .xlsx or .csv."); } }
function p6_dropFiles(files){ const f = files.find(x => /\.(csv|xlsx|xls|txt)$/i.test(x.name)); if (f) readTeamFile6(f); else toast("Drop a .csv or .xlsx file with the team's details."); }

/* --- the panel --- */
function teamFileHTML6(){ return `<section class="tf6" data-noopen aria-label="Fill the team from a file"><div class="tf6-t"><h2>Fill from a file</h2><p>Have a staff list? Download the template, add each head's name, designation and mobile, and upload it here. You can also drop the file on this box.</p></div>
  <div class="tf6-b"><button type="button" class="act" data-tf="csv">Download CSV template</button><button type="button" class="act" data-tf="xlsx">Download Excel template</button>
  <label class="go ready tf6-up"><input type="file" accept=".csv,.xlsx,.xls,text/csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" data-tfin> Upload filled file</label></div>
  <div class="tf6-r" data-v="tf6r" role="status" aria-live="polite"></div></section>`; }
function wireTeamFile6(root){
  root.querySelectorAll("[data-tf]").forEach(b => b.addEventListener("click", async e => { e.stopPropagation(); const day = new Date().toISOString().slice(0,10), base = `team-template-${day}`;
    if (b.dataset.tf === "csv") await saveFile6(base + ".csv", templateCSV6()); else await saveFile6(base + ".xlsx", templateXLSX6()); }));
  root.querySelectorAll("[data-tfin]").forEach(n => n.addEventListener("change", () => { const f = n.files && n.files[0]; if (f) readTeamFile6(f); n.value = ""; }));
  const box = root.querySelector(".tf6"); if (box) { box.addEventListener("dragover", e => { e.preventDefault(); box.classList.add("over"); }); box.addEventListener("dragleave", () => box.classList.remove("over"));
    box.addEventListener("drop", e => { e.preventDefault(); e.stopPropagation(); box.classList.remove("over"); document.body.classList.remove("dropping"); const fs = [...(e.dataTransfer?.files || [])]; if (fs.length) p6_dropFiles(fs); }); }
  root.querySelectorAll("[data-unm]").forEach(s => s.addEventListener("change", () => { const i = +s.dataset.unm, r = TFILE.unmatched[i]; if (!r || !s.value) return;
    TEAM.people[s.value] = { name: r.name, mobile: r.mobile, title: r.title }; TFILE.unmatched.splice(i, 1); mountLook(LOOKS.indexOf(CUR)); }));
}
function syncTeamFile6(root){ const el = root.querySelector('[data-v="tf6r"]'); if (!el) return; const L = TFILE.last;
  if (!L) { el.innerHTML = ""; return; }
  el.innerHTML = `<p><b>${esc(L.file)}</b>: ${L.read} row${L.read===1?"":"s"} read, ${L.matched} matched to a department${L.extra ? ` (${L.extra} not needed for this plan, kept anyway)` : ""}. ${L.missing ? `${L.missing} department${L.missing===1?" is":"s are"} still empty.` : "Every department now has a name."}</p>
    ${TFILE.unmatched.length ? `<p>These rows did not match a department. Pick one for each:</p><ul class="un6">${TFILE.unmatched.map((r,i) => `<li><span><b>${esc(r.name || "No name")}</b>${r.title ? ` · ${esc(r.title)}` : ""}${r.dept ? ` · ${esc(r.dept)}` : ""}</span><select data-unm="${i}" aria-label="Department for ${esc(r.name)}"><option value="">Pick a department</option>${DEPT_ORDER.map(k => `<option value="${k}">${esc(DEPTS[k][0])}</option>`).join("")}</select></li>`).join("")}</ul>` : ""}`;
  el.querySelectorAll("[data-unm]").forEach(s => s.addEventListener("change", () => { const i = +s.dataset.unm, r = TFILE.unmatched[i]; if (!r || !s.value) return; TEAM.people[s.value] = { name: r.name, mobile: r.mobile, title: r.title }; TFILE.unmatched.splice(i, 1); mountLook(LOOKS.indexOf(CUR)); })); }
