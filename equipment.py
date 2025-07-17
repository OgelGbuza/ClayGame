# equipment.py
"""
Equipment module defining Equipment and its subclasses.
"""
class Equipment:
    def __init__(self, name, slot, bonuses):
        self.name = name
        self.slot = slot
        self.bonuses = bonuses
    def __str__(self):
        bonus_str = ", ".join([f"{stat}: {value}" for stat, value in self.bonuses.items()])
        return f"{self.name} ({self.slot}) [{bonus_str}]"

class Weapon(Equipment):
    def __init__(self, name, bonuses):
        super().__init__(name, "weapon", bonuses)

class Armor(Equipment):
    def __init__(self, name, bonuses):
        super().__init__(name, "armor", bonuses)

class Accessory(Equipment):
    def __init__(self, name, bonuses):
        super().__init__(name, "accessory", bonuses)
