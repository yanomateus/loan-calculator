import pytest

from loan_calculator.grossup.service_fee import linear_service_fee


def test_linear_service_fee():
    assert linear_service_fee(100.0, 0.01) == pytest.approx(1.0, rel=0.01)
