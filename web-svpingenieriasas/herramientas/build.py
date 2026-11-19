#!/usr/bin/env python3
"""Arma el sitio v3 de svpingenieriasas.com: diseño visual de Lovable + contenido vigente de la v2."""
import html, json, re, shutil, sys
from pathlib import Path

V2 = Path('/home/claude/web_2026-11-05')
LOV = Path('/home/claude/svp-sgi-project-atlas')
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/SVP-WEB_sitio_v3_2026-11-19')
CSS = Path('/home/claude/build/site.css').read_text()

v2 = (V2 / 'index.html').read_text()
body = v2[v2.find('<body'):]

def section(sid):
    m = re.search(r'<section class="[^"]*" id="%s">.*?</section>' % sid, body, re.S)
    assert m, sid
    return m.group(0)

def esc(s):
    return html.escape(s, quote=True)

# ---------- íconos (trazos tipo lucide) ----------
P = {
 'search': '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
 'compass': '<circle cx="12" cy="5" r="2"/><path d="m11 7-6 14M13 7l6 14M8 15h8"/>',
 'hardhat': '<path d="M2 18h20M4 18v-3a8 8 0 0 1 16 0v3M10 10V6h4v4"/>',
 'clipboard': '<rect x="6" y="4" width="12" height="17" rx="2"/><path d="M9 4h6v3H9zM9 12h6M9 16h4"/>',
 'shield': '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
 'chart': '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
 'hammer': '<path d="m15 12-8.5 8.5a2 2 0 0 1-3-3L12 9"/><path d="m18 15 4-4-6-6-4 4z"/>',
 'building': '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10 21v-3h4v3"/>',
 'activity': '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
 'layers': '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
 'home': '<path d="m3 11 9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'chat': '<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z"/>',
 'pin': '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 'brain': '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 1V4.5A2.5 2.5 0 0 0 9 4zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 1"/>',
 'scan': '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3"/><circle cx="11.5" cy="11.5" r="3.5"/><path d="m16 16-2-2"/>',
 'badge': '<circle cx="12" cy="9" r="6"/><path d="m9 9 2 2 4-4M8.5 14 7 22l5-3 5 3-1.5-8"/>',
 'id': '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M6 16c.8-1.5 2-2 3-2s2.2.5 3 2M14 10h4M14 13h3"/>',
 'link': '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v6M8 7v.01M12 16v-3.5a2 2 0 0 1 4 0V16M12 10v6"/>',
}
def ic(n):
    return '<svg viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % P[n]

ARR = '<span class="arr" aria-hidden="true">→</span>'

# ---------- áreas de solución (proyecto Lovable, orden fijado por Marco) ----------
AREAS = [
 ('consultoria','Consultoría','Asesoría especializada para entidades públicas y privadas en estructuración de proyectos.','chart'),
 ('interventoria','Interventoría','Supervisión técnica, administrativa y financiera para garantizar la correcta ejecución contractual.','shield'),
 ('diseno','Diseño','Diseño de ingeniería civil, estructural, hidráulica y vial con criterios normativos y de optimización.','compass'),
 ('gerencia','Gerencia de proyectos','Planeación, control de costos, plazos y riesgos durante todo el ciclo de vida del proyecto.','clipboard'),
 ('construccion','Construcción','Construcción de obras civiles e infraestructura con control de calidad y seguridad.','hammer'),
 ('edificaciones','Edificaciones','Diseño, licenciamiento y construcción de edificaciones institucionales, comerciales y residenciales.','building'),
 ('actualizacion-sismica','Actualización sísmica','Evaluación de vulnerabilidad y adecuación de edificaciones a la norma sismorresistente vigente.','activity'),
 ('reforzamiento','Reforzamiento estructural','Diseño y ejecución de reforzamientos para recuperar o aumentar la capacidad de las estructuras.','layers'),
 ('mejoramiento','Mejoramiento de vivienda','Programas de mejoras estructurales, de habitabilidad y saneamiento para hogares y comunidades.','home'),
]

LOGO_H = '/assets/svp-horizontal.svg'
SELLO = '/assets/svp-sello.svg'

