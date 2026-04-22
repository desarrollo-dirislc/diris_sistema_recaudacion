from django.db import models

class SetupServicios(models.Model):
    descripcion_servicio = models.CharField(max_length=255)
    precio = models.FloatField()

    class Meta:
        db_table = 'setup_servicios'

    def __str__(self):
        return self.descripcion_servicio