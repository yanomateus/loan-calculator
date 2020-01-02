The internal return rate is effective rate at which the net principal is grows
in order to exactly match the sum of the due returns.

Let :math:`S_\circ` be a net principal (i.e., a principal with eventual
taxes and fees properly deduced), :math:`r_1,r_2\ldots,r_k` a sequence of
returns and :math:`n_1,n_2,\ldots,n_k` the due days for these returns. The
*internal return rate* :math:`c` is then determined from the unique positive
real root of the polynomial

.. math::

    f(X) = S_\circ X^{n_k} - r_k X^{n_k-n_1} - \cdots
    - r_2 X^{n_k-n_{k-1}} - r_1

on the real unknown

.. math::

    X = 1 + c.
