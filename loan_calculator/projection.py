from loan_calculator.grossup import GrossupType, GROSSUP_TYPE_CLASS_MAP


class Projection(object):
    """Project loan grossup for given projection dates.

    The grossup of a loan is dependent of a reference data, usually interpreted
    as the associated taxable event date
    """

    def __init__(
        self, loan, projection_dates, grossup_type=GrossupType.iof, *args
    ):

        self.loan = loan
        self.projection_dates = projection_dates

        self.grossup_type = GrossupType(grossup_type)
        self.grossup_cls = GROSSUP_TYPE_CLASS_MAP[self.grossup_type]

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
