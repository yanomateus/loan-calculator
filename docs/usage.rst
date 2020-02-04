Usage
*****

The internal implementations of this library are meant to be accessed through
a public API composed by the classes

*   ``Loan``
*   ``GenericGrossup``
*   ``IofGrossup``

Loan
----

For example, a ``Loan`` can be instantiated as

::

    >>> from datetime import date
    >>> from loan_calculator import Loan
    >>> loan = Loan(
    ...     10000.00,  # principal
    ...     0.54,  # annual interest rate
    ...     date(2020, 1, 5),  # start date
    ...     [
    ...         date(2020, 2, 12),  # expected return date
    ...         date(2020, 3, 13),  # expected return date
    ...         date(2020, 3, 11),  # expected return date
    ...         date(2020, 4, 13),  # expected return date
    ...         date(2020, 5, 12),  # expected return date
    ...         date(2020, 6, 12),  # expected return date
    ...         date(2020, 7, 14),  # expected return date
    ...         date(2020, 8, 15),  # expected return date
    ...     ],
    ...     year_size=365,  # used to convert between annual and daily interest rates
    ...     grace_period=0,  # number of days for which the principal is not affected by the interest rate
    ...     amortization_schedule_type='progressive_price_schedule',  # determines how the principal is amortized
    ... )


A summary of this loan can be displayed with the function ``display_summary``

::

    >>> from loan_calculator import display_summary
    >>> display_summary(loan)
    ... +------------+----------+--------------+--------------+--------------+--------------+
    ... |    dates   |    days  |    balance   | amortization |   interest   |    payment   |
    ... +------------+----------+--------------+--------------+--------------+--------------+
    ... | 2020-01-05 |        0 |     10000.00 |              |              |              |
    ... | 2020-02-12 |       38 |      9020.32 |      1105.69 |       333.77 |      1439.46 |
    ... | 2020-03-13 |       68 |      6463.86 |      1148.35 |       291.12 |      1439.46 |
    ... | 2020-03-11 |       66 |      7884.64 |      1192.65 |       246.81 |      1439.46 |
    ... | 2020-04-13 |       99 |      5265.84 |      1237.20 |       202.26 |      1439.46 |
    ... | 2020-05-12 |      128 |      4010.16 |      1280.38 |       159.08 |      1439.46 |
    ... | 2020-06-12 |      159 |      2720.49 |      1331.35 |       108.11 |      1439.46 |
    ... | 2020-07-14 |      191 |      1385.99 |      1328.20 |       111.26 |      1439.46 |
    ... | 2020-08-15 |      223 |         0.00 |      1376.19 |        63.27 |      1439.46 |
    ... +------------+----------+--------------+--------------+--------------+--------------+
    ... |            |          |              |     10000.00 |      1515.69 |     11515.69 |
    ... +------------+----------+--------------+--------------+--------------+--------------+

Grossup
-------

Loan operations will usually involve taxes and service fees. Therefore, the
loan's principal must be grossed up (i.e., "incremented") in order to
comprehend such quantities. Two grossup implementations are provided in this
library, namely,

*   `IOF Grossup`: apply the Brazilian tax IOF and a linear service fee over
    the loan. Its specifications are provided by current Brazilian law.
*   `Generic Grossup Solver`: apply a generic tax and service fee over the
    loan. Their specifications are provided by the user as python callables.

`IOF grossup`. Consider the same loan as above and let us apply the IOF grossup
over it. Picking ``date(2020, 1, 15)`` as the taxable event, we obtain

