# npc.py
"""
Base NPC class.
"""
import pygame
from resources import load_image_with_scale


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, name, sprite_path, dialogue_tree=None, behavior="static"):
        super().__init__()
        self.name = name
        self.image = load_image_with_scale(sprite_path, (50, 50))
        self.rect = self.image.get_rect(center=pos)
        self.dialogue_tree = dialogue_tree if dialogue_tree is not None else {}
        self.behavior = behavior
        self.interaction_prompt = f"Press E to talk to {self.name}"

    def update(self):
        pass

    def interact(self, player):
        if self.dialogue_tree and "intro" in self.dialogue_tree:
            for line in self.dialogue_tree["intro"]:
                print(f"{self.name}: {line}")
        else:
            print(f"{self.name} has nothing to say.")
