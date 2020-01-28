from loan_calculator.grossup.base import BaseGrossup
from loan_calculator.grossup.functions import br_iof_regressive_price_grossup, br_iof_progressive_price_grossup, \
    br_iof_constant_amortization_grossup
from loan_calculator.loan import Loan
from loan_calculator.schedule import RegressivePriceSchedule, ProgressivePriceSchedule, ConstantAmortizationSchedule


class IofGrossup(BaseGrossup):

    def __init__(
        self,
        loan,
        reference_date,
        daily_iof_aliquot=0.000082,
        complementary_iof_aliquot=0.0038,
        service_fee=0.05
    ):

        super(BaseGrossup, self).__init__(
            loan,
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

        if loan.amortization_schedule_cls is RegressivePriceSchedule:
            grossup_function = br_iof_regressive_price_grossup

        elif loan.amortization_schedule_cls is ProgressivePriceSchedule:
            grossup_function = br_iof_progressive_price_grossup

        elif loan.amortization_schedule_cls is ConstantAmortizationSchedule:
            grossup_function = br_iof_constant_amortization_grossup

        else:
            raise ValueError(
                'Unknown amortization schedule class {}.'
                .format(loan.amortization_schedule_cls.__name__)
            )

        return Loan(
            grossup_function(
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
            loan.daily_interest_rate, loan.start_date, loan.return_dates,
        )
