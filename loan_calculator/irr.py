def _solve(target_function, lowerbound, upperbound, allowed_error=0.00000001):
    """Approximate the root of a target function using bisection search.

    Parameters
    ----------

    target_function: callable, required
        Python callable accepting a single numerical argument and returning a
        single numerical valued.
    lowerbound: float, required
        Known lowerbound for a root of the target function.
    upperbound: float, required
        Known upperbound for a root of the target function.
    allowed_error: float, optional
        Maximum allowed error (default is 0.00000001)
    """

    if lowerbound >= upperbound:

        raise ValueError('must be lowerbound < upperbound')

    if target_function(lowerbound) * target_function(upperbound) >= 0:

        raise ValueError(
            'target function values must switch sings at the interval limits'
        )

    current_error_bound = upperbound - lowerbound

    while current_error_bound > allowed_error:

        mid_point = (upperbound + lowerbound) / 2

        if target_function(mid_point) > 0:

            upperbound = mid_point

        else:

            lowerbound = mid_point

        current_error_bound = upperbound - lowerbound

    return lowerbound


def approximate_irr(
    net_principal,
    returns,
    return_days,
    irr_lowerbound=0,
    irr_upperbound=10
):
    """Approximate the internal return rate of a series of returns.

    Use a bisection solver implementation to approximate the irr for the given
    parameters.

    Let :math:`s_\\circ` be a net principal (i.e., a principal with eventual
    taxes and fees properly deduced), :math:`r_1,r_2\\ldots,r_k` a sequence of
    returns and :math:`n_1,n_2,\\ldots,n_k` the due days for these returns. The
    *internal return rate* :math:`c` is then defined as the least positive root
    of the polynomial

    .. math::

        f(X) = s_\\circ X^{n_k} - r_k X^{n_k-n_1} - \\cdots
        - r_2 X^{n_k-n_{k-1}} - r_1

    on the real unknown

    .. math::

        X = 1 + c.

    Parameters
    ----------

    net_principal: float, required
        The principal used as reference to evaluate the irr, i.e., this is the
        amount of money which is, from the perspective of the borrower,
        affected by the irr.
    returns: list, required
        List of expected returns or due payments.
    return_days: list, required
        List of number of days since the loan was granted until each expected
        return.
    irr_lowerbound: float, optional
        Known lowerbound for the irr. If no bound is provided, the trivial
        bound 0 is assumed.
    irr_upperbound: float, optional
        Known upperbound the irr (default 10.)
    """

    r_days = return_days

    coefficients_vec = [net_principal] + [-1 * r for r in returns]

    def return_polynomial(irr_):

        powers_vec = [(1 + irr_) ** (r_days[-1] - n) for n in [0] + r_days]

        return sum(
            coef * power for coef, power in zip(coefficients_vec, powers_vec)
        )

    return _solve(
        return_polynomial, lowerbound=irr_lowerbound, upperbound=irr_upperbound
    )
