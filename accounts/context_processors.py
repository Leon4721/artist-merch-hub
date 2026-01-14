def premium_status(request):
    """
    Safe global template variable:
    - has_paid = True/False
    - never crashes if profile is missing
    """
    has_paid = False

    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        try:
            has_paid = bool(user.profile.has_paid)
        except Exception:
            has_paid = False

    return {"has_paid": has_paid}
