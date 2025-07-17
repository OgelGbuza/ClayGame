# ====================== File: main.py (Modified State Transition) ======================
import pygame
import sys
import logging

from config import (
    STATE_MENU,
    STATE_PLAYING,
    STATE_PAUSED,
    STATE_SETTINGS,
    STATE_UPGRADE,
    STATE_GAMEOVER,
    STATE_DIALOGUE,
    STATE_PUTIN_CUTSCENE,
    STATE_QUIT,
)

from states import (
    MainMenu,
    PlayingState,
    PauseState,
    SettingsState,
    UpgradeState,
    GameOverState,
    DialogueState,
    PutinCutsceneState,
)
from skill_tree_state import SkillTreeState
from narrative_cutscene_state import NarrativeCutsceneState
from dialogue_journal_state import DialogueJournalState
from state_manager import StateManager
from save_load import save_game, load_game
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


def handle_state_transitions(manager, screen, result):
    """Handle state changes based on the result string returned by states."""
    if result is None:
        return
    if result == STATE_QUIT:
        pygame.quit()
        sys.exit()

    current = manager.current_state()

    if result == STATE_PLAYING:
        # If coming from pause/settings/upgrade, simply pop to resume
        if isinstance(current, (PauseState, SettingsState, UpgradeState, GameOverState)):
            manager.pop_state()
        else:
            # Starting the actual game from menu or cutscene
            manager.states.clear()
            playing_state = PlayingState(screen)
            manager.push_state(playing_state)
            fade_transition(screen)
    elif result == STATE_PAUSED:
        pause_state = PauseState(screen, current)
        manager.push_state(pause_state)
    elif result == STATE_SETTINGS:
        settings_state = SettingsState(screen, current)
        manager.push_state(settings_state)
    elif result == STATE_UPGRADE:
        upgrade_state = UpgradeState(screen, current)
        manager.push_state(upgrade_state)
    elif result == STATE_GAMEOVER:
        score = getattr(current, "score", 0)
        gameover_state = GameOverState(screen, score)
        manager.push_state(gameover_state)
    elif result == STATE_MENU:
        manager.states.clear()
        manager.push_state(MainMenu(screen))
    elif result == STATE_DIALOGUE:
        manager.push_state(DialogueState(screen))
    elif result == STATE_PUTIN_CUTSCENE:
        manager.push_state(PutinCutsceneState(screen))

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

        # Handle direct results from process_events
        handle_state_transitions(manager, screen, result)

        # Some states signal transitions via a `next_state` attribute (e.g. PlayingState)
        current = manager.current_state()
        next_state = getattr(current, "next_state", STATE_PLAYING)
        if isinstance(current, PlayingState) and next_state != STATE_PLAYING:
            current.next_state = STATE_PLAYING
            handle_state_transitions(manager, screen, next_state)

        pygame.time.delay(10)


if __name__ == "__main__":
    main()
