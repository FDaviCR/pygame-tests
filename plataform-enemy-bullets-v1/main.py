import pygame
from player import Player
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = Player(100, 500)
enemy = Enemy(600, 500)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    keys = pygame.key.get_pressed()
    player.update(keys)
    enemy.update()

    player.projectiles.update()
    enemy.projectiles.update()

    screen.fill((30, 30, 30))
    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)

    player.projectiles.draw(screen)
    enemy.projectiles.draw(screen)

    pygame.display.flip()

pygame.quit()
