from .models import WalletProjection, DepositProjection
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

def apply_event_to_projections(event):
    etype = event.type
    data = event.data
    agg_id = event.aggregate_id
    version = event.version

    if event.aggregate_type == "wallet":
        _apply_wallet_event(agg_id, etype, data, version)
    elif event.aggregate_type == "deposit":
        _apply_deposit_event(agg_id, etype, data, version)

def _apply_wallet_event(wallet_id, etype, data, version):
    with transaction.atomic():
        wp, _ = WalletProjection.objects.select_for_update().get_or_create(wallet_id=wallet_id)
        if version <= wp.last_event_version:
            return
        if etype == "WalletCreated":
            wp.owner = data.get("owner")
            wp.addresses = data.get("addresses", [])
            wp.status = "active"
        elif etype == "AddressAdded":
            addresses = wp.addresses or []
            addr = data.get("address")
            if addr and addr not in addresses:
                addresses.append(addr)
                wp.addresses = addresses
        elif etype == "AddressRemoved":
            addresses = wp.addresses or []
            addr = data.get("address")
            if addr and addr in addresses:
                addresses.remove(addr)
                wp.addresses = addresses
        elif etype == "WalletSettingsUpdated":
            # <-- New event handling
            wp.addresses = data.get("addresses", wp.addresses)
        elif etype == "DepositConfirmed":
            amt = Decimal(str(data.get("amount", "0")))
            wp.balance = (Decimal(str(wp.balance)) if wp.balance is not None else Decimal("0")) + amt
        elif etype == "WalletDisabled":
            wp.status = "disabled"
        wp.last_event_version = version
        wp.updated_at = timezone.now()
        wp.save()

def _apply_deposit_event(deposit_id, etype, data, version):
    with transaction.atomic():
        dp, _ = DepositProjection.objects.select_for_update().get_or_create(deposit_id=deposit_id)
        if version <= dp.last_event_version:
            return
        if etype == "DepositInitiated":
            dp.wallet_id = data.get("wallet_id")
            dp.amount = data.get("amount")
            dp.currency = data.get("currency", "USD")
            dp.status = "initiated"
            dp.created_at = timezone.now()
        elif etype == "DepositConfirmed":
            dp.status = "confirmed"
            dp.tx_hash = data.get("tx_hash")
            dp.updated_at = timezone.now()
        elif etype == "DepositFailed":
            dp.status = "failed"
            dp.updated_at = timezone.now()
        dp.last_event_version = version
        dp.save()
