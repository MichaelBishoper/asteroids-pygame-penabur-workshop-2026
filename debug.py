# DEBUG SCRIPT FOR SCALING ERRORS
import pygame
from settings import SCALED_WIDTH, SCALED_HEIGHT
pygame.init()
screen = pygame.display.set_mode((SCALED_WIDTH, SCALED_HEIGHT))
print("surface:", screen.get_size())
print("window:", pygame.display.get_window_size())
# Fills screen with red
screen.fill((255, 0, 0))
pygame.display.flip()