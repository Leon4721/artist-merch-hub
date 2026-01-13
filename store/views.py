from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, "store/product_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Premium lock
    if product.is_premium:
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to view premium items.")
            return redirect("/")  # we'll change to login page after auth is wired

        # user is logged in, check paid status
        if not hasattr(request.user, "profile") or not request.user.profile.has_paid:
            return render(request, "store/product_locked.html", {"product": product})

    return render(request, "store/product_detail.html", {"product": product})
