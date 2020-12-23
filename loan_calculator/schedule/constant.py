from loan_calculator.schedule.base import (
    BaseSchedule, AmortizationScheduleType
)


class ConstantAmortizationSchedule(BaseSchedule):
    """Implement constant amortization schedule.

    The constant amortization schedule is defined as the amortization schedule
    where all the amortizations have the same value, given as
    :math:`s/k`, where :math:`s` is the principal and :math:`k`
    is the number of due payments. Therefore, the due payments do not
    have all the same value, as in the French system, but differ
    according to how much interest was accumulated over time. If
    :math:`d` is the daily interest rate, :math:`P_i` is the :math:`i`-th
    due payment, :math:`A_i` and :math:`J_i` are the associated amortization
    and interest, respectively, and :math:`b_i` is the balance after the
    :math:`i`-th payment, then

    - :math:`A_i = \\frac{s}{k}`.
    - :math:`J_i = ((1+d)^{n_i} - (1+d)^{n_{i-1}})
      (s - A\\displaystyle\\sum_{1\\leq j\\leq i-1}\\frac{1}{(1+d)^{n_j}})`.
    - :math:`P_i = A + J_i`.
    - :math:`b_i = s - iA`.
    """

    schedule_type = AmortizationScheduleType.constant_amortization_schedule

    def calculate_balance(self):
        """Calculate the balance after each payment.

        The balance after each payment is given by

        .. math::

            b_i := s(1 - \\frac{i}{k}),
            \\ \\mathrm{for\\ all}\\ i,0\\leq i\\leq k,

        where :math:`s` is the principal and :math:`k` is the number of
        instalments.
        """

        k = len(self.return_days)

        return [self.principal * (1 - float(i) / k) for i in range(k + 1)]

    def calculate_amortizations(self):
        """Calculate the amortizations by payments.

        Since this is a constant amortization schedule, all amortizations have
        the same value, given by

        .. math::

            A_i := \\frac{s}{k},\\mathrm{for\\ all}\\ i,1\\leq i\\leq k,

        where :math:`s` is the principal and :math:`k` is the number of
        instalments.
        """

        return [
            self.principal / len(self.return_days)
            for _ in self.return_days
        ]

    def calculate_interest(self):
        """Calculate the interest in each payment.

        The interest is calculated over the last balance and is given by

        .. math::

            J_i := b_{i-1}((1+d)^{n_i-n_{i-1}}-1)
            \\ \\mathrm{for\\ all}\\ i,1\\leq i\\leq k,

        where :math:`b_{i-1}` is the :math:`(i-1)`-th balance, :math:`d` is the
        daily interest rate and :math:`n_1,\\ldots,n_k` are the return days.
        """

        # rename variable to make the math more explicit
        d = self.daily_interest_rate

        return [
            b * ((1 + d) ** (n - m) - 1)
            for b, n, m in zip(self.balance[:-1],
                               self.return_days,
                               [0] + self.return_days[:-1])
        ]

    def calculate_due_payments(self):
        """Calculate the due payments.

        In the constant amortization schedule, the instalment value is not
        fixed as in Price type schedules but depends on how much interest is
        due for each period and the amortization, which is constant. The
        payments are then given by

        .. math::

            P_i = b_{i-1}((1+d)^{n_i-n_{i-1}}-1) + \\frac{S}{k},
            \\ \\mathrm{for\\ all}\\ i,1\\leq i\\leq k,

        where :math:`b_{i-1}` is the :math:`(i-1)`-th balance, :math:`d` is the
        daily interest rate, :math:`S` is the principal and
        :math:`n_1,\\ldots,n_k` are the return days.
        """

        # variables are renamed to make the math more explicit
        p = self.principal
        d = self.daily_interest_rate
        k = len(self.return_days)

        return [
            b * ((1 + d) ** (n - m) - 1) + p / k
            for b, n, m in zip(
                self.balance[:-1],
                self.return_days, [0] + self.return_days[:-1]
            )
        ]
