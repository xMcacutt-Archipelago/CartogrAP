"""
Options Here
"""
import dataclasses
from typing import ClassVar

from Options import Range, OptionGroup, PerGameCommonOptions, Choice


class CellCount(Choice):
    """
    How many cells to generate?
    """
    option_500: ClassVar[int] = 500
    option_750: ClassVar[int] = 750
    option_1000: ClassVar[int] = 1000
    option_1250: ClassVar[int] = 1250
    option_1500: ClassVar[int] = 1500
    option_1750: ClassVar[int] = 1750
    option_2000: ClassVar[int] = 2000
    default: ClassVar[int] = option_750

    @staticmethod
    def max_value():
        return CellCount.option_2000


cartogr_ap_option_groups: list[OptionGroup] = \
    [
        OptionGroup("Meta",
                    [
                        CellCount,
                    ]),
    ]

@dataclasses.dataclass
class CartogrAPOptions(PerGameCommonOptions):
    cell_count: CellCount