from django.contrib import admin
from .models import EtiquetaPS, PSolicitud, JuradoPS


@admin.register(EtiquetaPS)
class EtiquetaPSAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'color']
    search_fields = ['nombre']


class JuradoPSInline(admin.TabularInline):
    model = JuradoPS
    extra = 1


@admin.register(PSolicitud)
class PSolicitudAdmin(admin.ModelAdmin):
    list_display = ['id', 'estudiante', 'tema',
                    'tutor', 'estado_general', 'fecha_solicitud']
    list_filter = ['estado_general', 'fecha_solicitud']
    search_fields = ['tema', 'estudiante__nombre_completo', 'tutor__apellido']
    filter_horizontal = ['etiquetas']
    inlines = [JuradoPSInline]
    readonly_fields = ['fecha_solicitud']
