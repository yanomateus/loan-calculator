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

    def __init__(
        self,
        base_loan,
        reference_date,
        daily_iof_aliquot=0.000082,
        complementary_iof_aliquot=0.0038,
        service_fee=0.05
    ):

        super(IofGrossup, self).__init__(
            base_loan,
            reference_date,
            daily_iof_aliquot,
            complementary_iof_aliquot,
            service_fee,
        )

    def grossup(
        self,
        loan,
        reference_date,
        daily_iof_aliquot,
        complementary_iof_aliquot,
        service_fee,
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
                service_fee,
            ),
            loan.annual_interest_rate,
            loan.start_date,
            loan.return_dates,
            loan.year_size,
            loan.grace_period,
            loan.amortization_schedule_type
        )
