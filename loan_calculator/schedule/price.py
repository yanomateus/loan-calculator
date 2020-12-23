from loan_calculator.pmt import constant_return_pmt
from loan_calculator.schedule.base import (
    BaseSchedule, AmortizationScheduleType
)


class BasePriceSchedule(BaseSchedule):
    """Base class for Price type amortization schedules.

    Price amortization schedules are characterized by the payment value, which
    is the same for all instalments. The distributions of amortization and
    interest in each payment are given by either a increasing or decreasing
    rule over the amortizations. Both are implemented as subclasses of this.
    """

    def __init__(self, principal, daily_interest_rate, return_days):

        self.pmt = constant_return_pmt(
            principal,
            daily_interest_rate,
            return_days
        )

        super(BasePriceSchedule, self).__init__(
            principal,
            daily_interest_rate,
            return_days
        )

    def calculate_balance(self):
        """Calculate the balance after each payment.

        Implements the balance as defined by

        .. math::

            b_i := s(1+d)^{n_i}(1 - \\frac{\\sum_{j=1}^i\\frac{1}{(1+d)^{n_j}}}
                                        {\\sum_{j=1}^k\\frac{1}{(1+d)^{n_j}}}),
            \\mathrm{for}\\ i,0\\leq i\\leq k

        where :math:`s` is the principal, :math:`d` is the daily interest rate
        and :math:`n_1,\\ldots,n_k` are the return days.

        This equation can be directly deduced from the recursive definition
        of the balance given by

        .. math::

            b_i =
            \\left\\{
            \\begin{aligned}
                b_{i-1}(1+d)^{n_i-n_{i-1}} - P,
                &\\ \\mathrm{if}\\ i,1\\leq i\\leq k \\\\
                s, &\\ \\mathrm{if}\\ i = 0
            \\end{aligned}
            \\right.,

        where :math:`P = \\mathrm{PMT}(s,d,(n_1,\\ldots,n_k))`.
        """

        # variables are renamed to make the math more explicit
        p = self.principal
        d = self.daily_interest_rate
        r_days = self.return_days

        return [
            (p *
             ((1 + d) ** n) *
             (1 -
              sum(1 / (1 + d) ** m for m in r_days if m <= n) /
              sum(1 / (1 + d) ** m for m in r_days)))
            for n in [0] + r_days
        ]

    def calculate_due_payments(self):
        """Calculate due payments.

        Since this is a Price schedule, all due payments have the same value.
        """

        return [self.pmt for _ in self.return_days]


class ProgressivePriceSchedule(BasePriceSchedule):
    """Implement progressive Price amortization schedule.

    The progressive Price amortization schedule, or French amortization system,
    defines a schedule where all instalments have the same value and the
    amortizations and interest are calculated based on the principal, return
    days and daily interest rate.

    The amortizations are defined as the leftover after interest payment, i.e.,
    it is first calculated how much interest should be paid over the last
    balance, and the exceeding payment is used as amortization.

    In this schedule, the amortization values increase over time, hence the
    name progressive.

    If we denote by :math:`P` the instalment value, :math:`s` the principal,
    :math:`d` the daily interest rate, :math:`n_i` the number of days since the
    beginning of the operation until the :math:`i`-th due date, :math:`A_i`
    the :math:`i`-th amortization and :math:`J_i` the :math:`i`-th interest
    paid and :math:`b_i` the balance after the :math:`i`-th payment, then

      - :math:`P=\\mathrm{PMT}(s,d,(n_1,\\ldots,n_k))`.
      - :math:`b_i = b_{i-1}(1+d)^{n_i-n_{i-1}} - P`.
      - :math:`J_i = P - b_{i-1}((1+d)^{n_i-n_{i-1}}-1)`.
      - :math:`A_i = P - J_i`.
    """

    schedule_type = AmortizationScheduleType.progressive_price_schedule

    def calculate_interest(self):
        """Calculate interest in each payment.

        Calculate the interest as defined by

        .. math::

            J_i = \\frac{P}{(1+d)^{n_{k-i+1}}},
            \\mathrm{for\\ all}\\ i,1\\leq i\\leq k,

        where :math:`d` is the daily interest rate, :math:`P` is the PMT,
        and :math:`n_1,\\ldots,n_k` are the return days.
        """

        return [
            self.pmt * (1.0 - 1.0 / (1 + self.daily_interest_rate) ** n)
            for n in self.return_days[::-1]
        ]

    def calculate_amortizations(self):
        """Calculate the principal amortization due to each payment.

        Calculate the principal amortization as defined by

        .. math::

            A_i := \\frac{P}{(1+d)^{n_{k-i+1}}},
            \\mathrm{for\\ all}\\ i,1\\leq i\\leq k,

        where :math:`d` is the daily interest rate, :math:`n_1,\\ldots,n_k`
        are the return days and :math:`P=\\mathrm{PMT}(s,d,(n_1,\\ldots,n_k))`.
        """

        return [
            self.pmt / (1 + self.daily_interest_rate) ** n
            for n in self.return_days[::-1]
        ]


