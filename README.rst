========================
Loan Cashflow Calculator
========================


.. image:: https://img.shields.io/pypi/v/loan_cashflow_calculator.svg
        :target: https://pypi.python.org/pypi/loan_cashflow_calculator

.. image:: https://img.shields.io/travis/yanomateus/loan_cashflow_calculator.svg
        :target: https://travis-ci.org/yanomateus/loan_cashflow_calculator

.. image:: https://readthedocs.org/projects/loan-cashflow-calculator/badge/?version=latest
        :target: https://loan-cashflow-calculator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Implement constant amortization schedule.

The constant amortization schedule is defined as the amortization schedule
where all the amortizations have the same value, given as
:math:`\frac{S}{k}`, where :math:`S` is the principal and :math:`k`
is the number of due payments. Therefore, the due payments do not
have all the same value, as in the French system, but differ
according to how much interest was accumulated over time. If
:math:`d` is the daily interest rate, :math:`P_i` is the :math:`i`-th
due payment, :math:`A_i` and :math:`J_i` are the associated amortization
and interest, respectively, then

  - :math:`A_i = \frac{S}{k}`,
  - :math:`J_i = ((1+d)^{n_i} - (1+d)^{n_{i-1}})
    (S - A_i \sum_{1\leq j\leq i-1} \frac{1}{(1+d)^{n_j}})`
  - :math:`P_i = A + J_i`
  - :math:`b_i = S(1+d)^{n_i} - P \sum_{1\leq j\leq i} (1+d)^{n_i-n_j}`
  - :math:`b_i = S - iA`.


If we denote by :math:`P` the instalment value, :math:`S` the principal,
:math:`d` the daily interest rate, :math:`n_i` the number of days since the
beginning of the operation until the :math:`i`-th due date, :math:`A_i`
the :math:`i`-th amortization and :math:`J_i` the :math:`i`-th interest
paid and :math:`b_i` the balance after the :math:`i`-th payment, then

  - :math:`P=\mathrm{PMT}(S,d,(n_1,\ldots,n_k))`.
  - :math:`b_i = b_{i-1}(1+d)^{n_i-n_{i-1}} - P`.
  - :math:`J_i = P - b_{i-1}((1+d)^{n_i-n_{i-1}}-1)`.
  - :math:`A_i = P - J_i`.

.. math::

    \mathrm{IOF}(S, I^*, I^{**}, (A_1,\ldots,A_k),(n_1,\ldots,n_k)) =
    \sum_{i=1}^k A_i \min(n_i I^*,0.015) + SI^{**}

Loan Cashflow Solver

* Free software: MIT license
* Documentation: https://loan-cashflow-calculator.readthedocs.io.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
