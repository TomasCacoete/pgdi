from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from pgdi_api.models import *
from pgdi_api.serializers import *
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
import jwt

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['id'] = user.id
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        
        return token
    
class RegisterSerializer(serializers.ModelSerializer): #igual ao UserSerializer
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        
        # Create a base user
        user=User.objects.create_user(**validated_data)

        return user