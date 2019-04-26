from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', registration),
    path('auth/', auth),
    path('logout/', user_logout),
]