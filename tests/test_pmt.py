import pytest

from loan_cashflow_calculator.pmt import pmt


def test_unitary_evaluation():
    """Assert equation :math:`\mathrm{PMT}(1, 1, (1, 1)) = 1` holds."""

    assert 1.0 == pytest.approx(pmt(1.0, 1.0, [1, 1]), 0.01)


def test_proper_domain_validation():

    with pytest.raises(ValueError):
        pmt(-1.0, 1.0, [1, 1])

    with pytest.raises(ValueError):
        pmt(1.0, -1.0, [1, 1])

    with pytest.raises(ValueError):
        pmt(1.0, 1.0, [-1, 2])
