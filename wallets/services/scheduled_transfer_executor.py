from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from wallets.models import ScheduledTransfer,Wallet, Transaction

def get_next_run(interval, current):
    if interval == ScheduledTransfer.Interval.DAILY:
        return current + timedelta(days=1)
    if interval == ScheduledTransfer.Interval.WEEKLY:
        return current + timedelta(weeks=1)
    if interval == ScheduledTransfer.Interval.MONTHLY:
        return current + timedelta(days=30)
    
def execute_scheduled_transfers():
    now = timezone.now()

    transfers = ScheduledTransfer.objects.filter(
        is_active=True,
        next_run_at__lte=now,
    )

    with transaction.atomic():
        for transfer in transfers:
            sender_wallet = Wallet.objects.select_for_update().get(user=transfer.sender)
            receiver_wallet = Wallet.objects.select_for_update().get(user=transfer.receiver)

            if sender_wallet.balance >= transfer.amount:
                sender_wallet.balance -= transfer.amount
                receiver_wallet.balance += transfer.amount

                sender_wallet.save(update_fields=["balance"])
                receiver_wallet.save(update_fields=["balance"])

                Transaction.objects.create(
                    wallet=sender_wallet,
                    user=sender_wallet.user,
                    amount=transfer.amount,
                    type=Transaction.Type.TRANSFER_OUT,
                    reference=f"scheduled_transfer_to_{receiver_wallet.account_number}"
                )

                Transaction.objects.create(
                    wallet=receiver_wallet,
                    user=receiver_wallet.user,
                    amount=transfer.amount,
                    type=Transaction.Type.TRANSFER_IN,
                    reference=f"scheduled_transfer_from_{sender_wallet.account_number}"
                )

                transfer.next_run_at += transfer.interval  # assume interval is timedelta
                transfer.save(update_fields=["next_run_at"])
            else:
                print(f"Insufficient balance for scheduled transfer {transfer.id}")

            
