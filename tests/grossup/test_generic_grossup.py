from numpy.testing import assert_almost_equal
from loan_calculator.grossup.generic import GenericGrossup
from loan_calculator.grossup.iof import IofGrossup
from loan_calculator.grossup.iof_tax import (
    amortization_schedule_iof, complementary_iof
)
from loan_calculator.grossup.service_fee import linear_service_fee


def test_proper_grossup(loan):

    # this constant function will be used to evaluate the amortizations, the
    # reduced tax, the complementary tax and the service fee. Therefore, the
    # this grossup is expected to increase the principal by $ 30.00
    def f(*args, **kwargs):
        return 10.0

    grossup_ = GenericGrossup(loan, loan.start_date, f, f, f, f)

    assert_almost_equal(grossup_.grossed_up_principal, 130.0, decimal=2)
    assert_almost_equal(grossup_.base_principal, 100.0, decimal=2)

    # expected irr is given by
    # (173.33 + (173.33 ** 2 + 4 * 173.33 * 100.0) ** 0.5) / (2 * 100.0) - 1
    # where 173.33 is the PMT for the grossed up principal of $ 130.00
    assert_almost_equal(grossup_.irr, 1.4428787223382522)


def test_generic_grossup_properly_applies_to_iof_grossup_case(build_loan):

    def _do_assert(loan):

        def amortization_func(principal, daily_interest_rate, return_days):
            return loan.amortization_schedule_cls(
                principal,
                daily_interest_rate,
                return_days
            ).amortizations

        generic_grossup = GenericGrossup(
            loan,
            loan.start_date,
            amortization_func,
            amortization_schedule_iof,
            complementary_iof,
            linear_service_fee
        )

        iof_grossup = IofGrossup(
            loan,
            loan.start_date
        )

        assert_almost_equal(
            generic_grossup.grossed_up_principal,
            iof_grossup.grossed_up_principal,
            decimal=2
        )

    for amortization_schedule_type in [
        'progressive_price_schedule',
        'regressive_price_schedule',
        'constant_amortization_schedule',
    ]:

        _do_assert(build_loan(amortization_schedule_type))
