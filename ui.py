import pygame
from pygame.math import Vector2
from pygame.typing import ColorLike

class UI:
    def __init__(self, sprite: pygame.Surface, position: Vector2, size_factor: float = 1.0):
        self.sprite: pygame.Surface = sprite
        self.position: Vector2 = position
        self.size_factor: float = size_factor
        self.rect: pygame.Rect = self.sprite.get_rect(topleft=self.position)
        
    def draw(self, surface: pygame.Surface):
        """Draws a scaled version of the UI sprite

        Args:
            surface (pygame.Surface): The surface to be drawn on
        """
        sprite_copy = pygame.transform.scale(self.sprite, (self.sprite.get_width() * self.size_factor, self.sprite.get_height() * self.size_factor))
        new_rect = sprite_copy.get_rect(topleft=self.position)
        surface.blit(sprite_copy, new_rect)
        
class TextUI:
    def __init__(self, position: Vector2, text: str, color: ColorLike, font: pygame.font.Font):
        self.position: Vector2 = position
        self.text: str = text
        self.color: ColorLike = color
        self.font: pygame.font.Font = font
        self.surface = self.font.render(self.text, True, self.color) # for rendering the font once in init so rect has a shape
        self.rect: pygame.Rect = self.surface.get_rect(center=self.position)
        
    def draw(self, surface: pygame.Surface):
        """Draws text on the screen

        Args:
            surface (pygame.Surface): The surface to be drawn on
        """
        text_surface = self.font.render(self.text, True, self.color)
        new_rect = text_surface.get_rect(center=self.position)
        surface.blit(text_surface, new_rect)