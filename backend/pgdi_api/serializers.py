from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
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

    
class RouteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Route
        fields = '__all__'

        
class CompetitionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Competition
        fields = '__all__'
        
class SubmissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Submission
        fields = '__all__'
        
class UserCompetitionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User_Competition
        fields = '__all__'