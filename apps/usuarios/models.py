from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Perfil de usuario vinculado a departamentos"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    departamentos = models.ManyToManyField(
        'core.Departamento',
        related_name='usuarios',
        blank=True
    )
    es_superadmin = models.BooleanField(
        default=False,
        help_text="Acceso a todos los departamentos"
    )
    telefono = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def tiene_acceso_departamento(self, departamento):
        """Verifica si el usuario tiene acceso a un departamento"""
        if self.es_superadmin:
            return True
        return self.departamentos.filter(id=departamento.id).exists()
