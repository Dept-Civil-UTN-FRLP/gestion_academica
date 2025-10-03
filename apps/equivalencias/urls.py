from django.urls import path
from . import views

app_name = 'equivalencias'

urlpatterns = [
    # Dashboard
    path('', views.EquivalenciasDashboardView.as_view(), name='dashboard'),

    # Estudiantes
    path('estudiantes/', views.EstudianteListView.as_view(), name='estudiante_list'),
    path('estudiantes/crear/', views.EstudianteCreateView.as_view(),
         name='estudiante_create'),
    path('estudiantes/<int:pk>/', views.EstudianteDetailView.as_view(),
         name='estudiante_detail'),
    path('estudiantes/<int:pk>/editar/',
         views.EstudianteUpdateView.as_view(), name='estudiante_update'),

    # Solicitudes
    path('solicitudes/', views.SolicitudListView.as_view(), name='solicitud_list'),
    path('solicitudes/crear/', views.SolicitudCreateView.as_view(),
         name='solicitud_create'),
    path('solicitudes/<int:pk>/', views.SolicitudDetailView.as_view(),
         name='solicitud_detail'),
    path('solicitudes/<int:pk>/editar/',
         views.SolicitudUpdateView.as_view(), name='solicitud_update'),
    path('solicitudes/<int:pk>/completar/',
         views.SolicitudCompletarView.as_view(), name='solicitud_completar'),
]
