# HeroClassData.py
"""
Data definitions for hero classes.
"""
class HeroClassData:
    data = {
        "Warrior": {
            "sprite": "assets/warrior.png",
            "skills": {"strength": 8, "intelligence": 3, "agility": 5},
            "special_text": "Warrior Berserk activated: You charge with extra might!",
            "special_effect": lambda self: self.increase_strength(3),
            "passive_bonus": 1
        },
        "Mage": {
            "sprite": "assets/mage.png",
            "skills": {"strength": 3, "intelligence": 8, "agility": 5},
            "special_text": "Mage Spell Cast activated: Unleash a burst of arcane energy!",
            "special_effect": lambda self: self.cast_spell(),
            "passive_bonus": 2
        },
        "Rogue": {
            "sprite": "assets/rogue.png",
            "skills": {"strength": 5, "intelligence": 4, "agility": 8},
            "special_text": "Rogue Stealth activated: You vanish into the shadows!",
            "special_effect": lambda self: self.enter_stealth(),
            "passive_bonus": 1
        },
        "Engineer": {
            "sprite": "assets/engineer.png",
            "skills": {"strength": 4, "intelligence": 7, "agility": 5},
            "special_text": "Engineer Gadget deployed: A drone assists you!",
            "special_effect": lambda self: self.deploy_drone(),
            "passive_bonus": 2
        },
        "Artist": {
            "sprite": "assets/artist.png",
            "skills": {"strength": 4, "intelligence": 5, "agility": 6},
            "special_text": "Artist Inspiration activated: Your art dazzles enemies!",
            "special_effect": lambda self: self.inspire_art(),
            "passive_bonus": 1
        }
    }
