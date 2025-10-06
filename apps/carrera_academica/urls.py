from django.urls import path
from . import views

app_name = "carrera_academica"

urlpatterns = [
    # Dashboard
    path("", views.CarreraAcademicaDashboardView.as_view(), name="dashboard"),
    # Carreras Académicas
    path("carreras/", views.CarreraAcademicaListView.as_view(), name="carrera_list"),
    path(
        "carreras/crear/",
        views.CarreraAcademicaCreateView.as_view(),
        name="carrera_create",
    ),
    path(
        "carreras/<int:pk>/",
        views.CarreraAcademicaDetailView.as_view(),
        name="carrera_detail",
    ),
    path(
        "carreras/<int:pk>/editar/",
        views.CarreraAcademicaUpdateView.as_view(),
        name="carrera_update",
    ),
    # Evaluaciones
    path(
        "carreras/<int:pk>/nueva-evaluacion/",
        views.EvaluacionCreateView.as_view(),
        name="evaluacion_create",
    ),
    path(
        "evaluaciones/<int:pk>/",
        views.EvaluacionDetailView.as_view(),
        name="evaluacion_detail",
    ),
    # Formularios
    path(
        "evaluaciones/<int:pk>/subir-formulario/",
        views.FormularioUploadView.as_view(),
        name="formulario_upload",
    ),
    # Reportes
    path(
        "reportes/vencimientos/",
        views.ReporteVencimientosCAView.as_view(),
        name="reporte_vencimientos",
    ),
]
