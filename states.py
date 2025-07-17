# ====================== File: states.py ======================
import pygame
import random
import logging
from config import *  # Imports state constants and the config dictionary
from sprites import (
    ClaySoldier, EnemyUnit, BossEnemy, AnimatedEnemy, Drone,
    PropagandaPoster, Projectile, BossProjectile, PowerUp, ShieldPowerUp,
    Explosion, ParallaxBackground, Fortress, Village
)
from resources import load_image_with_scale, get_asset_path

logger = logging.getLogger(__name__) # Set up logger for this module

# ------------------------------
# PutinCutsceneState
# ------------------------------
class PutinCutsceneState:
    """
    State for displaying a Putin cutscene image with a timed duration and user prompt.
    """
    def __init__(self, screen: pygame.Surface):
        """
        Initializes the PutinCutsceneState.

        Args:
            screen: The pygame.Surface to draw on.
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.cutscene_image = load_image_with_scale("putin_caricature.png", (800, 600)) # Load cutscene image
        self.display_duration_ms = 3000  # Duration to display the cutscene in milliseconds
        self.start_time_ms = pygame.time.get_ticks() # Record start time
        self.font = pygame.font.Font(None, 36) # Font for instructions
        logger.debug("PutinCutsceneState initialized.")


    def process_events(self, events: list[pygame.event.Event]) -> str | None:
        """
        Handles events for the PutinCutsceneState.

        Listens for QUIT and SPACE key events.

        Args:
            events: A list of pygame.event.Event objects.

        Returns:
            STATE_QUIT if QUIT event is detected, STATE_DIALOGUE if SPACE is pressed or duration expires, otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return STATE_QUIT # Signal to quit the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    logger.debug("Space key pressed during PutinCutsceneState. Transitioning to DialogueState.")
                    return STATE_DIALOGUE # Proceed to dialogue on space press

        if pygame.time.get_ticks() - self.start_time_ms > self.display_duration_ms:
            logger.debug("PutinCutsceneState duration expired. Transitioning to DialogueState.")
            return STATE_DIALOGUE # Proceed to dialogue after duration
        return None # No state change

    def update(self):
        """
        Updates the PutinCutsceneState (currently no dynamic updates).
        """
        pass # No updates needed for this static cutscene state

    def draw(self):
        """
        Draws the Putin cutscene image and instructions on the screen.
        """
        self.screen.fill((0, 0, 0)) # Black background
        self.screen.blit(self.cutscene_image, (0, 0)) # Draw cutscene image

        instruction_text_surface = self.font.render("Press SPACE to continue...", True, (255, 255, 255)) # Render instruction text
        instruction_text_rect = instruction_text_surface.get_rect(center=(self.screen.get_width() // 2, 550)) # Position at bottom center
        self.screen.blit(instruction_text_surface, instruction_text_rect) # Draw instruction text

        pygame.display.flip() # Update the display
        self.clock.tick(60) # Limit frame rate to 60 FPS


# ------------------------------
# DialogueState
# ------------------------------
class DialogueState:
    """
    State for displaying dialogue text boxes with speaker names.
    """
    def __init__(self, screen: pygame.Surface):
        """
        Initializes the DialogueState.

        Args:
            screen: The pygame.Surface to draw on.
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36) # Font for dialogue text
        self.dialogue_lines = [ # Dialogue script - list of tuples (speaker, text)
            ("Commander Ivan", "Ukrainian defenders, Clayonia is under attack by clumsy Russian invaders!"),
            ("Lieutenant Petro", "Our brave clay soldiers with detailed uniforms and improvised weapons stand strong."),
            ("Colonel Alexei", "Look at our handmade drones soaring above the battlefield!"),
            ("", "SHOW_PUTIN_CUTSCENE"), # Special command to show Putin cutscene
            ("Commander Ivan", "Even the grotesque caricatures of Putin tremble before our absurd resistance!"),
            ("Lieutenant Petro", "Our heroic animals and clever tactics turn melted tanks into victories!"),
            ("Commander Ivan", "Today, we fight for freedom and the future of Ukraine. Rally and defend Clayonia!")
        ]
        self.current_dialogue_index = 0 # Index of the current dialogue line
        logger.debug("DialogueState initialized.")

    def process_events(self, events: list[pygame.event.Event]) -> str | None:
        """
        Handles events for the DialogueState.

        Listens for QUIT and SPACE key events to advance dialogue.

        Args:
            events: A list of pygame.event.Event objects.

        Returns:
            STATE_QUIT if QUIT event, STATE_PUTIN_CUTSCENE to show cutscene, STATE_PLAYING after dialogue ends, otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return STATE_QUIT # Signal quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_dialogue_line = self.dialogue_lines[self.current_dialogue_index]
                    if current_dialogue_line[1] == "SHOW_PUTIN_CUTSCENE":
                        self.current_dialogue_index += 1 # Move to next dialogue line after command
                        logger.debug("Dialogue requests PutinCutsceneState.")
                        return STATE_PUTIN_CUTSCENE # Transition to Putin cutscene
                    else:
                        self.current_dialogue_index += 1 # Advance to the next dialogue line
                        if self.current_dialogue_index >= len(self.dialogue_lines):
                            logger.debug("Dialogue finished. Transitioning to PlayingState.")
                            return STATE_PLAYING # Dialogue finished, start playing

        return None # No state change

    def update(self):
        """
        Updates the DialogueState (currently no dynamic updates).
        """
        pass # No updates needed for dialogue state

    def draw(self):
        """
        Draws the dialogue text and speaker name on the screen.
        """
        self.screen.fill((0, 0, 0)) # Black background

        if self.current_dialogue_index < len(self.dialogue_lines):
            speaker_name, dialogue_text = self.dialogue_lines[self.current_dialogue_index]

            if dialogue_text == "SHOW_PUTIN_CUTSCENE": # Skip drawing for cutscene command line
                dialogue_text = "" # Ensure no text is drawn for this line

            dialogue_surface = self.font.render(f"{speaker_name}: {dialogue_text}", True, (255, 255, 255)) # Render dialogue text
            dialogue_rect = dialogue_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2)) # Center dialogue
            self.screen.blit(dialogue_surface, dialogue_rect) # Draw dialogue

            instruction_surface = self.font.render("Press SPACE to continue...", True, (255, 255, 255)) # Render instruction
            instruction_rect = instruction_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50 )) # Position below dialogue
            self.screen.blit(instruction_surface, instruction_rect) # Draw instruction

        pygame.display.flip() # Update display
        self.clock.tick(60) # Limit FPS

