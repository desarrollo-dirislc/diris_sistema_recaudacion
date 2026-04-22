from django.db import models

class Establecimientos(models.Model):
    id = models.AutoField(primary_key=True)  # campo entero autoincremental
    descripcion = models.CharField(max_length=300)  # campo entero autoincremental
    estado = models.PositiveIntegerField("Estado", default=1)  # campo estado


    

    class Meta:
        db_table = 'setup_establecimientos'  # nombre de la tabla en la BD
        verbose_name = 'Establecimientos'
        verbose_name_plural = 'Establecimientos'

    def __str__(self):
        return self.descripcion