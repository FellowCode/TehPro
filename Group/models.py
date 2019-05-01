from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)

    plug = models.IntegerField(default=0)
    cable = models.IntegerField(default=0)
    rosette = models.IntegerField(default=0)
    connector = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Отряды'
        verbose_name = 'Отряд'

    def __str__(self):
        return str(self.name)
