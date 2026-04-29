from django.db import models
from django.utils.translation import gettext_lazy as _


class ConsolidadoDiario(models.Model):
    establecimiento_id = models.IntegerField()
    fecha = models.DateField()
    total_importe = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad_ventas = models.IntegerField()
    estado = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    cuentacorriente_id = models.IntegerField(null=True, blank=True)
    codigo_deposito = models.CharField(max_length=20, null=True, blank=True)
    fecha_deposito = models.DateField(null=True, blank=True)
    constancia_deposito = models.FileField(
        _('Archivo de constancia de depósito'),
        upload_to='constancias_deposito/',   # carpeta dentro de MEDIA_ROOT
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'reclamo_consolidado_diario'
        unique_together = ('establecimiento_id', 'fecha')

    def __str__(self):
        return f"{self.establecimiento_id} - {self.fecha}"