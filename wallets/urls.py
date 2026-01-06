from django.urls import path
from wallets.views.deposit import DepositView
from wallets.views.withdraw import WithdrawView
from wallets.views.transfer import TransferView

urlpatterns = [
    path("deposit/", DepositView.as_view(), name="wallet-deposit"),
    path("withdraw/", WithdrawView.as_view(), name="wallet-withdraw" ),
    path("transfer/", TransferView.as_view(), name="wallet-transfer"),
]
