from django.shortcuts import render

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from wallets.models.wallet import Wallet
from wallets.models.transaction import Transaction
from wallets.serializers import DepositSerializer
from decimal import Decimal

class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        wallet, _ = Wallet.objects.select_for_update().get_or_create(
            user=request.user,
            defaults={"balance": Decimal("0.00"), "is_active": True},
        )

        if not wallet.is_active:
            return Response(
                {"detail": "Wallet is inactive"},
                status=status.HTTP_403_FORBIDDEN
            )


        wallet.balance += amount
        wallet.save(update_fields=["balance"])

        Transaction.objects.create(
            wallet=wallet,
            user=request.user,
            amount=amount,
            type=Transaction.Type.DEPOSIT,
            reference="manual_deposit"
        )

        return Response(
            {
                "message": "Deposit successful",
                "wallet":{
                    "account_number": wallet.account_number,
                    "balance": wallet.balance,
                }
            },
            status=status.HTTP_200_OK
        )
