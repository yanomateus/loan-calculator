import numpy as np

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

    expected_amortizations = np.array([160, 160, 160, 160, 160], dtype=float)
    expected_balances = np.array([800, 640, 480, 320, 160, 0], dtype=float)
    expected_interests = np.array([640, 512, 384, 256, 128], dtype=float)
    expected_payments = np.array([800, 672, 544, 416, 288], dtype=float)

    np.testing.assert_almost_equal(
        schedule.amortizations, expected_amortizations
    )

    np.testing.assert_almost_equal(schedule.balance, expected_balances)

    np.testing.assert_almost_equal(
        schedule.interest_payments, expected_interests
    )

    np.testing.assert_almost_equal(schedule.due_payments, expected_payments)

    np.testing.assert_almost_equal(schedule.total_amortization, principal)
    np.testing.assert_almost_equal(schedule.total_interest, 1920.00)
    np.testing.assert_almost_equal(schedule.total_paid, 2720.00)
