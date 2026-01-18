import pygame
import sys
from random import randint

pygame.init()

# ================================
# CONFIG
# ================================
LARG, ALT = 960, 540
TELA = pygame.display.set_mode((LARG, ALT))
pygame.display.set_caption("Run'n Gun - Protótipo A")
CLOCK = pygame.time.Clock()
FPS = 60

GRAV = 0.7
MAPA_LARG = 3500

# ================================
# UTILS
# ================================
def texto(txt, tam, cor, x, y, center=True):
    font = pygame.font.SysFont("consolas", tam)
    s = font.render(txt, True, cor)
    if center:
        TELA.blit(s, (x - s.get_width()//2, y - s.get_height()//2))
    else:
        TELA.blit(s, (x, y))

# ================================
# SPRITES GERADOS POR CÓDIGO
# ================================
def spr_idle():
    surf = pygame.Surface((32,48), pygame.SRCALPHA)
    pygame.draw.rect(surf,(0,120,255),(6,8,20,32))
    pygame.draw.rect(surf,(255,255,255),(10,12,12,12))
    return [surf]

def spr_run():
    frames=[]
    for i in range(4):
        surf = pygame.Surface((32,48), pygame.SRCALPHA)
        pygame.draw.rect(surf,(0,120,255),(6,8,20,32))
        pygame.draw.rect(surf,(255,255,255),(10,12,12,12))
        if i%2==0:
            pygame.draw.rect(surf,(0,0,0),(6,38,6,8))
            pygame.draw.rect(surf,(0,0,0),(20,34,6,12))
        else:
            pygame.draw.rect(surf,(0,0,0),(6,34,6,12))
            pygame.draw.rect(surf,(0,0,0),(20,38,6,8))
        frames.append(surf)
    return frames

def spr_jump():
    surf = pygame.Surface((32,48), pygame.SRCALPHA)
    pygame.draw.rect(surf,(0,120,255),(6,8,20,32))
    pygame.draw.rect(surf,(255,255,255),(10,12,12,12))
    pygame.draw.rect(surf,(0,0,0),(6,34,20,6))
    return [surf]

def spr_crouch():
    surf = pygame.Surface((32,24), pygame.SRCALPHA)
    pygame.draw.rect(surf,(0,120,255),(6,4,20,16))
    pygame.draw.rect(surf,(255,255,255),(10,6,12,10))
    return [surf]

def spr_shoot():
    frames=[]
    for i in range(2):
        surf = pygame.Surface((40,48), pygame.SRCALPHA)
        pygame.draw.rect(surf,(0,120,255),(6,8,20,32))
        pygame.draw.rect(surf,(255,255,255),(10,12,12,12))
        pygame.draw.rect(surf,(0,0,0),(26,22,14,4))
        frames.append(surf)
    return frames

def spr_enemy():
    frames=[]
    for i in range(2):
        surf = pygame.Surface((32,48), pygame.SRCALPHA)
        pygame.draw.rect(surf,(255,60,60),(6,8,20,32))
        pygame.draw.rect(surf,(0,0,0),(10,12,12,12))
        frames.append(surf)
    return frames

PLAYER_ANIMS = {
    "idle": spr_idle(),
    "run": spr_run(),
    "jump": spr_jump(),
    "crouch": spr_crouch(),
    "shoot": spr_shoot(),
}

ENEMY_WALK = spr_enemy()

# ================================
# TIROS
# ================================
class Tiro:
    def __init__(self,x,y,dir,inimigo=False):
        self.x = x
        self.y = y
        self.dir = dir
        self.vel = 8 if not inimigo else 6
        self.inimigo = inimigo

    def update(self):
        self.x += self.vel*self.dir
        return (self.x < -100 or self.x > MAPA_LARG+100)

    def draw(self,cam):
        pygame.draw.rect(TELA,(255,255,0) if not self.inimigo else (255,120,0),(self.x-cam,self.y,10,4))

# ================================
# ENEMY
# ================================
class Enemy:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vx=2
        self.frame=0
        self.cool=randint(60,120)
        self.vivo=True

    def update(self,player,tiros):
        if not self.vivo:
            return
        self.x += self.vx
        if self.x<400 or self.x>MAPA_LARG-400:
            self.vx*=-1
        self.frame+=0.1
        if self.frame>=len(ENEMY_WALK): self.frame=0
        self.cool-=1
        if self.cool<=0:
            self.cool=randint(80,160)
            dir = -1 if self.x>player.x else 1
            tiros.append(Tiro(self.x,self.y+20,dir,True))

    def draw(self,cam):
        if self.vivo:
            TELA.blit(ENEMY_WALK[int(self.frame)],(self.x-cam,self.y))

# ================================
# PLAYER
# ================================
class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vx=0
        self.vy=0
        self.estado="idle"
        self.frame=0
        self.pulando=False
        self.abaixado=False
        self.tiros=[]
        self.vida=3

    def update(self,keys):
        self.vx=0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx=-4
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx=4

        self.x+=self.vx

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and not self.pulando and not self.abaixado:
            self.vy=-14
            self.pulando=True

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.abaixado=True
        else:
            self.abaixado=False

        self.vy+=GRAV
        self.y+=self.vy

        if self.y>ALT-100-48:
            self.y=ALT-100-48
            self.vy=0
            self.pulando=False

        if keys[pygame.K_j]:
            if len(self.tiros)==0 or self.tiros[-1].x-self.x>30:
                self.tiros.append(Tiro(self.x+30,self.y+20,1,False))

        if self.abaixado: self.estado="crouch"
        elif self.pulando: self.estado="jump"
        elif keys[pygame.K_j]: self.estado="shoot"
        elif self.vx!=0: self.estado="run"
        else: self.estado="idle"

        self.frame+=0.2
        if self.frame>=len(PLAYER_ANIMS[self.estado]):
            self.frame=0

    def draw(self,cam):
        img = PLAYER_ANIMS[self.estado][int(self.frame)]
        TELA.blit(img,(self.x-cam,self.y))
        for t in self.tiros:
            t.draw(cam)

# ================================
# INICIALIZAÇÃO
# ================================
player = Player(200,100)
inimigos = [Enemy(800,ALT-148), Enemy(1400,ALT-148), Enemy(2200,ALT-148)]
tiros=[]
estado="menu"
cam=0

# ================================
# LOOP PRINCIPAL
# ================================
while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()

    if estado=="menu":
        TELA.fill((20,20,30))
        texto("RUN'N GUN",48,(255,255,255),LARG//2,200)
        texto("Pressione ENTER para iniciar",22,(200,200,200),LARG//2,300)
        pygame.display.update()
        if keys[pygame.K_RETURN]:
            estado="jogo"
        CLOCK.tick(FPS)
        continue

    if estado=="pausa":
        texto("PAUSADO",42,(255,255,255),LARG//2,ALT//2)
        pygame.display.update()
        if keys[pygame.K_p]:
            estado="jogo"
        CLOCK.tick(FPS)
        continue

    if keys[pygame.K_p]:
        estado="pausa"

    # ==== GAMEPLAY ====
    player.update(keys)
    for i in inimigos: i.update(player,tiros)

    # tiros
    for t in player.tiros[:]:
        if t.update(): player.tiros.remove(t)

    for t in tiros[:]:
        if t.update(): tiros.remove(t)

    # colisão tiros → inimigos
    for t in player.tiros[:]:
        for en in inimigos:
            if en.vivo and en.x<t.x<en.x+32 and en.y<t.y<en.y+48:
                en.vivo=False
                player.tiros.remove(t)
                break

    # colisão tiros → player
    h = 24 if player.abaixado else 48
    for t in tiros[:]:
        if player.x<t.x<player.x+32 and player.y<t.y<player.y+h:
            if not player.abaixado:
                player.vida-=1
                tiros.remove(t)
                if player.vida<=0:
                    estado="gameover"

    # final do mapa
    if player.x>MAPA_LARG-300:
        estado="fim"

    cam = max(0,min(player.x-200,MAPA_LARG-LARG))

    TELA.fill((80,180,240))
    pygame.draw.rect(TELA,(100,200,100),(0-cam,ALT-100,MAPA_LARG,100))

    for en in inimigos: en.draw(cam)
    for t in tiros: t.draw(cam)
    player.draw(cam)

    texto(f"HP: {player.vida}",22,(255,255,255),50,20,center=False)

    pygame.display.update()
    CLOCK.tick(FPS)
