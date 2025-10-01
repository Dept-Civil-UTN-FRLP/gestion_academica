# 🔧 Guía de Configuración de Variables de Entorno

Esta guía te ayudará a configurar correctamente las variables de entorno para el proyecto de Gestión Académica Universitaria.

---

## 📋 Tabla de Contenidos

- [Paso 1: Instalar python-decouple](#paso-1-instalar-python-decouple)
- [Paso 2: Crear archivo .env](#paso-2-crear-archivo-env)
- [Paso 3: Generar SECRET_KEY](#paso-3-generar-secret_key)
- [Paso 4: Configurar Base de Datos](#paso-4-configurar-base-de-datos-postgresql)
- [Paso 5: Configurar Email](#paso-5-configurar-email-gmail)
- [Paso 6: Verificar Configuración](#paso-6-verificar-configuración)
- [Paso 7: Variables para Producción](#paso-7-variables-para-producción)
- [Paso 8: AWS S3 (Opcional)](#paso-8-aws-s3-opcional)
- [Variables Críticas de Seguridad](#-variables-críticas-de-seguridad)
- [Troubleshooting](#-troubleshooting)

---

## Paso 1: Instalar python-decouple

Instala la librería que nos permite manejar variables de entorno de forma segura:

```bash
pip install python-decouple
```

---

## Paso 2: Crear archivo .env

1. Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

2. Abre el archivo `.env` y completa los valores necesarios

> **⚠️ Importante**: El archivo `.env` NO debe subirse a Git. Verifica que esté en tu `.gitignore`

---

## Paso 3: Generar SECRET_KEY

Ejecuta el script para generar una clave secreta segura:

```bash
python generate_secret_key.py
```

Copia la clave generada y pégala en tu archivo `.env`:

```env
SECRET_KEY=tu-clave-generada-aqui
```

---

## Paso 4: Configurar Base de Datos PostgreSQL

### 4.1 Crear la base de datos

```bash
createdb gestion_academica
```

### 4.2 Completar credenciales en `.env`

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=gestion_academica
DB_USER=postgres
DB_PASSWORD=tu_password_postgres
DB_HOST=localhost
DB_PORT=5432
```

### 4.3 Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Paso 5: Configurar Email (Gmail)

### 5.1 Activar verificación en dos pasos

1. Ve a tu cuenta de Google: [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Activa la **Verificación en dos pasos**

### 5.2 Generar contraseña de aplicación

1. Ve a: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Selecciona **Correo** y **Otro (nombre personalizado)**
3. Escribe "Django Gestión Académica"
4. Copia la contraseña generada (16 caracteres)

### 5.3 Configurar en `.env`

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=contraseña-de-16-caracteres-generada
DEFAULT_FROM_EMAIL=tu_email@gmail.com
```

> **💡 Tip**: Para desarrollo, puedes usar `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` para ver los emails en la consola

---

## Paso 6: Verificar Configuración

Ejecuta el comando personalizado para verificar que todo está correctamente configurado:

```bash
python manage.py check_config
```

Deberías ver algo como:

```
Verificando configuración...
==================================================
✓ SECRET_KEY: Configurado
✓ DEBUG: Configurado
✓ DATABASE: Configurado
✓ DB_PASSWORD: Configurado
✓ EMAIL_HOST_USER: Configurado
✓ ALLOWED_HOSTS: Configurado
==================================================

✓ Todas las variables están configuradas correctamente
```

---

## Paso 7: Variables para Producción

Cuando despliegues a producción, asegúrate de configurar:

### En tu archivo `.env` de producción

```env
# Seguridad
DEBUG=False
SECRET_KEY=clave-unica-y-diferente-a-desarrollo
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# HTTPS/SSL
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Base de datos (credenciales de producción)
DB_PASSWORD=contraseña-muy-segura-de-produccion
```

### Checklist de producción

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` única y segura
- [ ] `ALLOWED_HOSTS` con tu dominio
- [ ] Certificado SSL instalado
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] Contraseñas de base de datos seguras
- [ ] Backups configurados

---

## Paso 8: AWS S3 (Opcional)

Si deseas usar Amazon S3 para almacenar archivos estáticos y media:

### 8.1 Crear bucket en AWS S3

1. Accede a [AWS Console](https://console.aws.amazon.com/)
2. Ve a S3 y crea un nuevo bucket
3. Configura permisos públicos para archivos estáticos

### 8.2 Crear usuario IAM

1. Ve a IAM → Usuarios → Crear usuario
2. Asigna permisos de S3 (AmazonS3FullAccess o política personalizada)
3. Genera credenciales de acceso (Access Key ID y Secret Access Key)

### 8.3 Completar variables en `.env`

```env
USE_S3=True
AWS_ACCESS_KEY_ID=tu_access_key_id
AWS_SECRET_ACCESS_KEY=tu_secret_access_key
AWS_STORAGE_BUCKET_NAME=nombre-de-tu-bucket
AWS_S3_REGION_NAME=us-east-1
```

### 8.4 Instalar dependencias adicionales

```bash
pip install boto3 django-storages
```

### 8.5 Recolectar archivos estáticos

```bash
python manage.py collectstatic
```

---

## 🔐 Variables Críticas de Seguridad

### ❌ NUNCA hagas esto

| ❌ | Acción Prohibida |
|---|---|
| ❌ | Subir archivo `.env` a Git |
| ❌ | Usar `DEBUG=True` en producción |
| ❌ | Usar `SECRET_KEY` por defecto o compartida |
| ❌ | Hardcodear contraseñas en el código |
| ❌ | Compartir credenciales por email/chat |

### ✅ SIEMPRE haz esto

| ✅ | Buena Práctica |
|---|---|
| ✅ | Usar contraseñas seguras y únicas |
| ✅ | Configurar `ALLOWED_HOSTS` en producción |
| ✅ | Usar HTTPS en producción |
| ✅ | Rotar SECRET_KEY periódicamente |
| ✅ | Usar variables de entorno para secretos |
| ✅ | Mantener `.env.example` actualizado |

---

## 🔧 Troubleshooting

### Problema: "SECRET_KEY not found"

**Solución:**

```bash
# Verifica que existe el archivo .env en la raíz del proyecto
ls -la .env

# Si no existe, crea uno desde el ejemplo
cp .env.example .env
```

---

### Problema: "No module named 'decouple'"

**Solución:**

```bash
pip install python-decouple
```

---

### Problema: Error de conexión a base de datos

**Causas comunes:**

1. **PostgreSQL no está corriendo**

   ```bash
   # Linux/Mac
   sudo service postgresql status
   sudo service postgresql start
   
   # Mac con Homebrew
   brew services start postgresql
   
   # Windows
   # Buscar "Services" y verificar PostgreSQL
   ```

2. **Credenciales incorrectas en `.env`**

   ```bash
   # Verificar credenciales
   psql -U postgres -d gestion_academica
   ```

3. **Base de datos no existe**

   ```bash
   createdb gestion_academica
   ```

---

### Problema: Email no se envía

**Soluciones:**

1. **Verificar que usas contraseña de aplicación (no tu contraseña normal)**
   - Genera una nueva en: <https://myaccount.google.com/apppasswords>

2. **Verificar variables en `.env`**

   ```env
   EMAIL_HOST_USER=tu_email@gmail.com
   EMAIL_HOST_PASSWORD=contraseña-de-16-caracteres
   ```

3. **Para testing, usar consola**

   ```env
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   ```

4. **Verificar que Gmail permite aplicaciones menos seguras**
   - Asegúrate de tener verificación en dos pasos activa
   - Usa contraseña de aplicación, no contraseña normal

---

### Problema: "This field cannot be blank" en admin

**Solución:**

```bash
# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario si no existe
python manage.py createsuperuser
```

---

### Problema: Archivos media no se guardan

**Solución:**

1. **Verificar que existe la carpeta media**

   ```bash
   mkdir -p media/cvs media/resoluciones media/ps/planes media/ps/informes
   ```

2. **Verificar permisos**

   ```bash
   # Linux/Mac
   chmod -R 755 media/
   ```

3. **Verificar configuración en settings.py**

   ```python
   MEDIA_URL = 'media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```

---

## 📚 Recursos Adicionales

- [Documentación Django sobre configuración](https://docs.djangoproject.com/en/5.0/topics/settings/)
- [Documentación python-decouple](https://pypi.org/project/python-decouple/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 📞 Soporte

Si encuentras algún problema no listado aquí:

1. Verifica los logs de Django: `logs/django.log`
2. Ejecuta: `python manage.py check --deploy`
3. Revisa la consola para errores específicos

---

## 📄 Estructura de Archivos de Configuración

```
proyecto/
├── .env                    # ❌ NO subir a Git (tus valores reales)
├── .env.example            # ✅ Template para otros desarrolladores
├── .gitignore              # ✅ Incluye .env
├── config/
│   └── settings.py         # Usa variables de .env
├── generate_secret_key.py  # Script para generar SECRET_KEY
└── requirements.txt        # Incluye python-decouple
```

---

**¡Listo!** Ahora tu proyecto está configurado de forma segura con variables de entorno. 🎉
