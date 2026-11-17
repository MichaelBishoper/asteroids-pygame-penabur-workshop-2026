import pygame
from pygame.math import Vector2
from settings import IMAGES_DIR, EXPLOSION_TIME

class Explosion:
    def __init__(self, position: Vector2, rotation: int = 0, size_factor: float = 1.0, time: float = EXPLOSION_TIME):
        self.position: Vector2 = Vector2(position)
        self.rotation: int = rotation
        self.size_factor: float = size_factor
        self.sprite: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'explosion.png'))
        self.rect: pygame.Rect = self.sprite.get_rect(center = self.position)
        self.time: float = time
        self.timer: float = 0.0
        self.alive: bool = True # NOTE: an alive variable does not separate the concerns explosion from the game world itself and is hence bad OOP, but I am too lazy to refactor it
    
    def update(self, dt: float):
        """Update the explosion's internal timeer. Sets self.alive to False when the timer runs out.

        Args:
            dt (float): The time elapsed since the last frame, in seconds (converted and defined in the main loop).
        """
        self.timer = self.timer + dt
        
        # check timer after incrementing
        # explosion death logic is handled in main.py
        if self.timer >= self.time:
            self.alive = False
    
    def draw(self, surface: pygame.Surface):
        """Draws the explosion's current position.

        Args:
            surface (pygame.Surface): The surface to draw the explosion sprite on (defined in the main loop).
        """
        sprite_copy = pygame.transform.scale(self.sprite, (self.sprite.get_width() * self.size_factor, self.sprite.get_height() * self.size_factor))
        sprite_copy = pygame.transform.rotate(sprite_copy, self.rotation)
        new_rect = sprite_copy.get_rect(center=self.position) # get a new standardized collision rect so the explosion sprite doesn't drift since its size will be random.
        surface.blit(sprite_copy, new_rect)