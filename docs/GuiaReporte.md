## Contexto
Capa de consulta/reporte pública (raíz del proyecto, SIN login) para el seguimiento
de convocatorias de la Gobernación de Sucre. La parametrización y el registro se
hacen en el admin; esto es solo lectura.

## Stack (no mezclar otras opciones)
- Filtros dinámicos: Alpine.js + HTMX (parciales de Django, sin recargar).
- Gráficos: Chart.js.
- Estilos: Tailwind, siguiendo frontend-design skill y GUIA_DISEÑO.md
  (identidad institucional Gob. de Sucre; herramienta de consulta, priorizar
  densidad y legibilidad sobre ornamento).

## Lógica de dominio (NO crear campos de estado en los modelos)
- Estado de convocatoria DERIVADO:
  - Si falta fecha_apertura o fecha_cierre → "Fechas incompletas" (mensaje visible).
  - Si hoy < apertura → "Próxima"; entre apertura y cierre → "Abierta"; > cierre → "Cerrada".
- Etapa de proyecto DERIVADA del pipeline de fechas:
  postulado → subsanación solicitada → subsanación enviada → resultados publicados.
  - Si no hay ninguna fecha del pipeline → "Sin fechas registradas" (mensaje visible).
- djmoney: al sumar montos (monto, valor_comprometido, valor_pagado) tener en cuenta
  que guarda la moneda en columna aparte; agregar correctamente y formatear en COP.
- Rendimiento: en TODA consulta de listado usar select_related para FKs y
  prefetch_related para los M2M; los conteos con annotate(Count(...)).

## Vista 1 — Convocatorias (incluye detalle de proyectos)
- Filtros (HTMX/Alpine): dependencia, aliado, segmento, sector, ubicación,
  estado derivado, estado_monto, rango de fechas apertura/cierre.
- Listado con: nombre, estado (con su mensaje si faltan fechas), fechas, monto (COP),
  nro de proyectos postulados (annotate(Count('proyecto'))).
- Detalle: proyectos postulados a esa convocatoria, cada uno con su etapa del pipeline,
  BPIN, dependencia, responsable, fuentes (comprometido vs pagado), beneficiarios por
  tipo e indicadores MGA con meta_proyecto.
- Gráficos (Chart.js): convocatorias por estado (dona), proyectos por convocatoria
  (barras), embudo de proyectos por etapa del pipeline.

## Vista 2 — Proyectos
- Cada proyecto muestra la convocatoria en la que se postuló (FK Proyecto.convocatoria),
  su etapa del pipeline, dependencia, responsable, BPIN.
- Filtros: convocatoria, dependencia, responsable, etapa derivada, municipio.
- Gráficos: comprometido vs pagado por vigencia y por fuente (FuenteFinanciacion,
  barras apiladas), beneficiarios por tipo.

## General
- Navegación cruzada: desde una convocatoria se llega a sus proyectos y desde un
  proyecto se vuelve a su convocatoria.
- Todo público, solo lectura.

## Importante
- Trabaja con los modelos que existen y no los modifiques. Esta pagina sirve como reporte de lo que ya existe.