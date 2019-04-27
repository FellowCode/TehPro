from django.urls import path
from .views import *

urlpatterns = [
    path('add/', add),
    path('my/', user_orders),
]