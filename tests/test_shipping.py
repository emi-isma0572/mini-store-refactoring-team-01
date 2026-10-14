from mini_store.shipping import (
    chargeable_weight,
    shipping_quote,
    volumetric_weight,
)


def test_volumetric_weight_calculation():
    assert volumetric_weight(50, 40, 30) == 12.0


def test_chargeable_weight_uses_real_weight_when_it_is_higher():
    assert chargeable_weight(10, 20, 20, 20) == 10


def test_chargeable_weight_uses_volumetric_weight_when_higher():
    assert chargeable_weight(2, 50, 40, 30) == 12.0


def test_domestic_shipping_quote_uses_billable_weight():
    assert shipping_quote(2, 50, 40, 30, "MX", False) == 305.0


def test_us_shipping_quote():
    assert shipping_quote(2, 50, 40, 30, "US", False) == 703.0


def test_international_shipping_quote():
    assert shipping_quote(2, 50, 40, 30, "CA", False) == 1079.0


def test_expedited_shipping_adds_surcharge():
    assert shipping_quote(2, 50, 40, 30, "MX", True) == 411.75


def test_oversize_dimension_surcharge():
    assert shipping_quote(2, 105, 40, 30, "MX", False) == 662.6