The grossup consists of including due taxes and service fee into a given
principal augmenting it so its resulting net value equals the originally given
principal.

It seems fairly reasonable to assume the service fee is simply an aliquot
applied over the principal so, if :math:`S` is the principal and :math:`\gamma` is
the service fee aliquot, then the service if given by :math:`\gamma S`.

On the other hand, it is hard to pin down a reasonable and generic expression
for a tax being applied over the principal, since taxes are very context bound
and their rules might be revised as laws are amended.

This is addressed by a grossup solver, which approximates solutions
for the grossup problem given the user provides python implementations of some
mathematical functions. Such mathematical functions are

*   :math:`a = a(s, d, (n_1,\ldots,n_k))` returning :math:`(a_1,\ldots,a_k)` a
    vector of amortizations, where :math:`s` is the principal, :math:`d` is the
    daily interest rate and :math:`n_i` is the :math:`i`-th return day,
*   :math:`f = f((a_1,\ldots,a_k), (n_1,\ldots,n_k), \alpha)`, where :math:`a_i`
    is the :math:`i`-th amortization, :math:`n_i` is the :math:`i`-th the return
    day, and :math:`\alpha` is the tax's daily aliquot,
*   :math:`c = c(s, \beta)`, where :math:`s` is the principal and :math:`\beta`
    is the complementary aliquot,
*   :math:`g = g(s, \gamma)`, where :math:`s` is the principal and
    :math:`\gamma` is the service fee aliquot.

The grossed up principal is then approximated as a positive real root of the
function

.. math::

    s \longmapsto
    s_\circ
    - (s - f(a(s, d, (n_1,\ldots,n_k)), (n_1,\ldots,n_k), \alpha)
    - c(s,\beta)
    - g(s,\gamma)).
