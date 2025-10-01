from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class Docente(models.Model):
    """Información básica del docente"""
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    legajo = models.CharField(
        max_length=20, unique=True, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    cv_confirmado = models.BooleanField(default=False)
    cv_fecha_confirmacion = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    @property
    def edad(self):
        """Calcula la edad actual del docente"""
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (
                self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def cv_requiere_actualizacion(self):
        """Verifica si el CV debe actualizarse (anualmente)"""
        if not self.cv_fecha_confirmacion:
            return True
        return date.today() > self.cv_fecha_confirmacion + timedelta(days=365)


class Correo(models.Model):
    """Correos electrónicos del docente"""
    docente = models.ForeignKey(
        Docente, related_name='correos', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    es_principal = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Correo Electrónico"
        verbose_name_plural = "Correos Electrónicos"

    def __str__(self):
        return f"{self.email} {'(Principal)' if self.es_principal else ''}"

    def save(self, *args, **kwargs):
        """Si se marca como principal, desmarcar los otros del mismo docente"""
        if self.es_principal:
            Correo.objects.filter(docente=self.docente,
                                  es_principal=True).update(es_principal=False)
        super().save(*args, **kwargs)


class Asignatura(models.Model):
    """Asignaturas de las carreras"""
    NIVEL_CHOICES = [
        ('I', 'Nivel I'),
        ('II', 'Nivel II'),
        ('III', 'Nivel III'),
        ('IV', 'Nivel IV'),
        ('V', 'Nivel V'),
        ('VI', 'Nivel VI'),
    ]

    FORMA_DICTADO_CHOICES = [
        ('anual', 'Anual'),
        ('1c', '1er Cuatrimestre'),
        ('2c', '2do Cuatrimestre'),
    ]

    nombre = models.CharField(max_length=200)
    codigo = models.CharField(
        max_length=20, unique=True, null=True, blank=True)
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES)
    puntaje = models.PositiveIntegerField(help_text="Puntaje de la asignatura")
    horas_semanales = models.PositiveIntegerField()
    horas_totales = models.PositiveIntegerField()
    departamento = models.ForeignKey(
        'core.Departamento', on_delete=models.PROTECT)
    carrera = models.ForeignKey('core.Carrera', on_delete=models.PROTECT)
    es_obligatoria = models.BooleanField(default=True)
    forma_dictado = models.CharField(
        max_length=10, choices=FORMA_DICTADO_CHOICES)
    areas = models.ManyToManyField('core.Area', blank=True)
    bloques = models.ManyToManyField('core.Bloque', blank=True)

    class Meta:
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"
        ordering = ['carrera', 'nivel', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.carrera.nombre})"


class Resolucion(models.Model):
    """Resoluciones administrativas"""
    OBJETO_CHOICES = [
        ('alta', 'Alta'),
        ('baja', 'Baja'),
        ('licencia', 'Licencia'),
        ('prorroga', 'Prórroga'),
        ('cambio_dedicacion', 'Cambio de Dedicación'),
        ('otro', 'Otro'),
    ]

    ORIGEN_CHOICES = [
        ('decano', 'Decano'),
        ('rector', 'Rector'),
        ('consejo_academico', 'Consejo Académico'),
        ('consejo_superior', 'Consejo Superior'),
    ]

    numero = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    objeto = models.CharField(max_length=50, choices=OBJETO_CHOICES)
    origen = models.CharField(max_length=50, choices=ORIGEN_CHOICES)
    fecha_emision = models.DateField()
    archivo_digital = models.FileField(
        upload_to='resoluciones/', null=True, blank=True)
    detalle_funciones_sustantivas = models.TextField(
        null=True,
        blank=True,
        help_text="Requerido para cargos con menos de 4 horas semanales"
    )
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Resolución"
        verbose_name_plural = "Resoluciones"
        ordering = ['-anio', '-numero']
        unique_together = ['numero', 'anio', 'origen']

    def __str__(self):
        return f"Res. {self.numero}/{self.anio} ({self.get_origen_display()})"


class Cargo(models.Model):
    """Cargos docentes"""
    CARACTER_CHOICES = [
        ('ordinario', 'Ordinario'),
        ('regular', 'Regular'),
        ('interino', 'Interino'),
        ('extraordinario', 'Extraordinario'),
    ]

    CATEGORIA_CHOICES = [
        ('profesor_titular', 'Profesor Titular'),
        ('profesor_asociado', 'Profesor Asociado'),
        ('profesor_adjunto', 'Profesor Adjunto'),
        ('jefe_trabajos_practicos', 'Jefe de Trabajos Prácticos'),
        ('ayudante_diplomado', 'Ayudante Diplomado'),
        ('ayudante_estudiante', 'Ayudante Estudiante'),
    ]

    DEDICACION_CHOICES = [
        ('simple', 'Simple'),
        ('semiexclusiva', 'Semiexclusiva'),
        ('exclusiva', 'Exclusiva'),
    ]

    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('licencia', 'Licencia'),
        ('baja', 'Baja'),
    ]

    docente = models.ForeignKey(
        Docente, on_delete=models.CASCADE, related_name='cargos')
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    comision = models.CharField(
        max_length=20, default='1', help_text="Número de comisión")
    caracter = models.CharField(max_length=50, choices=CARACTER_CHOICES)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    dedicacion = models.CharField(max_length=50, choices=DEDICACION_CHOICES)
    cantidad_horas = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='activo')
    fecha_inicio = models.DateField()
    fecha_final = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField()
    resolucion_alta = models.ForeignKey(Resolucion, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.docente} - {self.get_categoria_display()} - {self.asignatura}"

    def clean(self):
        """Validaciones del cargo"""
        # Validar que solo exista un cargo activo por docente-asignatura-comisión
        if self.estado == 'activo':
            cargos_activos = Cargo.objects.filter(
                docente=self.docente,
                asignatura=self.asignatura,
                comision=self.comision,
                estado='activo'
            ).exclude(pk=self.pk)

            if cargos_activos.exists():
                raise ValidationError(
                    'Ya existe un cargo activo para este docente en esta asignatura y comisión.'
                )

        # Validar detalle de funciones sustantivas para cargos con pocas horas
        if self.asignatura.horas_semanales < 4:
            if not self.resolucion_alta.detalle_funciones_sustantivas:
                raise ValidationError(
                    'Se requiere detalle de funciones sustantivas en la resolución '
                    'para asignaturas con menos de 4 horas semanales.'
                )

    def save(self, *args, **kwargs):
        """Calcular fecha de vencimiento automáticamente"""
        if not self.fecha_vencimiento:
            if self.caracter == 'interino':
                # Interinos vencen el 31 de marzo del año siguiente
                anio_vencimiento = self.fecha_inicio.year + 1
                self.fecha_vencimiento = date(anio_vencimiento, 3, 31)
            elif self.caracter in ['regular', 'ordinario']:
                # Regulares/Ordinarios: 5 o 7 años según categoría
                anios = 7 if 'profesor' in self.categoria else 5
                self.fecha_vencimiento = self.fecha_inicio + \
                    relativedelta(years=anios)

        super().save(*args, **kwargs)
