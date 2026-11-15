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
        self.alive: bool = True
    
    def update(self, dt: float):
        self.timer = self.timer + dt
        
        # for main.py to know if an explosion should die
        if self.timer >= self.time:
            self.alive = False
    
    def draw(self, surface: pygame.Surface):
        sprite_copy = pygame.transform.scale(self.sprite, (self.sprite.get_width() * self.size_factor, self.sprite.get_height() * self.size_factor))
        sprite_copy = pygame.transform.rotate(sprite_copy, self.rotation)
        new_rect = sprite_copy.get_rect(center=self.position)
        surface.blit(sprite_copy, new_rect)
    