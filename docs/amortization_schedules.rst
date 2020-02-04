After a loan is granted, it must be continuously paid over time until it is
considered to be fully paid. The total amount of money the borrower returns
must be exactly the summed amounts of the loan's principal and interest. Thus,
each payment the borrower performs must be properly split into principal and
interest portions in such a way that, after all payments are performed, neither
principal or interest remain. The schedule according to which a loan is paid
is called an *amortization schedule*.

Let :math:`s` be the principal, :math:`d` the daily interest rate and
:math:`n_i` the number of days since the loan started until the due date of
the :math:`i`-th payment. An amortization schedule must describe

*   a sequence of payments :math:`P_1,P_2,\ldots,P_k`.
*   a sequence of partitions :math:`(A_1,J_1),(A_2,J_2),\ldots,(A_k,J_k)` of
    :math:`P_1,P_2,\ldots,P_k`, respectively, where

    *   :math:`A_i` is the portion of :math:`P_i` used as principal
        amortization,
    *   :math:`J_i` is the portion of :math:`P_i` used as interest payment,
        and
    *   :math:`P_i = A_i + J_i`, for all :math:`i,1\leq i\leq k`,

and these are such that

.. math::

    \sum_{i=1}^k A_i = s

holds. From the partitions and the sequence of payments one can define the
balance after each payment by

