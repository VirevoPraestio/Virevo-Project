#!/usr/bin/env python3
"""Build the simulation review pages.  python3 build.py [options|approved]
options  -> out/sim-p1-options.html   (all four page-1 looks, kept as the record of the choice)
approved -> out/sim-pages.html        (the approved look only; grows page by page)
Each also writes a .preview.html with local fonts (set FONTS to the font folder)."""
import os, sys, glob, json
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, "src")
FONTS = os.environ.get("FONTS", "/tmp/claude-0/fonts")
BUILDS = {
  "options":  dict(out="sim-p1-options", looks=sorted(os.path.basename(p) for p in glob.glob(os.path.join(S, "3[0-9]-*.js"))),
                   page=dict(title="Simulation · page 1 of 8 · Your data · options", sub="Four options for the first page. Each is live: drop real CSVs to see it fill. Option B was chosen on 13 Oct 2026.", only=["night","web","records","strip"])),
  "p2":       dict(out="sim-p2-options", pre=["11-targets.js"], looks=["32-web.js", "21-p2.js", "40-p2base.js", "41-board.js", "42-ladders.js", "43-tiers.js", "89-p2pre.js"],
                   page=dict(title="Simulation · page 2 of 8 · Targets · options", sub="Three options for setting targets, in the approved One formula look. Each is live: move pins, tap marks, type numbers.", rvtools=False, only=["board","ladders","tiers"])),
  "p2v2":     dict(out="sim-p2-board", pre=["12-catalogue.js"], looks=["32-web.js", "40-p2base.js", "22-p2v2.js", "44-board2.js", "88-p2v2pre.js"],
                   page=dict(title="Simulation · page 2 of 8 · Targets · Measuring board, revised", sub="Revised 13 Oct: grouped by department, shown according to the hospital's data, plain English throughout. Live: move pins, type numbers, flip switches.", rvtools=True, only=["board2"])),
  "p3":       dict(out="sim-p3-options", pre=["12-catalogue.js"], looks=["32-web.js", "40-p2base.js", "22-p2v2.js", "44-board2.js", "23-p3.js", "45-seats.js", "46-wheel3.js", "47-sets.js", "88-p2v2pre.js", "87-p3pre.js"],
                   page=dict(title="Simulation · page 3 of 8 · Six KPIs · options", sub="Three options for picking the six KPIs the plan is steered by, in the approved One formula look. Targets carry over from page 2.", only=["seats","wheel3","sets"])),
  "p4":       dict(out="sim-p4-options", pre=["12-catalogue.js"], looks=["32-web.js", "40-p2base.js", "22-p2v2.js", "44-board2.js", "23-p3.js", "45-seats.js", "24-p4.js", "48-desk.js", "49-chain.js", "50-year.js", "88-p2v2pre.js", "86-p4pre.js"],
                   page=dict(title="Simulation · page 4 of 8 · Simulate · options", sub="Three options for simulating the plan, in the approved One formula look. The six KPIs are Tojo's balanced six; levels start from the page-2 targets.", only=["desk","chain","year"])),
  "sim":      dict(out="sim-p4-sim", pre=["12-catalogue.js", "13-costs.js"], looks=["32-web.js", "40-p2base.js", "22-p2v2.js", "44-board2.js", "23-p3.js", "45-seats.js", "25-sim.js", "51-simbase.js", "52-approve.js", "88-p2v2pre.js", "85-simpre.js"],
                   page=dict(title="Simulation · page 4 of 7 · Simulate · Approval list, revised", sub="Revised 14 Oct: plan summary and Selected KPIs stay in view while scrolling; every change has Approve the Cost (units, unit cost, total cost); plain wording throughout.", only=["apprlist"])),
  "simopts":  dict(out="sim-p4-sim-options", pre=["12-catalogue.js", "13-costs.js"], looks=["32-web.js", "40-p2base.js", "22-p2v2.js", "44-board2.js", "23-p3.js", "45-seats.js", "25-sim.js", "51-simbase.js", "52-approve.js", "53-table.js", "54-bykpi.js", "88-p2v2pre.js", "85-simpre.js"],
                   page=dict(title="Simulation · page 4 of 7 · Simulate · options (rebuilt)", sub="Record of the three rebuilt treatments. Option A, Approval list, was chosen on 14 Oct.", only=["apprlist","plantable","bykpi"])),
  "p5":       dict(out="sim-p5-options", pre=["12-catalogue.js", "13-costs.js"], looks=["32-web.js", "40-p2base.js", "22-p2v2.js", "44-board2.js", "23-p3.js", "45-seats.js", "25-sim.js", "26-p5.js", "51-simbase.js", "55-p5.js", "88-p2v2pre.js", "84-p5pre.js"],
                   page=dict(title="Simulation · page 5 of 7 · Freeze · options", sub="Three options for checking and confirming the plan frozen on Simulate. The sample plan is Tojo's balanced six with every change approved at Achievable.", rvtools=False, only=["p5sheet","p5ba","p5time"])),
  "p6":       dict(out="sim-p6-options", pre=["12-catalogue.js", "13-costs.js"], looks=["32-web.js", "40-p2base.js", "22-p2v2.js", "44-board2.js", "23-p3.js", "45-seats.js", "25-sim.js", "26-p5.js", "27-p6.js", "28-teamfile.js", "51-simbase.js", "55-p5.js", "56-p6.js", "88-p2v2pre.js", "84-p5pre.js", "83-p6pre.js"],
                   page=dict(title="Simulation · page 6 of 7 · Your team · options", sub="Three options for naming the head of each department and who leads each change. Option C, Team chart, was chosen on 14 Oct and now takes a CSV or Excel team list.", rvtools=False, only=["p6cards","p6list","p6org"])),
  "approved": dict(out="sim-pages", pre=["12-catalogue.js", "13-costs.js"], looks=["32-web.js", "40-p2base.js", "22-p2v2.js", "44-board2.js", "23-p3.js", "45-seats.js", "25-sim.js", "26-p5.js", "27-p6.js", "28-teamfile.js", "51-simbase.js", "52-approve.js", "55-p5.js", "56-p6.js", "88-p2v2pre.js", "85-simpre.js", "84-p5pre.js", "83-p6pre.js"],
                   page=dict(title="Simulation · approved pages", sub="Approved so far: page 1, Your data (One formula, 13 Oct); page 2, Targets (Measuring board, 13 Oct); page 3, Six KPIs (Six seats, 14 Oct); page 4, Simulate (Approval list, 14 Oct); page 5, Freeze (Month by month, 14 Oct); page 6, Your team (Team chart with file upload, 14 Oct). Pick a page above, or use the step bar on the page.", only=["web","board2","seats","apprlist","p5time","p6org"], byPage=True)),
  "product":  dict(out="tojo-simulation", doctitle="Tojo Simulation", pre=["12-catalogue.js", "13-costs.js"], looks=["32-web.js", "40-p2base.js", "22-p2v2.js", "44-board2.js", "23-p3.js", "45-seats.js", "25-sim.js", "26-p5.js", "27-p6.js", "28-teamfile.js", "51-simbase.js", "52-approve.js", "55-p5.js", "56-p6.js", "88-p2v2pre.js", "85-simpre.js"],
                   page=dict(title="Tojo Simulation", sub="", product=True, byPage=True, rvtools=False, only=["web","board2","seats","apprlist","p5time","p6org"])),
}
def read(f): return open(os.path.join(S, f), encoding="utf-8").read()
def build(name):
    b = BUILDS[name]
    head = read("00-head.html").replace("/*@@SUITE_BASE@@*/", read("suite-base.css"))
    if b.get("doctitle"): head = head.replace("<title>Simulation Page Options</title>", "<title>" + b["doctitle"] + "</title>")
    js = "\n".join(read(f) for f in ["10-data.js"] + b.get("pre", []) + ["20-runtime.js"] + b["looks"])
    js += "\nconst PAGE = " + json.dumps(b["page"], ensure_ascii=False) + ";\n" + read("90-init.js")
    page = head + "<script>\n" + js + "\n</script>\n"
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    open(os.path.join(HERE, "out", b["out"] + ".html"), "w", encoding="utf-8").write(page)
    faces = "".join(f'@font-face{{font-family:"{a}";font-weight:{w};src:url(file://{FONTS}/{f})}}' for a, w, f in [
      ("Bebas Neue", 400, "bebas-neue-latin-400-normal.woff2"), ("Caveat", "500 700", "caveat-latin-700-normal.woff2"),
      ("Poppins", 400, "poppins-latin-400-normal.woff2"), ("Poppins", 500, "poppins-latin-500-normal.woff2"),
      ("Poppins", 600, "poppins-latin-600-normal.woff2"), ("Poppins", 700, "poppins-latin-700-normal.woff2")])
    prev = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>' + faces + "</style></head><body>" + "\n".join(l for l in page.split("\n") if "fonts.g" not in l) + "</body></html>"
    open(os.path.join(HERE, "out", b["out"] + ".preview.html"), "w", encoding="utf-8").write(prev)
    print(name, len(page))
for n in (sys.argv[1:] or BUILDS): build(n)
