import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APIClient
from wallets.models import Wallet, Transaction
from users.models import User

@pytest.mark.django_db
class TestWithdrawAPI:

    def setup_method(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            email="withdraw_test@example.com",
            password = "testpass123",
            name ="withdraw User"
        )
        self.wallet, _ = Wallet.objects.get_or_create(user=self.user)
        Wallet.objects.filter(id=self.wallet.id).update(balance=Decimal("200.00"))
        self.wallet.refresh_from_db()

        self.client.force_authenticate(user=self.user)
        self.url = reverse("wallet-withdraw")

    def test_withdraw_success(self):
        response = self.client.post(
            self.url,
            {"amount":"100.00"},
            format="json"
        )

        assert response.status_code == 200
        self.wallet.refresh_from_db()
        assert self.wallet.balance == Decimal("100.00")
        assert Transaction.objects.count() == 1
        txn = Transaction.objects.first()
        assert txn.amount == Decimal("100.00")
        assert txn.type == Transaction.Type.WITHDRAW
        assert txn.reference == "manual_withdraw"

    def test_withdraw_insufficient_balance(self):
        response = self.client.post(
            self.url,
            {"amount":"500.00"},
            format="json"
        )

        assert response.status_code == 400
        assert Transaction.objects.count() == 0

    def test_withdraw_invalid_amount(self):
        response = self.client.post(
            self.url,
            {"amount": "-10"},
            format ="json"
        )
        assert response.status_code == 400
        assert Transaction.objects.count() == 0

    def test_withdraw_requires_authentication(self):
        client = APIClient()
        response = client.post(
            self.url,
            {"amount": "50"},
            format = "json"
        )
        assert response.status_code == 401