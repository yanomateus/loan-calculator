from numpy.testing import assert_almost_equal

from loan_calculator.irr import approximate_irr


def test_approximate_irr():

    assert_almost_equal(
        approximate_irr(1.0, [1.0, 1.0], [1, 2]),
        0.618033988749895
    )
