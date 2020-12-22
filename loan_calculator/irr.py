def newton_raphson_solver(
    target_function,
    target_function_derivative,
    initial_point,
    maximum_relative_error=0.0000000001,
    max_iterations=100,
):
    """Numerical solver based on Newton-Raphson approximation method.

    The Newton-Raphson method allows algorithmic approximation for the root
    of a differentiable function, given its derivative and an initial point at
    which this derivative does not vanish.

    Let :math:`f:\\left[a,b\\right]\\longrightarrow\\mathbb{R}` a
    differentiable function, :math:`f^{\\prime}` its derivative function and
    :math:`x_0\\in\\left[a,b\\right]`. A root of :math:`f` is then iteratively
    approximated by the recurrence

    .. math::

        x_n := x_{n-1} - \\frac{f(x_{n-1})}{f^{\\prime}(x_{n-1})}, n\\geq 1.

    The *relative error* associated with the :math:`n`-th iteration of the
    recurrence above is defined as

    .. math::

        e_n := | \\frac{x_n - x_{n-1}}{x_{n-1}} |, n \\geq 1.

    The approximation stops if either :math:`e_n` > `maximum_relative_error`
    or :math:`n` > `max_iterations`.
    """

    def _iterating_function(x):
        return x - target_function(x) / target_function_derivative(x)

    def _error_function(reference_point, new_point):
        return abs((new_point - reference_point) / reference_point)

    past_point = initial_point
    iterating_point = _iterating_function(past_point)

    relative_error = _error_function(past_point, iterating_point)

    num_iterations = 1

    while (
        relative_error >= maximum_relative_error and
        num_iterations < max_iterations
    ):

        past_point, iterating_point = (
            iterating_point, _iterating_function(iterating_point)
        )
        relative_error = _error_function(past_point, iterating_point)

        num_iterations += 1

    return iterating_point


def approximate_irr(
    net_principal,
    returns,
    return_days,
    daily_interest_rate,
):
    """Approximate the internal return rate of a series of returns.

    Use a Newton-Raphson solver implementation to approximate the IRR for the
    given loan parameters.

    Let :math:`s_\\circ` be a net principal (i.e., a principal with eventual
    taxes and fees properly deduced), :math:`r_1,r_2\\ldots,r_k` a sequence of
    returns and :math:`n_1,n_2,\\ldots,n_k` the due days for these returns. The
    *internal return rate* :math:`c` is then defined as the least positive root
    of the polynomial

    .. math::

        f(X) = s_\\circ X^{n_k} - r_1 X^{n_k-n_1} - \\cdots
        - r_{k-1} X^{n_k-n_{k-1}} - r_k

    on the real unknown

    .. math::

        X = 1 + c.

    The derivative of :math:`f` is given by

    .. math::

        f^\\prime (X) = n_k s_\\circ X^{n_k - 1}
        - \\sum_{i=1}^{k-1} (n_k - n_i) r_i X^{n_k - n_i - 1}.

    The polynomial :math:`f` and its derivative derivative :math:`f^\\prime`
    are implemented as Python callables and passed to the Newton-Raphson
    search implementation with the daily interest rate as initial approximation
    for the IRR.

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
    daily_interest_rate: float, required
        Loan's daily interest rate (for the grossed up principal), used as the
        start point for the approximation of the IRR.
    """

    coefficients_vec = [net_principal] + [-1 * r for r in returns]

    def return_polynomial(irr_):

        powers_vec = [
            (1 + irr_) ** (return_days[-1] - n) for n in [0] + return_days
        ]

        return sum(
            coef * power
            for coef, power in zip(coefficients_vec, powers_vec)
        )

    derivative_coefficients_vec = [
        net_principal * (return_days[-1] - return_days[-2])
    ] + [
        r * (return_days[-1] - r_day)
        # last term does not need to be evaluated
        for r, r_day in zip(returns[:-1], return_days[:-1])
    ]

    def return_polynomial_derivative(irr_):

        powers_vec = [
            (1 + irr_) ** (return_days[-1] - r_day - 1)
            for r_day in return_days
        ]

        return sum(
            coef * power
            for coef, power in zip(derivative_coefficients_vec, powers_vec)
        )

    return newton_raphson_solver(
        return_polynomial, return_polynomial_derivative, daily_interest_rate
    )
