from django.contrib import admin
from .models import Recharge, Invoice


@admin.register(Recharge)
class RechargeAdmin(admin.ModelAdmin):
    list_display = ("customer", "amount", "channel", "created_at")
    list_filter = ("channel",)
    search_fields = ("customer__msisdn",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("customer", "total_amount", "period_start", "period_end")

# Register your models here.
