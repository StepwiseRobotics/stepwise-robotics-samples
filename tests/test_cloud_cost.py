import pytest

from stepwise_samples.cloud_cost import (
    HOURS_PER_MONTH,
    estimate_monthly_cost,
    forgotten_stop_cost,
)


def test_compute_only():
    est = estimate_monthly_cost(hourly_rate=2.0, hours_running=20)
    assert est.compute == pytest.approx(40.0)
    assert est.storage == 0.0
    assert est.total == pytest.approx(40.0)


def test_with_storage():
    est = estimate_monthly_cost(
        hourly_rate=1.0, hours_running=10, storage_gb=100, storage_rate_per_gb_month=0.08
    )
    assert est.storage == pytest.approx(8.0)
    assert est.total == pytest.approx(18.0)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"hourly_rate": -1, "hours_running": 1},
        {"hourly_rate": 1, "hours_running": -1},
        {"hourly_rate": 1, "hours_running": 1, "storage_gb": -1},
        {"hourly_rate": 1, "hours_running": HOURS_PER_MONTH + 1},
    ],
)
def test_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        estimate_monthly_cost(**kwargs)


def test_forgotten_stop_cost():
    assert forgotten_stop_cost(1.0) == pytest.approx(HOURS_PER_MONTH)
