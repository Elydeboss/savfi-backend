from django.contrib import admin
from .models import Event, WalletProjection, DepositProjection, WithdrawalProjection, IdempotencyKey

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id","aggregate_type","aggregate_id","version","type","created_at")
    readonly_fields = ("id","aggregate_type","aggregate_id","version","type","data","metadata","created_at")

@admin.register(WalletProjection)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("wallet_id","user","owner","balance","status","last_event_version")

@admin.register(DepositProjection)
class DepositAdmin(admin.ModelAdmin):
    list_display = ("deposit_id","wallet_id","amount","status","tx_hash")

@admin.register(WithdrawalProjection)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("withdrawal_id","wallet_id","user","amount","status","tx_hash")

@admin.register(IdempotencyKey)
class IdempAdmin(admin.ModelAdmin):
    list_display = ("key","created_at")
