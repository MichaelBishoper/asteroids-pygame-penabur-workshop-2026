import pygame
from pygame.math import Vector2
from settings import IMAGES_DIR

class Asteroid:
    def __init__(self, position: Vector2, rotation: int, speed: int):
        self.position: Vector2 = Vector2(position)
        self.sprite: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'meteor.png'))
        self.rect: pygame.Rect = self.sprite.get_rect(center = self.position)
        self.rotation: int = rotation
        self.speed: int = speed
    
    def update(self, dt: float):
        """Update the asteroid's position. The asteroid moves only backward (positive y) from a starting coordinate.

        Args:
            dt (float): The time elapsed since the last frame, in seconds (converted and defined in the main loop).
        """
        
        self.position.y += self.speed * dt
        self.rect.center = self.position
        
    def draw(self, surface: pygame.Surface):
        """Draws the asteroid's current position.

        Args:
            surface (pygame.Surface): The surface to draw the asteroid sprite on (defined in the main loop).
        """
        sprite_copy = pygame.transform.rotate(self.sprite, self.rotation)
        surface.blit(sprite_copy, self.rect)
        
        ##########################
        # debug: show collisions #
        ##########################
        
        # pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)