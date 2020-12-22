import pytest

from loan_calculator.irr import approximate_irr


def test_approximate_irr():

    assert approximate_irr(1.0, [1.0, 1.0], [1, 2], 0.5) == pytest.approx(0.618033988749895)  # noqa
