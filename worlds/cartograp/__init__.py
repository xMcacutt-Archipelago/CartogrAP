from typing import ClassVar, Any, override

from BaseClasses import MultiWorld
from Options import PerGameCommonOptions
from worlds.AutoWorld import World


class CartogrAPWorld(World):
    """
    Move around a tiled map, completing quests and unveiling new areas.
    Created for the Archipelago Game Jam May-June 2026
    """
    game: ClassVar[str] = "CartogrAP"
    options_dataclass = ClassVar[type[PerGameCommonOptions]] = CartogrAPOptions
    options: CartogrAPOptions
    topology_present: bool = True
    option_groups: list[OptionGroup] = cartograp_option_groups
    item_name_to_id: ClassVar[dict[str, int]] = cartograp_items
    location_name_to_id: ClassVar[dict[str, int]] =  cartograp_locations

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.item_pool: list[CartogrAPItem] = []

    @override
    def fill_slot_data(self) -> dict[str, Any]:
        return {

        }

    @override
    def get_filler_items(self) -> dict[str, Any]:
        return get_random_item_names(self.random, 1, junk_weights)[0]

    @override
    def create_item(self, name: str) -> CartogrAPItem:
        return CartogrAPItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    @override
    def create_regions(self):
        create_cartograp_regions(self)

    @override
    def create_items(self):
        create_cartograp_items(self)

    @override
    def set_rules(self):
        set_cartograp_rules
        pass