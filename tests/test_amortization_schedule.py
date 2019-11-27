import numpy as np
import numpy.testing as npt

from loan_cashflow_calculator.amortization_schedule import (
    ProgressivePriceSchedule,
    ConstantAmortizationSchedule,
    RegressivePriceSchedule)


def test_constant_amortization_schedule():
    """Assert basic textbook scenario."""
    principal = 800.00
    daily_interest_rate = 0.8
    return_days = [1, 2, 3, 4, 5]

    schedule = ConstantAmortizationSchedule(principal, daily_interest_rate, return_days)

    expected_amortizations = np.array([160, 160, 160, 160, 160], dtype=float)
    expected_balances = np.array([800, 640, 480, 320, 160, 0], dtype=float)
    expected_interests = np.array([640, 512, 384, 256, 128], dtype=float)
    expected_payments = np.array([800, 672, 544, 416, 288], dtype=float)

    np.testing.assert_almost_equal(schedule.amortizations, expected_amortizations)
    np.testing.assert_almost_equal(schedule.balance, expected_balances)
    np.testing.assert_almost_equal(schedule.interest_payments, expected_interests)
    np.testing.assert_almost_equal(schedule.due_payments, expected_payments)

    np.testing.assert_almost_equal(schedule.total_amortization, principal)
    np.testing.assert_almost_equal(schedule.total_interest, 1920.00)
    np.testing.assert_almost_equal(schedule.total_paid, 2720.00)


def test_price_amortization_schedule():
    """Assert basic textbook scenario."""
    principal = 8530.20
    daily_interest_rate = 0.03
    return_days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    schedule = ProgressivePriceSchedule(principal, daily_interest_rate, return_days)

    expected_amortizations = np.array(
        [744.09, 766.42, 789.41, 813.09, 837.48,
         862.61, 888.49, 915.14, 942.60, 970.87],
        dtype=float
    )

    expected_balances = np.array(
        [8530.20, 7786.11, 7019.69, 6230.28, 5417.19,
         4579.71, 3717.10, 2828.61, 1913.47, 970.87, 0.0],
        dtype=float
    )

    expected_interests = np.array(
        [255.91, 233.58, 210.59, 186.91, 162.52,
         137.39, 111.51, 84.86, 57.40, 29.13],
        dtype=float
    )

    expected_payments = np.array(
        [1000.00, 1000.00, 1000.00, 1000.00, 1000.00,
         1000.00, 1000.00, 1000.00, 1000.00, 1000.00],
        dtype=float
    )

    r_schedule = RegressivePriceSchedule(principal, daily_interest_rate, return_days)

    npt.assert_almost_equal(schedule.amortizations, expected_amortizations,
                            decimal=2)
    npt.assert_almost_equal(schedule.balance, expected_balances, decimal=2)
    npt.assert_almost_equal(schedule.interest_payments, expected_interests,
                            decimal=2)
    npt.assert_almost_equal(schedule.due_payments, expected_payments, decimal=2)

    npt.assert_almost_equal(schedule.total_amortization, principal, decimal=2)
    npt.assert_almost_equal(schedule.total_interest, 1469.80, decimal=2)
    npt.assert_almost_equal(schedule.total_paid, 10000.00, decimal=2)
