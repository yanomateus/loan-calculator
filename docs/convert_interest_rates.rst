The mathematics for converting aliquots between two different interest rates
is fairly simple. In fact, let :math:`s` be a semiannual interest rate and let
us assume a year has 365 days (this convention is also called as "commercial
year". There is also the "banker year", with 360 days). If :math:`d_s` is the
equivalent daily interest rate, applying :math:`d_s` 365 to an amount produces
as much capital as the semiannual rate :math:`s` applied twice over the
same initial amount, i.e.,

.. math::

    (1 + d_s)^{365} = (1 + s)^2

from which follows that

.. math::

    d_s = (1 + s)^{\frac{2}{365}} - 1.

The conversion expression for monthly and quarterly rate can be obtained in an
analogue manner: for a monthly interest rate :math:`m`, the equivalent daily
interest rate :math:`d_m` is given by

.. math::

    d_m = (1 + m)^\frac{12}{365} - 1

and for a quarterly interest rate :math:`q`, the equivalent daily interest rate
is :math:`d_q` is given by

.. math::

    d_q = (1 + q)^\frac{4}{365} - 1.
