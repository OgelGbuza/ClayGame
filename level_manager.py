# level_manager.py
import pygame
import os
import logging
from data_loader import load_json  # Assuming you have a data_loader.py for JSON loading
from resources import load_image_with_scale

logger = logging.getLogger(__name__)

class LevelManager:
    """
    Manages level loading, rendering, and object placement based on level data from a JSON file.

    Attributes:
        level_data: A dictionary containing level information loaded from a JSON file.
        background: pygame.Surface for the level background image, or None if no background is specified.
        tile_size:  Integer representing the size of each tile in pixels.
        tileset:    pygame.Surface containing the tileset image, or None if no tileset is specified.
        layout:     2D list representing the tile layout of the level.
        objects:    List of dictionaries, each defining an object to be placed in the level.
        object_assets: Dictionary mapping object types to their asset paths.
        loaded_objects: List of tuples, each containing a pygame.Surface (object image) and its position (tuple).
        npcs_data:  List of dictionaries, each defining NPC (Non-Player Character) data for the level.
    """
    def __init__(self, level_filename: str):
        """
        Initializes the LevelManager by loading level data from the specified JSON file.

        Args:
            level_filename: Path to the JSON file containing level data.
        """
        self.level_data = self._load_level_data(level_filename) # Load level data from JSON
        if not self.level_data: # Handle case where level data loading failed
            raise ValueError(f"Failed to load level data from: {level_filename}. LevelManager cannot be initialized.")

        self.background = self._load_background() # Load background image
        self.tile_size = self.level_data.get("tile_size", 32) # Default tile size if not in level data
        self.tileset = self._load_tileset() # Load tileset image
        self.layout = self.level_data.get("layout", []) # Default to empty layout if not specified
        self.objects = self.level_data.get("objects", []) # Default to empty objects list
        self.object_assets = { # Define object asset paths - consider moving to config or data file if more objects are added
            "tree": "assets/tree.png",
            "rock": "assets/rock.png"
        }
        self.loaded_objects = self._load_level_objects() # Load and create object sprites
        self.npcs_data = self.level_data.get("npcs", []) # Load NPC data

        logger.debug(f"LevelManager initialized for level: {level_filename}")


    def _load_level_data(self, level_filename: str) -> dict:
        """
        Loads level data from a JSON file.

        Args:
            level_filename: Path to the JSON level file.

        Returns:
            A dictionary containing the level data, or None if loading fails.
        """
        try:
            level_data = load_json(level_filename) # Use data_loader to load JSON
            logger.debug(f"Level data loaded successfully from: {level_filename}")
            return level_data
        except FileNotFoundError:
            logger.error(f"Level JSON file not found: {level_filename}")
            return None
        except Exception as e: # Catch other potential JSON loading errors
            logger.error(f"Error loading level data from {level_filename}: {e}")
            return None

    def _load_background(self) -> pygame.Surface | None:
        """
        Loads the background image for the level, if specified in the level data.

        Returns:
            A pygame.Surface for the background, or None if no background path is in level data.
        """
        bg_path = self.level_data.get("background")
        if bg_path:
            background_image = load_image_with_scale(bg_path, (800, 600))
            if background_image:
                logger.debug(f"Background image loaded: {bg_path}")
                return background_image
            else:
                logger.warning(f"Failed to load background image from path specified in level data: {bg_path}")
        return None # No background path specified or loading failed

    def _load_tileset(self) -> pygame.Surface | None:
        """
        Loads the tileset image for the level, if specified in the level data.

        Assumes the tileset is a horizontal strip of 10 tiles.

        Returns:
            A pygame.Surface for the tileset, or None if no tileset path is in level data.
        """
        tileset_path = self.level_data.get("tileset")
        tile_size = self.level_data.get("tile_size", 32) # Ensure tile_size is available
        if tileset_path:
            tileset_image = load_image_with_scale(tileset_path, (tile_size * 10, tile_size)) # Assuming 10 tiles in a row
            if tileset_image:
                logger.debug(f"Tileset image loaded: {tileset_path}")
                return tileset_image
            else:
                logger.warning(f"Failed to load tileset image from path specified in level data: {tileset_path}")
        return None # No tileset path specified or loading failed


    def _load_level_objects(self) -> list[tuple[pygame.Surface, list[int]]]:
        """
        Loads and creates pygame.Surface objects for level objects based on the level data.

        Returns:
            A list of tuples, where each tuple contains:
            - A pygame.Surface representing the object's image.
            - A list [x, y] representing the object's position.
        """
        loaded_objects = []
        for obj_data in self.objects:
            obj_type = obj_data.get("type")
            pos = obj_data.get("position", [0, 0]) # Default position if not specified
            asset_path = self.object_assets.get(obj_type) # Get asset path from object_assets dictionary

            if asset_path:
                image = load_image_with_scale(asset_path, (self.tile_size, self.tile_size)) # Load and scale object image
                if image:
                    loaded_objects.append((image, pos)) # Add image and position to the list
                    logger.debug(f"Loaded object: {obj_type} at position: {pos}")
                else:
                    logger.warning(f"Failed to load image for object type: {obj_type} from path: {asset_path}")
            else:
                logger.warning(f"Object type '{obj_type}' has no asset path defined in object_assets.")
        return loaded_objects


    def draw(self, screen: pygame.Surface):
        """
        Draws the level background, tiles, and objects onto the given screen.

        Args:
            screen: The pygame.Surface to draw the level onto.
        """
        if self.background:
            screen.blit(self.background, (0, 0)) # Draw background first
        else:
            screen.fill((0, 0, 0)) # Fill screen with black if no background

        self._draw_tiles(screen) # Draw level tiles
        self._draw_objects(screen) # Draw level objects


    def _draw_tiles(self, screen: pygame.Surface):
        """
        Draws the level tiles based on the layout and tileset.

        Args:
            screen: The pygame.Surface to draw the tiles onto.
        """
        if not self.tileset or not self.layout: # Check if tileset and layout are loaded
            return # Exit if tileset or layout is missing

        tile_size = self.tile_size # Get tile size for calculations
        for row_idx, row in enumerate(self.layout):
            for col_idx, tile_index in enumerate(row):
                if tile_index > 0: # Tile index 0 is considered empty/transparent
                    source_rect = pygame.Rect((tile_index - 1) * tile_size, 0, tile_size, tile_size) # Calculate source rect in tileset
                    dest_rect = pygame.Rect(col_idx * tile_size, row_idx * tile_size, tile_size, tile_size) # Calculate destination rect on screen
                    screen.blit(self.tileset, dest_rect, source_rect) # Blit tile onto the screen


    def _draw_objects(self, screen: pygame.Surface):
        """
        Draws the loaded level objects onto the screen.

        Args:
            screen: The pygame.Surface to draw the objects onto.
        """
        for image, pos in self.loaded_objects:
            screen.blit(image, pos) # Blit each object image at its position