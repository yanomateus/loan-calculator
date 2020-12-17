import pytest

from loan_calculator.grossup.iof_tax import (
    amortization_iof,
    complementary_iof,
    loan_iof,
    amortization_schedule_iof
)


def test_amortization_iof():
    assert amortization_iof(100.0, 1, 1.0 / 200) == pytest.approx(0.5, rel=0.01)  # noqa


def test_amortization_schedule_iof():
    assert amortization_schedule_iof([200.0, 100.0], [1, 2], 1.0 / 200) == pytest.approx(2.0, rel=0.01)  # noqa


def test_amortization_iof_aliquot_bound():
    assert amortization_iof(100.0, 1, 1.0 / 10) == pytest.approx(1.5, rel=2)


def test_complementary_iof():
    assert complementary_iof(100.0, 0.01) == pytest.approx(1.0, rel=0.01)


def test_loan_iof():
    assert loan_iof(300.0, [100.0, 200.0], [1, 2], 1.0 / 200, 1.0 / 600) == pytest.approx(3.0, rel=0.01)  # noqa
