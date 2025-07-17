import os
import pygame
from datetime import datetime


def capture_screenshot(screen: pygame.Surface, directory: str = "screenshots") -> str:
    """Save a screenshot of the given screen to the specified directory."""
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(directory, f"screenshot_{timestamp}.png")
    pygame.image.save(screen, path)
    return path
