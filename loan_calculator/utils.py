import numpy as np


def display_summary(loan):
    lines = list(
        zip(
            [loan.start_date] + loan.return_dates,
            map(lambda d: (d - loan.start_date).days,
                [loan.start_date] + loan.return_dates),
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
                *[line[0].isoformat()]
                + list(map(lambda n: np.round(n, 2), line[1:]))
            )
            for line in lines[1:]
        ] + [
            separator,
            footer_line,
            separator,
        ]
    )

    print(summary)
