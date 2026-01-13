from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "has_paid")
    list_filter = ("has_paid",)
    search_fields = ("user__username", "user__email")
