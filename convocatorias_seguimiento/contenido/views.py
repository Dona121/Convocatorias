"""Vistas públicas de consulta/reporte (solo lectura, sin login).

La parametrización y el registro se hacen en el admin; estas vistas solo leen.
Todo lo DERIVADO (estado de convocatoria, etapa de proyecto, sumas de dinero) se
calcula en el servidor para mantener las plantillas simples.
"""
from collections import Counter
from datetime import datetime

from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from contenido import models
from contenido import reportes


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _parse_fecha(valor):
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _get(request, nombre):
    """Devuelve el valor de un filtro o None si viene vacío."""
    valor = request.GET.get(nombre, "").strip()
    return valor or None


def _tono_to_dataset_color(tono):
    return {
        "verde": "#109d39",
        "azul": "#0b72ab",
        "rojo": "#d92a34",
        "ambar": "#d88c16",
        "gris": "#686868",
    }.get(tono, "#686868")


# ---------------------------------------------------------------------------
# Vista 1 — Convocatorias
# ---------------------------------------------------------------------------
def convocatorias_list(request):
    ahora = timezone.now()

    qs = (
        models.Convocatorias.objects.all()
        .prefetch_related("dependencia", "segmento", "sectores", "ubicacion", "aliados")
        .annotate(
            num_proyectos=Count("proyecto", distinct=True),
            num_postulados=Count(
                "proyecto",
                filter=Q(proyecto__fecha_envio_postulacion_proyecto__isnull=False),
                distinct=True,
            ),
        )
        .order_by("-fecha_apertura", "nombre_convocatoria")
    )

    # --- Filtros ---
    f = {
        "dependencia": _get(request, "dependencia"),
        "aliado": _get(request, "aliado"),
        "segmento": _get(request, "segmento"),
        "sector": _get(request, "sector"),
        "ubicacion": _get(request, "ubicacion"),
        "estado": _get(request, "estado"),
        "estado_monto": _get(request, "estado_monto"),
        "apertura_desde": _get(request, "apertura_desde"),
        "apertura_hasta": _get(request, "apertura_hasta"),
        "cierre_desde": _get(request, "cierre_desde"),
        "cierre_hasta": _get(request, "cierre_hasta"),
    }

    if f["dependencia"]:
        qs = qs.filter(dependencia__id=f["dependencia"])
    if f["aliado"]:
        qs = qs.filter(aliados__id=f["aliado"])
    if f["segmento"]:
        qs = qs.filter(segmento__id=f["segmento"])
    if f["sector"]:
        qs = qs.filter(sectores__id=f["sector"])
    if f["ubicacion"]:
        qs = qs.filter(ubicacion__id=f["ubicacion"])
    if f["estado_monto"]:
        qs = qs.filter(estado_monto=f["estado_monto"])
    if f["estado"] in reportes.ESTADOS_CONVOCATORIA:
        qs = qs.filter(reportes.q_estado_convocatoria(f["estado"], ahora))

    ad, ah = _parse_fecha(f["apertura_desde"]), _parse_fecha(f["apertura_hasta"])
    cd, ch = _parse_fecha(f["cierre_desde"]), _parse_fecha(f["cierre_hasta"])
    if ad:
        qs = qs.filter(fecha_apertura__date__gte=ad)
    if ah:
        qs = qs.filter(fecha_apertura__date__lte=ah)
    if cd:
        qs = qs.filter(fecha_cierre__date__gte=cd)
    if ch:
        qs = qs.filter(fecha_cierre__date__lte=ch)

    qs = qs.distinct()
    convocatorias = list(qs)

    # --- Enriquecer filas con estado derivado + monto formateado ---
    filas = []
    conteo_estado = {k: 0 for k in reportes.ESTADOS_CONVOCATORIA}
    for c in convocatorias:
        clave, info = reportes.estado_convocatoria(c, ahora)
        conteo_estado[clave] += 1
        filas.append({
            "obj": c,
            "estado_clave": clave,
            "estado": info,
            "monto_fmt": reportes.format_cop(c.monto) if c.monto else None,
        })

    # --- Datos de gráficos ---
    # Dona: convocatorias por estado.
    dona_estado = {
        "labels": [reportes.ESTADOS_CONVOCATORIA[k]["label"] for k in conteo_estado],
        "data": [conteo_estado[k] for k in conteo_estado],
        "colors": [_tono_to_dataset_color(reportes.ESTADOS_CONVOCATORIA[k]["tono"]) for k in conteo_estado],
    }

    # Distribución: cuántas convocatorias tienen 0, 1, 2… proyectos.
    # (Un gráfico con una barra por convocatoria es ilegible: nombres largos y
    #  muchas categorías; el histograma resume mejor la cobertura.)
    conteo_dist = Counter(
        "5+" if c.num_proyectos >= 5 else str(c.num_proyectos)
        for c in convocatorias
    )
    orden_dist = ["0", "1", "2", "3", "4", "5+"]
    barras_proyectos = {
        "labels": [k for k in orden_dist if conteo_dist.get(k)],
        "data": [conteo_dist[k] for k in orden_dist if conteo_dist.get(k)],
    }

    # Embudo: proyectos por etapa del pipeline (sobre las convocatorias filtradas).
    conv_ids = [c.id for c in convocatorias]
    embudo = _embudo_proyectos(models.Proyecto.objects.filter(convocatoria_id__in=conv_ids))

    contexto = {
        "seccion": "convocatorias",
        "filas": filas,
        "total": len(filas),
        "filtros": f,
        "estados_choices": reportes.ESTADOS_CONVOCATORIA,
        "estado_monto_choices": models.Convocatorias._meta.get_field("estado_monto").choices,
        "opciones": {
            "dependencias": models.Dependencia.objects.order_by("dependencia"),
            "aliados": models.Aliados.objects.order_by("aliado"),
            "segmentos": models.Segmentos.objects.order_by("segmento"),
            "sectores": models.Sectores.objects.order_by("codigo_sector"),
            "ubicaciones": models.Ubicacion.objects.order_by("ubicacion"),
        },
        "chart_dona": dona_estado,
        "chart_barras": barras_proyectos,
        "chart_embudo": embudo,
    }

    plantilla = "reportes/_convocatorias_resultados.html" if _is_htmx(request) else "reportes/convocatorias.html"
    return render(request, plantilla, contexto)


