# Generated by Django 2.2 on 2019-05-01 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0005_auto_20190501_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Order.City'),
        ),
    ]
