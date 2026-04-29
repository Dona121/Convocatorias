from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline
from contenido import models
from contenido import forms
from unfold.sections import TableSection, TemplateSection
from unfold.datasets import BaseDataset
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse

class BeneficiariosInline(TabularInline):
    model = models.Beneficiarios
    form = forms.BeneficiariosForm
    extra = 1
    tab = True
    verbose_name = "Beneficiario"
    verbose_name_plural = "Beneficiarios"
    show_count = True
    hide_title = True
    can_delete = True
    autocomplete_fields = ("beneficiario",)
    list_fullwidth = True

class FuentesInline(TabularInline):
    model = models.FuenteFinanciacion
    form = forms.FuentesForm
    extra = 1
    tab = True
    verbose_name = "Fuente de Financiación"
    verbose_name_plural = "Fuentes de Financiación"
    show_count = True
    hide_title = True
    can_delete = True
    ordering_field = "id"
    autocomplete_fields = ("fuente","vigencia")
    list_fullwidth = True

class IndicadoresInline(TabularInline):
    model = models.IndicadorMGA
    form = forms.IndicadoresForm
    extra = 1
    tab = True
    verbose_name = "Indicador MGA"
    verbose_name_plural = "Indicadores MGA"
    show_count = True
    hide_title = True
    can_delete = True
    ordering_field = "id"
    autocomplete_fields = ("indicadores","vigencia")
    list_fullwidth = True

class SeccionProyectos(TableSection):
    verbose_name = "Proyectos"
    height = 500
    related_name = 'proyecto_set'
    fields = ["enlace_proyecto","proyecto_postulado","dependencia"]

    def enlace_proyecto(self,obj):
        admin = reverse("admin:contenido_proyecto_changelist") + f"?id={obj.id}" 
        return format_html("<a href='{}'>{}</a>",admin,obj.nombre_proyecto)
    
    enlace_proyecto.short_description = "Nombre del Proyecto"

    def proyecto_postulado(self, obj):
        base = "padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600;white-space:nowrap;display:inline-block;"
        postulado = "Proyecto postulado"
        no_postulado= "Proyecto no postulado"
        if obj.fecha_envio_postulacion_proyecto:
            return format_html("<span style='{}background-color:#dcfce7;color:#166534;'>{}</span>",base,postulado)
        return format_html("<span style='{}background-color:#fee2e2;color:#991b1b;'>{}</p>",base,no_postulado)

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


@admin.register(models.ClasificacionAliados)
class ClasificacionAliadosAdmin(UnfoldModelAdmin):
    list_display = ("clasificacion_aliado",)


@admin.register(models.Aliados)
class AliadosAdmin(UnfoldModelAdmin):
    list_display = ("clasificacion","aliado", "fecha_creacion", "fecha_actualizacion")
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

@admin.register(models.ClasificacionFuenteFinanciacion)
class EstadoAdmin(UnfoldModelAdmin):
    list_display = ("tipo_de_fuente","subtipo","fuente")
    search_fields = ("tipo_de_fuente","subtipo","fuente")
    ordering = ("fecha_creacion",)

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
    list_display = (
        "codigo_meta", 
        "codigo_indicador", 
        "nombre_indicador",
        "medido_a_atraves_de",
        "meta_del_cuatrienio",
        "tipo_acumulacion",
        "responsable",
        "meta_fisica_esp_2024",
        "meta_fisica_esp_2025",
        "meta_fisica_esp_2026",
        "meta_fisica_esp_2027",
    )
    search_fields = ("codigo_indicador", "nombre_indicador","responsable","medido_a_atraves_de")
    ordering = ("codigo_meta",)

    # --- Métodos de formato para Indicadores ---
    @admin.display(description="Meta cuatrienio", ordering="meta_cuatrienio")
    def meta_del_cuatrienio(self, obj):
        return f"{obj.meta_cuatrienio:,.2f}" if obj.meta_cuatrienio is not None else "-"

    @admin.display(description="Meta física esp. 2024", ordering="meta_fisica_esperada_2024")
    def meta_fisica_esp_2024(self, obj):
        return f"{obj.meta_fisica_esperada_2024:,.2f}" if obj.meta_fisica_esperada_2024 is not None else "-"

    @admin.display(description="Meta física esp. 2025", ordering="meta_fisica_esperada_2025")
    def meta_fisica_esp_2025(self, obj):
        return f"{obj.meta_fisica_esperada_2025:,.2f}" if obj.meta_fisica_esperada_2025 is not None else "-"

    @admin.display(description="Meta física esp. 2026", ordering="meta_fisica_esperada_2026")
    def meta_fisica_esp_2026(self, obj):
        return f"{obj.meta_fisica_esperada_2026:,.2f}" if obj.meta_fisica_esperada_2026 is not None else "-"

    @admin.display(description="Meta física esp. 2027", ordering="meta_fisica_esperada_2027")
    def meta_fisica_esp_2027(self, obj):
        return f"{obj.meta_fisica_esperada_2027:,.2f}" if obj.meta_fisica_esperada_2027 is not None else "-"


