from django.db import models
from django.utils.translation import gettext_lazy as _

class Clasificadores_ingreso(models.Model):
    id = models.AutoField(primary_key=True)  # campo entero autoincremental
    codigo = models.CharField(_('Código clasificador'),max_length=300)  # campo entero autoincremental

    descripcion = models.CharField(_('Descripción '),max_length=300)
    cuentacorriente = models.IntegerField(_('Cuenta corriente'), null=True, blank=True)   
    estado = models.IntegerField(_('estado'), null=True, blank=True)    
 

    class Meta:
        db_table = 'setup_clasificadores_ingreso'  # nombre de la tabla en la BD
        verbose_name = 'Clasificadores_ingreso'
        verbose_name_plural = 'Clasificadores_ingreso'

    def __str__(self):
        return self.descripcion