Usage
*****

The internal implementations of this library are meant to be accessed through
a public API composed by the classes

*   ``Loan``
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
comprehend such quantities. This library implements a grossup for the brazilian
tax IOF. Its specifications are provided by current Brazilian law.

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
