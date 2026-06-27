"""
Main World class
"""
from typing import ClassVar, override, Mapping, Any

from BaseClasses import MultiWorld, ItemClassification, CollectionState, Region, Item
from NetUtils import MultiData
from Options import Option
from rule_builder.rules import Has

from .constants import GAME_NAME, REGION_CHEST_EVENT_ITEM, REGION_CHESTS_NEEDED_FOR_GOAL
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
    ut_can_gen_without_yaml: ClassVar[bool] = True

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        return slot_data


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld=multiworld, player=player)

        self.is_ut_gen: bool = False

        self.location_list: list[LocationData] = []
        self.items_created_dict: dict[str, int] = {}

        self.cell_type_sphere_data: dict[int, dict[int, list[tuple[int, int]]]] = {}
        """dict of cell_item_id to dict of sphere to list of tuple of player and location id"""


    @override
    def get_filler_item_name(self) -> str:
        return self.random.choice([item.item_name for item in CartogrAPItems if item.classification is ItemClassification.filler])


    @override
    def create_item(self, name: str) -> CartogrAPItem:
        return get_item_with_right_classification(world=self, item_name=name)


    def generate_early(self) -> None:
        self.handle_ut_gen()
        super().generate_early()
        self.location_list = generate_location_list(world=self)


    def create_regions(self) -> None:
        create_regions(world=self)
        connect_regions(world=self)
        self.set_completion_rule(Has(item_name=REGION_CHEST_EVENT_ITEM, count=REGION_CHESTS_NEEDED_FOR_GOAL))


    def create_items(self) -> None:
        create_items(world=self)


    def modify_multidata(self, multidata: MultiData) -> None:

        # sphere
        # list[dict[int, set[int]]]
        # list of spheres
        # dict key is player

        #location_data
        # dict[int, dict[int, tuple[int, int, int]]]
        # first int player
        # second int loc ID
        # item id, item player, item flags

        # dict of cell_item_id to dict of sphere to list of tuple of player and location id

        cell_types: list[CartogrAPItems] = CartogrAPItems.get_unique_cell_items()

        for cell_type in cell_types:
            self.cell_type_sphere_data[cell_type.code] = {}

            for sphere_index, sphere in enumerate(multidata["spheres"]):
                self.cell_type_sphere_data[cell_type.code][sphere_index + 1] = []
                for sphere_player, loc_list in sphere.items():
                    for loc_id in loc_list:
                        item_id, item_player, item_flags = multidata["locations"][sphere_player][loc_id]
                        if item_player != self.player or item_id != cell_type.code:
                            continue

                        self.cell_type_sphere_data[cell_type.code][sphere_index + 1].append((sphere_player, loc_id))


    def fill_slot_data(self) -> Mapping[str, Any]:
        #self.make_puml()

        # dict of celltype to dict of sphere to tuple of player and location id


        return \
        {
            "Cell Count": self.options.cell_count.value,
            "Cell Item Sphere Data": self.cell_type_sphere_data
        }


    def handle_ut_gen(self) -> None:
        re_gen_passthrough: dict[str, dict[str, Any]] | None = getattr(self.multiworld, "re_gen_passthrough", {})
        if not re_gen_passthrough or not self.game in re_gen_passthrough:
            return
        self.is_ut_gen = True
        slot_data: dict[str, Any] = re_gen_passthrough[self.game]  # pyright: ignore[reportExplicitAny]
        self.options.cell_count.value = slot_data["Cell Count"]
        self.cell_type_sphere_data = slot_data["Cell Item Sphere Data"]


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
