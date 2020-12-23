from loan_calculator.grossup.iof import IofGrossup
from loan_calculator.grossup.base import GrossupType


GROSSUP_TYPE_CLASS_MAP = {
    GrossupType.iof: IofGrossup,
}
