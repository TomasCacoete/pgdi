from django.contrib import admin
from django.urls import path, include
from .serializers import *
from .models import *
from .views import *

urlpatterns = [
    path('get_users/', GetUsers.as_view()),
    path('create_route/',CreateRoute.as_view()),
]