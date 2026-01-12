import pygame

from projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.projectiles = pygame.sprite.Group()

    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Projectile(self.rect.centerx, self.rect.centery, 1)
        self.projectiles.add(bullet)
