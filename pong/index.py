import pygame
import sys

pygame.init()

# --- Configurações ---
WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
WHITE = (255, 255, 255)

BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 90
BALL_SPEED = 5
PADDLE_SPEED = 6

font = pygame.font.SysFont("comicsans", 40)


# --- Objetos ---
player = pygame.Rect(20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
enemy = pygame.Rect(WIDTH-30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)

ball_vel = [BALL_SPEED, BALL_SPEED]
score_player = 0
score_enemy = 0


# --- Loop principal ---
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controles do jogador (W / S)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.top > 0:
        player.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += PADDLE_SPEED

    # Inimigo simples (segue a bola)
    if enemy.centery < ball.centery:
        enemy.y += PADDLE_SPEED
    else:
        enemy.y -= PADDLE_SPEED

    # Limites do inimigo
    enemy.y = max(0, min(enemy.y, HEIGHT - PADDLE_HEIGHT))

    # Movimento da bola
    ball.x += ball_vel[0]
    ball.y += ball_vel[1]

    # Colisões com parede
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel[1] *= -1

    # Colisão com raquetes
    if ball.colliderect(player) or ball.colliderect(enemy):
        ball_vel[0] *= -1

    # Pontuação
    if ball.left <= 0:
        score_enemy += 1
        ball.center = (WIDTH//2, HEIGHT//2)
    if ball.right >= WIDTH:
        score_player += 1
        ball.center = (WIDTH//2, HEIGHT//2)

    # --- Render ---
    WIN.fill((0, 0, 0))
    pygame.draw.rect(WIN, WHITE, player)
    pygame.draw.rect(WIN, WHITE, enemy)
    pygame.draw.ellipse(WIN, WHITE, ball)
    pygame.draw.aaline(WIN, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    score_text = font.render(f"{score_player}   {score_enemy}", True, WHITE)
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    pygame.display.flip()
