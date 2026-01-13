from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Extra user data for paid access control."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} (paid={self.has_paid})"
