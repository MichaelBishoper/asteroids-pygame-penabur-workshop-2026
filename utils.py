# NOTE: There is a lot of code reuse, escpecially with get_random_asteroid_speed() and get_random_explosion_size(), but the separate names are more readable. Feel free to rewrite it though.

import pygame
import random
import math
from pygame.math import Vector2
from settings import WIDTH, HEIGHT, ASTEROID_SPEED, ASTEROID_SPEED_VARIATION, EXPLOSION_SIZE_VARIATION, EXPLOSION_SCALE, ASTEROID_SPEED_CHANGE_OVER_TIME

def get_random_asteroid_position(screen_offset_x: int = 14, screen_offset_y: int = -30) -> Vector2:
    """
        Returns a Vector2 between (10, -30) and (10, -30)
    """
    rand_x = random.randint(screen_offset_x, WIDTH - screen_offset_x)
    return Vector2(rand_x, screen_offset_y)

def get_random_rotation() -> int:
    """
        Returns an int between 0 and 360
    """
    rand_rot: int = random.randint(0, 360)
    return rand_rot

def get_random_asteroid_speed(asteroid_speed: int = ASTEROID_SPEED) -> int:
    """
        Returns a variable int between -ASTEROID_SPEED_VARIATION% and ASTEROID_SPEED_VARIATION% of ASTEROID_SPEED
    """
    rand_sign: int = 0
    negative: bool = bool(random.getrandbits(1))
    if negative:
        rand_sign = -1
    else:
        rand_sign = 1
    
    rand_percent: float = (100 + (rand_sign * random.randint(0, ASTEROID_SPEED_VARIATION)))/100
    
    rand_speed: int = int(asteroid_speed * rand_percent)
    print("asteroid speed global: ", asteroid_speed)
    print(rand_speed)
    return rand_speed

def is_laser_off_screen(position: Vector2, offset: int = 10) -> bool:
    """
        Returns True if a Vector2 is outside screen boundaries +- offsets
        
        Args:
            Position - The Vector2 that is to be checked
    """
    if position.y < 0 - offset:
        return True
    else: 
        return False
    
def is_asteroid_off_screen(position: Vector2, offset: int = 20) -> bool:
    """
        Returns True if a Vector2 is outside screen boundaries +- offsets
        
        Args:
            Position - The Vector2 that is to be checked
    """
    if position.y > HEIGHT + offset:
        return True
    else: 
        return False
    
def get_random_explosion_size() -> float:
    """
        Returns a random float varying from EXPLOSION_SIZE_VARIATION
    """
    rand_sign: int = 0
    negative: bool = bool(random.getrandbits(1))
    if negative:
        rand_sign = -1
    else:
        rand_sign = 1
    
    rand_percent: float = (100 + (rand_sign * random.randint(0, EXPLOSION_SIZE_VARIATION)))/100
    
    rand_size: float = rand_percent * EXPLOSION_SCALE
    return rand_size

def get_random_score() -> int:
    """
        Returns a random float varying from 1000
    """
    rand_modifier = random.uniform(0.8, 1.2)
    rand_score = rand_modifier * 1000
    return int(rand_score)

def get_asteroid_speed(aasteroids_destroyed: int, a: int = 35) -> int:
    return int(a*math.pow(ASTEROID_SPEED_CHANGE_OVER_TIME, aasteroids_destroyed))