from sys import exit
from settings import SCALED_HEIGHT, SCALED_WIDTH, HEIGHT, WIDTH, FPS, IMAGES_DIR, MUSIC_DIR, SFX_DIR
from player import Player
import pygame

pygame.init()
game_screen: pygame.Surface = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((SCALED_WIDTH, SCALED_HEIGHT), pygame.SCALED)
print(screen.get_size())
pygame.display.set_caption('Asteroids')
clock = pygame.time.Clock()
player = Player(pygame.Vector2(WIDTH/2, HEIGHT/1.25)) 
background = pygame.image.load(str(IMAGES_DIR / 'background_stars.png'))

while True:
    game_screen.blit(background, (0, 0))
    
    dt = clock.tick(60) / 1000
    player.update(dt)
    player.draw(game_screen)

    pygame.transform.scale(game_screen, (SCALED_WIDTH, SCALED_HEIGHT), screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    pygame.display.update()
    