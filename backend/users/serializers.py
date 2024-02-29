from rest_framework import serializers
from .models import CustomUser

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'firstname', 'lastname' 'email']
        
        
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)  # E-Mail-Feld hinzufügen und als erforderlich markieren

    class Meta:
        model = CustomUser
        fields = ['email',  'first_name', 'last_name']  #'password',

  