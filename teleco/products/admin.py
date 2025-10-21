from django.contrib import admin
from .models import Product, Offer


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "category", "price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("code", "name")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "discount_percent", "is_personalized", "is_active")
    list_filter = ("is_personalized", "is_active")

# Register your models here.
