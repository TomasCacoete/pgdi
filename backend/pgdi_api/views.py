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
        
        # Check if the user is a creator
        try:
            creator = User.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_403_FORBIDDEN)
        
        # Add creator to the request data
        request.data['creator'] = creator.id
        
        # Serialize the data
        serializer = CompetitionSerializer(data=request.data)
        
        if serializer.is_valid():
            competition = serializer.save()
            
            # Handle routes if provided
            routes = request.data.get('routes', [])
            if routes:
                competition.routes.set(routes)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
        
        # Check if the user is a contestant
        try:
            contestant = User.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_403_FORBIDDEN)
        
        competition_id = request.data.get('competition_id')
        if not competition_id:
            return Response({"error": "Please provide a competition_id."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            competition = Competition.objects.get(id=competition_id)
        except Competition.DoesNotExist:
            return Response({"error": "Competition not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a submission
        submission, created = Submission.objects.get_or_create(
            contestant=contestant,
            competition=competition,
            defaults={'score': 0}
        )
        
        if not created:
            return Response({"error": "You have already signed up for this competition."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Successfully signed up for the competition."}, status=status.HTTP_201_CREATED)