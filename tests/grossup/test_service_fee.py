from numpy.testing import assert_almost_equal

from loan_calculator.grossup.service_fee import linear_service_fee


def test_linear_service_fee():
    assert_almost_equal(
        linear_service_fee(100.0, 0.01),
        1.0,
        decimal=2
    )
