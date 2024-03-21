from django.shortcuts import redirect, render
import secrets

# Create your views here.
# users/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backend.settings import CLIENT_BASE_URL
from .models import CustomUser
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.username = request.data['username']
        user.confirmation_token = generate_token()
        user.save()

        # Render HTML template
        subject = 'Activate Your Account'
        context = {'user': user, 'activation_link': f'{settings.BASE_URL}/users/activate/{user.confirmation_token}/'}
        html_message = render_to_string('confirmation_email.html', context)
        plain_message = strip_tags(html_message)

        # Send confirmation email
        email = EmailMultiAlternatives(subject, plain_message, settings.EMAIL_HOST_USER, [user.email])
        email.attach_alternative(html_message, "text/html")
        try:
            email.send()
        except:
            usermail = user.email
            user.delete()
            return Response({'error' :f'Failed to send mail to: {usermail}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
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
    return redirect_to_success_site()
    


def redirect_to_success_site():
    success_frontend_url = CLIENT_BASE_URL + '/success'
    return redirect(success_frontend_url)




@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = get_object_or_404(CustomUser, email =request.data['email'])
    if user.is_activated:
        if not user.check_password(request.data['password']):
            return Response({"detail": "Not found."} , status=status.HTTP_400_NOT_FOUND)
    
        token, created = Token.objects.get_or_create(user=user)
        token_key = token.key
        
        serializer = UserSerializer(instance=user)
        return Response({"token": token_key, "user": serializer.data})
    else:
        return Response({"detail": "Your Account is not registered, or not activated yet"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    token_key = request.headers.get('Authorization').split()[1]

    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

    token.delete()

    return Response({"detail": "Logged out successfully."})


@api_view(['POST'])
def delete_user(request):
    # Extrahiere das Token aus dem Authorization-Header
    token_key = request.headers.get('Authorization').split()[1]

    try:
        # Versuche, das Token im Backend zu finden
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

    # Lösche das Token, um es ungültig zu machen
    token.delete()

    try:
        # Versuche, den Benutzer zu finden und zu löschen
        user = CustomUser.objects.get(id=token.user_id)
        user.delete()
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "User deleted successfully."})