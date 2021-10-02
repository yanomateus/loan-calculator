import pytest

from datetime import date

from loan_calculator.loan import Loan
from loan_calculator.interest_rate import YearSizeType


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


def test_proper_interest_rate_conversion_on_loan_initialization():

    # (1 + 0.5) ** (1 / 360) - 1 ~ 0.0011269264719548922
    assert Loan(*args_, year_size=YearSizeType.banker).daily_interest_rate == pytest.approx(0.0011269264719548922)  # noqa
    # (1 + 0.5) ** (1 / 365) - 1 ~ 0.0011114805470662237
    assert Loan(*args_, year_size=YearSizeType.commercial).daily_interest_rate == pytest.approx(0.0011114805470662237)  # noqa
