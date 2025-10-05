from django import forms
from .models import CarreraAcademica, JuntaEvaluadora, Evaluacion, Formulario


class CarreraAcademicaForm(forms.ModelForm):
    """Formulario para carrera académica"""

    class Meta:
        model = CarreraAcademica
        fields = [
            'cargo', 'numero_expediente', 'fecha_inicio',
            'fecha_vencimiento_original', 'fecha_vencimiento_actual',
            'resolucion_designacion', 'resolucion_puesta_en_funcion',
            'observaciones'
        ]
        widgets = {
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'numero_expediente': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento_original': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento_actual': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'resolucion_designacion': forms.TextInput(attrs={'class': 'form-control'}),
            'resolucion_puesta_en_funcion': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class JuntaEvaluadoraForm(forms.ModelForm):
    """Formulario para junta evaluadora"""

    class Meta:
        model = JuntaEvaluadora
        fields = [
            'titular_frlp', 'titular_externo1', 'institucion_externo1',
            'titular_externo2', 'institucion_externo2', 'suplente_frlp',
            'suplente_externo', 'institucion_suplente_externo',
            'veedor_alumno', 'veedor_graduado', 'fecha_conformacion'
        ]
        widgets = {
            'titular_frlp': forms.Select(attrs={'class': 'form-select'}),
            'titular_externo1': forms.TextInput(attrs={'class': 'form-control'}),
            'institucion_externo1': forms.TextInput(attrs={'class': 'form-control'}),
            'titular_externo2': forms.TextInput(attrs={'class': 'form-control'}),
            'institucion_externo2': forms.TextInput(attrs={'class': 'form-control'}),
            'suplente_frlp': forms.Select(attrs={'class': 'form-select'}),
            'suplente_externo': forms.TextInput(attrs={'class': 'form-control'}),
            'institucion_suplente_externo': forms.TextInput(attrs={'class': 'form-control'}),
            'veedor_alumno': forms.TextInput(attrs={'class': 'form-control'}),
            'veedor_graduado': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_conformacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class EvaluacionForm(forms.ModelForm):
    """Formulario para evaluación"""

    class Meta:
        model = Evaluacion
        fields = [
            'numero_evaluacion', 'fecha_iniciada', 'anios_evaluados', 'observaciones'
        ]
        widgets = {
            'numero_evaluacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_iniciada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'anios_evaluados': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '[2022, 2023]'
            }),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FormularioUploadForm(forms.ModelForm):
    """Formulario para subir formularios"""

    class Meta:
        model = Formulario
        fields = ['tipo', 'anio_actividad', 'archivo', 'observaciones']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'anio_actividad': forms.NumberInput(attrs={'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
