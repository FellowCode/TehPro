from django.urls import path
from .views import *

urlpatterns = [
    path('create/', create_group),
    path('change/<id>/', change_group),
    path('list/', group_list),
    path('<id>/', worker_group),
    path('', worker_group),
]