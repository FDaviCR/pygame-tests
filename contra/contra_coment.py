# =============================
# IMPORTAÇÕES
# =============================

# Importa a biblioteca principal do jogo
import pygame

# Usado para encerrar o programa corretamente
import sys

# Usado para comportamentos aleatórios (movimento e tiro dos inimigos)
import random


# =============================
# INICIALIZAÇÃO DO PYGAME
# =============================

# Inicializa todos os módulos do pygame
pygame.init()


# =============================
# CONFIGURAÇÕES DE TELA
# =============================

# Largura da janela do jogo
LARGURA = 960

# Altura da janela do jogo
ALTURA = 540

# Cria a janela do jogo
TELA = pygame.display.set_mode((LARGURA, ALTURA))

# Define o título da janela
pygame.display.set_caption("Contra - Protótipo")

# FPS do jogo (quadros por segundo)
FPS = 60

# Relógio usado para controlar o FPS
clock = pygame.time.Clock()


# =============================
# CORES (RGB)
# =============================

AZUL = (50, 150, 255)       # Player
VERMELHO = (255, 70, 70)    # Inimigos
AMARELO = (255, 255, 0)     # Tiros
VERDE = (60, 200, 60)       # Chão
PRETO = (0, 0, 0)           # Fundo
BRANCO = (255, 255, 255)    # Texto principal
CINZA = (70, 70, 70)        # Texto secundário


# =============================
# PARÂMETROS DO JOGO
# =============================

# Força da gravidade aplicada ao player
GRAVIDADE = 0.8

# Largura total do mapa (maior que a tela)
MAPA_LARGURA = 4000

# Posição vertical do chão
CHAO_Y = ALTURA - 80


# =============================
# CLASSE PLAYER
# =============================
class Player:
    def __init__(self):
        # Posição inicial do player
        self.x = 100
        self.y = CHAO_Y - 48

        # Tamanho do player
        self.larg = 32
        self.alt = 48

        # Velocidade horizontal
        self.vel = 5

        # Velocidade vertical (pulo / queda)
        self.dy = 0

        # Estados do player
        self.pulando = False
        self.abaixado = False
        self.atirando = False

        # Vida do player
        self.vida = 3

        # Cooldown entre tiros
        self.cooldown = 0

    # Lê entradas do teclado
    def input(self, teclas):
        # Reseta estados a cada frame
        self.atirando = False
        self.abaixado = False

        # Movimento para esquerda
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.x -= self.vel

        # Movimento para direita
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.x += self.vel

        # Pulo (apenas se não estiver pulando)
        if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and not self.pulando:
            self.pulando = True
            self.dy = -15

        # Abaixar
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self.abaixado = True

        # Atirar
        if teclas[pygame.K_SPACE]:
            self.atirando = True

    # Atualiza física e estados do player
    def update(self):
        # Aplica gravidade
        self.dy += GRAVIDADE
        self.y += self.dy

        # Verifica colisão com o chão
        if self.y + self.alt >= CHAO_Y:
            self.y = CHAO_Y - self.alt
            self.pulando = False
            self.dy = 0

        # Reduz cooldown do tiro
        if self.cooldown > 0:
            self.cooldown -= 1

    # Desenha o player na tela
    def draw(self, camera_x):
        # Se estiver abaixado, desenha hitbox menor
        if self.abaixado:
            pygame.draw.rect(
                TELA, AZUL,
                (self.x - camera_x, self.y + 24, 32, 24)
            )
        else:
            pygame.draw.rect(
                TELA, AZUL,
                (self.x - camera_x, self.y, 32, 48)
            )


