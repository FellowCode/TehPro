# Generated by Django 2.2 on 2019-04-29 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Group', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('surname', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=16)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='OrderType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UsedMaterials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plug', models.IntegerField(default=0)),
                ('cable', models.IntegerField(default=0)),
                ('router', models.IntegerField(default=0)),
                ('tv_plug', models.IntegerField(default=0)),
                ('rosette', models.IntegerField(default=0)),
                ('connector', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_complete', models.BooleanField(default=False)),
                ('cable_number', models.CharField(max_length=32, unique=True)),
                ('appointed_time', models.DateTimeField()),
                ('time_start', models.DateTimeField(blank=True, null=True)),
                ('time_end', models.DateTimeField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=2048, null=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='Order.Client')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Group.Group')),
                ('materials', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='Order.UsedMaterials')),
                ('order_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Order.OrderType')),
                ('work_type', models.ManyToManyField(blank=True, null=True, to='Order.WorkType')),
                ('workers', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
