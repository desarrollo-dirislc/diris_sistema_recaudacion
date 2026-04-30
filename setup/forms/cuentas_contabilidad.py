from django import forms
from setup.models.cuentas_contabilidad import ContabilidadCuenta


class ContabilidadCuentaForm(forms.ModelForm):

    class Meta:
        model = ContabilidadCuenta
        fields = [
            'descripcion_contabilidad',
            'codigo_contabilidad'
        ]
        widgets = {
            'descripcion_contabilidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese descripción contable'
            }),
            'codigo_contabilidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese código contable'
            }),
        }
        labels = {
            'descripcion_contabilidad': 'Descripción Contabilidad',
            'codigo_contabilidad': 'Código Contabilidad',
        }