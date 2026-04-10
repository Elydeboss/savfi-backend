from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    deposit_count = models.IntegerField(default=0)
    withdraw_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return timezone.now() < self.expires_at and not self.is_used

    def __str__(self):
        return f"OTP {self.code} for {self.user.username}"

    class Meta:
        ordering = ["-created_at"]
