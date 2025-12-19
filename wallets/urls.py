from django.urls import path
from wallets.views.deposit import DepositView

urlpatterns = [
    path("deposit/", DepositView.as_view(), name="wallet-deposit"),
]