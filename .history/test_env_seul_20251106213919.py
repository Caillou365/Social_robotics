import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Test Pygame")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Fond blanc
    pygame.draw.rect(screen, (0, 0, 0), (250, 250, 100, 100))  # Carré noir
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
