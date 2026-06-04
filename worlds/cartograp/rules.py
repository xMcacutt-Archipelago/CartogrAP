"""
Rules here
"""
import dataclasses
from math import floor, ceil
from typing import override
from unittest import case

from rule_builder.rules import Rule, True_, TWorld, Has, HasFromList, False_

from .constants import GAME_NAME, CellType, PLAIN_CELL_ITEM_NAME, FOREST_CELL_ITEM_NAME, BOG_CELL_ITEM_NAME, \
    OCEAN_CELL_ITEM_NAME, STARTING_CELLS_REVEALED, CELL_ITEM_UNLOCKS, CellObject
from .items import CartogrAPItems, get_cell_item_name, get_region_chest_key_item_name
from .world_base import CartogrAPWorldBase


def get_default_true_rule() -> Rule[CartogrAPWorldBase]:
    return True_[CartogrAPWorldBase]()


def get_rule_for_cell_object(cell_object: CellObject, cell_type: CellType, cell_index: int) -> Rule[CartogrAPWorldBase]:
    rule: Rule[CartogrAPWorldBase] = HasCellSpawned(cell_type=cell_type, cell_index=cell_index)
    if cell_object is CellObject.CHEST_REGION:
        rule &= CanUnlockChest(cell_object=cell_object, cell_type=cell_type, cell_index=cell_index)
    return rule


@dataclasses.dataclass(kw_only=True)
class HasCellSpawned(Rule[CartogrAPWorldBase], game=GAME_NAME):
    cell_type: CellType
    cell_index: int

    @override
    def _instantiate(self, world: CartogrAPWorldBase) -> Rule.Resolved:
        return self.get_cell_item_rule().resolve(world=world)

    def _get_required_cell_name_amount(self) -> tuple[str, int]:
        cell_items_needed: int = self.cell_index + 1

        if self.cell_type is CellType.PLAIN_CELL:
            # starting cells
            cell_items_needed -= STARTING_CELLS_REVEALED

        return get_cell_item_name(cell_type=self.cell_type), ceil(cell_items_needed / CELL_ITEM_UNLOCKS)

    def get_cell_item_rule(self) -> Rule[CartogrAPWorldBase]:
        cell_item_name, cell_items_needed = self._get_required_cell_name_amount()

        if cell_items_needed < 1:
            return True_[CartogrAPWorldBase]()
        return Has(item_name=cell_item_name, count=cell_items_needed)


@dataclasses.dataclass(kw_only=True)
class CanUnlockChest(HasCellSpawned, game=GAME_NAME):
    cell_object: CellObject

    @override
    def _instantiate(self, world: CartogrAPWorldBase) -> Rule.Resolved:
        return (self.get_cell_item_rule() & self.get_chest_key_item_rule()).resolve(world=world)

    def _get_required_key_name(self) -> str:
        return get_region_chest_key_item_name(self.cell_type)

    def get_chest_key_item_rule(self) -> Rule[CartogrAPWorldBase]:
        match self.cell_object:
            case CellObject.CHEST_UNLOCKED:
                return True_[CartogrAPWorldBase]()
            case CellObject.CHEST_REGION:
                return Has(item_name=get_region_chest_key_item_name(self.cell_type))
            case _:
                return False_[CartogrAPWorldBase]()


@dataclasses.dataclass(kw_only=True)
class CanCutTree(Rule[CartogrAPWorldBase], game=GAME_NAME):

    @override
    def _instantiate(self, world: CartogrAPWorldBase) -> Rule.Resolved:
        return Has(CartogrAPItems.AXE.item_name).resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class CanBreakRock(Rule[CartogrAPWorldBase], game=GAME_NAME):

    @override
    def _instantiate(self, world: CartogrAPWorldBase) -> Rule.Resolved:
        return Has(CartogrAPItems.WELLIES.item_name).resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class CanGoOverWater(Rule[CartogrAPWorldBase], game=GAME_NAME):

    @override
    def _instantiate(self, world: CartogrAPWorldBase) -> Rule.Resolved:
        return Has(CartogrAPItems.BOAT.item_name).resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class CanSeeInDark(Rule[CartogrAPWorldBase], game=GAME_NAME):

    @override
    def _instantiate(self, world: CartogrAPWorldBase) -> Rule.Resolved:
        return Has(CartogrAPItems.LANTERN.item_name).resolve(world=world)


@dataclasses.dataclass(kw_only=True)
class CanAccessTopLayer(Rule[CartogrAPWorldBase], game=GAME_NAME):

    @override
    def _instantiate(self, world: CartogrAPWorldBase) -> Rule.Resolved:
        return Has(CartogrAPItems.LADDER.item_name).resolve(world=world)










