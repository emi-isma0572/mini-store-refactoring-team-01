"""Pricing rules for orders."""

def _calculate_shipping(country: str, discounted_subtotal: float) -> float:
    """Return shipping fee based on destination and subtotal threshold."""
    if country == "MX":
        return 0.0 if discounted_subtotal >= 1000 else 99.0
    return 199.0 if discounted_subtotal >= 2000 else 299.0


def calculate_order_total(
    subtotal: float,
    customer_type: str,
    coupon_code: str | None,
    country: str,
) -> float:
    """Return the final order total after discounts, tax, and shipping."""
    discount = 0.0

    if customer_type == "premium":
        discount = subtotal * 0.10
    elif customer_type == "employee":
        discount = subtotal * 0.15

    if coupon_code == "SAVE5":
        discount += subtotal * 0.05
    elif coupon_code == "SAVE20" and subtotal >= 1500:
        discount += subtotal * 0.20

    discounted_subtotal = max(0.0, subtotal - discount)
    tax = discounted_subtotal * 0.16 if country == "MX" else 0.0
    shipping = _calculate_shipping(country, discounted_subtotal)

    return round(discounted_subtotal + tax + shipping, 2)