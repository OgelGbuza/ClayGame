# branching_dialogue_ui.py
"""
Enhanced Dialogue UI that scrolls text letter-by-letter and presents selectable dialogue choices.
Includes a gradient background and text shadow for improved readability.
"""
import pygame, textwrap
from ui_helpers import draw_vertical_gradient

# Global dialogue journal
dialogue_journal = []


class BranchingDialogueUI:
    def __init__(self, screen, dialogue_script, scroll_delay=30, wrap_width=60):
        self.screen = screen
        self.script = dialogue_script
        self.full_text = dialogue_script.get("text", "")
        self.choices = dialogue_script.get("choices", {})
        self.choice_keys = list(self.choices.keys())
        self.selected = 0
        self.font = pygame.font.SysFont("arial", 28)
        self.clock = pygame.time.Clock()
        self.scroll_delay = scroll_delay
        self.wrap_width = wrap_width
        self.displayed_text = ""
        self.text_index = 0
        self.last_char_time = pygame.time.get_ticks()
        self.in_choice_mode = False
        self.running = True
        self.portrait_path = dialogue_script.get("portrait", None)
        self.portrait = None
        if self.portrait_path:
            from resources import load_image_with_scale
            self.portrait = load_image_with_scale(self.portrait_path, (100, 100))

    def wrap_text(self, text):
        return "\n".join(textwrap.wrap(text, self.wrap_width))

    def update(self):
        now = pygame.time.get_ticks()
        if not self.in_choice_mode:
            if self.text_index < len(self.full_text) and now - self.last_char_time > self.scroll_delay:
                self.displayed_text += self.full_text[self.text_index]
                self.text_index += 1
                self.last_char_time = now
            elif self.text_index >= len(self.full_text):
                if self.choices:
                    self.in_choice_mode = True

    def run(self):
        selected_option = None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                elif event.type == pygame.KEYDOWN:
                    if not self.in_choice_mode:
                        self.displayed_text = self.full_text
                        self.text_index = len(self.full_text)
                        if self.choices:
                            self.in_choice_mode = True
                    else:
                        if event.key == pygame.K_UP:
                            self.selected = (self.selected - 1) % len(self.choice_keys)
                        elif event.key == pygame.K_DOWN:
                            self.selected = (self.selected + 1) % len(self.choice_keys)
                        elif event.key == pygame.K_RETURN:
                            selected_option = self.choice_keys[self.selected]
                            self.running = False
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
                            return None
            self.update()
            self.draw()
            self.clock.tick(30)
        dialogue_journal.append(self.displayed_text)
        return selected_option

    def draw(self):
        self.screen.fill((30, 30, 30))
        x_offset = 50
        if self.portrait:
            self.screen.blit(self.portrait, (50, 310))
            x_offset += 110
        # Create dialogue panel with gradient.
        panel_width = 700 - (x_offset - 50)
        panel_height = 150
        panel = pygame.Surface((panel_width, panel_height))
        draw_vertical_gradient(panel, (20, 20, 40), (0, 0, 0))
        pygame.draw.rect(panel, (255, 255, 255), panel.get_rect(), 2)
        self.screen.blit(panel, (x_offset, 400))
        # Render dialogue text with a shadow.
        wrapped_text = self.wrap_text(self.displayed_text)
        lines = wrapped_text.split("\n")
        y = 410
        for line in lines:
            # Draw shadow.
            shadow = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(shadow, (x_offset + 12, y + 2))
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (x_offset + 10, y))
            y += 30
        if self.in_choice_mode and self.choices:
            y += 10
            for idx, key in enumerate(self.choice_keys):
                choice_text = f"{key}: {self.choices[key]}"
                color = (255, 255, 0) if idx == self.selected else (255, 255, 255)
                option_surf = self.font.render(choice_text, True, color)
                self.screen.blit(option_surf, (x_offset + 20, y))
                y += 30
        pygame.display.flip()
