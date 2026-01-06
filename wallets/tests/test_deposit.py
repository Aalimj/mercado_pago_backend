
import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APIClient
from wallets.models import Wallet, Transaction

from users.models import User



@pytest.mark.django_db
class TestDepositAPI:

    def setup_method(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test User"
        )

        self.wallet = Wallet.objects.get(user=self.user)

        self.client.force_authenticate(user=self.user)
        self.url = reverse("wallet-deposit")

    def test_deposit_success(self):
        response = self.client.post(
            self.url,
            {"amount": "100.00"},
            format="json"
        )

        assert response.status_code == 200

        self.wallet.refresh_from_db()

        assert self.wallet.balance == Decimal("100.00")
        assert Transaction.objects.count() == 1

        transaction = Transaction.objects.first()
        assert transaction.amount == Decimal("100.00")
        assert transaction.type == Transaction.Type.DEPOSIT

    def test_deposit_invalid_amount(self):
        response = self.client.post(
            self.url,
            {"amount": "-10"},
            format="json"
        )

        assert response.status_code == 400
        assert Transaction.objects.count() == 0

    def test_deposit_requires_authentication(self):
        client = APIClient()

        response = client.post(
            self.url,
            {"amount": "50"},
            format="json"
        )

        assert response.status_code == 401
