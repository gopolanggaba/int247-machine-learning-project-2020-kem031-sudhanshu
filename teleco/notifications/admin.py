from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("customer", "subject", "channel", "status", "scheduled_at", "sent_at")
    list_filter = ("channel", "status")
    search_fields = ("customer__msisdn", "subject")

# Register your models here.
