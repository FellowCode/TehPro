from django.db import models

class Material(models.Model):
    plug = models.IntegerField(default=0)
    cable = models.IntegerField(default=0)
    rosette = models.IntegerField(default=0)
    connector = models.IntegerField(default=0)

    def __str__(self):
        return 'Материалы'

    class Meta:
        verbose_name_plural = 'Материалы'
        verbose_name = 'Материалы'
