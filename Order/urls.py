from django.urls import path
from .views import *

urlpatterns = [
    path('add/', staff_add),
    path('change/<id>/', staff_change),
    path('my/', user_orders),
]