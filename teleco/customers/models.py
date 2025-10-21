from django.db import models


class Customer(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )

    msisdn = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Derived fields for segmentation
    is_high_value = models.BooleanField(default=False)
    average_monthly_spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_active_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.msisdn} - {self.first_name} {self.last_name}" 

    class Meta:
        ordering = ["-created_at"]

# Create your models here.
