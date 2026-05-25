"""
Locations
"""
import dataclasses
import enum
from math import floor, ceil
from unittest import case

from BaseClasses import Location, LocationProgressType
from rule_builder.rules import Rule, Has

from .constants import CellType, GAME_NAME, LocationLayer, QuestType, ChestType, PLAIN_CELL_REGION, \
    REGION_CHEST_EVENT_ITEM, get_region_name_for_cell_type, CELL_UNLOCK_EVENT_ITEM, CELLS_NEEDED_PER_SHOP_ITEM, \
    SHOP_REGION
from .options import CellCount
from .rules import get_default_true_rule, CanCutTree, HasCellSpawned, CanUnlockChest
from .world_base import CartogrAPWorldBase


@dataclasses.dataclass(frozen=True)
class LocationData:
    loc_name: str
    code: int | None
    region: str
    rule: Rule[CartogrAPWorldBase] = dataclasses.field(default_factory=get_default_true_rule)
    layer: LocationLayer = LocationLayer.STARTING_LAYER
    locked_item: str | None = None
    progress_type: LocationProgressType = LocationProgressType.DEFAULT


def get_id_offset(cell_type: CellType, is_quest_or_chest: bool = False) -> int:
    if is_quest_or_chest:
        match cell_type:
            case CellType.PLAIN_CELL:
                return 0x10000
            case CellType.FOREST_CELL:
                return 0x11000
            case CellType.MOUNTAIN_CELL:
                return 0x12000
            case CellType.OCEAN_CELL:
                return 0x13000
            case CellType.CAVE_CELL:
                return 0x14000
            case CellType.SKY_CELL:
                return 0x15000

    else:
        match cell_type:
            case CellType.PLAIN_CELL:
                return 0
            case CellType.FOREST_CELL:
                return 0x1000
            case CellType.MOUNTAIN_CELL:
                return 0x2000
            case CellType.OCEAN_CELL:
                return 0x3000
            case CellType.CAVE_CELL:
                return 0x4000
            case CellType.SKY_CELL:
                return 0x5000


def get_region_cell_counts(world: CartogrAPWorldBase | None = None) -> tuple[int, int]:
    max_cell_count: int = CellCount.max_value()
    if world is not None:
        max_cell_count = world.options.cell_count.value
    starting_region_cell_count: int = int(max_cell_count / 5)
    other_region_cell_count: int = int((max_cell_count - starting_region_cell_count) / 5)
    if world is not None:
        # print(f"Starting Region: {starting_region_cell_count} Cells. Other Regions: {other_region_cell_count} Cells")
        for cell_type in CellType:
            match cell_type:
                case CellType.PLAIN_CELL:
                    world.plain_cell_count = starting_region_cell_count
                case _:
                    world.other_cell_type_count = other_region_cell_count

    return starting_region_cell_count, other_region_cell_count

        # 1 starting cell
        # 25 unlocked by default
        # 174 plain cells

        # 5 chests (4 + 1 region)
        # 3 quests
        # / 8 (round down)

        # 1 chest
        # 1 quest (speedrun)
        # 2 chest
        # 2 quest (path then treasure)
        # 1 chest
        # 1 region chest

        # event on last cell of all regions
        # goal


def generate_location_list(world: CartogrAPWorldBase | None = None) -> list[LocationData]:
    _location_data: list[LocationData] = []
    starting_region_cell_count, other_region_cell_count = get_region_cell_counts(world=world)

    for cell_type in CellType:
        if cell_type is CellType.PLAIN_CELL:
            _location_data += generate_locations_for_cell_region(cell_count=starting_region_cell_count, cell_type=cell_type)
        else:
            _location_data += generate_locations_for_cell_region(cell_count=other_region_cell_count, cell_type=cell_type)

    # _location_data += generate_locations_for_shop_region(total_cell_count=starting_region_cell_count + (other_region_cell_count * (len(CellType) - 1)))
    return _location_data


