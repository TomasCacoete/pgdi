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
        user_type = self.context['request'].data.get('user_type', 'user')
        
        # Create a base user
        user = User.objects.create_user(**validated_data)

        # Create specific type of user if needed
        if user_type == 'contestant':
            Contestant.objects.create(user=user)
        elif user_type == 'creator':
            Creator.objects.create(user=user)

        return user
