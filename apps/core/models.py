from django.db import models


class Bloque(models.Model):
    """Bloques temáticos de asignaturas"""

    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Bloque"
        verbose_name_plural = "Bloques"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Area(models.Model):
    """Áreas de conocimiento"""

    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    """Departamentos académicos"""

    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=20, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    """Carreras universitarias"""

    nombre = models.CharField(max_length=100, unique=True)
    departamento_cabecera = models.ForeignKey(
        Departamento, on_delete=models.PROTECT, related_name="carreras"
    )
    codigo = models.CharField(max_length=20, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
