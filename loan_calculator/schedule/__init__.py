from .base import AmortizationScheduleType
from .price import ProgressivePriceSchedule, RegressivePriceSchedule
from .constant import ConstantAmortizationSchedule


SCHEDULE_TYPE_CLASS_MAP = {
    AmortizationScheduleType.constant_amortization_schedule: ConstantAmortizationSchedule,  # noqa
    AmortizationScheduleType.regressive_price_schedule: RegressivePriceSchedule,  # noqa
    AmortizationScheduleType.progressive_price_schedule: ProgressivePriceSchedule,  # noqa
}

__all__ = [
    'ProgressivePriceSchedule',
    'RegressivePriceSchedule',
    'ConstantAmortizationSchedule',
    'SCHEDULE_TYPE_CLASS_MAP',
]
