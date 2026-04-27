from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import OTP
from .serializers import RegisterSerializer, LoginSerializer
from .utils import generate_otp
from django.conf import settings
DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
User = get_user_model()


class RegisterThrottle(UserRateThrottle):
    rate = '3/minute'


class OTPThrottle(UserRateThrottle):
    rate = '5/minute'

def send_otp_email(email, code):
    send_mail(
        subject="Your Verification OTP Code",
        message=f"Your OTP code is: {code}\nIt expires in 10 minutes.",
        from_email = DEFAULT_FROM_EMAIL,  
        recipient_list=[email],
        fail_silently=False,
    )


def send_otp_to_console(email, code):
    # Later replace with email/SMS sending service
    print(f"Sending OTP to {email}: {code}")


# REGISTER
class RegisterView(APIView):
    throttle_classes = [RegisterThrottle]

    @extend_schema(request=RegisterSerializer, responses={201: RegisterSerializer})
    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()

        # Generate and send OTP
        code = generate_otp()
        OTP.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        send_otp_email(user.email, code)   # send email instead of print

        return Response(
            {"message": "Registration successful. OTP sent to your email for verification."},
            status=status.HTTP_201_CREATED
        )


# LOGIN
class LoginView(APIView):
    @extend_schema(request=LoginSerializer, responses={200: LoginSerializer})
    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        return Response(ser.validated_data, status=status.HTTP_200_OK)


# VERIFY OTP
class VerifyOTPView(APIView):
    throttle_classes = [OTPThrottle]

    @extend_schema(
        summary="Verify OTP",
        description="Confirm OTP sent to the user",
        request=None,
        responses={200: dict},
    )
    def post(self, request):
        code = request.data.get("code")
        username = request.data.get("username")

        if not code or not username:
            return Response({"detail": "code and username required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        otp = OTP.objects.filter(user=user, code=code, is_used=False).order_by("-created_at").first()

        if otp and otp.is_valid():
            otp.is_used = True
            otp.save()
            # Activate user account after successful OTP verification
            user.is_active = True
            user.save()
            return Response({"message": "OTP verified successfully. Account activated."}, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)


# RESEND OTP
class ResendOTPView(APIView):
    throttle_classes = [OTPThrottle]

    @extend_schema(summary="Resend OTP")
    def post(self, request):
        username = request.data.get("username")
        if not username:
            return Response({"detail": "username required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        code = generate_otp()
        OTP.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        send_otp_email(user.email, code)  # Updated to real email

        return Response({"message": "OTP resent to email"}, status=status.HTTP_200_OK)
