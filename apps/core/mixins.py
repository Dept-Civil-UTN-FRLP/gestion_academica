from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


class DepartamentoAccessMixin(LoginRequiredMixin):
    """
    Mixin para verificar acceso por departamento
    """

    departamento_field = "departamento"  # Campo del modelo que tiene el departamento

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Superadmin tiene acceso a todo
        if hasattr(request.user, "profile") and request.user.profile.es_superadmin:
            return super().dispatch(request, *args, **kwargs)

        # Verificar acceso al departamento
        obj = self.get_object() if hasattr(self, "get_object") else None
        if obj:
            departamento = getattr(obj, self.departamento_field, None)
            if departamento and not request.user.profile.tiene_acceso_departamento(
                departamento
            ):
                messages.error(
                    request, "No tienes permiso para acceder a este departamento."
                )
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class SuperadminRequiredMixin(UserPassesTestMixin):
    """
    Mixin para restringir vistas solo a superadmins
    """

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and hasattr(self.request.user, "profile")
            and self.request.user.profile.es_superadmin
        )

    def handle_no_permission(self):
        messages.error(
            self.request, "Solo los superadministradores pueden acceder a esta sección."
        )
        return redirect("home")
