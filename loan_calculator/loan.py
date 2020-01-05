import importlib


class Loan(object):

    def __init__(
        self,
        principal,
        daily_interest_rate,
        start_date,
        return_dates,
        amortization_schedule='progressive_price_schedule'
    ):

        self.principal = principal
        self.daily_interest_rate = daily_interest_rate
        self.start_date = start_date
        self.return_dates = return_dates

        self.amortization_schedule_discriminator = amortization_schedule

        try:
            self.amortization_schedule_cls = getattr(
                importlib.import_module('loan_calculator.schedule'),
                amortization_schedule.title().replace('_', '')
            )
        except AttributeError:
            raise AttributeError('Unknown amortization schedule class.')

        self.amortization_schedule = self.amortization_schedule_cls(
            principal,
            daily_interest_rate,
            [(r_date - start_date).days for r_date in return_dates]
        )

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
