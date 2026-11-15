import pygame
from pygame.math import Vector2
from settings import PLAYER_SPEED, IMAGES_DIR, DAMAGE_COOLDOWN

class Player:
    def __init__(self, position: Vector2):
        self.position: Vector2 = Vector2(position)
        self.health: int = 4
        self.max_health: int = 4
        
        # sprite variables
        self.default_sprite: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'ship_1.png'))
        self.hurt_sprite: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'ship_hit_white_var.png'))
        self.sprite: pygame.Surface = self.default_sprite
        
        self.rect: pygame.Rect = self.sprite.get_rect(center = self.position)
        self.rect.topleft = self.position
        
        # timer variables
        self.damage_cooldown: float = 0.0

    def update(self, dt: float):
        """Update the player's position based on input and deltatime.

        Args:
            dt (float): The time elapsed since the last frame, in seconds (converted and defined in the main loop).
        """
        if self.damage_cooldown > 0.0:
            self.damage_cooldown = max(self.damage_cooldown - dt, 0.0)
            if self.damage_cooldown == 0.0:
                self.sprite = self.default_sprite
        
        # returns a list of all keys currently pressed this frame
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            next_position = self.position.x - PLAYER_SPEED * dt
            self.position.x = max(next_position, 16)
            
        if keys[pygame.K_RIGHT]:
            next_position = self.position.x + PLAYER_SPEED * dt
            self.position.x = min(next_position, 83)
        
        
        self.rect.center = self.position
    
    def draw(self, surface: pygame.Surface):
        """Draws the player's current position.

        Args:
            surface (pygame.Surface): The surface to draw the player sprite on (defined in the main loop).
        """
        surface.blit(self.sprite, self.rect)
        
        # DEBUG
        # pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)
    
    def take_damage(self):
        """Decreases the player health by 1 and changes the sprite to the hurt sprite. The damage_cooldown timer is filled. 
        """
        if self.damage_cooldown == 0.0:
            next_health: int = self.health - 1
            self.health = max(next_health, 0)
            self.sprite = self.hurt_sprite
            self.damage_cooldown = DAMAGE_COOLDOWN