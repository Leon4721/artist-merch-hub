import random
from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = "Seed the database with fake products"

    def handle(self, *args, **kwargs):
        titles = [
            "T-Shirt", "Hoodie", "Sticker Pack", "Art Print", "Hat",
            "Poster", "Phone Case", "Mug", "Limited Edition Vinyl", "Keychain"
        ]
        descriptions = [
            "High-quality merch.", "Official artist drop.", "Limited edition.",
            "Exclusive design.", "Made with love and creativity."
        ]

        # Delete old
        Product.objects.all().delete()

        # Create 10 new products
        for i in range(10):
            Product.objects.create(
                title=random.choice(titles) + f" #{i+1}",
                description=random.choice(descriptions),
                price=random.uniform(9.99, 99.99),
                is_premium=random.choice([True, False]),
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully added 10 products"))

