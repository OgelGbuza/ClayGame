# ====================== File: narrative_cutscene_state.py ======================
import pygame, textwrap
from data_loader import load_json
from resources import load_image_with_scale

class NarrativeCutsceneState:
    def __init__(self, screen, filename="cutscene_intro.json", scroll_delay=40, wrap_width=70):
        self.screen = screen
        self.data = load_json(filename)
        if not self.data:
            self.data = {"text": "In a world torn by conflict, a new era begins...", "bg_image": ""}
        self.full_text = self.data.get("text", "")
        self.scroll_delay = scroll_delay
        self.wrap_width = wrap_width
        self.font = pygame.font.SysFont("arial", 28)
        self.clock = pygame.time.Clock()
        self.displayed_text = ""
        self.text_index = 0
        self.last_char_time = pygame.time.get_ticks()
        self.done = False
        self.bg_image = None
        bg_path = self.data.get("bg_image", "")
        if bg_path:
            self.bg_image = load_image_with_scale(bg_path, (800,600))
        self.alpha = 0
        self.fading_in = True
        # Flag to wait for key release before signaling state transition.
        self.waiting_for_release = False

    def wrap_text(self, text):
        import textwrap
        return "\n".join(textwrap.wrap(text, self.wrap_width))

    def process_events(self, events):
        # Process each event from the list.
        for event in events:
            # Debug print: Uncomment the next line if you want to see all events.
            # print("Event received:", event)
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                # If the text is not yet complete and Enter (or Space) is pressed,
                # immediately complete the text.
                if not self.done and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                    print("KEYDOWN: Completing text because it is not done yet.")
                    self.displayed_text = self.full_text
                    self.text_index = len(self.full_text)
                    self.done = True
                    # Set flag so we wait for the key to be released.
                    self.waiting_for_release = True

        # If the text is complete, check the current key state.
        if self.done:
            keys = pygame.key.get_pressed()
            if self.waiting_for_release:
                # Wait until the Enter key is released.
                if not keys[pygame.K_RETURN]:
                    # Key was released; now trigger the transition.
                    self.waiting_for_release = False
                    print("Enter released after completion; transitioning state.")
                    return "playing"
            else:
                # In case Enter is pressed again after release,
                # you may also check here if needed.
                pass

        return None

    def update(self):
        if self.fading_in:
            self.alpha += 5
            if self.alpha >= 255:
                self.alpha = 255
                self.fading_in = False
        if not self.done:
            now = pygame.time.get_ticks()
            if self.text_index < len(self.full_text) and now - self.last_char_time > self.scroll_delay:
                self.displayed_text += self.full_text[self.text_index]
                self.text_index += 1
                self.last_char_time = now
            if self.text_index >= len(self.full_text):
                self.done = True
                # Begin waiting for key release.
                self.waiting_for_release = True

    def draw(self):
        if self.bg_image:
            bg = self.bg_image.copy()
        else:
            bg = pygame.Surface((800,600))
            bg.fill((0, 0, 0))
        fade = pygame.Surface((800,600))
        fade.set_alpha(255 - self.alpha)
        fade.fill((0, 0, 0))
        bg.blit(fade, (0,0))
        self.screen.blit(bg, (0,0))
        wrapped_text = self.wrap_text(self.displayed_text)
        lines = wrapped_text.split("\n")
        y = 100
        for line in lines:
            text_surf = self.font.render(line, True, (255,255,255))
            self.screen.blit(text_surf, (100, y))
            y += 35
        if self.done:
            instruction = self.font.render("Press ENTER to continue...", True, (200,200,200))
            self.screen.blit(instruction, (100, y+20))
        pygame.display.flip()
        self.clock.tick(30)
