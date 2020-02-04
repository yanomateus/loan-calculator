import pytest

from loan_calculator.pmt import constant_return_pmt


def test_unitary_evaluation():
    """Assert equation :math:`\\mathrm{PMT}(1, 1, (1, 1)) = 1` holds."""

    assert 1.0 == pytest.approx(constant_return_pmt(1.0, 1.0, [1, 1]), 0.01)
