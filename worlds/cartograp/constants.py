"""
Constants used by the APWorld
"""
import enum

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
PICKAXE_ITEM_NAME: str = "Pickaxe"
MOUNTAIN_CELL_ITEM_NAME: str = "Mountain Cell"
MOUNTAIN_KEY_ITEM_NAME: str = "Mountain Key"
MOUNTAIN_CELL_REGION: str = "Mountain Region"
BOAT_ITEM_NAME: str = "Boat"
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
FILLER_ITEM_NAME: str = "Filler Item"
TRAP_ITEM_NAME: str = "Trap Item"

MENU_REGION: str = "Menu"
REGION_CHEST_EVENT_ITEM: str = "Region Chest Event Item"
STARTING_CELLS_REVEALED: int = 200
CELL_ITEM_UNLOCKS: int = 1




class CellType(enum.StrEnum):
    PLAIN_CELL = "Plain Cell"
    FOREST_CELL = "Forest Cell"
    MOUNTAIN_CELL = "Mountain Cell"
    OCEAN_CELL = "Ocean Cell"
    CAVE_CELL = "Cave Cell"
    SKY_CELL = "Sky Cell"


class LocationLayer(enum.Enum):
    STARTING_LAYER = "Starting Layer"
    ABOVE_LAYER = "Above Layer"
    BELOW_LAYER = "Below Layer"


class QuestType(enum.StrEnum):
    SPEED_RUN = "Speedrun"
    SHORTEST_PATH = "Shortest Path"
    TREASURE_HUNT = "Treasure Hunt"


class ChestType(enum.StrEnum):
    UNLOCKED_CHEST = "Unlocked Chest"
    REGION_CHEST = "Region Chest"





def get_region_name_for_cell_type(cell_type: CellType) -> str:
    """returns the region chest key item name when provided the cell type"""
    match cell_type:
        case CellType.PLAIN_CELL:
            return PLAIN_CELL_REGION
        case CellType.FOREST_CELL:
            return FOREST_CELL_REGION
        case CellType.MOUNTAIN_CELL:
            return MOUNTAIN_CELL_REGION
        case CellType.OCEAN_CELL:
            return OCEAN_CELL_REGION
        case CellType.CAVE_CELL:
            return CAVE_CELL_REGION
        case CellType.SKY_CELL:
            return SKY_CELL_REGION