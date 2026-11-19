import asyncio
from playwright.async_api import async_playwright
def lum(c):
    c=[int(c[i:i+2],16)/255 for i in (1,3,5)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]
def cr(a,b):
    l1,l2=sorted([lum(a),lum(b)],reverse=True);return (l1+.05)/(l2+.05)
for fg,bg,n in [('#ffffff','#b25a00','botón naranja'),('#b25a00','#ffffff','texto naranja pequeño'),('#b25a00','#f3f5f9','eyebrow en fondo gris'),('#5a6475','#ffffff','texto secundario'),('#5a6475','#f3f5f9','texto secundario en gris'),('#c9d3e6','#0d2f6b','texto claro en azul'),('#ffffff','#0d2f6b','blanco en azul'),('#d45f00','#ffffff','acento grande (íconos/titular)')]:
    print(f'{n:32} {cr(fg,bg):.2f}')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':900})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.goto('http://localhost:8765/',wait_until='networkidle')
        await pg.click('#f-int'); print('filtro interventoría:',await pg.inner_text('#count'))
        await pg.fill('#q','Bosa'); print('búsqueda Bosa:',await pg.inner_text('#count'))
        await pg.click('#f-all'); await pg.fill('#q',''); await pg.check('#cert'); print('certificados:',await pg.inner_text('#count'))
        print('año pie:',await pg.inner_text('.cyear'),'| primer año exp:',await pg.inner_text('#exp li .yr'))
        await pg.click('#form button[type=submit]')
        print('errores formulario:',[await e.inner_text() for e in await pg.query_selector_all('.err') if (await e.inner_text())])
        hrefs=[]
        pg.on('framenavigated',lambda f: hrefs.append(f.url))
        await pg.fill('[name=nombre]','Prueba'); await pg.fill('[name=email]','prueba@ejemplo.com'); await pg.check('input[name=area][value="Interventoría"]'); await pg.fill('[name=mensaje]','Hola'); await pg.check('[name=autorizo]')
        url=await pg.evaluate("""()=>{let u='';const o=Object.getOwnPropertyDescriptor(Location.prototype,'href');document.getElementById('form').addEventListener('submit',e=>{},true);window.__u=null;const f=document.getElementById('form');const orig=window.location;return 'ok'}""")
        await pg.evaluate("""()=>{window.addEventListener('beforeunload',()=>{})}""")
        try:
            async with pg.expect_event('request',timeout=1500) as r: await pg.click('#form button[type=submit]')
        except Exception as e: pass
        print('errores tras envío válido:',[await e.inner_text() for e in await pg.query_selector_all('.err') if (await e.inner_text())])
        for path in ['/politica-de-datos/']:
            await pg.goto('http://localhost:8765'+path,wait_until='networkidle')
        print('errores JS:',errs or 'ninguno')
        await b.close()
asyncio.run(main())
