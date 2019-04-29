from .models import Group as WorkerGroup
from django.contrib import admin

@admin.register(WorkerGroup)
class WorkerGroupAdmin(admin.ModelAdmin):
    pass
