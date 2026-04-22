from django import forms
from setup.models.servicios import SetupServicios


class SetupServiciosForm(forms.ModelForm):
    class Meta:
        model = SetupServicios
        fields = ['descripcion_servicio', 'precio']
        widgets = {
            'descripcion_servicio': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'descripcion_servicio': 'Descripción del Servicio',
            'precio': 'Precio',
        }