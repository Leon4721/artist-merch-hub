# store/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import UserProfile
from .forms import ReviewForm
from .models import Product, Review


def product_list(request):
    q = (request.GET.get("q") or "").strip()
    products = Product.objects.all().order_by("-created_at")

    if q:
        products = products.filter(Q(title__icontains=q) | Q(description__icontains=q))

    return render(request, "store/product_list.html", {"products": products, "q": q})


def product_detail(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)

    has_paid = False
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        has_paid = profile.has_paid

    # Protect premium items
    if product.is_premium and not has_paid:
        # Use the working template inside the store app
        return render(request, "store/product_locked.html", {"product": product})

    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "reviews": product.reviews.select_related("user").all(),
            "user_review": user_review,
            "review_form": ReviewForm(),
        },
    )


@login_required
def review_add(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if product.is_premium and not profile.has_paid:
        messages.error(request, "That item is premium. Please unlock access first.")
        return redirect("checkout")

    if Review.objects.filter(product=product, user=request.user).exists():
        messages.info(request, "You already reviewed this product. You can edit your review.")
        return redirect("store:review_edit", product_id=product.id)

    form = ReviewForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        messages.success(request, "Review posted.")
        return redirect("store:product_detail", product_id=product.id)

    return render(request, "store/review_form.html", {"form": form, "product": product, "mode": "add"})


@login_required
def review_edit(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(Review, product=product, user=request.user)

    form = ReviewForm(request.POST or None, instance=review)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Review updated.")
        return redirect("store:product_detail", product_id=product.id)

    return render(request, "store/review_form.html", {"form": form, "product": product, "mode": "edit"})


@login_required
def review_delete(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(Review, product=product, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Review deleted.")
        return redirect("store:product_detail", product_id=product.id)

    return render(request, "store/review_delete_confirm.html", {"product": product})


@login_required
def premium_library(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not profile.has_paid:
        messages.info(request, "Unlock access to view the premium library.")
        return redirect("checkout")

    premium_products = Product.objects.filter(is_premium=True).order_by("-created_at")
    return render(request, "store/premium_library.html", {"products": premium_products})
