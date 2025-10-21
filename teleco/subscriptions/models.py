from django.db import models
from django.utils import timezone


class Subscription(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='subscriptions')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='subscriptions')
    offer = models.ForeignKey('products.Offer', on_delete=models.SET_NULL, related_name='subscriptions', null=True, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.customer.msisdn} -> {self.product.code} ({'active' if self.is_active else 'inactive'})"

    class Meta:
        indexes = [
            models.Index(fields=["customer", "started_at"]),
            models.Index(fields=["product", "started_at"]),
        ]

# Create your models here.
