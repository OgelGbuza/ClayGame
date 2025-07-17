# inventory_state.py
import pygame
import textwrap
from ui_helpers import draw_vertical_gradient


class InventoryState:
    """
    Displays the player's inventory in a scrollable, polished panel.
    Use UP/DOWN to scroll; press ESC to exit.
    """

    def __init__(self, screen, inventory):
        self.screen = screen
        self.inventory = inventory  # Expect list of Equipment objects.
        self.font = pygame.font.SysFont("arial", 24)
        self.clock = pygame.time.Clock()
        self.offset = 0
        self.instruction = self.font.render("UP/DOWN: Scroll, ESC: Exit Inventory", True, (200, 200, 200))
        self.inv_text = "\n\n".join([str(item) for item in self.inventory]) if self.inventory else "Inventory is empty."
        self.wrap_width = 80
        self.inv_lines = self.wrap_text(self.inv_text).split("\n")

    def wrap_text(self, text):
        import textwrap
        return "\n".join(textwrap.wrap(text, self.wrap_width))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "playing"
                elif event.key == pygame.K_UP:
                    self.offset = max(self.offset - 10, 0)
                elif event.key == pygame.K_DOWN:
                    self.offset += 10
        return None

    def update(self):
        pass

    def draw(self):
        self.screen.fill((30, 30, 30))
        panel = pygame.Surface((760, 540))
        draw_vertical_gradient(panel, (50, 50, 100), (10, 10, 40))
        pygame.draw.rect(panel, (255, 255, 255), panel.get_rect(), 2)
        self.screen.blit(panel, (20, 20))
        y = 30 - self.offset
        for line in self.inv_lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (40, y))
            y += 30
        self.screen.blit(self.instruction, (40, 500))
        pygame.display.flip()
        self.clock.tick(60)
