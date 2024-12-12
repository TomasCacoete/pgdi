from django.contrib import admin
from django.urls import path, include
from .serializers import *
from .models import *
from .views import *

urlpatterns = [
    path('user/', UserInformation.as_view()),
    path('get_users/', GetUsers.as_view()),
    path('create_route/',CreateRoute.as_view()),
    path('user_routes/', UserRoutes.as_view()),
    path('create_competition/', CompetitionCreationView.as_view()),
    path('competitions/', GetCompetitions.as_view()),
    path('competition_signup/', CompetitionSignUpView.as_view()),
    path('user_competitions/', userCompetitions.as_view()),
    path('upload_submission/', uploadSubmission.as_view()),
    path('get_competition_scores/', getScoresCompetition.as_view()),
]