def head(title, desc, canonical, og_type='website', extra=''):
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="es_CO">
<meta property="og:image" content="https://svpingenieriasas.com/assets/imagen-compartir.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="SVP Ingeniería SAS · Estudios, diseños, ejecución y gerencia de proyectos · 1994">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0d2f6b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{extra}</head>
'''

NAV_ITEMS = [('Servicios','servicios'),('Experiencia','experiencia'),('Proyectos','proyectos'),('Publicaciones','publicaciones'),('La firma','empresa'),('SGI','sgi'),('Dirección','direccion')]

def header(prefix=''):
    lis = ''.join(f'<li><a href="{prefix}#{i}">{l}</a></li>' for l, i in NAV_ITEMS)
    return f'''<a class="skip" href="#contenido">Ir al contenido</a>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="{prefix or '#inicio'}" aria-label="SVP Ingeniería SAS, inicio"><img src="{LOGO_H}" alt="SVP Ingeniería SAS" width="220" height="44"></a>
    <button class="burger" type="button" id="burger" aria-expanded="false" aria-controls="menu">Menú</button>
    <ul class="menu" id="menu">{lis}<li><a class="cta-mini" href="{prefix}#contacto">Solicitar propuesta</a></li></ul>
  </div>
</header>
'''

def footer(prefix=''):
    lis = ''.join(f'<li><a href="{prefix}#{i}">{l}</a></li>' for l, i in NAV_ITEMS)
    return f'''<footer>
  <div class="wrap foot">
    <div><img src="{LOGO_H}" alt="SVP Ingeniería SAS" width="200" height="40"><p>Estudios, diseños, construcción, reconstrucción, interventoría, administración y gerencia de proyectos. Bogotá D.C., desde 1994.</p></div>
    <div><h4>Navegación</h4><ul>{lis}</ul></div>
    <div><h4>Contacto</h4><ul>
      <li><a href="mailto:contacto@svpingenieriasas.com">contacto@svpingenieriasas.com</a></li>
      <li><a href="mailto:gerencia@svpingenieriasas.com">gerencia@svpingenieriasas.com</a></li>
      <li>WhatsApp @marcopastranaborrero</li>
      <li><a href="https://www.linkedin.com/in/marco-pastrana-903510310/" target="_blank" rel="noopener me">LinkedIn</a></li>
      <li>Bogotá D.C., Colombia</li></ul></div>
  </div>
  <div class="legal">© <span class="cyear">2026</span> SVP Ingeniería SAS · Matrícula mercantil 00600568 CCB · <a href="/politica-de-datos/">Política de tratamiento de datos personales</a></div>
