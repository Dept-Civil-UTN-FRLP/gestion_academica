from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class CarreraAcademica(models.Model):
    """Expediente de carrera académica de un docente"""

    ESTADO_CHOICES = [
        ("activa", "Activa"),
        ("licencia", "En Standby/Licencia"),
        ("finalizada", "Finalizada"),
    ]

    cargo = models.OneToOneField(
        "planta_docente.Cargo",
        on_delete=models.CASCADE,
        limit_choices_to={"caracter__in": ["regular", "ordinario"]},
    )
    numero_expediente = models.CharField(max_length=100, unique=True)
    fecha_inicio = models.DateField()
    fecha_vencimiento_original = models.DateField()
    fecha_vencimiento_actual = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="activa")
    resolucion_designacion = models.CharField(max_length=100)
    resolucion_puesta_en_funcion = models.CharField(max_length=100)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Carrera Académica"
        verbose_name_plural = "Carreras Académicas"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"CA {self.numero_expediente} - {self.cargo.docente}"

    @property
    def docente(self):
        return self.cargo.docente

    @property
    def anios_activa(self):
        """Calcula los años de carrera académica activa"""
        if self.fecha_finalizacion:
            fecha_fin = self.fecha_finalizacion
        else:
            fecha_fin = date.today()
        return (fecha_fin - self.fecha_inicio).days // 365

    @property
    def dias_hasta_vencimiento(self):
        """Días hasta el vencimiento actual"""
        return (self.fecha_vencimiento_actual - date.today()).days

    def aplicar_prorroga(self, meses):
        """Aplica una prórroga a la carrera académica"""
        self.fecha_vencimiento_actual = self.fecha_vencimiento_actual + relativedelta(
            months=meses
        )
        self.save()

    def aplicar_licencia(self, fecha_inicio_licencia, fecha_fin_licencia):
        """Aplica una licencia y ajusta el vencimiento"""
        dias_licencia = (fecha_fin_licencia - fecha_inicio_licencia).days
        self.fecha_vencimiento_actual = self.fecha_vencimiento_actual + relativedelta(
            days=dias_licencia
        )
        self.estado = "licencia"
        self.save()


class JuntaEvaluadora(models.Model):
    """Junta evaluadora de la carrera académica"""

    carrera_academica = models.OneToOneField(
        CarreraAcademica, on_delete=models.CASCADE, related_name="junta"
    )
    titular_frlp = models.ForeignKey(
        "planta_docente.Docente",
        related_name="titular_frlp",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    titular_externo1 = models.CharField(max_length=255)
    institucion_externo1 = models.CharField(max_length=255, blank=True)
    titular_externo2 = models.CharField(max_length=255)
    institucion_externo2 = models.CharField(max_length=255, blank=True)
    suplente_frlp = models.ForeignKey(
        "planta_docente.Docente",
        related_name="suplente_frlp",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    suplente_externo = models.CharField(max_length=255, blank=True)
    institucion_suplente_externo = models.CharField(max_length=255, blank=True)
    veedor_alumno = models.CharField(max_length=255, blank=True)
    veedor_graduado = models.CharField(max_length=255, blank=True)
    fecha_conformacion = models.DateField()

    class Meta:
        verbose_name = "Junta Evaluadora"
        verbose_name_plural = "Juntas Evaluadoras"

    def __str__(self):
        return f"Junta - {self.carrera_academica.numero_expediente}"


class Evaluacion(models.Model):
    """Evaluaciones periódicas de la carrera académica"""

    CALIFICACION_CHOICES = [
        ("insuficiente", "Insuficiente"),
        ("suficiente", "Suficiente"),
        ("bueno", "Bueno"),
        ("muy_bueno", "Muy Bueno"),
        ("excelente", "Excelente"),
    ]

    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("en_proceso", "En Proceso"),
        ("completada", "Completada"),
    ]

    carrera_academica = models.ForeignKey(
        CarreraAcademica, on_delete=models.CASCADE, related_name="evaluaciones"
    )
    numero_evaluacion = models.PositiveIntegerField()
    fecha_iniciada = models.DateField()
    fecha_evaluacion = models.DateField(null=True, blank=True)
    anios_evaluados = models.JSONField(
        help_text="Lista de años evaluados, ej: [2022, 2023]"
    )
    estado = models.CharField(
        max_length=30, choices=ESTADO_CHOICES, default="pendiente"
    )
    calificacion = models.CharField(
        max_length=30, choices=CALIFICACION_CHOICES, null=True, blank=True
    )
    informe_junta = models.FileField(
        upload_to="evaluaciones/informes/", null=True, blank=True
    )
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ["carrera_academica", "numero_evaluacion"]
        unique_together = ["carrera_academica", "numero_evaluacion"]

    def __str__(self):
        return f"Evaluación {self.numero_evaluacion} - {self.carrera_academica.numero_expediente}"

    @property
    def esta_completa(self):
        """Verifica si todos los formularios obligatorios están presentados"""
        # F01-F13 + CV + ENC
        formularios_requeridos = 15
        formularios_presentados = self.formulario_set.filter(evaluacion=self).count()
        return formularios_presentados >= formularios_requeridos


class Formulario(models.Model):
    """Formularios de la carrera académica"""

    TIPO_FORMULARIO_CHOICES = [
        ("F01", "F01 - Docencia de Grado"),
        ("F02", "F02 - Docencia de Posgrado"),
        ("F03", "F03 - Dirección de Tesis"),
        ("F04", "F04 - Formación de RRHH"),
        ("F05", "F05 - Extensión"),
        ("F06", "F06 - Publicaciones"),
        ("F07", "F07 - Transferencia"),
        ("F08", "F08 - Gestión"),
        ("F09", "F09 - Cursos y Congresos"),
        ("F10", "F10 - Distinciones"),
        ("F11", "F11 - Actividades Profesionales"),
        ("F12", "F12 - Proyectos de Investigación"),
        ("F13", "F13 - Desarrollo e Innovación"),
        ("CV", "Curriculum Vitae"),
        ("ENC", "Encuesta Estudiantil"),
    ]

    carrera_academica = models.ForeignKey(CarreraAcademica, on_delete=models.CASCADE)
    evaluacion = models.ForeignKey(
        Evaluacion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Evaluación a la que pertenece (si aplica)",
    )
    tipo = models.CharField(max_length=10, choices=TIPO_FORMULARIO_CHOICES)
    anio_actividad = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Año de la actividad (para formularios anuales)",
    )
    archivo = models.FileField(upload_to="formularios_ca/%Y/")
    fecha_entrega = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    validado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Formulario"
        verbose_name_plural = "Formularios"
        ordering = ["-fecha_entrega"]

    def __str__(self):
        anio_str = f" ({self.anio_actividad})" if self.anio_actividad else ""
        return f"{self.get_tipo_display()}{anio_str} - {self.carrera_academica.docente}"

    def clean(self):
        """Validaciones del formulario"""
        # Validar límites de formularios según tipo
        if self.tipo in [
            "F01",
            "F02",
            "F03",
            "F04",
            "F05",
            "F06",
            "F07",
            "F08",
            "F09",
            "F10",
            "F11",
            "F12",
            "F13",
        ]:
            # Formularios anuales: máximo uno por año
            if self.anio_actividad:
                formularios_existentes = Formulario.objects.filter(
                    carrera_academica=self.carrera_academica,
                    tipo=self.tipo,
                    anio_actividad=self.anio_actividad,
                ).exclude(pk=self.pk)

                if formularios_existentes.exists():
                    raise ValidationError(
                        f"Ya existe un formulario {self.tipo} para el año {self.anio_actividad}"
                    )
