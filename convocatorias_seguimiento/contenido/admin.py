from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline, StackedInline
from contenido import models
from contenido import forms
from unfold.sections import TableSection, TemplateSection
from unfold.datasets import BaseDataset
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.contrib.admin import register
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
from guardian.admin import GuardedModelAdmin
from django.db.models import Prefetch
from django.template.defaultfilters import truncatechars, truncatechars_html
from django.views.generic import TemplateView
from unfold.views import UnfoldModelAdminViewMixin
from django.urls import path
from django.shortcuts import get_object_or_404

class PerfilUsuarioInline(StackedInline):
    model = models.PerfilUsuario
    can_delete = False
    filter_horizontal = ("dependencia",)

class UsuarioAdmin(BaseUserAdmin):
    inlines = [PerfilUsuarioInline]

admin.site.unregister(User)

@register(User)
class UserAdmin(GuardedModelAdmin,UsuarioAdmin,UnfoldModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

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


    def has_view_permission(self, request,obj=None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )
    
    def has_change_permission(self, request, obj =None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )
        
    def has_add_permission(self, request, obj=None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )

class ComentariosInline(StackedInline):
    model = models.ComentariosProyectos
    form = forms.ComentariosDelProyecto
    # class Media:
    #     css = {
    #         "all" : (
    #             "css/comentarios.css",
    #         )
    #     }

    extra = 1
    tab = True

    readonly_fields = ("fecha_creacion",)

    fields = (
        "fecha_creacion",
        "comentario",
    )
    show_count = True
    hide_title = True
    can_delete = True
    collapsible = True

    def has_view_permission(self, request,obj=None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )
    
    def has_change_permission(self, request, obj =None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )
        
    def has_add_permission(self, request, obj=None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )
    
class FuentesInline(StackedInline):
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
    collapsible = True

    def has_view_permission(self, request,obj=None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )
    
    def has_change_permission(self, request, obj =None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )
        
    def has_add_permission(self, request, obj=None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )

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

    def has_view_permission(self, request,obj=None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )
    
    def has_change_permission(self, request, obj =None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )
        
    def has_add_permission(self, request, obj=None):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="Seguimiento de Proyectos") 
            or request.user.groups.filter(name="Administrador")
        )

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
class DependenciaAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("dependencia", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("dependencia",)
    ordering = ("dependencia",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser


@admin.register(models.Responsable)
class ResponsableAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("responsable", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("responsable",)
    ordering = ("responsable",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser

@admin.register(models.ClasificacionAliados)
class ClasificacionAliadosAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("clasificacion_aliado",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser


@admin.register(models.Aliados)
class AliadosAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("clasificacion","aliado", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("aliado",)
    ordering = ("aliado",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser
    

@admin.register(models.Segmentos)
class SegmentosAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("segmento", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("segmento",)
    ordering = ("segmento",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser


@admin.register(models.Sectores)
class SectoresAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("codigo_sector", "sector", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("codigo_sector", "sector")
    ordering = ("codigo_sector",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser

@admin.register(models.ClasificacionFuenteFinanciacion)
class EstadoAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("tipo_de_fuente","subtipo","fuente")
    search_fields = ("tipo_de_fuente","subtipo","fuente")
    ordering = ("fecha_creacion",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser

@admin.register(models.Municipios)
class MunicipiosAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("municipio", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("municipio",)
    ordering = ("municipio",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser

@admin.register(models.Ubicacion)
class UbicacionAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("ubicacion", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("ubicacion",)
    ordering = ("ubicacion",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser


@admin.register(models.ClasificacionBeneficiario)
class ClasificacionBeneficiarioAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("tipo_beneficiario", "fecha_creacion", "fecha_actualizacion")
    search_fields = ("tipo_beneficiario",)
    ordering = ("tipo_beneficiario",)

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser


@admin.register(models.ClasificacionVigencia)
class VigenciaAdmin(UnfoldModelAdmin):
    list_display = ("id", "vigencia",)
    search_fields = ("vigencia",)


@admin.register(models.ClasificacionIndicadorMGA)
class ClasificacionIndicadorAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
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

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser

class TarjetaConvocatoriaView(
    UnfoldModelAdminViewMixin,
    TemplateView
):
    title = "Tarjeta convocatoria"
    permission_required = ()
    template_name = "convocatoria.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        convocatoria = get_object_or_404(
            models.Convocatorias,
            pk=self.kwargs["object_id"]
        )

        context["convocatoria"] = convocatoria

        return context

@admin.register(models.Convocatorias)
class ConvocatoriasAdmin(UnfoldModelAdmin,ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    conditional_fields = {
        "monto" : "estado_monto == 'ES'"
    }
    list_per_page = 20
    list_display = (
        "nombre_convocatoria_recortada",
        "detalle_convocatoria",
        "monto",
        "fecha_apertura",
        "fecha_cierre",
        "estado",
        'numero_proyectos',
        "enlace_convocatoria_formato",
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
                "observaciones_monto",
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
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        try:
            usuario_actual = request.user.perfilusuario
            dependencias = [id_dependencia.id for id_dependencia in usuario_actual.dependencia.all()]

            return (
                qs.filter(dependencia__id__in=dependencias).distinct()
                .prefetch_related(
                    Prefetch(
                        "proyecto_set",
                        queryset=models.Proyecto.objects.filter(
                            dependencia__in=dependencias
                        )
                    )
                )
            )

        except models.PerfilUsuario.DoesNotExist:
            return qs.none()
            

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

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser
    
    def nombre_convocatoria_recortada(self, obj):
        return truncatechars(obj.nombre_convocatoria,50)
    
    nombre_convocatoria_recortada.short_description = "Nombre de la Convocatoria"

    def enlace_convocatoria_formato(self, obj):
        url_convocatoria = ""
        if obj.enlace_convocatoria:
            url_convocatoria = truncatechars_html(
                format_html("<a href='{}' style='text-decoration-line:underline'>{}</a>",obj.enlace_convocatoria,obj.enlace_convocatoria),
                50
                )
            return url_convocatoria
        return url_convocatoria
            
    
    enlace_convocatoria_formato.short_description = "Enlace de la convocatoria"

    def get_urls(self):

        custom_view = self.admin_site.admin_view(
            TarjetaConvocatoriaView.as_view(
                model_admin=self
            )
        )

        custom_urls = [
            path(
                "<int:object_id>/",
                custom_view,
                name="tarjeta_convocatoria",
            ),
        ]

        return custom_urls + super().get_urls()
    
    def detalle_convocatoria(self, obj):
        url = reverse("admin:tarjeta_convocatoria", args=[obj.id])
        return format_html(
            '<a href="{}" style="display:inline-flex; align-items:center; gap:6px;">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" '
            'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>'
            '</svg>'
            '</a>',
            url
        )

    detalle_convocatoria.short_description = "Detalle"

@admin.register(models.Proyecto)
class ProyectoAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    inlines = (BeneficiariosInline, IndicadoresInline,FuentesInline,ComentariosInline)
    list_display = (
        "id",
        "nombre_proyecto_recortado",
        "bpin",
        "convocatoria",
        "dependencia",
        "responsable", 
        "proyecto_postulado",
        "fecha_envio_postulacion_proyecto"
    )
    autocomplete_fields = ("dependencia","responsable")
    raw_id_fields = ("convocatoria",)
    list_filter = ("dependencia", "responsable", "convocatoria")
    search_fields = ("nombre_proyecto", "bpin","convocatoria__nombre_convocatoria")
    list_display_links = ("id","nombre_proyecto")
    filter_horizontal = ("municipios",)
    ordering = ("id",)
    readonly_fields = ("fecha_creacion","fecha_actualizacion")
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
            "fields" : ("fecha_creacion","fecha_actualizacion","fecha_envio_postulacion_proyecto","fecha_solicitud_subsanacion_proyecto",
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

    def has_import_permission(self, request):
        return request.user.is_superuser

    def has_export_permission(self, request):
        return request.user.is_superuser
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        try:
            usuario_actual = request.user.perfilusuario
            dependencias = usuario_actual.dependencia.all()
            return qs.filter(dependencia__in=dependencias)
        except models.PerfilUsuario.DoesNotExist:
            return qs.none()
    
    def nombre_proyecto_recortado(self, obj):
        return truncatechars(obj.nombre_proyecto,50)
    
    nombre_proyecto_recortado.short_description = "Nombre del Proyecto"
    

@admin.register(models.Beneficiarios)
class BeneficiariosProyectosAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("beneficiario","proyecto","numero_beneficiarios",)

    def has_import_permission(self,request):
        return request.user.is_superuser
    
    def has_export_permission(self,request):
        return request.user.is_superuser

@admin.register(models.IndicadorMGA)
class IndicadoresProyectosAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("vigencia","indicadores","proyecto","meta_proyecto")

    def has_import_permission(self, request):
        return request.user.is_superuser
    
    def has_export_permission(self, request):
            return request.user.is_superuser
    
@admin.register(models.FuenteFinanciacion)
class FuentesProyectosAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ("vigencia","fuente","proyecto","valor_comprometido","valor_pagado")

    def has_import_permission(self, request):
        return request.user.is_superuser
    
    def has_export_permission(self, request):
            return request.user.is_superuser