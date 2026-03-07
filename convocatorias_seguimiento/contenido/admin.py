from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline
from contenido import models
from contenido import forms


# ─── Inlines ────────────────────────────────────────────────────────────────

class BeneficiariosInline(TabularInline):
    model = models.Beneficiarios
    form = forms.BeneficariosForm
    tab = True
    extra = 1
    verbose_name = "Beneficiario"
    verbose_name_plural = "Beneficiarios"


class IndicadoresInline(TabularInline):
    model = models.IndicadorMGA
    form = forms.IndicadoresForm
    tab = True
    extra = 1
    verbose_name = "Indicador MGA"
    verbose_name_plural = "Indicadores MGA"


# Modelos simples ─────────────────────────────────────────────

@admin.register(models.Dependencia)
class DependenciaAdmin(UnfoldModelAdmin):
    list_display = ("dependencia", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("dependencia",)
    ordering = ("dependencia",)


@admin.register(models.Responsable)
class ResponsableAdmin(UnfoldModelAdmin):
    list_display = ("responsable", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("responsable",)
    ordering = ("responsable",)


@admin.register(models.Aliados)
class AliadosAdmin(UnfoldModelAdmin):
    list_display = ("aliado", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("aliado",)
    ordering = ("aliado",)


@admin.register(models.Segmentos)
class SegmentosAdmin(UnfoldModelAdmin):
    list_display = ("segmento", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("segmento",)
    ordering = ("segmento",)


@admin.register(models.Sectores)
class SectoresAdmin(UnfoldModelAdmin):
    list_display = ("codigo_sector", "sector", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("codigo_sector", "sector")
    ordering = ("codigo_sector",)


@admin.register(models.Estado)
class EstadoAdmin(UnfoldModelAdmin):
    list_display = ("estado", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("estado",)
    ordering = ("estado",)


@admin.register(models.Municipios)
class MunicipiosAdmin(UnfoldModelAdmin):
    list_display = ("municipio", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("municipio",)
    ordering = ("municipio",)


@admin.register(models.Ubicacion)
class UbicacionAdmin(UnfoldModelAdmin):
    list_display = ("ubicacion", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("ubicacion",)
    ordering = ("ubicacion",)


@admin.register(models.ClasificacionBeneficiario)
class ClasificacionBeneficiarioAdmin(UnfoldModelAdmin):
    list_display = ("tipo_beneficiario", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("tipo_beneficiario",)
    ordering = ("tipo_beneficiario",)


@admin.register(models.ClasificacionIndicadorMGA)
class ClasificacionIndicadorAdmin(UnfoldModelAdmin):
    list_display = ("codigo_indicador", "nombre_indicador", "meta_indicador", "fecha_creacion")
    search_fields = ("codigo_indicador", "nombre_indicador")
    ordering = ("codigo_indicador",)


# ─── Modelos principales ─────────────────────────────────────────────────────

@admin.register(models.Convocatorias)
class ConvocatoriasAdmin(UnfoldModelAdmin):
    list_display = (
        "nombre_convocatoria",
        "estado",
        "monto",
        "fecha_apertura",
        "fecha_cierre",
        "contacto",
    )
    list_filter = ("estado", "segmento", "sectores")
    search_fields = ("nombre_convocatoria", "contacto", "que_ofrece")
    filter_horizontal = ("sectores", "dependencia", "segmento", "ubicacion")
    ordering = ("-fecha_apertura",)
    fieldsets = (
        ("Información general", {
            "fields": (
                "nombre_convocatoria",
                "estado",
                "monto",
                "contacto",
            )
        }),
        ("Fechas", {
            "fields": ("fecha_apertura", "fecha_cierre")
        }),
        ("Clasificación", {
            "fields": ("dependencia", "segmento", "sectores", "ubicacion")
        }),
        ("Detalles", {
            "fields": (
                "que_ofrece",
                "quienes_pueden_participar",
                "publico_priorizado",
            )
        }),
    )


@admin.register(models.Proyecto)
class ProyectoAdmin(UnfoldModelAdmin):
    list_display = (
        "nombre_proyecto",
        "convocatoria",
        "dependencia",
        "responsable",
        "valor_proyecto",
        "monto_contrapartida",
        "bpin",
        "fecha_creacion",
    )
    list_filter = ("dependencia", "responsable", "convocatoria")
    search_fields = ("nombre_proyecto", "bpin")
    filter_horizontal = ("municipios",)
    ordering = ("-fecha_creacion",)
    inlines = (BeneficiariosInline, IndicadoresInline)
    fieldsets = (
        ("Información general", {
            "fields": (
                "nombre_proyecto",
                "convocatoria",
                "bpin",
            )
        }),
        ("Responsables", {
            "fields": ("dependencia", "responsable")
        }),
        ("Financiero", {
            "fields": ("valor_proyecto", "monto_contrapartida")
        }),
        ("Ubicación", {
            "fields": ("municipios",)
        }),
    )
