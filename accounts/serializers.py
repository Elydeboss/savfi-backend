from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
import random

from .models import OTP
from .utils import generate_otp

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        user.is_active = False  # requires verification
        user.save()

        code = generate_otp()
        OTP.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timezone.timedelta(minutes=10)
        )

        print("OTP for verification:", code)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            if not user.is_active:
                raise serializers.ValidationError("Account not verified. Please verify with OTP.")

            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        raise serializers.ValidationError("Invalid credentials")

    
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError("User not found")

        otp = OTP.objects.filter(user=user, code=data["code"], is_used=False).last()
        if not otp or not otp.is_valid():
            raise serializers.ValidationError("Invalid or expired OTP")

        otp.is_used = True
        otp.save()

        user.is_active = True
        user.save()

        return {"message": "Account verified successfully"}

    
