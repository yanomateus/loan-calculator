from datetime import timedelta

from loan_calculator.schedule import (
    ProgressivePriceSchedule,
    RegressivePriceSchedule,
    ConstantAmortizationSchedule,
)


class Loan(object):

    def __init__(
        self,
        principal,
        annual_interest_rate,
        start_date,
        return_dates,
        year_size=365,
        grace_period=0,
        amortization_schedule='progressive_price_schedule'
    ):
        """Initialize loan.

        Parameters
        ----------
        principal : float, required
            The loan's principal.
        annual_interest_rate : float, required
            The loan's annual interest rate.
        start_date : date, required
            The loan's reference date. This date is usually the one when the
            borrower signed the loan's contract.
        return_dates : list, required
            List of date objects with the expected return dates. These dates
            are usually contractually agreed.
        year_size : int, optional
            The reference year size for converting from annual to daily
            interest rates. (default 365)
        grace_period : int, optional
            The number of days for which the principal is not affected by the
            capitalization process. (default 0)
        amortization_schedule : str, optional
            A discriminator string indicating the amortization schedule to be
            adopted. The available schedules are progressive_price_schedule,
            regressive_price_schedule, constant_amortization_schedule.
            (default progressive_price_schedule).

        """

        self.principal = principal
        self.daily_interest_rate = (
            (1 + annual_interest_rate) ** (1.0 / year_size) - 1
        )

        self.start_date = start_date
        self.capitalization_start_date = (
            start_date + timedelta(grace_period)
        )

        self.return_dates = return_dates

        self.amortization_schedule_discriminator = amortization_schedule

        if amortization_schedule == 'progressive_price_schedule':
            self.amortization_schedule_cls = ProgressivePriceSchedule

        elif amortization_schedule == 'regressive_price_schedule':
            self.amortization_schedule_cls = RegressivePriceSchedule

        elif amortization_schedule == 'constant_amortization_schedule':
            self.amortization_schedule_cls = ConstantAmortizationSchedule

        else:
            raise TypeError('Unknown amortization schedule type.')

        self.amortization_schedule = self.amortization_schedule_cls(
            principal,
            self.daily_interest_rate,
            [
                (r_date - self.capitalization_start_date).days
                for r_date in return_dates
            ]
        )

    @property
    def return_days(self):
        return self.amortization_schedule.return_days

    @property
    def balance(self):
        return self.amortization_schedule.balance

    @property
    def due_payments(self):
        return self.amortization_schedule.due_payments

    @property
    def interest_payments(self):
        return self.amortization_schedule.interest_payments

    @property
    def amortizations(self):
        return self.amortization_schedule.amortizations

    @property
    def total_amortization(self):
        return self.amortization_schedule.total_amortization

    @property
    def total_interest(self):
        return self.amortization_schedule.total_interest

    @property
    def total_paid(self):
        return self.amortization_schedule.total_paid
