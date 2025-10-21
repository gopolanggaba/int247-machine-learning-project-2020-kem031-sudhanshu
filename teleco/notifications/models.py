from django.db import models


class Notification(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='notifications')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    channel = models.CharField(max_length=50, default='email')
    scheduled_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Notification to {self.customer.msisdn}: {self.subject} ({self.status})"

# Create your models here.
