from django.shortcuts import render
import secrets

# Create your views here.
# users/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.is_activated = False
        user.confirmation_token = generate_token()
        user.save()

        # Send confirmation email
        subject = 'Activate Your Account'
        message = f'Click on the following link to activate your account: {settings.BASE_URL}/users/activate/{user.confirmation_token}/'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return Response({'success': 'Registration successful. A confirmation email has been sent.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_token():
    token_length = 32
    token = secrets.token_hex(token_length)
    return token


@api_view(['GET'])
@permission_classes([AllowAny])
def activate_account(request, confirmation_token):
    user = get_object_or_404(CustomUser, confirmation_token=confirmation_token)
    user.is_activated = True
    token = Token.objects.create(user=user)
    user.confirmation_token = None
    user.save()
    
    return Response({'success': 'Account successfully activated.', 'token': token.key, 'user': user.username}, status=status.HTTP_200_OK)   



