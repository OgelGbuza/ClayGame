# config.py
# Global configuration and state constants

import os

# Game configuration settings
config = {
    "volume": 0.5,  # Initial music volume (0.0 to 1.0)
    "control_scheme": "arrows",  # Default control scheme: "arrows" or "wasd"
    "art_theme": "default",      # Default art theme: "default" or "dark"
    "boss_health": 5             # Initial boss health points
}

def load_high_score():
    """
    Loads the high score from the 'highscore.txt' file.
    Returns the high score as an integer, or 0 if the file is not found or an error occurs.
    """
    try:
        filepath = os.path.join(".", "highscore.txt") # Ensure file is in the same directory
        with open(filepath, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        print("Highscore file not found. Initializing high score to 0.")
        return 0
    except ValueError:
        print("Error reading highscore file. Resetting high score to 0.")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred while loading high score: {e}")
        return 0

def save_high_score(score):
    """
    Saves the given score to the 'highscore.txt' file.
    Creates the file if it doesn't exist.
    """
    try:
        filepath = os.path.join(".", "highscore.txt") # Ensure file is in the same directory
        with open(filepath, "w") as f:
            f.write(str(score))
    except Exception as e:
        print(f"Error saving high score: {e}")


def reset_high_score() -> None:
    """Reset the stored high score to zero."""
    save_high_score(0)


# Game state constants - used by the state manager to control game flow
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_SETTINGS = "settings"
STATE_UPGRADE = "upgrade"
STATE_INVENTORY = "inventory" # (Not currently used in the provided code, but defined)
STATE_QUEST_JOURNAL = "quest_journal" # (Not currently used in the provided code, but defined)
STATE_CUTSCENE = "cutscene"
STATE_QUIT = "quit"
STATE_DIALOGUE = "dialogue"
STATE_GAMEOVER = "gameover"
STATE_PUTIN_CUTSCENE = "putin_cutscene"