def generate_locations_for_cell_region(cell_count: int, cell_type: CellType) -> list[LocationData]:
    location_data: list[LocationData] = []
    special_feature_indexes: dict[int, QuestType | ChestType] = get_cell_indexes_for_special_cells(cell_count)
    cell_id_offset: int = get_id_offset(cell_type)
    quest_chest_id_offset: int = get_id_offset(cell_type, is_quest_or_chest=True)
    layer: LocationLayer = LocationLayer.ABOVE_LAYER if cell_type is CellType.SKY_CELL else LocationLayer.BELOW_LAYER if cell_type is CellType.CAVE_CELL else LocationLayer.STARTING_LAYER

    for x in range(cell_count):
        loc_data: LocationData = LocationData(loc_name=f"{cell_type.value} #{x + 1}", code=cell_id_offset + 0x1 + x, region=get_region_name_for_cell_type(cell_type=cell_type), layer=layer, rule=HasCellSpawned(cell_type=cell_type, cell_index=x))
        location_data.append(loc_data)

        # Cell Event Location
        # loc_data: LocationData = LocationData(loc_name=f"{cell_type.value} Unlock #{x + 1} Event Location", code=None, region=get_region_name_for_cell_type(cell_type=cell_type), layer=layer, rule=HasCellSpawned(cell_type=cell_type, cell_index=x), locked_item=CELL_UNLOCK_EVENT_ITEM)
        # location_data.append(loc_data)

        if x in special_feature_indexes.keys():
            x_index: int = list(special_feature_indexes.keys()).index(x)
            if isinstance(special_feature_indexes[x], QuestType):
                loc_data: LocationData = LocationData(loc_name=f"{cell_type.value} {special_feature_indexes[x].value} Quest", code=quest_chest_id_offset + 0x1 + x_index, region=get_region_name_for_cell_type(cell_type=cell_type), layer=layer, rule=HasCellSpawned(cell_type=cell_type, cell_index=x))
            elif isinstance(special_feature_indexes[x], ChestType):
                match special_feature_indexes[x]:
                    case ChestType.UNLOCKED_CHEST:
                        chest_indexes: list[int] = [0, 2, 3, 6]
                        chest_number: int = chest_indexes.index(round(x / (cell_count / 8)) - 1)
                        loc_data: LocationData = LocationData(loc_name=f"{cell_type.value} {special_feature_indexes[x].value} #{chest_number + 1}", code=quest_chest_id_offset + 0x1 + x_index, region=get_region_name_for_cell_type(cell_type=cell_type), layer=layer, rule=CanUnlockChest(cell_type=cell_type, cell_index=x, chest_type=ChestType.UNLOCKED_CHEST))
                    case ChestType.REGION_CHEST:
                        loc_data: LocationData = LocationData(loc_name=f"{cell_type.value} {special_feature_indexes[x].value}", code=quest_chest_id_offset + 0x1 + x_index, region=get_region_name_for_cell_type(cell_type=cell_type), layer=layer, rule=CanUnlockChest(cell_type=cell_type, cell_index=x, chest_type=ChestType.REGION_CHEST))
            else:
                raise ValueError(f"Unknown feature type in special features: {special_feature_indexes[x]}")
            location_data.append(loc_data)

    loc_data: LocationData = LocationData(loc_name=f"{cell_type.value} Region Chest Event Location", code=None, region=get_region_name_for_cell_type(cell_type=cell_type), layer=layer, rule=CanUnlockChest(cell_type=cell_type, cell_index=cell_count - 1, chest_type=ChestType.REGION_CHEST), locked_item=REGION_CHEST_EVENT_ITEM)
    location_data.append(loc_data)
    return location_data


# def generate_locations_for_shop_region(total_cell_count: int) -> list[LocationData]:
#     _location_data: list[LocationData] = []
#     for x in range(floor(total_cell_count / CELLS_NEEDED_PER_SHOP_ITEM)):
#         loc_data: LocationData = LocationData(loc_name=f"{(x + 1) * CELLS_NEEDED_PER_SHOP_ITEM} Cells Shop Item", code=0x20000 + 0x1 + x, region=SHOP_REGION, layer=LocationLayer.STARTING_LAYER, rule=Has(item_name=CELL_UNLOCK_EVENT_ITEM, count=(x + 1) * CELLS_NEEDED_PER_SHOP_ITEM))
#         _location_data.append(loc_data)
#     return _location_data


def get_cell_indexes_for_special_cells(region_cell_count: int) -> dict[int, QuestType | ChestType]:
    feature_index_increment: float | int = region_cell_count / 8
    # 1 chest
    # 1 quest (speedrun)
    # 2 chest
    # 2 quest (path then treasure)
    # 1 chest
    # 1 region chest
    return \
    {
        floor(feature_index_increment * 1): ChestType.UNLOCKED_CHEST,
        floor(feature_index_increment * 2): QuestType.SPEED_RUN,
        floor(feature_index_increment * 3): ChestType.UNLOCKED_CHEST,
        floor(feature_index_increment * 4): ChestType.UNLOCKED_CHEST,
        floor(feature_index_increment * 5): QuestType.SHORTEST_PATH,
        floor(feature_index_increment * 6): QuestType.TREASURE_HUNT,
        floor(feature_index_increment * 7): ChestType.UNLOCKED_CHEST,
        floor(feature_index_increment * 8): ChestType.REGION_CHEST,
    }


FULL_LOCATION_LIST: list[LocationData] = generate_location_list()

