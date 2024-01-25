from django.urls import path
from .views import register, activate_account

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<str:confirmation_code>/', activate_account, name='activate_account'),
]