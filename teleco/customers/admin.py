from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("msisdn", "first_name", "last_name", "age", "is_high_value", "average_monthly_spend")
    search_fields = ("msisdn", "first_name", "last_name")

# Register your models here.
