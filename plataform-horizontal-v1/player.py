import pygame

class Player:
    def __init__(self, x, y, level):
        self.level = level
        self.rect = pygame.Rect(x, y, 26, 32)
        self.vel = pygame.Vector2(0, 0)
        self.speed = 180
        self.jump_force = -420
        self.gravity = 900
        self.on_ground = False

    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.vel.x = 0
        if keys[pygame.K_a]:
            self.vel.x = -self.speed
        if keys[pygame.K_d]:
            self.vel.x = self.speed

        # pular
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = self.jump_force

        # gravidade
        self.vel.y += self.gravity * dt

        # mover e colidir
        self.move(dt)

    def move(self, dt):
        self.rect.x += self.vel.x * dt
        self.collide("x")

        self.rect.y += self.vel.y * dt
        self.collide("y")

    def collide(self, axis):
        self.on_ground = False
        for tile in self.level.tiles:
            if self.rect.colliderect(tile):
                if axis == "x":
                    if self.vel.x > 0:
                        self.rect.right = tile.left
                    elif self.vel.x < 0:
                        self.rect.left = tile.right
                if axis == "y":
                    if self.vel.y > 0:
                        self.rect.bottom = tile.top
                        self.vel.y = 0
                        self.on_ground = True
                    elif self.vel.y < 0:
                        self.rect.top = tile.bottom
                        self.vel.y = 0

    def draw(self, win, cam_x):
        pygame.draw.rect(win, (255, 50, 50),
        pygame.Rect(self.rect.x - cam_x, self.rect.y, self.rect.width, self.rect.height))

