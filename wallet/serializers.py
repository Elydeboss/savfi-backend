from rest_framework import serializers
from .models import WalletAddress

class WalletAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAddress
        fields = ["id", "address", "created_at"]
