from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import ExtUser


admin.site.unregister(Group)

@admin.register(ExtUser)
class ExtUserAdmin(admin.ModelAdmin):
    readonly_fields = ['user']



