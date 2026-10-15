"""Shipping quotation rules."""

from dataclasses import dataclass

# AI FIX: Extraer configuración para separar los datos de la lógica matemática.
SHIPPING_RATES = {
    "MX": {"base": 89.0, "per_kg": 18.0},
    "US": {"base": 199.0, "per_kg": 42.0},
    "DEFAULT": {"base": 299.0, "per_kg": 65.0}
}
EXPEDITED_MULTIPLIER = 1.35
OVERSIZE_SURCHARGE = 120.0

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
    
    # AI FIX: Lógica mucho más limpia sin estructuras if/elif complejas
    rates = SHIPPING_RATES.get(destination_country, SHIPPING_RATES["DEFAULT"])
    
    total = rates["base"] + (pkg.chargeable_weight * rates["per_kg"])

    if expedited:
        total *= EXPEDITED_MULTIPLIER

    if pkg.is_oversized:
        total += OVERSIZE_SURCHARGE

    return round(total, 2)