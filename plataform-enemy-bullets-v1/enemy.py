import pygame
from projectile import Projectile


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cooldown = 60
        self.timer = 0
        self.projectiles = pygame.sprite.Group()

    def update(self):
        self.timer += 1
        if self.timer >= self.cooldown:
            self.shoot()
            self.timer = 0

    def shoot(self):
        bullet = Projectile(self.rect.centerx, self.rect.centery, -1)
        self.projectiles.add(bullet)
