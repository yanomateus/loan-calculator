from scipy.optimize import fsolve


def approximate_grossup(
    net_principal,
    daily_interest_rate,
    return_days,
    amortization_function,
    reduced_tax_function,
    complementary_tax_function,
    service_fee_function,
    *args,
    **kwargs
):
    """Approximate the grossup given tax and fee functions.

    Wrap around scipy.optimize.fsolve to find a zero of a residue function,
    which is evaluated as the difference between a grossed up principal and the
    net principal.

    Given

    *   :math:`s` the principal,
    *   :math:`d` the daily interest rate,
    *   :math:`r = (n_1,\\ldots,n_k)` a vector of return days,
    *   :math:`a = a(s, d, r)` a mathematical function evaluating the vector
        of amortizations,
    *   :math:`f = f(a,r)` a mathematical function evaluating the tax over the
        amortizations,
    *   :math:`c = c(s)` a mathematical function evaluating the tax over the
        principal,
    *   :math:`g = g(s)` a mathematical function evaluating the service fee
        over the principal,

    the *residue function* is then defined as

    .. math::

        \\Delta_{s_\\circ,r,a,f,c,g} (s) :=
        s_\\circ - (s - f(a,r) - c(s) - g(s)).

    Thus, the grossed up principal :math:`s` is approximated as a zero of the
    residue function.

    Parameters
    ----------
    net_principal: float, required
        Is the expected net value for the grossed up principal.
    daily_interest_rate: float, required
        The loan's daily interest rate.
    amortization_function: list, required
        A callable implementing the signature
        ::
            a(float: principal, return_days: list, daily_aliquot)
            -> list[float]
    return_days: list, required
        List of return days, where returns are expected to be performed.
    reduced_tax_function: Callable, required
        A callable implementing the signature
        ::
            f(amortizations: list, return_days: list, daily_aliquot) -> float
    complementary_tax_function: Callable, required
        A callable implementing the signature
        ::
            c(principal: float, complementary_aliquot: float) -> float
    service_fee_function: Callable, required
        A callable implementing the signature
        ::
            g(principal: float, service_fee_aliquot: float) -> float
    args: list, optional
        Passed as optional positional arguments to scipy's `fsolve`.
    kwargs: dict, optional
        Passed as optional keyword arguments to scipy's `fsolve`.

    """

    # variables are renamed to make the math more explicit
    p = net_principal
    d = daily_interest_rate
    r_days = return_days
    a = amortization_function
    r_tax_f = reduced_tax_function
    c_tax_f = complementary_tax_function
    fee_f = service_fee_function

    def residue_function(s):

        return (s -
                r_tax_f(a(s, d, r_days), r_days) -
                c_tax_f(s) -
                fee_f(s) -
                p)

    return fsolve(residue_function, p, *args, **kwargs)
