from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('SocialBD Info', {'fields': ('bio', 'profile_picture', 'cover_photo', 'location', 'website', 'date_of_birth', 'is_verified')}),
    )
