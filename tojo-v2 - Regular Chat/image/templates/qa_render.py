"""Internal QA only: render each sample SVG to PNG so it can be looked at.
The PNG is never the delivered artefact — the SVG is."""

import glob
import os
import sys

from playwright.sync_api import sync_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
SAMPLES = os.path.join(os.path.dirname(__file__), "..", "samples")


def render(paths, scale=2):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        page = b.new_page(device_scale_factor=scale)
        for svg_path in paths:
            with open(svg_path) as f:
                svg = f.read()
            page.set_content(f"<html><body style='margin:0'>{svg}</body></html>")
            el = page.query_selector("svg")
            png = svg_path.replace(".svg", ".png")
            el.screenshot(path=png)
            print("rendered", os.path.basename(png))
        b.close()


if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(SAMPLES, "*.svg")))
    render(files)
