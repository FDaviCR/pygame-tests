import pygame
import sys

pygame.init()

LARGURA = 1000
ALTURA = 600
TAMANHO = 40

tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()

mapa = [
    "############################",
    "#..........................#",
    "#..............E...........#",
    "#.....#####................#",
    "#..P...E...................#",
    "############################",
]

WORLD_WIDTH = len(mapa[0]) * TAMANHO
WORLD_HEIGHT = len(mapa) * TAMANHO

# -------------------------------------

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TAMANHO, TAMANHO))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.vel_y = 0
        self.vel_x = 0

    def update(self, plataformas):
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x = -5
        if keys[pygame.K_RIGHT]:
            self.vel_x = 5
        if keys[pygame.K_SPACE] and self.vel_y == 0:
            self.vel_y = -15

        # ---- MOVE X ----
        self.rect.x += self.vel_x
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right

        # ---- MOVE Y ----
        self.vel_y += 1
        self.rect.y += self.vel_y

        for p in plataformas:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

        # Limites mundo
        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, WORLD_HEIGHT - self.rect.height))

# -------------------------------------

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TAMANHO, TAMANHO))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.vel_y = 0
        self.direcao = 1

    def update(self, plataformas):
        # Move X
        self.rect.x += self.direcao * 2

        # Colisão lateral
        colidiu = False
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                colidiu = True
                if self.direcao > 0:
                    self.rect.right = p.rect.left
                else:
                    self.rect.left = p.rect.right

        if colidiu:
            self.direcao *= -1

        # Gravidade
        self.vel_y += 1
        self.rect.y += self.vel_y

        # Chão
        no_chao = True
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                no_chao = False
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                self.vel_y = 0

        # Se sair da plataforma → vira
        if no_chao:
            self.direcao *= -1

# -------------------------------------

class Bloco(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TAMANHO, TAMANHO))
        self.image.fill((120,120,120))
        self.rect = self.image.get_rect(topleft=(x,y))

# -------------------------------------

plataformas = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
todos = pygame.sprite.Group()

for y, linha in enumerate(mapa):
    for x, char in enumerate(linha):
        px, py = x * TAMANHO, y * TAMANHO
        if char == '#':
            bloco = Bloco(px, py)
            plataformas.add(bloco)
            todos.add(bloco)
        elif char == 'P':
            jogador = Jogador(px, py)
            todos.add(jogador)
        elif char == 'E':
            inimigo = Inimigo(px, py)
            inimigos.add(inimigo)
            todos.add(inimigo)

camera_x = 0

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    jogador.update(plataformas)
    inimigos.update(plataformas)

    camera_x = -jogador.rect.x + LARGURA//2
    camera_x = min(0, max(camera_x, LARGURA - WORLD_WIDTH))

    tela.fill((50,50,100))

    for entidade in todos:
        tela.blit(entidade.image, (entidade.rect.x + camera_x, entidade.rect.y))

    pygame.display.flip()
    clock.tick(60)
