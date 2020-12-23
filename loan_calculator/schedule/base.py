from enum import Enum


class AmortizationScheduleType(Enum):

    progressive_price_schedule = 'progressive-price-schedule'
    regressive_price_schedule = 'regressive-price-schedule'
    constant_amortization_schedule = 'constant-amortization-schedule'


class BaseSchedule(object):
    """Base amortization schedule.

    Specific amortization schedules should subclass this class and implement
    the methods

    *   `calculate_due_payments`
    *   `calculate_balance`
    *   `calculate_interest_payments`
    *   `calculate_amortizations`

    These methods do not receive any parameters and should be able to return
    based only on principal, daily_interest_rate and return_days.

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

    schedule_type = None

    def __init__(self, principal, daily_interest_rate, return_days):
        """Initialize schedule."""

        self.principal = principal
        self.daily_interest_rate = daily_interest_rate
        self.return_days = return_days

        self.balance = getattr(
            self, 'calculate_balance', (len(return_days) + 1) * [0]
        )()

        self.due_payments = getattr(
            self, 'calculate_due_payments', len(return_days) * [0]
        )()

        self.interest_payments = getattr(
            self, 'calculate_interest', len(return_days) * [0]
        )()

        self.amortizations = getattr(
            self, 'calculate_amortizations', len(return_days) * [0]
        )()

    def calculate_due_payments(self):
        raise NotImplementedError  # pragma: nocover

    def calculate_balance(self):
        raise NotImplementedError  # pragma: nocover

    def calculate_interest_payments(self):
        raise NotImplementedError  # pragma: nocover

    def calculate_amortizations(self):
        raise NotImplementedError  # pragma: nocover

    @property
    def total_paid(self):
        return sum(getattr(self, 'due_payments', 0.0))

    @property
    def total_amortization(self):
        return sum(getattr(self, 'amortizations', 0.0))

    @property
    def total_interest(self):
        return sum(getattr(self, 'interest_payments', 0.0))
