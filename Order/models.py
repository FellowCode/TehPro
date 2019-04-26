from django.db import models
from Account.models import Group
from Account.models import ExtUser

class Order(models.Model):

    is_complete = models.BooleanField(default=False)

    workers = models.ManyToManyField(ExtUser)

    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True)

    cable_number = models.CharField(max_length=32)

    appointed_time = models.DateTimeField()

    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)

    remark = models.TextField(null=True, blank=True)

    client = models.OneToOneField('Client', on_delete=models.PROTECT)

    order_type = models.ForeignKey('OrderType', models.PROTECT)

    work_type = models.ManyToManyField('WorkType')

    materials = models.OneToOneField('UsedMaterials', models.PROTECT)


class Client(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)

    phone = models.CharField(max_length=16)

    email = models.EmailField(null=True, blank=True)

    address = models.CharField(max_length=2048)


class OrderType(models.Model):
    name = models.CharField(max_length=256, unique=True)

    price = models.IntegerField()

class WorkType(models.Model):
    name = models.CharField(max_length=256, unique=True)

class UsedMaterials(models.Model):
    plug = models.IntegerField(default=0)
    cable = models.IntegerField(default=0)
    router = models.IntegerField(default=0)
    tv_plug = models.IntegerField(default=0)
    rosette = models.IntegerField(default=0)
    connector = models.IntegerField(default=0)

