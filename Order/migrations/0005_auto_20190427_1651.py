# Generated by Django 2.2 on 2019-04-27 06:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0004_auto_20190427_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='workers',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
