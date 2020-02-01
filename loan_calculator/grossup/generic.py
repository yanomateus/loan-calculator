from loan_calculator.grossup.base import BaseGrossup
from loan_calculator.grossup.solver import approximate_grossup
from loan_calculator.loan import Loan


class GenericGrossup(BaseGrossup):

    def __init__(
        self,
        base_loan,
        reference_date,
        amortization_function,
        reduced_tax_function,
        complementary_tax_function,
        service_fee_function,
    ):
        """Initialize GenericGrossup."""

        super(GenericGrossup, self).__init__(
            base_loan,
            reference_date,
            amortization_function,
            reduced_tax_function,
            complementary_tax_function,
            service_fee_function,
        )

    def grossup(
        self,
        loan,
        reference_date,
        amortization_function,
        reduced_tax_function,
        complementary_tax_function,
        service_fee_function
    ):

        return Loan(
            approximate_grossup(
                loan.principal,
                loan.daily_interest_rate,
                [
                    (r_date - reference_date).days
                    for r_date in loan.return_dates
                ],
                amortization_function,
                reduced_tax_function,
                complementary_tax_function,
                service_fee_function
            )[0],
            loan.annual_interest_rate,
            loan.start_date,
            loan.return_dates,
            loan.year_size,
            loan.grace_period,
            loan.amortization_schedule_type
        )