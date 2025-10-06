from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib import messages
from django.shortcuts import redirect
from datetime import date

from .models import (
    Estudiante,
    SolicitudEquivalencia,
    DetalleSolicitud,
    DocumentoAdjunto,
)
from .forms import EstudianteForm, SolicitudEquivalenciaForm, DocumentoAdjuntoForm
from apps.core.mixins import DepartamentoAccessMixin


class EquivalenciasDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard de equivalencias con estadísticas"""

    template_name = "equivalencias/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Estadísticas
        context["total_solicitudes"] = SolicitudEquivalencia.objects.count()
        context["en_proceso"] = SolicitudEquivalencia.objects.filter(
            estado_general="proceso"
        ).count()
        context["completadas"] = SolicitudEquivalencia.objects.filter(
            estado_general="completada"
        ).count()
        context["total_estudiantes"] = Estudiante.objects.count()

        # Solicitudes recientes
        context["solicitudes_recientes"] = SolicitudEquivalencia.objects.select_related(
            "estudiante"
        ).order_by("-fecha_inicio")[:10]

        return context


class EstudianteListView(LoginRequiredMixin, ListView):
    """Lista de estudiantes"""

    model = Estudiante
    template_name = "equivalencias/estudiante_list.html"
    context_object_name = "estudiantes"
    paginate_by = 20

    def get_queryset(self):
        queryset = Estudiante.objects.all()

        # Búsqueda
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(nombre_completo__icontains=search)
                | Q(dni_pasaporte__icontains=search)
                | Q(email_estudiante__icontains=search)
            )

        return queryset.order_by("nombre_completo")


class EstudianteDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un estudiante"""

    model = Estudiante
    template_name = "equivalencias/estudiante_detail.html"
    context_object_name = "estudiante"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["solicitudes"] = self.object.solicitudequivalencia_set.all().order_by(
            "-fecha_inicio"
        )
        return context


class EstudianteCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo estudiante"""

    model = Estudiante
    form_class = EstudianteForm
    template_name = "equivalencias/estudiante_form.html"
    success_url = reverse_lazy("equivalencias:estudiante_list")

    def form_valid(self, form):
        messages.success(self.request, "Estudiante creado exitosamente.")
        return super().form_valid(form)


class EstudianteUpdateView(LoginRequiredMixin, UpdateView):
    """Editar estudiante"""

    model = Estudiante
    form_class = EstudianteForm
    template_name = "equivalencias/estudiante_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "equivalencias:estudiante_detail", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        messages.success(self.request, "Estudiante actualizado exitosamente.")
        return super().form_valid(form)


class SolicitudListView(LoginRequiredMixin, ListView):
    """Lista de solicitudes de equivalencia"""

    model = SolicitudEquivalencia
    template_name = "equivalencias/solicitud_list.html"
    context_object_name = "solicitudes"
    paginate_by = 20

    def get_queryset(self):
        queryset = SolicitudEquivalencia.objects.select_related("estudiante")

        # Filtros
        estado = self.request.GET.get("estado")
        if estado:
            queryset = queryset.filter(estado_general=estado)

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(estudiante__nombre_completo__icontains=search)
                | Q(estudiante__dni_pasaporte__icontains=search)
            )

        return queryset.order_by("-fecha_inicio")


class SolicitudDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una solicitud de equivalencia"""

    model = SolicitudEquivalencia
    template_name = "equivalencias/solicitud_detail.html"
    context_object_name = "solicitud"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detalles"] = self.object.detallesolicitud_set.select_related(
            "asignatura__asignatura", "asignatura__docente_responsable"
        ).all()
        context["documentos"] = self.object.documentoadjunto_set.all()
        return context


class SolicitudCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva solicitud de equivalencia"""

    model = SolicitudEquivalencia
    form_class = SolicitudEquivalenciaForm
    template_name = "equivalencias/solicitud_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "equivalencias:solicitud_detail", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        messages.success(self.request, "Solicitud creada exitosamente.")
        return super().form_valid(form)


class SolicitudUpdateView(LoginRequiredMixin, UpdateView):
    """Editar solicitud de equivalencia"""

    model = SolicitudEquivalencia
    form_class = SolicitudEquivalenciaForm
    template_name = "equivalencias/solicitud_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "equivalencias:solicitud_detail", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        messages.success(self.request, "Solicitud actualizada exitosamente.")
        return super().form_valid(form)


class SolicitudCompletarView(LoginRequiredMixin, UpdateView):
    """Completar una solicitud de equivalencia"""

    model = SolicitudEquivalencia
    fields = ["acta_firmada"]
    template_name = "equivalencias/solicitud_completar.html"

    def form_valid(self, form):
        form.instance.estado_general = "completada"
        form.instance.fecha_completada = date.today()
        messages.success(self.request, "Solicitud completada exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "equivalencias:solicitud_detail", kwargs={"pk": self.object.pk}
        )
