from django.urls import path
from . import views

urlpatterns = [
    path("wallets/", views.CreateWalletView.as_view(), name="create_wallet"),
    path("wallets/<uuid:wallet_id>/add-address/", views.AddAddressView.as_view(), name="add_address"),
    path("deposits/", views.InitiateDepositView.as_view(), name="initiate_deposit"),
    path("deposits/<uuid:deposit_id>/confirm/", views.ConfirmDepositView.as_view(), name="confirm_deposit"),
    path("wallets/<uuid:wallet_id>/edit-settings/", views.EditWalletSettingsView.as_view(), name="edit_wallet_settings"),
]

