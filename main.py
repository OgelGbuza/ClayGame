# ====================== File: main.py (Modified State Transition) ======================
import pygame, sys, logging
from config import *
from states import MainMenu, PlayingState  # Ensure these are defined in your states module
from skill_tree_state import SkillTreeState
from narrative_cutscene_state import NarrativeCutsceneState
from dialogue_journal_state import DialogueJournalState
from state_manager import StateManager
from save_load import save_game, load_game
from settings_state import SettingsState
from inventory_state import InventoryState
from quest_journal_state import QuestJournalState
from pause_state import PauseState
from level_manager import LevelManager

import resources
resources

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def fade_transition(screen, duration=500):
    fade = pygame.Surface(screen.get_size()).convert_alpha()
    clock = pygame.time.Clock()
    for alpha in range(0, 256, 5):
        fade.fill((0, 0, 0, alpha))
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(60)
    for alpha in range(255, -1, -5):
        fade.fill((0, 0, 0, alpha))
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        clock.tick(60)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pixel War: Multiverse Battle")

    # Start with MainMenu.
    menu_state = MainMenu(screen)
    manager = StateManager(menu_state)

    # Push narrative cutscene state on top.
    cutscene_state = NarrativeCutsceneState(screen, filename="cutscene_intro.json")
    manager.push_state(cutscene_state)

    current_settings = {"volume": 50, "difficulty": "Normal", "controls": "Default"}

    while True:
        # Get all events once per frame.
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Debug: check if Enter key is pressed.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            print("Enter key is pressed (get_pressed)!")

        current = manager.current_state()
        # print("Current state:", type(current).__name__)  # Debug print

        # Pass events to the current state's process_events.
        result = manager.current_state().process_events(events)

        # Update and draw current state.
        manager.current_state().update()
        manager.current_state().draw()

        # When the state signals "playing", we want to transition into the game.
        if result == "playing":
            # Clear all states (i.e. remove MainMenu and the cutscene)
            manager.states.clear()
            # Push a new PlayingState
            from states import PlayingState  # Make sure PlayingState is defined in your states module
            playing_state = PlayingState(screen)
            manager.push_state(playing_state)
            fade_transition(screen)

        pygame.time.delay(10)


if __name__ == "__main__":
    main()
