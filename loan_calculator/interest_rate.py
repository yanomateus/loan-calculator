from enum import Enum

from loan_calculator import YearSizeType


class InterestRateType(Enum):
    daily = 'daily'
    annual = 'annual'
    semiannual = 'semiannual'
    monthly = 'monthly'
    quarterly = 'quarterly'


def convert_to_daily_interest_rate(
    interest_rate_aliquot,
    interest_rate_type=InterestRateType.daily,
    year_size=YearSizeType.commercial
):
    """"Convert aliquots from a given rate to a daily interest rate.

    This function will convert an aliquot from a given rate (as in
    InterestRateType) to a daily interest rate, since "a day" is the default
    unit time adopted for financial modelling in this library. It is also
    important to note that the proper conversion of rates depends on the
    size of a year in days.

    Parameters
    ----------
    interest_rate_aliquot: float, required
        Aliquot to be converted to a daily interest rate aliquot.
    interest_rate_type: InterestRateType, optional
        The type of rate in which the input aliquot is capitalized
        (default: InterestRateType.daily).
    year_size: YearSizeType, optional
        A year size is necessary since monthly, quarterly and semiannual
        rates are relative to an annum (default YearSizeType.commercial).

    Returns
    -------
    float
        Aliquot as a daily interest rate.

    Raises
    ------
    TypeError
        If the interest_rate_type is none one of the enumerated in
        InterestRateType.
    """
    if interest_rate_type == InterestRateType.daily:
        return interest_rate_aliquot
    elif interest_rate_type == InterestRateType.annual:
        # 1 + a = (1 + d)^365 => d = (1 + a)^(1/365) - 1
        return (1 + interest_rate_aliquot) ** (1 / year_size.value) - 1
    elif interest_rate_type == InterestRateType.semiannual:
        # (1 + s)^2 = (1 + d)^365 => d = (1 + s)^(2/365) - 1
        return (1 + interest_rate_aliquot) ** (2 / year_size.value) - 1
    elif interest_rate_type == InterestRateType.monthly:
        # (1 + m)^12 = (1 + d)^365 => d = (1 + m)^(12/365) - 1
        return (1 + interest_rate_aliquot) ** (12 / year_size.value) - 1
    elif interest_rate_type == InterestRateType.quarterly:
        # (1 + q)^4 = (1 + d)^365 => d = (1 + q)^(4/365) - 1
        return (1 + interest_rate_aliquot) ** (4 / year_size.value) - 1
    else:
        raise TypeError('Unknown interest rate type')
