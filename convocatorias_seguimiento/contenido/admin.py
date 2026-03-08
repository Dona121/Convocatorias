from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline
from contenido import models
from contenido import forms

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


@admin.register(models.ClasificacionVigencia)
class VigenciaAdmin(UnfoldModelAdmin):
    list_display = ("id", "vigencia",)
    search_fields = ("vigencia",)


@admin.register(models.ClasificacionIndicadorMGA)
class ClasificacionIndicadorAdmin(UnfoldModelAdmin):
    list_display = ("codigo_meta", "codigo_indicador", "nombre_indicador",
                    "medido_a_atraves_de","meta_cuatrienio","tipo_acumulacion","responsable",
                    "meta_fisica_esperada_2024","meta_fisica_esperada_2025","meta_fisica_esperada_2026","meta_fisica_esperada_2027",)
    search_fields = ("codigo_indicador", "nombre_indicador","responsable","medido_a_atraves_de")
    ordering = ("codigo_meta",)

@admin.register(models.Convocatorias)
class ConvocatoriasAdmin(UnfoldModelAdmin):
    list_display = (
        "nombre_convocatoria",
        "estado",
        "monto_formateado",
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

    @admin.display(description="monto", ordering="monto")
    def monto_formateado(self, obj):
        return f"${intcomma(round(obj.monto, 2)):,.2f}" if obj.monto is not None else "-"


@admin.register(models.Proyecto)
class ProyectoAdmin(UnfoldModelAdmin):
    list_display = (
        "nombre_proyecto",
        "convocatoria",
        "dependencia",
        "responsable",
        "valor_proyecto_formateado",
        "monto_contrapartida_formateado",
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

    @admin.display(description="valor_proyecto", ordering="valor_proyecto")
    def valor_proyecto_formateado(self, obj):
        return f"${intcomma(round(obj.valor_proyecto, 2)):,.2f}" if obj.valor_proyecto is not None else "-"

    @admin.display(description="monto_contrapartida", ordering="monto_contrapartida")
    def monto_contrapartida_formateado(self, obj):
        return f"${intcomma(round(obj.monto_contrapartida, 2)):,.2f}" if obj.monto_contrapartida is not None else "-"