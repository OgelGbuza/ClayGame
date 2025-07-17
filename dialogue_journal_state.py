# dialogue_journal_state.py
import pygame
import textwrap
from branching_dialogue_ui import dialogue_journal


class DialogueJournalState:
    """
    Displays a scrollable dialogue journal.
    Use UP/DOWN to scroll; press ESC to exit.
    """

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 24)
        self.clock = pygame.time.Clock()
        self.offset = 0
        self.instruction = self.font.render("UP/DOWN: Scroll, ESC: Exit Journal", True, (200, 200, 200))
        self.journal_text = "\n\n".join(dialogue_journal) if dialogue_journal else "No dialogue recorded."
        self.wrap_width = 80
        self.journal_lines = self.wrap_text(self.journal_text).split("\n")

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
        self.screen.fill((20, 20, 20))
        panel = pygame.Surface((760, 540), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        pygame.draw.rect(panel, (255, 255, 255), panel.get_rect(), 2)
        self.screen.blit(panel, (20, 20))
        y = 30 - self.offset
        for line in self.journal_lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (40, y))
            y += 30
        self.screen.blit(self.instruction, (40, 500))
        pygame.display.flip()
        self.clock.tick(60)
