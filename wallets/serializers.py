from rest_framework import serializers
from wallets.models import Wallet
from decimal import Decimal

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "account_number",
            "balance",
            "is_active",
        )

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01")
    )

class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01")
    )