class RegressivePriceSchedule(BasePriceSchedule):
    """Implement regressive Price amortization schedule.

    The regressive Price amortization schedule defines a schedule where all
    instalments have the same value and the amortization and interest
    distribution is calculated based on the principal, daily interest rate and
    return days.

    The amortizations are defined as the present value of each payment. The
    interest is then defined as the remaining instalment value after
    amortization.

    In this schedule, the amortization values decrease over time, hence the
    name regressive.

    If we denote by :math:`P` the instalment value, :math:`S` the principal,
    :math:`d` the daily interest rate, :math:`n_i` the number of days since the
    beginning of the operation until the :math:`i`-th due date, :math:`A_i`
    the :math:`i`-th amortization and :math:`J_i` the :math:`i`-th interest
    paid and :math:`b_i` the balance after the :math:`i`-th payment, then

      - :math:`P=\\mathrm{PMT}(s,d,(n_1,\\ldots,n_k))`.
      - :math:`b_i = b_{i-1}(1+d)^{n_i-n_{i-1}} - P`.
      - :math:`A_i = \\displaystyle\\frac{P}{(1+d)^{n_i}}`.
      - :math:`J_i = P(1 - \\displaystyle\\frac{P}{(1+d)^{n_i}})`.
    """

    schedule_type = AmortizationScheduleType.regressive_price_schedule

    def calculate_amortizations(self):
        """Calculate the amortization due to each payment.

        The amortization is considered to be the present value of each payment,
        therefore is given by

        .. math::

            A_i := \\frac{P}{(1+d)^{n_i}}
            \\ \\mathrm{for\\ all}\\ i,1\\leq i\\leq k,

        where :math:`d` is the daily interest rate, :math:`n_i` is the
        :math:`i`-th return date and
        :math:`P = \\mathrm{PMT}(s,d,(n_1,\\ldots,n_k))`
        """

        return [
            self.pmt / (1 + self.daily_interest_rate) ** n
            for n in self.return_days
        ]

    def calculate_interest(self):
        """Calculate the interest in each payment.

        The interest is defined as the leftover after the present value
        of the payment is used as a principal amortization, i.e., defined by

        .. math::

            J_i := P (1-\\frac{1}{(1+d)^{n_i}}),
            \\mathrm{for\\ all}\\ i,1\\leq i\\leq n,

        where :math:`d` is the daily interest rate, :math:`n_i` is the
        :math:`i`-th return date and
        :math:`P = \\mathrm{PMT}(s,d,(n_1,\\ldots,n_k))`
        """

        return [
            self.pmt * (1 - 1.0 / (1 + self.daily_interest_rate) ** n)
            for n in self.return_days
        ]
