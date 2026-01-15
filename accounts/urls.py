from django.urls import path
from . import views

app_name = "accounts"  # REQUIRED if using "accounts:login" etc.

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]
