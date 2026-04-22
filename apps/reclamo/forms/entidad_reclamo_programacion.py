from django import forms
from apps.reclamo.models.programacion import Programacion
from setup.models.establecimientos import Establecimientos
from django_select2.forms import Select2Widget


class EntidadReclamoForm_programacion(forms.ModelForm):

    # 🔥 AHORA DESDE BD (Establecimientos)
    dependencia_service = forms.ModelChoiceField(
        queryset=Establecimientos.objects.all().order_by('descripcion'),
        label="Dependencia",
        widget=Select2Widget(attrs={
            "style": "width: 100%;",
            "id": "id_dependencia_service"
        }),
        empty_label="Seleccione una dependencia",
        required=False
    )

    class Meta:
        model = Programacion
        fields = [
            'dependencia_service',
            'entidad_id',
            'cantidad_personal',
            'evidencia',
            'documento',
            'comentario_atencion',
            'fecha_atencion',
            'estado_programacion',
        ]

        widgets = {
            'entidad_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_personal': forms.NumberInput(attrs={'class': 'form-control'}),
            'detalle_programacion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
            'evidencia': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'comentario_atencion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control'
            }),
            'fecha_programada': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'fecha_atencion': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'estado_programacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'detalle_programacion': 'Detalle de las actividades a realizar',
            'fecha_programada': 'Fecha y hora programada',
            'descripcion_general': 'Descripción General de las actividades a realizar'
        }

    # ==============================
    # GUARDAR DESDE ESTABLECIMIENTOS
    # ==============================
    def save(self, commit=True):
        instance = super().save(commit=False)

        establecimiento = self.cleaned_data.get("dependencia_service")

        if establecimiento:
            # Guardar ID
            instance.dependencia_service = establecimiento.id

            # Guardar descripción
            if hasattr(instance, 'dependencia_service_nombre'):
                instance.dependencia_service_nombre = establecimiento.descripcion

        if commit:
            instance.save()

        return instance