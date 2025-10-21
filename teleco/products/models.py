from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = (
        ("DATA", "Data"),
        ("VOICE", "Voice"),
        ("SMS", "SMS"),
        ("BUNDLE", "Bundle"),
    )

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers")
    name = models.CharField(max_length=200)
    details = models.TextField()
    discount_percent = models.PositiveIntegerField(default=0)
    is_personalized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Offer {self.name} on {self.product.code}"

# Create your models here.
