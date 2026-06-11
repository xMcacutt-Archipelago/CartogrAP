"""
Locations
"""
import dataclasses
import enum
from math import floor, ceil
from unittest import case

from BaseClasses import Location, LocationProgressType
from rule_builder.rules import Rule, Has, True_

from .constants import CellType, GAME_NAME, LocationLayer, PLAIN_CELL_REGION, \
    REGION_CHEST_EVENT_ITEM, get_region_name_for_cell_type, CELL_UNLOCK_EVENT_ITEM, CELLS_NEEDED_PER_SHOP_ITEM, \
    CellObject, CellObjectType, CHANCE_TO_EXCLUDE_FISH_LOCATION, FISH_LOCATION_START_ID
from .options import CellCount
from .rules import get_default_true_rule, CanCutTree, HasCellSpawned, CanUnlockChest, get_rule_for_cell_object
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


@dataclasses.dataclass(kw_only=True, frozen=True)
class _FishData:
    fish_name: str
    spawn_weight: int



class Fish(enum.Enum):
    LARGEMOUTH_BASS = _FishData(fish_name="Largemouth Bass", spawn_weight=100)
    BLUEGILL = _FishData(fish_name="Bluegill", spawn_weight=100)
    KOKANEE_SALMON = _FishData(fish_name="Kokanee Salmon", spawn_weight=70)
    BLACK_BULLHEAD_CATFISH = _FishData(fish_name="Black Bullhead Catfish", spawn_weight=50)
    RAINBOW_TROUT = _FishData(fish_name="Rainbow Trout", spawn_weight=40)
    GOLDEN_TROUT = _FishData(fish_name="Golden Trout", spawn_weight=20)
    ARCTIC_GRAYLING = _FishData(fish_name="Arctic Grayling", spawn_weight=15)
    DERP_FISH = _FishData(fish_name="Derp Fish", spawn_weight=5)
    CAT_IN_QUOTATION_MARKS_FISH = _FishData(fish_name="Cat In Quotation Marks Fish", spawn_weight=1)


    def __new__(cls, fish_data: _FishData):
        obj = object.__new__(cls)
        obj._value_ = fish_data
        return obj


    def __init__(self, fish_data: _FishData):
        self.fish_name = fish_data.fish_name
        self.spawn_weight = fish_data.spawn_weight


    def get_spawn_chance(self) -> float:
        total_spawn_weight: int = sum([fish_data.spawn_weight for fish_data in Fish])
        return self.spawn_weight / total_spawn_weight


    def should_exclude_location(self) -> bool:
        return self.get_spawn_chance() <= CHANCE_TO_EXCLUDE_FISH_LOCATION



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


    # fish locations
    _location_data += generate_fish_locations()

    # _location_data += generate_locations_for_shop_region(total_cell_count=starting_region_cell_count + (other_region_cell_count * (len(CellType) - 1)))
    return _location_data


def generate_locations_for_cell_region(cell_count: int, cell_type: CellType) -> list[LocationData]:
    location_data: list[LocationData] = []
    layer: LocationLayer = LocationLayer.ABOVE_LAYER if cell_type is CellType.SKY_CELL else LocationLayer.BELOW_LAYER if cell_type is CellType.CAVE_CELL else LocationLayer.STARTING_LAYER
    total_object_count: int = CellObject.get_total_object_count()
    object_index_increment: float = cell_count / total_object_count
    object_indices: list[int] = [floor(object_index_increment * (x + 1)) for x in range(total_object_count)]
    for x in range(cell_count):
        loc_data: LocationData = LocationData(loc_name=f"{cell_type.cell_type_name} #{x + 1}", code=CellObject.NONE.get_id_offset(cell_type) + 0x1 + x, region=get_region_name_for_cell_type(cell_type=cell_type), layer=layer, rule=HasCellSpawned(cell_type=cell_type, cell_index=x))
        location_data.append(loc_data)

        # Cell Event Location
        if x + 1 in object_indices:
            object_index: int = object_indices.index(x + 1)
            cell_object: CellObject = CellObject.get_object_for_index(object_index)
            cell_object_index: int = cell_object.object_indices.index(object_index)
            loc_name: str = f"{cell_type.cell_type_name} {cell_object.object_name}"
            loc_id: int = cell_object.get_id_offset(cell_type) + 0x1 + cell_object.object_extra_id_offset + cell_object_index
            if len(cell_object.object_indices) > 1:
                loc_name += f" {cell_object_index + 1}"
            loc_data: LocationData = LocationData(loc_name=loc_name, code=loc_id, region=get_region_name_for_cell_type(cell_type=cell_type), layer=layer, rule=get_rule_for_cell_object(cell_object, cell_type, x))
            location_data.append(loc_data)
    loc_data: LocationData = LocationData(loc_name=f"{cell_type.cell_type_name} Region Chest Event Location", code=None, region=get_region_name_for_cell_type(cell_type=cell_type), layer=layer, rule=CanUnlockChest(cell_type=cell_type, cell_index=cell_count - 1, cell_object=CellObject.CHEST_REGION), locked_item=REGION_CHEST_EVENT_ITEM)
    location_data.append(loc_data)
    return location_data


# def generate_locations_for_shop_region(total_cell_count: int) -> list[LocationData]:
#     _location_data: list[LocationData] = []
#     for x in range(floor(total_cell_count / CELLS_NEEDED_PER_SHOP_ITEM)):
#         loc_data: LocationData = LocationData(loc_name=f"{(x + 1) * CELLS_NEEDED_PER_SHOP_ITEM} Cells Shop Item", code=0x20000 + 0x1 + x, region=SHOP_REGION, layer=LocationLayer.STARTING_LAYER, rule=Has(item_name=CELL_UNLOCK_EVENT_ITEM, count=(x + 1) * CELLS_NEEDED_PER_SHOP_ITEM))
#         _location_data.append(loc_data)
#     return _location_data



def generate_fish_locations() -> list[LocationData]:
    # loc_name: str
    # code: int | None
    # region: str
    # rule: Rule[CartogrAPWorldBase] = dataclasses.field(default_factory=get_default_true_rule)
    # layer: LocationLayer = LocationLayer.STARTING_LAYER
    # locked_item: str | None = None
    # progress_type: LocationProgressType = LocationProgressType.DEFAULT

    _result: list[LocationData] = []
    for index, fish in enumerate(Fish):
        loc_progress_type: LocationProgressType = LocationProgressType.EXCLUDED if fish.should_exclude_location() else LocationProgressType.DEFAULT
        loc_data = LocationData(loc_name=f"Catch {fish.fish_name}", code=FISH_LOCATION_START_ID + index, region=get_region_name_for_cell_type(cell_type=CellType.OCEAN_CELL), rule=HasCellSpawned(cell_type=CellType.OCEAN_CELL, cell_index=0), progress_type=loc_progress_type)
        _result.append(loc_data)

    return _result






FULL_LOCATION_LIST: list[LocationData] = generate_location_list()

