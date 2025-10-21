from django.db import models


class PersonalizedOffer(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='personalized_offers')
    offer = models.ForeignKey('products.Offer', on_delete=models.CASCADE, related_name='personalized_for')
    score = models.FloatField(default=0.0)
    rationale = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Personalized {self.offer.name} for {self.customer.msisdn} ({self.score:.2f})"

# Create your models here.
