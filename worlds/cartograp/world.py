"""
Main World class
"""
from typing import ClassVar, override, Mapping, Any

from BaseClasses import MultiWorld, ItemClassification, CollectionState, Region, Item
from rule_builder.rules import Has

from .constants import GAME_NAME, REGION_CHEST_EVENT_ITEM
from .items import CartogrAPItem, get_item_with_right_classification, CartogrAPItems, create_items
from .locations import LocationData, generate_location_list, FULL_LOCATION_LIST
from .regions import create_regions, connect_regions
from .world_base import CartogrAPWorldBase


class CartogrAPWorld(CartogrAPWorldBase):
    """
    Move around a tiled map, completing quests and unveiling new areas.
    Created for the Archipelago Game Jam May-June 2026
    """
    game: ClassVar[str] = GAME_NAME
    # item_name_groups = item_name_groups
    # location_name_groups = location_name_groups
    item_name_to_id: ClassVar[dict[str, int]] = {item.item_name: item.code for item in CartogrAPItems}
    location_name_to_id: ClassVar[dict[str, int]] = {loc_data.loc_name: loc_data.code for loc_data in FULL_LOCATION_LIST if loc_data.code is not None}
    topology_present: bool = True

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        self.location_list: list[LocationData] = []

    @override
    def get_filler_item_name(self) -> str:
        return CartogrAPItems.FILLER_ITEM.item_name


    @override
    def create_item(self, name: str) -> CartogrAPItem:
        return get_item_with_right_classification(world=self, item_name=name)


    def generate_early(self) -> None:
        # UT Stuff
        super().generate_early()
        self.location_list = generate_location_list(world=self)


    def create_regions(self) -> None:
        create_regions(world=self)
        connect_regions(world=self)
        self.set_completion_rule(Has(item_name=REGION_CHEST_EVENT_ITEM, count=6))


    def create_items(self) -> None:
        create_items(world=self)


    def fill_slot_data(self) -> Mapping[str, Any]:
        self.make_puml()
        return \
        {
            "Cell Count": self.options.cell_count.value,
        }


    def make_puml(self) -> None:
        if self.player_name[0:1].isdigit():
            return

        from Utils import visualize_regions
        temp_state: CollectionState = self.multiworld.get_all_state()
        temp_state.update_reachable_regions(self.player)

        reachable_regions: set[Region] = set(temp_state.reachable_regions[self.player])
        unreachable_regions: set[Region] = set()
        for region in self.multiworld.regions:
            if region not in reachable_regions:
                unreachable_regions.add(region)

        visualize_regions(self.get_region(self.origin_region_name), f"{self.player_name}_world.puml", show_entrance_names=True, regions_to_highlight=unreachable_regions)
