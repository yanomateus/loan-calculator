import numpy as np
from scipy.optimize import fsolve


def approximate_irr(net_principal, returns, return_days):
    """Approximate the internal return rate of a series of returns.

    Wrap around scipy.optimize.solve to approximate the root of a polynomial
    which is used to defined the internal return rate.

    Let :math:`S_\\circ` be a net principal (i.e., a principal with eventual
    taxes and fees properly deduced), :math:`r_1,r_2\\ldots,r_k` a sequence of
    returns and :math:`n_1,n_2,\\ldots,n_k` the due days for these returns. The
    *internal return rate* :math:`c` is then determined from the unique
    positive real root of the polynomial

    .. math::

        f(X) = S_\\circ X^{n_k} - r_k X^{n_k-n_1} - \\cdots
        - r_2 X^{n_k-n_{k-1}} - r_1

    on the real unknown

    .. math::

        X = 1 + c.
    """

    r_days = return_days

    def return_polynomial(irr_):
        coefficients_vec = np.array(
            [net_principal] + [-1 * r for r in returns],
            dtype=float
        )

        unknowns_vec = np.array(
            [(1 + irr_) ** (r_days[-1] - n) for n in [0] + r_days],
            dtype=float
        )

        return np.dot(coefficients_vec, unknowns_vec)

    return fsolve(return_polynomial, np.array(0.0))[0]
