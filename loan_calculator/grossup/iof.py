from loan_calculator.loan import Loan
from loan_calculator.grossup.base import BaseGrossup
from loan_calculator.grossup.functions import (
    br_iof_regressive_price_grossup,
    br_iof_progressive_price_grossup,
    br_iof_constant_amortization_grossup
)
from loan_calculator.schedule import (
    RegressivePriceSchedule,
    ProgressivePriceSchedule,
    ConstantAmortizationSchedule
)


class IofGrossup(BaseGrossup):
    """Implement grossup based on IOF tax and linear service fee.

    The mathematical model for this grossup is given by

    .. math::

        s -
        \\sum_{i=1}^k A(n_i-n_d,d,s)\\min((n_i-n_d)I^*,1\\frac{1}{2}\\%) -
        sI^{**} - gs = s_\\circ

    where

    *   :math:`s` is the grossed up principal,
    *   :math:`s_\\circ` is the net principal,
    *   :math:`d` is the daily interest rate,
    *   :math:`n_d` is the number of days in the grace period,
    *   :math:`n_i` is the number of days since the contract start,
    *   :math:`A(n_i,n_d,d,s)` is the amortization for the given parameters,
    *   :math:`I^{*}` is the reduced IOF tax aliquot,
    *   :math:`I^{**}` is the complementary IOF tax aliquot, and
    *   :math:`g` is the service fee aliquot.

    Parameters
    ----------
    reference_date : date, required
        The date the loan's net principal is made available.
    daily_iof_aliquot : float, optional
        Reduced IOF tax aliquot. The amortizations are the tax calculation
        basis and the aliquot is incident in proportion to the number of
        days since the taxable event. The IOF taxes over the amortization
        are summed up this aggregated value is the due tax over the
        amortizations. (Default 0.000082)
    complementary_iof_aliquot : float, optional
        Complementary IOF tax aliquot. The tax calculation basis is the
        principal. (Default 0.0038)
    service_fee_aliquot : float, optional
        Aliquot applied over the principal and is meant to model the
        service fee. (Default 0.0)
    """

    def __init__(
        self,
        base_loan,
        reference_date,
        daily_iof_aliquot=0.000082,
        complementary_iof_aliquot=0.0038,
        service_fee_aliquot=0.0
    ):
        """Initialize IOF grossup."""

        super(IofGrossup, self).__init__(
            base_loan,
            reference_date,
            daily_iof_aliquot,
            complementary_iof_aliquot,
            service_fee_aliquot,
        )

    def grossup(
        self,
        loan,
        reference_date,
        daily_iof_aliquot,
        complementary_iof_aliquot,
        service_fee_aliquot,
    ):

        dispatch_table = {
            RegressivePriceSchedule: br_iof_regressive_price_grossup,
            ProgressivePriceSchedule: br_iof_progressive_price_grossup,
            ConstantAmortizationSchedule: br_iof_constant_amortization_grossup,
        }

        return Loan(
            dispatch_table[loan.amortization_schedule_cls](
                loan.principal,
                loan.daily_interest_rate,
                daily_iof_aliquot,
                complementary_iof_aliquot,
                [
                    (r_date - reference_date).days
                    for r_date in loan.return_dates
                ],
                service_fee_aliquot,
            ),
            loan.annual_interest_rate,
            loan.start_date,
            loan.return_dates,
            loan.year_size,
            loan.grace_period,
            loan.amortization_schedule_type
        )
