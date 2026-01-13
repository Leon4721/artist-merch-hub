from django.db import models


class Product(models.Model):
    PRODUCT_TYPES = (
        ("MERCH", "Merch"),
        ("MUSIC", "Music"),
    )

    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    product_type = models.CharField(max_length=5, choices=PRODUCT_TYPES)
    is_premium = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.product_type})"