</footer>
'''

BASE_JS = '''<script>
(function(){
  var burger=document.getElementById('burger'), menu=document.getElementById('menu');
  if(burger){burger.addEventListener('click',function(){var o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
  menu.addEventListener('click',function(e){if(e.target.tagName==='A'){menu.classList.remove('open');burger.setAttribute('aria-expanded','false')}});}
  [].forEach.call(document.querySelectorAll('.cyear'),function(n){n.textContent=new Date().getFullYear()});
})();
</script>
'''

# ---------- secciones conservadas de la v2 (texto con fuente) ----------
servicios_v2 = section('servicios')
svc_grid = servicios_v2[servicios_v2.find('<div class="services">'):servicios_v2.rfind('</div>\n</section>')]
assert svc_grid.count('<article class="svc">') >= 8, 'servicios'
experiencia = section('experiencia')
proyectos = section('proyectos').replace('<section class="block alt" id="proyectos">', '<section class="block" id="proyectos">')
publicaciones = section('publicaciones').replace('<section class="block" id="publicaciones">', '<section class="block alt" id="publicaciones">')
metodo = section('metodo').replace('<section class="block" id="metodo">', '<section class="block alt" id="metodo">')
empresa = section('empresa').replace('<section class="block alt" id="empresa">', '<section class="block" id="empresa">')
sgi = section('sgi').replace('<section class="block" id="sgi">', '<section class="block alt" id="sgi">')
direccion = section('direccion').replace('<section class="block" id="direccion">', '<section class="block alt" id="direccion">')
exp_js = v2[v2.find('function norm(s)'):v2.find("cert.addEventListener('change',draw); q.addEventListener('input',draw);")]
exp_js += "cert.addEventListener('change',draw); q.addEventListener('input',draw);"
jsonld = v2[v2.find('<script type="application/ld+json">'):v2.find('</script>', v2.find('<script type="application/ld+json">'))+9]

# Experiencia: título sin superlativo
experiencia = experiencia.replace('<h2>Tres décadas de contratos</h2>', '<h2>124 contratos que respaldan la firma</h2>')

# Publicaciones: solo el informe de seguimiento del 8-oct (sin nota de Claude ni notas de prensa)
publicaciones = re.sub(r'\s*<article class="proj">\s*<span class="tag">Nota de divulgación.*?</article>', '', publicaciones, flags=re.S)
assert 'Claude' not in publicaciones and publicaciones.count('<article class="proj">') == 1
publicaciones = publicaciones.replace('<p>Informes de seguimiento elaborados por la firma', '<p>Informe de seguimiento elaborado por la firma')

# ---------- bloques nuevos con el diseño de Lovable ----------
areas_html = ''.join(f'<div class="area">{ic(n)}<h4>{t}</h4><p>{d}</p></div>' for _, t, d, n in AREAS)
servicios = f'''<section class="block alt" id="servicios">
  <div class="wrap">
    <div class="head">
      <div><div class="eyebrow">Servicios</div><h2>Soluciones integrales de ingeniería</h2></div>
      <p>Acompañamos a entidades públicas, contratistas, consorcios y clientes privados en todo el ciclo de un proyecto de infraestructura: desde la idea y su estructuración hasta los estudios y diseños, la interventoría, la construcción y la liquidación, con las especificaciones del INVÍAS, el IDU, la Aerocivil, la NSR-10 y las entidades territoriales.</p>
    </div>
    <div class="featured">
      <div class="lead-card">
        <div class="eyebrow">Solución destacada</div>
        <h3>Soluciones integrales para infraestructura, superestructuras, edificaciones, vivienda, refuerzo estructural, actualización sísmica y mejoramiento de vivienda</h3>
        <p>Desde la infraestructura y las superestructuras hasta la vivienda y su mejoramiento, acompañamos cada proyecto de principio a fin: estudios, diseños, licencias, ejecución y gerencia, con un solo equipo responsable del resultado.</p>
        <a class="btn orange" href="#contacto">Consultar alcance {ARR}</a>
      </div>
      <div class="areas">{areas_html}</div>
    </div>
    <div class="sub-head"><h3>Líneas de servicio y experiencia que las respalda</h3><p>Cada línea con su alcance típico y un ejemplo de la relación de contratos.</p></div>
    {svc_grid}
  </div>
</section>
'''

ia = f'''<section class="block" id="ia-sgi">
  <div class="wrap">
    <div class="head">
      <div><div class="eyebrow">IA aplicada al SGI</div><h2>Apoyo con inteligencia artificial en los procesos del SGI</h2></div>
      <p>Incorporamos la inteligencia artificial al Sistema de Gestión Integral como apoyo al juicio profesional: aporta pensamiento crítico en la toma de decisiones y una revisión final con el rigor de un interventor y un auditor interno de calidad. Su uso sigue la política integral: supervisión humana y protección de la información de clientes y personas.</p>
    </div>
    <div class="pillars">
      <article class="pillar">{ic('brain')}<h3>Pensamiento crítico para decidir</h3><p>La IA contrasta alternativas, expone supuestos, riesgos y consecuencias, y deja la decisión final en criterio del equipo profesional.</p></article>
      <article class="pillar">{ic('scan')}<h3>Revisión final como interventor</h3><p>Verificación independiente de cada entregable: coherencia entre cálculos, memorias, planos y anexos antes de la entrega.</p></article>
      <article class="pillar">{ic('badge')}<h3>Auditoría interna de calidad</h3><p>Revisión del proceso y del producto con hallazgos, acciones correctivas y evidencia trazable para la mejora continua.</p></article>
    </div>
    <div class="review">
      <div class="lead-card">
        <div class="eyebrow">Revisión final</div>
        <h3>Criterio de interventor y auditor interno de calidad</h3>
        <p>La IA acelera el análisis y el cruce de información, pero la decisión y la firma siguen siendo del equipo profesional: cada producto se revisa con el rigor de una interventoría y de una auditoría interna de calidad antes de entregarse.</p>
        <a class="btn orange" href="#contacto">Consultar este servicio {ARR}</a>
      </div>
      <ul class="checks">
        <li>Organización y cruce de la información de cada proceso del SGI.</li>
        <li>Detección temprana de hallazgos, desviaciones y omisiones.</li>
        <li>Seguimiento de acciones correctivas con evidencia trazable.</li>
        <li>Soporte documental para informes, actas y anexos.</li>
      </ul>
    </div>
  </div>
</section>
'''

hero = f'''<section class="hero" id="inicio">
  <div class="wrap hero-grid">
    <div>
      <span class="pill">Ingeniería desde 1994</span>
      <h1>Estudios, diseños, construcción, reconstrucción, interventoría, administración y <em>gerencia de proyectos.</em></h1>
      <p class="lead">SVP Ingeniería SAS estructura, diseña, supervisa y ejecuta proyectos de vías, edificaciones, mejoramiento de vivienda, aeródromos, saneamiento básico y gestión ambiental para entidades públicas, contratistas y consorcios en Colombia, con análisis y gestión del riesgo y metodología BIM.</p>
      <div class="cta">
        <a class="btn solid" href="#servicios">Nuestros servicios {ARR}</a>
        <a class="btn ghost" href="#experiencia">Ver los 124 contratos</a>
      </div>
    </div>
    <div class="seal" aria-hidden="true">
      <div class="r1"></div><div class="r2"></div>
      <img src="{SELLO}" alt="" width="240" height="240">
      <div class="badge-card"><b>32</b><span>años de trayectoria</span></div>
    </div>
  </div>
</section>
<div class="stats" aria-label="Cifras de la firma">
  <div class="wrap">
    <div class="stat"><b>1994</b><span>Año de constitución en Bogotá (E.P. 1.267, Notaría 32)</span></div>
    <div class="stat"><b>32</b><span>Años de trayectoria en infraestructura</span></div>
    <div class="stat"><b>124</b><span>Contratos en la relación de experiencia</span></div>
    <div class="stat"><b>55 · 62 · 7</b><span>Interventorías · estudios y diseños · obras</span></div>
  </div>
</div>
'''

opts = ''.join(f'<label class="opt"><input type="radio" name="area" value="{esc(t)}"> {t}</label>' for _, t, _, _ in AREAS)
contacto = f'''<section class="contact" id="contacto">
  <div class="wrap contact-grid">
    <div>
      <div class="eyebrow">Contacto</div>
      <h2>Hablemos de su próximo proyecto</h2>
      <p class="intro">Escríbanos con el tipo de servicio, el alcance y la ubicación del proyecto. Le respondemos con una propuesta técnica.</p>
      <ul class="info">
        <li>{ic('mail')}<div><small>Correo</small><a href="mailto:contacto@svpingenieriasas.com">contacto@svpingenieriasas.com</a></div></li>
        <li>{ic('mail')}<div><small>Gerencia</small><a href="mailto:gerencia@svpingenieriasas.com">gerencia@svpingenieriasas.com</a></div></li>
        <li>{ic('chat')}<div><small>WhatsApp</small>@marcopastranaborrero</div></li>
        <li>{ic('link')}<div><small>LinkedIn</small><a href="https://www.linkedin.com/in/marco-pastrana-903510310/" target="_blank" rel="noopener me">Marco Pastrana</a></div></li>
        <li>{ic('pin')}<div><small>Ciudad</small>Bogotá D.C., Colombia</div></li>
        <li>{ic('id')}<div><small>Razón social</small>SVP Ingeniería SAS · Matrícula mercantil 00600568 CCB</div></li>
      </ul>
    </div>
    <form class="form" id="form" novalidate>
      <div class="two">
        <label class="field"><span>Nombre</span><input type="text" name="nombre" maxlength="100" autocomplete="name"><em class="err" data-for="nombre"></em></label>
        <label class="field"><span>Correo electrónico</span><input type="email" name="email" maxlength="255" autocomplete="email"><em class="err" data-for="email"></em></label>
      </div>
      <label class="field"><span>Empresa o entidad</span><input type="text" name="empresa" maxlength="120" autocomplete="organization"></label>
      <fieldset><legend>Área de solución que necesita</legend><div class="opts">{opts}</div><em class="err" data-for="area"></em></fieldset>
      <label class="field"><span>Mensaje</span><textarea name="mensaje" rows="5" maxlength="1000"></textarea><em class="err" data-for="mensaje"></em></label>
      <div><label class="consent"><input type="checkbox" name="autorizo"><span>Autorizo el tratamiento de mis datos personales conforme a la Ley 1581 de 2012. <a href="/politica-de-datos/" target="_blank" rel="noopener">Ver la política de tratamiento de datos</a></span></label><em class="err" data-for="autorizo"></em></div>
      <button class="btn orange" type="submit">Enviar mensaje {ARR}</button>
      <p class="form-note">Al enviar se abre su programa de correo con el mensaje listo para contacto@svpingenieriasas.com. El sitio no guarda sus datos.</p>
    </form>
  </div>
</section>
'''

form_js = r'''
  var f=document.getElementById('form');
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var d=new FormData(f), errs={};
    var nombre=(d.get('nombre')||'').trim(), email=(d.get('email')||'').trim(), msg=(d.get('mensaje')||'').trim();
    if(!nombre)errs.nombre='Escriba su nombre.';
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))errs.email='Escriba un correo válido.';
    if(!d.get('area'))errs.area='Seleccione el área de solución que necesita.';
    if(!msg)errs.mensaje='Escriba su mensaje.';
    if(!d.get('autorizo'))errs.autorizo='Debe autorizar el tratamiento de sus datos personales para enviar el mensaje.';
    [].forEach.call(f.querySelectorAll('.err'),function(x){x.textContent=errs[x.dataset.for]||''});
    var first=Object.keys(errs)[0]; if(first){var el=f.querySelector('[name="'+first+'"]'); if(el)el.focus(); return;}
    var body='Nombre: '+nombre+'\nCorreo: '+email+'\nEmpresa o entidad: '+(d.get('empresa')||'').trim()+'\nÁrea: '+d.get('area')+'\n\n'+msg+'\n\nAutorizo el tratamiento de mis datos personales conforme a la Ley 1581 de 2012.';
    location.href='mailto:contacto@svpingenieriasas.com?subject='+encodeURIComponent('Solicitud de propuesta · '+d.get('area'))+'&body='+encodeURIComponent(body);
  });
