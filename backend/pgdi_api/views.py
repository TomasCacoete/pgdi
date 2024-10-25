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
    
class GetUsers(APIView):
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)