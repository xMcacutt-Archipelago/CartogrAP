"""
Items
"""
import dataclasses
import enum
from math import ceil
from typing import ClassVar, Self

from BaseClasses import Item, ItemClassification

from .constants import *
from .world_base import CartogrAPWorldBase


class CartogrAPItem(Item):
    game: str = GAME_NAME


@dataclasses.dataclass(frozen=True)
class ItemData:
    item_name: str
    code: int
    classification: ItemClassification
    amount: int = 1


def get_item_with_right_classification(world: CartogrAPWorldBase, item_name: str) -> CartogrAPItem:
    """returns the item when provided the name"""
    filtered_item_list: list[CartogrAPItems] = [item for item in CartogrAPItems if item.item_name == item_name]
    # print(f"item_name: {item_name}")
    return CartogrAPItem(name=filtered_item_list[0].item_name, code=filtered_item_list[0].code, classification=filtered_item_list[0].classification, player=world.player)


def get_cell_item_name(cell_type: CellType) -> str:
    """returns the cell item name when provided the cell type"""
    match cell_type:
        case CellType.PLAIN_CELL:
            return PLAIN_CELL_ITEM_NAME
        case CellType.FOREST_CELL:
            return FOREST_CELL_ITEM_NAME
        case CellType.MOUNTAIN_CELL:
            return MOUNTAIN_CELL_ITEM_NAME
        case CellType.OCEAN_CELL:
            return OCEAN_CELL_ITEM_NAME
        case CellType.CAVE_CELL:
            return CAVE_CELL_ITEM_NAME
        case CellType.SKY_CELL:
            return SKY_CELL_ITEM_NAME


def get_region_chest_key_item_name(cell_type: CellType) -> str:
    """returns the region chest key item name when provided the cell type"""
    match cell_type:
        case CellType.PLAIN_CELL:
            return PLAIN_KEY_ITEM_NAME
        case CellType.FOREST_CELL:
            return FOREST_KEY_ITEM_NAME
        case CellType.MOUNTAIN_CELL:
            return MOUNTAIN_KEY_ITEM_NAME
        case CellType.OCEAN_CELL:
            return OCEAN_KEY_ITEM_NAME
        case CellType.CAVE_CELL:
            return CAVE_KEY_ITEM_NAME
        case CellType.SKY_CELL:
            return SKY_KEY_ITEM_NAME


def create_items(world: CartogrAPWorldBase) -> None:
    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))
    print(f"total_location_count: {total_location_count}")
    for item in CartogrAPItems:
        if item.classification is ItemClassification.progression:
            if item.amount > 0:
                for _ in range(item.amount):
                    world.multiworld.itempool.append(world.create_item(name=item.item_name))
                    total_location_count -= 1
            elif item.item_name == PLAIN_CELL_ITEM_NAME:
                for _ in range(ceil((world.plain_cell_count - STARTING_CELLS_REVEALED) / CELL_ITEM_UNLOCKS)):
                    world.multiworld.itempool.append(world.create_item(name=item.item_name))
                    total_location_count -= 1
            else:
                for _ in range(ceil(world.other_cell_type_count / CELL_ITEM_UNLOCKS)):
                    world.multiworld.itempool.append(world.create_item(name=item.item_name))
                    total_location_count -= 1

    # print(f"filler to place: {total_location_count}")
    for _ in range(total_location_count):
        world.multiworld.itempool.append(world.create_item(name=world.get_filler_item_name()))
        total_location_count -= 1


class CartogrAPItems(enum.Enum):
    # NOTHING = ItemData(item_name=NOTHING_ITEM_NAME, code=0x1, classification=ItemClassification.progression, amount=0) # <- plain region needs no item
    PLAIN_CELL = ItemData(item_name=get_cell_item_name(CellType.PLAIN_CELL), code=0x2, classification=ItemClassification.progression, amount=-1)
    PLAIN_KEY = ItemData(item_name=get_region_chest_key_item_name(CellType.PLAIN_CELL), code=0x3, classification=ItemClassification.progression)

    AXE = ItemData(item_name=AXE_ITEM_NAME, code=0x11, classification=ItemClassification.progression)
    FOREST_CELL = ItemData(item_name=get_cell_item_name(CellType.FOREST_CELL), code=0x12, classification=ItemClassification.progression, amount=-1)
    FOREST_KEY = ItemData(item_name=get_region_chest_key_item_name(CellType.FOREST_CELL), code=0x13, classification=ItemClassification.progression)

    PICKAXE = ItemData(item_name=PICKAXE_ITEM_NAME, code=0x21, classification=ItemClassification.progression)
    MOUNTAIN_CELL = ItemData(item_name=get_cell_item_name(CellType.MOUNTAIN_CELL), code=0x22, classification=ItemClassification.progression, amount=-1)
    MOUNTAIN_KEY = ItemData(item_name=get_region_chest_key_item_name(CellType.MOUNTAIN_CELL), code=0x23, classification=ItemClassification.progression)

    BOAT = ItemData(item_name=BOAT_ITEM_NAME, code=0x31, classification=ItemClassification.progression)
    OCEAN_CELL = ItemData(item_name=get_cell_item_name(CellType.OCEAN_CELL), code=0x32, classification=ItemClassification.progression, amount=-1)
    OCEAN_KEY = ItemData(item_name=get_region_chest_key_item_name(CellType.OCEAN_CELL), code=0x33, classification=ItemClassification.progression)

    LANTERN = ItemData(item_name=LANTERN_ITEM_NAME, code=0x41, classification=ItemClassification.progression)
    CAVE_CELL = ItemData(item_name=get_cell_item_name(CellType.CAVE_CELL), code=0x42, classification=ItemClassification.progression, amount=-1)
    CAVE_KEY = ItemData(item_name=get_region_chest_key_item_name(CellType.CAVE_CELL), code=0x43, classification=ItemClassification.progression)

    LADDER = ItemData(item_name=LADDER_ITEM_NAME, code=0x51, classification=ItemClassification.progression)
    SKY_CELL = ItemData(item_name=get_cell_item_name(CellType.SKY_CELL), code=0x52, classification=ItemClassification.progression, amount=-1)
    SKY_KEY = ItemData(item_name=get_region_chest_key_item_name(CellType.SKY_CELL), code=0x53, classification=ItemClassification.progression)


    FILLER_ITEM = ItemData(item_name=FILLER_ITEM_NAME, code=0x100, classification=ItemClassification.filler)

    TRAP_ITEM = ItemData(item_name=TRAP_ITEM_NAME, code=0x200, classification=ItemClassification.trap)

    def __new__(cls, item_data: ItemData) -> Self:
        obj = object.__new__(cls)
        obj._value_ = item_data
        return obj

    def __init__(self, item_data: ItemData) -> None:
        self.item_name: str = item_data.item_name
        self.code: int = item_data.code
        self.classification: ItemClassification = item_data.classification
        self.amount: int = item_data.amount



