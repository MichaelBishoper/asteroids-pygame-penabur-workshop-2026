import pygame
from pygame.math import Vector2
from settings import IMAGES_DIR, LASER_SPEED

class Laser:
    def __init__(self, position):
        self.position: Vector2 = Vector2(position)
        self.sprite: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'laser.png'))
        self.rect: pygame.Rect = self.sprite.get_rect(center = self.position)
    
    def update(self, dt: float):
        """Update the laser's position. The laser moves only forward (nagtive y) from a starting coordinate.

        Args:
            dt (float): The time elapsed since the last frame, in seconds (converted and defined in the main loop).
        """
        
        self.position.y -= LASER_SPEED * dt
        self.rect.center = self.position
    
    def draw(self, surface: pygame.Surface):
        """Draws the laser's current position.

        Args:
            surface (pygame.Surface): The surface to draw the player sprite on (defined in the main loop).
        """
        
        surface.blit(self.sprite, self.rect)
        
        ##########################
        # debug: show collisions #
        ##########################
        
        # pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)
        