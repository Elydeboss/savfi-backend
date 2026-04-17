from django.urls import path
from . import views

urlpatterns = [
    path("addresses/", views.AddWalletAddressView.as_view(), name="add_wallet_address"),
    path("addresses/list/", views.ListWalletAddressesView.as_view(), name="list_wallet_addresses"),
]
