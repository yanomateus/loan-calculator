from loan_calculator.irr import approximate_irr


class BaseGrossup(object):
    """Base class for grossup implementations."""

    def __init__(self, base_loan, reference_date, *args):
        """Initialize grossup.

        Parameters
        ----------
        base_loan : Loan, required
            Loan to be grossed up.
        reference_date : date, required
            Reference used to the gross up evaluation. It is usually the date
            of the associated taxable event.
        args
            Passed as args to grossup implementation.
        """

        self.reference_date = reference_date

        self.base_loan = base_loan
        self.grossed_up_loan = getattr(self, 'grossup', base_loan)(
            base_loan, reference_date, *args
        )

    def grossup(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def base_principal(self):
        """Principal of the base loan."""
        return self.base_loan.principal

    @property
    def grossed_up_principal(self):
        """Principal of the grossed up loan."""
        return self.grossed_up_loan.principal

    @property
    def irr(self):
        """The IRR affecting the net principal."""
        return approximate_irr(
            self.base_principal,
            self.grossed_up_loan.due_payments,
            [
                (r_date - self.reference_date).days
                for r_date in self.base_loan.return_dates
            ]
        )
