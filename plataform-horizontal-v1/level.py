import pygame
from player import Player
from enemy import Enemy

TILE = 32

# 1 = bloco, 0 = vazio
MAPA = [
    "000000000000000000",
    "000000000000000000",
    "000000000000000000",
    "000000000000000000",
    "000000010000000100",
    "000000000000000100",
    "11111111100111111101111111",
]

class Level:
    def __init__(self):
        self.tiles = []
        self.enemies = []
        self.player = Player(100, 100, self)
        self.camera_x = 0


        # cria blocos
        for y, row in enumerate(MAPA):
            for x, col in enumerate(row):
                if col == "1":
                    rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)
                    self.tiles.append(rect)

        # cria inimigo
        self.enemies.append(Enemy(400, 150, self))

    def update(self, dt):
        self.player.update(dt)
        # câmera segue o player
        self.camera_x = self.player.rect.centerx - 400  # 400 = metade da tela

        for e in self.enemies:
            e.update(dt)

        # colisão com inimigos
        for e in self.enemies:
            if self.player.rect.colliderect(e.rect):
                print("GAME OVER")
                pygame.quit()
                exit()

    def draw(self, win):
        win.fill((135, 206, 235))

        # tiles
        for t in self.tiles:
            pygame.draw.rect(win, (100, 100, 100),
                pygame.Rect(t.x - self.camera_x, t.y, t.width, t.height))

        # inimigos
        for e in self.enemies:
            e.draw(win, self.camera_x)

        # player
        self.player.draw(win, self.camera_x)
