import pygame
import sys

pygame.init()

LARG = 960
ALT = 540
TELA = pygame.display.set_mode((LARG, ALT))
CLOCK = pygame.time.Clock()
FPS = 60
GRAV = 0.6

# ======================================================
#   FUNÇÕES DE SPRITES CONTRA
# ======================================================

def contra_idle():
    frames = []
    for _ in range(2):
        surf = pygame.Surface((46,56), pygame.SRCALPHA)
        # tronco
        pygame.draw.rect(surf,(40,120,255),(18,12,20,30))
        # cabeça
        pygame.draw.rect(surf,(255,200,150),(20,2,16,10))
        # rifle
        pygame.draw.rect(surf,(60,60,60),(32,24,18,4))
        pygame.draw.rect(surf,(20,20,20),(44,24,8,2))
        frames.append(surf)
    return frames

def contra_run():
    frames=[]
    for i in range(4):
        surf = pygame.Surface((46,56), pygame.SRCALPHA)
        pygame.draw.rect(surf,(40,120,255),(18,12,20,30))
        pygame.draw.rect(surf,(255,200,150),(20,2,16,10))
        pygame.draw.rect(surf,(60,60,60),(32,24,18,4))
        pygame.draw.rect(surf,(20,20,20),(44,24,8,2))
        # pernas estilo contra
        if i%2==0:
            pygame.draw.rect(surf,(40,120,255),(18,42,8,12))
            pygame.draw.rect(surf,(40,120,255),(28,36,8,18))
        else:
            pygame.draw.rect(surf,(40,120,255),(18,36,8,18))
            pygame.draw.rect(surf,(40,120,255),(28,42,8,12))
        frames.append(surf)
    return frames

def contra_jump():
    surf = pygame.Surface((46,56), pygame.SRCALPHA)
    pygame.draw.rect(surf,(40,120,255),(18,10,20,32))
    pygame.draw.rect(surf,(255,200,150),(20,2,16,10))
    pygame.draw.rect(surf,(60,60,60),(32,24,18,4))
    pygame.draw.rect(surf,(20,20,20),(44,24,8,2))
    pygame.draw.rect(surf,(40,120,255),(20,40,18,10))
    return [surf]

def contra_shoot():
    frames=[]
    for i in range(2):
        surf = pygame.Surface((46,56), pygame.SRCALPHA)
        pygame.draw.rect(surf,(40,120,255),(18,12,20,30))
        pygame.draw.rect(surf,(255,200,150),(20,2,16,10))
        pygame.draw.rect(surf,(60,60,60),(32,24,22,4))
        pygame.draw.rect(surf,(20,20,20),(50,24,10,2))
        frames.append(surf)
    return frames

def enemy_walk():
    frames=[]
    for i in range(2):
        surf = pygame.Surface((46,56), pygame.SRCALPHA)
        pygame.draw.rect(surf,(220,60,60),(18,12,20,30))
        pygame.draw.rect(surf,(200,180,150),(20,2,16,10))
        pygame.draw.rect(surf,(60,60,60),(32,24,18,4))
        if i==0:
            pygame.draw.rect(surf,(220,60,60),(18,42,8,12))
            pygame.draw.rect(surf,(220,60,60),(28,36,8,18))
        else:
            pygame.draw.rect(surf,(220,60,60),(18,36,8,18))
            pygame.draw.rect(surf,(220,60,60),(28,42,8,12))
        frames.append(surf)
    return frames

PLAYER_ANIM = {
    "idle": contra_idle(),
    "run": contra_run(),
    "jump": contra_jump(),
    "shoot": contra_shoot()
}

ENEMY_ANIM = enemy_walk()

# ======================================================
#                    CLASSES
# ======================================================

class Player:
    def __init__(self,x,y):
        self.rect=pygame.Rect(x,y,46,56)
        self.vx=0
        self.vy=0
        self.estado="idle"
        self.frame=0
        self.no_chao=False
        self.balas=[]

    def update(self,keys):
        self.vx=0
        if keys[pygame.K_a]: self.vx=-5
        if keys[pygame.K_d]: self.vx=5

        self.rect.x+=self.vx

        if keys[pygame.K_SPACE] and self.no_chao:
            self.vy=-14
            self.no_chao=False

        self.vy+=GRAV
        self.rect.y+=self.vy

        if keys[pygame.K_j]: self.shoot()

        if not self.no_chao:
            self.estado="jump"
        elif keys[pygame.K_j]:
            self.estado="shoot"
        elif self.vx!=0:
            self.estado="run"
        else:
            self.estado="idle"

        self.frame+=0.2
        if self.frame>=len(PLAYER_ANIM[self.estado]):
            self.frame=0

    def shoot(self):
        if len(self.balas)==0 or self.balas[-1].x-self.rect.x>40:
            self.balas.append(pygame.Rect(self.rect.centerx+20,self.rect.centery,12,4))

    def draw(self,tela,ox):
        img=PLAYER_ANIM[self.estado][int(self.frame)]
        tela.blit(img,(self.rect.x-ox,self.rect.y))
        for b in self.balas:
            pygame.draw.rect(tela,(255,240,60),(b.x-ox,b.y,12,4))

class Enemy:
    def __init__(self,x,y):
        self.rect=pygame.Rect(x,y,46,56)
        self.dir=1
        self.frame=0

    def update(self):
        self.rect.x+=self.dir*2
        if self.rect.x<200 or self.rect.x>1800: self.dir*=-1
        self.frame+=0.1
        if self.frame>=2: self.frame=0

    def draw(self,tela,ox):
        tela.blit(ENEMY_ANIM[int(self.frame)],(self.rect.x-ox,self.rect.y))

# ======================================================
#                    CENÁRIO
# ======================================================

player=Player(200,200)
inimigos=[Enemy(700,ALT-156),Enemy(1200,ALT-156)]
chao=pygame.Rect(0,ALT-100,2000,100)
offset=0

# ======================================================
#                LOOP PRINCIPAL
# ======================================================

while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT: pygame.quit();sys.exit()

    keys=pygame.key.get_pressed()
    CLOCK.tick(FPS)
    player.update(keys)
    for i in inimigos: i.update()

    if player.rect.colliderect(chao):
        player.rect.bottom=chao.top
        player.vy=0
        player.no_chao=True
    else:
        player.no_chao=False

    for b in player.balas[:]:
        b.x+=10
        if b.x>2000: player.balas.remove(b)

    offset=max(0,min(player.rect.x-LARG//2,2000-LARG))

    TELA.fill((30,30,80))
    pygame.draw.rect(TELA,(60,140,60),(chao.x-offset,chao.y,2000,100))
    for i in inimigos: i.draw(TELA,offset)
    player.draw(TELA,offset)
    pygame.display.update()
