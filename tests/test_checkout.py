from mini_store.checkout import validate_checkout


def test_valid_checkout_is_accepted():
    assert validate_checkout(3, 750, "MX", "44100", "card") == (True, "ok")


def test_empty_cart_is_rejected():
    assert validate_checkout(0, 750, "MX", "44100", "card") == (
        False,
        "cart is empty",
    )


def test_too_many_items_are_rejected():
    assert validate_checkout(51, 750, "MX", "44100", "card") == (
        False,
        "too many items",
    )


def test_maximum_item_count_is_accepted():
    assert validate_checkout(50, 750, "MX", "44100", "card") == (True, "ok")


def test_zero_subtotal_is_rejected():
    assert validate_checkout(3, 0, "MX", "44100", "card") == (
        False,
        "subtotal must be positive",
    )


def test_negative_subtotal_is_rejected():
    assert validate_checkout(3, -100, "MX", "44100", "card") == (
        False,
        "subtotal must be positive",
    )


def test_unsupported_country_is_rejected():
    assert validate_checkout(3, 750, "CA", "44100", "card") == (
        False,
        "unsupported country",
    )


def test_blank_postal_code_is_rejected():
    assert validate_checkout(3, 750, "MX", "   ", "card") == (
        False,
        "postal code is required",
    )


def test_unsupported_payment_method_is_rejected():
    assert validate_checkout(3, 750, "MX", "44100", "cash") == (
        False,
        "unsupported payment method",
    )
