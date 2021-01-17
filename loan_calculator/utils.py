from decimal import Decimal, ROUND_HALF_UP


def display_summary(loan, reference_date=None):
    """Display a legible summary of a loan.

    Parameters
    ----------
    loan : Loan, required
        Loan to be displayed.
    reference_date : date, optional
        Date object with the date to consider as reference when calculating
        the values of the column `day` in the function's output. (default None)
    """

    reference_date = reference_date or loan.start_date

    dates = [reference_date] + loan.return_dates

    lines = list(
        zip(
            dates,
            map(lambda d: (d - reference_date).days,
                dates),
            loan.balance,
            [''] + loan.amortizations.tolist(),
            [''] + loan.interest_payments.tolist(),
            [''] + loan.due_payments.tolist(),
        )
    )

    separator = ('+------------+----------+--------------'
                 '+--------------+--------------+--------------+')

    header = ('|    dates   |    days  |    balance   '
              '| amortization |   interest   |    payment   |')

    trailing_line = (
        '| {:>8} | {:>8d} | {:>12.2f} |              '
        '|              |              |'
        .format(*[lines[0][0].isoformat()] + list(lines[0][1:3]))
    )

    body_line = ('| {:>8} | {:>8d} | {:>12.2f} '
                 '| {:>12.2f} | {:>12.2f} | {:>12.2f} |')

    footer_line = (
        '|            |          |              '
        '| {:>12.2f} | {:>12.2f} | {:>12.2f} |'
        .format(
            loan.total_amortization,
            loan.total_interest,
            loan.total_paid
        )
    )

    summary = '\n'.join(
        [
            separator,
            header,
            separator,
            trailing_line,
        ] + [
            body_line.format(
                line[0].isoformat(),
                line[1],
                *list(
                    map(
                        lambda n: Decimal(n).quantize(
                            Decimal('0.01'),
                            rounding=ROUND_HALF_UP
                        ),
                        line[2:])
                )
            )
            for line in lines[1:]
        ] + [
            separator,
            footer_line,
            separator,
        ]
    )

    print(summary)
