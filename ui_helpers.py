# ui_helpers.py
import pygame

def draw_vertical_gradient(surface, color_top, color_bottom):
    """Draws a vertical gradient over the entire surface."""
    height = surface.get_height()
    width = surface.get_width()
    for y in range(height):
        ratio = y / height
        color = (
            int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio),
            int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio),
            int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        )
        pygame.draw.line(surface, color, (0, y), (width, y))