def _embudo_proyectos(proyectos_qs):
    """Cuenta cuántos proyectos alcanzaron cada etapa del pipeline."""
    agg = proyectos_qs.aggregate(
        postulado=Count("id", filter=Q(fecha_envio_postulacion_proyecto__isnull=False)),
        subsanacion_solicitada=Count("id", filter=Q(fecha_solicitud_subsanacion_proyecto__isnull=False)),
        subsanacion_enviada=Count("id", filter=Q(fecha_envio_subsanciones_proyecto__isnull=False)),
        resultados=Count("id", filter=Q(fecha_publicacion_resultados_proyecto__isnull=False)),
    )
    return {
        "labels": [reportes.ETAPAS_PROYECTO[k]["label"] for k in reportes.ETAPAS_PIPELINE],
        "data": [agg[k] for k in reportes.ETAPAS_PIPELINE],
    }


def convocatoria_detail(request, pk):
    convocatoria = get_object_or_404(
        models.Convocatorias.objects.prefetch_related(
            "dependencia", "segmento", "sectores", "ubicacion", "aliados"
        ),
        pk=pk,
    )

    proyectos = (
        convocatoria.proyecto_set
        .select_related("dependencia", "responsable")
        .prefetch_related(
            "municipios",
            "beneficiarios_set__beneficiario",
            "fuentefinanciacion_set__vigencia",
            "fuentefinanciacion_set__fuente",
            "indicadormga_set__indicadores",
            "indicadormga_set__vigencia",
        )
        .order_by("nombre_proyecto")
    )

    proyectos_data = []
    for p in proyectos:
        clave, info = reportes.etapa_proyecto(p)
        fuentes = list(p.fuentefinanciacion_set.all())
        proyectos_data.append({
            "obj": p,
            "etapa_clave": clave,
            "etapa": info,
            "fuentes": fuentes,
            "comprometido_fmt": reportes.format_cop(reportes.sumar_montos(ff.valor_comprometido for ff in fuentes)),
            "pagado_fmt": reportes.format_cop(reportes.sumar_montos(ff.valor_pagado for ff in fuentes)),
            "beneficiarios": list(p.beneficiarios_set.all()),
            "indicadores": list(p.indicadormga_set.all()),
        })

    clave_estado, estado_info = reportes.estado_convocatoria(convocatoria)

    contexto = {
        "seccion": "convocatorias",
        "convocatoria": convocatoria,
        "estado": estado_info,
        "monto_fmt": reportes.format_cop(convocatoria.monto) if convocatoria.monto else None,
        "proyectos": proyectos_data,
    }
    return render(request, "reportes/convocatoria_detalle.html", contexto)


