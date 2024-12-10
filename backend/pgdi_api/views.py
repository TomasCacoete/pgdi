from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
import jwt
from django.conf import settings
from auth.views import *
from django.utils import timezone


@permission_classes([IsAuthenticated])
class GetUsers(APIView):
    
    def get(self, request):
        auth_header = request.headers.get("Authorization")
        access_token = auth_header.split(" ")[1]
        #print(access_token)
        #user=jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        #print(user)
        user = get_user_from_token(access_token)
        print(user)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class UserInformation(APIView):
    
    def get(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            access_token = auth_header.split(" ")[1]
            user = get_user_from_token(access_token)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class CreateRoute(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            access_token = auth_header.split(" ")[1]
            user = get_user_from_token(access_token)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the GPX file
        gpx_file = request.FILES.get('file')  # Match 'file' with FormData key

        if not gpx_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize data
        route_serializer = RouteSerializer(data={'creator': user.id, 'file': gpx_file})

        if route_serializer.is_valid():
            route_serializer.save()
            return Response(route_serializer.data, status=status.HTTP_201_CREATED)
        
        print(route_serializer.errors)
        return Response(route_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class UserRoutes(APIView):
    
    def get(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            access_token = auth_header.split(" ")[1]
            user = get_user_from_token(access_token)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        routes = Route.objects.filter(creator=user)
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class CompetitionCreationView(APIView):
    def post(self, request):
        # Extract token from the Authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            # Decode and get the user from the token
            access_token = auth_header.split(" ")[1]
            user = get_user_from_token(access_token)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Add creator to the request data
        request.data['creator'] = user.id
        
        # Serialize the data
        serializer = CompetitionSerializer(data=request.data)
        
        if serializer.is_valid():
            competition = serializer.save()
            
            # Handle routes: validate and associate
            route_ids = request.data.get('routes', [])
            if route_ids:
                # Validate the route IDs by ensuring they belong to the user
                user_routes = Route.objects.filter(creator=user, id__in=route_ids)
                if user_routes.count() != len(route_ids):
                    return Response(
                        {"error": "One or more routes are invalid or do not belong to the user"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                competition.routes.set(user_routes)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class GetCompetitions(APIView):
    
    def get(self, request):
        competitions = Competition.objects.all()
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class CompetitionSignUpView(APIView):
    def post(self, request):
        # Extract token from the Authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            # Decode and get the user from the token
            access_token = auth_header.split(" ")[1]
            user = get_user_from_token(access_token)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        competition_id = request.data.get('competition_id')
        if not competition_id:
            return Response({"error": "Please provide a competition_id."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            competition = Competition.objects.get(id=competition_id)
        except Competition.DoesNotExist:
            return Response({"error": "Competition not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already signed up for the competition
        user_competition, created = User_Competition.objects.get_or_create(
            user=user, competition=competition
        )
        
        if not created:
            return Response({"error": "You have already signed up for this competition."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Successfully signed up for the competition."}, status=status.HTTP_201_CREATED)
    
class userCompetitions(APIView):
    #get all the competitions info the user is signed up to
    def get(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            access_token = auth_header.split(" ")[1]
            user = get_user_from_token(access_token)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        #get competitions id user is signed up , then get the info aboput them
        user_competitions = User_Competition.objects.filter(user=user)
        competitions = []
        for user_competition in user_competitions:
            competition = Competition.objects.get(id=user_competition.competition.id)
            competitions.append(competition)
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data)
    
        
class uploadSubmission(APIView):
    
    def post(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            access_token = auth_header.split(" ")[1]
            user = get_user_from_token(access_token)
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Get the GPX file
        gpx_file = request.FILES.get('file')
        
        competition_id = request.data.get('competition_id')
        
        if not gpx_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not competition_id:
            return Response({"error": "Please provide a competition_id."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            competition = Competition.objects.get(id=competition_id)
        except Competition.DoesNotExist:
            return Response({"error": "Competition not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Validar datas da competição
        if competition.start_date > timezone.now():
            return Response({"error": "Competition has not started yet."}, status=status.HTTP_400_BAD_REQUEST)
        if competition.end_date < timezone.now():
            return Response({"error": "Competition has already ended."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user has signed up for the competition
        try:
            user_competition = User_Competition.objects.get(user=user, competition=competition)
        except User_Competition.DoesNotExist:
            return Response({"error": "You have not signed up for this competition."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Serialize data
        submission_serializer = SubmissionSerializer(data={'file': gpx_file, 'contestant': user.id, 'competition': competition_id})
        
        if submission_serializer.is_valid():
            submission_serializer.save()
            return Response(submission_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(submission_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
