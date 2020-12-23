import pytest

from loan_calculator.projection import Projection


def test_exception_raising_on_unknown_grossup_type(loan):

    with pytest.raises(ValueError):

        Projection(loan, [loan.start_date], grossup_type='unknown')
