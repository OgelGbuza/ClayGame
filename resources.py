# resources.py
import pygame
import os
import logging

# Set up logging for resource loading (useful for debugging)
logger = logging.getLogger(__name__)

# Resource cache to store loaded images and sounds for efficiency
_resource_cache = {}

def get_asset_path(filename: str) -> str:
    """
    Constructs the full path to an asset file.

    If the given filename is not already absolute and doesn't start with "assets",
    it prepends the "assets" directory to the filename. This assumes all game
    assets are located in the "assets" subdirectory relative to the script's location.

    Args:
        filename: The name of the asset file (e.g., "player.png").

    Returns:
        The full, normalized path to the asset file.
    """
    normalized_path = os.path.normpath(filename) # Normalize path for OS compatibility

    if normalized_path.startswith("assets"):
        return normalized_path # Assume path is already correctly specified
    return os.path.join("assets", normalized_path) # Prepend "assets" directory

def load_image_with_scale(path: str, expected_size: tuple[int, int], colorkey=None) -> pygame.Surface:
    """
    Loads an image from the given path, scales it to the expected size, and applies an optional colorkey.

    Utilizes a resource cache to avoid reloading images from disk repeatedly.
    If the image is not found in the cache, it is loaded, scaled, and then stored in the cache.

    Args:
        path:      Path to the image file, relative to the 'assets' directory.
        expected_size:  Tuple (width, height) defining the size to scale the image to.
        colorkey:  Optional color to set as transparent (e.g., pygame.Color('white')).
                   If None, no transparency is set.

    Returns:
        A pygame.Surface object representing the loaded and processed image.
        Returns an empty, transparent Surface of the expected size if loading fails.
    """
    global _resource_cache
    full_path = get_asset_path(path)

    if full_path in _resource_cache:
        return _resource_cache[full_path] # Return cached image if available

    try:
        image = pygame.image.load(full_path).convert_alpha() # Load and convert with alpha transparency
        current_size = image.get_size()
        if current_size != expected_size:
            logger.debug(f"Scaling image {path} from {current_size} to {expected_size}")
            image = pygame.transform.scale(image, expected_size) # Scale image to expected size

        if colorkey is not None:
            image.set_colorkey(colorkey) # Set specific color to be transparent

    except pygame.error as e: # Catch Pygame image loading errors specifically
        logger.error(f"Error loading image {path}: {e}")
        image = pygame.Surface(expected_size, pygame.SRCALPHA) # Create a transparent surface as a placeholder
        image.fill((0, 0, 0, 0)) # Fill with transparent black

    _resource_cache[full_path] = image # Store loaded image in cache
    return image

def load_sprite_sheet(path: str, frame_width: int, frame_height: int, num_frames: int, colorkey=None) -> list[pygame.Surface]:
    """
    Loads a sprite sheet from the given path and extracts individual frames.

    Assumes the sprite sheet is a horizontal strip of frames of equal size.
    Returns a list of pygame.Surface objects, each representing a frame.

    Args:
        path:        Path to the sprite sheet image file.
        frame_width:   Width of each frame in pixels.
        frame_height:  Height of each frame in pixels.
        num_frames:    Number of frames in the sprite sheet.
        colorkey:    Optional color to set as transparent for the entire sheet.

    Returns:
        A list of pygame.Surface objects, where each Surface is a frame from the sprite sheet.
        Returns an empty list if loading fails.
    """
    full_path = get_asset_path(path)

    try:
        sprite_sheet = pygame.image.load(full_path).convert_alpha() # Load sprite sheet
        expected_sheet_size = (frame_width * num_frames, frame_height)
        current_sheet_size = sprite_sheet.get_size()

        if current_sheet_size != expected_sheet_size:
            logger.debug(f"Scaling sprite sheet {path} from {current_sheet_size} to {expected_sheet_size}")
            sprite_sheet = pygame.transform.scale(sprite_sheet, expected_sheet_size) # Scale if size doesn't match

        if colorkey is not None:
            sprite_sheet.set_colorkey(colorkey) # Apply colorkey transparency to the whole sheet

        frames = []
        for i in range(num_frames):
            frame_rect = (i * frame_width, 0, frame_width, frame_height) # Calculate frame rectangle
            frame = sprite_sheet.subsurface(frame_rect).copy() # Extract frame as a subsurface and create independent copy
            frames.append(frame)
        return frames

    except pygame.error as e: # Catch Pygame image loading errors
        logger.error(f"Error loading sprite sheet {path}: {e}")
        return [] # Return empty list if loading fails

def load_sound(path: str) -> pygame.mixer.Sound | None:
    """
    Loads a sound file from the given path.

    Uses resource caching to store loaded sounds.

    Args:
        path: Path to the sound file, relative to the 'assets' directory.

    Returns:
        A pygame.mixer.Sound object if loading is successful, otherwise None.
    """
    global _resource_cache
    full_path = get_asset_path(path)

    if full_path in _resource_cache:
        return _resource_cache[full_path] # Return cached sound if available

    try:
        sound = pygame.mixer.Sound(full_path) # Load sound file
    except pygame.error as e: # Catch Pygame sound loading errors
        logger.error(f"Error loading sound {path}: {e}")
        sound = None # Return None if loading fails

    _resource_cache[full_path] = sound # Cache the loaded sound (or None in case of failure)
    return sound

def clear_cache():
    """
    Clears the resource cache.

    This forces resources to be reloaded from disk on their next access.
    Useful for debugging or resource reloading scenarios.
    """
    global _resource_cache
    _resource_cache.clear() # Clear the dictionary to release cached resources
    logger.debug("Resource cache cleared.")