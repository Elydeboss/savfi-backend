from django.contrib import admin
from django.contrib.auth.models import User
from .models import OTP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'date_joined']
    search_fields = ['username', 'email']


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'created_at', 'expires_at', 'is_used']
    search_fields = ['user__username', 'user__email']
