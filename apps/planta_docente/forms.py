from django import forms
from .models import Docente, Asignatura, Cargo, Resolucion, Correo


class DocenteForm(forms.ModelForm):
    """Formulario para crear/editar docentes"""

    class Meta:
        model = Docente
        fields = ["apellido", "nombre", "documento", "legajo", "fecha_nacimiento", "cv"]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "documento": forms.TextInput(attrs={"class": "form-control"}),
            "legajo": forms.TextInput(attrs={"class": "form-control"}),
            "cv": forms.FileInput(attrs={"class": "form-control"}),
        }


class CorreoFormSet(forms.BaseInlineFormSet):
    """FormSet para gestionar múltiples correos"""

    def clean(self):
        super().clean()
        principales = sum(
            1 for form in self.forms if form.cleaned_data.get("es_principal")
        )
        if principales > 1:
            raise forms.ValidationError("Solo puede haber un correo principal.")


class AsignaturaForm(forms.ModelForm):
    """Formulario para asignaturas"""

    class Meta:
        model = Asignatura
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "codigo": forms.TextInput(attrs={"class": "form-control"}),
            "nivel": forms.Select(attrs={"class": "form-select"}),
            "forma_dictado": forms.Select(attrs={"class": "form-select"}),
            "puntaje": forms.NumberInput(attrs={"class": "form-control"}),
            "horas_semanales": forms.NumberInput(attrs={"class": "form-control"}),
            "horas_totales": forms.NumberInput(attrs={"class": "form-control"}),
            "departamento": forms.Select(attrs={"class": "form-select"}),
            "carrera": forms.Select(attrs={"class": "form-select"}),
            "areas": forms.SelectMultiple(attrs={"class": "form-select"}),
            "bloques": forms.SelectMultiple(attrs={"class": "form-select"}),
        }


class CargoForm(forms.ModelForm):
    """Formulario para cargos"""

    class Meta:
        model = Cargo
        fields = [
            "docente",
            "asignatura",
            "comision",
            "caracter",
            "categoria",
            "dedicacion",
            "cantidad_horas",
            "fecha_inicio",
            "resolucion_alta",
            "observaciones",
        ]
        widgets = {
            "fecha_inicio": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "docente": forms.Select(attrs={"class": "form-select"}),
            "asignatura": forms.Select(attrs={"class": "form-select"}),
            "comision": forms.TextInput(attrs={"class": "form-control"}),
            "caracter": forms.Select(attrs={"class": "form-select"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "dedicacion": forms.Select(attrs={"class": "form-select"}),
            "cantidad_horas": forms.NumberInput(attrs={"class": "form-control"}),
            "resolucion_alta": forms.Select(attrs={"class": "form-select"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class ResolucionForm(forms.ModelForm):
    """Formulario para resoluciones"""

    class Meta:
        model = Resolucion
        fields = "__all__"
        widgets = {
            "fecha_emision": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "anio": forms.NumberInput(attrs={"class": "form-control"}),
            "objeto": forms.Select(attrs={"class": "form-select"}),
            "origen": forms.Select(attrs={"class": "form-select"}),
            "archivo_digital": forms.FileInput(attrs={"class": "form-control"}),
            "detalle_funciones_sustantivas": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
