import pygame
import random
import sys

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Alvos")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
BLACK = (0, 0, 0)

# Jogador
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 20
player_y = HEIGHT - 50

# Balas
bullets = []
BULLET_SPEED = 8

# Alvos
targets = []
TARGET_SPEED = 2
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1200)

# Pontuação
score = 0
font = pygame.font.SysFont(None, 36)

def spawn_target():
    direction = random.choice(["up", "down"])
    x = random.randint(20, WIDTH - 20)

    if direction == "up":
        y = HEIGHT + 30
        speed = -TARGET_SPEED
    else:
        y = -30
        speed = TARGET_SPEED

    rect = pygame.Rect(x, y, 30, 30)
    targets.append({"rect": rect, "speed": speed})

# Loop principal
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_EVENT:
            spawn_target()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mx, my = pygame.mouse.get_pos()
                bullet_rect = pygame.Rect(mx - 3, player_y, 6, 10)
                bullets.append(bullet_rect)

    # Jogador segue o mouse
    mouse_x, _ = pygame.mouse.get_pos()
    player_rect = pygame.Rect(mouse_x - PLAYER_WIDTH // 2, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    pygame.draw.rect(screen, BLUE, player_rect)

    # Atualizar balas
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        pygame.draw.rect(screen, BLACK, bullet)
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Atualizar alvos
    for target in targets[:]:
        target["rect"].y += target["speed"]
        pygame.draw.rect(screen, RED, target["rect"])

        # Remover se sair da tela
        if target["rect"].top > HEIGHT or target["rect"].bottom < 0:
            targets.remove(target)

        # Colisão bala x alvo
        for bullet in bullets[:]:
            if bullet.colliderect(target["rect"]):
                bullets.remove(bullet)
                targets.remove(target)
                score += 1
                break

    # Mostrar pontuação
    score_text = font.render(f"Pontos: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
