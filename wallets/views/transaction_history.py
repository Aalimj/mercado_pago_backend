from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wallets.serializers import TransactionSerializer
from wallets.models.transaction import Transaction
from rest_framework import status

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_wallet = request.user.wallet
        transactions = Transaction.objects.filter(wallet=user_wallet).order_by("-created_at")

        page = int(request.query_params.get("page",1))
        page_size = int(request.query_params.get("page_size",10))
        start = (page - 1) * page_size
        end = start + page_size
        pageinated = transactions[start:end]

        serializer = TransactionSerializer(pageinated, many=True)
        return Response({
            "count":transactions.count(),
            "page": page,
            "page_size":page_size,
            "transaction": serializer.data
        }, status=status.HTTP_200_OK)
