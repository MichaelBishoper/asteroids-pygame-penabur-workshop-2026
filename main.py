# External Libs
from sys import exit
import pygame
from pygame.math import Vector2

# Local Modules/Classes
from settings import SCALED_HEIGHT, SCALED_WIDTH, HEIGHT, WIDTH, FPS, IMAGES_DIR, MUSIC_DIR, SFX_DIR, FONTS_DIR, LASER_BUFFER, asteroid_speed, asteroid_spawn_buffer, FONT_SIZE
from utils import get_random_rotation, get_random_asteroid_position, get_random_asteroid_speed, is_laser_off_screen, is_asteroid_off_screen, get_random_explosion_size, get_random_score, get_asteroid_speed
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
sfx_destroy = pygame.mixer.Sound(str(SFX_DIR / 'sfx_asteroid_destroyed_2.wav'))
sfx_hit = pygame.mixer.Sound(str(SFX_DIR / 'sfx_player_hit.wav'))

# load and play music
music = pygame.mixer.music.load(str(MUSIC_DIR / 'main_music.ogg'))
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)

# set sfx volumes
sfx_laser.set_volume(0.15)
sfx_destroy.set_volume(0.71)
sfx_hit.set_volume(0.8)

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
final_score_font: pygame.font.Font = pygame.font.Font(str(FONTS_DIR / 'W95F.otf'), 100)
    
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

asteroids_destroyed: int = 0
asteroid_counter: int = 0

# DO NOT TOUCH
# counters
laser_buffer_counter: float = 0.0
asteroid_buffer_counter: float = 0.0


#####################
# --- GAME LOOP --- #
#####################

# to change between the playing logic and game_over logic
game_state: str = "play"

while True:
    game_screen.blit(background, (0, 0))
    
    # clock.tick() returns milliseconds
    # for deltatime math convert it to seconds
    dt = clock.tick(FPS)/1000
    
    if game_state == "play":
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
                game_state = "game_over"
            case _:
                health_bar.sprite = no_health
        
        # recalculate base asteroid speed based on number of asteroids destroyed already
        asteroid_speed = get_asteroid_speed(asteroids_destroyed)
        
        # decreases the rate of spawn of asteroids every 5 asteroids destroyed
        if asteroid_counter == 5:
            next_spawn_buffer = max(0.45, asteroid_spawn_buffer - 0.2)
            asteroid_spawn_buffer = next_spawn_buffer
            asteroid_counter = 0
        
        ##################################
        # -- Spawn Lasers/Obstacles -- #
        ##################################
        
        # spawn lasers and handle quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() # exit the program deliberately so it doesn't return a crash error
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x and laser_buffer_counter == 0:
                sfx_laser.play()
                lasers.append(Laser(Vector2(player.position.x, player.position.y - 15)))
                laser_buffer_counter = LASER_BUFFER # fill back the counter after a laser is fired
        
        # spawn asteroids
        if asteroid_buffer_counter == 0:
            asteroids.append(Asteroid(get_random_asteroid_position(), get_random_rotation(), get_random_asteroid_speed(asteroid_speed)))
            asteroid_buffer_counter = asteroid_spawn_buffer # fill the counter after an asteroid is spawned
        
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
                        
                        asteroids_destroyed += 1
                        asteroid_counter += 1
                        
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
                    sfx_hit.play()
                    
                    asteroids_destroyed += 1
                    asteroid_counter += 1
                    
                    asteroids_to_remove.append(a)
                    player.take_damage()          
                    break

        # append dead explosions to be removed
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
        
        # order matters, last call is drawn on top of the canvas
        if game_state != "game_over":
            for l in lasers: l.draw(game_screen) 
            for a in asteroids: a.draw(game_screen)
            player.draw(game_screen)
            for e in explosions: e.draw(game_screen)

        # scale the 100px x 100px logical game_screen to a 1000px x 1000px viewport
        pygame.transform.scale(game_screen, (SCALED_WIDTH, SCALED_HEIGHT), screen)
        
        # UI is drawn on the scaled screen and not the game screen
        if game_state != "game_over":
            health_bar.draw(screen)
            score_text = TextUI(Vector2(SCALED_WIDTH/1.23, 55), f"Score: {player.score}", (255, 255, 255), game_font)
            score_text.draw(screen)
        
        # update counters after the frame is about to end
        laser_buffer_counter = max(0, laser_buffer_counter - dt)
        asteroid_buffer_counter = max(0, asteroid_buffer_counter - dt)
        
    if game_state == "game_over":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                player.reset()
                
                # holy readability
                asteroid_spawn_buffer = 2.5
                asteroid_speed = 35
                asteroids_destroyed = 0
                asteroid_counter = 0
                asteroids = []
                lasers = []
                explosions = []
                game_state = "play"
        
        # draw UI on the scaled screen and not the game screen
        # NOTE: asteroids_destroyed - 4 because asteroid ship collisions also count
        score_text = TextUI(Vector2(SCALED_WIDTH/2.0, SCALED_HEIGHT/3), f"Score: {player.score}", (255, 255, 255), final_score_font)
        score_text.draw(screen)
        stats_text = TextUI(Vector2(SCALED_WIDTH/2.0, SCALED_HEIGHT/2.3), f"Asteroids Destroyed: {asteroids_destroyed - 4}", (255, 255, 255), game_font)
        stats_text.draw(screen)
        retry_text = TextUI(Vector2(SCALED_WIDTH/2.0, SCALED_HEIGHT/1.96), "Press [R] to Retry", (255, 255, 255), game_font)
        retry_text.draw(screen)
        if (asteroids_destroyed - 4) == 0:
            shame_text = TextUI(Vector2(SCALED_WIDTH/2.0, SCALED_HEIGHT/1.25), "Wow! You suck.", (255, 255, 255), game_font)
            shame_text.draw(screen)
    
    pygame.display.update()