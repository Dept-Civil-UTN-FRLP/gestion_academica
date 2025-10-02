"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),

    # Página principal
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Módulos de la aplicación
    path('planta-docente/', include('apps.planta_docente.urls')),
    #path('equivalencias/', include('apps.equivalencias.urls')),
    #path('practica-supervisada/', include('apps.practica_supervisada.urls')),
    #path('carrera-academica/', include('apps.carrera_academica.urls')),

    # API REST (opcional)
    #path('api/', include('apps.api.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

# Personalizar títulos del admin
admin.site.site_header = "Gestión Académica - Administración"
admin.site.site_title = "Gestión Académica"
admin.site.index_title = "Panel de Administración"
