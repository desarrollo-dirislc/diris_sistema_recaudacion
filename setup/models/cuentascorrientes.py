from django.db import models

class CuentaCorriente(models.Model):
    numero_cuenta = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'setup_cuentascorrientes'
        verbose_name = 'Cuenta Corriente'
        verbose_name_plural = 'Cuentas Corrientes'

    def __str__(self):
        return f"{self.numero_cuenta} - {self.descripcion}"