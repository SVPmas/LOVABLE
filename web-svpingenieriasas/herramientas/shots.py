import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w,name in [(1440,'d'),(390,'m')]:
            pg = await b.new_page(viewport={'width':w,'height':900}, device_scale_factor=1)
            await pg.goto('http://localhost:8765/', wait_until='networkidle')
            await pg.add_style_tag(content='.nav{position:static!important}')
            await pg.screenshot(path=f'/home/claude/shots/full_{name}.png', full_page=True)
            for sid in ['inicio','servicios','experiencia','proyectos','publicaciones','empresa','sgi','ia-sgi','direccion','contacto']:
                el = await pg.query_selector('#'+sid)
                await el.screenshot(path=f'/home/claude/shots/{name}_{sid}.png')
            for path,n in [('/politica-de-datos/','pol')]:
                await pg.goto('http://localhost:8765'+path, wait_until='networkidle')
                await pg.screenshot(path=f'/home/claude/shots/{name}_{n}.png', full_page=(name=='d'))
            await pg.close()
        await b.close()
asyncio.run(main())
