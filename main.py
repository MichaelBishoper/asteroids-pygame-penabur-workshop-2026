# External Libs
from sys import exit
import pygame
from pygame.math import Vector2

# Local Modules/Classes
from settings import SCALED_HEIGHT, SCALED_WIDTH, HEIGHT, WIDTH, FPS, IMAGES_DIR, MUSIC_DIR, SFX_DIR, FONTS_DIR, LASER_BUFFER, ASTEROID_SPEED, ASTEROID_SPAWN_BUFFER, FONT_SIZE
from utils import get_random_rotation, get_random_asteroid_position, get_random_asteroid_speed, is_laser_off_screen, is_asteroid_off_screen, get_random_explosion_size, get_random_score
from player import Player
from laser import Laser
from asteroid import Asteroid
from explosion import Explosion
from ui import UI, TextUI

pygame.init()
pygame.mixer.init()

# pygame variables
clock = pygame.time.Clock()

# load sfx
sfx_laser = pygame.mixer.Sound(str(SFX_DIR / 'asteroids_laser.wav'))
sfx_destroy = pygame.mixer.Sound(str(SFX_DIR / 'sfx_asteroid_destroyed.wav'))
# set sfx volumes
sfx_laser.set_volume(0.2)
sfx_destroy.set_volume(0.8)

# load sprites
background: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'background_stars.png'))
icon: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'icon.png'))
four_health: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'health1.png'))
three_health: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'health2.png'))
two_health: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'health3.png'))
one_health: pygame.Surface = pygame.image.load(str(IMAGES_DIR / 'health4.png'))
no_health: pygame.Surface =  pygame.image.load(str(IMAGES_DIR / 'health5.png'))

# load fonts
game_font: pygame.font.Font = pygame.font.Font(str(FONTS_DIR / 'W95F.otf'), FONT_SIZE)
    
# the size of the background sprite is 100px x 100px
# all drawing logic is written on the game_screen surface NOT on screen
game_screen: pygame.Surface = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((SCALED_WIDTH, SCALED_HEIGHT), pygame.SCALED)

# customize game window
pygame.display.set_caption('Asteroids')
pygame.display.set_icon(icon)

# initialize game objects 
# y increases going upwards, hence lower ratio (1.25)
player = Player(pygame.Vector2(WIDTH/2, HEIGHT/1.25)) 
health_bar = UI(four_health, Vector2(10, 10), 5.0)

# DO NOT TOUCH
# object arrays
lasers: list[Laser] = []
asteroids: list[Asteroid] = []
explosions: list[Explosion] = []

# DO NOT TOUCH
# counters
laser_buffer_counter: float = 0.0
asteroid_buffer_counter: float = 0.0

#####################
# --- GAME LOOP --- #
#####################

while True:
    game_screen.blit(background, (0, 0))
    
    # clock.tick() returns milliseconds
    # for dt math I convert it to seconds
    dt = clock.tick(FPS)/1000
    
    match player.health:
        case 4:
            health_bar.sprite = four_health
        case 3:
            health_bar.sprite = three_health
        case 2:
            health_bar.sprite = two_health
        case 1:
            health_bar.sprite = one_health
        case 0: 
            health_bar.sprite = no_health
            exit() # you suck!!!
        case _:
            health_bar.sprite = no_health
    
    ##################################
    # -- Spawn Lasers/Obstacles -- #
    ##################################
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() # exit the program deliberately so it doesn't return a crash error
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x and laser_buffer_counter == 0:
            sfx_laser.play()
            lasers.append(Laser(Vector2(player.position.x, player.position.y - 15)))
            laser_buffer_counter = LASER_BUFFER # fill back the counter after a laser is fired
    
    if asteroid_buffer_counter == 0:
        asteroids.append(Asteroid(get_random_asteroid_position(), get_random_rotation(), get_random_asteroid_speed()))
        asteroid_buffer_counter = ASTEROID_SPAWN_BUFFER # fill the counter after an asteroid is spawned
    
    ##########################
    # -- Position Updates -- #
    ##########################
    
    # the order of objects don't matter
    player.update(dt)
    for l in lasers: l.update(dt)
    for a in asteroids: a.update(dt)
    for e in explosions: e.update(dt)
    
    #####################################
    # -- Object Collisions + Removal -- #
    #####################################
    
    # object to be removed arrays
    # objects which collide 
    lasers_to_remove: list[Laser] = []
    asteroids_to_remove: list[Asteroid] = []
    explosions_to_remove: list[Explosion] = []
    
    # detect laser and asteroid collisions
    for l in lasers:
        for a in asteroids:
            if l.rect.colliderect(a.rect):
                if l.position.y > 0 and a.position.y > 0:
                    # -- collision -- #
                    sfx_destroy.play()
                    player.score += get_random_score()
                    # -- spawn an explosion object -- #
                    # NOTE: explosion timer logic is inside its class
                    explosions.append(Explosion(l.position, get_random_rotation(), get_random_explosion_size()))
                    lasers_to_remove.append(l)
                    asteroids_to_remove.append(a)
                    break
    
    # detect player and asteroid collisions
    for a in asteroids:
        if a.rect.colliderect(player.rect):
                # -- collision -- #
                asteroids_to_remove.append(a)
                player.take_damage()
                break

    # append dead collisions
    for e in explosions:
            if not e.alive:
                explosions_to_remove.append(e)
    
    # comparisons to sets are algorithmically faster than direct array value comparison
    lasers_to_remove_set = set(lasers_to_remove)
    asteroids_to_remove_set = set(asteroids_to_remove)
    explosions_to_remove_set = set(explosions_to_remove)
    
    # Destroy Collided Objects + Explosions
    lasers = [l for l in lasers if l not in lasers_to_remove_set]
    asteroids = [a for a in asteroids if a not in asteroids_to_remove_set]
    explosions = [e for e in explosions if e not in explosions_to_remove_set]
    
    # lasers which above the viewport die
    # asteroids which are below the viewport die
    lasers = [l for l in lasers if not is_laser_off_screen(l.position)]
    asteroids = [a for a in asteroids if not is_asteroid_off_screen(a.position)]
    
    #################
    # -- Drawing -- #
    #################
    
    # order matters, last call is drawn on top of the canvas.
    for l in lasers: l.draw(game_screen) 
    for a in asteroids: a.draw(game_screen)
    player.draw(game_screen)
    for e in explosions: e.draw(game_screen)
    

    # scale the 100px x 100px logical game_screen to a 1000px x 1000px viewport
    pygame.transform.scale(game_screen, (SCALED_WIDTH, SCALED_HEIGHT), screen)
    health_bar.draw(screen)
    score_text = TextUI(Vector2(SCALED_WIDTH/1.55, 10), f"Score: {player.score}", (255, 255, 255), game_font)
    score_text.draw(screen)
    
    # update counters after the frame is about to end
    laser_buffer_counter = max(0, laser_buffer_counter - dt)
    asteroid_buffer_counter = max(0, asteroid_buffer_counter - dt)
    
    pygame.display.update()