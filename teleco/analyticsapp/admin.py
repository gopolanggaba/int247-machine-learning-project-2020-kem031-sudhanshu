from django.contrib import admin
from .models import LeaderboardEntry


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ("kind", "period", "period_start", "period_end", "customer", "value", "rank")
    list_filter = ("kind", "period")
    search_fields = ("customer__msisdn",)

# Register your models here.
