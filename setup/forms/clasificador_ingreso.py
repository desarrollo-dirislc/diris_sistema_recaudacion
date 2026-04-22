from django import forms
from setup.models.clasificadores_ingreso import Clasificadores_ingreso

class ClasificadoresIngresoForm(forms.ModelForm):
    class Meta:
        model = Clasificadores_ingreso
        fields = ['codigo', 'descripcion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }