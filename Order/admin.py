from django.contrib import admin
from .models import *

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderType)
class OrderTypesAdmin(admin.ModelAdmin):
    pass

@admin.register(WorkType)
class WorkTypesAdmin(admin.ModelAdmin):
    pass

@admin.register(UsedMaterials)
class UsedMaterialsAdmin(admin.ModelAdmin):
    pass