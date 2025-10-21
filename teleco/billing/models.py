from django.db import models
from django.utils import timezone


class Recharge(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='recharges')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    channel = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self) -> str:
        return f"Recharge {self.amount} for {self.customer.msisdn} at {self.created_at}"


class Invoice(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='invoices')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Invoice {self.id} for {self.customer.msisdn}"

# Create your models here.
