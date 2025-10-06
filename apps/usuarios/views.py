from django.http import HttpResponse


def index(request):
    """
    Vista de ejemplo que muestra una página de 'en construcción'.

    Este es un placeholder para asegurar que el archivo no esté vacío y
    tenga una estructura válida.
    """
    return HttpResponse("<h1>Página en Construcción</h1>")


# Para que esta vista funcione en el navegador, necesitarás
# conectarla en un archivo urls.py de la aplicación.
