from django.urls import path
from . import views

app_name = "planta_docente"

urlpatterns = [
    # Dashboard
    path("", views.PlantaDocenteDashboardView.as_view(), name="dashboard"),
    # Docentes
    path("docentes/", views.DocenteListView.as_view(), name="docente_list"),
    path("docentes/crear/", views.DocenteCreateView.as_view(), name="docente_create"),
    path(
        "docentes/<int:pk>/", views.DocenteDetailView.as_view(), name="docente_detail"
    ),
    path(
        "docentes/<int:pk>/editar/",
        views.DocenteUpdateView.as_view(),
        name="docente_update",
    ),
    path(
        "docentes/<int:pk>/eliminar/",
        views.DocenteDeleteView.as_view(),
        name="docente_delete",
    ),
    # Asignaturas
    path("asignaturas/", views.AsignaturaListView.as_view(), name="asignatura_list"),
    path(
        "asignaturas/crear/",
        views.AsignaturaCreateView.as_view(),
        name="asignatura_create",
    ),
    path(
        "asignaturas/<int:pk>/",
        views.AsignaturaDetailView.as_view(),
        name="asignatura_detail",
    ),
    path(
        "asignaturas/<int:pk>/editar/",
        views.AsignaturaUpdateView.as_view(),
        name="asignatura_update",
    ),
    # Cargos
    path("cargos/", views.CargoListView.as_view(), name="cargo_list"),
    path("cargos/crear/", views.CargoCreateView.as_view(), name="cargo_create"),
    path("cargos/<int:pk>/", views.CargoDetailView.as_view(), name="cargo_detail"),
    path(
        "cargos/<int:pk>/editar/", views.CargoUpdateView.as_view(), name="cargo_update"
    ),
    path("cargos/<int:pk>/dar-baja/", views.CargoBajaView.as_view(), name="cargo_baja"),
    # Resoluciones
    path("resoluciones/", views.ResolucionListView.as_view(), name="resolucion_list"),
    path(
        "resoluciones/crear/",
        views.ResolucionCreateView.as_view(),
        name="resolucion_create",
    ),
    # Reportes
    path(
        "reportes/planta-completa/",
        views.ReportePlantaCompletaView.as_view(),
        name="reporte_planta",
    ),
    path(
        "reportes/vencimientos/",
        views.ReporteVencimientosView.as_view(),
        name="reporte_vencimientos",
    ),
]
