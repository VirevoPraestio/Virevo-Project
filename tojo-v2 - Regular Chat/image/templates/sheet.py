"""Contact sheet of every sample, for the look-at-it pass."""
import glob, os, sys
from playwright.sync_api import sync_playwright
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
S = os.path.join(os.path.dirname(__file__), "..", "samples")

def sheet(kind, cols, out):
    files = sorted(glob.glob(os.path.join(S, f"*-{kind}-*.svg")))
    cells = []
    for f in files:
        svg = open(f).read()
        cells.append(f'<div class=c><div class=n>{os.path.basename(f)}</div>{svg}</div>')
    html = ("<style>body{margin:0;background:#7a7a7a;font:12px monospace}"
            f".g{{display:grid;grid-template-columns:repeat({cols},1fr);gap:10px;padding:10px}}"
            ".c{background:#555;padding:4px}.n{color:#fff;padding:2px 0}"
            "svg{width:100%;height:auto;display:block}</style>"
            f"<div class=g>{''.join(cells)}</div>")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": 1900, "height": 1200}, device_scale_factor=1)
        pg.set_content(html)
        pg.screenshot(path=out, full_page=True)
        b.close()
    print("wrote", out, len(files), "images")

sheet("desktop", 3, os.path.join(S, "_sheet-desktop.png"))
sheet("mobile", 5, os.path.join(S, "_sheet-mobile.png"))
