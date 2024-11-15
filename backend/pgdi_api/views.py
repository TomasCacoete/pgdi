from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *

class CreateUser(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.user_type == 'contestant':
                Contestant.objects.create(user=user)
            elif user.user_type == 'creator':
                Creator.objects.create(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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