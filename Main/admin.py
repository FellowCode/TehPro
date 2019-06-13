from django.contrib import admin

from Main.models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass
