from django.contrib import admin
from .models import CallDetailRecord


@admin.register(CallDetailRecord)
class CallDetailRecordAdmin(admin.ModelAdmin):
    list_display = ("customer", "call_type", "started_at", "duration_seconds", "cost_amount")
    list_filter = ("call_type",)
    search_fields = ("customer__msisdn",)

# Register your models here.
