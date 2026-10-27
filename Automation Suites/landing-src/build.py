#!/usr/bin/env python3
"""Build suite pages from the shared runtime.  python3 build.py [name ...]  (no name = all)
Each build: page shell + data files + runtime + look files + PAGE config. Writes out/<name>.html
and out/<name>.preview.html (local fonts, for screenshots)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = ["10-data.js", "12-data-billing.js", "13-data-admission.js", "14-data-diagnostic.js", "18-data-procurement.js", "19-data-financial.js"]
RUNTIME = ["15-helpers.js", "16-ticker.js", "20-shared.js", "25-fh.js"]
FONTS = "/mnt/user-data/uploads/Discharge/tojo-html/diagnosis-html-generator/assets/fonts"
SUB = "Example figures for a 250-bed hospital in Bhubaneswar."
BUILDS = {
  "discharge":  dict(title="Discharge Summary Suite Landings", looks=["33-diorama.js"],
                     page=dict(mode="review", suite="discharge", schemes=["diorama"], title="Discharge Summary · suite landing", sub="Approved look: the hospital diorama. " + SUB)),
  "billing":    dict(title="Billing &amp; Insurance Suite", looks=["38-sorter.js"],
                     page=dict(mode="review", suite="billing", schemes=["sorter"], title="Billing & Insurance · suite landing", sub="Approved look: olive and marigold. Every event in the stay is charged the moment it is recorded. " + SUB)),
  "admission":  dict(title="Admission Process Suite", looks=["40-radar.js"],
                     page=dict(mode="review", suite="admission", schemes=["radar"], title="Admission Process · suite landing", sub="Approved look: indigo and sunflower. The right patient in the right bed, called in before the bed is free. " + SUB)),
  "diagnostic": dict(title="Diagnostic Scheduling Suite", looks=["41-dayboard.js"],
                     page=dict(mode="review", suite="diagnostic", schemes=["dayboard"], title="Diagnostic Scheduling · suite landing", sub="Approved look: magenta and sky. Every prescribed test slotted the moment it is written, and done here. " + SUB)),
  "procurement": dict(title="Procurement Suite", looks=["44-lines.js"],
                     page=dict(mode="review", suite="procurement", schemes=["lines"], title="Procurement · suite landing", sub="Approved look: teal and coral. The right item at the agreed price, on the shelf before it runs out, and on the patient's bill. " + SUB)),
  "financial": dict(title="Financial Health Suite", looks=["47-bridge.js"],
                     page=dict(mode="review", suite="financial", schemes=["bridge"], title="Financial Health · suite landing", sub="Approved look: graphite and lime, with the overview frozen at the top. EBITDA, revenue and two measures you choose, checked every morning against the day and the total since the start, with the causes and the recovery. " + SUB)),
  "approved":   dict(title="Approved Suite Landings", looks=["33-diorama.js", "38-sorter.js", "40-radar.js", "41-dayboard.js", "44-lines.js", "47-bridge.js"],
                     page=dict(mode="pages", title="Automation suites · approved landing pages", sub="Every approved suite landing, live and interactive, for the development team. " + SUB)),
  "library":    dict(title="Suite Block Library", looks=["33-diorama.js", "38-sorter.js", "40-radar.js", "41-dayboard.js", "44-lines.js", "47-bridge.js"], extra=["91-library.js"],
                     page=dict(mode="library", title="Automation suites · block library", sub="Every block of the approved suite landing pages, by suite and by section, with how to use each. " + SUB)),
}
def read(f): return open(os.path.join(HERE, f), encoding="utf-8").read()
def build(name):
    b = BUILDS[name]
    head = re.sub(r"<title>.*?</title>", f"<title>{b['title']}</title>", read("00-head.html"), count=1)
    js = "\n".join(read(f) for f in DATA + RUNTIME + b["looks"] + b.get("extra", []))
    js += "\nconst PAGE = " + json.dumps(b["page"], ensure_ascii=False) + ";\n" + read("90-init.js")
    page = head + "<script>\n" + js + "\n</script>\n"
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    open(os.path.join(HERE, "out", name + ".html"), "w", encoding="utf-8").write(page)
    faces = "".join(f'@font-face{{font-family:"{fam}";font-weight:{w};src:url(file://{FONTS}/{f})}}' for fam, w, f in [
        ("Bebas Neue", 400, "bebas-neue-latin-400-normal.woff2"), ("Caveat", "500 700", "caveat-latin-700-normal.woff2"),
        ("Poppins", 400, "poppins-latin-400-normal.woff2"), ("Poppins", 500, "poppins-latin-500-normal.woff2"),
        ("Poppins", 600, "poppins-latin-600-normal.woff2"), ("Poppins", 700, "poppins-latin-700-normal.woff2")])
    prev = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>' + faces + "</style></head><body>" + "\n".join(l for l in page.split("\n") if "fonts.g" not in l) + "</body></html>"
    open(os.path.join(HERE, "out", name + ".preview.html"), "w", encoding="utf-8").write(prev)
    # standalone: a complete document that opens on its own (double-click), for the Automation Suites folder
    i = page.index("</style>") + len("</style>")
    alone = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
             + page[:i] + "\n</head>\n<body>\n" + page[i:] + "\n</body>\n</html>\n")
    os.makedirs(os.path.join(HERE, "out", "standalone"), exist_ok=True)
    open(os.path.join(HERE, "out", "standalone", name + ".html"), "w", encoding="utf-8").write(alone)
    print(name, len(page))
for n in (sys.argv[1:] or BUILDS): build(n)
