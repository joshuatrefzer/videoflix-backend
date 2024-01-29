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
        email.send()

        return Response({'success': 'Registration successful. A confirmation email has been sent.'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         user.set_password(request.data['password'])
#         user.is_activated = False
#         user.confirmation_token = generate_token()
#         user.save()

#         # Send confirmation email
#         subject = 'Activate Your Account'
#         message = f'Click on the following link to activate your account: {settings.BASE_URL}/users/activate/{user.confirmation_token}/'
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

#         return Response({'success': 'Registration successful. A confirmation email has been sent.'}, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    
    #Redirect to Login Page 
    return Response({'success': 'Account successfully activated.', 'token': token.key, 'user': user.username}, status=status.HTTP_200_OK)   



@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, username =request.data['username'])
    if user.is_activated:
        if not user.check_password(request.data['password']):
            return Response({"detail": "Not found."} , status=status.HTTP_400_NOT_FOUND)
    
        token, created = Token.objects.get_or_create(user=user)
        token_key = token.key
        
        serializer = UserSerializer(instance=user)
        return Response({"token": token_key, "user": serializer.data})
    else:
        return Response({"Your Account is not registred, or not activated yet"})

