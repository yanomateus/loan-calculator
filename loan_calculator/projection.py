from loan_calculator.grossup.iof import IofGrossup


class Projection(object):
    """Project loan grossup for given projection dates.

    The grossup of a loan is dependent of a reference data, usually interpreted
    as the associated taxable event date
    """

    def __init__(
        self, loan, projection_dates, grossup_type='iof', *args
    ):

        self.loan = loan
        self.projection_dates = projection_dates

        if grossup_type == 'iof':
            self.grossup_cls = IofGrossup
        else:
            raise TypeError('Unknown grossup type.')

        self.projections = [
            self.grossup_cls(loan, reference_date, *args)
            for reference_date in projection_dates
        ]

    @property
    def projected_principals(self):
        for projection in self.projections:
            yield projection.grossed_up_principal

    @property
    def projected_irrs(self):
        for projection in self.projections:
            yield projection.irr
