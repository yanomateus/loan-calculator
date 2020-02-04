import pytest

from loan_calculator.grossup.base import BaseGrossup


def test_base_class_can_not_perform_grossup(loan):

    with pytest.raises(NotImplementedError):

        BaseGrossup(loan, loan.start_date).grossup()
