# Generated by Django 2.2 on 2019-06-13 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plug', models.IntegerField(default=0)),
                ('cable', models.IntegerField(default=0)),
                ('rosette', models.IntegerField(default=0)),
                ('connector', models.IntegerField(default=0)),
            ],
        ),
    ]