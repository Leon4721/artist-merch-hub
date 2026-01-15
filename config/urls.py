# config/urls.py
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),

    # Store only lives at /store/
    path("store/", include(("store.urls", "store"), namespace="store")),

    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("checkout/", include("checkout.urls")),
]
