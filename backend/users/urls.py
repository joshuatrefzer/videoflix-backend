from django.urls import path
from .views import register, activate_account, login

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('activate/<str:confirmation_token>/', activate_account, name='activate_account'),
]