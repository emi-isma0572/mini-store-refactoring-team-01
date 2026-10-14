"""Shipping quotation rules."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Package:
    weight_kg: float
    length_cm: float
    width_cm: float
    height_cm: float

    @property
    def volumetric_weight(self) -> float:
        return (self.length_cm * self.width_cm * self.height_cm) / 5000

    @property
    def chargeable_weight(self) -> float:
        return max(self.weight_kg, self.volumetric_weight)

    @property
    def is_oversized(self) -> bool:
        return (
            self.length_cm > 100
            or self.width_cm > 100
            or self.height_cm > 100
        )


def volumetric_weight(length_cm: float, width_cm: float, height_cm: float) -> float:
    return Package(0.0, length_cm, width_cm, height_cm).volumetric_weight


def chargeable_weight(
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
) -> float:
    return Package(weight_kg, length_cm, width_cm, height_cm).chargeable_weight


def shipping_quote(
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
    destination_country: str,
    expedited: bool,
) -> float:
    pkg = Package(weight_kg, length_cm, width_cm, height_cm)
    
    rates = {
        "MX": (89.0, 18.0),
        "US": (199.0, 42.0),
    }
    base, per_kg = rates.get(destination_country, (299.0, 65.0))

    total = base + pkg.chargeable_weight * per_kg

    if expedited:
        total *= 1.35

    if pkg.is_oversized:
        total += 120.0

    return round(total, 2)