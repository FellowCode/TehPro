# Generated by Django 2.2 on 2019-05-01 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extuser',
            options={'verbose_name': 'Расш. пользователь', 'verbose_name_plural': 'Расш. пользователи'},
        ),
    ]
