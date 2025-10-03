from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages

from .models import PSolicitud, JuradoPS, EtiquetaPS
from .forms import PSolicitudForm, JuradoPSForm, DictamenPlanForm, DictamenInformeForm


class PracticaSupervisadaDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard de prácticas supervisadas"""
    template_name = 'practica_supervisada/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_solicitudes'] = PSolicitud.objects.count()
        context['en_proceso'] = PSolicitud.objects.filter(
            estado_general='en proceso').count()
        context['completadas'] = PSolicitud.objects.filter(
            estado_general='completada').count()
        context['pendientes_dictamen'] = PSolicitud.objects.filter(
            estado_general__in=['en proceso', 'informe_presentado']
        ).count()

        context['solicitudes_recientes'] = PSolicitud.objects.select_related(
            'estudiante', 'tutor'
        ).order_by('-fecha_solicitud')[:10]

        return context


class PSolicitudListView(LoginRequiredMixin, ListView):
    """Lista de solicitudes de práctica supervisada"""
    model = PSolicitud
    template_name = 'practica_supervisada/solicitud_list.html'
    context_object_name = 'solicitudes'
    paginate_by = 20

    def get_queryset(self):
        queryset = PSolicitud.objects.select_related('estudiante', 'tutor')

        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado_general=estado)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(estudiante__nombre_completo__icontains=search) |
                Q(tema__icontains=search)
            )

        return queryset.order_by('-fecha_solicitud')


class PSolicitudDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una solicitud de práctica supervisada"""
    model = PSolicitud
    template_name = 'practica_supervisada/solicitud_detail.html'
    context_object_name = 'solicitud'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jurados'] = self.object.jurados.all()
        return context


class PSolicitudCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva solicitud de práctica supervisada"""
    model = PSolicitud
    form_class = PSolicitudForm
    template_name = 'practica_supervisada/solicitud_form.html'

    def get_success_url(self):
        return reverse_lazy('practica_supervisada:solicitud_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Solicitud creada exitosamente.')
        return super().form_valid(form)


class PSolicitudUpdateView(LoginRequiredMixin, UpdateView):
    """Editar solicitud de práctica supervisada"""
    model = PSolicitud
    form_class = PSolicitudForm
    template_name = 'practica_supervisada/solicitud_form.html'

    def get_success_url(self):
        return reverse_lazy('practica_supervisada:solicitud_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Solicitud actualizada exitosamente.')
        return super().form_valid(form)


class DictaminarPlanView(LoginRequiredMixin, UpdateView):
    """Dictaminar plan de trabajo"""
    model = JuradoPS
    form_class = DictamenPlanForm
    template_name = 'practica_supervisada/dictaminar_plan.html'

    def get_success_url(self):
        return reverse_lazy('practica_supervisada:solicitud_detail',
                            kwargs={'pk': self.object.solicitud.pk})


class DictaminarInformeView(LoginRequiredMixin, UpdateView):
    """Dictaminar informe final"""
    model = JuradoPS
    form_class = DictamenInformeForm
    template_name = 'practica_supervisada/dictaminar_informe.html'

    def get_success_url(self):
        return reverse_lazy('practica_supervisada:solicitud_detail',
                            kwargs={'pk': self.object.solicitud.pk})
