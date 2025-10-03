from django.urls import path
from . import views

app_name = 'practica_supervisada'

urlpatterns = [
    # Dashboard
    path('', views.PracticaSupervisadaDashboardView.as_view(), name='dashboard'),

    # Solicitudes
    path('solicitudes/', views.PSolicitudListView.as_view(), name='solicitud_list'),
    path('solicitudes/crear/', views.PSolicitudCreateView.as_view(),
         name='solicitud_create'),
    path('solicitudes/<int:pk>/', views.PSolicitudDetailView.as_view(),
         name='solicitud_detail'),
    path('solicitudes/<int:pk>/editar/',
         views.PSolicitudUpdateView.as_view(), name='solicitud_update'),

    # Dictámenes
    path('solicitudes/<int:pk>/dictaminar-plan/',
         views.DictaminarPlanView.as_view(), name='dictaminar_plan'),
    path('solicitudes/<int:pk>/dictaminar-informe/',
         views.DictaminarInformeView.as_view(), name='dictaminar_informe'),
]
