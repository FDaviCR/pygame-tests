import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
GRAY = (120,120,120)
BLUE = (50,50,200)
ORANGE = (200,150,50)

# ===== ANDARES =====
floors = [
    pygame.Rect(50, 500, 700, 20),
    pygame.Rect(50, 350, 700, 20),
    pygame.Rect(50, 200, 700, 20)
]
floors_y = [f.top for f in floors]

# ===== ELEVADOR =====
class Elevator:
    def __init__(self, x, floors_y):
        self.rect = pygame.Rect(x, floors_y[0], 60, 15)
        self.floors_y = floors_y
        self.target = 0
        self.speed = 2
        self.moving = False
        self.last_y = self.rect.y

    def call(self, floor):
        self.target = floor
        self.moving = True

    def update(self):
        self.last_y = self.rect.y
        if not self.moving:
            return

        target_y = self.floors_y[self.target]
        if self.rect.y < target_y:
            self.rect.y += self.speed
        elif self.rect.y > target_y:
            self.rect.y -= self.speed
        else:
            self.moving = False

    def draw(self):
        pygame.draw.rect(screen, ORANGE, self.rect)

elevator = Elevator(370, floors_y)

# ===== PLAYER =====
player = pygame.Rect(100, 460, 30, 40)
speed = 4
gravity = 0

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_1:
                elevator.call(0)
            if e.key == pygame.K_2:
                elevator.call(1)
            if e.key == pygame.K_3:
                elevator.call(2)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed

    gravity += 0.5
    player.y += gravity

    elevator.update()

    # Jogador acompanha elevador
    if player.bottom == elevator.rect.top and \
       player.centerx > elevator.rect.left and \
       player.centerx < elevator.rect.right:
        player.y += elevator.rect.y - elevator.last_y
        gravity = 0

    # Colisão com andares
    for floor in floors:
        if player.colliderect(floor) and gravity >= 0:
            player.bottom = floor.top
            gravity = 0

    # Desenho
    for floor in floors:
        pygame.draw.rect(screen, GRAY, floor)

    elevator.draw()
    pygame.draw.rect(screen, BLUE, player)

    pygame.display.flip()

pygame.quit()
