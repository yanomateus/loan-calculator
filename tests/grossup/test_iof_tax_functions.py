from numpy.testing import assert_almost_equal

from loan_calculator.grossup.iof_tax import (
    amortization_iof,
    complementary_iof,
    loan_iof,
    amortization_schedule_iof
)


def test_amortization_iof():
    assert_almost_equal(amortization_iof(100.0, 1, 1.0 / 200), 0.5, decimal=2)


def test_amortization_schedule_iof():
    assert_almost_equal(
        amortization_schedule_iof([200.0, 100.0], [1, 2], 1.0 / 200),
        2.0,
        decimal=2
    )


def test_amortization_iof_aliquot_bound():
    assert_almost_equal(amortization_iof(100.0, 1, 1.0 / 10), 1.5, decimal=2)


def test_complementary_iof():
    assert_almost_equal(complementary_iof(100.0, 0.01), 1.0, decimal=2)


def test_loan_iof():
    assert_almost_equal(
        loan_iof(300.0, [100.0, 200.0], [1, 2], 1.0 / 200, 1.0 / 600),
        3.0,
        decimal=2
    )
