from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aggregate_id = models.UUIDField(db_index=True)
    aggregate_type = models.CharField(max_length=100, db_index=True)
    version = models.PositiveIntegerField()
    type = models.CharField(max_length=100)
    data = models.JSONField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        unique_together = ("aggregate_id", "version")
        ordering = ("created_at", "version")

class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    response = models.JSONField(null=True, blank=True)

class WalletProjection(models.Model):
    wallet_id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    balance = models.DecimalField(max_digits=36, decimal_places=18, default=0)
    addresses = models.JSONField(default=list)
    status = models.CharField(max_length=50, default="active")
    last_event_version = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(default=timezone.now)

class DepositProjection(models.Model):
    deposit_id = models.UUIDField(primary_key=True)
    wallet_id = models.UUIDField(db_index=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)
    currency = models.CharField(max_length=20, default="USD")
    status = models.CharField(max_length=50, default="initiated")
    tx_hash = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    last_event_version = models.PositiveIntegerField(default=0)

class WithdrawalProjection(models.Model):
    withdrawal_id = models.UUIDField(primary_key=True)
    wallet_id = models.UUIDField(db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=36, decimal_places=18)
    currency = models.CharField(max_length=20, default="USD")
    status = models.CharField(max_length=50, default="initiated")
    tx_hash = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    last_event_version = models.PositiveIntegerField(default=0)
