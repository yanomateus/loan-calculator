

def constant_return_pmt(principal, daily_interest_rate, return_days):
    """Calculate the PMT (payment value) for the given parameters.

    If :math:`s` is the principal, :math:`d` is the daily interest rate and
    :math:`(n_1,\\ldots,n_k)` is the vector with the number of days since the
    start reference date, then the PMT is given by

    .. math::

        \\mathrm{PMT}\\ (s, d, (n_1,\\ldots,n_k)) =
        \\frac{s}{\\sum\\frac{1}{(1+d)^{n_j}}},

    where the sum is taken for :math:`j,1\\leq j\\leq k`.

    Parameters
    ----------
    principal : float, required
        The value which should be fully paid by consecutive payments with value
        returned by this function.
    daily_interest_rate : float, required
        The daily rate at which the principal grows over time.
    return_days : list, required
        List of integers representing the numbers of days since the start
        reference date.

    Returns
    -------
    The required payment value for the given parameters.
    """

    # variables are renamed in order to make the math more explicit
    p = principal
    d = daily_interest_rate

    return p / sum(1.0 / (1 + d) ** n for n in return_days)
