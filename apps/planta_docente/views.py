from .models import Cargo
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count, Sum
from django.contrib import messages
from datetime import date, timedelta

from .models import Docente, Asignatura, Cargo, Resolucion
from .forms import DocenteForm, AsignaturaForm, CargoForm, ResolucionForm
from apps.core.mixins import DepartamentoAccessMixin


class PlantaDocenteDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de planta docente"""

    template_name = "planta_docente/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Filtrar por departamentos del usuario
        if hasattr(user, "profile"):
            if user.profile.es_superadmin:
                cargos = Cargo.objects.all()
            else:
                cargos = Cargo.objects.filter(
                    asignatura__departamento__in=user.profile.departamentos.all()
                )
        else:
            cargos = Cargo.objects.none()

        # Estadísticas
        context["total_docentes"] = cargos.values("docente").distinct().count()
        context["cargos_activos"] = cargos.filter(estado="activo").count()
        context["cargos_por_vencer"] = cargos.filter(
            estado="activo", fecha_vencimiento__lte=date.today() + timedelta(days=90)
        ).count()

        # Cargos próximos a vencer
        context["vencimientos_proximos"] = (
            cargos.filter(
                estado="activo",
                fecha_vencimiento__lte=date.today() + timedelta(days=90),
            )
            .select_related("docente", "asignatura")
            .order_by("fecha_vencimiento")[:10]
        )

        return context


class DocenteListView(LoginRequiredMixin, ListView):
    """Lista de docentes con búsqueda y filtros"""

    model = Docente
    template_name = "planta_docente/docente_list.html"
    context_object_name = "docentes"
    paginate_by = 20

    def get_queryset(self):
        queryset = Docente.objects.all()

        # Búsqueda
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(apellido__icontains=search)
                | Q(nombre__icontains=search)
                | Q(documento__icontains=search)
                | Q(legajo__icontains=search)
            )

        return queryset.order_by("apellido", "nombre")


class DocenteDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un docente"""

    model = Docente
    template_name = "planta_docente/docente_detail.html"
    context_object_name = "docente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cargos"] = self.object.cargos.select_related(
            "asignatura", "resolucion_alta"
        ).order_by("-fecha_inicio")
        return context


class DocenteCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo docente"""

    model = Docente
    form_class = DocenteForm
    template_name = "planta_docente/docente_form.html"
    success_url = reverse_lazy("planta_docente:docente_list")

    def form_valid(self, form):
        messages.success(self.request, "Docente creado exitosamente.")
        return super().form_valid(form)


class DocenteUpdateView(LoginRequiredMixin, UpdateView):
    """Editar docente"""

    model = Docente
    form_class = DocenteForm
    template_name = "planta_docente/docente_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "planta_docente:docente_detail", kwargs={"pk": self.object.pk}
        )

    def form_valid(self, form):
        messages.success(self.request, "Docente actualizado exitosamente.")
        return super().form_valid(form)


class DocenteDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar docente"""

    model = Docente
    template_name = "planta_docente/docente_confirm_delete.html"
    success_url = reverse_lazy("planta_docente:docente_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Docente eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)


class AsignaturaListView(LoginRequiredMixin, ListView):
    """Lista de asignaturas"""

    model = Asignatura
    template_name = "planta_docente/asignatura_list.html"
    context_object_name = "asignaturas"
    paginate_by = 20

    def get_queryset(self):
        queryset = Asignatura.objects.select_related("departamento", "carrera")

        # Filtros
        departamento = self.request.GET.get("departamento")
        carrera = self.request.GET.get("carrera")
        nivel = self.request.GET.get("nivel")

        if departamento:
            queryset = queryset.filter(departamento_id=departamento)
        if carrera:
            queryset = queryset.filter(carrera_id=carrera)
        if nivel:
            queryset = queryset.filter(nivel=nivel)

        return queryset.order_by("carrera", "nivel", "nombre")


class AsignaturaDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una asignatura"""

    model = Asignatura
    template_name = "planta_docente/asignatura_detail.html"
    context_object_name = "asignatura"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cargos_activos"] = (
            self.object.cargo_set.filter(estado="activo")
            .select_related("docente")
            .order_by("categoria")
        )
        return context


class AsignaturaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva asignatura"""

    model = Asignatura
    form_class = AsignaturaForm
    template_name = "planta_docente/asignatura_form.html"
    success_url = reverse_lazy("planta_docente:asignatura_list")


class AsignaturaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar asignatura"""

    model = Asignatura
    form_class = AsignaturaForm
    template_name = "planta_docente/asignatura_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "planta_docente:asignatura_detail", kwargs={"pk": self.object.pk}
        )


class CargoListView(LoginRequiredMixin, ListView):
    """Lista de cargos"""

    model = Cargo
    template_name = "planta_docente/cargo_list.html"
    context_object_name = "cargos"
    paginate_by = 20

    def get_queryset(self):
        queryset = Cargo.objects.select_related(
            "docente", "asignatura", "resolucion_alta"
        )

        # Filtros
        estado = self.request.GET.get("estado", "activo")
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset.order_by("-fecha_inicio")


class CargoDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un cargo"""

    model = Cargo
    template_name = "planta_docente/cargo_detail.html"
    context_object_name = "cargo"


class CargoCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo cargo"""

    model = Cargo
    form_class = CargoForm
    template_name = "planta_docente/cargo_form.html"
    success_url = reverse_lazy("planta_docente:cargo_list")


class CargoUpdateView(LoginRequiredMixin, UpdateView):
    """Editar cargo"""

    model = Cargo
    form_class = CargoForm
    template_name = "planta_docente/cargo_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "planta_docente:cargo_detail", kwargs={"pk": self.object.pk}
        )


class CargoBajaView(LoginRequiredMixin, UpdateView):
    """Dar de baja un cargo"""

    model = Cargo
    fields = ["fecha_final", "observaciones"]
    template_name = "planta_docente/cargo_baja.html"

    def form_valid(self, form):
        form.instance.estado = "baja"
        messages.success(self.request, "Cargo dado de baja exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "planta_docente:cargo_detail", kwargs={"pk": self.object.pk}
        )


class ResolucionListView(LoginRequiredMixin, ListView):
    """Lista de resoluciones"""

    model = Resolucion
    template_name = "planta_docente/resolucion_list.html"
    context_object_name = "resoluciones"
    paginate_by = 20

    def get_queryset(self):
        return Resolucion.objects.all().order_by("-anio", "-numero")


class ResolucionCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva resolución"""

    model = Resolucion
    form_class = ResolucionForm
    template_name = "planta_docente/resolucion_form.html"
    success_url = reverse_lazy("planta_docente:resolucion_list")


class ReportePlantaCompletaView(LoginRequiredMixin, TemplateView):
    """Reporte de planta docente completa"""

    template_name = "planta_docente/reporte_planta.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Queryset base que usaremos para todo
        cargos_qs = Cargo.objects.filter(estado="activo")

        # --- 1. CÁLCULO DE TOTALES POR DEPARTAMENTO (LA MAGIA DE ANNOTATE) ---
        # Agrupamos por departamento y calculamos todos los totales para cada uno en una sola consulta.
        resumen_por_departamento = (
            cargos_qs.values(
                "asignatura__departamento__pk",  # Usamos el ID para búsquedas
                "asignatura__departamento__nombre",  # y el nombre para mostrar
            )
            .annotate(
                total_cargos=Count("id"),
                total_cargos_reg=Count(
                    "id", filter=Q(caracter__in=["regular", "concursado"])
                ),
                total_exclusivas=Count("id", filter=Q(dedicacion="exclusiva")),
                total_exclusivas_reg=Count(
                    "id",
                    filter=Q(
                        dedicacion="exclusiva", caracter__in=["regular", "concursado"]
                    ),
                ),
                # Ajustado a 'semidedicacion'
                total_semis=Count("id", filter=Q(dedicacion="semidedicacion")),
                total_semis_reg=Count(
                    "id",
                    filter=Q(
                        dedicacion="semidedicacion",
                        caracter__in=["regular", "concursado"],
                    ),
                ),
                total_simples=Count("id", filter=Q(dedicacion="simple")),
                total_simples_reg=Count(
                    "id",
                    filter=Q(
                        dedicacion="simple", caracter__in=["regular", "concursado"]
                    ),
                ),
            )
            .order_by("asignatura__departamento__nombre")
        )

        # Convertimos la lista de resultados en un diccionario para buscar fácilmente en el template
        # La llave será el ID del departamento
        context["resumen_por_depto_dict"] = {
            item["asignatura__departamento__pk"]: item
            for item in resumen_por_departamento
        }

        # --- 2. CÁLCULO DE TOTALES GENERALES (COMO YA LO TENÍAS) ---
        # Usamos la misma lógica que ya tenías para el resumen general.
        resumen_general = cargos_qs.aggregate(
            total_cargos=Count("id"),
            total_cargos_reg=Count(
                "id", filter=Q(caracter__in=["regular", "concursado"])
            ),
            total_exclusivas=Count("id", filter=Q(dedicacion="exclusiva")),
            total_exclusivas_reg=Count(
                "id",
                filter=Q(
                    dedicacion="exclusiva", caracter__in=["regular", "concursado"]
                ),
            ),
            total_semis=Count("id", filter=Q(dedicacion="semidedicacion")),
            total_semis_reg=Count(
                "id",
                filter=Q(
                    dedicacion="semidedicacion", caracter__in=["regular", "concursado"]
                ),
            ),
            total_simples=Count("id", filter=Q(dedicacion="simple")),
            total_simples_reg=Count(
                "id",
                filter=Q(dedicacion="simple", caracter__in=["regular", "concursado"]),
            ),
        )
        context["resumen_general"] = resumen_general
        context["total_docentes"] = cargos_qs.values("docente").distinct().count()
        context["total_departamentos"] = (
            cargos_qs.values("asignatura__departamento").distinct().count()
        )

        # --- 3. PASAMOS LA LISTA COMPLETA DE CARGOS PARA LA TABLA DETALLADA ---
        context["cargos"] = cargos_qs.select_related(
            "docente", "asignatura", "asignatura__departamento", "asignatura__carrera"
        ).order_by(
            "asignatura__departamento__nombre", "docente__apellido", "docente__nombre"
        )

        return context


class ReporteVencimientosView(LoginRequiredMixin, TemplateView):
    """Reporte de cargos próximos a vencer"""

    template_name = "planta_docente/reporte_vencimientos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        hoy = date.today()

        context["vencidos"] = Cargo.objects.filter(
            estado="activo", fecha_vencimiento__lt=hoy
        ).select_related("docente", "asignatura")

        context["proximos_30"] = Cargo.objects.filter(
            estado="activo",
            fecha_vencimiento__gte=hoy,
            fecha_vencimiento__lte=hoy + timedelta(days=30),
        ).select_related("docente", "asignatura")

        context["proximos_90"] = Cargo.objects.filter(
            estado="activo",
            fecha_vencimiento__gt=hoy + timedelta(days=30),
            fecha_vencimiento__lte=hoy + timedelta(days=90),
        ).select_related("docente", "asignatura")

        return context
