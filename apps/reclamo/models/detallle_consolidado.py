from django.db import models

class DetalleConsolidado(models.Model):
    consolidado_id = models.IntegerField()
    venta_id = models.IntegerField()

    class Meta:
        db_table = 'detalle_consolidado'

    def __str__(self):
        return f"Consolidado {self.consolidado_id} - Venta {self.venta_id}"