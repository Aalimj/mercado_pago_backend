from django.urls import path
from wallets.views.deposit import DepositView
from wallets.views.withdraw import WithdrawView
from wallets.views.transfer import TransferView
from wallets.views.transaction_history import TransactionHistoryView

urlpatterns = [
    path("deposit/", DepositView.as_view(), name="wallet-deposit"),
    path("withdraw/", WithdrawView.as_view(), name="wallet-withdraw" ),
    path("transfer/", TransferView.as_view(), name="wallet-transfer"),
    path("transactions/", TransactionHistoryView.as_view(), name="wallet-transactions"),
    
]
