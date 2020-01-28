from loan_calculator.irr import approximate_irr


class BaseGrossup(object):

    def __init__(self, loan, reference_date, *args):
        """Initialize grossup.

        Parameters
        ----------
        loan : Loan, required
            Loan to be grossed up.
        reference_date : date, required
            Reference used to the gross up evaluation. It is usually the date
            of the associated taxable event.
        args
            Passed as args to grossup implementation.
        """

        self.reference_date = reference_date

        self.loan = loan
        self.grossed_up_loan = getattr(self, 'grossup', loan)(
            loan, reference_date, *args
        )

    def grossup(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def net_principal(self):
        return self.loan.principal

    @property
    def grossed_up_principal(self):
        return self.grossed_up_loan.principal

    @property
    def irr(self):
        return approximate_irr(
            self.net_principal,
            self.grossed_up_loan.due_payments,
            [
                (r_date - self.reference_date).days
                for r_date in self.loan.return_dates
            ]
        )


