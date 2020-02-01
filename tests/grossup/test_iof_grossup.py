from numpy.testing import assert_almost_equal

from loan_calculator.grossup.iof import IofGrossup


def test_trivial_iof_grossup(loan):

    iof_grossup = IofGrossup(
        loan,
        loan.start_date,
        daily_iof_aliquot=0.0,
        complementary_iof_aliquot=0.0
        # service_fee_aliquot=0.0
    )

    assert_almost_equal(
        iof_grossup.grossed_up_principal, loan.principal, decimal=2
    )

    # In a trivial grossup, the IRR should be equal to the daily interest rate
    assert_almost_equal(
        iof_grossup.irr, iof_grossup.base_loan.daily_interest_rate
    )
