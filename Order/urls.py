from django.urls import path
from .views import *

urlpatterns = [
    path('add/', staff_add),
    path('change/<id>/', staff_change),
    path('full/<id>/', order_full),
    path('list/', orders_list),
    path('worker/list/', worker_orders),
    path('fromworker/<id>/', worker_order),
]