::

    >>> from loan_calculator import IofGrossup
    >>> iof_grossup = IofGrossup(
    ...     loan,
    ...     date(2020, 1, 15),
    ...     daily_iof_aliquot=0.000082,
    ...     complementary_iof_aliquot=0.0038,
    ...     service_fee_aliquot=0.05
    ... )
    >>> display_summary(grossup.grossed_up_loan, reference_date=grossup.reference_date)
    ... +------------+----------+--------------+--------------+--------------+--------------+
    ... |    dates   |    days  |    balance   | amortization |   interest   |    payment   |
    ... +------------+----------+--------------+--------------+--------------+--------------+
    ... | 2020-01-15 |        0 |     10664.51 |              |              |              |
    ... | 2020-02-12 |       28 |      9619.73 |      1179.16 |       355.95 |      1535.12 |
    ... | 2020-03-13 |       58 |      6893.39 |      1224.65 |       310.46 |      1535.12 |
    ... | 2020-03-11 |       89 |      8408.59 |      1271.90 |       263.21 |      1535.12 |
    ... | 2020-04-13 |      118 |      5615.76 |      1319.41 |       215.70 |      1535.12 |
    ... | 2020-05-12 |      149 |      4276.64 |      1365.46 |       169.65 |      1535.12 |
    ... | 2020-06-12 |      181 |      2901.27 |      1419.82 |       115.30 |      1535.12 |
    ... | 2020-07-14 |      213 |      1478.09 |      1416.46 |       118.65 |      1535.12 |
    ... | 2020-08-15 |      240 |         0.00 |      1467.64 |        67.48 |      1535.12 |
    ... +------------+----------+--------------+--------------+--------------+--------------+
    ... |            |          |              |     10664.51 |      1616.41 |     12280.92 |
    ... +------------+----------+--------------+--------------+--------------+--------------+

`Generic grossup solver`. Say we came up with a grossup problem composed by

*   a tax applied over the amortizations and for which $ 1 is charged for each
    day between the amortization and the taxable event, limited to $ 200,
*   a complementary tax charging 1% over the principal, and
*   a service fee which is constant to $ 20.

Suppose we want to solve this grossup problem for the same loan as used before,
considering the same taxable event, ``2020-01-15``. The grossed up principal
can be obtained by performing the following calculation

.. math::

   \frac{10000.00 + (28.00 + 58.00 + 89.00 + 118.00 + 149.00 + 181.00 + 200.00 + 200.00) + 20.00}{1 - 1\%},

which yields $11154.55. To obtain a solution for this problem using the grossup
solver, we must provide three functions: one implementing the reduced tax,
incident over the amortizations, one implementing the complementary tax and
one implementing the service fee, these both incident over the principal.

::

    >>> def reduced_tax_function(amortizations, r_days):
    >>>     tax = 0.0
    >>>     for r in r_days:
    >>>         tax += r if r <= 200.0 else 200.0
    >>>     return tax
    ...
    >>> def complementary_tax_function(principal):
    >>>     return 0.01 * principal
    ...
    >>> def service_fee(principal):
    >>>     return 20.0
    ...
    >>> grossup = GenericGrossup(
    ...     loan,
    ...     date(2020, 1, 15),
    ...     reduced_tax_function,
    ...     complementary_tax_function,
    ...     service_fee
    ... )
    >>> display_summary(grossup.grossed_up_loan, grossup.reference_date)
    ... +------------+----------+--------------+--------------+--------------+--------------+
    ... |    dates   |    days  |    balance   | amortization |   interest   |    payment   |
    ... +------------+----------+--------------+--------------+--------------+--------------+
    ... | 2020-01-15 |        0 |     11154.55 |              |              |              |
    ... | 2020-02-12 |       28 |     10018.83 |      1226.51 |       422.07 |      1648.59 |
    ... | 2020-03-13 |       58 |      8732.18 |      1266.32 |       382.26 |      1648.59 |
    ... | 2020-04-13 |       89 |      7409.77 |      1315.18 |       333.41 |      1648.59 |
    ... | 2020-05-12 |      118 |      6019.79 |      1365.92 |       282.67 |      1648.59 |
    ... | 2020-06-12 |      149 |      4596.06 |      1416.94 |       231.65 |      1648.59 |
    ... | 2020-07-14 |      181 |      3124.79 |      1466.39 |       182.19 |      1648.59 |
    ... | 2020-08-15 |      213 |      1596.76 |      1521.16 |       127.42 |      1648.59 |
    ... | 2020-09-11 |      240 |         0.00 |      1576.12 |        72.47 |      1648.59 |
    ... +------------+----------+--------------+--------------+--------------+--------------+
    ... |            |          |              |     11154.55 |      2034.14 |     13188.69 |
    ... +------------+----------+--------------+--------------+--------------+--------------+
