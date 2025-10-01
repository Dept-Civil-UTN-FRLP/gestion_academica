from django.contrib import admin
from .models import Docente, Correo, Asignatura, Resolucion, Cargo


class CorreoInline(admin.TabularInline):
    model = Correo
    extra = 1


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ['apellido', 'nombre', 'documento', 'legajo', 'edad']
    search_fields = ['apellido', 'nombre', 'documento', 'legajo']
    list_filter = ['fecha_nacimiento']
    inlines = [CorreoInline]
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']


@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'carrera',
                    'nivel', 'forma_dictado', 'departamento']
    list_filter = ['carrera', 'nivel', 'forma_dictado',
                   'departamento', 'es_obligatoria']
    search_fields = ['nombre', 'codigo']
    filter_horizontal = ['areas', 'bloques']


@admin.register(Resolucion)
class ResolucionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'anio', 'origen', 'objeto', 'fecha_emision']
    list_filter = ['anio', 'origen', 'objeto']
    search_fields = ['numero', 'observaciones']


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['docente', 'asignatura', 'categoria',
                    'dedicacion', 'estado', 'fecha_vencimiento']
    list_filter = ['estado', 'caracter', 'categoria', 'dedicacion']
    search_fields = ['docente__apellido',
                     'docente__nombre', 'asignatura__nombre']
    date_hierarchy = 'fecha_inicio'
