from django.contrib import admin
from django.urls import path, include
from .serializers import *
from .models import *
from .views import *

urlpatterns = [
    path('get_users/', GetUsers.as_view()),
    path('create_route/',CreateRoute.as_view()),
    path('user_routes/', UserRoutes.as_view()),
    path('create_competition/', CompetitionCreationView.as_view()),
    path('competitions/', GetCompetitions.as_view()),
    path('competition_signup/', CompetitionSignUpView.as_view()),
]