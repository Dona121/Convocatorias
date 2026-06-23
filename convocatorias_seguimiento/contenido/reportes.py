"""Lógica de dominio para la capa pública de reportes (solo lectura).

Aquí viven los estados DERIVADOS (no hay campos de estado en los modelos) y las
utilidades de agregación/formato de dinero (djmoney guarda la moneda aparte).
Se mantiene separado de las vistas para poder reutilizarlo y probarlo.
"""
from decimal import Decimal

from django.db.models import Q
from django.utils import timezone


# ---------------------------------------------------------------------------
# Estado DERIVADO de una convocatoria
# ---------------------------------------------------------------------------
# Cada estado: clave interna, etiqueta visible y "tono" para el color (mapea a
# las clases del semáforo institucional de GUIA_DISEÑO.md).
ESTADOS_CONVOCATORIA = {
    "abierta":    {"label": "Abierta",           "tono": "verde"},
    "proxima":    {"label": "Próxima",           "tono": "azul"},
    "cerrada":    {"label": "Cerrada",           "tono": "rojo"},
    "incompleta": {"label": "Fechas incompletas", "tono": "ambar"},
}


def estado_convocatoria(convocatoria, ahora=None):
    """Devuelve (clave, info) del estado derivado de una convocatoria.

    - Falta fecha_apertura o fecha_cierre -> "Fechas incompletas".
    - hoy < apertura -> "Próxima"; apertura <= hoy <= cierre -> "Abierta";
      hoy > cierre -> "Cerrada".
    """
    ahora = ahora or timezone.now()
    apertura = convocatoria.fecha_apertura
    cierre = convocatoria.fecha_cierre

    if not apertura or not cierre:
        clave = "incompleta"
    elif ahora < apertura:
        clave = "proxima"
    elif ahora > cierre:
        clave = "cerrada"
    else:
        clave = "abierta"
    return clave, ESTADOS_CONVOCATORIA[clave]


def q_estado_convocatoria(clave, ahora=None):
    """Traduce un estado derivado a un filtro de base de datos (Q)."""
    ahora = ahora or timezone.now()
    if clave == "incompleta":
        return Q(fecha_apertura__isnull=True) | Q(fecha_cierre__isnull=True)
    completas = Q(fecha_apertura__isnull=False, fecha_cierre__isnull=False)
    if clave == "proxima":
        return completas & Q(fecha_apertura__gt=ahora)
    if clave == "cerrada":
        return completas & Q(fecha_cierre__lt=ahora)
    if clave == "abierta":
        return completas & Q(fecha_apertura__lte=ahora) & Q(fecha_cierre__gte=ahora)
    return Q()


# ---------------------------------------------------------------------------
# Etapa DERIVADA de un proyecto (pipeline de fechas)
# ---------------------------------------------------------------------------
# Orden del pipeline: postulado -> subsanación solicitada -> subsanación
# enviada -> resultados publicados. La etapa es la MÁS avanzada alcanzada.
ETAPAS_PROYECTO = {
    "resultados":              {"label": "Resultados publicados",   "tono": "verde",  "orden": 4},
    "subsanacion_enviada":     {"label": "Subsanación enviada",     "tono": "azul",   "orden": 3},
    "subsanacion_solicitada":  {"label": "Subsanación solicitada",  "tono": "ambar",  "orden": 2},
    "postulado":               {"label": "Postulado",               "tono": "azul",   "orden": 1},
    "sin_fechas":              {"label": "Sin fechas registradas",  "tono": "gris",   "orden": 0},
}

# Etapas reales del embudo, de la primera a la última (excluye "sin_fechas").
ETAPAS_PIPELINE = ["postulado", "subsanacion_solicitada", "subsanacion_enviada", "resultados"]


def etapa_proyecto(proyecto):
    """Devuelve (clave, info) de la etapa más avanzada alcanzada por el proyecto."""
    if proyecto.fecha_publicacion_resultados_proyecto:
        clave = "resultados"
    elif proyecto.fecha_envio_subsanciones_proyecto:
        clave = "subsanacion_enviada"
    elif proyecto.fecha_solicitud_subsanacion_proyecto:
        clave = "subsanacion_solicitada"
    elif proyecto.fecha_envio_postulacion_proyecto:
        clave = "postulado"
    else:
        clave = "sin_fechas"
    return clave, ETAPAS_PROYECTO[clave]


def q_etapa_proyecto(clave):
    """Traduce una etapa derivada a un filtro de base de datos (Q)."""
    res = Q(fecha_publicacion_resultados_proyecto__isnull=False)
    env = Q(fecha_envio_subsanciones_proyecto__isnull=False)
    sol = Q(fecha_solicitud_subsanacion_proyecto__isnull=False)
    pos = Q(fecha_envio_postulacion_proyecto__isnull=False)

    if clave == "resultados":
        return res
    if clave == "subsanacion_enviada":
        return env & ~res
    if clave == "subsanacion_solicitada":
        return sol & ~env & ~res
    if clave == "postulado":
        return pos & ~sol & ~env & ~res
    if clave == "sin_fechas":
        return ~pos & ~sol & ~env & ~res
    return Q()


# ---------------------------------------------------------------------------
# Dinero (djmoney): agregación y formato en COP
# ---------------------------------------------------------------------------
def monto_amount(valor):
    """Devuelve el Decimal subyacente de un MoneyField (o 0 si es None)."""
    if valor is None:
        return Decimal("0")
    # djmoney expone Money.amount; un Sum() puede devolver ya un Decimal.
    return getattr(valor, "amount", valor)


def sumar_montos(valores):
    """Suma una lista de Money/Decimal/None devolviendo un único Decimal.

    Se suman los importes asumiendo una sola moneda (COP por defecto del
    proyecto). Si llegaran monedas mixtas, se agregan los importes igualmente;
    la moneda se rotula como COP al formatear.
    """
    total = Decimal("0")
    for v in valores:
        total += monto_amount(v)
    return total


def format_cop(valor):
    """Formatea un importe como pesos colombianos: '$ 1.234.567'."""
    monto = monto_amount(valor)
    entero = int(monto.quantize(Decimal("1")))
    # Separador de miles con punto (convención es-CO).
    return "$ " + f"{entero:,}".replace(",", ".")
