# pause_state.py
import pygame
from ui_helpers import draw_vertical_gradient


class PauseState:
    """
    A polished pause menu state.
    Use UP/DOWN to navigate and ENTER to select.
    Options: Resume, Settings, Save, Quit.
    """

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.options = ["Resume", "Settings", "Save", "Quit"]
        self.selection = 0
        self.font = pygame.font.SysFont("arial", 36)
        self.instruction = self.font.render("UP/DOWN: Navigate, ENTER: Select", True, (255, 255, 255))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                elif event.key == pygame.K_UP:
                    self.selection = (self.selection - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selection = (self.selection + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selection].lower()
        return None

    def update(self):
        pass

    def draw(self):
        self.screen.fill((20, 20, 20))
        panel = pygame.Surface((400, 300))
        draw_vertical_gradient(panel, (50, 50, 100), (10, 10, 40))
        pygame.draw.rect(panel, (255, 255, 255), panel.get_rect(), 3)
        panel_x = (800 - panel.get_width()) // 2
        panel_y = (600 - panel.get_height()) // 2
        self.screen.blit(panel, (panel_x, panel_y))
        y = panel_y + 50
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selection else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(centerx=panel_x + panel.get_width() // 2, top=y)
            self.screen.blit(text, text_rect)
            y += 60
        inst_rect = self.instruction.get_rect(center=(800 // 2, panel_y + panel.get_height() - 30))
        self.screen.blit(self.instruction, inst_rect)
        pygame.display.flip()
        self.clock.tick(60)
