from django.contrib import admin
from .models import Bloque, Area, Departamento, Carrera


@admin.register(Bloque)
class BloqueAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    search_fields = ["nombre"]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
    search_fields = ["nombre"]


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "codigo"]
    search_fields = ["nombre", "codigo"]


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ["nombre", "departamento_cabecera", "codigo"]
    list_filter = ["departamento_cabecera"]
    search_fields = ["nombre", "codigo"]
