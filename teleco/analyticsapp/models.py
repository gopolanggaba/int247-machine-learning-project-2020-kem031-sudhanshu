from django.db import models


class LeaderboardEntry(models.Model):
    KIND_CHOICES = (
        ("REVENUE", "Revenue"),
        ("CALLS", "Calls"),
    )

    PERIOD_CHOICES = (
        ("HOURLY", "Hourly"),
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
        ("ANNUAL", "Annual"),
    )

    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=20, decimal_places=4)
    rank = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("kind", "period", "period_start", "period_end", "customer")
        indexes = [
            models.Index(fields=["kind", "period", "period_start", "period_end"]),
            models.Index(fields=["customer"]),
        ]

    def __str__(self) -> str:
        return f"{self.kind} {self.period} rank {self.rank} {self.customer.msisdn}"

# Create your models here.