# ---------------------------------------------------------------------------
# Vista 2 — Proyectos
# ---------------------------------------------------------------------------
def proyectos_list(request):
    qs = (
        models.Proyecto.objects.all()
        .select_related("convocatoria", "dependencia", "responsable")
        .prefetch_related("municipios")
        .order_by("nombre_proyecto")
    )

    f = {
        "convocatoria": _get(request, "convocatoria"),
        "dependencia": _get(request, "dependencia"),
        "responsable": _get(request, "responsable"),
        "etapa": _get(request, "etapa"),
        "municipio": _get(request, "municipio"),
    }

    if f["convocatoria"]:
        qs = qs.filter(convocatoria_id=f["convocatoria"])
    if f["dependencia"]:
        qs = qs.filter(dependencia_id=f["dependencia"])
    if f["responsable"]:
        qs = qs.filter(responsable_id=f["responsable"])
    if f["municipio"]:
        qs = qs.filter(municipios__id=f["municipio"])
    if f["etapa"] in reportes.ETAPAS_PROYECTO:
        qs = qs.filter(reportes.q_etapa_proyecto(f["etapa"]))

    qs = qs.distinct()
    proyectos = list(qs)

    filas = []
    for p in proyectos:
        clave, info = reportes.etapa_proyecto(p)
        filas.append({"obj": p, "etapa_clave": clave, "etapa": info})

    proyecto_ids = [p.id for p in proyectos]

    # --- Gráficos de dinero (agregación correcta de djmoney) ---
    fuentes = (
        models.FuenteFinanciacion.objects
        .filter(proyecto_id__in=proyecto_ids)
        .select_related("vigencia", "fuente")
    )
    por_vigencia = _dinero_por(fuentes, lambda ff: str(ff.vigencia.vigencia) if ff.vigencia else "—")
    por_fuente = _dinero_por(fuentes, lambda ff: ff.fuente.fuente if ff.fuente else "—")

    # --- Beneficiarios por tipo ---
    benef = (
        models.Beneficiarios.objects
        .filter(proyecto_id__in=proyecto_ids)
        .values("beneficiario__tipo_beneficiario")
        .annotate(total=Sum("numero_beneficiarios"))
        .order_by("-total")
    )
    chart_benef = {
        "labels": [b["beneficiario__tipo_beneficiario"] or "—" for b in benef],
        "data": [b["total"] or 0 for b in benef],
    }

    contexto = {
        "seccion": "proyectos",
        "filas": filas,
        "total": len(filas),
        "filtros": f,
        "etapas_choices": reportes.ETAPAS_PROYECTO,
        "opciones": {
            "convocatorias": models.Convocatorias.objects.order_by("nombre_convocatoria"),
            "dependencias": models.Dependencia.objects.order_by("dependencia"),
            "responsables": models.Responsable.objects.order_by("responsable"),
            "municipios": models.Municipios.objects.order_by("municipio"),
        },
        "chart_vigencia": por_vigencia,
        "chart_fuente": por_fuente,
        "chart_benef": chart_benef,
    }

    plantilla = "reportes/_proyectos_resultados.html" if _is_htmx(request) else "reportes/proyectos.html"
    return render(request, plantilla, contexto)


def _dinero_por(fuentes_qs, clave_func):
    """Agrupa comprometido vs pagado por una clave (vigencia o fuente)."""
    grupos = {}
    for ff in fuentes_qs:
        k = clave_func(ff)
        g = grupos.setdefault(k, {"comprometido": 0, "pagado": 0})
        g["comprometido"] += float(reportes.monto_amount(ff.valor_comprometido))
        g["pagado"] += float(reportes.monto_amount(ff.valor_pagado))
    labels = sorted(grupos.keys())
    return {
        "labels": labels,
        "comprometido": [round(grupos[k]["comprometido"]) for k in labels],
        "pagado": [round(grupos[k]["pagado"]) for k in labels],
    }


def proyecto_detail(request, pk):
    proyecto = get_object_or_404(
        models.Proyecto.objects
        .select_related("convocatoria", "dependencia", "responsable")
        .prefetch_related(
            "municipios", "aliados",
            "beneficiarios_set__beneficiario",
            "fuentefinanciacion_set__vigencia",
            "fuentefinanciacion_set__fuente",
            "indicadormga_set__indicadores",
            "indicadormga_set__vigencia",
        ),
        pk=pk,
    )
    clave, info = reportes.etapa_proyecto(proyecto)
    fuentes = list(proyecto.fuentefinanciacion_set.all())
    contexto = {
        "seccion": "proyectos",
        "p": proyecto,
        "etapa": info,
        "etapa_clave": clave,
        "fuentes": fuentes,
        "comprometido_fmt": reportes.format_cop(reportes.sumar_montos(ff.valor_comprometido for ff in fuentes)),
        "pagado_fmt": reportes.format_cop(reportes.sumar_montos(ff.valor_pagado for ff in fuentes)),
        "beneficiarios": list(proyecto.beneficiarios_set.all()),
        "indicadores": list(proyecto.indicadormga_set.all()),
    }
    return render(request, "reportes/proyecto_detalle.html", contexto)
