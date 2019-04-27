from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import ExtUser
from .models import Group as WorkerGroup

admin.site.unregister(Group)

@admin.register(ExtUser)
class ExtUserAdmin(admin.ModelAdmin):
    pass

@admin.register(WorkerGroup)
class WorkerGroupAdmin(admin.ModelAdmin):
    pass

