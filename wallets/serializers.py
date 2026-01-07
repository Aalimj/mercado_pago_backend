from rest_framework import serializers
from wallets.models import Wallet
from decimal import Decimal
from rest_framework import serializers
from wallets.models.transaction import Transaction

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

class TransferSerializer(serializers.Serializer):
    receiver_account_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, min_value=Decimal("0.01")
    )

    def validate_receiver_account_number(self, value):
        try:
            reciever_wallet = Wallet.objects.get(account_number=value)
        except Wallet.DoesNotExist:
            raise serializers.ValidationError("Receiver wallet not found.")
        return value
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "type",
            "reference",
            "created_at",
            "wallet_id"
        ]
    