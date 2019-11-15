from typing import List


# TODO:properly handle monetary quantities
def br_grossup(
    net_principal: float,
    daily_interest_rate: float,
    daily_iof_fee: float,
    complementary_iof_fee: float,
    return_days: List[int],
    service_fee: float = 0.0,
) -> float:
    """Calculate the grossup of the given principal.

    The grossup of a net principal is an augmented principal value whose net
    value corresponds to the given net principal. The net value of a principal
    is the one obtained after subtracting due taxes and service fees according
    to very specific mathematical rule.

    The grossup operation implemented by this function represents a fairly
    common situation for loan calculations inside Brazilian context, where


    If :math:`S` is the principal, :math:`d` is the daily interest rate,
    :math:`I^*` is the daily IOF fee, :math:`I^{**}` is the complementary IOF
    fee, :math:`g` is the service fee and :math:`(n_1,n_2,\ldots,n_k)` is the
    vector with the return dates, then the grossup is given by

    .. math::
        \mathrm{GROSSUP}\ (S, d, I^*, I^{**}, (n_1,\ldots,n_k), g)\ =
        \frac{S}
        {1
         - \alpha
         - I^{**}
         - g
        },

    where

    .. math::
        \alpha := \frac{\sum_{j=1}^k\frac{min(n_j\ I^*, 0.015)}{(1+d)^{n_j}}}
                       {\sum_{j=1}^k\frac{1}{(1+d)^{n_j}}}.

    Parameters
    ----------
    net_principal : float, required
        The principal to be "grossed up".
    daily_interest_rate : float, required
        The rate at which the principal grows over time.
    daily_iof_fee : float, required
        Daily tax due to brazilian tax IOF.
    complementary_iof_fee : float, required
        Complementary tax due to brazilian tax IOF.
    return_days : list, required
        List containing the number of days since the start reference date.
    service_fee : float, optional
        Eventual service fee. It is assumed to be an aliquot
        applied on the principal


    Returns
    -------
    The grossed up principal.
    """

    # variables are renamed in order to make the math more explicit
    p = net_principal
    d = daily_interest_rate
    d_iof = daily_iof_fee
    c_iof = complementary_iof_fee
    s_fee = service_fee
    pmt_days = return_days

    # TODO:think of a better name for this coefficient
    # transport coefficient
    transport_coef = sum(1.0 / (1 + d) ** n for n in pmt_days)

    # iof coefficient
    iof_coef = sum(float(min(n, 365)) / (1 + d) ** n for n in pmt_days)

    return p / (1 - d_iof * (iof_coef / transport_coef) - c_iof - s_fee)