# ------------------------------
# MainMenu
# ------------------------------
class MainMenu:
    """
    State for the main menu screen.
    """
    def __init__(self, screen: pygame.Surface):
        """
        Initializes the MainMenu state.

        Args:
            screen: The pygame.Surface to draw on.
        """
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 32) # Font for menu text
        logger.debug("MainMenu initialized.")

    def process_events(self, events: list[pygame.event.Event]) -> str | None:
        """
        Handles events for the MainMenu state.

        Listens for QUIT and RETURN (Enter) key events.

        Args:
            events: A list of pygame.event.Event objects.

        Returns:
            STATE_QUIT if QUIT event, STATE_PLAYING if ENTER is pressed, otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return STATE_QUIT # Signal quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    logger.debug("Enter key pressed in MainMenu. Transitioning to PlayingState.")
                    return STATE_PLAYING # Start game on Enter press
        return None # No state change

    def update(self):
        """
        Updates the MainMenu state (currently no dynamic updates).
        """
        pass # No updates needed for main menu

    def draw(self):
        """
        Draws the main menu title and instructions on the screen.
        """
        self.screen.fill((0, 0, 0)) # Black background
        title_surface = self.font.render("Main Menu - Press ENTER to start", True, (255, 255, 255)) # Render title text
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2)) # Center title
        self.screen.blit(title_surface, title_rect) # Draw title
        pygame.display.flip() # Update display


# ------------------------------
# SettingsState
# ------------------------------
class SettingsState:
    """
    State for the settings menu, allowing players to adjust game configurations.
    """
    def __init__(self, screen: pygame.Surface, playing_state):
        """
        Initializes the SettingsState.

        Args:
            screen: The pygame.Surface to draw on.
            playing_state: Reference to the PlayingState (for resuming game).
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.playing_state = playing_state # Store reference to PlayingState
        self.font_large = pygame.font.Font(None, 74) # Large font for title
        self.font_small = pygame.font.Font(None, 36) # Small font for options and instructions
        self.setting_options = [ # List of setting options
            "1: Volume Up (+0.1)",
            "2: Volume Down (-0.1)",
            "3: Toggle Control Scheme (Arrows/WASD)",
            "4: Toggle Art Theme (Default/Dark)",
            "5: Increase Boss Health (+1)",
            "6: Decrease Boss Health (-1)"
        ]
        self.title_surface = self.font_large.render("Settings Menu", True, (255, 255, 255)) # Render title
        self.title_rect = self.title_surface.get_rect(center=(self.screen.get_width() // 2, 100)) # Title position
        self.rendered_options = self._render_options() # Render setting options
        self.instructions_surface = self.font_small.render("Press 1-6 to adjust, S to Save & Resume", True, (255, 255, 255)) # Instructions
        self.instructions_rect = self.instructions_surface.get_rect(center=(self.screen.get_width() // 2, 500)) # Instruction position
        self.next_state = STATE_SETTINGS # Default next state is self (stay in settings)
        logger.debug("SettingsState initialized.")


    def _render_options(self) -> list[tuple[pygame.Surface, pygame.Rect]]:
        """
        Renders the settings options text surfaces and their rectangles.

        Returns:
            A list of tuples, each containing a rendered pygame.Surface and its pygame.Rect.
        """
        rendered_options = []
        y_offset = 180 # Starting Y position for options
        for option_text in self.setting_options:
            rendered_text = self.font_small.render(option_text, True, (255, 255, 255)) # Render each option
            text_rect = rendered_text.get_rect(center=(self.screen.get_width() // 2, y_offset)) # Position option
            rendered_options.append((rendered_text, text_rect)) # Add to list
            y_offset += 50 # Increment Y for next option
        return rendered_options


    def process_events(self, events: list[pygame.event.Event]) -> str | None:
        """
        Handles events for the SettingsState.

        Listens for QUIT and number keys (1-6) for settings adjustments, and 'S' to save and resume.

        Args:
            events: A list of pygame.event.Event objects.

        Returns:
            STATE_QUIT if QUIT event, STATE_PLAYING to resume game, otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return STATE_QUIT # Signal quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    config["volume"] = min(1.0, config["volume"] + 0.1) # Increase volume
                    pygame.mixer.music.set_volume(config["volume"]) # Apply volume change
                    logger.debug(f"Volume increased to {config['volume']}")
                elif event.key == pygame.K_2:
                    config["volume"] = max(0.0, config["volume"] - 0.1) # Decrease volume
                    pygame.mixer.music.set_volume(config["volume"]) # Apply volume change
                    logger.debug(f"Volume decreased to {config['volume']}")
                elif event.key == pygame.K_3:
                    config["control_scheme"] = "wasd" if config["control_scheme"] == "arrows" else "arrows" # Toggle control scheme
                    logger.debug(f"Control scheme toggled to {config['control_scheme']}")
                elif event.key == pygame.K_4:
                    config["art_theme"] = "dark" if config["art_theme"] == "default" else "default" # Toggle art theme
                    logger.debug(f"Art theme toggled to {config['art_theme']}")
                elif event.key == pygame.K_5:
                    config["boss_health"] += 1 # Increase boss health
                    logger.debug(f"Boss health increased to {config['boss_health']}")
                elif event.key == pygame.K_6:
                    config["boss_health"] = max(1, config["boss_health"] - 1) # Decrease boss health
                    logger.debug(f"Boss health decreased to {config['boss_health']}")
                elif event.key == pygame.K_s:
                    logger.debug("Settings saved and resuming game. Transitioning to PlayingState.")
                    return STATE_PLAYING # Resume game on 'S' press

        return None # No state change

    def update(self):
        """
        Updates the SettingsState (currently no dynamic updates).
        """
        pass # No updates needed in settings state

    def draw(self):
        """
        Draws the settings menu on the screen.
        """
        self.screen.fill((20, 20, 20)) # Dark background
        self.screen.blit(self.title_surface, self.title_rect) # Draw title
        for rendered_option, option_rect in self.rendered_options: # Draw each option
            self.screen.blit(rendered_option, option_rect)
        self.screen.blit(self.instructions_surface, self.instructions_rect) # Draw instructions
# Update display and maintain frame rate
        pygame.display.flip()
        self.clock.tick(60)


# ------------------------------
# UpgradeState
# ------------------------------
class UpgradeState:
    """
    State for the upgrade shop, allowing players to purchase upgrades.
    """
    def __init__(self, screen: pygame.Surface, playing_state):
        """
        Initializes the UpgradeState.

        Args:
            screen: The pygame.Surface to draw on.
            playing_state: Reference to the PlayingState to apply upgrades.
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.playing_state = playing_state # Store PlayingState reference
        self.font_large = pygame.font.Font(None, 74) # Large font for title
        self.font_small = pygame.font.Font(None, 36) # Small font for options and instructions
        self.upgrade_options_text = [ # Upgrade options text
            "1: Increase Speed (+1)",
            "2: Increase Projectile Speed (+2)",
            "3: Increase Shield Duration (+100)",
            "4: Extra Life (+1)"
        ]
        self.title_surface = self.font_large.render("Upgrade Shop", True, (255, 255, 255)) # Render title
        self.title_rect = self.title_surface.get_rect(center=(self.screen.get_width() // 2, 100)) # Title position
        self.rendered_options = self._render_options() # Render upgrade options
        self.instructions_surface = self.font_small.render("Press 1-4 to choose upgrade", True, (255, 255, 255)) # Instructions
        self.instructions_rect = self.instructions_surface.get_rect(center=(self.screen.get_width() // 2, 450)) # Instruction position
        self.next_state = STATE_UPGRADE # Default next state is self (stay in upgrade state)
        logger.debug("UpgradeState initialized.")


    def _render_options(self) -> list[tuple[pygame.Surface, pygame.Rect]]:
        """
        Renders the upgrade options text surfaces and their rectangles.

        Returns:
            A list of tuples, each containing a rendered pygame.Surface and its pygame.Rect.
        """
        rendered_options = []
        y_offset = 200 # Starting Y position for options
        for option_text in self.upgrade_options_text:
            rendered_text = self.font_small.render(option_text, True, (255, 255, 255)) # Render option text
            text_rect = rendered_text.get_rect(center=(self.screen.get_width() // 2, y_offset)) # Position option
            rendered_options.append((rendered_text, text_rect)) # Add to list
            y_offset += 50 # Increment Y for next option
        return rendered_options


    def process_events(self, events: list[pygame.event.Event]) -> str | None:
        """
        Handles events for the UpgradeState.

        Listens for QUIT and number keys (1-4) to purchase upgrades.

        Args:
            events: A list of pygame.event.Event objects.

        Returns:
            STATE_QUIT if QUIT event, STATE_PLAYING to resume game after upgrade, otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return STATE_QUIT # Signal quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.playing_state.soldier.speed += 1 # Increase player speed
                    logger.debug(f"Player speed increased to {self.playing_state.soldier.speed}")
                    self.next_state = STATE_PLAYING # Resume game after upgrade
                elif event.key == pygame.K_2:
                    self.playing_state.projectile_speed += 2 # Increase projectile speed
                    logger.debug(f"Projectile speed increased to {self.playing_state.projectile_speed}")
                    self.next_state = STATE_PLAYING # Resume game
                elif event.key == pygame.K_3:
                    self.playing_state.shield_duration += 100 # Increase shield duration
                    logger.debug(f"Shield duration increased to {self.playing_state.shield_duration}")
                    self.next_state = STATE_PLAYING # Resume game
                elif event.key == pygame.K_4:
                    self.playing_state.lives += 1 # Add extra life
                    logger.debug(f"Extra life awarded. Lives now: {self.playing_state.lives}")
                    self.next_state = STATE_PLAYING # Resume game

        if self.next_state != STATE_UPGRADE: # Check if state should change
            return self.next_state # Return next state if upgrade selected
        return None # Stay in upgrade state

    def update(self):
        """
        Updates the UpgradeState (currently no dynamic updates).
        """
        pass # No updates needed in upgrade state

    def draw(self):
        """
        Draws the upgrade menu on the screen.
        """
        self.screen.fill((0, 0, 0)) # Black background
        self.screen.blit(self.title_surface, self.title_rect) # Draw title
        for rendered_option, option_rect in self.rendered_options: # Draw each option
            self.screen.blit(rendered_option, option_rect)
        self.screen.blit(self.instructions_surface, self.instructions_rect) # Draw instructions
        pygame.display.flip() # Update display
        self.clock.tick(60) # Limit FPS


# ------------------------------
# PlayingState (Main Gameplay)
# ------------------------------
class PlayingState:
    """
    State for the main gameplay of the game.
    """
    def __init__(self, screen: pygame.Surface):
        """
        Initializes the PlayingState, setting up game elements and music.

        Args:
            screen: The pygame.Surface to draw on.
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.parallax_background = ParallaxBackground(screen) # Initialize parallax background
        self.soldier = ClaySoldier((self.screen.get_width() // 2, self.screen.get_height() // 2)) # Initialize player soldier
        self.soldier_group = pygame.sprite.GroupSingle(self.soldier) # Group for player soldier (using GroupSingle for easier access)
        self.enemy_group = pygame.sprite.Group() # Group for enemies
        self._spawn_initial_enemy() # Spawn the first enemy
        self.projectile_group = pygame.sprite.Group() # Group for player projectiles
        self.boss_projectile_group = pygame.sprite.Group() # Group for boss projectiles
        self.powerup_group = pygame.sprite.Group() # Group for power-ups
        self.explosion_group = pygame.sprite.Group() # Group for explosions (visual effects)
        self.drone_group = pygame.sprite.Group() # Group for drone enemies
        self.structure_group = self._create_structures() # Create and group level structures
        self.score = 0 # Player score
        self.lives = 3 # Player lives
        self.level = 1 # Game level
        self.invulnerable_timer_ms = 0 # Timer for player invulnerability after hit
        self.font = pygame.font.Font(None, 36) # Font for UI text
        self.next_state = STATE_PLAYING # Default next state is self (stay in playing)
        self.is_shield_active = False # Shield power-up active flag
        self.shield_timer_ms = 0 # Timer for shield duration
        self.shield_duration_ms = 300 * (1000/60) # Shield duration in milliseconds (assuming 60 FPS) - converted from frames to ms
        self.projectile_speed = 10 # Projectile speed
        self.powerup_spawn_timer_ms = 0 # Timer for power-up spawning
        self.powerup_spawn_interval_ms = 600 * (1000/60) # Power-up spawn interval in milliseconds (frames to ms)
        self._load_music_and_sounds() # Load background music and sound effects
        self.show_debug_info = False  # Toggle for debug overlay
        logger.debug("PlayingState initialized.")


    def _create_structures(self) -> pygame.sprite.Group:
        """
        Creates and groups the level structures (Fortress, Village, PropagandaPoster).

        Returns:
            A pygame.sprite.Group containing the structure sprites.
        """
        structure_group = pygame.sprite.Group()
        fortress = Fortress((self.screen.get_width() // 2, 500)) # Fortress at bottom center
        village = Village((150, 550)) # Village on the left
        poster = PropagandaPoster((650, 550)) # Poster on the right
        structure_group.add(fortress, village, poster) # Add structures to the group
        return structure_group


    def _spawn_initial_enemy(self):
        """
        Spawns the initial enemy at the start of the game (randomly AnimatedEnemy or EnemyUnit).
        """
        enemy_x_pos = 200 # Initial enemy X position
        enemy_y_pos = 150 # Initial enemy Y position
        if random.random() < 0.5:
            initial_enemy = AnimatedEnemy((enemy_x_pos, enemy_y_pos)) # Spawn AnimatedEnemy
        else:
            initial_enemy = EnemyUnit((enemy_x_pos, enemy_y_pos)) # Spawn EnemyUnit
        self.enemy_group.add(initial_enemy) # Add initial enemy to the enemy group
        logger.debug("Initial enemy spawned.")


    def _load_music_and_sounds(self):
        """
        Loads background music and sound effects for the PlayingState.
        Handles potential loading errors gracefully.
        """
        try:
            pygame.mixer.music.load(get_asset_path("background.mp3")) # Load background music
            pygame.mixer.music.set_volume(config["volume"]) # Set music volume from config
            pygame.mixer.music.play(-1) # Start playing music in a loop
            logger.debug("Background music loaded and started.")
        except Exception as e:
            logger.error(f"Error loading background music: {e}")

        try:
            self.collision_sound = pygame.mixer.Sound(get_asset_path("collision.wav")) # Load collision sound effect
            logger.debug("Collision sound loaded.")
        except Exception as e:
            logger.error(f"Error loading collision sound: {e}")
            self.collision_sound = None # Set to None if loading fails


    def process_events(self, events: list[pygame.event.Event]) -> str | None:
        """
        Handles events for the PlayingState.

        Listens for QUIT, P (Pause), O (Settings), and SPACE (Fire Projectile) key events.

        Args:
            events: A list of pygame.event.Event objects.

        Returns:
            STATE_QUIT if QUIT event, STATE_PAUSED for pause, STATE_SETTINGS for settings, otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return STATE_QUIT # Signal quit
            elif event.type == pygame.KEYDOWN:
                logger.debug(f"KEYDOWN event detected: key code = {event.key}, key name = {pygame.key.name(event.key)}") # Debug log key presses
                if event.key == pygame.K_p:
                    logger.debug("P key pressed. Transitioning to PauseState.")
                    return STATE_PAUSED # Pause game on 'P' press
                elif event.key == pygame.K_o:
                    logger.debug("O key pressed. Transitioning to SettingsState.")
                    return STATE_SETTINGS # Open settings on 'O' press
                elif event.key == pygame.K_SPACE:
                    self._fire_projectile() # Fire projectile on Space press
                elif event.key == pygame.K_F3:
                    # Toggle debug overlay when F3 is pressed
                    self.show_debug_info = not self.show_debug_info
                    logger.debug(f"Debug overlay toggled to {self.show_debug_info}")
        return None # No state change

    def _fire_projectile(self):
        """
        Creates and adds a projectile to the projectile group, fired by the player.
        """
        spawn_pos = (self.soldier.rect.centerx, self.soldier.rect.top - 5) # Projectile spawn position (slightly above soldier)
        projectile = Projectile(spawn_pos, self.projectile_speed) # Create projectile sprite
        self.projectile_group.add(projectile) # Add projectile to group
        logger.debug(f"Projectile fired from {spawn_pos}")


    def update(self):
        """
        Updates game logic in the PlayingState: player, enemies, projectiles, collisions, level progression, power-ups, etc.
        """
        keys = pygame.key.get_pressed() # Get currently pressed keys

        self.parallax_background.update() # Update background parallax effect
        self.soldier_group.update(keys) # Update player soldier based on key presses
        self.enemy_group.update() # Update enemies
        self.projectile_group.update() # Update player projectiles
        self.boss_projectile_group.update() # Update boss projectiles
        self.powerup_group.update() # Update power-ups
        self.explosion_group.update() # Update explosions (animation)
        self.structure_group.update() # Update structures (if any animation)
        self.drone_group.update() # Update drones

        self._spawn_drones_randomly() # Randomly spawn drone enemies
        self._increase_score() # Increment score based on time
        self._check_level_up() # Check if level should increase and handle level up logic
        self._boss_actions() # Handle boss enemy actions (attacks, spawning)
        self._spawn_powerups_over_time() # Spawn power-ups at intervals
        self._update_shield_status() # Update shield active status based on timer
        self._update_invulnerability_timer() # Update player invulnerability timer

        self._handle_projectile_enemy_collisions() # Handle collisions between player projectiles and enemies
        self._handle_boss_projectile_collisions() # Handle collisions between boss projectiles and player
        self._handle_powerup_collisions() # Handle collisions between player and power-ups
        self._handle_enemy_soldier_collision() # Handle collisions between enemies and player soldier


    def _spawn_drones_randomly(self):
        """
        Randomly spawns drone enemies at the top of the screen.
        """
        if random.random() < 0.01: # 1% chance to spawn a drone per frame
            drone = Drone((0, random.randint(50, 200))) # Spawn drone at random Y position near top
            self.drone_group.add(drone) # Add drone to drone group


    def _increase_score(self):
        """
        Increments the player's score over time.
        """
        self.score += 1 # Increment score each frame


    def _check_level_up(self):
        """
        Checks if the score threshold for leveling up is reached and handles level up logic.
        Increases level, enemy speed, spawns new enemies, and transitions to UpgradeState.
        """
        new_level = self.score // 1000 + 1 # Calculate new level based on score
        if new_level > self.level:
            self.level = new_level # Increase level
            logger.info(f"Level Up! Current Level: {self.level}")

            for enemy in self.enemy_group: # Increase speed of existing enemies
                enemy.speed = enemy.base_speed + (self.level - 1)

            self._spawn_new_enemy_on_level_up() # Spawn a new enemy on level up

            if self.level >= 5: # Check if boss should be spawned
                self._spawn_boss_if_not_exists() # Spawn boss if level 5 or higher and no boss present

            self.next_state = STATE_UPGRADE # Transition to upgrade state after level up


    def _spawn_new_enemy_on_level_up(self):
        """
        Spawns a new regular enemy (AnimatedEnemy or EnemyUnit) when the level increases.
        """
        if random.random() < 0.5:
            new_enemy = AnimatedEnemy((random.randint(50, 750), random.randint(50, 550))) # Spawn AnimatedEnemy randomly
        else:
            new_enemy = EnemyUnit((random.randint(50, 750), random.randint(50, 550))) # Spawn EnemyUnit randomly
        new_enemy.speed = new_enemy.base_speed + (self.level - 1) # Increase new enemy speed based on level
        self.enemy_group.add(new_enemy) # Add new enemy to enemy group
        logger.debug(f"New enemy spawned due to level up. Level: {self.level}")


    def _spawn_boss_if_not_exists(self):
        """
        Spawns a BossEnemy if the current level is 5 or greater and no boss is already present.
        """
        boss_exists = any(isinstance(enemy, BossEnemy) for enemy in self.enemy_group) # Check if a BossEnemy already exists
        if not boss_exists:
            boss = BossEnemy((random.randint(100, 700), random.randint(100, 300))) # Spawn boss at random position
            boss.speed = boss.base_speed + (self.level - 1) # Set boss speed based on level
            boss.health = config["boss_health"] # Set boss health from config
            self.enemy_group.add(boss) # Add boss to enemy group
            logger.info("Boss spawned!")


    def _boss_actions(self):
        """
        Handles actions specific to BossEnemy units, such as attacking.
        """
        for enemy in self.enemy_group:
            if isinstance(enemy, BossEnemy): # Check if enemy is a BossEnemy
                enemy.attack_timer += 1 # Increment boss attack timer
                if enemy.attack_timer >= 180: # Boss attack interval (every 180 frames)
                    boss_projectile = BossProjectile(enemy.rect.center) # Create boss projectile
                    self.boss_projectile_group.add(boss_projectile) # Add to boss projectile group
                    enemy.attack_timer = 0 # Reset attack timer
                    logger.debug("Boss fired projectile.")


    def _spawn_powerups_over_time(self):
        """
        Spawns power-ups randomly at intervals.
        """
        self.powerup_spawn_timer_ms += self.clock.get_time() # Increment power-up spawn timer by elapsed time
        if self.powerup_spawn_timer_ms >= self.powerup_spawn_interval_ms: # Check if spawn interval reached
            powerup_pos = (random.randint(30, 770), -15) # Spawn power-up at random X near top
            if random.random() < 0.5:
                powerup = ShieldPowerUp(powerup_pos) # Spawn ShieldPowerUp (50% chance)
            else:
                powerup = PowerUp(powerup_pos) # Spawn regular PowerUp (50% chance)
            self.powerup_group.add(powerup) # Add power-up to group
            self.powerup_spawn_timer_ms = 0 # Reset power-up timer
            logger.debug(f"Power-up spawned: {type(powerup).__name__} at {powerup_pos}")


    def _update_shield_status(self):
        """
        Updates the shield status based on the shield timer. Deactivates shield when timer runs out.
        """
        if self.is_shield_active:
            self.shield_timer_ms -= self.clock.get_time() # Decrement shield timer by elapsed time
            if self.shield_timer_ms <= 0:
                self.is_shield_active = False # Deactivate shield
                self.shield_timer_ms = 0 # Reset timer
                logger.debug("Shield deactivated.")


    def _update_invulnerability_timer(self):
        """
        Updates the player's invulnerability timer. Decrements timer if active.
        """
        if self.invulnerable_timer_ms > 0:
            self.invulnerable_timer_ms -= self.clock.get_time() # Decrement invulnerability timer


    def _handle_projectile_enemy_collisions(self):
        """
        Handles collisions between player projectiles and enemies.
        Reduces enemy health, increases score, spawns explosions, and removes enemies if health is depleted.
        """
        collisions = pygame.sprite.groupcollide(self.projectile_group, self.enemy_group, True, False) # Detect projectile-enemy collisions
        for projectile, enemies in collisions.items():
            for enemy in enemies:
                if hasattr(enemy, "health"): # Check if enemy has health attribute (BossEnemy, AnimatedEnemy, EnemyUnit)
                    enemy.health -= 1 # Decrease enemy health
                    self.score += 100 # Increase score for hit
                    explosion = Explosion(enemy.rect.center) # Create explosion at collision point
                    self.explosion_group.add(explosion) # Add explosion to group

                    if enemy.health <= 0: # Check if enemy health is depleted
                        self.score += 500 # Increase score for enemy kill
                        enemy.kill() # Remove enemy sprite
                        logger.debug(f"{type(enemy).__name__} destroyed. Score +500.")
                else: # Handle collision for enemies without health (e.g., Drones if they had no health)
                    self.score += 100 # Increase score
                    explosion = Explosion(enemy.rect.center) # Create explosion
                    self.explosion_group.add(explosion) # Add explosion
                    enemy.rect.center = (random.randint(50, 750), random.randint(50, 550)) # Reposition enemy (e.g., Drone respawn)
                    logger.debug(f"{type(enemy).__name__} hit (no health). Repositioned.")


    def _handle_boss_projectile_collisions(self):
        """
        Handles collisions between boss projectiles and the player soldier.
        Reduces player lives, activates invulnerability, and handles game over if lives reach zero.
        """
        if pygame.sprite.spritecollideany(self.soldier, self.boss_projectile_group): # Check for soldier-boss projectile collision
            if self.is_shield_active: # Check if shield is active
                logger.info("Shield absorbed boss attack!")
                self.is_shield_active = False # Deactivate shield
                self.shield_timer_ms = 0 # Reset shield timer
                pygame.sprite.spritecollide(self.soldier, self.boss_projectile_group, True) # Remove boss projectiles on collision
            elif self.invulnerable_timer_ms == 0: # Check if player is not invulnerable
                self.lives -= 1 # Decrease player lives
                logger.info(f"Hit by boss projectile! Lives remaining: {self.lives}")
                if self.collision_sound:
                    self.collision_sound.play() # Play collision sound
                self.soldier.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2) # Reposition player
                self.invulnerable_timer_ms = 2000 # Set invulnerability timer (2 seconds)

                if self.lives <= 0: # Check for game over
                    logger.info("No lives left! Game Over!")
                    pygame.mixer.music.stop() # Stop background music
                    self.next_state = STATE_GAMEOVER # Transition to game over state
                else:
                    self.next_state = STATE_PLAYING # Stay in playing state (but player hit)
            # else: # Player is invulnerable, no damage
            #     self.next_state = STATE_PLAYING # Stay in playing state


    def _handle_powerup_collisions(self):
        """
        Handles collisions between the player soldier and power-ups.
        Activates shield or grants extra life based on power-up type.
        """
        powerup_hits = pygame.sprite.spritecollide(self.soldier, self.powerup_group, True) # Detect soldier-powerup collisions
        for powerup in powerup_hits:
            if isinstance(powerup, ShieldPowerUp): # Check if power-up is ShieldPowerUp
                self.is_shield_active = True # Activate shield
                self.shield_timer_ms = self.shield_duration_ms # Set shield timer
                logger.info("Shield activated!")
            else: # Assume it's a regular PowerUp (extra life)
                self.lives += 1 # Increase player lives
                logger.info("Extra life collected!")


    def _handle_enemy_soldier_collision(self):
        """
        Handles collisions between regular enemies and the player soldier.
        Reduces player lives, activates invulnerability, and handles game over if lives reach zero.
        """
        if pygame.sprite.spritecollideany(self.soldier, self.enemy_group): # Check for soldier-enemy collision
            if self.is_shield_active: # Check if shield is active
                logger.info("Shield absorbed enemy damage!")
                self.is_shield_active = False # Deactivate shield
                self.shield_timer_ms = 0 # Reset shield timer
            elif self.invulnerable_timer_ms == 0: # Check if player is not invulnerable
                self.lives -= 1 # Decrease player lives
                logger.info(f"Enemy collision! Lives remaining: {self.lives}")
                if self.collision_sound:
                    self.collision_sound.play() # Play collision sound
                self.soldier.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2) # Reposition player
                self.invulnerable_timer_ms = 2000 # Set invulnerability timer (2 seconds)

                if self.lives <= 0: # Check for game over
                    logger.info("No lives left! Game Over!")
                    pygame.mixer.music.stop() # Stop music
                    self.next_state = STATE_GAMEOVER # Transition to game over
                else:
                    self.next_state = STATE_PLAYING # Stay in playing state
            # else: # Player is invulnerable, no damage
            #     self.next_state = STATE_PLAYING # Stay in playing state


    def draw(self):
        """
        Draws all elements of the PlayingState: background, structures, sprites, UI, and boss health bars.
        """
        self.parallax_background.draw() # Draw parallax background
        self.structure_group.draw(self.screen) # Draw level structures
        self.soldier_group.draw(self.screen) # Draw player soldier
        self.enemy_group.draw(self.screen) # Draw enemies
        self.projectile_group.draw(self.screen) # Draw player projectiles
        self.boss_projectile_group.draw(self.screen) # Draw boss projectiles
        self.powerup_group.draw(self.screen) # Draw power-ups
        self.explosion_group.draw(self.screen) # Draw explosions
        self.drone_group.draw(self.screen) # Draw drones

        self._draw_ui() # Draw score, level, lives
        self._draw_shield_indicator() # Draw shield visual indicator if active
        self._draw_boss_health_bars() # Draw boss health bars
        if self.show_debug_info:
            self._draw_debug_info()


    def _draw_ui(self):
        """
        Draws the score, level, and lives UI elements on the screen.
        """
        score_text_surface = self.font.render(f"Score: {self.score}", True, (0, 0, 0)) # Render score text
        level_text_surface = self.font.render(f"Level: {self.level}", True, (0, 0, 0)) # Render level text
        lives_text_surface = self.font.render(f"Lives: {self.lives}", True, (0, 0, 0)) # Render lives text

        self.screen.blit(score_text_surface, (10, 10)) # Position score top-left
        self.screen.blit(level_text_surface, (self.screen.get_width() // 2 - level_text_surface.get_width() // 2, 10)) # Center level
        self.screen.blit(lives_text_surface, (self.screen.get_width() - lives_text_surface.get_width() - 10, 10)) # Position lives top-right


    def _draw_shield_indicator(self):
        """
        Draws a visual indicator (circle) around the player soldier when the shield is active.
        """
        if self.is_shield_active:
            shield_color = (0, 255, 255) # Cyan color for shield
            shield_radius = 35
            shield_border_width = 3
            pygame.draw.circle(self.screen, shield_color, self.soldier.rect.center, shield_radius, shield_border_width) # Draw shield circle


    def _draw_boss_health_bars(self):
        """
        Draws health bars above BossEnemy sprites.
        """
        for enemy in self.enemy_group:
            if isinstance(enemy, BossEnemy): # Check if enemy is BossEnemy
                bar_width = enemy.rect.width # Health bar width matches enemy width
                bar_height = 5 # Health bar height
                health_ratio = enemy.health / config["boss_health"] # Health ratio for bar fill
                health_bar_width = int(bar_width * health_ratio) # Calculate filled width
                health_bar_rect = pygame.Rect(enemy.rect.left, enemy.rect.top - 10, health_bar_width, bar_height) # Health bar rect (above enemy)
                border_rect = pygame.Rect(enemy.rect.left, enemy.rect.top - 10, bar_width, bar_height) # Border rect
                pygame.draw.rect(self.screen, (0, 255, 0), health_bar_rect) # Draw filled health bar (green)
                pygame.draw.rect(self.screen, (255, 255, 255), border_rect, 1) # Draw health bar border (white)


        pygame.display.flip() # Update display
        self.clock.tick(60) # Limit FPS

    def _draw_debug_info(self):
        """Draw the FPS and player position for debugging."""
        fps_text = self.font.render(f"FPS: {self.clock.get_fps():.1f}", True, (255, 255, 0))
        pos_text = self.font.render(f"Pos: {self.soldier.rect.center}", True, (255, 255, 0))
        self.screen.blit(fps_text, (10, 40))
        self.screen.blit(pos_text, (10, 60))


# ------------------------------
# PauseState
# ------------------------------
class PauseState:
    """
    State for pausing the game.
    """
    def __init__(self, screen: pygame.Surface, playing_state: "PlayingState"):
        """
        Initializes the PauseState.

        Args:
            screen: The pygame.Surface to draw on.
            playing_state: Reference to the PlayingState to return to.
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.playing_state = playing_state # Store PlayingState reference
        self.font_large = pygame.font.Font(None, 74) # Large font for "Paused"
        self.font_small = pygame.font.Font(None, 36) # Small font for instructions
        self.pause_text_surface = self.font_large.render("Paused", True, (255, 255, 255)) # Render "Paused" text
        self.pause_rect = self.pause_text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50)) # Position "Paused"
        self.instruction_surface = self.font_small.render("Press P to Resume", True, (255, 255, 255)) # Render instruction
        self.instruction_rect = self.instruction_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50)) # Position instruction
        logger.debug("PauseState initialized.")


    def process_events(self, events: list[pygame.event.Event]) -> str | None:
        """
        Handles events for the PauseState.

        Listens for QUIT and P key events to resume the game.

        Args:
            events: A list of pygame.event.Event objects.

        Returns:
            STATE_QUIT if QUIT event, STATE_PLAYING to resume game, otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return STATE_QUIT # Signal quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    logger.debug("P key pressed in PauseState. Transitioning to PlayingState.")
                    return STATE_PLAYING # Resume game on 'P' press
        return None # No state change

    def update(self):
        """
        Updates the PauseState (currently no dynamic updates).
        """
        pass # No updates needed in pause state

    def draw(self):
        """
        Draws the pause screen with "Paused" text and instructions.
        """
        self.screen.fill((0, 0, 0)) # Black background
        self.screen.blit(self.pause_text_surface, self.pause_rect) # Draw "Paused" text
        self.screen.blit(self.instruction_surface, self.instruction_rect) # Draw instructions
        pygame.display.flip() # Update display
        self.clock.tick(60) # Limit FPS


# ------------------------------
# GameOverState
# ------------------------------
class GameOverState:
    """
    State for the game over screen, displaying the final score and high score.
    """
    def __init__(self, screen: pygame.Surface, final_score: int):
        """
        Initializes the GameOverState.

        Args:
            screen: The pygame.Surface to draw on.
            final_score: The player's final score in the game.
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.final_score = final_score # Store final score
        self.font_large = pygame.font.Font(None, 74) # Large font for "Game Over"
        self.font_small = pygame.font.Font(None, 36) # Small font for score and instructions
        self.gameover_text_surface = self.font_large.render("Game Over", True, (255, 255, 255)) # Render "Game Over"
        self.gameover_rect = self.gameover_text_surface.get_rect(center=(self.screen.get_width() // 2, 150)) # Position "Game Over"
        self.score_surface = self.font_small.render(f"Final Score: {final_score}", True, (255, 255, 255)) # Render score
        self.score_rect = self.score_surface.get_rect(center=(self.screen.get_width() // 2, 250)) # Position score

        high_score = load_high_score() # Load high score from file
        if final_score > high_score:
            save_high_score(final_score) # Save new high score if current score is higher
            high_score = final_score # Update high_score to the new value

        self.high_score_surface = self.font_small.render(f"High Score: {high_score}", True, (255, 255, 255)) # Render high score
        self.high_score_rect = self.high_score_surface.get_rect(center=(self.screen.get_width() // 2, 320)) # Position high score
        self.instruction_surface = self.font_small.render("Press R to Restart or M for Menu", True, (255, 255, 255)) # Instructions
        self.instruction_rect = self.instruction_surface.get_rect(center=(self.screen.get_width() // 2, 400)) # Instruction position
        logger.debug(f"GameOverState initialized. Final Score: {final_score}, High Score: {high_score}")


    def process_events(self, events: list[pygame.event.Event]) -> str | None:
        """
        Handles events for the GameOverState.

        Listens for QUIT, R (Restart), and M (Menu) key events.

        Args:
            events: A list of pygame.event.Event objects.

        Returns:
            STATE_QUIT if QUIT event, STATE_PLAYING to restart game, STATE_MENU to go to main menu, otherwise None.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return STATE_QUIT # Signal quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    logger.debug("R key pressed in GameOverState. Transitioning to PlayingState (restart).")
                    return STATE_PLAYING # Restart game on 'R' press
                elif event.key == pygame.K_m:
                    logger.debug("M key pressed in GameOverState. Transitioning to MainMenu.")
                    return STATE_MENU # Go to main menu on 'M' press
        return None # No state change

    def update(self):
        """
        Updates the GameOverState (currently no dynamic updates).
        """
        pass # No updates needed in game over state

    def draw(self):
        """
        Draws the game over screen with "Game Over" text, final score, high score, and instructions.
        """
        self.screen.fill((0, 0, 0)) # Black background
        self.screen.blit(self.gameover_text_surface, self.gameover_rect) # Draw "Game Over"
        self.screen.blit(self.score_surface, self.score_rect) # Draw final score
        self.screen.blit(self.high_score_surface, self.high_score_rect) # Draw high score
        self.screen.blit(self.instruction_surface, self.instruction_rect) # Draw instructions
        pygame.display.flip() # Update display
        self.clock.tick(60) # Limit FPS