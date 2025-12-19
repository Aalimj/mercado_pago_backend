from decimal import Decimal

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from wallets.models.wallet import Wallet
from wallets.models.transaction import Transaction
from wallets.serializers import WithdrawSerializer

class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        with transaction.atomic():
            wallet = (
                Wallet.objects
                .select_for_update()
                .get(user=request.user)
            )

            if wallet.balance < amount:
                return Response(
                    {"detail": "Insufficient balance"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            wallet.balance -= amount
            wallet.save(update_fields=["balance"])

            Transaction.objects.create(
                wallet=wallet,
                user=request.user,
                amount=amount,
                type=Transaction.Type.WITHDRAW,
                reference="manual_withdraw"
            )

        return Response(
            {
                "message": "Withdraw successful",
                "wallet": {
                    "account_number": wallet.account_number,
                    "balance": wallet.balance,
                }
            },
            status=status.HTTP_200_OK
        )
