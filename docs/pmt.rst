Let :math:`s` be the principal,
:math:`d` the daily interest rate and :math:`n_i` the number of days since the
principal was granted until the due date of the :math:`i`-th payment, for
:math:`i,1\leq i\leq k`. We want to
determine the so called PMT of these parameters, i.e., the due payment value
which completely pays the principal if made in the expected dates and considered
under the daily interest rate.

Let :math:`P` denote the PMT value. Brought to present value using the daily
interest rate, the :math:`k` payments should exactly meet the principal.
Then

.. math::

    \frac{P}{(1+d)^{n_1}} + \frac{P}{(1+d)^{n_2}} + \cdots +
    \frac{P}{(1+d)^{n_k}} = s

and it follows that

.. math::

    P\ \sum_{i=1}^k \frac{1}{(1+d)^{n_i}} = s.

Therefore, the PMT can be defined as

.. math::

    \mathrm{PMT}(s,d,(n_1,\ldots,n_k)) :=
    \frac{s}{\displaystyle\sum_{i=1}^k \frac{1}{(1+d)^{n_i}}}.
