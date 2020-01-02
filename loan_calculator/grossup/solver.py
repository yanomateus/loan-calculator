from scipy.optimize import fsolve


def approximate_grossup(
    net_principal,
    daily_interest_rate,
    return_days,
    amortization_function,
    reduced_tax_function,
    reduced_aliquot,
    complementary_tax_function,
    complementary_aliquot,
    service_fee_function,
    service_fee_aliquot,
    *args,
    **kwargs
):
    """Approximate the grossup given tax and fee functions.

    Wrap around scipy.optimize.fsolve to find a zero of a residue function,
    which is evaluated as the difference between a grossed up principal and the
    net principal.

    Given

    *   :math:`a = (a_1,\\ldots,a_k)` a vector of amortizations,
    *   :math:`r = (n_1,\\ldots,n_k)` a vector of return days,
    *   :math:`\\alpha` a daily aliquot for the tax over the amortizations,
    *   :math:`f = f(a,r,\\alpha)` a mathematical function evaluating the tax
        over the amortizations,
    *   :math:`s` the principal,
    *   :math:`\\beta` an aliquot for the tax over the principal,
    *   :math:`c = c(s,\\beta)` a mathematical function evaluating the tax
        over the principal,,
    *   :math:`\\gamma` an aliquot for the service fee over the principal,
    *   :math:`g = g(s,\\gamma)` a mathematical function evaluating the
        service fee over the principal,

    the *residue function* is then defined as

    .. math::

        \\Delta_{s_\\circ,a,\\alpha,\\beta,\\gamma,r} (s) :=
        s_\\circ - (s - f(a,r,\\alpha) - c(s,\\beta) - g(s,\\gamma)).

    Thus, the grossed up principal :math:`s` is approximated as a zero of the
    residue function.

    Parameters
    ----------
    net_principal: float, required
        Is the expected net value for the grossed up principal.
    daily_interest_rate: float, required
        The loan's daily interest rate.
    amortization_function: list, required
        List of expected amortizations.
    return_days: list, required
        List of return days, where returns are expected to be performed.
    reduced_tax_function: Callable, required
        A callable implementing the signature

        ::

            f(amortizations: list, return_days: list, daily_aliquot) -> float

    reduced_aliquot: float, required
        The aliquot to be used by the `reduced_tax_function`.
    complementary_tax_function: Callable, required
        A callable implementing the signature
        ::
            c(principal: float, complementary_aliquot: float) -> float
    complementary_aliquot: float, required
        Complementary aliquot to be used by `complementary_tax_function`.
    service_fee_function: Callable, required
        A callable implementing the signature
        ::
            g(principal: float, service_fee_aliquot: float) -> float
    service_fee_aliquot: float, required
        The aliquot to be used by `service_fee_function`.
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
    r_alq = reduced_aliquot
    c_tax_f = complementary_tax_function
    c_alq = complementary_aliquot
    fee_f = service_fee_function
    s_alq = service_fee_aliquot

    def residue_function(s):

        return (p -
                r_tax_f(a(s, d, r_days), r_days, r_alq) -
                c_tax_f(s, c_alq) -
                fee_f(s, s_alq))

    return fsolve(residue_function, p, *args, **kwargs)
