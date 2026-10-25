import pytest
from ai_ecolens.analytics.metrics import monthly_energy_kwh, estimated_carbon_kgco2e


def test_monthly_energy():
    assert monthly_energy_kwh(100_000, 0.5) == 50


def test_carbon():
    assert estimated_carbon_kgco2e(50, 100) == 5


def test_negative_inputs():
    with pytest.raises(ValueError):
        monthly_energy_kwh(-1, 0.5)
