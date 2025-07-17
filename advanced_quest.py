# advanced_quest.py
import pygame

class Quest:
    def __init__(self, quest_id, description, objectives=None, rewards=None, prerequisites=None):
        self.quest_id = quest_id
        self.description = description
        self.objectives = objectives if objectives is not None else []
        self.rewards = rewards if rewards is not None else {}
        self.prerequisites = prerequisites if prerequisites is not None else []
        self.status = "Active"

    def add_objective(self, objective_desc, goal):
        self.objectives.append({"desc": objective_desc, "progress": 0, "goal": goal})

    def update_objective(self, objective_index, amount):
        if 0 <= objective_index < len(self.objectives):
            self.objectives[objective_index]["progress"] += amount
            if self.objectives[objective_index]["progress"] > self.objectives[objective_index]["goal"]:
                self.objectives[objective_index]["progress"] = self.objectives[objective_index]["goal"]
            self.check_completion()

    def check_completion(self):
        if self.objectives and all(obj["progress"] >= obj["goal"] for obj in self.objectives):
            self.status = "Completed"
            print(f"Quest {self.quest_id} completed!")
            return True
        return False

    def apply_rewards(self, player):
        for key, value in self.rewards.items():
            if key == "experience":
                player.experience += value
                print(f"Player gains {value} experience!")
            elif key == "reputation":
                for faction, rep_val in value.items():
                    player.adjust_reputation(faction, rep_val)
            elif key == "item":
                print(f"Player receives item: {value}")

    def __str__(self):
        obj_lines = []
        for obj in self.objectives:
            obj_lines.append(f"{obj['desc']}: {obj['progress']}/{obj['goal']}")
        objectives_str = "\n".join(obj_lines)
        rewards_str = ", ".join([f"{k}: {v}" for k, v in self.rewards.items()])
        return (f"Quest {self.quest_id}: {self.description}\nStatus: {self.status}\n"
                f"Objectives:\n{objectives_str}\nRewards: {rewards_str}")

class AdvancedQuestLog:
    def __init__(self):
        self.quests = {}
        self.player_reference = None

    def add_quest(self, quest):
        if quest.quest_id not in self.quests:
            self.quests[quest.quest_id] = quest
            print(f"Quest added: {quest.quest_id} - {quest.description}")
        else:
            print(f"Quest {quest.quest_id} is already active.")

    def update_quest_progress(self, quest_id, objective_index, amount):
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            quest.update_objective(objective_index, amount)
            if quest.status == "Completed" and self.player_reference:
                quest.apply_rewards(self.player_reference)
                print(f"Quest {quest_id} rewards applied!")

    def complete_quest(self, quest_id):
        if quest_id in self.quests:
            self.quests[quest_id].status = "Completed"
            if self.player_reference:
                self.quests[quest_id].apply_rewards(self.player_reference)
            print(f"Quest {quest_id} marked as completed!")

    def draw(self, screen):
        font = pygame.font.Font(None, 20)
        y = 10
        panel = pygame.Surface((280,200), pygame.SRCALPHA)
        panel.fill((0,0,0,180))
        pygame.draw.rect(panel, (255,255,255), panel.get_rect(), 2)
        screen.blit(panel, (500,10))
        for quest in self.quests.values():
            quest_text = font.render(f"{quest.quest_id}: {quest.description} [{quest.status}]", True, (255,255,255))
            screen.blit(quest_text, (510, y))
            y += 20
            for obj in quest.objectives:
                obj_text = font.render(f"   {obj['desc']}: {obj['progress']}/{obj['goal']}", True, (200,200,200))
                screen.blit(obj_text, (530, y))
                y += 18
            y += 5
