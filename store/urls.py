from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("premium/", views.premium_library, name="premium_library"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
    path("<int:product_id>/review/add/", views.review_add, name="review_add"),
    path("<int:product_id>/review/edit/", views.review_edit, name="review_edit"),
    path("<int:product_id>/review/delete/", views.review_delete, name="review_delete"),
]
