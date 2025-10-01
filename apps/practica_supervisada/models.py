from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from datetime import date


class EtiquetaPS(models.Model):
    """Etiquetas para clasificar prácticas supervisadas"""
    nombre = models.CharField(max_length=50, unique=True)
    color = models.CharField(
        max_length=7, default='#007bff', help_text="Color en formato hexadecimal")

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class PSolicitud(models.Model):
    """Solicitud de Práctica Supervisada"""
    ESTADO_CHOICES = [
        ('en_proceso', 'En Proceso'),
        ('plan_aprobado', 'Plan Aprobado'),
        ('en_ejecucion', 'En Ejecución'),
        ('informe_presentado', 'Informe Presentado'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    estudiante = models.ForeignKey(
        'equivalencias.Estudiante', on_delete=models.PROTECT)
    fecha_solicitud = models.DateField(auto_now_add=True)
    estado_general = models.CharField(
        max_length=30, choices=ESTADO_CHOICES, default='en_proceso')
    tema = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    etiquetas = models.ManyToManyField(EtiquetaPS, blank=True)
    tutor = models.ForeignKey(
        'planta_docente.Docente',
        related_name='tutor_ps',
        on_delete=models.PROTECT
    )
    supervisor = models.CharField(
        max_length=255,
        blank=True,
        help_text="Nombre del supervisor. Puede ser externo"
    )
    empresa_institucion = models.CharField(max_length=255, blank=True)
    plan_trabajo = models.FileField(upload_to='ps/planes/')
    fecha_aprobacion_plan = models.DateField(null=True, blank=True)
    informe_final = models.FileField(
        upload_to='ps/informes/', null=True, blank=True)
    fecha_presentacion_informe = models.DateField(null=True, blank=True)
    fecha_completada = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Práctica Supervisada"
        verbose_name_plural = "Prácticas Supervisadas"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"PS {self.id} - {self.estudiante} - {self.tema}"

    def notificar_jurados(self, tipo='plan'):
        """Notifica a los jurados sobre nueva documentación"""
        jurados = self.jurados.all()
        asunto = f"Nueva documentación - Práctica Supervisada: {self.tema}"

        if tipo == 'plan':
            mensaje = f"Se ha cargado el plan de trabajo para la práctica supervisada '{self.tema}'."
        else:
            mensaje = f"Se ha cargado el informe final para la práctica supervisada '{self.tema}'."

        for jurado in jurados:
            if jurado.docente and jurado.docente.correos.filter(es_principal=True).exists():
                email = jurado.docente.correos.get(es_principal=True).email
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                )


class JuradoPS(models.Model):
    """Jurados evaluadores de práctica supervisada"""
    ESTADO_DICTAMEN_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('aprobado_observaciones', 'Aprobado con Observaciones'),
        ('denegado', 'Denegado'),
    ]

    solicitud = models.ForeignKey(
        PSolicitud, related_name='jurados', on_delete=models.CASCADE)
    docente = models.ForeignKey(
        'planta_docente.Docente',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    nombre_externo = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Nombre completo si es jurado externo"
    )
    institucion_externa = models.CharField(max_length=255, blank=True)
    estado_dictamen_plan = models.CharField(
        max_length=30,
        choices=ESTADO_DICTAMEN_CHOICES,
        default='pendiente'
    )
    observaciones_plan = models.TextField(blank=True)
    fecha_dictamen_plan = models.DateField(null=True, blank=True)
    estado_dictamen_informe = models.CharField(
        max_length=30,
        choices=ESTADO_DICTAMEN_CHOICES,
        default='pendiente'
    )
    observaciones_informe = models.TextField(blank=True)
    fecha_dictamen_informe = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Jurado"
        verbose_name_plural = "Jurados"

    def __str__(self):
        if self.docente:
            return str(self.docente)
        return self.nombre_externo or "Jurado sin asignar"

    def clean(self):
        """Validar que tenga docente o nombre externo"""
        from django.core.exceptions import ValidationError
        if not self.docente and not self.nombre_externo:
            raise ValidationError(
                'Debe especificar un docente o un nombre externo.')

    def save(self, *args, **kwargs):
        """Actualizar estado general de la solicitud al guardar"""
        super().save(*args, **kwargs)
        self._actualizar_estado_solicitud()

    def _actualizar_estado_solicitud(self):
        """Actualiza el estado de la solicitud según dictámenes de jurados"""
        solicitud = self.solicitud
        jurados = solicitud.jurados.all()

        # Verificar plan de trabajo
        if solicitud.estado_general == 'en_proceso':
            dictamenes_plan = [j.estado_dictamen_plan for j in jurados]
            if all(d == 'aprobado' or d == 'aprobado_observaciones' for d in dictamenes_plan):
                solicitud.estado_general = 'plan_aprobado'
                solicitud.fecha_aprobacion_plan = date.today()
                solicitud.save()

        # Verificar informe final
        if solicitud.estado_general == 'informe_presentado':
            dictamenes_informe = [j.estado_dictamen_informe for j in jurados]
            if all(d == 'aprobado' or d == 'aprobado_observaciones' for d in dictamenes_informe):
                solicitud.estado_general = 'completada'
                solicitud.fecha_completada = date.today()
                solicitud.save()
