from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = (  'first_name',  'last_name', 'email', 'id', 'is_staff', 'is_active', 'is_activated')

    # Add any additional fields you want to be editable in the admin
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_activated', 'confirmation_token')}),
    )

# Register your custom user model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)