"""
Constants used by the APWorld
"""
import enum
from typing import Self, Literal

from BaseClasses import LocationProgressType

GAME_NAME: str = "CartogrAP"
WEB_WORLD_THEME: str = "partyTime"

EN_TUTORIAL_NAME: str = "Multiworld Setup Guide"
EN_TUTORIAL_DESC: str = f"A guide to setting up the {GAME_NAME} randomizer connected to an Archipelago Multiworld."
EN_TUTORIAL_LANGUAGE: str = "English"
EN_TUTORIAL_FILENAME: str = "setup_en.md"
EN_TUTORIAL_LINK: str = "setup/en"
EN_TUTORIAL_AUTHORS: list[str] = ["EthicalLogic", "xMcacutt", "CallMeZero"]



NOTHING_ITEM_NAME: str = "Nothing"
PLAIN_CELL_ITEM_NAME: str = "Plain Cell"
PLAIN_KEY_ITEM_NAME: str = "Plain Key"
PLAIN_CELL_REGION: str = "Plain Region"
AXE_ITEM_NAME: str = "Axe"
FOREST_CELL_ITEM_NAME: str = "Forest Cell"
FOREST_KEY_ITEM_NAME: str = "Forest Key"
FOREST_CELL_REGION: str = "Forest Region"
WELLIES_ITEM_NAME: str = "Wellies"
BOG_CELL_ITEM_NAME: str = "Bog Cell"
BOG_KEY_ITEM_NAME: str = "Bog Key"
BOG_CELL_REGION: str = "Bog Region"
BOAT_ITEM_NAME: str = "Fishing Boat"
OCEAN_CELL_ITEM_NAME: str = "Ocean Cell"
OCEAN_KEY_ITEM_NAME: str = "Ocean Key"
OCEAN_CELL_REGION: str = "Ocean Region"
LANTERN_ITEM_NAME: str = "Lantern"
CAVE_CELL_ITEM_NAME: str = "Cave Cell"
CAVE_KEY_ITEM_NAME: str = "Cave Key"
CAVE_CELL_REGION: str = "Cave Region"
LADDER_ITEM_NAME: str = "Ladder"
SKY_CELL_ITEM_NAME: str = "Sky Cell"
SKY_KEY_ITEM_NAME: str = "Sky Key"
SKY_CELL_REGION: str = "Sky Region"
WIND_SHIELD_ITEM_NAME: str = "Wind Shield"
FILLER_ITEM_NAME: str = "Filler Item"

MONEY_ITEM_NAME: str = "Money"

TRAP_ITEM_NAME: str = "Trap Item"

MENU_REGION: str = "Menu"
REGION_CHEST_EVENT_ITEM: str = "Region Chest Event Item"
STARTING_CELLS_REVEALED: int = 25
CELL_ITEM_UNLOCKS: int = 2
REGION_CHESTS_NEEDED_FOR_GOAL: int = 6

CELLS_NEEDED_PER_SHOP_ITEM: int = 2
CELL_UNLOCK_EVENT_ITEM: str = "Cell Unlock Event Item"


FISH_LOCATION_START_ID: int = 0x20000
CHANCE_TO_EXCLUDE_FISH_LOCATION: float = 0.05


class CellType(enum.Enum):
    PLAIN_CELL = ("Plain Cell", 0)
    FOREST_CELL = ("Forest Cell", 1)
    BOG_CELL = ("Bog Cell", 2)
    OCEAN_CELL = ("Ocean Cell", 3)
    CAVE_CELL = ("Cave Cell", 4)
    SKY_CELL = ("Sky Cell", 5)

    def __init__(self, cell_type_name: str, cell_type_index: int):
        self.cell_type_name = cell_type_name
        self.cell_type_index = cell_type_index


class LocationLayer(enum.Enum):
    STARTING_LAYER = "Starting Layer"
    ABOVE_LAYER = "Above Layer"
    BELOW_LAYER = "Below Layer"


class CellObjectType(enum.Enum):
    NONE = -1
    QUEST = 0
    CHEST = 1


class CellObject(enum.Enum):
    NONE = ("", CellObjectType.NONE, [], None)
    QUEST_SPEEDRUN = ("Speedrun Quest", CellObjectType.QUEST, [1], 0)
    QUEST_PATH = ("Shortest Path Quest", CellObjectType.QUEST, [4], 1)
    QUEST_HUNT = ("Treasure Hunt Quest", CellObjectType.QUEST, [5], 2)
    CHEST_UNLOCKED = ("Unlocked Chest", CellObjectType.CHEST, [0, 2, 3, 6], 1)
    CHEST_REGION = ("Region Chest", CellObjectType.CHEST, [7], 0)

    def __init__(self, object_name: str, object_type: CellObjectType, object_indices: list[int], object_extra_id_offset: int):
        self.object_name = object_name
        self.object_type = object_type
        self.object_indices = object_indices
        self.object_extra_id_offset = object_extra_id_offset

    def get_id_offset(self, cell_type) -> int:
        if self.object_type is CellObjectType.NONE:
            return 0x1000 * cell_type.cell_type_index
        if self.object_type is CellObjectType.CHEST:
            return 0x10000 + 0x10 * cell_type.cell_type_index
        if self.object_type is CellObjectType.QUEST:
            return 0x10100 + 0x10 * cell_type.cell_type_index
        return -1


    def get_location_progress_type(self) -> LocationProgressType:
        # Priority Locations does not work when solo (as Cell Items are deprioritized)
        match self.object_type:
            case CellObjectType.NONE:
                return LocationProgressType.DEFAULT
            case CellObjectType.QUEST:
                return LocationProgressType.DEFAULT
            case CellObjectType.CHEST:
                return LocationProgressType.DEFAULT

    @classmethod
    def get_object_for_index(cls, index: int) -> Self:
        for cell_object in cls:
            if index in cell_object.object_indices:
                return cell_object
        return cls.NONE

    @classmethod
    def get_total_object_count(cls) -> int:
        count: int = 0
        for cell_object in cls:
            count += len(cell_object.object_indices)
        return count


def get_region_name_for_cell_type(cell_type: CellType) -> str:
    """returns the region chest key item name when provided the cell type"""
    match cell_type:
        case CellType.PLAIN_CELL:
            return PLAIN_CELL_REGION
        case CellType.FOREST_CELL:
            return FOREST_CELL_REGION
        case CellType.BOG_CELL:
            return BOG_CELL_REGION
        case CellType.OCEAN_CELL:
            return OCEAN_CELL_REGION
        case CellType.CAVE_CELL:
            return CAVE_CELL_REGION
        case CellType.SKY_CELL:
            return SKY_CELL_REGION


"""
MOVEMENT
Checkpoint filler (spawn checkpoint) (limit count apworld)
placeable bridge (limited amount) (much better) (non-ocean)
placeable checkpoint
placeable ladder
placeable downstairs


Color (something here)
audio filler?

charmy trap?

fast travel (prob not)


freeze trap
slow trap
rotate map trap
trap sends to start cell of region

"""







