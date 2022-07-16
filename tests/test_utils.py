from datetime import date

from loan_calculator.loan import Loan
from loan_calculator.utils import display_summary
from loan_calculator.schedule.base import AmortizationScheduleType


def test_display_summary_shows_expected_loan_summary(capsys):
    """ Asserts utils.display_summary outputs expected loan data.

    This raised AttributeError before PR #14 was merged:
    https://github.com/yanomateus/loan-calculator/pull/14

    utils.py:26-27 : display_summary(): - loan.amortizations.tolist(),...
    (AttributeError: 'list' object has no attribute 'tolist')
    """
    loan = Loan(
        principal=10000.00,  # principal
        annual_interest_rate=0.05,  # annual interest rate
        start_date=date(2020, 1, 5),  # start date
        return_dates=[
            date(2020, 2, 12),  # expected return date
            date(2020, 3, 13),  # expected return date
            date(2020, 3, 11),  # expected return date
            date(2020, 4, 13),  # expected return date
            date(2020, 5, 12),  # expected return date
            date(2020, 6, 12),  # expected return date
            date(2020, 7, 14),  # expected return date
            date(2020, 8, 15),  # expected return date
        ],
        year_size=365,  # used to convert between annual and daily interest rates # noqa
        grace_period=0,  # number of days for which the principal is not affected by the interest rate  # noqa
        amortization_schedule_type=AmortizationScheduleType.progressive_price_schedule, # noqa
        # determines how the principal is amortized
    )
    display_summary(loan)

    assert capsys.readouterr().out == (
        '+------------+----------+--------------+--------------+--------------+--------------+\n'  # noqa
        '|    dates   |    days  |    balance   | amortization |   interest   |    payment   |\n'  # noqa
        '+------------+----------+--------------+--------------+--------------+--------------+\n'  # noqa
        '| 2020-01-05 |        0 |     10000.00 |              |              |              |\n'  # noqa
        '| 2020-02-12 |       38 |      8780.50 |      1233.11 |        37.31 |      1270.42 |\n'  # noqa
        '| 2020-03-13 |       68 |      6274.59 |      1238.40 |        32.03 |      1270.42 |\n'  # noqa
        '| 2020-03-11 |       66 |      7543.00 |      1243.71 |        26.72 |      1270.42 |\n'  # noqa
        '| 2020-04-13 |       99 |      5030.22 |      1248.87 |        21.55 |      1270.42 |\n'  # noqa
        '| 2020-05-12 |      128 |      3779.34 |      1253.72 |        16.70 |      1270.42 |\n'  # noqa
        '| 2020-06-12 |      159 |      2524.60 |      1259.27 |        11.16 |      1270.42 |\n'  # noqa
        '| 2020-07-14 |      191 |      1265.00 |      1258.93 |        11.50 |      1270.42 |\n'  # noqa
        '| 2020-08-15 |      223 |         0.00 |      1263.99 |         6.44 |      1270.42 |\n'  # noqa
        '+------------+----------+--------------+--------------+--------------+--------------+\n'  # noqa
        '|            |          |              |     10000.00 |       163.40 |     10163.40 |\n'  # noqa
        '+------------+----------+--------------+--------------+--------------+--------------+\n'  # noqa
    )
