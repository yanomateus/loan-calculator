import pytest

from datetime import date

from loan_calculator.loan import Loan
from loan_calculator.schedule.base import AmortizationScheduleType

args_ = (
    1000.0,
    0.5,
    date(2020, 1, 1),
    [
        date(2020, 1, 2), date(2020, 1, 3),
        date(2020, 1, 4), date(2020, 1, 5),
    ]
)


def test_grace_period_exceeds_loan_start():

    for date_ in args_[3]:

        with pytest.raises(ValueError):

            Loan(
                *args_,
                grace_period=(date_ - args_[2]).days
            )


def test_unknown_amortization_schedule():

    with pytest.raises(ValueError):

        Loan(*args_, amortization_schedule_type='foo')
