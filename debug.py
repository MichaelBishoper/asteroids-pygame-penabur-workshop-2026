import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
print("surface:", screen.get_size())
print("window:", pygame.display.get_window_size())
screen.fill((255, 0, 0))
pygame.display.flip()
input("press enter to quit")