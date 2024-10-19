from django.contrib import admin
from django.urls import path, include
from .serializers import *
from .models import *
from .views import *

urlpatterns = [
    path('user/', CreateUser.as_view()),
]