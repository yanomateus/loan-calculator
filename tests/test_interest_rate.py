import pytest

from loan_calculator.interest_rate import (
    InterestRateType, convert_to_daily_interest_rate
)
from loan_calculator.loan import YearSizeType


def test_convert_daily_interest_rate():
    assert (
        convert_to_daily_interest_rate(
            1.2,
            InterestRateType.daily,
            YearSizeType.commercial
        )
        == pytest.approx(1.2)
    )


def test_convert_annual_interest_rate():
    assert (
        convert_to_daily_interest_rate(
            2 ** YearSizeType.commercial.value - 1,
            InterestRateType.annual,
            YearSizeType.commercial
        )
        == pytest.approx(1.0)
    )


def test_convert_semiannual_interest_rate():
    assert (
        convert_to_daily_interest_rate(
            2 ** (YearSizeType.commercial.value / 2) - 1,
            InterestRateType.semiannual,
            YearSizeType.commercial
        )
        == pytest.approx(1.0)
    )


def test_convert_quarterly_interest_rate():
    assert (
        convert_to_daily_interest_rate(
            2 ** (YearSizeType.commercial.value / 4) - 1,
            InterestRateType.quarterly,
            YearSizeType.commercial
        )
        == pytest.approx(1.0)
    )
