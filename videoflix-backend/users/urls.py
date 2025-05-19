from django.urls import include, path

from .views import register, activate_account, login, logout, delete_user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('delete/', delete_user, name='delete'),
    path('activate/<str:confirmation_token>/', activate_account, name='activate_account'),
    
]