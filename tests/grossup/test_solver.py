from numpy.testing import assert_almost_equal

from loan_calculator.grossup.service_fee import linear_service_fee
from loan_calculator.grossup.solver import approximate_grossup
from loan_calculator.grossup.iof_tax import (
    amortization_schedule_iof,
    complementary_iof
)


def test_approximate_grossup_for_progressive_price_schedule():

    from loan_calculator.schedule.price import ProgressivePriceSchedule

    gup = approximate_grossup(
        1.0,
        1.0,
        [1, 2],
        (lambda p, d, r_days:
         ProgressivePriceSchedule(p, d, r_days).amortizations),
        amortization_schedule_iof,
        3.0 / 500,
        complementary_iof,
        0.09,
        linear_service_fee,
        0.4
    )

    assert_almost_equal(gup, 2.0, decimal=2)


def test_approximate_grossup_for_regressive_price_schedule():

    from loan_calculator.schedule.price import RegressivePriceSchedule

    gup = approximate_grossup(
        1.0,
        1.0,
        [1, 2],
        (lambda p, d, r_days:
         RegressivePriceSchedule(p, d, r_days).amortizations),
        amortization_schedule_iof,
        0.0075,
        complementary_iof,
        0.09,
        linear_service_fee,
        0.4
    )

    assert_almost_equal(gup, 2.0, decimal=2)


def test_approximate_grossup_for_constant_amortization_schedule():

    from loan_calculator.schedule.constant import ConstantAmortizationSchedule

    gup = approximate_grossup(
        1.0,
        1.0,
        [1, 2],
        (lambda p, d, r_days:
         ConstantAmortizationSchedule(p, d, r_days).amortizations),
        amortization_schedule_iof,
        1.0 / 200,
        complementary_iof,
        1.0 / 400,
        linear_service_fee,
        0.49
    )

    assert_almost_equal(gup, 2.0, decimal=2)
