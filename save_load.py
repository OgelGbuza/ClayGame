# save_load.py
import pickle
import os
import logging

logger = logging.getLogger(__name__)
SAVE_FILENAME = "savegame.dat" # Define the default save filename as a constant

def save_game(game_state, filename: str = SAVE_FILENAME) -> bool:
    """
    Saves the current game state to a file using pickle serialization.

    Args:
        game_state: The game state object to be saved. This should be an object
                    that can be pickled (serialized).
        filename:   The name of the file to save the game state to.
                    Defaults to 'savegame.dat' if not provided.

    Returns:
        True if the game was saved successfully, False otherwise.
    """
    filepath = os.path.join(".", filename) # Ensure file is saved in the current directory
    try:
        with open(filepath, "wb") as save_file: # Open file in binary write mode
            pickle.dump(game_state, save_file) # Serialize and save the game state
        logger.info(f"Game state saved successfully to: {filename}")
        return True # Indicate successful save
    except pickle.PicklingError as pickle_err: # Catch pickle-specific serialization errors
        logger.error(f"Pickling error during game save to {filename}: {pickle_err}")
    except Exception as e: # Catch any other potential errors during file saving
        logger.error(f"General error during game save to {filename}: {e}")
    return False # Indicate save failure if any exception occurred

def load_game(filename: str = SAVE_FILENAME):
    """
    Loads a saved game state from a file using pickle deserialization.

    Args:
        filename: The name of the file to load the game state from.
                  Defaults to 'savegame.dat' if not provided.

    Returns:
        The loaded game state object if loading is successful, otherwise None.
    """
    filepath = os.path.join(".", filename) # Construct file path to savegame file
    if not os.path.exists(filepath): # Check if the save file exists
        logger.warning(f"Save file not found: {filename}")
        return None # Return None if save file doesn't exist

    try:
        with open(filepath, "rb") as save_file: # Open file in binary read mode
            loaded_state = pickle.load(save_file) # Deserialize and load the game state
        logger.info(f"Game state loaded successfully from: {filename}")
        return loaded_state # Return the loaded game state
    except pickle.UnpicklingError as pickle_err: # Catch pickle-specific deserialization errors
        logger.error(f"Unpickling error during game load from {filename}: {pickle_err}")
    except FileNotFoundError: # Explicitly handle FileNotFoundError (though unlikely after os.path.exists check)
        logger.error(f"File not found during game load (even after existence check): {filename}")
    except Exception as e: # Catch any other potential errors during file loading
        logger.error(f"General error during game load from {filename}: {e}")

    return None # Return None if loading failed for any reason