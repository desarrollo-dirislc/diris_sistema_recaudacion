import os
import sys
import json
from setup.models.clasificadores_ingreso import Clasificadores_ingreso
from setup.models.servicios import SetupServicios

from django.utils.decorators import method_decorator
from django.views.generic import DeleteView

from apps.util.valid_user_access_views import HttpResponseRedirect, valid_access_view, valid_medidas_adoptadas_add
from django.http import HttpResponseRedirect

if os.path.splitext(os.path.basename(sys.argv[0]))[0] == 'pydoc-script':
    pass

from django.contrib import messages
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Sum

from apps.reclamo.forms.medida_adoptada import MedidaAdoptadaForm
from apps.reclamo.models.entidad_reclamo import EntidadReclamo
from apps.reclamo.models.medida_adoptada import MedidaAdoptada
from django.shortcuts import get_object_or_404



class MedidaAdoptadaCreate(CreateView):
    model = MedidaAdoptada
    form_class = MedidaAdoptadaForm

    @method_decorator(valid_access_view(valid_medidas_adoptadas_add, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(MedidaAdoptadaCreate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MedidaAdoptadaCreate, self).get_form_kwargs(*args, **kwargs)
        entidad_reclamo = EntidadReclamo.objects.get(pk=self.kwargs['reclamo_id'])
        kwargs['entidad_reclamo'] = entidad_reclamo
        return kwargs

     
    def form_valid(self, form):
        self.object = form.save(commit=False)

        # Calcular importe
        self.object.importe = self.object.precio * self.object.cantidad

        # Guardar objeto
        self.object.save()

        # Guardar relaciones many-to-many si existen
        form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(MedidaAdoptadaCreate, self).get_context_data(**kwargs)
        entidad_reclamo = EntidadReclamo.objects.get(pk=self.kwargs['reclamo_id'])

        totales = entidad_reclamo.medidas_adoptadas.aggregate(
            total_importe=Sum('importe'),
            total_cantidad=Sum('cantidad')
        )

        # 🔥 SERVICIOS → JSON
        servicios = SetupServicios.objects.all()
        servicios_json = {
            s.id: {
                "precio": float(s.precio) if s.precio else 0
            }
            for s in servicios
        }

        context['title'] = "Agregar venta"
        context['entidad_reclamo'] = entidad_reclamo
        context['total_importe'] = totales['total_importe'] or 0
        context['total_cantidad'] = totales['total_cantidad'] or 0

        # 👇 IMPORTANTE
        context['servicios_json'] = json.dumps(servicios_json)

        return context

    def get_success_url(self):
        return reverse_lazy('reclamo:medida-adoptada-new', kwargs={'reclamo_id': self.kwargs['reclamo_id']})



class MedidaAdoptadaCreate_soporte(CreateView):
    model = MedidaAdoptada
    form_class = MedidaAdoptadaForm
    template_name = 'reclamo/medidaadoptada_form_soporte.html'

    @method_decorator(valid_access_view(valid_medidas_adoptadas_add, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(MedidaAdoptadaCreate_soporte, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MedidaAdoptadaCreate_soporte, self).get_form_kwargs(*args, **kwargs)
        # Pasamos la instancia de EntidadReclamo al form
        entidad_reclamo = EntidadReclamo.objects.get(pk=self.kwargs['reclamo_id'])
        kwargs['entidad_reclamo'] = entidad_reclamo
        return kwargs

    def get_initial(self):
        # Generar código correlativo con 2 dígitos
        codigo = str(
            MedidaAdoptada.objects.filter(entidad_reclamo_id=self.kwargs['reclamo_id']).count() + 1
        ).zfill(2)
        return {
            'codigo': codigo
        }

    def get_context_data(self, **kwargs):
        entidad_reclamo = EntidadReclamo.objects.get(pk=self.kwargs['reclamo_id'])
        title = "Agregar Medida Adoptada"
        return dict(
            super(MedidaAdoptadaCreate_soporte, self).get_context_data(**kwargs),
            title=title,
            entidad_reclamo=entidad_reclamo
        )

    def get_success_url(self):
        # 🔹 Aquí decides el flujo:
        # 1) Para volver a crear otra medida:
        # return reverse_lazy('reclamo:medida-adoptada-new', kwargs={'reclamo_id': self.kwargs['reclamo_id']})

        # 2) O para ir al listado de medidas:
        return reverse_lazy('reclamo:medida-adoptada-new', kwargs={'reclamo_id': self.kwargs['reclamo_id']})

    def form_valid(self, form):
        entidad_reclamo_id = self.kwargs['reclamo_id']
        usuario_soporte = form.cleaned_data.get("usuario_soporte")

        # Verificamos si ya existe esa combinación
        if MedidaAdoptada.objects.filter(
            entidad_reclamo_id=entidad_reclamo_id,
            usuario_soporte=usuario_soporte
        ).exists():
            messages.warning(
                self.request,
                "⚠️ Este usuario ya fue asignado para esta programación."
            )
            return self.form_invalid(form)

        msg = "Personal agregado correctamente"
        messages.success(self.request, msg)
        return super().form_valid(form)


 
class MedidaAdoptadaCreate2(CreateView):
    model = MedidaAdoptada
    form_class = MedidaAdoptadaForm
    template_name= 'reclamo/modal_medidas.html'

    @method_decorator(valid_access_view(valid_medidas_adoptadas_add, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(MedidaAdoptadaCreate2, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MedidaAdoptadaCreate2, self).get_form_kwargs(*args, **kwargs)
        entidad_reclamo = EntidadReclamo.objects.filter(pk=self.kwargs['reclamo_id']).values_list('id',
                                                                                                  'codigo_registro')[
                          0:1]
        kwargs['entidad_reclamo'] = entidad_reclamo
        return kwargs

    def get_initial(self):
        codigo = str(MedidaAdoptada.objects.filter(entidad_reclamo_id=self.kwargs['reclamo_id']).count() + 1).zfill(2)

        return {'entidad_reclamo': self.kwargs['reclamo_id'], 'codigo': codigo}

    def get_context_data(self, **kwargs):
        entidad_reclamo = EntidadReclamo.objects.get(pk=self.kwargs['reclamo_id'])

        title = "Agregar Medida Adoptada"

        return dict(
            super(MedidaAdoptadaCreate2, self).get_context_data(**kwargs), title=title, entidad_reclamo=entidad_reclamo)

    def get_success_url(self):
        return reverse_lazy('reclamo:medida-adoptada-new2', kwargs={'reclamo_id': self.kwargs['reclamo_id']})

    def form_valid(self, form):
        msg = "Medida agregada correctamente"
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)





class MedidaAdoptadaUpdate(UpdateView):
    model = MedidaAdoptada
    form_class = MedidaAdoptadaForm

    @method_decorator(valid_access_view(valid_medidas_adoptadas_add, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(MedidaAdoptadaUpdate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MedidaAdoptadaUpdate, self).get_form_kwargs(*args, **kwargs)
        entidad_reclamo = EntidadReclamo.objects.filter(pk=self.kwargs['reclamo_id']).values_list('id',
                                                                                                  'codigo_administrado')[
                          0:1]
        kwargs['entidad_reclamo'] = entidad_reclamo
        return kwargs

    def get_context_data(self, **kwargs):
        entidad_reclamo = EntidadReclamo.objects.get(pk=self.kwargs['reclamo_id'])
        title = "Editar Medida Adoptada"
        return dict(
            super(MedidaAdoptadaUpdate, self).get_context_data(**kwargs), title=title, entidad_reclamo=entidad_reclamo)

    def get_success_url(self):
        return reverse_lazy('reclamo:medida-adoptada-new', kwargs={'reclamo_id': self.kwargs['reclamo_id']})

    def form_valid(self, form):
        msg = "Medida actualizada correctamente"
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super().form_valid(form)


class MedidaAdoptadaDelete(DeleteView):
    model = MedidaAdoptada
    template_name = 'reclamo/medidaadoptada_confirm_delete.html'

    @method_decorator(valid_access_view(valid_medidas_adoptadas_add, login_url='/validate'))
    def dispatch(self, *args, **kwargs):
        return super(MedidaAdoptadaDelete, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('reclamo:medida-adoptada-new', kwargs={'reclamo_id': self.kwargs['reclamo_id']})

    def delete(self, request, *args, **kwargs):
        msg = "Medida adoptada eliminada correctamente"
        messages.add_message(self.request, messages.ERROR, msg, extra_tags='danger')
        return super(MedidaAdoptadaDelete, self).delete(request, *args, **kwargs)





class MedidaAdoptadaCreate_entidad(CreateView):
    model = MedidaAdoptada
    form_class = MedidaAdoptadaForm
    template_name = (
        'reclamo/medidaadoptada_form_entidad.html'
    )

    # 🔹 Pasar entidad_reclamo
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        entidad_reclamo = get_object_or_404(
            EntidadReclamo,
            pk=self.kwargs['reclamo_id']
        )

        kwargs[
            'entidad_reclamo'
        ] = entidad_reclamo

        return kwargs

    # 🔹 Guardado personalizado
    def form_valid(self, form):
        self.object = form.save(
            commit=False
        )

        # importe
        self.object.importe = (
            self.object.precio *
            self.object.cantidad
        )

        # relacion reclamo
        self.object.entidad_reclamo_id = (
            self.kwargs['reclamo_id']
        )

        # 🔥 SI FORM NO LO GUARDA, FORZAR
        data = form.cleaned_data.get(
            'clasificador_ingreso'
        )

        if data and '|' in data:

            clasificador_id, codigo = (
                data.split('|')
            )

            obj = Clasificadores_ingreso.objects.get(
                pk=int(clasificador_id)
            )

            self.object.cuentacorriente = int(
                obj.cuentacorriente
            )

        self.object.save()

        form.save_m2m()

        messages.success(
            self.request,
            "Venta registrada correctamente"
        )

        return HttpResponseRedirect(
            self.get_success_url()
        )

    # 🔹 Redirección
    def get_success_url(self):
        return reverse_lazy(
            'reclamo:medida-adoptada-new-entidad',
            kwargs={
                'reclamo_id':
                self.kwargs['reclamo_id']
            }
        )

    # 🔹 Contexto adicional
    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )

        entidad_reclamo = get_object_or_404(
            EntidadReclamo,
            pk=self.kwargs['reclamo_id']
        )

        # Totales
        totales = (
            entidad_reclamo
            .medidas_adoptadas
            .aggregate(
                total_importe=Sum(
                    'importe'
                ),
                total_cantidad=Sum(
                    'cantidad'
                ),
            )
        )

        # Servicios
        servicios = (
            SetupServicios.objects.all()
        )

        servicios_json = {
            s.id: {
                "precio": float(
                    s.precio
                ) if s.precio else 0
            }
            for s in servicios
        }

        context.update({
            'title': "Agregar venta",
            'entidad_reclamo':
                entidad_reclamo,
            'total_importe':
                totales[
                    'total_importe'
                ] or 0,
            'total_cantidad':
                totales[
                    'total_cantidad'
                ] or 0,
            'servicios_json':
                json.dumps(
                    servicios_json
                )
        })

        return context