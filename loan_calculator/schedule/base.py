import numpy as np


class BaseSchedule(object):
    """Base amortization schedule"""

    def __init__(self, principal, daily_interest_rate, return_days):
        """Initialize schedule.

        Parameters
        ----------
        principal: float, required
            Loan's principal.
        daily_interest_rate: float, required
            Loan's daily interest rate.
        return_days: list, required
            List of integers representing the number of days since the loan
            was granted until the payments' due dates.
        """

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
