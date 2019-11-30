"""Calculate the Brazilian IOF taxation over loan operations.

The IOF tax (Imposto sobre Operações de Crédito, Câmbio e Seguro ou relativas a
Títulos ou Valores Mobiliários) is a Brazilian tax incident over many financial
operations. In particular, they apply over on operations, the borrower being
either a legal or natural person.

This tax is composed by two parts: the tax over the principal and the tax over
the amortizations.

The IOF aliquot over amortizations is
  - in proportion to the number of days since the loan was granted,
  - in proportion to a fixed reduced aliquot with its value defined by law,
  - limited to 1.5%.

The IOF aliquot over the principal, called the complementary IOF aliquot, is
a fixed aliquot with its value defined by law.
"""


def amortization_iof(amortization, daily_iof_fee, num_days):
    """IOF tax over amortization.

    If :math:`A` is the amortization, :math:`I^*` is the daily IOF fee and
    :math:`n` is the number of days since the beginning of the operation, then
    the due IOF tax over the amortization is

    .. math::

        A\ \min(nI^*, 0.015).

    Parameters
    ----------
    amortization: float, required
        The amortization, i.e., principal payment, which is the basis for the
        amortization IOF tax.
    daily_iof_fee: float, required
        Aliquot applied over the amortization, as described in its current law.
    num_days: int, required
        Number of days since the loan was granted.
    """

    return float(amortization * min(daily_iof_fee * num_days, 0.015))


def complementary_iof(principal, complementary_iof_fee):
    """Complementary IOF tax over the principal.

    If :math:`S` is the principal and :math:`I^{**}` is the complementary IOF
    fee, then the due complementary IOF tax over the principal is

    .. math::

        S\ I^{**}.

    Parameters
    ----------
    principal: float, required
        The loan principal, which is the basis for the complementary IOF tax.
    complementary_iof_fee: float, required
        Aliquot applied over the principal, as described in its current law.
    """

    return float(principal * complementary_iof_fee)


def loan_iof(
    principal,
    amortizations,
    return_days,
    daily_iof_fee,
    complementary_iof_fee
):
    """The total IOF of a loan.

    If :math:`S` is the principal, :math:`A_i` is the :math:`i`-th amortization,
    :math:`n_1,\ldots,n_k` are the return days, :math:`I^*` is the daily IOF
    aliquot and :math:`I^{**}` is the complementary IOF aliquot, then the loan
    IOF tax amount is

    .. math::

        \mathrm{IOF}(S, I^*, I^{**}, (A_1,\ldots,A_k),(n_1,\ldots,n_k)) =
         SI^{**} + \sum_{i=1}^k A_i \min(n_i I^*,0.015)

    Parameters
    ----------
    principal: float, required
        Loan principal.
    amortizations: list, required
        List of floats providing the amortization due to each payment.
    return_days: list, required
        List of integers with the numbers of days since the loan was granted.
    daily_iof_fee: float, required
        Daily IOF aliquot, as described in its current law.
    complementary_iof_fee: float, required
        Complementary IOF aliquot, as described in its current law.
    """

    p = principal
    d_iof = daily_iof_fee
    c_iof = complementary_iof_fee

    return c_iof * p + sum(a * min(n * d_iof, 0.015)
                           for a, n in zip(amortizations, return_days))
