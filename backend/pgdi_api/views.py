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
    
 
#@permission_classes[IsAuthenticated]
class CreateRoute(APIView):
    
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
        
        # Get the GPX file from the request
        gpx_file = request.FILES.get('gpx_file')
        
        if not gpx_file:
            return Response({"error": "No GPX file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Call the RouteSerializer with the data
        route_serializer = RouteSerializer(data={'creator': user.id, 'file': gpx_file})
        
        # Check if the serializer is valid
        if route_serializer.is_valid():
            # Save the validated data to create a Route
            route_serializer.save()
            return Response(route_serializer.data, status=status.HTTP_201_CREATED)
        
        # If the serializer is not valid, return the errors
        return Response(route_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
