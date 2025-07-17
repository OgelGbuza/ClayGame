# npc_dialogue.py
"""
ClassDependentNPC that loads external dialogue data if available.
"""
import pygame
import logging
from npc import NPC
from branching_dialogue_ui import BranchingDialogueUI
from data_loader import load_json

logger = logging.getLogger(__name__)

class ClassDependentNPC(NPC):
    def __init__(self, pos, name, sprite_path, dialogue_script=None, faction="wise", friendly_threshold=0):
        super().__init__(pos, name, sprite_path, dialogue_tree=None, behavior="static")
        self.faction = faction
        self.friendly_threshold = friendly_threshold
        self.interaction_prompt = f"Press E to talk to {self.name}"
        if dialogue_script is None:
            dialogue_script = load_json("dialogue_elder.json")
            if not dialogue_script:
                dialogue_script = {
                    "text": "Greetings, traveler. What do you seek?",
                    "choices": {
                        "A": "I seek wisdom.",
                        "B": "I seek power.",
                        "C": "I am merely passing through."
                    }
                }
        self.dialogue_script = dialogue_script

    def interact(self, player):
        if player.char_class == "Warrior":
            class_line = "Ah, a battle-hardened warrior! Your scars speak of honor."
        elif player.char_class == "Mage":
            class_line = "I sense a swirling aura of magic about you—a true prodigy."
        elif player.char_class == "Rogue":
            class_line = "The shadows embrace you, nimble one. Use them wisely."
        elif player.char_class == "Engineer":
            class_line = "Your innovative mind heralds a new era of progress."
        elif player.char_class == "Artist":
            class_line = "Your creative spirit brightens even the darkest times."
        else:
            class_line = "Every hero has their own story."
        dialogue_script = {
            "text": self.dialogue_script.get("text", "") + "\n" + class_line,
            "choices": self.dialogue_script.get("choices", {})
        }
        dialogue_ui = BranchingDialogueUI(pygame.display.get_surface(), dialogue_script)
        choice = dialogue_ui.run()
        logger.info(f"{self.name} received choice: {choice}")
        if choice == "A":
            print(f"{self.name}: Wisdom is the light that guides your journey!")
        elif choice == "B":
            print(f"{self.name}: Power must be tempered with responsibility!")
        elif choice == "C":
            print(f"{self.name}: Very well, wanderer. May fortune favor you!")
        else:
            print(f"{self.name} remains silent.")
