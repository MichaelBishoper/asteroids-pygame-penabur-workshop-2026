import pygame
from pygame.math import Vector2
from settings import PLAYER_SPEED, IMAGES_DIR, WIDTH, HEIGHT

class Player:
    def __init__(self, position: Vector2):
        self.position: Vector2 = Vector2(position)
        self.velocity: Vector2 = pygame.Vector2(0, 0)
        self.angle: float = 0.0
        self.health: int = 4
        self.max_health: int = 4
        self.sprite: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'ship_1.png'))
        self.rect: pygame.Rect = self.sprite.get_rect(center = self.position)
        self.rect.topleft = self.position

    def update(self, dt: float):
        """Update the player's position based on input and deltatime.

        Args:
            dt (float): The time elapsed since the last frame, in seconds (converted and defined in the main loop).
        """
        
        # DEBUG
        print(self.position)
        
        # returns a list of all keys currently pressed this frame
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            next_position = self.position.x - PLAYER_SPEED * dt
            self.position.x = max(next_position, 16)
            
            print("left")
        if keys[pygame.K_RIGHT]:
            next_position = self.position.x + PLAYER_SPEED * dt
            self.position.x = min(next_position, 83)
            print("right")
        
        self.rect.center = self.position
    
    def draw(self, surface: pygame.Surface):
        """Draws the player's current position.

        Args:
            surface (pygame.Surface): The surface to draw the player sprite on (defined in the main loop).
        """
        surface.blit(self.sprite, self.rect)
        
        # DEBUG
        # draws collision shape
        # pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)