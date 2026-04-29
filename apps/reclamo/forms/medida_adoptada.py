from django import forms
from apps.reclamo.models.medida_adoptada import MedidaAdoptada
from apps.util.generic_filters import forms as gf
from setup.models.clasificadores_ingreso import Clasificadores_ingreso
from setup.models.servicios import SetupServicios

 

class MedidaAdoptadaForm(forms.ModelForm):

    cantidad = forms.IntegerField(
        initial=1,
        widget=forms.HiddenInput()
    )

    # ==========================
    # CLASIFICADOR
    # ==========================
    clasificador_ingreso = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            "class": "form-control select2",
            "id": "id_descripcion",
            "style": "width:100%;"
        }),
        label="Clasificador"
    )

    # ==========================
    # SERVICIO
    # ==========================
    servicio = forms.ModelChoiceField(
        queryset=SetupServicios.objects.all().order_by(
            'descripcion_servicio'
        ),
        required=False,
        widget=forms.Select(attrs={
            "class": "form-control select2",
            "id": "id_servicio",
            "style": "width:100%;"
        }),
        label="Servicio",
        empty_label="Seleccione un servicio"
    )

    class Meta:
        model = MedidaAdoptada
        fields = [
            'precio',
            'cantidad'
        ]

    def __init__(self, *args, **kwargs):
        self.entidad_reclamo = kwargs.pop(
            'entidad_reclamo',
            None
        )

        super().__init__(*args, **kwargs)

        if self.entidad_reclamo:
            self.instance.entidad_reclamo = (
                self.entidad_reclamo
            )

        # ==========================
        # CHOICES CLASIFICADOR
        # ==========================
        choices = [
            ('', 'Seleccione una descripción')
        ]

        for c in Clasificadores_ingreso.objects.all():
            choices.append(
                (
                    f"{c.id}|{c.codigo}",
                    c.descripcion
                )
            )

        self.fields[
            'clasificador_ingreso'
        ].choices = choices

        self.order_fields([
            'clasificador_ingreso',
            'servicio',
            'precio',
            'cantidad'
        ])

    def save(self, commit=True):
        instance = super().save(commit=False)

        # ==========================
        # CLASIFICADOR
        # ==========================
        data = self.cleaned_data.get(
            'clasificador_ingreso'
        )

        if data and '|' in data:

            clasificador_id, codigo = (
                data.split('|')
            )

            obj = Clasificadores_ingreso.objects.get(
                pk=int(clasificador_id)
            )

            # guardar datos
            instance.codigo = obj.id
            instance.descripcion = (
                obj.descripcion
            )

            # 🔥 GUARDAR CUENTA CORRIENTE
            instance.cuentacorriente = int(
                obj.cuentacorriente
            )

        # ==========================
        # SERVICIO
        # ==========================
        servicio = self.cleaned_data.get(
            'servicio'
        )

        if servicio:
            instance.servicio = servicio.id
            instance.servicio_descripcion = (
                servicio.descripcion_servicio
            )

        if commit:
            instance.save()

        return instance


class MedidaAdoptadaListFilter(gf.FilteredForm):

    def get_order_by_choices(self):
        return []