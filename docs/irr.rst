The internal return rate is the effective rate at which the net principal
is grows in order to exactly match the sum of the due returns. The IRR is the
actual "interest rate" from the point of view of a borrower, who receives
the net principal but will have to pay off its grossed up value.

Let :math:`r_1, r_2,\ldots ,r_k` be the expected returns that will pay
off the grossed up principal, :math:`n_1, n_2,\ldots, n_k` the number
of days since the loan was granted until each expected return. If
:math:`s_\circ` is the net principal, the IRR :math:`c` is defined as
the least positive real solution of the equation

.. math::

    s_\circ (1 + c)^{n_k} - \sum_{i=1}^k r_i (1 + c)^{n_k - n_i} = 0.

Note that this is an algebraic equation on the unknown :math:`1 + c`. Let
:math:`X = 1 + c` and :math:`f(X)` be the polynomial

.. math::

    f(X) = s_\circ X^{n_k} - r_1 X^{n_k - n_1} - r_2 X^{n_k - n_2}
    - \cdots - r_k.

Therefore, to approximate the IRR is equivalent to approximate
a positive real root of :math:`f(X)`. In this library, this is achieved by
a Newton-Raphson based solver, which is a natural choice since it is easy
to evaluate the derivative :math:`f^\prime (X)` of :math:`f(X)` and the
loan's daily interest rate can be adopted as starting point for the
approximation as we know the IRR is a slightly greater aliquot.
