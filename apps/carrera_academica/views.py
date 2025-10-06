from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from datetime import date, timedelta

from .models import CarreraAcademica, JuntaEvaluadora, Evaluacion, Formulario
from .forms import (
    CarreraAcademicaForm,
    JuntaEvaluadoraForm,
    EvaluacionForm,
    FormularioUploadForm,
)


class CarreraAcademicaDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard de carrera académica"""

    template_name = "carrera_academica/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_carreras"] = CarreraAcademica.objects.count()
        context["activas"] = CarreraAcademica.objects.filter(estado="activa").count()
        context["en_licencia"] = CarreraAcademica.objects.filter(
            estado="licencia"
        ).count()
        context["evaluaciones_pendientes"] = Evaluacion.objects.filter(
            estado="pendiente"
        ).count()

        # Carreras próximas a vencer
        hoy = date.today()
        context["proximas_vencer"] = (
            CarreraAcademica.objects.filter(
                estado="activa", fecha_vencimiento_actual__lte=hoy + timedelta(days=180)
            )
            .select_related("cargo__docente")
            .order_by("fecha_vencimiento_actual")[:10]
        )

        return context


class CarreraAcademicaListView(LoginRequiredMixin, ListView):
    """Lista de carreras académicas"""

    model = CarreraAcademica
    template_name = "carrera_academica/carrera_list.html"
    context_object_name = "carreras"
    paginate_by = 20

    def get_queryset(self):
        queryset = CarreraAcademica.objects.select_related("cargo__docente")

        # Filtros
        estado = self.request.GET.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(numero_expediente__icontains=search)
                | Q(cargo__docente__apellido__icontains=search)
                | Q(cargo__docente__nombre__icontains=search)
            )

        return queryset.order_by("-fecha_inicio")


class CarreraAcademicaDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una carrera académica"""

    model = CarreraAcademica
    template_name = "carrera_academica/carrera_detail.html"
    context_object_name = "carrera"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["evaluaciones"] = self.object.evaluaciones.all().order_by(
            "numero_evaluacion"
        )
        context["formularios_recientes"] = self.object.formulario_set.all().order_by(
            "-fecha_entrega"
        )[:10]
        try:
            context["junta"] = self.object.junta
        except self.object.junta.DoesNotExist:
            context["junta"] = None
        return context


class CarreraAcademicaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva carrera académica"""

    model = CarreraAcademica
    form_class = CarreraAcademicaForm
    template_name = "carrera_academica/carrera_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "carrera_academica:carrera_detail", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        messages.success(self.request, "Carrera académica creada exitosamente.")
        return super().form_valid(form)


class CarreraAcademicaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar carrera académica"""

    model = CarreraAcademica
    form_class = CarreraAcademicaForm
    template_name = "carrera_academica/carrera_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "carrera_academica:carrera_detail", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        messages.success(self.request, "Carrera académica actualizada exitosamente.")
        return super().form_valid(form)


class EvaluacionCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva evaluación"""

    model = Evaluacion
    form_class = EvaluacionForm
    template_name = "carrera_academica/evaluacion_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carrera"] = CarreraAcademica.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        form.instance.carrera_academica_id = self.kwargs["pk"]
        messages.success(self.request, "Evaluación creada exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "carrera_academica:carrera_detail",
            kwargs={"pk": self.object.carrera_academica.pk},
        )


class EvaluacionDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una evaluación"""

    model = Evaluacion
    template_name = "carrera_academica/evaluacion_detail.html"
    context_object_name = "evaluacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formularios"] = self.object.formulario_set.all().order_by("tipo")
        return context


class FormularioUploadView(LoginRequiredMixin, CreateView):
    """Subir formulario a una evaluación"""

    model = Formulario
    form_class = FormularioUploadForm
    template_name = "carrera_academica/formulario_upload.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["evaluacion"] = Evaluacion.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        form.instance.evaluacion_id = self.kwargs["pk"]
        form.instance.carrera_academica = form.instance.evaluacion.carrera_academica
        messages.success(self.request, "Formulario cargado exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "carrera_academica:evaluacion_detail",
            kwargs={"pk": self.object.evaluacion.pk},
        )


class ReporteVencimientosCAView(LoginRequiredMixin, TemplateView):
    """Reporte de carreras académicas próximas a vencer"""

    template_name = "carrera_academica/reporte_vencimientos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        hoy = date.today()

        context["vencidas"] = CarreraAcademica.objects.filter(
            estado="activa", fecha_vencimiento_actual__lt=hoy
        ).select_related("cargo__docente")

        context["proximos_6_meses"] = CarreraAcademica.objects.filter(
            estado="activa",
            fecha_vencimiento_actual__gte=hoy,
            fecha_vencimiento_actual__lte=hoy + timedelta(days=180),
        ).select_related("cargo__docente")

        context["proximos_12_meses"] = CarreraAcademica.objects.filter(
            estado="activa",
            fecha_vencimiento_actual__gt=hoy + timedelta(days=180),
            fecha_vencimiento_actual__lte=hoy + timedelta(days=365),
        ).select_related("cargo__docente")

        return context
