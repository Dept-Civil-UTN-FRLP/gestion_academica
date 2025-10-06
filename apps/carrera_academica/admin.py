from django.contrib import admin
from .models import CarreraAcademica, JuntaEvaluadora, Evaluacion, Formulario


class JuntaEvaluadoraInline(admin.StackedInline):
    model = JuntaEvaluadora
    can_delete = False


class EvaluacionInline(admin.TabularInline):
    model = Evaluacion
    extra = 0
    readonly_fields = ["fecha_iniciada"]


@admin.register(CarreraAcademica)
class CarreraAcademicaAdmin(admin.ModelAdmin):
    list_display = [
        "numero_expediente",
        "docente",
        "estado",
        "fecha_vencimiento_actual",
        "dias_hasta_vencimiento",
    ]
    list_filter = ["estado", "fecha_inicio"]
    search_fields = [
        "numero_expediente",
        "cargo__docente__apellido",
        "cargo__docente__nombre",
    ]
    inlines = [JuntaEvaluadoraInline, EvaluacionInline]
    readonly_fields = ["anios_activa", "dias_hasta_vencimiento"]


class FormularioInline(admin.TabularInline):
    model = Formulario
    extra = 0
    readonly_fields = ["fecha_entrega"]


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = [
        "carrera_academica",
        "numero_evaluacion",
        "estado",
        "calificacion",
        "fecha_evaluacion",
    ]
    list_filter = ["estado", "calificacion"]
    search_fields = ["carrera_academica__numero_expediente"]
    inlines = [FormularioInline]
