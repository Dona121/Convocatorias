# Capa pública de reportes — implementación de `GuiaReporte.md`

**Fecha:** 2026-06-21
**Estado:** Implementada y verificada (todas las vistas responden `200`, incl. parciales HTMX y detalles con datos reales).

Capa de **consulta pública, solo lectura**, montada en la **raíz** del sitio. La
parametrización y el registro siguen en el admin; estas vistas solo leen. **No se
modificó ningún modelo.**

---

## Cómo se accede

| URL | Vista |
|---|---|
| `/` | Vista 1 — Convocatorias (listado + filtros + gráficos) |
| `/convocatorias/<id>/` | Detalle de una convocatoria con sus proyectos |
| `/proyectos/` | Vista 2 — Proyectos (listado + filtros + gráficos) |
| `/proyectos/<id>/` | Detalle de un proyecto |

El admin sigue en `/es/admin/` (antes la raíz redirigía allí; ahora la raíz es el reporte público).

---

## Archivos creados / modificados

**Backend (`contenido/`)**
- `reportes.py` *(nuevo)* — lógica de dominio: estados/etapas **derivados** (sin campos en
  los modelos) y utilidades de djmoney (suma + formato COP).
- `views.py` — vistas públicas de listado, detalle y parciales HTMX.
- `urls.py` — rutas con `app_name = "reportes"`.

**Proyecto**
- `convocatorias_seguimiento/urls.py` — la raíz incluye `contenido.urls`; servido de `MEDIA` en DEBUG.
- `convocatorias_seguimiento/settings.py` — se añadieron `MEDIA_URL` / `MEDIA_ROOT`.

**Plantillas (`templates/reportes/`)** *(nuevas)*
- `base.html` — masthead institucional, tokens de `GUIA_DISEÑO.md`, librerías vendorizadas.
- `convocatorias.html` + `_convocatorias_resultados.html` (parcial HTMX).
- `convocatoria_detalle.html`.
- `proyectos.html` + `_proyectos_resultados.html` (parcial HTMX).
- `proyecto_detalle.html`.

**Estáticos (`contenido/static/vendor/`)** *(vendorizados, sin CDN en runtime)*
- `chart.umd.min.js` (Chart.js 4.4.4), `htmx.min.js` (2.0.3), `alpine.min.js` (3.14.1),
  `tailwind.min.js` (Tailwind Play 3.4.16).

---

## Decisiones de diseño técnico

### Estados y etapas DERIVADOS (no hay campos de estado)
- **Convocatoria** (`reportes.estado_convocatoria`): sin apertura o cierre → *Fechas
  incompletas*; hoy < apertura → *Próxima*; entre apertura y cierre → *Abierta*; hoy > cierre
  → *Cerrada*. Para **filtrar en BD** se traduce con `reportes.q_estado_convocatoria`.
- **Proyecto** (`reportes.etapa_proyecto`): etapa más avanzada del pipeline
  *postulado → subsanación solicitada → subsanación enviada → resultados publicados*; sin
  ninguna fecha → *Sin fechas registradas*. Filtro en BD con `reportes.q_etapa_proyecto`.

### Dinero (djmoney)
- djmoney guarda el importe y la moneda en columnas separadas. Las sumas se hacen sobre el
  importe (`Money.amount`) y se formatean en **COP** (`reportes.format_cop` → `$ 1.234.567`).
- Los gráficos de dinero agregan en Python sobre `FuenteFinanciacion` (con `select_related`)
  para evitar los problemas de `Sum()` de djmoney en `GROUP BY`.

### Rendimiento
- Listados con `select_related` (FKs) y `prefetch_related` (M2M); conteos con
  `annotate(Count(..., distinct=True))` (proyectos por convocatoria y postulados).

### Filtros dinámicos (HTMX + Alpine)
- El formulario hace `hx-get` y reemplaza solo `#resultados` (`hx-trigger="change, submit"`,
  `hx-push-url="true"`). Sin JS hay un botón "Aplicar filtros" de respaldo (`<noscript>`).
- Cada parcial trae sus datos de gráfico como `json_script` y un `<script>` que reconstruye
  los Chart.js; `makeChart` destruye el gráfico previo antes de recrearlo en cada swap.

### Gráficos (Chart.js)
- Vista 1: dona (convocatorias por estado), histograma (convocatorias por nº de proyectos,
  buckets 0/1/2/3/4/5+), barras horizontales (embudo de proyectos por etapa).
- Vista 2: comprometido vs pagado por vigencia y por fuente, y beneficiarios por tipo.
- Paleta institucional: serie principal verde `#109d39`, secundaria azul `#0b72ab`.

---

## Desviaciones respecto al brief (a confirmar)

- **"barras apiladas" para comprometido vs pagado:** se implementaron como **barras
  agrupadas** (no apiladas), porque *pagado* es un subconjunto de *comprometido* y apilarlas
  duplicaría el total visualmente. Si se prefiere apiladas, es un cambio de una línea por
  gráfico (`stacked: true` en las escalas).
- **Tailwind:** se usó el motor **Play** vendorizado localmente (no hay pipeline de build en
  el proyecto). Funciona offline; en consola advierte que Play no es para producción. Si se
  quiere un CSS compilado, habría que añadir un build de Tailwind.

---

## Notas de despliegue

- **Producción (`DEBUG=False`):** ejecutar `python manage.py collectstatic` para que WhiteNoise
  sirva `vendor/*` y los CSS. Las imágenes (`MEDIA`) requieren servirse aparte (no las cubre
  WhiteNoise por defecto).
- En desarrollo (`runserver`) los estáticos se sirven directo desde `contenido/static/`.
