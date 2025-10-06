from django.db import models


class DepartamentoFilterManager(models.Manager):
    """Manager que filtra por departamento del usuario"""

    def for_user(self, user):
        """Retorna queryset filtrado por departamentos del usuario"""
        if not user.is_authenticated:
            return self.none()

        # Superadmin ve todo
        if hasattr(user, "profile") and user.profile.es_superadmin:
            return self.all()

        # Filtrar por departamentos asignados
        if hasattr(user, "profile"):
            return self.filter(departamento__in=user.profile.departamentos.all())

        return self.none()
