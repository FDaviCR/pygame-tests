import pygame

class Enemy:
    def __init__(self, x, y, level):
        self.level = level
        self.rect = pygame.Rect(x, y, 28, 28)
        self.vel = 60

        # descer até encontrar o chão
        self.drop_to_ground()

    def drop_to_ground(self):
        grounded = None
        for tile in self.level.tiles:
            # inimigo está acima do tile?
            if tile.x <= self.rect.centerx <= tile.right and tile.top >= self.rect.bottom:
                if grounded is None or tile.top < grounded:
                    grounded = tile.top

        if grounded is not None:
            self.rect.bottom = grounded

    def update(self, dt):
        self.rect.x += self.vel * dt

        for tile in self.level.tiles:
            if self.rect.colliderect(tile):
                self.vel *= -1  # troca direção

    def draw(self, win, cam_x):
        pygame.draw.rect(win, (50, 50, 255),
        pygame.Rect(self.rect.x - cam_x, self.rect.y, self.rect.width, self.rect.height))

