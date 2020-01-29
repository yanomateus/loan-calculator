from datetime import date

import pytest
from numpy.testing import assert_almost_equal

from loan_calculator.loan import Loan


class TestLoanBorders:

    args_ = (
        1000.0,
        0.5,
        date(2020, 1, 1),
        [
            date(2020, 1, 2), date(2020, 1, 3),
            date(2020, 1, 4), date(2020, 1, 5),
        ]
    )

    def test_very_large_year_size(self):
        """Assert trivial year provides equal amortizations."""

        def _do_assert(schedule):
            loan = Loan(
                *self.args_,
                year_size=100000,
                # grace_period=0,
                amortization_schedule=schedule
            )

            assert_almost_equal(
                [250.0, 250.0, 250.0, 250.0],
                loan.amortizations,
                2,
                'Unexpected amortizations for schedule %s'
                % schedule,
            )

            assert_almost_equal(
                [0.0, 0.0, 0.0, 0.0],
                loan.interest_payments,
                2,
                'Unexpected interests for schedule %s'
                % schedule
            )

            assert_almost_equal(
                loan.due_payments,
                loan.amortizations,
                2,
                'Unexpected payments/amortizations for schedule %s'
                % schedule
            )

        for schedule in [
            'progressive_price_schedule',
            'regressive_price_schedule',
            'constant_amortization_schedule',
        ]:

            _do_assert(schedule)

    def test_grace_period_exceeds_loan_start(self):

        for date_ in self.args_[3]:

            with pytest.raises(ValueError):

                Loan(
                    *self.args_,
                    grace_period=(date_ - self.args_[2]).days
                )
