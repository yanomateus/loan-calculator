import numpy as np

from loan_cashflow_calculator.pmt import constant_return_pmt


# TODO: docstring this class: should provide an overview about the mathematics
#       of amortization schedules
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


class BasePriceSchedule(BaseSchedule):
    """Base class for Price type amortization schedules.

    Price amortization schedules are characterized by the payment value, which
    is the same for all instalments. The distributions of amortization and
    interest in each payment are given by either a increasing or decreasing
    rule over the amortizations. Both are implemented as subclasses of this.
    """

    def __init__(self, principal, daily_interest_rate, return_days):

        super(BasePriceSchedule, self).__init__(
            principal,
            daily_interest_rate,
            return_days
        )

        self.pmt = constant_return_pmt(
            principal,
            daily_interest_rate,
            return_days
        )

        self.due_payments = self.calculate_due_payments()
        self.balance = self.calculate_balance()

        self.interest_payments = getattr(
            self, 'calculate_interest', np.zeros(len(return_days))
        )()

        self.amortizations = getattr(
            self, 'calculate_amortizations', np.zeros(len(return_days))
        )()

    def calculate_balance(self):
        """Calculate the balance after each payment.

        Implements the balance as defined by
        .. math::
            b_i = S(1+d)^{n_i}(1 - \frac{\sum_{j=1}^i\frac{1}{(1+d)^{n_j}}}
                                        {\sum_{j=1}^k\frac{1}{(1+d)^{n_j}}}),
            \mathrm{for}\ i,0\leq i\leq k

        where :math:`S` is the principal, :math:`d` is the daily interest rate
        and :math:`n_1,\ldots,n_k` are the return days.

        This equation can be directly deduced from the recursive definition
        of the balance given by

        .. math::

            b_i =
            \left\{
            \begin{aligned}
                b_{i-1}(1+d)^{n_i-n_{i-1}} - P & \mathrm{se}\ i,1\leq i\leq k \\
                S & \mathrm{se}\ i = 0
            \end{aligned}
            \right.,

        where :math:`P = \mathrm{PMT}(S,d,(n_1,\ldots,n_k))`.
        """

        # variables are renamed to make the math more explicit
        p = self.principal
        d = self.daily_interest_rate
        r_days = self.return_days

        return np.array(
            [
                (p *
                 ((1 + d) ** n) *
                 (1 -
                  sum(1 / (1 + d) ** m for m in r_days if m <= n) /
                  sum(1 / (1 + d) ** m for m in r_days)))
                for n in [0] + r_days
            ],
            dtype=float
        )

    def calculate_due_payments(self):
        """Calculate due payments.

        Since this is a Price schedule, all due payments have the same value.
        """

        return np.array(
            [self.pmt for _ in self.return_days],
            dtype=float
        )


class ProgressivePriceSchedule(BasePriceSchedule):
    """Implement progressive Price amortization schedule.

    The progressive Price amortization schedule, or French amortization system,
    defines a schedule where all instalments have the same value and the
    amortizations and interest are calculated based on the principal, return
    days and daily interest rate.

    The amortizations are defined as the leftover after interest payment, i.e.,
    it is first calculated how much interest should be paid over the last
    balance, and the exceeding payment is used as amortization.

    In this schedule, the amortization values increase over time, hence the name
    progressive.

    If we denote by :math:`P` the instalment value, :math:`S` the principal,
    :math:`d` the daily interest rate, :math:`n_i` the number of days since the
    beginning of the operation until the :math:`i`-th due date, :math:`A_i`
    the :math:`i`-th amortization and :math:`J_i` the :math:`i`-th interest
    paid and :math:`b_i` the balance after the :math:`i`-th payment, then

      - :math:`P=\mathrm{PMT}(S,d,(n_1,\ldots,n_k))`.
      - :math:`b_i = b_{i-1}(1+d)^{n_i-n_{i-1}} - P`.
      - :math:`J_i = P - b_{i-1}((1+d)^{n_i-n_{i-1}}-1)`.
      - :math:`A_i = P - J_i`.
    """

    def calculate_interest(self):
        """Calculate interest in each payment.

        Calculate the interest as defined by

        .. math::

            J_i = \frac{P}{(1+d)^{n_{k-i+1}}},
            \mathrm{for\ all}\ i,1\leq i\leq k,

        where :math:`d` is the daily interest rate, :math:`P` is the PMT,
        and :math:`n_1,\ldots,n_k` are the return days.
        """

        return np.array(
            [
                self.pmt * (1.0 - 1.0 / (1 + self.daily_interest_rate) ** n)
                for n in self.return_days[::-1]
            ],
            dtype=float
        )

    def calculate_amortizations(self):
        """Calculate the principal amortization due to each payment.

        Calculate the principal amortization as defined by

        .. math::

            A_i := \frac{P}{(1+d)^{n_{k-i+1}}},
            \mathrm{for\ all}\ i,1\leq i\leq k,

        where :math:`d` is the daily interest rate, :math:`n_1,\ldots,n_k`
        are the return days and :math:`P = \mathrm{PMT}(S,d,(n_1,\ldots,n_k))`.
        """

        return np.array(
            [
                self.pmt / (1 + self.daily_interest_rate) ** n
                for n in self.return_days[::-1]
            ],
            dtype=float
        )


