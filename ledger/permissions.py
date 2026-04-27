from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from django.shortcuts import get_object_or_404
from .models import WalletProjection


class IsWalletOwner(permissions.BasePermission):
    """
    Permission class to check if the user owns the wallet.
    """

    def has_object_permission(self, request, view, obj):
        # obj is the WalletProjection instance
        return obj.user == request.user


def require_wallet_owner(view_func):
    """
    Decorator to verify wallet ownership.
    Usage: @require_wallet_owner in views that access wallet_id from request data
    """
    @wraps(view_func)
    def wrapped_view(view, request, *args, **kwargs):
        # Get wallet_id from request data or kwargs
        wallet_id = request.data.get('wallet_id') or kwargs.get('wallet_id')

        if not wallet_id:
            return Response(
                {"detail": "wallet_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        wallet = get_object_or_404(
            WalletProjection.objects.select_related('user'),
            wallet_id=wallet_id
        )

        if wallet.user != request.user:
            return Response(
                {"detail": "You do not have permission to access this wallet"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Attach wallet to request for use in view
        request.wallet = wallet
        return view_func(view, request, *args, **kwargs)

    return wrapped_view


def require_withdrawal_owner(view_func):
    """
    Decorator to verify withdrawal ownership.
    Usage: @require_withdrawal_owner in views that access withdrawal_id
    """
    @wraps(view_func)
    def wrapped_view(view, request, *args, **kwargs):
        withdrawal_id = kwargs.get('withdrawal_id')

        if not withdrawal_id:
            return Response(
                {"detail": "withdrawal_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        from .models import WithdrawalProjection
        withdrawal = get_object_or_404(WithdrawalProjection, withdrawal_id=withdrawal_id)
        wallet = get_object_or_404(
            WalletProjection.objects.select_related('user'),
            wallet_id=withdrawal.wallet_id
        )

        if wallet.user != request.user:
            return Response(
                {"detail": "You do not have permission to access this withdrawal"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Attach withdrawal and wallet to request
        request.withdrawal = withdrawal
        request.wallet = wallet
        return view_func(view, request, *args, **kwargs)

    return wrapped_view
