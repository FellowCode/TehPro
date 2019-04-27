from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

def get_full_name(self):
    title = self.first_name + ' ' + self.last_name
    if len(title) < 2:
        title = self.username
    return title

User.add_to_class("__str__", get_full_name)

class ExtUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_worker = models.BooleanField(default=False)

    surname = models.CharField(max_length=256, default='')
    phone = models.CharField(max_length=16, default='')

    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'ExtUser'
        verbose_name_plural = 'ExtUsers'

    def __str__(self):
        title = self.user.first_name + ' ' + self.user.last_name
        if len(title) < 2:
            title = self.user.username
        return title


class Group(models.Model):
    name = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)

    plug = models.IntegerField(default=0)
    cable = models.IntegerField(default=0)
    rosette = models.IntegerField(default=0)
    connector = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ExtUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.extuser.save()
