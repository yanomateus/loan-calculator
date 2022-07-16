import pytest

from datetime import date

from loan_calculator.loan import Loan
from loan_calculator.utils import display_summary
from loan_calculator.schedule.base import AmortizationScheduleType


def test_this_was_an_error_before():
    """
    This was an error before:
    utils.py:26-27 : display_summary(): - loan.amortizations.tolist(),... (AttributeError: 'list' object has no attribute 'tolist')
    """
    loan = Loan(
        principal=10000.00,  # principal
        annual_interest_rate=0.05,  # annual interest rate
        start_date=date(2020, 1, 5),  # start date
        return_dates=[
            date(2020, 2, 12),  # expected return date
            date(2020, 3, 13),  # expected return date
            date(2020, 3, 11),  # expected return date
            date(2020, 4, 13),  # expected return date
            date(2020, 5, 12),  # expected return date
            date(2020, 6, 12),  # expected return date
            date(2020, 7, 14),  # expected return date
            date(2020, 8, 15),  # expected return date
        ],
        year_size=365,  # used to convert between annual and daily interest rates # noqa
        grace_period=0,  # number of days for which the principal is not affected by the interest rate  # noqa
        amortization_schedule_type=AmortizationScheduleType.progressive_price_schedule, # noqa
        # determines how the principal is amortized
    )
    display_summary(loan)
