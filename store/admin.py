from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "product_type", "price", "is_premium", "created_at")
    list_filter = ("product_type", "is_premium")
    search_fields = ("title",)
