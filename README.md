# Sistema de Gestión Académica

Sistema Django para gestión de planta docente, carreras académicas, equivalencias y prácticas supervisadas.

## Stack Tecnológico

- **Django 5.0**
- **Python 3.x**
- **PostgreSQL** (recomendado)
- **python-decouple** para variables de entorno

## Estructura del Proyecto

```
apps/
├── core/                    # Modelos base y utilidades
├── planta_docente/          # Gestión de docentes y cargos
├── carrera_academica/       # Carreras académicas docentes
├── equivalencias/           # Equivalencias de asignaturas
├── practica_supervisada/    # Prácticas supervisadas
└── usuarios/                # Perfiles y permisos
```

## Modelos Principales

### Core
- **Departamento**: Departamentos académicos
- **Carrera**: Carreras universitarias
- **Área/Bloque**: Clasificaciones académicas

### Planta Docente
- **Docente**: Información personal y contacto
- **Cargo**: Asignaciones docentes (dedicación, categoría)
- **Asignatura**: Materias del plan de estudios

### Carrera Académica
- **CarreraAcademica**: Expedientes de CA
- **Evaluacion**: Evaluaciones periódicas (cada 2 años)
- **Formulario**: F01-F13, CV, encuestas
- **JuntaEvaluadora**: Jurados de evaluación

### Equivalencias
- **Estudiante**: Datos de estudiantes
- **SolicitudEquivalencia**: Trámites de equivalencia
- **DetalleSolicitud**: Estados por asignatura
- **DocumentoAdjunto**: Archivos adjuntos

### Práctica Supervisada
- **PSolicitud**: Solicitudes de PS
- **JuradoPS**: Evaluadores (internos/externos)
- **EtiquetaPS**: Clasificación de PS

## Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd <proyecto>

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env con tus credenciales

# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py crear_superadmin

# Verificar configuración
python manage.py check_config

# Ejecutar servidor
python manage.py runserver
```

## Configuración (.env)

```env
SECRET_KEY=tu-secret-key-segura
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=nombre_db
DB_USER=usuario_db
DB_PASSWORD=password_db
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password
```

## Sistema de Permisos

### UserProfile
- **es_superadmin**: Acceso total
- **departamentos**: M2M con departamentos asignados

### Mixins Disponibles
- `DepartamentoAccessMixin`: Filtra por departamento
- `SuperadminRequiredMixin`: Solo superadmin

## Managers Personalizados

```python
# Filtrar por departamento del usuario
queryset = Modelo.objects.for_user(request.user)
```

## Template Tags Útiles

### Fechas
```django
{{ fecha|days_until }}
{{ fecha|days_since }}
{{ fecha|add_days:30 }}
```

### Formato
```django
{{ docente|principal_email }}
{{ estado|badge_color }}
{{ dni|format_dni }}
```

### Conteo
```django
{{ cargos|count_where:'caracter=ordinario' }}
{{ cargos|sum_attribute:'horas_semanales' }}
```

## APIs y Endpoints

### Carrera Académica
```
/carrera-academica/
├── carreras/                    # CRUD carreras
├── carreras/<pk>/nueva-evaluacion/
├── evaluaciones/<pk>/
└── reportes/vencimientos/
```

### Equivalencias
```
/equivalencias/
├── estudiantes/                 # CRUD estudiantes
├── solicitudes/                 # CRUD solicitudes
└── solicitudes/<pk>/completar/
```

### Práctica Supervisada
```
/practica-supervisada/
├── solicitudes/                 # CRUD solicitudes
├── solicitudes/<pk>/dictaminar-plan/
└── solicitudes/<pk>/dictaminar-informe/
```

## Comandos Útiles

```bash
# Crear superadmin con perfil
python manage.py crear_superadmin

# Verificar configuración
python manage.py check_config

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Shell interactivo
python manage.py shell
```

## Flujos Principales

### 1. Carrera Académica
1. Crear CarreraAcademica vinculada a Cargo
2. Conformar JuntaEvaluadora
3. Crear Evaluacion cada 2 años
4. Cargar Formularios (F01-F13, CV, ENC)
5. Junta dictamina (calificación)
6. Prórroga si es necesario

### 2. Equivalencias
1. Crear/buscar Estudiante
2. Crear SolicitudEquivalencia
3. Agregar DetalleSolicitud por asignatura
4. Docente responsable dictamina
5. Cargar DocumentoAdjunto
6. Completar solicitud con acta firmada

### 3. Práctica Supervisada
1. Crear PSolicitud con estudiante y tutor
2. Asignar JuradoPS (internos/externos)
3. Cargar plan_trabajo
4. Jurados dictaminan plan
5. Cargar informe_final
6. Jurados dictaminan informe
7. Auto-completar cuando todos aprueban

## Notificaciones

El sistema envía emails automáticos:
- PS: Notificación a jurados (plan/informe)

Configurar SMTP en `.env` para activar.

## Desarrollo

### Crear nueva app
```bash
python manage.py startapp apps/nueva_app
```

### Agregar a INSTALLED_APPS
```python
INSTALLED_APPS = [
    # ...
    'apps.nueva_app',
]
```

### Usar mixins de permisos
```python
from apps.core.mixins import DepartamentoAccessMixin

class MiVista(DepartamentoAccessMixin, ListView):
    departamento_field = 'departamento'
```

## Testing

```bash
python manage.py test
python manage.py test apps.carrera_academica
```

## Contribuir

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar funcionalidad'`)
4. Push a rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
