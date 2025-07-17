# npc_quest_branch.py
"""
QuestMasterNPC offers branching quests using external quest data.
"""
import pygame
import logging
from npc_dialogue import ClassDependentNPC
from advanced_quest import Quest
from branching_dialogue_ui import BranchingDialogueUI
from data_loader import load_json

logger = logging.getLogger(__name__)


class QuestMasterNPC(ClassDependentNPC):
    def __init__(self, pos, name, sprite_path, dialogue_script=None, faction="questmaster", friendly_threshold=0):
        if dialogue_script is None:
            dialogue_script = {
                "text": "Quest Master: I offer you a choice. Which path do you choose?",
                "choices": {
                    "A": "Defend the Outpost",
                    "B": "Steal the Royal Artifact"
                }
            }
        super().__init__(pos, name, sprite_path, dialogue_script, faction, friendly_threshold)

    def interact(self, player):
        dialogue_ui = BranchingDialogueUI(pygame.display.get_surface(), self.dialogue_script)
        choice = dialogue_ui.run()
        logger.info(f"{self.name} received choice: {choice}")
        quest_data = load_json("quest_data.json")
        quests = quest_data.get("quests", [])
        if choice == "A":
            if quests:
                q = quests[0]
                new_quest = Quest(q["quest_id"], q["description"], q.get("objectives", []), q.get("rewards", {}))
                if hasattr(player, "quest_log"):
                    player.quest_log.add_quest(new_quest)
                print(f"{self.name}: You must defend the outpost!")
            else:
                print(f"{self.name}: No quest data available for path A.")
        elif choice == "B":
            if len(quests) > 1:
                q = quests[1]
                new_quest = Quest(q["quest_id"], q["description"], q.get("objectives", []), q.get("rewards", {}))
                if hasattr(player, "quest_log"):
                    player.quest_log.add_quest(new_quest)
                print(f"{self.name}: Infiltrate the castle and steal the artifact!")
            else:
                print(f"{self.name}: No quest data available for path B.")
        else:
            print(f"{self.name}: Return when you are ready.")
