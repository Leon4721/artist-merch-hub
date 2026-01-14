from django.conf import settings
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_session_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField(default=0)  # in pence
    currency = models.CharField(max_length=10, default="gbp")
    status = models.CharField(max_length=50, default="created")  # created, paid, cancelled
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user} - {self.status}"