class RegressivePriceSchedule(BasePriceSchedule):
    """Implement regressive Price amortization schedule.

    The regressive Price amortization schedule defines a schedule where all
    instalments have the same value and the amortization and interest
    distribution is calculated based on the principal, daily interest rate and
    return days.

    The amortizations are defined as the present value of each payment. The
    interest is then defined as the remaining instalment value after
    amortization.

    In this schedule, the amortization values decrease over time, hence the name
    regressive.

    If we denote by :math:`P` the instalment value, :math:`S` the principal,
    :math:`d` the daily interest rate, :math:`n_i` the number of days since the
    beginning of the operation until the :math:`i`-th due date, :math:`A_i`
    the :math:`i`-th amortization and :math:`J_i` the :math:`i`-th interest
    paid and :math:`b_i` the balance after the :math:`i`-th payment, then

      - :math:`P=\mathrm{PMT}(S,d,(n_1,\ldots,n_k))`.
      - :math:`b_i = b_{i-1}(1+d)^{n_i-n_{i-1}} - P`.
      - :math:`A_i = \frac{P}{(1+d)^{n_i}`.
      - :math:`J_i = P - \frac{P}{(1+d)^{n_i}`.
    """

    def calculate_amortizations(self):
        """Calculate the amortization due to each payment.

        The amortization is considered to be the present value of each payment,
        therefore is given by

        .. math::

            A_i := \frac{P}{(1+d)^{n_i}
            \mathrm{for\ all}\ i,1\leq i\leq k,

        where :math:`d` is the daily interest rate, :math:`n_i` is the
        :math:`i`-th return date and
        :math:`P = \mathrm{PMT}(S,d,(n_1,\ldots,n_k)`
        """

        # variables are renamed to make the math more explicit
        d = self.daily_interest_rate

        return np.array(
            [self.pmt / (1 + d) ** n for n in self.return_days],
            dtype=float
        )

    def calculate_interest(self):
        """Calculate the interest in each payment.

        The interest is defined as the leftover after the present value
        of the payment is used as a principal amortization, i.e., defined by

        .. math::

            J_i := P - \frac{P}{(1+d)^{n_i}},
            \mathrm{for\ all}\ i,1\leq i\leq n,

        where :math:`d` is the daily interest rate, :math:`n_i` is the
        :math:`i`-th return date and
        :math:`P = \mathrm{PMT}(S,d,(n_1,\ldots,n_k)`
        """

        pmt = constant_return_pmt(
            self.principal,
            self.daily_interest_rate,
            self.return_days
        )

        # variable is renamed to make the math more explicit
        d = self.daily_interest_rate

        return np.array(
            [pmt * (1 - 1.0 / (1 + d)) ** n for n in self.return_days],
            dtype=float
        )


