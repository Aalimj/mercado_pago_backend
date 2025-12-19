from django.urls import path
from wallets.views.deposit import DepositView
from wallets.views.withdraw import WithdrawView

urlpatterns = [
    path("deposit/", DepositView.as_view(), name="wallet-deposit"),
    path("withdraw/", WithdrawView.as_view(), name="wallet-withdraw" )
]