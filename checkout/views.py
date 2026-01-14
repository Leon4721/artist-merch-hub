import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """
    Create a Stripe Checkout Session (one-time payment).
    """

    if request.user.profile.has_paid:
        messages.info(request, "You already have premium access.")
        return redirect("product_list")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {"name": "Premium Access Pass"},
                        "unit_amount": 999,
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
    session_id = request.GET.get("session_id")

    if not session_id:
        messages.error(request, "Missing Stripe session. Please try again.")
        return redirect("product_list")

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status != "paid":
            messages.error(request, "Payment not completed.")
            return redirect("product_list")

        order = Order.objects.get(stripe_session_id=session_id, user=request.user)
        order.status = "paid"
        order.save()

        # Ensure profile exists
        profile = request.user.profile
        profile.has_paid = True
        profile.save()

        messages.success(request, "Payment successful! Premium access unlocked.")
        return redirect("product_list")

    except Order.DoesNotExist:
        messages.error(request, "Order not found for this session.")
        return redirect("product_list")

    except Exception as e:
        messages.error(request, f"Stripe error: {e}")
        return redirect("product_list")


@login_required
def checkout_cancel(request):
    messages.info(request, "Payment cancelled.")
    return redirect("product_list")
