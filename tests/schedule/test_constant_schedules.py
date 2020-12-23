import pytest

from loan_calculator.schedule.constant import ConstantAmortizationSchedule


def test_constant_amortization_schedule():
    """Assert basic textbook scenario."""
    principal = 800.00
    daily_interest_rate = 0.8
    return_days = [1, 2, 3, 4, 5]

    schedule = ConstantAmortizationSchedule(
        principal,
        daily_interest_rate,
        return_days
    )

    expected_amortizations = [160, 160, 160, 160, 160]
    expected_balances = [800, 640, 480, 320, 160, 0]
    expected_interests = [640, 512, 384, 256, 128]
    expected_payments = [800, 672, 544, 416, 288]

    assert schedule.amortizations == pytest.approx(expected_amortizations, rel=0.01)  # noqa
    assert schedule.balance == pytest.approx(expected_balances, rel=0.01)
    assert schedule.interest_payments == pytest.approx(expected_interests, rel=0.01)  # noqa
    assert schedule.due_payments == pytest.approx(expected_payments, rel=0.01)

    assert schedule.total_amortization == pytest.approx(principal, rel=0.01)
    assert schedule.total_interest == pytest.approx(1920.00, rel=0.01)
    assert schedule.total_paid == pytest.approx(2720.00, rel=0.01)
