import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """
    Create a Stripe Checkout Session (one-time payment).
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {"name": "Premium Access Pass"},
                        "unit_amount": 999,  # £9.99 in pence
                    },
                    "quantity": 1,
                }
            ],
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
        )
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f"Stripe error: {e}")
        return redirect("home")


@login_required
def checkout_success(request):
    request.user.profile.has_paid = True
    request.user.profile.save()
    messages.success(request, "Payment successful! Premium access unlocked.")
    return redirect("product_list")


@login_required
def checkout_cancel(request):
    messages.info(request, "Payment cancelled.")
    return redirect("product_list")
