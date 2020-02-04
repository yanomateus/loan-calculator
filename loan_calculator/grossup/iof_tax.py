# -*- coding: utf-8 -*-
"""Calculate the Brazilian IOF tax on loan operations.

The IOF tax (Imposto sobre Operações de Crédito, Câmbio e Seguro ou relativas a
Títulos ou Valores Mobiliários) is a Brazilian tax incident over many financial
operations. In particular, they apply on loan operations, the borrower being
either a legal or natural person. It is institutionalized by the law-decree
Nº 6.306, from December 14th, 2007, as in its text_.

.. _text: http://www.planalto.gov.br/ccivil_03/_Ato2007-2010/2007/Decreto/D6306compilado.htm  # noqa: E501

This tax is composed by two parts: the tax over the principal and the tax over
the amortizations.

The IOF aliquot over amortizations is
  - in proportion to the number of days since the loan was granted,
  - in proportion to a fixed reduced aliquot with its value defined by law,
  - limited to 1.5%.

The IOF aliquot over the principal, called the complementary IOF aliquot, is
a fixed aliquot with its value defined by law.
"""


def amortization_schedule_iof(
        amortizations,
        return_days,
        daily_iof_aliquot=0.000082
):
    """IOF tax over an amortization schedule.

    If :math:`A_1,A_2\\ldots,A_k` are the amortizations,
    :math:`n_1,n_2,\\ldots,n_k` the return days and :math:`I^*` the daily IOF
    aliquot, then the due IOF tax is

    .. math::

        \\sum_{i=1}^k A_i \\min(n_i I^*, 0.015).

    Parameters
    ----------
    amortizations: list, required
        Sequence of amortizations.
    return_days: list, required
        Sequence of assumed return days.
    daily_iof_aliquot: float, required
        The daily IOF aliquot, defined by law.

    Returns
    -------
        The due IOF tax on the amortizations in the given days.
    """

    # variables are renamed to make the math more explicit
    amts = amortizations
    r_days = return_days
    d = daily_iof_aliquot

    return sum(a * min(n * d, 0.015) for a, n in zip(amts, r_days))


def amortization_iof(amortization, num_days, daily_iof_aliquot=0.000082):
    """IOF tax over amortization.

    If :math:`A` is the amortization, :math:`I^*` is the daily IOF fee and
    :math:`n` is the number of days since taxable event, then the due IOF tax
    over the amortization is

    .. math::

        A\\ \\min(nI^*, 0.015).

    Parameters
    ----------
    amortization: float, required
        The amortization, i.e., principal payment, which is the basis for the
        amortization IOF tax.
    daily_iof_aliquot: float, required
        Aliquot applied over the amortization with its value define by law.
    num_days: int, required
        Number of days since the taxable event.
    """

    return float(amortization * min(daily_iof_aliquot * num_days, 0.015))


def complementary_iof(principal, complementary_iof_fee=0.0038):
    """Complementary IOF tax over the principal.

    If :math:`s` is the principal and :math:`I^{**}` is the complementary IOF
    fee, then the due complementary IOF tax over the principal is

    .. math::

        s\\ I^{**}.

    Parameters
    ----------
    principal: float, required
        The loan principal, which is the basis for the complementary IOF tax.
    complementary_iof_fee: float, required
        Aliquot applied over the principal. Its value is defined by law.
    """

    return float(principal * complementary_iof_fee)


def loan_iof(
    principal,
    amortizations,
    return_days,
    daily_iof_aliquot,
    complementary_iof_aliquot
):
    """The total IOF of a loan.

    If :math:`s` is the principal, :math:`A_i` is the :math:`i`-th
    amortization, :math:`n_1,\\ldots,n_k` are the return days, :math:`I^*` is
    the daily IOF aliquot and :math:`I^{**}` is the complementary IOF aliquot,
    then the loan IOF tax amount is

    .. math::

        \\mathrm{IOF}(s, I^*, I^{**}, (A_1,\\ldots,A_k),(n_1,\\ldots,n_k)) =
         sI^{**} + \\sum_{i=1}^k A_i \\min(n_i I^*,0.015)

    Parameters
    ----------
    principal: float, required
        Loan principal.
    amortizations: list, required
        List of floats providing the amortization due to each payment.
    return_days: list, required
        List of integers with the numbers of days since the loan was granted.
    daily_iof_aliquot: float, required
        Daily IOF aliquot. Its value is defined by law.
    complementary_iof_aliquot: float, required
        Complementary IOF aliquot. Its value is defined by law.
    """

    p = principal
    d_iof = daily_iof_aliquot
    c_iof = complementary_iof_aliquot

    return c_iof * p + sum(a * min(n * d_iof, 0.015)
                           for a, n in zip(amortizations, return_days))