# =============================
# CLASSE INIMIGO
# =============================
class Inimigo:
    def __init__(self, x):
        # Posição inicial
        self.x = x
        self.y = CHAO_Y - 48

        # Tamanho
        self.larg = 32
        self.alt = 48

        # Velocidade de movimento
        self.vel = 2

        # Direção inicial
        self.direita = True

        # Cooldown entre tiros
        self.cooldown = random.randint(40, 140)

    # Atualiza movimentação do inimigo
    def update(self):
        if self.direita:
            self.x += self.vel
            # Chance aleatória de mudar direção
            if random.random() < 0.01:
                self.direita = False
        else:
            self.x -= self.vel
            if random.random() < 0.01:
                self.direita = True

        # Atualiza cooldown do tiro
        if self.cooldown > 0:
            self.cooldown -= 1

    # Desenha o inimigo
    def draw(self, camera_x):
        pygame.draw.rect(
            TELA, VERMELHO,
            (self.x - camera_x, self.y, 32, 48)
        )


# =============================
# CLASSE TIRO
# =============================
class Tiro:
    def __init__(self, x, y, dir, inimigo=False):
        # Posição do tiro
        self.x = x
        self.y = y

        # Direção (1 direita, -1 esquerda)
        self.dir = dir

        # Velocidade depende se é do inimigo ou não
        self.vel = 8 if not inimigo else 6

        # Identifica se o tiro é inimigo
        self.inimigo = inimigo

    # Move o tiro
    def update(self):
        self.x += self.vel * self.dir

    # Desenha o tiro
    def draw(self, camera_x):
        pygame.draw.rect(
            TELA, AMARELO,
            (self.x - camera_x, self.y, 10, 4)
        )


# =============================
# OBJETOS DO JOGO
# =============================

# Instância do player
player = Player()

# Lista de inimigos
inimigos = [Inimigo(700 + i * 400) for i in range(6)]

# Lista de tiros
tiros = []

# Controle da câmera
camera_x = 0

# Estado do jogo
estado = "menu"

# Fonte usada nos textos
fonte = pygame.font.SysFont(None, 40)


# =============================
# LOOP PRINCIPAL DO JOGO
# =============================
rodando = True
while rodando:

    # Controla o FPS
    clock.tick(FPS)

    # =============================
    # EVENTOS
    # =============================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if estado == "menu" and event.key == pygame.K_RETURN:
                estado = "jogo"

            elif estado == "jogo" and event.key == pygame.K_ESCAPE:
                estado = "pausa"

            elif estado == "pausa" and event.key == pygame.K_ESCAPE:
                estado = "jogo"

    # =============================
    # TELAS DE MENU / PAUSA
    # =============================
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

    # Disparo do player
    if player.atirando and player.cooldown == 0:
        y_tiro = player.y + (32 if player.abaixado else 16)
        tiros.append(Tiro(player.x + 32, y_tiro, +1))
        player.cooldown = 12

    # Atualiza inimigos e tiros deles
    for inimigo in inimigos:
        inimigo.update()
        if inimigo.cooldown == 0:
            tiros.append(Tiro(inimigo.x, inimigo.y + 26, -1, inimigo=True))
            inimigo.cooldown = random.randint(60, 140)

    # Atualiza tiros
    for t in tiros[:]:
        t.update()

        # Remove tiros fora do mapa
        if t.x < 0 or t.x > MAPA_LARGURA:
            tiros.remove(t)
            continue

        # Tiro inimigo acertando player
        if t.inimigo and not player.abaixado:
            if (player.x < t.x < player.x + player.larg and
                player.y < t.y < player.y + player.alt):
                player.vida -= 1
                tiros.remove(t)
                continue

        # Tiro do player acertando inimigo
        if not t.inimigo:
            for inimigo in inimigos[:]:
                if (inimigo.x < t.x < inimigo.x + inimigo.larg and
                    inimigo.y < t.y < inimigo.y + inimigo.alt):
                    inimigos.remove(inimigo)
                    tiros.remove(t)
                    break

    # =============================
    # CÂMERA
    # =============================
    camera_x = max(0, min(player.x - 200, MAPA_LARGURA - LARGURA))

    # =============================
    # CONDIÇÕES DE FIM
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
    # TELAS FINAIS
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
