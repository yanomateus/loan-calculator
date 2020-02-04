from loan_calculator import Loan, GenericGrossup, display_summary
from datetime import date

if __name__ == '__main__':

    loan = Loan(
        10000.00,  # principal
        0.54,  # annual interest rate
        date(2020, 1, 5),  # start date
        [
            date(2020, 2, 12),  # expected return date
            date(2020, 3, 13),  # expected return date
            date(2020, 4, 13),  # expected return date
            date(2020, 5, 12),  # expected return date
            date(2020, 6, 12),  # expected return date
            date(2020, 7, 14),  # expected return date
            date(2020, 8, 15),  # expected return date
            date(2020, 9, 11),  # expected return date
        ],
        year_size=365,  # used to convert between annual and daily interest rates
        grace_period=0,  # number of days for which the principal is not affected by the interest rate
        amortization_schedule_type='progressive_price_schedule',  # determines how the principal is amortized
    )

    def reduced_tax_function(_, r_days):
        tax = 0.0
        for r in r_days:
            tax += r if r <= 200.0 else 200.0
        return tax

    def complementary_tax_function(principal):
        return 0.01 * principal

    def service_fee(_):
        return 20.0

    gup = GenericGrossup(
        loan,
        date(2020, 1, 15),
        reduced_tax_function,
        complementary_tax_function,
        service_fee
    )

    display_summary(gup.grossed_up_loan, gup.reference_date)
