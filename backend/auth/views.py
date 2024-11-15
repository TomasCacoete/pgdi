from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from pgdi_api.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken

def get_username_from_token(token):
    try:
        # Decode the token
        decoded_token = UntypedToken(token)

        # Access the username from the decoded token
        username = decoded_token['username']
        id = decoded_token['id']

        return decoded_token, username
    except Exception as e:
        # Handle any decoding errors
        print(f"Token decoding failed: {e}")
        return None, None
        

class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer