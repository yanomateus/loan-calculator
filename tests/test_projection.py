import pytest

from loan_calculator.projection import Projection


def test_exception_raising_on_unknown_grossup_type(loan):

    with pytest.raises(TypeError):

        Projection(loan, [loan.start_date], grossup_type='unknown')
