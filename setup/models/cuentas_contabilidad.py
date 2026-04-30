from django.db import models


class ContabilidadCuenta(models.Model):
    descripcion_contabilidad = models.CharField(max_length=255)
    codigo_contabilidad = models.CharField(max_length=100)

    class Meta:
        db_table = 'setup_contabilidad_cuentas'
        verbose_name = 'Cuenta Contable'
        verbose_name_plural = 'Cuentas Contables'

    def __str__(self):
        return f"{self.codigo_contabilidad} - {self.descripcion_contabilidad}"