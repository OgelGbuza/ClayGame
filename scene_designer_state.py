"""Basic drag-and-drop scene designer.

This state lets the user arrange sprite objects and save the result
as a scene template under ``assets/scenes``. It is intentionally
simple but provides a starting point for more advanced tools."""

import json
import pygame
from sprites import PropagandaPoster, ClaySoldier


class SceneDesignerState:
    def __init__(self, screen: pygame.Surface, template: str | None = None):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        if template:
            self.load_template(template)
        self.dragged = None

    def load_template(self, name: str):
        path = f"assets/scenes/{name}.json"
        try:
            data = json.load(open(path))
        except FileNotFoundError:
            data = {}
        for obj in data.get("objects", []):
            if obj["type"] == "poster":
                sprite = PropagandaPoster(obj["position"])
                self.sprites.add(sprite)
        for npc in data.get("npcs", []):
            sprite = ClaySoldier(npc["position"])
            self.sprites.add(sprite)

    def save_template(self, name: str):
        data = {"objects": [], "npcs": []}
        for sprite in self.sprites:
            if isinstance(sprite, PropagandaPoster):
                data["objects"].append({"type": "poster", "position": list(sprite.rect.topleft)})
            elif isinstance(sprite, ClaySoldier):
                data["npcs"].append({"type": "soldier", "position": list(sprite.rect.topleft)})
        with open(f"assets/scenes/{name}.json", "w") as f:
            json.dump(data, f, indent=2)

    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in reversed(self.sprites.sprites()):
                    if sprite.rect.collidepoint(event.pos):
                        self.dragged = sprite
                        break
                else:
                    # add a poster where clicked
                    poster = PropagandaPoster(event.pos)
                    self.sprites.add(poster)
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragged = None
        if self.dragged:
            self.dragged.rect.center = pygame.mouse.get_pos()
        return None

    def update(self):
        self.sprites.update()

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.sprites.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
