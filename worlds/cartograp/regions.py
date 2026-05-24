"""
Regions
"""
from BaseClasses import Region, Location, Entrance, Item, ItemClassification
from rule_builder.rules import Rule, True_

from .constants import *
from .locations import FULL_LOCATION_LIST
from .rules import CanCutTree, CanBreakRock, CanGoOverWater, CanSeeInDark, CanAccessTopLayer
from .world_base import CartogrAPWorldBase


def create_region(world: CartogrAPWorldBase, region_name: str) -> None:
    region: Region = Region(name=region_name, player=world.player, multiworld=world.multiworld)
    for loc_data in world.location_list:
        if loc_data.region == region_name:
            location: Location = Location(name=loc_data.loc_name, player=world.player, address=loc_data.code, parent=region)
            world.set_rule(spot=location, rule=loc_data.rule)
            location.progress_type = loc_data.progress_type
            if loc_data.locked_item is not None:
                location.place_locked_item(Item(name=loc_data.locked_item, classification=ItemClassification.progression, code=None, player=world.player))
            region.locations.append(location)
    world.multiworld.regions.append(region)


def create_regions(world: CartogrAPWorldBase) -> None:
    create_region(world=world, region_name=MENU_REGION)
    for cell_type in CellType:
        create_region(world=world, region_name=get_region_name_for_cell_type(cell_type=cell_type))


def connect_region_to_region(world: CartogrAPWorldBase, source: str, target: str, rule: Rule[CartogrAPWorldBase]) -> None:
    source_region: Region = world.get_region(source)
    target_region: Region = world.get_region(target)
    entrance: Entrance = source_region.connect(connecting_region=target_region, name=f"{source} -> {target}")
    world.set_rule(spot=entrance, rule=rule)


def connect_regions(world: CartogrAPWorldBase) -> None:
    connect_region_to_region(world=world, source=MENU_REGION, target=PLAIN_CELL_REGION, rule=True_[CartogrAPWorldBase]())
    connect_region_to_region(world=world, source=PLAIN_CELL_REGION, target=FOREST_CELL_REGION, rule=CanCutTree())
    connect_region_to_region(world=world, source=PLAIN_CELL_REGION, target=MOUNTAIN_CELL_REGION, rule=CanBreakRock())
    connect_region_to_region(world=world, source=PLAIN_CELL_REGION, target=OCEAN_CELL_REGION, rule=CanGoOverWater())
    connect_region_to_region(world=world, source=PLAIN_CELL_REGION, target=CAVE_CELL_REGION, rule=CanSeeInDark())
    connect_region_to_region(world=world, source=PLAIN_CELL_REGION, target=SKY_CELL_REGION, rule=CanAccessTopLayer())