'''

index = head('SVP Ingeniería SAS · Estudios, diseños, construcción, reconstrucción, interventoría, administración y gerencia de proyectos',
             'SVP Ingeniería SAS: estudios, diseños, construcción, reconstrucción, interventoría, administración y gerencia de proyectos; estructuración y maduración, gestión del riesgo, gerencia y ejecución de infraestructura vial, aeródromos, edificaciones, saneamiento básico y gestión ambiental, con metodología BIM. Bogotá, desde 1994.',
             'https://svpingenieriasas.com/', extra=jsonld + '\n')
index += '<body>\n' + header() + '<main id="contenido">\n' + hero + servicios + experiencia + '\n' + proyectos + '\n' + publicaciones + '\n' + metodo + '\n' + empresa + '\n' + sgi + '\n' + ia + direccion + '\n</main>\n' + contacto + footer()
index += BASE_JS.replace('})();\n</script>', '  ' + exp_js + form_js + '})();\n</script>') + '</body>\n</html>\n'

# ---------- política de datos (resumen de la política de SVP vigente desde el 1-mar-2017) ----------
pol = head('Política de tratamiento de datos personales · SVP Ingeniería SAS',
           'Resumen de la política de protección de datos personales de SVP Ingeniería SAS, conforme a la Ley 1581 de 2012 y sus decretos reglamentarios.',
           'https://svpingenieriasas.com/politica-de-datos/')
pol += '<body>\n' + header('/') + '''<main id="contenido"><article class="page">
  <a class="back" href="/#contacto">← Volver al inicio</a>
  <h1>Política de tratamiento de datos personales</h1>
  <p class="sub">Resumen para el sitio web de la Política de Protección de Datos Personales de SVP Ingeniería SAS, vigente desde el 1 de marzo de 2017, conforme a la Ley Estatutaria 1581 de 2012 y sus decretos reglamentarios.</p>
  <h2>Responsable del tratamiento</h2>
  <p>SVP Ingeniería SAS, Bogotá D.C., Colombia · Matrícula mercantil 00600568 de la Cámara de Comercio de Bogotá. Correo para asuntos de datos personales: <a href="mailto:contacto@svpingenieriasas.com">contacto@svpingenieriasas.com</a>.</p>
  <h2>Principios</h2>
  <p>Aplicamos los principios de legalidad, finalidad, libertad, veracidad o calidad, transparencia, acceso y circulación restringida, seguridad y confidencialidad.</p>
  <h2>Finalidades</h2>
  <ul>
    <li>Responder consultas, solicitudes de propuesta, peticiones, quejas y reclamos.</li>
    <li>Cumplir las obligaciones con clientes, proveedores, trabajadores y accionistas, y la relación contractual que corresponda.</li>
    <li>Atender requerimientos de autoridades judiciales o administrativas.</li>
  </ul>
  <p>Los datos que usted escribe en el formulario de contacto de este sitio (nombre, correo, empresa o entidad, área y mensaje) se envían desde su propio programa de correo a contacto@svpingenieriasas.com y se usan solo para responder su solicitud. El sitio no los almacena.</p>
  <h2>Derechos del titular</h2>
  <p>Usted puede conocer, actualizar, rectificar y solicitar la supresión de sus datos; pedir prueba de la autorización; ser informado sobre su uso; revocar la autorización cuando no exista un deber legal o contractual de permanecer en la base de datos; acceder gratuitamente a sus datos y presentar quejas ante la Superintendencia de Industria y Comercio.</p>
  <h2>Consultas y reclamos</h2>
  <p>Escriba a <a href="mailto:contacto@svpingenieriasas.com">contacto@svpingenieriasas.com</a> indicando su nombre, un medio de respuesta y la descripción de su solicitud, con los documentos que acrediten su identidad o representación. Las consultas se atienden en máximo diez (10) días hábiles y los reclamos en máximo quince (15) días hábiles, prorrogables en los términos de la ley.</p>
  <h2>Datos sensibles</h2>
  <p>No solicitamos datos sensibles por este sitio. Cuando se requieran en otros procesos, informaremos que su entrega es facultativa y pediremos autorización expresa.</p>
  <h2>Seguridad</h2>
  <p>Adoptamos medidas técnicas, humanas y administrativas para proteger los datos y las exigimos a los encargados que los traten por cuenta de la firma.</p>
  <h2>Normas aplicables</h2>
  <p>Artículo 15 de la Constitución Política, Ley 1266 de 2008, Ley 1581 de 2012 y Decreto 1377 de 2013 (compilado en el Decreto 1074 de 2015), y las normas que los modifiquen o sustituyan.</p>
  <p class="note">Este texto resume la política interna de la firma. La política completa está disponible a solicitud en contacto@svpingenieriasas.com.</p>
</article></main>
''' + footer('/') + BASE_JS + '</body>\n</html>\n'

# ---------- escribir ----------
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / 'assets').mkdir(parents=True)
(OUT / 'publicaciones').mkdir(parents=True)
(OUT / 'politica-de-datos').mkdir(parents=True)
(OUT / 'index.html').write_text(index)
(OUT / 'politica-de-datos/index.html').write_text(pol)
(OUT / 'assets/site.css').write_text(CSS)
for a in ['svp-sello.svg', 'svp-sello-1024.png', 'svp-horizontal.svg', 'imagen-compartir.png']:
    shutil.copy(V2 / 'assets' / a, OUT / 'assets' / a)
for a in ['favicon.svg', 'favicon-16.png', 'favicon-32.png', 'favicon-48.png', 'apple-touch-icon.png']:
    shutil.copy(V2 / a, OUT / a)
shutil.copy(V2 / 'publicaciones/reconstruccion-patria-milagro-2026-10-08.pdf', OUT / 'publicaciones')
print('ok', OUT, len(index))
