from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("customer", "product", "offer", "started_at", "expires_at", "is_active")
    list_filter = ("is_active",)
    search_fields = ("customer__msisdn", "product__code")

# Register your models here.
