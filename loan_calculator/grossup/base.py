from loan_calculator.grossup.solver import approximate_grossup
from loan_calculator.loan import Loan
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


class Grossup(object):

    def __init__(self, loan):
        self.loan = loan

    @property
    def net_principal(self):
        return self.loan.principal


class GenericGrossup(Grossup):

    def __init__(
        self,
        loan,
        amortization_function,
        reduced_tax_function,
        reduced_aliquot,
        complementary_tax_function,
        complementary_aliquot,
        service_fee_function,
        service_fee_aliquot,
    ):

        super(Grossup, self).__init__(loan)

        grossed_up_principal = approximate_grossup(
            self.net_principal,
            loan.daily_interest_rate,
            [(r_date - loan.start_date).days for r_date in loan.return_dates],
            amortization_function,
            reduced_tax_function,
            reduced_aliquot,
            complementary_tax_function,
            complementary_aliquot,
            service_fee_function,
            service_fee_aliquot
        )[0]

        self.grossed_up_loan = Loan(
            grossed_up_principal,
            loan.daily_interest_rate,
            loan.start_date,
            loan.return_dates,
            loan.amortization_schedule_discriminator
        )


class IofGrossup(Grossup):

    def __init__(
        self,
        loan,
        daily_iof_aliquot=0.000082,
        complementary_iof_aliquot=0.0038,
        service_fee=0.05
    ):

        super(Grossup, self).__init__(loan)

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

        grossed_up_principal = grossup_function(
            loan.principal,
            loan.daily_interest_rate,
            daily_iof_aliquot,
            complementary_iof_aliquot,
            [(r_date - loan.start_date).days for r_date in loan.return_dates],
            service_fee
        )

        self.grossed_up_loan = Loan(
            grossed_up_principal,
            loan.daily_interest_rate,
            loan.start_date,
            loan.return_dates,
        )
