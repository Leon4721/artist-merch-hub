from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path('store/', include('store.urls', namespace="store")),
    path('', include('store.urls', namespace="store")),  
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("checkout/", include("checkout.urls")),
]
