# External Libs
from sys import exit
import pygame
from pygame.math import Vector2

# Local Modules/Classes
from settings import SCALED_HEIGHT, SCALED_WIDTH, HEIGHT, WIDTH, FPS, IMAGES_DIR, MUSIC_DIR, SFX_DIR, LASER_BUFFER, ASTEROID_SPEED, ASTEROID_SPAWN_BUFFER
from utils import get_random_asteroid_rotation, get_random_asteroid_position, get_random_speed, is_laser_off_screen, is_asteroid_off_screen, get_random_explosion_size
from player import Player
from laser import Laser
from asteroid import Asteroid
from explosion import Explosion


pygame.init()
pygame.mixer.init()

# SFX
sfx_laser = pygame.mixer.Sound(str(SFX_DIR / 'asteroids_laser.wav'))
sfx_laser.set_volume(0.2)

game_screen: pygame.Surface = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((SCALED_WIDTH, SCALED_HEIGHT), pygame.SCALED)
pygame.display.set_caption('Asteroids')
clock = pygame.time.Clock()

player = Player(pygame.Vector2(WIDTH/2, HEIGHT/1.25)) 
background = pygame.image.load(str(IMAGES_DIR / 'background_stars.png'))

lasers: list[Laser] = []
asteroids: list[Asteroid] = []
explosions: list[Explosion] = []

laser_buffer_counter: float = 0.0
asteroid_buffer_counter: float = 0.0

while True:
    game_screen.blit(background, (0, 0))
    
    # get deltatime
    dt = clock.tick(FPS)/1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x and laser_buffer_counter == 0:
            sfx_laser.play()
            lasers.append(Laser(Vector2(player.position.x, player.position.y - 15)))
            laser_buffer_counter = LASER_BUFFER
    
    # -- Updates -- #
    player.update(dt)
    for l in lasers: l.update(dt)
    for a in asteroids: a.update(dt)
    for e in explosions: e.update(dt)
    
    # -- Collisions -- #
    lasers_to_remove: list[Laser] = []
    asteroids_to_remove: list[Asteroid] = []
    explosions_to_remove: list[Explosion] = []
    
    for l in lasers:
        for a in asteroids:
            if l.rect.colliderect(a.rect):
                if l.position.y > 0 and a.position.y > 0:
                    # laser and asteroid collides
                    explosions.append(Explosion(l.position, get_random_asteroid_rotation(), get_random_explosion_size()))
                    lasers_to_remove.append(l)
                    asteroids_to_remove.append(a)
                    break
    
    for a in asteroids:
        if a.rect.colliderect(player.rect):
                # player and asteroid collides
                asteroids_to_remove.append(a)
                player.take_damage()
                break
            
    for e in explosions:
            if not e.alive:
                explosions_to_remove.append(e)
    
    # Destroy Collided Objects + Explosions
    lasers_to_remove_set = set(lasers_to_remove)
    asteroids_to_remove_set = set(asteroids_to_remove)
    explosions_to_remove_set = set(explosions_to_remove)
    
    lasers = [l for l in lasers if l not in lasers_to_remove_set]
    asteroids = [a for a in asteroids if a not in asteroids_to_remove_set]
    explosions = [e for e in explosions if e not in explosions_to_remove_set]
    
    # Destroy Outside Objects
    lasers = [l for l in lasers if not is_laser_off_screen(l.position)]
    asteroids = [a for a in asteroids if not is_asteroid_off_screen(a.position)]
    
    
    # -- Drawing -- #
    # NOTE: Order matters! Last call is drawn on top of the canvas.
    for l in lasers: l.draw(game_screen) 
    for a in asteroids: a.draw(game_screen)
    player.draw(game_screen)
    for e in explosions: e.draw(game_screen)

    pygame.transform.scale(game_screen, (SCALED_WIDTH, SCALED_HEIGHT), screen)
    
    laser_buffer_counter = max(0, laser_buffer_counter - dt)
    asteroid_buffer_counter = max(0, asteroid_buffer_counter - dt)
    
    if asteroid_buffer_counter == 0:
        asteroids.append(Asteroid(get_random_asteroid_position(), get_random_asteroid_rotation(), get_random_speed()))
        asteroid_buffer_counter = ASTEROID_SPAWN_BUFFER
    
    pygame.display.update()