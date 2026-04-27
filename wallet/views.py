from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WalletAddressSerializer
from .models import WalletAddress
from drf_spectacular.utils import extend_schema

class AddWalletAddressView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=WalletAddressSerializer, responses={201: WalletAddressSerializer})
    def post(self, request):
        ser = WalletAddressSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(user=request.user)
        return Response(ser.data, status=status.HTTP_201_CREATED)
class ListWalletAddressesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: WalletAddressSerializer(many=True)})
    def get(self, request):
        addresses = WalletAddress.objects.select_related('user').filter(user=request.user)
        ser = WalletAddressSerializer(addresses, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    
