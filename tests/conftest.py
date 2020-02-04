from datetime import date

from pytest import fixture

from loan_calculator.loan import Loan


@fixture()
def loan():
    return Loan(
        100.0,
        1.0,
        date(2020, 1, 1),
        year_size=1,
        return_dates=[date(2020, 1, 2), date(2020, 1, 3)]
    )


@fixture()
def build_loan():

    def _build_loan(amortization_schedule_type):

        return Loan(
            100.0,
            1.0,
            date(2020, 1, 1),
            year_size=1,
            return_dates=[date(2020, 1, 2), date(2020, 1, 3)],
            amortization_schedule_type=amortization_schedule_type
        )

    return _build_loan
