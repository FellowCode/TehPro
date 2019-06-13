from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('debug/', debug),
    path('materials/', show_materials)
]