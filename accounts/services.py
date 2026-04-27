"""
Service layer for accounts app.

This module contains business logic for user operations,
separating it from views and serializers.
"""

from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import OTP
from .utils import generate_otp

User = get_user_model()
DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


class OTPService:
    """
    Service class for OTP-related operations.
    Centralizes OTP generation, storage, validation, and email sending.
    """

    @staticmethod
    def generate_and_send(user):
        """
        Generate a new OTP for the user and send it via email.

        Args:
            user: User instance

        Returns:
            OTP: The created OTP instance
        """
        code = generate_otp()

        otp = OTP.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        # Send email
        OTPService._send_email(user.email, code)

        return otp

    @staticmethod
    def verify(user, code):
        """
        Verify OTP code for a user and activate the account.

        Args:
            user: User instance
            code: OTP code to verify

        Returns:
            tuple: (is_valid: bool, message: str)

        Raises:
            ValueError: If user or OTP is not found
        """
        otp = OTP.objects.filter(
            user=user,
            code=code,
            is_used=False
        ).order_by("-created_at").first()

        if not otp:
            return False, "Invalid OTP"

        if not otp.is_valid():
            return False, "OTP has expired"

        # Mark OTP as used
        otp.is_used = True
        otp.save()

        # Activate user account
        user.is_active = True
        user.save()

        return True, "OTP verified successfully. Account activated."

    @staticmethod
    def resend(username):
        """
        Resend OTP to a user.

        Args:
            username: Username of the user

        Returns:
            tuple: (success: bool, message: str, otp: OTP or None)

        Raises:
            ValueError: If user not found
        """
        user = User.objects.filter(username=username).first()

        if not user:
            return False, "User not found", None

        otp = OTPService.generate_and_send(user)

        return True, "OTP resent to email", otp

    @staticmethod
    def _send_email(email, code):
        """
        Internal method to send OTP email.

        Args:
            email: Email address
            code: OTP code
        """
        send_mail(
            subject="Your Verification OTP Code",
            message=f"Your OTP code is: {code}\nIt expires in 10 minutes.",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )


class UserService:
    """
    Service class for user-related operations.
    """

    @staticmethod
    def create_user(username, email, password):
        """
        Create a new user with OTP verification.

        Args:
            username: Username
            email: Email address
            password: Password

        Returns:
            User: Created user instance

        Raises:
            ValidationError: If validation fails
        """
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = False  # Require OTP verification
        user.save()

        return user
