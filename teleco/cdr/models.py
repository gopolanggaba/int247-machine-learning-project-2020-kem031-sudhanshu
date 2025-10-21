from django.db import models
from django.utils import timezone


class CallDetailRecord(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='cdrs')
    call_type = models.CharField(max_length=20, choices=(
        ("VOICE_OUT", "Outgoing Voice"),
        ("VOICE_IN", "Incoming Voice"),
        ("SMS_OUT", "Outgoing SMS"),
        ("SMS_IN", "Incoming SMS"),
        ("DATA", "Data"),
    ))
    started_at = models.DateTimeField(default=timezone.now, db_index=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    cost_amount = models.DecimalField(max_digits=12, decimal_places=4, default=0)

    def __str__(self) -> str:
        return f"CDR {self.customer.msisdn} {self.call_type} {self.duration_seconds}s"

    class Meta:
        indexes = [
            models.Index(fields=["customer", "started_at"]),
        ]

# Create your models here.
