"""
The base APWorld
"""
from typing import ClassVar

from BaseClasses import MultiWorld
from Options import PerGameCommonOptions
from worlds.AutoWorld import World

from .options import CartogrAPOptions
from .web_world import CartogrAPWebWorld


class CartogrAPWorldBase(World):
    web = CartogrAPWebWorld()
    options_dataclass: ClassVar[type[PerGameCommonOptions]] = CartogrAPOptions
    options: CartogrAPOptions  # pyright: ignore[reportIncompatibleVariableOverride]

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        super().__init__(multiworld=multiworld, player=player)
        self.plain_cell_count: int = 0
        self.other_cell_type_count: int = 0