@admin.register(models.Convocatorias)
class ConvocatoriasAdmin(UnfoldModelAdmin):
    conditional_fields = {
        "monto" : "estado_monto == 'ES'"
    }
    list_per_page = 20
    list_display = (
        "id",
        "nombre_convocatoria",
        "monto", 
        "estado",
        'numero_proyectos',
        "fecha_creacion",
    )
    list_sections = [
        SeccionProyectos
    ]
    radio_fields = {"estado_monto":admin.HORIZONTAL}
    list_filter = ("segmento", "sectores")
    search_fields = ("nombre_convocatoria", "contacto", "que_ofrece")
    list_display_links = ("id","nombre_convocatoria")
    filter_horizontal = ("sectores", "aliados" ,"dependencia", "segmento", "ubicacion")
    ordering = ("id",)
    fieldsets = (
        ("Información general", {
            "fields": (
                "nombre_convocatoria",
                "estado_monto",
                "monto", 
                "contacto",
                "objetivo",
                "enlace_convocatoria",
                "enlace_del_actor"
            )
        }),
        ("Fechas", {
            "fields": ("fecha_apertura", "fecha_cierre")
        }),
        ("Clasificación", {
            "fields": ("aliados","dependencia", "segmento", "sectores", "ubicacion")
        }),
        ("Detalles", {
            "fields": (
                "imagen_convocatoria",
                "que_ofrece",
                "quienes_pueden_participar",
                "publico_priorizado",
            )
        }),
    )
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related(
                "proyecto_set",
            )
        )

    def numero_proyectos(self,obj):
        proyectos = obj.proyecto_set.all()
        numero_proyectos = proyectos.count()
        base = "padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600;white-space:nowrap;display:inline-block;"
        plural = "Sin proyectos"
        if numero_proyectos == 1:
            plural = " Proyecto"
            return format_html("<span style='{}background-color:#fef9c3;color:#854d0e;'>{}{}</span>",base,numero_proyectos,plural)
        elif numero_proyectos > 1: 
            plural = " Proyectos"
            return format_html("<span style='{}background-color:#dcfce7;color:#166534;'>{}{}</span>",base,numero_proyectos,plural)
        return format_html("<span style='{}background-color:#fee2e2;color:#991b1b;'>{}</span>",base,plural)
    
    def estado(self, obj):
        fecha_cierre = obj.fecha_cierre
        if fecha_cierre:
            dias = (fecha_cierre.date() - timezone.now().date()).days

            base = "padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600;white-space:nowrap;display:inline-block;"

            if dias < 0:
                return format_html(
                    "<span style='{}background-color:#fee2e2;color:#991b1b;'>Cerrada</span>", base
                )
            elif dias <= 7:
                return format_html(
                    "<span style='{}background-color:#fee2e2;color:#991b1b;'>{} días para cierre</span>", base, dias
                )
            elif dias <= 15:
                return format_html(
                    "<span style='{}background-color:#fef9c3;color:#854d0e;'>{} días para cierre</span>", base, dias
                )
            else:
                return format_html(
                    "<span style='{}background-color:#dcfce7;color:#166534;'>{} días para cierre</span>", base, dias
                )
        return "Pendiente asignar fecha"
    
@admin.register(models.Proyecto)
class ProyectoAdmin(UnfoldModelAdmin):
    inlines = (BeneficiariosInline, IndicadoresInline,FuentesInline)
    list_display = (
        "id",
        "nombre_proyecto",
        "convocatoria",
        "dependencia",
        "responsable", 
        "bpin",
        "proyecto_postulado",
    )
    autocomplete_fields = ("convocatoria","dependencia","responsable")
    list_filter = ("dependencia", "responsable", "convocatoria")
    search_fields = ("nombre_proyecto", "bpin","convocatoria")
    list_display_links = ("id","nombre_proyecto")
    filter_horizontal = ("municipios",)
    ordering = ("id",)
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
        ("Ubicación", {
            "fields": ("municipios",)
        }),
        ("Aliados" , {
            "fields" : ("aliados",)
        }),
        ("Fechas de Trazabilidad" , {
            "fields" : ("fecha_envio_postulacion_proyecto","fecha_solicitud_subsanacion_proyecto",
                        "fecha_envio_subsanciones_proyecto","fecha_publicacion_resultados_proyecto")
        }
        )
    )

    def proyecto_postulado(self, obj):
        base = "padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600;white-space:nowrap;display:inline-block;"
        postulado = "Proyecto postulado"
        no_postulado= "Proyecto no postulado"
        if obj.fecha_envio_postulacion_proyecto:
            return format_html("<span style='{}background-color:#dcfce7;color:#166534;'>{}</span>",base,postulado)
        return format_html("<span style='{}background-color:#fee2e2;color:#991b1b;'>{}</p>",base,no_postulado)