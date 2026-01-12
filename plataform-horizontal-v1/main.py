import pygame
from level import Level

pygame.init()

WIDTH, HEIGHT = 800, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()
FPS = 60

level = Level()

run = True
while run:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    level.update(dt)
    level.draw(WIN)

    pygame.display.update()

pygame.quit()
