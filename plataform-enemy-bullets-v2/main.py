import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 480
TILE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plataforma com Queda Mortal")

clock = pygame.time.Clock()

# MAPA
# 0 = vazio
# 1 = bloco sólido
# 2 = inimigo
# 9 = final
map_data = [
    "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "0000000000000000000000000020000000000000200000000000000000000000000000000000000000000000000000000000000000000000",
    "0000000000000000111000000011100000000011111100000000000000000000000000000000000000000000000000000000000000000000",
    "0000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000",
    "1111111100000011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111190"
]

MAP_HEIGHT = len(map_data)
MAP_WIDTH = len(map_data[0]) * TILE

# PLAYER
player = pygame.Rect(100, 00, 30, 40)
player_vel_y = 0
player_speed = 5
gravity = 0.6
jump = False
alive = True
victory = False

# TIROS
player_bullets = []
enemy_bullets = []
bullet_speed = 7

# INIMIGOS
enemies = []
for r, row in enumerate(map_data):
    for c, cell in enumerate(row):
        if cell == "2":
            enemies.append({
                "rect": pygame.Rect(c*TILE, r*TILE, 30, 40),
                "cooldown": random.randint(60, 120)
            })

# CAMERA
camera_x = 0

def shoot_player():
    player_bullets.append([player.centerx, player.centery, 1])

def shoot_enemy(e):
    enemy_bullets.append([e["rect"].centerx, e["rect"].centery, -1])

def get_tiles():
    tiles = []
    for r in range(MAP_HEIGHT):
        for c in range(len(map_data[0])):
            if map_data[r][c] == "1":
                tiles.append(pygame.Rect(c*TILE, r*TILE, TILE, TILE))
    return tiles

tiles = get_tiles()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if alive and not victory:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_player()

    if alive and not victory:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_a]: dx -= player_speed
        if keys[pygame.K_d]: dx += player_speed

        # Pulo
        if keys[pygame.K_w] and not jump:
            jump = True
            player_vel_y = -12

        player_vel_y += gravity
        dy += player_vel_y

        # Eixo X
        player.x += dx
        for t in tiles:
            if player.colliderect(t):
                if dx > 0: player.right = t.left
                if dx < 0: player.left = t.right

        # Eixo Y
        player.y += dy
        for t in tiles:
            if player.colliderect(t):
                if dy > 0:
                    player.bottom = t.top
                    player_vel_y = 0
                    jump = False
                if dy < 0:
                    player.top = t.bottom
                    player_vel_y = 0

        # **MORTE POR QUEDA**
        if player.y > HEIGHT + 200:
            alive = False

        # INIMIGOS
        for e in enemies:
            e["cooldown"] -= 1
            if e["cooldown"] <= 0:
                shoot_enemy(e)
                e["cooldown"] = random.randint(80, 140)

        # TIROS PLAYER
        for b in player_bullets[:]:
            b[0] += bullet_speed
            if b[0] > MAP_WIDTH:
                player_bullets.remove(b)

        # TIROS INIMIGO
        for b in enemy_bullets[:]:
            b[0] -= bullet_speed
            if b[0] < 0:
                enemy_bullets.remove(b)

        # ACERTOS
        for b in enemy_bullets:
            if player.collidepoint(b[0], b[1]):
                alive = False

        for e in enemies[:]:
            for b in player_bullets[:]:
                if e["rect"].collidepoint(b[0], b[1]):
                    enemies.remove(e)
                    player_bullets.remove(b)
                    break

        # FINAL DO MAPA
        for r in range(MAP_HEIGHT):
            for c in range(len(map_data[0])):
                if map_data[r][c] == "9":
                    end = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
                    if player.colliderect(end):
                        victory = True

    # CÂMERA
    camera_x = max(0, min(player.x - WIDTH//2, MAP_WIDTH - WIDTH))

    # DESENHO
    screen.fill((100, 180, 255))

    for r in range(MAP_HEIGHT):
        for c in range(len(map_data[0])):
            cell = map_data[r][c]
            x, y = c*TILE - camera_x, r*TILE
            if cell == "1": pygame.draw.rect(screen, (70,70,70), (x,y,TILE,TILE))
            if cell == "9": pygame.draw.rect(screen, (0,255,0), (x,y,TILE,TILE))

    for e in enemies:
        pygame.draw.rect(screen, (255,50,50), (e["rect"].x-camera_x, e["rect"].y, 30,40))

    if alive:
        pygame.draw.rect(screen, (50,255,50), (player.x-camera_x, player.y, player.width, player.height))

    for b in player_bullets:
        pygame.draw.circle(screen, (255,255,0), (b[0]-camera_x, b[1]), 4)
    for b in enemy_bullets:
        pygame.draw.circle(screen, (255,0,0), (b[0]-camera_x, b[1]), 4)

    font = pygame.font.SysFont(None, 32)
    if not alive: screen.blit(font.render("Você Morreu!", True, (255,0,0)), (350,200))
    if victory: screen.blit(font.render("Você Venceu!", True, (0,255,0)), (350,200))

    pygame.display.update()

pygame.quit()
