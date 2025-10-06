from django import forms
from .models import (
    Estudiante,
    SolicitudEquivalencia,
    DetalleSolicitud,
    DocumentoAdjunto,
)


class EstudianteForm(forms.ModelForm):
    """Formulario para estudiantes"""

    class Meta:
        model = Estudiante
        fields = [
            "nombre_completo",
            "dni_pasaporte",
            "email_estudiante",
            "telefono",
            "carrera",
        ]
        widgets = {
            "nombre_completo": forms.TextInput(attrs={"class": "form-control"}),
            "dni_pasaporte": forms.TextInput(attrs={"class": "form-control"}),
            "email_estudiante": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "carrera": forms.Select(attrs={"class": "form-select"}),
        }


class SolicitudEquivalenciaForm(forms.ModelForm):
    """Formulario para solicitudes de equivalencia"""

    class Meta:
        model = SolicitudEquivalencia
        fields = ["estudiante", "observaciones"]
        widgets = {
            "estudiante": forms.Select(attrs={"class": "form-select"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class DetalleSolicitudForm(forms.ModelForm):
    """Formulario para detalle de solicitud"""

    class Meta:
        model = DetalleSolicitud
        fields = [
            "asignatura",
            "estado_asignatura",
            "detalle_pc",
            "observaciones_docente",
        ]
        widgets = {
            "asignatura": forms.Select(attrs={"class": "form-select"}),
            "estado_asignatura": forms.Select(attrs={"class": "form-select"}),
            "detalle_pc": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "observaciones_docente": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
        }


class DocumentoAdjuntoForm(forms.ModelForm):
    """Formulario para documentos adjuntos"""

    class Meta:
        model = DocumentoAdjunto
        fields = ["archivo", "nombre_archivo", "descripcion"]
        widgets = {
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
            "nombre_archivo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
        }
