import pytest

from datetime import date

from loan_calculator.loan import Loan


args_ = (
    1000.0,
    0.5,
    date(2020, 1, 1),
    [
        date(2020, 1, 2), date(2020, 1, 3),
        date(2020, 1, 4), date(2020, 1, 5),
    ]
)


def test_very_large_year_size():
    """Assert trivial year provides equal amortizations."""

    def _do_assert(schedule_):
        loan = Loan(
            *args_,
            year_size=100000,
            grace_period=0,
            amortization_schedule_type=schedule_
        )

        assert loan.amortizations == pytest.approx([250.0, 250.0, 250.0, 250.0], rel=0.01)  # noqa
        assert loan.amortizations == pytest.approx(loan.amortizations)

    for schedule in [
        'progressive_price_schedule',
        'regressive_price_schedule',
        'constant_amortization_schedule',
    ]:

        _do_assert(schedule)


def test_grace_period_exceeds_loan_start():

    for date_ in args_[3]:

        with pytest.raises(ValueError):

            Loan(
                *args_,
                grace_period=(date_ - args_[2]).days
            )


def test_unknown_amortization_schedule():

    with pytest.raises(TypeError):

        Loan(*args_, amortization_schedule_type='foo')
