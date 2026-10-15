from mini_store.pricing import calculate_order_total


def test_standard_customer_in_mexico_pays_tax_and_shipping():
    assert calculate_order_total(500, "standard", None, "MX") == 679.0

def test_premium_customer_receives_discount():
    assert calculate_order_total(1000, "premium", None, "MX") == 1143.0

def test_save20_coupon_requires_minimum_subtotal():
    assert calculate_order_total(1400, "standard", "SAVE20", "MX") == 1624.0

def test_international_shipping_below_threshold():
    assert calculate_order_total(500, "standard", None, "US") == 799.0

def test_international_shipping_above_threshold():
    assert calculate_order_total(2000, "standard", None, "US") == 2199.0

def test_employee_customer_receives_discount():
    assert calculate_order_total(
        1000, "employee", None, "MX"
    ) == 1085.0

def test_save20_coupon_applies_at_minimum_subtotal():
    assert calculate_order_total(1500, "standard", "SAVE20", "MX") == 1392.0

def test_customer_discount_and_coupon_stack_on_original_subtotal():
    assert calculate_order_total(2000, "employee", "SAVE20", "MX") == 1508.0

def test_unknown_coupon_is_ignored():
    assert calculate_order_total(500, "standard", "BOGUS", "MX") == 679.0


