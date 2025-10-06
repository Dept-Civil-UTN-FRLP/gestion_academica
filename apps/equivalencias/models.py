from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Estudiante(models.Model):
    """Estudiantes que solicitan equivalencias"""

    nombre_completo = models.CharField(max_length=255)
    email_estudiante = models.EmailField(null=True, blank=True)
    dni_pasaporte = models.CharField(max_length=50, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    carrera = models.ForeignKey(
        "core.Carrera", on_delete=models.PROTECT, null=True, blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ["nombre_completo"]

    def __str__(self):
        return self.nombre_completo


class AsignaturaParaEquivalencia(models.Model):
    """Configuración de asignaturas para equivalencias"""

    asignatura = models.OneToOneField(
        "planta_docente.Asignatura",
        on_delete=models.CASCADE,
        related_name="config_equivalencia",
    )
    docente_responsable = models.ForeignKey(
        "planta_docente.Docente", on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        verbose_name = "Asignatura para Equivalencia"
        verbose_name_plural = "Asignaturas para Equivalencia"

    def __str__(self):
        return str(self.asignatura)

    def save(self, *args, **kwargs):
        """Auto-asignar docente responsable si no está definido"""
        if not self.docente_responsable:
            # Buscar el docente con mayor categoría y antigüedad en la asignatura
            from django.db.models import Min

            cargo_principal = (
                self.asignatura.cargo_set.filter(
                    estado="activo", caracter__in=["ordinario", "regular"]
                )
                .order_by("categoria", "fecha_inicio")
                .first()
            )

            if cargo_principal:
                self.docente_responsable = cargo_principal.docente

        super().save(*args, **kwargs)


class SolicitudEquivalencia(models.Model):
    """Solicitud de equivalencia de un estudiante"""

    ESTADO_CHOICES = [
        ("proceso", "En Proceso"),
        ("completada", "Completada"),
        ("cancelada", "Cancelada"),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignaturas = models.ManyToManyField(
        AsignaturaParaEquivalencia, through="DetalleSolicitud"
    )
    fecha_inicio = models.DateField(auto_now_add=True)
    estado_general = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="proceso"
    )
    acta_firmada = models.FileField(
        upload_to="actas_equivalencia/", null=True, blank=True
    )
    fecha_completada = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Solicitud de Equivalencia"
        verbose_name_plural = "Solicitudes de Equivalencia"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"Solicitud {self.id} - {self.estudiante}"

    @property
    def progreso(self):
        """Calcula el progreso de la solicitud"""
        total = self.detallesolicitud_set.count()
        if total == 0:
            return "0 de 0"
        dictaminadas = self.detallesolicitud_set.exclude(
            estado_asignatura="pendiente"
        ).count()
        return f"{dictaminadas} de {total}"

    @property
    def porcentaje_progreso(self):
        """Porcentaje de avance"""
        total = self.detallesolicitud_set.count()
        if total == 0:
            return 0
        dictaminadas = self.detallesolicitud_set.exclude(
            estado_asignatura="pendiente"
        ).count()
        return int((dictaminadas / total) * 100)


class DetalleSolicitud(models.Model):
    """Detalle de cada asignatura en la solicitud"""

    ESTADO_ASIGNATURA_CHOICES = [
        ("pendiente", "Pendiente"),
        ("enviada", "Enviada al Docente"),
        ("aprobada", "Aprobada"),
        ("aprobada_pc", "Aprobada con Programa Complementario"),
        ("denegada", "Denegada"),
    ]

    solicitud = models.ForeignKey(SolicitudEquivalencia, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(AsignaturaParaEquivalencia, on_delete=models.CASCADE)
    estado_asignatura = models.CharField(
        max_length=50, choices=ESTADO_ASIGNATURA_CHOICES, default="pendiente"
    )
    detalle_pc = models.TextField(
        blank=True, help_text="Detallar qué debe cubrir el programa complementario"
    )
    fecha_dictamen = models.DateField(null=True, blank=True)
    observaciones_docente = models.TextField(blank=True)

    class Meta:
        verbose_name = "Detalle de Solicitud"
        verbose_name_plural = "Detalles de Solicitud"
        unique_together = ["solicitud", "asignatura"]

    def __str__(self):
        return f"{self.solicitud} - {self.asignatura}"


class DocumentoAdjunto(models.Model):
    """Documentos adjuntos a las solicitudes"""

    solicitud = models.ForeignKey(SolicitudEquivalencia, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to="adjuntos_equivalencia/%Y/%m/")
    nombre_archivo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=500, blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Documento Adjunto"
        verbose_name_plural = "Documentos Adjuntos"
        ordering = ["-fecha_carga"]

    def __str__(self):
        return f"{self.nombre_archivo} - {self.solicitud}"
