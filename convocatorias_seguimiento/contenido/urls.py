from django.urls import path

from contenido import views

app_name = "reportes"

urlpatterns = [
    path("", views.convocatorias_list, name="convocatorias"),
    path("convocatorias/<int:pk>/", views.convocatoria_detail, name="convocatoria_detalle"),
    path("proyectos/", views.proyectos_list, name="proyectos"),
    path("proyectos/<int:pk>/", views.proyecto_detail, name="proyecto_detalle"),
]
