# settings_state.py
import pygame


class SettingsState:
    """
    A state for adjusting game settings.
    Options: Volume, Difficulty, Controls.
    Use UP/DOWN to select, LEFT/RIGHT to adjust, ESC to exit.
    """

    def __init__(self, screen, settings=None):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.settings = settings if settings is not None else {
            "volume": 50,
            "difficulty": "Normal",
            "controls": "Default"
        }
        self.options = list(self.settings.keys())
        self.selection = 0
        self.font = pygame.font.SysFont("arial", 32)
        self.instruction = self.font.render("UP/DOWN: Select, LEFT/RIGHT: Adjust, ESC: Exit", True, (255, 255, 255))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "playing"
                elif event.key == pygame.K_UP:
                    self.selection = (self.selection - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selection = (self.selection + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    self.adjust_setting(self.options[self.selection], decrease=True)
                elif event.key == pygame.K_RIGHT:
                    self.adjust_setting(self.options[self.selection], decrease=False)
        return None

    def adjust_setting(self, key, decrease=False):
        if key == "volume":
            change = -5 if decrease else 5
            self.settings[key] = max(0, min(100, self.settings[key] + change))
        elif key == "difficulty":
            difficulties = ["Easy", "Normal", "Hard"]
            idx = difficulties.index(self.settings[key])
            idx = (idx - 1) % len(difficulties) if decrease else (idx + 1) % len(difficulties)
            self.settings[key] = difficulties[idx]
        elif key == "controls":
            self.settings[key] = "Alternative" if self.settings[key] == "Default" else "Default"

    def update(self):
        pass

    def draw(self):
        self.screen.fill((30, 30, 30))
        header = self.font.render("Settings", True, (255, 255, 0))
        self.screen.blit(header, (50, 50))
        y = 120
        for i, key in enumerate(self.options):
            value = self.settings[key]
            color = (255, 255, 0) if i == self.selection else (255, 255, 255)
            option_text = self.font.render(f"{key.capitalize()}: {value}", True, color)
            self.screen.blit(option_text, (50, y))
            y += 50
        self.screen.blit(self.instruction, (50, 500))
        pygame.display.flip()
        self.clock.tick(60)
