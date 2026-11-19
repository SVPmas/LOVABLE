# svpingenieriasas.com · sitio web v3 rev1 (19-nov-2026)

Sitio institucional de **SVP Ingeniería SAS**, publicado en https://svpingenieriasas.com.

| Dato | Valor |
|---|---|
| Versión | v3 rev1, aprobada por Marco Aurelio Pastrana Borrero el 19-nov-2026 |
| Netlify | Proyecto `svpingenieriasas` (cuenta svpingenieria@gmail.com, equipo `svpingenieria`) · siteId `e5ef903c-0253-4704-8607-d380c9dbd527` |
| Despliegue | `6aff21243d70b7cb697ba3c3` (por carga, sin build) |
| Diseño | Tomado del proyecto Lovable «SVP-SGI Web» (repositorio SVPmas/svp-sgi-project-atlas) |
| Contenido | Sitio v2 (servicios, 124 contratos, proyectos, SGI, política integral, marco normativo, dirección) |
| Copia maestra en Drive | 4.0_WEB_Y_COMUNICACIONES › SVP-WEB_sitio_v3rev1_2026-11-19 |
| Registros SGI | P5.4 Web: SVP-WEB-BIT-001 v1 rev2 (bitácora) y SVP-WEB-MEM-001 v2 (memoria) |

## Carpetas

- `sitio/` — los 13 archivos publicados tal cual (sitio estático: `index.html`, `assets/`, íconos, `politica-de-datos/`, `publicaciones/`).
- `herramientas/` — scripts con que se armó y verificó el sitio:
  - `build.py`: arma el sitio con el diseño de Lovable y las secciones de la v2 (rutas de trabajo de la sesión de Claude; ajústalas antes de reutilizarlo).
  - `site.css`: hoja de estilos fuente (copia de `sitio/assets/site.css`).
  - `shots.py`: capturas con Playwright a 1440 px y 390 px.
  - `check.py`: contrastes de color, filtros de contratos, formulario y errores de JavaScript.

## Publicar una versión nueva

Sirve `sitio/` con `python3 -m http.server`, verifica, y despliega la carpeta `sitio/` en el proyecto Netlify `svpingenieriasas` (arrastrar en Deploys o con el conector de Netlify). No publicar sin aprobación expresa de Marco.

## Reglas de contenido

Solo «SVP Ingeniería SAS» (nunca «Suelos, Vías y Pavimentos»), sin logos MPB, sin YUMA, sin dirección física, WhatsApp @marcopastranaborrero sin número de celular, sin notas de prensa, SGI «documentado según» y no certificado.
