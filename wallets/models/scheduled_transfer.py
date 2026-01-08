from django.db import models 
from django.utils import timezone

class ScheduledTransfer(models.Model):
    
    class Interval(models.TextChoices):
        DAILY="daily", "Daily"
        WEEKLY = "weekly","Weekly"
        MONTHLY = "monthly", "Monthly"

    sender_wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="scheduled_outgoing"
    )

    receiver_wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="scheduled_incoming"

    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interval = models.CharField(
        max_length=10,
        choices=Interval.choices
    )
    next_run_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    create_at =  models.DateTimeField(auto_now_add=True)
