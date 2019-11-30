import numpy as np


class BaseSchedule:

    def __init__(self, principal, daily_interest_rate, return_days):

        self.principal = principal
        self.daily_interest_rate = daily_interest_rate
        self.return_days = return_days

    @property
    def total_paid(self):
        return np.sum(getattr(self, 'due_payments', 0.0))

    @property
    def total_amortization(self):
        return np.sum(getattr(self, 'amortizations', 0.0))

    @property
    def total_interest(self):
        return np.sum(getattr(self, 'interest_payments', 0.0))
