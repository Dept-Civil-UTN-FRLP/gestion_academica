from django import forms
from .models import PSolicitud, JuradoPS


class PSolicitudForm(forms.ModelForm):
    """Formulario para solicitudes de práctica supervisada"""

    class Meta:
        model = PSolicitud
        fields = [
            "estudiante",
            "tema",
            "descripcion",
            "tutor",
            "supervisor",
            "empresa_institucion",
            "plan_trabajo",
            "etiquetas",
        ]
        widgets = {
            "estudiante": forms.Select(attrs={"class": "form-select"}),
            "tema": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "tutor": forms.Select(attrs={"class": "form-select"}),
            "supervisor": forms.TextInput(attrs={"class": "form-control"}),
            "empresa_institucion": forms.TextInput(attrs={"class": "form-control"}),
            "plan_trabajo": forms.FileInput(attrs={"class": "form-control"}),
            "etiquetas": forms.SelectMultiple(attrs={"class": "form-select"}),
        }


class JuradoPSForm(forms.ModelForm):
    """Formulario para jurados"""

    class Meta:
        model = JuradoPS
        fields = ["docente", "nombre_externo", "institucion_externa"]
        widgets = {
            "docente": forms.Select(attrs={"class": "form-select"}),
            "nombre_externo": forms.TextInput(attrs={"class": "form-control"}),
            "institucion_externa": forms.TextInput(attrs={"class": "form-control"}),
        }


class DictamenPlanForm(forms.ModelForm):
    """Formulario para dictaminar plan de trabajo"""

    class Meta:
        model = JuradoPS
        fields = ["estado_dictamen_plan", "observaciones_plan"]
        widgets = {
            "estado_dictamen_plan": forms.Select(attrs={"class": "form-select"}),
            "observaciones_plan": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }


class DictamenInformeForm(forms.ModelForm):
    """Formulario para dictaminar informe final"""

    class Meta:
        model = JuradoPS
        fields = ["estado_dictamen_informe", "observaciones_informe"]
        widgets = {
            "estado_dictamen_informe": forms.Select(attrs={"class": "form-select"}),
            "observaciones_informe": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }
