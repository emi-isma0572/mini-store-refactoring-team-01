"""Pricing rules for orders."""

_CUSTOMER_DISCOUNT_RATES = {"premium": 0.10, "employee": 0.15}
_TAX_RATES = {"MX": 0.16}


def _customer_discount(subtotal: float, customer_type: str) -> float:
    return subtotal * _CUSTOMER_DISCOUNT_RATES.get(customer_type, 0.0)


def _coupon_discount(subtotal: float, coupon_code: str | None) -> float:
    """Coupons are evaluated against the pre-discount subtotal."""
    if coupon_code == "SAVE5":
        return subtotal * 0.05
    if coupon_code == "SAVE20" and subtotal >= 1500:
        return subtotal * 0.20
    return 0.0


def _calculate_tax(country: str, discounted_subtotal: float) -> float:
    return discounted_subtotal * _TAX_RATES.get(country, 0.0)


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
    discount = _customer_discount(subtotal, customer_type) + _coupon_discount(
        subtotal, coupon_code
    )
    discounted_subtotal = max(0.0, subtotal - discount)
    tax = _calculate_tax(country, discounted_subtotal)
    shipping = _calculate_shipping(country, discounted_subtotal)
    return round(discounted_subtotal + tax + shipping, 2)