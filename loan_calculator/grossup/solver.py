from scipy.optimize import fsolve


def approximate_grossup(
    net_principal,
    daily_interest_rate,
    return_days,
    amortization_schedule_cls,
    reduced_tax_function,
    reduced_aliquot,
    complementary_tax_function,
    complementary_aliquot,
    service_fee_function,
    service_fee_aliquot,
):
    """Approximate the grossup for given tax and fee functions.

    Wrap around scipy.optimize.fsolve to find a zero of a residue function,
    which is evaluated as the difference between a grossed up principal and the
    net principal.

    Let :math:`S_\\circ` be target net principal, :math:`\\mathcal{A}` be an
    amortization class, :math:`d` the daily interest rate,
    :math:`n_1,n_2,\\ldots,n_k` the return days, :math:`I^*` a
    reduced aliquot which quantifies the tax over the amortization schedule,
    :math:`I^{**}` a complementary aliquot quantifying the tax over the
    principal and :math:`\\sigma` an aliquot over the principal, quantifying
    the service fee.

    Given

    *   :math:`A = \\mathcal{A}(S, (n_1,\\ldots,n_k), d)` an amortization
        schedule,
    *   :math:`f = f_{I^{*}} (A)` a mathematical function evaluating the tax over
        the amortization schedule,
    *   :math:`c = c_{I^{**}}(S)` a mathematical function evaluating the tax
        over the principal,
    *   :math:`g = g_{\\sigma}(S)` a mathematical function evaluating the
        service fee over the principal,

    the *residue function* is then defined as

    .. math::

        \\Delta_{S_\\circ,A,I^*,I^{**},\\sigma} (S) :=
        S_\circ - (S - f_{I^*}(A) - c_{I^{**}}(S) - g_\\sigma (S)).

    Thus, the grossed up principal :math:`S` is approximated as a zero of the
    residue function.

    Parameters
    ----------
    net_principal: float, required
        Is the expected net value for the grossed up principal.
    daily_interest_rate: float, required
        The loan's daily interest rate.
    return_days: list, required
        List of return days, where returns are expected to be performed.
    amortization_schedule_cls: BaseSchedule, required
        Amortization schedule class. Must be a subclass of BaseSchedule,
        since its constructor's interface is assumed, or be a class implementing
        the same interface.
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

    """

    # variables are renamed to make the math more explicit
    p = net_principal
    d = daily_interest_rate
    r_days = return_days
    a_cls = amortization_schedule_cls
    r_tax_f = reduced_tax_function
    r_alq = reduced_aliquot
    c_tax_f = complementary_tax_function
    c_alq = complementary_aliquot
    fee_f = service_fee_function
    s_alq = service_fee_aliquot

    def residue_function(s):

        return (p -
                r_tax_f(a_cls(s, d, r_days).amortizations, r_days, r_alq) -
                c_tax_f(s, c_alq) -
                fee_f(s, s_alq))

    return fsolve(residue_function, p)[0]
