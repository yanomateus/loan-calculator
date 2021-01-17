import pytest

from loan_calculator.grossup.functions import (
    br_iof_regressive_price_grossup,
    br_iof_progressive_price_grossup,
    br_iof_constant_amortization_grossup
)


def test_br_progressive_price_grossup_basic_evaluation():
    gup = br_iof_progressive_price_grossup(1.0,
                                           1.0,
                                           3.0 / 500,
                                           0.09,
                                           [1, 2],
                                           0.4)

    assert gup == pytest.approx(2.0, rel=0.01)


def test_br_regressive_price_grossup_basic_evaluation():
    gup = br_iof_regressive_price_grossup(1.0,
                                          1.0,
                                          0.0075,
                                          0.09,
                                          [1, 2],
                                          0.4)

    assert gup == pytest.approx(2.0, rel=0.01)


def test_br_constant_amortization_grossup_basic_evaluation():
    gup = br_iof_constant_amortization_grossup(1.0,
                                               1.0,
                                               1.0 / 200,
                                               1.0 / 400,
                                               [1, 2],
                                               0.49)

    assert gup == pytest.approx(2.0, rel=0.01)
