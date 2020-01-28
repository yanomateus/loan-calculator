from loan_calculator.grossup.iof import IofGrossup
from loan_calculator.grossup.generic import GenericGrossup


class Projection(object):

    def __init__(
        self, loan, projection_dates, grossup_type='generic', *args
    ):

        self.loan = loan
        self.projection_dates = projection_dates

        if grossup_type == 'generic':
            self.grossup_cls = GenericGrossup

        elif grossup_type == 'iof':
            self.grossup_cls = IofGrossup

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
