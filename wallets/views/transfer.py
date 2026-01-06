from decimal import Decimal
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from wallets.models.wallet import Wallet
from wallets.models.transaction import Transaction
from wallets.serializers import TransferSerializer

class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender_wallet = Wallet.objects.select_for_update().get(user=request.user)
        receiver_wallet = Wallet.objects.get(
            account_number = serializer.validated_data["receiver_account_number"]
        )
        amount = serializer.validated_data["amount"]

        if sender_wallet.id == receiver_wallet.id:
            return Response({"detail":"Cannot transfer to yourself"}, status=400)
        
        with transaction.atomic():
            if sender_wallet.balance < amount:
                return Response({"detail": "Insufficient balance"}, status = 400)
            
            sender_wallet.balance -= amount
            sender_wallet.save(update_fields=["balance"])
            Transaction.objects.create(
                wallet=sender_wallet,
                user=request.user,
                amount=amount,
                type=Transaction.type.TRANSFER_OUT,
                reference=f"transfer_to_{receiver_wallet.account_number}"
            )
            
            receiver_wallet.balance += amount
            receiver_wallet.save(update_fields=["balance"])
            Transaction.objects.create(
                wallet=receiver_wallet,
                user=receiver_wallet.user,
                amount=amount,
                type=Transaction.type.TRANSFER_IN,
                reference=f"transfer_from_{sender_wallet.account_number}"
            )

        return Response(
            {
                "message":"Transfer successful",
                "sender_balance": sender_wallet.balance,
                "reciever_account": receiver_wallet.account_number,
                "amount_transferred":amount,
            },
            status=status.HTTP_200_OK
        )