.. math::

    \left\{
    \begin{aligned}
        b_i &:=  b_{i-1}\ (1+d)^{n_i-n_{i-1}} - P_i,
        \ \mathrm{for}\ i,1\leq i\leq k,\ \mathrm{and}\\
        b_0 &:= s
    \end{aligned}
    \right..

*Regressive Price Schedule*. All the payments have the same value and it is
given by the PMT of the schedule parameters. The amortizations are then defined
as the PMT's present values, considering it can be brought back to the start
date according to the loan's daily interest rate. The interest due to each
payment is then defined as the difference between the PMT and the associated
amortization. Therefore, the payments, amortization and interest are defined by

*   :math:`P := \mathrm{PMT}(s,d,(n_1,\ldots,n_k))
    = \displaystyle\frac{s}{\sum_{j=1}^k \frac{1}{(1+d)^{n_j}}},
    \ \ \mathrm{for\ all}\ i,1\leq i\leq k`,
*   :math:`A_i := P\ \displaystyle\frac{1}{(1+d)^{n_i}},
    \ \ \mathrm{for\ all}\ i,1\leq i\leq k`,
*   :math:`J_i := P\ (1 - \displaystyle\frac{1}{(1+d)^{n_i}}),
    \ \ \mathrm{for\ all}\ i,1\leq i\leq k`,

respectively, for all :math:`i,1\leq i\leq k`.

This schedule is said to be "regressive" since it yields a decreasing sequence
of amortizations.

For example, consider a principal of R$ :math:`8530.20`, with interest rate of
:math:`0.0985\%` per day (which yields around :math:`3\%` every :math:`30` days)
and paid with :math:`10` instalments. Suppose payments should be made every
30 days. The regressive price schedule of such a loan is presented in the table
below.

+-----+------+---------+--------------+-----------+----------+
| #   | days | balance | amortization | interest  | payment  |
+-----+------+---------+--------------+-----------+----------+
| 0   |    0 | 8530.20 |              |           |          |
+-----+------+---------+--------------+-----------+----------+
| 1   |   30 | 7786.11 |    970.87    |   29.13   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 2   |   60 | 7019.69 |    942.60    |   57.40   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 3   |   90 | 6230.28 |    915.14    |   84.86   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 4   |  120 | 5417.19 |    888.49    |  111.51   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 5   |  150 | 4579.71 |    862.61    |  137.39   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 6   |  180 | 3717.10 |    837.48    |  162.52   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 7   |  210 | 2828.61 |    813.09    |  186.91   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 8   |  240 | 1913.47 |    789.41    |  210.59   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 9   |  270 |  970.87 |    766.42    |  233.58   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 10  |  300 |    0.00 |    744.09    |  255.91   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| EOL |      |         |   8530.20    | 1469.80   | 10000.00 |
+-----+------+---------+--------------+-----------+----------+

*Progressive Price Schedule*. As in the regressive Price schedule, all the
payments are given by the PMT of the schedule parameters, but the sequence
of amortizations and interests are reversed and therefore the amortizations
form an increasing sequence, hence the name "progressive". The sequences
of amortizations and interests are given by

*   :math:`A_i = P\ \displaystyle\frac{1}{(1+d)^{n_{k-i+1}}},
    \ \mathrm{for\ all}\ i,1\leq i\leq k`,
*   :math:`J_I = P\ (1 - \displaystyle\frac{1}{(1+d)^{n_{k-i+1}}}),
    \ \mathrm{for\ all}\ i,1\leq i\leq k`,

respectively.

For example, consider a principal of R$ :math:`8530.20`, with interest rate of
:math:`0.0985\%` per day (which yields around :math:`3\%` every :math:`30` days)
and paid with :math:`10` instalments. Suppose payments should be made every
30 days. The progressive Price schedule of such a loan is presented in the table
below.

+-----+------+---------+--------------+-----------+----------+
| #   | days | balance | amortization |  interest | payment  |
+-----+------+---------+--------------+-----------+----------+
| 0   |    0 | 8530.20 |              |           |          |
+-----+------+---------+--------------+-----------+----------+
| 1   |   30 | 7786.11 |    744.09    |  255.91   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 2   |   60 | 7019.69 |    766.42    |  233.58   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 3   |   90 | 6230.28 |    789.41    |  210.59   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 4   |  120 | 5417.19 |    813.09    |  186.91   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 5   |  150 | 4579.71 |    837.48    |  162.52   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 6   |  180 | 3717.10 |    862.61    |  137.39   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 7   |  210 | 2828.61 |    888.49    |  111.51   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 8   |  240 | 1913.47 |    915.14    |   84.86   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 9   |  270 |  970.87 |    942.60    |   57.40   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| 10  |  300 |    0.00 |    970.87    |   29.13   |  1000.00 |
+-----+------+---------+--------------+-----------+----------+
| EOL |      |         |   8530.20    | 1469.80   | 10000.00 |
+-----+------+---------+--------------+-----------+----------+

*Constant Amortization Schedule*. As the name implies, all amortizations are
taken so to have the same value, which is obtained by equally dividing the
principal into :math:`k` parts. The interest of each period is calculated over
the last remaining balance, and this is added to the amortization to compound
the due payment. These are given by

*   :math:`J_i := S(1 - \displaystyle\frac{i-1}{k})((1+d)^{n_i-n_{i-1}} - 1),
    \ \mathrm{for\ all}\ i,1\leq i\leq k`,
*   :math:`A_i := \displaystyle\frac{S}{k},
    \ \mathrm{for\ all}\ i,1\leq i\leq k`,

respectively. Note that the payments form a decreasing sequence, since the
interest part of each payment is calculate over an ever decreasing balance.
Moreover the balance decrease at a constant rate, due to the constant
amortization.

For example, consider a principal of R$ :math:`800.00`, with interest rate of
:math:`1,979\%` per day (which yields around :math:`80\%` every :math:`30` days)
and paid with :math:`10` instalments. Suppose payments should be made every
30 days. The constant amortization schedule of such a loan is presented in the
table below.

+-----+------+---------+--------------+----------+---------+
| #   | days | balance | amortization | interest | payment |
+-----+------+---------+--------------+----------+---------+
| 0   |    0 | 800.00  |              |          |         |
+-----+------+---------+--------------+----------+---------+
| 1   |   30 | 640.00  |    160.00    | 640.00   | 800.00  |
+-----+------+---------+--------------+----------+---------+
| 2   |   60 | 480.00  |    160.00    | 512.00   | 672.00  |
+-----+------+---------+--------------+----------+---------+
| 3   |   90 | 320.00  |    160.00    | 384.00   | 544.00  |
+-----+------+---------+--------------+----------+---------+
| 4   |  120 | 160.00  |    160.00    | 256.00   | 416.00  |
+-----+------+---------+--------------+----------+---------+
| 5   |  150 |   0.00  |    160.00    | 128.00   | 288.00  |
+-----+------+---------+--------------+----------+---------+
| EOL |      |         |    800.00    | 1920.00  | 2720.00 |
+-----+------+---------+--------------+----------+---------+
