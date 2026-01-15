from decimal import Decimal
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from accounts.models import UserProfile
from .models import Order

# ✅ Always use environment variable for safety
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if profile.has_paid:
        messages.info(request, "You already have premium access.")
        return redirect("store:product_list")

    try:
        success_url = request.build_absolute_uri("/checkout/success/") + "?session_id={CHECKOUT_SESSION_ID}"
        cancel_url = request.build_absolute_uri("/checkout/cancel/") + "?session_id={CHECKOUT_SESSION_ID}"

        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {
                            "name": "Premium Access Pass",
                        },
                        "unit_amount": 999,  # £9.99 in pence
                    },
                    "quantity": 1,
                }
            ],
            client_reference_id=str(request.user.id),
            success_url=success_url,
            cancel_url=cancel_url,
        )

        Order.objects.create(
            user=request.user,
            stripe_session_id=session.id,
            amount=Decimal("9.99"),
            currency="gbp",
            status="pending",
        )

        return redirect(session.url)

    except Exception as e:
        messages.error(request, f"Stripe error: {e}")
        return redirect("store:product_list")


@login_required
def checkout_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        messages.error(request, "Missing Stripe session.")
        return redirect("store:product_list")

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status != "paid":
            messages.error(request, "Payment not completed.")
            return redirect("store:product_list")

        order = Order.objects.get(
            stripe_session_id=session_id,
            user=request.user,
            status="pending",
        )
        order.status = "paid"
        order.save()

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.has_paid = True
        profile.save()

        messages.success(request, "Payment successful! Premium access unlocked.")
        return redirect("store:premium_library")

    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect("store:product_list")

    except Exception as e:
        messages.error(request, f"Stripe error: {e}")
        return redirect("store:product_list")


@login_required
def checkout_cancel(request):
    session_id = request.GET.get("session_id")

    if session_id:
        Order.objects.filter(
            stripe_session_id=session_id,
            user=request.user,
            status="pending",
        ).update(status="cancelled")

    messages.info(request, "Payment cancelled.")
    return redirect("store:product_list")
