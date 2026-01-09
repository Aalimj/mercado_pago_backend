import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APIClient

from wallets.models import Wallet, Transaction
from users.models import User


@pytest.mark.django_db
class TestTransferAPI:

    def setup_method(self):
        self.client = APIClient()

      
        self.sender = User.objects.create_user(
        email="sender@test.com",
        password="testpass123",
        name="Sender User",
        cpf="11111111111"
        )

        self.receiver = User.objects.create_user(
        email="receiver@test.com",
        password="testpass123",
        name="Receiver User",
        cpf="22222222222"
        )

       
        self.sender_wallet = Wallet.objects.get(user=self.sender)
        self.receiver_wallet = Wallet.objects.get(user=self.receiver)

       
        self.sender_wallet.balance = Decimal("500.00")
        self.sender_wallet.save(update_fields=["balance"])

        self.receiver_wallet.balance = Decimal("100.00")
        self.receiver_wallet.save(update_fields=["balance"])

        self.client.force_authenticate(user=self.sender)
        self.url = reverse("wallet-transfer")

    def test_transfer_success(self):
        response = self.client.post(
            self.url,
            {
                "receiver_account_number": self.receiver_wallet.account_number,
                "amount": "200.00"
            },
            format="json"
        )

        assert response.status_code == 200

        self.sender_wallet.refresh_from_db()
        self.receiver_wallet.refresh_from_db()

        assert self.sender_wallet.balance == Decimal("300.00")
        assert self.receiver_wallet.balance == Decimal("300.00")

        assert Transaction.objects.count() == 2

    def test_transfer_insufficient_balance(self):
        response = self.client.post(
            self.url,
            {
                "receiver_account_number": self.receiver_wallet.account_number,
                "amount": "1000.00"
            },
            format="json"
        )

        assert response.status_code == 400
        assert Transaction.objects.count() == 0

    def test_transfer_to_self(self):
        response = self.client.post(
            self.url,
            {
                "receiver_account_number": self.sender_wallet.account_number,
                "amount": "50.00"
            },
            format="json"
        )

        assert response.status_code == 400
        assert Transaction.objects.count() == 0

    def test_transfer_requires_authentication(self):
        client = APIClient()

        response = client.post(
            self.url,
            {
                "receiver_account_number": self.receiver_wallet.account_number,
                "amount": "50.00"
            },
            format="json"
        )

        assert response.status_code == 401