class ConstantAmortizationSchedule(BaseSchedule):
    """Implement constant amortization schedule.

    The constant amortization schedule is defined as the amortization schedule
    where all the amortizations have the same value, given as
    :math:`\frac{S}{k}`, where :math:`S` is the principal and :math:`k`
    is the number of due payments. Therefore, the due payments do not
    have all the same value, as in the French system, but differ
    according to how much interest was accumulated over time. If
    :math:`d` is the daily interest rate, :math:`P_i` is the :math:`i`-th
    due payment, :math:`A_i` and :math:`J_i` are the associated amortization
    and interest, respectively, and :math:`b_i` is the balance after the
    :math:`i`-th payment, then

      - :math:`A_i = \frac{S}{k}`.
      - :math:`J_i = ((1+d)^{n_i} - (1+d)^{n_{i-1}})
        (S - A \sum_{1\leq j\leq i-1} \frac{1}{(1+d)^{n_j}})`.
      - :math:`P_i = A + J_i`.
      - :math:`b_i = S - iA`.
    """

    def __init__(self, principal, daily_interest_rate, return_days):

        super(ConstantAmortizationSchedule, self).__init__(
            principal,
            daily_interest_rate,
            return_days
        )

        self.balance = self.calculate_balance()
        self.due_payments = self.calculate_due_payments()
        self.interest_payments = self.calculate_interest()
        self.amortizations = self.calculate_amortizations()

    def calculate_balance(self):
        """Calculate the balance after each payment.

        The balance after each payment is given by

        .. math::

            b_i := \frac{S}(1 - \frac{i}{k}),
            \mathrm{for\ all}\ i,0\leq i\leq k,

        where :math:`S` is the principal and :math:`k` is the number of
        instalments.
        """

        k = len(self.return_days)

        return np.array(
            [
                self.principal * (1 - i / k)
                for i in range(k + 1)
            ],
            dtype=float
        )

    def calculate_amortizations(self):
        """Calculate the amortizations by payments.

        Since this is a constant amortization schedule, all amortizations have
        the same value, given by

        .. math::

            A_i := \frac{S}{k},\mathrm{for\ all}\ i,1\leq i\leq k,

        where :math:`S` is the principal and :math:`k` is the number of
        instalments.
        """

        return np.array(
            [
                self.principal / len(self.return_days)
                for _ in self.return_days
            ],
            dtype=float
        )

    def calculate_interest(self):
        """Calculate the interest in each payment.

        The interest is calculated over the last balance and is given by

        .. math::

            J_i := b_{i-1}((1+d)^{n_i-n_{i-1}}-1)
            \mathrm{for\ all}\ i,1\leq i\leq k,

        where :math:`b_{i-1}` is the :math:`(i-1)`-th balance, :math:`d` is the
        daily interest rate and :math:`n_1,\ldots,n_k` are the return days.
        """

        # rename variable to make the math more explicit
        d = self.daily_interest_rate

        return np.array(
            [
                b * ((1 + d) ** (n - m) - 1)
                for b, n, m in zip(self.balance[:-1],
                                   self.return_days,
                                   [0] + self.return_days[:-1])
            ],
            dtype=float
        )

    def calculate_due_payments(self):
        """Calculate the due payments.

        In the constant amortization schedule, the instalment value is not fixed
        as in Price type schedules but depends on how much interest is due
        for each period and the amortization, which is constant. The payments
        are then given by

        .. math::

            P_i = b_{i-1}((1+d)^{n_i-n_{i-1}}-1) + \frac{S}{k},
            \mathrm{for\ all}\ i,1\leq i\leq k,

        where :math:`b_{i-1}` is the :math:`(i-1)`-th balance, :math:`d` is the
        daily interest rate, :math:`S` is the principal and
        :math:`n_1,\ldots,n_k` are the return days.
        """

        # variables are renamed to make the math more explicit
        p = self.principal
        d = self.daily_interest_rate
        k = len(self.return_days)

        return np.array(
            [b * ((1 + d) ** (n - m) - 1) + p / k
             for b, n, m in zip(self.balance[:-1],
                                self.return_days,
                                [0] + self.return_days[:-1])],
            dtype=float
        )

