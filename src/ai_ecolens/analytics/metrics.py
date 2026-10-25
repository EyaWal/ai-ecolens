"""Transparent unit conversions for estimated inference emissions."""


def monthly_energy_kwh(requests: int, energy_wh_per_request: float) -> float:
    if requests < 0 or energy_wh_per_request < 0:
        raise ValueError("Requests and energy must be non-negative")
    return requests * energy_wh_per_request / 1000


def estimated_carbon_kgco2e(energy_kwh: float, grid_intensity_gco2e_kwh: float) -> float:
    if energy_kwh < 0 or grid_intensity_gco2e_kwh < 0:
        raise ValueError("Energy and grid intensity must be non-negative")
    return energy_kwh * grid_intensity_gco2e_kwh / 1000
