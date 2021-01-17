import pytest
from loan_calculator.schedule.price import (ProgressivePriceSchedule,
                                            RegressivePriceSchedule)


def test_progressive_price_amortization_schedule():
    """Assert basic textbook scenario."""
    principal = 8530.20
    daily_interest_rate = 0.03
    return_days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    schedule = ProgressivePriceSchedule(
        principal,
        daily_interest_rate,
        return_days
    )

    expected_amortizations = [
        744.09, 766.42, 789.41, 813.09, 837.48,
        862.61, 888.49, 915.14, 942.60, 970.87
    ]

    expected_balances = [
        8530.20, 7786.11, 7019.69, 6230.28, 5417.19,
        4579.71, 3717.10, 2828.61, 1913.47, 970.87, 0.0
    ]

    expected_interests = [
        255.91, 233.58, 210.59, 186.91, 162.52,
        137.39, 111.51, 84.86, 57.40, 29.13
    ]

    expected_payments = [
        1000.00, 1000.00, 1000.00, 1000.00, 1000.00,
        1000.00, 1000.00, 1000.00, 1000.00, 1000.00
    ]

    assert schedule.amortizations == pytest.approx(expected_amortizations, rel=0.01)  # noqa
    assert schedule.balance == pytest.approx(expected_balances, rel=0.01)
    assert schedule.interest_payments == pytest.approx(expected_interests, rel=0.01)  # noqa
    assert schedule.due_payments == pytest.approx(expected_payments, rel=0.01)
    assert schedule.total_amortization == pytest.approx(principal, rel=0.01)
    assert schedule.total_interest == pytest.approx(1469.80, rel=0.01)
    assert schedule.total_paid == pytest.approx(10000.00, rel=0.01)


def test_regressive_price_amortization_schedule():
    """Assert basic textbook scenario."""
    principal = 8530.20
    daily_interest_rate = 0.0009857789690617125  # yields 3% every 30 days
    return_days = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]

    schedule = RegressivePriceSchedule(
        principal,
        daily_interest_rate,
        return_days
    )

    expected_amortizations = [
        970.87, 942.6, 915.14, 888.49, 862.61,
        837.48, 813.09, 789.41, 766.42, 744.09
    ]

    expected_balances = [
        8530.20, 7786.11, 7019.69, 6230.28, 5417.19,
        4579.71, 3717.10, 2828.61, 1913.47, 970.87, 0.0
    ]

    expected_interests = [
        29.13, 57.4, 84.86, 111.51, 137.39,
        162.52, 186.91, 210.59, 233.58, 255.91
    ]

    expected_payments = [
        1000.00, 1000.00, 1000.00, 1000.00, 1000.00,
        1000.00, 1000.00, 1000.00, 1000.00, 1000.00
    ]

    assert schedule.amortizations == pytest.approx(expected_amortizations, rel=0.01)  # noqa
    assert schedule.balance == pytest.approx(expected_balances, rel=0.01)
    assert schedule.interest_payments == pytest.approx(expected_interests, rel=0.01)  # noqa
    assert schedule.due_payments == pytest.approx(expected_payments, rel=0.01)
    assert schedule.total_amortization == pytest.approx(principal, rel=0.01)
    assert schedule.total_interest == pytest.approx(1469.80, rel=0.01)
    assert schedule.total_paid == pytest.approx(10000.00, rel=0.01)
