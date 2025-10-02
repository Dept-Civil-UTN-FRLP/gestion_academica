from django import template
from datetime import date, timedelta
from django.utils import timezone

register = template.Library()

# =========================
# FILTROS DE FECHAS
# =========================


@register.filter
def add_days(value, days):
    """Agrega días a una fecha"""
    if not value:
        return None
    try:
        return value + timedelta(days=int(days)) if isinstance(value, date) else value
    except (ValueError, TypeError):
        return value


@register.filter
def subtract_days(value, days):
    """Resta días a una fecha"""
    if not value:
        return None
    try:
        return value - timedelta(days=int(days)) if isinstance(value, date) else value
    except (ValueError, TypeError):
        return value


@register.filter
def days_until(value):
    """Días hasta una fecha"""
    if not value:
        return None
    try:
        today = timezone.now().date() if timezone.is_aware(
            timezone.now()) else date.today()
        return (value - today).days if isinstance(value, date) else None
    except (ValueError, TypeError):
        return None


@register.filter
def days_since(value):
    """Días desde una fecha"""
    if not value:
        return None
    try:
        today = timezone.now().date() if timezone.is_aware(
            timezone.now()) else date.today()
        return (today - value).days if isinstance(value, date) else None
    except (ValueError, TypeError):
        return None

# =========================
# FILTROS NUMÉRICOS / TEXTO
# =========================


@register.filter
def percentage(value, total):
    """Calcula el porcentaje"""
    try:
        return round((float(value)/float(total))*100, 2) if float(total) != 0 else 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def truncate_chars(value, length):
    """Trunca un string a cierta longitud"""
    if not value:
        return ''
    try:
        length = int(length)
        return value[:length] + '...' if len(value) > length else value
    except (ValueError, TypeError):
        return value


@register.filter
def multiply(value, arg):
    """Multiplica dos valores"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """Divide dos valores"""
    try:
        return float(value)/float(arg) if float(arg) != 0 else 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

# =========================
# FILTROS DE FORMATO
# =========================


@register.filter
def format_dni(value):
    """Formatea un DNI con puntos"""
    if not value:
        return ''
    try:
        s = str(value)
        parts = []
        while len(s) > 3:
            parts.insert(0, s[-3:])
            s = s[:-3]
        if s:
            parts.insert(0, s)
        return '.'.join(parts)
    except (ValueError, TypeError):
        return value


@register.filter
def format_phone(value):
    """Formatea un teléfono"""
    if not value:
        return ''
    try:
        s = str(value).replace(' ', '').replace('-', '')
        return f"({s[:3]}) {s[3:6]}-{s[6:]}" if len(s) == 10 else value
    except (ValueError, TypeError):
        return value


@register.filter
def get_item(dictionary, key):
    """Obtiene un item de un diccionario"""
    return dictionary.get(key) if dictionary else None


@register.filter
def badge_color(estado):
    """Clase CSS para badges según estado"""
    colors = {
        'activo': 'success', 'inactivo': 'secondary', 'pendiente': 'warning',
        'aprobado': 'success', 'rechazado': 'danger', 'en_proceso': 'info',
        'completado': 'success', 'cancelado': 'danger', 'licencia': 'warning', 'baja': 'danger'
    }
    return colors.get(estado.lower() if estado else '', 'secondary')


@register.filter
def status_icon(estado):
    """Icono Bootstrap según estado"""
    icons = {
        'activo': 'check-circle-fill', 'inactivo': 'x-circle', 'pendiente': 'clock',
        'aprobado': 'check-circle-fill', 'rechazado': 'x-circle-fill', 'en_proceso': 'hourglass-split',
        'completado': 'check-all', 'cancelado': 'x-circle'
    }
    return icons.get(estado.lower() if estado else '', 'circle')

# =========================
# SIMPLE TAGS
# =========================


@register.simple_tag
def query_transform(request, **kwargs):
    """Mantiene parámetros GET al cambiar página"""
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)
    return updated.urlencode()


@register.simple_tag
def get_verbose_name(instance, field_name):
    """Obtiene el verbose_name de un campo del modelo"""
    return instance._meta.get_field(field_name).verbose_name.title()


@register.simple_tag
def url_replace(request, field, value):
    """Reemplaza un parámetro en la URL manteniendo los demás"""
    d = request.GET.copy()
    d[field] = value
    return d.urlencode()

# =========================
# INCLUSION TAGS
# =========================


@register.inclusion_tag('components/pagination.html', takes_context=True)
def pagination(context, page_obj, adjacent_pages=2):
    """Genera paginación completa"""
    start_page = max(page_obj.number - adjacent_pages, 1)
    end_page = min(page_obj.number + adjacent_pages,
                   page_obj.paginator.num_pages)
    page_numbers = range(start_page, end_page + 1)
    return {
        'page_obj': page_obj,
        'page_numbers': page_numbers,
        'show_first': start_page > 1,
        'show_last': end_page < page_obj.paginator.num_pages,
        'request': context.get('request'),
    }


@register.filter
def principal_email(docente):
    correo = docente.correos.filter(es_principal=True).first()
    return correo.email if correo else None


@register.filter
def sum_attribute(queryset, attribute):
    """Suma el valor de un atributo para todos los objetos en una lista."""
    try:
        return sum(getattr(obj, attribute) for obj in queryset)
    except (AttributeError, TypeError):
        return 0


@register.filter
def count_where(queryset, condition):
    """
    Cuenta elementos en una lista que cumplen una o varias condiciones separadas por ','.
    Ej: {{ mi_lista|count_where:'caracter=ordinario,dedicacion=simple' }}
    También puedes usar operadores lógicos simples como suma: 'campo1=valor1+campo2=valor2'
    """
    try:
        conditions = [c.split('=') for c in condition.split(',')]
        count = 0
        for obj in queryset:
            match = True
            for attr, value in conditions:
                if str(getattr(obj, attr.strip(), None)) != value.strip():
                    match = False
                    break
            if match:
                count += 1
        return count
    except (ValueError, AttributeError):
        return 0
