from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from decimal import Decimal
import uuid

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)

from .serializers import (
    CreateWalletSerializer,
    InitiateDepositSerializer,
    WalletProjectionSerializer,
    DepositProjectionSerializer,
    EditWalletSettingsSerializer,
)
from .events import append_event
from .projections import apply_event_to_projections
from .models import WalletProjection, DepositProjection


class CreateWalletView(APIView):
    @extend_schema(
        request=CreateWalletSerializer,
        responses={201: WalletProjectionSerializer},
        summary="Create a new wallet",
        description="Creates a wallet and returns the wallet projection with zero balance and empty addresses.",
        examples=[
            OpenApiExample(
                "Create Wallet Example",
                value={
                    "owner": "John Doe",
                    "addresses": ["0x123abcd...", "bc1qxyz..."],
                    "idempotency_key": "unique-key-123"
                }
            )
        ],
    )
    def post(self, request):
        ser = CreateWalletSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        p = ser.validated_data

        wallet_id = p.get("wallet_id") or uuid.uuid4()
        idemp = p.get("idempotency_key")

        ev = append_event(
            aggregate_id=wallet_id,
            aggregate_type="wallet",
            event_type="WalletCreated",
            data={"owner": p["owner"], "addresses": p.get("addresses", [])},
            expected_version=0,
            idempotency_key=idemp,
        )
        apply_event_to_projections(ev)

        proj = WalletProjection.objects.get(wallet_id=wallet_id)
        return Response(WalletProjectionSerializer(proj).data, status=status.HTTP_201_CREATED)


class AddAddressView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("wallet_id", str, OpenApiParameter.PATH, description="ID of the wallet"),
        ],
        request=None,
        responses={200: WalletProjectionSerializer},
        summary="Add new wallet address",
        description="Add a blockchain address to an existing wallet."
    )
    def post(self, request, wallet_id):
        address = request.data.get("address")
        if not address:
            return Response({"detail": "address required"}, status=status.HTTP_400_BAD_REQUEST)

        ev = append_event(
            aggregate_id=wallet_id,
            aggregate_type="wallet",
            event_type="AddressAdded",
            data={"address": address}
        )
        apply_event_to_projections(ev)

        proj = get_object_or_404(WalletProjection, wallet_id=wallet_id)
        return Response(WalletProjectionSerializer(proj).data)


class InitiateDepositView(APIView):
    @extend_schema(
        request=InitiateDepositSerializer,
        responses={201: DepositProjectionSerializer},
        summary="Initiate Deposit",
        description="Begin a deposit request before confirmation (off-chain or on-chain verification)."
    )
    def post(self, request):
        ser = InitiateDepositSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        p = ser.validated_data

        deposit_id = p.get("deposit_id") or uuid.uuid4()
        idemp = p.get("idempotency_key")

        ev = append_event(
            aggregate_id=deposit_id,
            aggregate_type="deposit",
            event_type="DepositInitiated",
            data={"wallet_id": str(p["wallet_id"]), "amount": str(p["amount"]), "currency": p.get("currency", "USD")},
            idempotency_key=idemp,
        )
        apply_event_to_projections(ev)

        dp = DepositProjection.objects.get(deposit_id=deposit_id)
        return Response(DepositProjectionSerializer(dp).data, status=status.HTTP_201_CREATED)


class ConfirmDepositView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("deposit_id", str, OpenApiParameter.PATH, description="Deposit ID to confirm")
        ],
        request=None,
        responses={200: DepositProjectionSerializer},
        summary="Confirm Deposit",
        description="Confirms a pending deposit and updates the wallet balance."
    )
    def post(self, request, deposit_id):
        tx_hash = request.data.get("tx_hash")
        amount = request.data.get("amount")

        if not tx_hash:
            return Response({"detail": "tx_hash required"}, status=status.HTTP_400_BAD_REQUEST)

        ev = append_event(
            aggregate_id=deposit_id,
            aggregate_type="deposit",
            event_type="DepositConfirmed",
            data={"tx_hash": tx_hash, "amount": amount},
        )
        apply_event_to_projections(ev)

        dp = DepositProjection.objects.get(deposit_id=deposit_id)
        wallet_id = dp.wallet_id

        # Update wallet balance
        w_ev = append_event(
            aggregate_id=wallet_id,
            aggregate_type="wallet",
            event_type="DepositConfirmed",
            data={"amount": str(amount)},
        )
        apply_event_to_projections(w_ev)

        return Response(DepositProjectionSerializer(dp).data)

class EditWalletSettingsView(APIView):
    @extend_schema(
        request=EditWalletSettingsSerializer,
        responses={200: WalletProjectionSerializer},
        summary="Edit wallet settings",
        description="Allows editing wallet configuration such as address replacement."
    )
    def put(self, request, wallet_id):
        ser = EditWalletSettingsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        p = ser.validated_data

        ev = append_event(
            aggregate_id=wallet_id,
            aggregate_type="wallet",
            event_type="WalletSettingsUpdated",
            data={"addresses": p["addresses"]},
            idempotency_key=p.get("idempotency_key"),
        )
        apply_event_to_projections(ev)

        proj = get_object_or_404(WalletProjection, wallet_id=wallet_id)
        return Response(WalletProjectionSerializer(proj).data)
