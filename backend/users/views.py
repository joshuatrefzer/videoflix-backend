from django.shortcuts import render

# Create your views here.
# users/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
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
        user.confirmation_token = 'generate-unique-code-here'
        user.save()

        # Send confirmation email
        subject = 'Activate Your Account'
        message = f'Click on the following link to activate your account: {settings.BASE_URL}/activate/{user.confirmation_token}/'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return Response({'success': 'Registration successful. A confirmation email has been sent.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def activate_account(request, confirmation_token):
    user = get_object_or_404(CustomUser, confirmation_token=confirmation_token)
    user.is_activated = True
    user.confirmation_code = None
    user.save()

    return Response({'success': 'Account successfully activated.'}, status=status.HTTP_200_OK)
