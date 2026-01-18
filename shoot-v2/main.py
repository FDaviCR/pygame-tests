import pygame
import random
import sys

pygame.init()

# ================= CONFIG =================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter com Menu, Pause e Movimento")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GRAY = (180, 180, 180)

# Fonte
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

# Estados
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
state = MENU

# ================= CLASSES =================
class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 20)
        self.speed = 5
        self.lives = 3

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Limites da tela
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(HEIGHT // 2, min(HEIGHT - self.rect.height, self.rect.y))

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top, -8, "player")


class Bullet:
    def __init__(self, x, y, speed, owner):
        self.rect = pygame.Rect(x - 3, y, 6, 12)
        self.speed = speed
        self.owner = owner

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)


class Enemy:
    def __init__(self):
        self.x = random.randint(30, WIDTH - 30)
        self.direction = random.choice(["down", "up"])

        if self.direction == "down":
            self.y = -40
            self.speed = 2
            self.bullet_speed = 6
        else:
            self.y = HEIGHT + 40
            self.speed = -2
            self.bullet_speed = -6

        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed

    def can_shoot(self):
        return pygame.time.get_ticks() - self.last_shot > 1500

    def shoot(self):
        self.last_shot = pygame.time.get_ticks()
        return Bullet(self.rect.centerx, self.rect.centery, self.bullet_speed, "enemy")

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# ================= FUNÇÕES =================
def reset_game():
    global player, bullets, enemies
    player = Player()
    bullets = []
    enemies = []

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    label = font.render(text, True, BLACK)
    screen.blit(label, (rect.centerx - label.get_width() // 2,
                        rect.centery - label.get_height() // 2))

# ================= SETUP =================
reset_game()
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 1200)

# ================= LOOP PRINCIPAL =================
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    reset_game()
                    state = PLAYING
                if quit_btn.collidepoint(event.pos):
                    running = False

        elif state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(player.shoot())
                if event.key == pygame.K_ESCAPE:
                    state = PAUSED

            if event.type == SPAWN_ENEMY:
                enemies.append(Enemy())

        elif state == PAUSED:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = PLAYING

        elif state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                state = MENU

    # ================= DESENHO =================
    if state == MENU:
        title = big_font.render("SHOOTER", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        start_btn = pygame.Rect(WIDTH//2 - 100, 280, 200, 50)
        quit_btn = pygame.Rect(WIDTH//2 - 100, 350, 200, 50)

        draw_button(start_btn, "Iniciar")
        draw_button(quit_btn, "Sair")

    elif state == PLAYING:
        player.update(keys)
        player.draw()

        for enemy in enemies[:]:
            enemy.update()
            enemy.draw()

            if enemy.can_shoot():
                bullets.append(enemy.shoot())

            # Remove somente depois que já passou pela tela
            if enemy.direction == "down" and enemy.rect.top > HEIGHT:
                enemies.remove(enemy)

            if enemy.direction == "up" and enemy.rect.bottom < 0:
                enemies.remove(enemy)

        for bullet in bullets[:]:
            bullet.update()
            bullet.draw()

            if bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT:
                bullets.remove(bullet)

            if bullet.owner == "enemy" and bullet.rect.colliderect(player.rect):
                bullets.remove(bullet)
                player.lives -= 1

            if bullet.owner == "player":
                for enemy in enemies[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        break

        hud = font.render(f"Vidas: {player.lives}", True, BLACK)
        screen.blit(hud, (10, 10))

        if player.lives <= 0:
            state = GAME_OVER

    elif state == PAUSED:
        pause = big_font.render("PAUSE", True, BLACK)
        screen.blit(pause, (WIDTH//2 - pause.get_width()//2,
                            HEIGHT//2 - pause.get_height()//2))

    elif state == GAME_OVER:
        over = big_font.render("GAME OVER", True, RED)
        info = font.render("Pressione qualquer tecla", True, BLACK)

        screen.blit(over, (WIDTH//2 - over.get_width()//2, 250))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 320))

    pygame.display.flip()

pygame.quit()
sys.exit()
