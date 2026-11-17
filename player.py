import pygame
from pygame.math import Vector2
from settings import PLAYER_SPEED, IMAGES_DIR, DAMAGE_COOLDOWN, WIDTH, HEIGHT

class Player:
    def __init__(self, position: Vector2):
        self.position: Vector2 = Vector2(position)
        self.health: int = 4
        self.score: int = 0
        self.default_sprite: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'ship_1.png'))
        self.hurt_sprite: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'ship_hit_white_var.png'))
        self.current_sprite: pygame.Surface = self.default_sprite
        self.rect: pygame.Rect = self.current_sprite.get_rect(center = self.position)
        self.rect.topleft = self.position
        self.damage_cooldown: float = 0.0
    
    @property
    def score(self) -> int:
        return self._score
    
    @score.setter
    def score(self, value: int):
        self._score = max(0, min(99999, value))

    def update(self, dt: float):
        """Update the player's position based on input and deltatime.
S
        Args:
            dt (float): The time elapsed since the last frame, in seconds (converted and defined in the main loop).
        """
        if self.damage_cooldown > 0.0:
            self.damage_cooldown = max(self.damage_cooldown - dt, 0.0)
            if self.damage_cooldown == 0.0:
                # -- damage_cooldown just turned 0 -- #
                self.current_sprite = self.default_sprite
        
        # returns a list of all keys currently pressed this frame
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.health > 0:
            next_position = self.position.x - PLAYER_SPEED * dt
            self.position.x = max(next_position, 16)
            
        if keys[pygame.K_RIGHT] and self.health > 0:
            next_position = self.position.x + PLAYER_SPEED * dt
            self.position.x = min(next_position, 83)
        
        self.rect.center = self.position
    
    def draw(self, surface: pygame.Surface):
        """Draws the player's current position.

        Args:
            surface (pygame.Surface): The surface to draw the player sprite on (defined in the main loop).
        """
        surface.blit(self.current_sprite, self.rect)
        
        ##########################
        # debug: show collisions #
        ##########################
        
        # pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)
    
    def take_damage(self):
        """Decreases the player health by 1, changes the sprite to the hurt sprite and fills the damage_cooldown timer. 
        """
        if self.damage_cooldown == 0.0: 
            next_health: int = self.health - 1
            self.health = max(next_health, 0)
            self.current_sprite = self.hurt_sprite
            self.damage_cooldown = DAMAGE_COOLDOWN
            
    def reset(self):
        """Resets the player's state to its starting state
        """
        self.health = 4
        self.score = 0
        self.position = Vector2(WIDTH/2, HEIGHT/1.25)