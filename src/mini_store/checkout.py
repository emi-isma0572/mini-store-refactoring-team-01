"""Checkout validation rules."""

MAX_ITEMS_PER_ORDER = 50
SUPPORTED_COUNTRIES = frozenset({"MX", "US"})
SUPPORTED_PAYMENT_METHODS = frozenset({"card", "paypal"})


def validate_checkout(
    item_count: int,
    subtotal: float,
    country: str,
    postal_code: str,
    payment_method: str,
) -> tuple[bool, str]:
    """Validate whether an order may proceed to checkout.

    Rules are checked in order and the first failure is reported.
    Returns ``(True, "ok")`` when every rule passes.
    """
    if item_count <= 0:
        return False, "cart is empty"

    if item_count > MAX_ITEMS_PER_ORDER:
        return False, "too many items"

    if subtotal <= 0:
        return False, "subtotal must be positive"

    if country not in SUPPORTED_COUNTRIES:
        return False, "unsupported country"

    if not postal_code.strip():
        return False, "postal code is required"

    if payment_method not in SUPPORTED_PAYMENT_METHODS:
        return False, "unsupported payment method"

    return True, "ok"
