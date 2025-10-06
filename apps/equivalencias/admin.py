from django.contrib import admin
from .models import (
    Estudiante,
    AsignaturaParaEquivalencia,
    SolicitudEquivalencia,
    DetalleSolicitud,
    DocumentoAdjunto,
)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ["nombre_completo", "dni_pasaporte", "email_estudiante", "carrera"]
    search_fields = ["nombre_completo", "dni_pasaporte", "email_estudiante"]
    list_filter = ["carrera"]


@admin.register(AsignaturaParaEquivalencia)
class AsignaturaParaEquivalenciaAdmin(admin.ModelAdmin):
    list_display = ["asignatura", "docente_responsable"]
    search_fields = ["asignatura__nombre"]


class DetalleSolicitudInline(admin.TabularInline):
    model = DetalleSolicitud
    extra = 1


class DocumentoAdjuntoInline(admin.TabularInline):
    model = DocumentoAdjunto
    extra = 1
    readonly_fields = ["fecha_carga"]


@admin.register(SolicitudEquivalencia)
class SolicitudEquivalenciaAdmin(admin.ModelAdmin):
    list_display = ["id", "estudiante", "fecha_inicio", "estado_general", "progreso"]
    list_filter = ["estado_general", "fecha_inicio"]
    search_fields = ["estudiante__nombre_completo"]
    inlines = [DetalleSolicitudInline, DocumentoAdjuntoInline]
    readonly_fields = ["fecha_inicio"]
