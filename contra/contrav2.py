import pygame
import sys
import random

pygame.init()

# =============================
# CONFIGURAÇÕES DE TELA
# =============================
LARGURA = 960
ALTURA = 540
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Contra - Protótipo")

FPS = 60
clock = pygame.time.Clock()

# =============================
# CORES (Protótipo)
# =============================
AZUL = (50, 150, 255)
VERMELHO = (255, 70, 70)
AMARELO = (255, 255, 0)
VERDE = (60, 200, 60)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (70, 70, 70)

# =============================
# PARAMETROS DE JOGO
# =============================
GRAVIDADE = 0.8
MAPA_LARGURA = 4000
CHAO_Y = ALTURA - 80

# =============================
# CLASSES
# =============================
class Player:
    def __init__(self):
        self.x = 100
        self.y = CHAO_Y - 48
        self.larg = 32
        self.alt = 48
        self.vel = 5
        self.dy = 0
        self.pulando = False
        self.abaixado = False
        self.atirando = False
        self.vida = 3
        self.cooldown = 0

    def input(self, teclas):
        self.atirando = False
        self.abaixado = False

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.x -= self.vel
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.x += self.vel

        if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and not self.pulando:
            self.pulando = True
            self.dy = -15

        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self.abaixado = True

        if teclas[pygame.K_SPACE]:
            self.atirando = True

    def update(self):
        self.dy += GRAVIDADE
        self.y += self.dy

        if self.y + self.alt >= CHAO_Y:
            self.y = CHAO_Y - self.alt
            self.pulando = False
            self.dy = 0

        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, camera_x):
        if self.abaixado:
            pygame.draw.rect(TELA, AZUL, (self.x - camera_x, self.y + 24, 32, 24))
        else:
            pygame.draw.rect(TELA, AZUL, (self.x - camera_x, self.y, 32, 48))


class Inimigo:
    def __init__(self, x):
        self.x = x
        self.y = CHAO_Y - 48
        self.larg = 32
        self.alt = 48
        self.vel = 2
        self.direita = True
        self.cooldown = random.randint(40, 140)

    def update(self):
        if self.direita:
            self.x += self.vel
            if random.random() < 0.01:
                self.direita = False
        else:
            self.x -= self.vel
            if random.random() < 0.01:
                self.direita = True

        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, camera_x):
        pygame.draw.rect(TELA, VERMELHO, (self.x - camera_x, self.y, 32, 48))


class Tiro:
    def __init__(self, x, y, dir, inimigo=False):
        self.x = x
        self.y = y
        self.dir = dir
        self.vel = 8 if not inimigo else 6
        self.inimigo = inimigo

    def update(self):
        self.x += self.vel * self.dir

    def draw(self, camera_x):
        pygame.draw.rect(TELA, AMARELO, (self.x - camera_x, self.y, 10, 4))


# =============================
# OBJETOS
# =============================
player = Player()
inimigos = [Inimigo(700 + i * 400) for i in range(6)]
tiros = []

camera_x = 0
estado = "menu"
fonte = pygame.font.SysFont(None, 40)

# =============================
# LOOP PRINCIPAL
# =============================
rodando = True
while rodando:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if estado == "menu":
                if event.key == pygame.K_RETURN:
                    estado = "jogo"

            elif estado == "jogo":
                if event.key == pygame.K_ESCAPE:
                    estado = "pausa"

            elif estado == "pausa":
                if event.key == pygame.K_ESCAPE:
                    estado = "jogo"

    if estado == "menu":
        TELA.fill(PRETO)
        TELA.blit(fonte.render("CONTRA PROTÓTIPO", True, BRANCO), (300, 200))
        TELA.blit(fonte.render("ENTER para iniciar", True, CINZA), (330, 260))
        pygame.display.update()
        continue

    if estado == "pausa":
        TELA.fill(PRETO)
        TELA.blit(fonte.render("PAUSADO", True, BRANCO), (420, 240))
        TELA.blit(fonte.render("ESC para voltar", True, CINZA), (380, 280))
        pygame.display.update()
        continue

    # =============================
    # LÓGICA DO JOGO
    # =============================
    teclas = pygame.key.get_pressed()
    player.input(teclas)
    player.update()

    # atirar player
    if player.atirando and player.cooldown == 0:
        if player.abaixado:
            tiros.append(Tiro(player.x + 32, player.y + 32, +1))
        else:
            tiros.append(Tiro(player.x + 32, player.y + 16, +1))
        player.cooldown = 12

    for inimigo in inimigos:
        inimigo.update()
        if inimigo.cooldown == 0:
            tiros.append(Tiro(inimigo.x, inimigo.y + 26, -1, inimigo=True))
            inimigo.cooldown = random.randint(60, 140)

    # atualizar tiros
    for t in tiros[:]:
        t.update()

        if t.x < 0 or t.x > MAPA_LARGURA:
            tiros.remove(t)
            continue

        # colisão tiro inimigo com player
        if t.inimigo:
            if not player.abaixado:
                if (player.x < t.x < player.x + player.larg and
                        player.y < t.y < player.y + player.alt):
                    player.vida -= 1
                    tiros.remove(t)
                    continue

        # colisão tiro do player com inimigo
        else:
            for inimigo in inimigos[:]:
                if (inimigo.x < t.x < inimigo.x + inimigo.larg and
                        inimigo.y < t.y < inimigo.y + inimigo.alt):
                    inimigos.remove(inimigo)
                    tiros.remove(t)
                    break

    # =============================
    # CÂMERA
    # =============================
    camera_x = player.x - 200
    if camera_x < 0:
        camera_x = 0
    if camera_x > MAPA_LARGURA - LARGURA:
        camera_x = MAPA_LARGURA - LARGURA

    # =============================
    # FINAL DA FASE
    # =============================
    if player.x > MAPA_LARGURA - 120:
        estado = "fim"

    if player.vida <= 0:
        estado = "gameover"

    # =============================
    # RENDERIZAÇÃO
    # =============================
    TELA.fill((40, 40, 40))

    pygame.draw.rect(TELA, VERDE, (0 - camera_x, CHAO_Y, MAPA_LARGURA, 80))

    player.draw(camera_x)

    for inimigo in inimigos:
        inimigo.draw(camera_x)

    for t in tiros:
        t.draw(camera_x)

    pygame.display.update()

    # =============================
    # TELA FINAL
    # =============================
    if estado == "fim":
        TELA.fill(PRETO)
        TELA.blit(fonte.render("VITÓRIA!", True, BRANCO), (420, 240))
        pygame.display.update()
        pygame.time.wait(2000)
        break

    if estado == "gameover":
        TELA.fill(PRETO)
        TELA.blit(fonte.render("GAME OVER", True, BRANCO), (420, 240))
        pygame.display.update()
        pygame.time.wait(2000)
        break

pygame.quit()
sys.exit()

