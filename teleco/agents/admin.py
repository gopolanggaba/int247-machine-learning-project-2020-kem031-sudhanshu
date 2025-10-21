from django.contrib import admin
from .models import PersonalizedOffer


@admin.register(PersonalizedOffer)
class PersonalizedOfferAdmin(admin.ModelAdmin):
    list_display = ("customer", "offer", "score", "is_active", "created_at")
    list_filter = ("is_active",)

# Register your models here.
