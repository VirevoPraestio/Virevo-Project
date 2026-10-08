import sys, asyncio, os
from playwright.async_api import async_playwright
async def main(names):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for n in names:
            mob = '.mobile.' in n
            pg = await b.new_page(viewport={'width': 390 if mob else 1440, 'height': 2300 if not mob else 3600})
            await pg.goto('file://' + os.path.abspath('out/landing/los-%s.html' % n))
            await pg.add_style_tag(content='.sh-mid,.sh-mc{height:auto!important;overflow:visible!important}');await pg.wait_for_timeout(400)
            el = pg.locator('.sh-mid' if not mob else '.sh-mc').first
            await el.screenshot(path='/tmp/claude-0/-home-claude/03c88069-df42-5adc-81c0-8363d8048bff/scratchpad/%s.png' % n)
        await b.close()
asyncio.run(main(sys.argv[1:]))
