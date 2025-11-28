from rest_framework import serializers
from .models import WalletProjection, DepositProjection
import uuid

class CreateWalletSerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField(required=False, default=uuid.uuid4)
    owner = serializers.CharField(max_length=255)
    addresses = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    idempotency_key = serializers.CharField(required=False, allow_blank=True)

class InitiateDepositSerializer(serializers.Serializer):
    deposit_id = serializers.UUIDField(required=False, default=uuid.uuid4)
    wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=36, decimal_places=18)
    currency = serializers.CharField(max_length=20, default="USD")
    idempotency_key = serializers.CharField(required=False, allow_blank=True)

class WalletProjectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletProjection
        fields = "__all__"

class DepositProjectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProjection
        fields = "__all__"
        
class EditWalletSettingsSerializer(serializers.Serializer):
    addresses = serializers.ListField(
        child=serializers.CharField(),
        required=True
    )
    idempotency_key = serializers.CharField(required=False, allow_blank=True)
