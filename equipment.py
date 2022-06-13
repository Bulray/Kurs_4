from dataclasses import dataclass, field
from typing import List, Optional
from random import uniform

import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    max_damage: float
    min_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, arg: Optional[Weapon] = None) -> None:
        for weapon in self.equipment.weapons:
            if weapon.name == arg:
                return weapon

    def get_armor(self, var: Optional[Armor] = None) -> None:
        for armor in self.equipment.armors:
            if armor.name == var:
                return armor

    def get_weapons_names(self) -> list:
        return [item.name for item in self.equipment.weapons]

    def get_armors_names(self) -> list:
        return [item.name for item in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        equipment_file = open("data/equipment.json", encoding="utf-8")
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
