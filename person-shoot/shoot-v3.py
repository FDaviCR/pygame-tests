import pygame
import sys
import random

pygame.init()

LARG = 960
ALT = 540
TELA = pygame.display.set_mode((LARG, ALT))
pygame.display.set_caption("Contra Mini")
CLOCK = pygame.time.Clock()
FPS = 60

GRAV = 0.6

# ==========================================================
#   SPRITES
# ==========================================================

def player_idle():
    frames=[]
    for i in range(2):
        s=pygame.Surface((40,60),pygame.SRCALPHA)
        pygame.draw.rect(s,(0,120,255),(10,10,20,40))
        pygame.draw.rect(s,(255,255,255),(15,15,10,10))
        if i: pygame.draw.rect(s,(0,0,0),(18,18,5,2))
        frames.append(s)
    return frames

def player_run():
    frames=[]
    for i in range(4):
        s=pygame.Surface((40,60),pygame.SRCALPHA)
        pygame.draw.rect(s,(0,120,255),(10,10,20,40))
        pygame.draw.rect(s,(255,255,255),(15,15,10,10))
        pygame.draw.rect(s,(0,0,0),(18,18,5,2))
        if i%2:
            pygame.draw.rect(s,(0,0,0),(10,45,5,15))
            pygame.draw.rect(s,(0,0,0),(25,50,5,10))
        else:
            pygame.draw.rect(s,(0,0,0),(10,50,5,10))
            pygame.draw.rect(s,(0,0,0),(25,45,5,15))
        frames.append(s)
    return frames

def player_jump():
    s=pygame.Surface((40,60),pygame.SRCALPHA)
    pygame.draw.rect(s,(0,120,255),(10,10,20,40))
    pygame.draw.rect(s,(255,255,255),(15,15,10,10))
    pygame.draw.rect(s,(0,0,0),(18,18,5,2))
    pygame.draw.rect(s,(0,0,0),(10,48,20,6))
    return [s]

def player_shoot():
    frames=[]
    for i in range(2):
        s=pygame.Surface((40,60),pygame.SRCALPHA)
        pygame.draw.rect(s,(0,120,255),(10,10,20,40))
        pygame.draw.rect(s,(255,255,255),(15,15,10,10))
        pygame.draw.rect(s,(0,0,0),(18,18,5,2))
        pygame.draw.rect(s,(0,0,0),(30,28,15,4))
        frames.append(s)
    return frames

def player_crouch():
    s=pygame.Surface((40,35),pygame.SRCALPHA)
    pygame.draw.rect(s,(0,120,255),(10,5,20,25))
    pygame.draw.rect(s,(255,255,255),(15,8,10,10))
    return [s]

def enemy_walk():
    frames=[]
    for i in range(2):
        s=pygame.Surface((40,60),pygame.SRCALPHA)
        pygame.draw.rect(s,(255,50,50),(10,10,20,40))
        pygame.draw.rect(s,(0,0,0),(15,15,10,10))
        if i:
            pygame.draw.rect(s,(0,0,0),(10,45,5,15))
            pygame.draw.rect(s,(0,0,0),(25,50,5,10))
        else:
            pygame.draw.rect(s,(0,0,0),(10,50,5,10))
            pygame.draw.rect(s,(0,0,0),(25,45,5,15))
        frames.append(s)
    return frames

PLAYER_ANIM={
    "idle":player_idle(),
    "run":player_run(),
    "jump":player_jump(),
    "shoot":player_shoot(),
    "crouch":player_crouch()
}

ENEMY_ANIM=enemy_walk()

# ==========================================================
#   CLASSES
# ==========================================================

class Player:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,40,60)
        self.vx = 0
        self.vy = 0
        self.no_chao = False
        self.estado="idle"
        self.frame=0
        self.normal_h=60
        self.crouch_h=35
        self.balas=[]
        self.vivo=True

    def update(self,tecla):
        if not self.vivo: return

        self.vx=0
        if tecla[pygame.K_a]: self.vx=-4
        if tecla[pygame.K_d]: self.vx=4
        self.rect.x+=self.vx

        crouch = tecla[pygame.K_s]
        if crouch and self.no_chao:
            self.estado="crouch"
            self.rect.height=self.crouch_h
        else:
            self.rect.height=self.normal_h

        if tecla[pygame.K_SPACE] and self.no_chao:
            self.vy=-12
            self.no_chao=False

        self.vy+=GRAV
        self.rect.y+=self.vy

        if tecla[pygame.K_j]:
            self.shoot()

        if not self.no_chao: self.estado="jump"
        elif tecla[pygame.K_j]: self.estado="shoot"
        elif self.vx!=0: self.estado="run"
        elif crouch: pass
        else: self.estado="idle"

        self.frame+=0.2
        if self.frame>=len(PLAYER_ANIM[self.estado]):
            self.frame=0

    def shoot(self):
        if len(self.balas)==0 or self.balas[-1].x-self.rect.x>40:
            self.balas.append(pygame.Rect(self.rect.centerx,self.rect.centery-5,14,4))

    def draw(self,t,ox):
        if not self.vivo:return
        img=PLAYER_ANIM[self.estado][int(self.frame)]
        t.blit(img,(self.rect.x-ox,self.rect.y))
        for b in self.balas:
            pygame.draw.rect(t,(255,255,0),(b.x-ox,b.y,b.w,b.h))

class Enemy:
    def __init__(self,x,y):
        self.rect=pygame.Rect(x,y,40,60)
        self.vx=2
        self.vy=0
        self.frame=0
        self.balas=[]
        self.no_chao=False
        self.vivo=True

    def update(self,player):
        if not self.vivo:return

        self.rect.x+=self.vx
        if self.rect.x<200 or self.rect.x>2000:
            self.vx*=-1

        # IA: desviar tiros
        for b in player.balas:
            if abs(b.x-self.rect.x)<120:
                if random.random()<0.3 and self.no_chao:
                    self.vy=-10
                elif random.random()<0.4:
                    self.rect.height=35

        if random.random()<0.01:
            self.shoot()

        self.vy+=GRAV
        self.rect.y+=self.vy

        self.frame+=0.1
        if self.frame>=2:self.frame=0

    def shoot(self):
        self.balas.append(pygame.Rect(self.rect.centerx,self.rect.centery-5,14,4))

    def draw(self,t,ox):
        if not self.vivo:return
        t.blit(ENEMY_ANIM[int(self.frame)],(self.rect.x-ox,self.rect.y))
        for b in self.balas:
            pygame.draw.rect(t,(255,50,50),(b.x-ox,b.y,b.w,b.h))

# ==========================================================
#   CENÁRIO
# ==========================================================

player=Player(200,200)
inimigos=[Enemy(600,ALT-160),Enemy(1100,ALT-160),Enemy(1700,ALT-160)]
chao=pygame.Rect(0,ALT-100,2400,100)
fim=2400
offset=0

jogo_fim=False
mensagem=""

# ==========================================================
#   LOOP PRINCIPAL
# ==========================================================

while True:
    CLOCK.tick(FPS)

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if jogo_fim and e.type==pygame.KEYDOWN:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    if not jogo_fim:
        player.update(teclas)
        for i in inimigos:
            i.update(player)

        if player.rect.colliderect(chao):
            player.rect.bottom=chao.top
            player.vy=0
            player.no_chao=True
        else: player.no_chao=False

        for i in inimigos:
            if i.rect.colliderect(chao):
                i.rect.bottom=chao.top
                i.vy=0
                i.no_chao=True
            else: i.no_chao=False

        for b in player.balas[:]:
            b.x+=10
            if b.x>fim: player.balas.remove(b)
            for i in inimigos:
                if i.vivo and i.rect.colliderect(b):
                    i.vivo=False
                    player.balas.remove(b)
                    break

        for i in inimigos:
            for b in i.balas[:]:
                b.x-=8
                if b.x<0: i.balas.remove(b)
                if player.estado=="crouch" and b.y<player.rect.y+15:
                    continue
                if player.rect.colliderect(b):
                    player.vivo=False
                    jogo_fim=True
                    mensagem="DERROTA!"

        if all(not i.vivo for i in inimigos) and player.rect.x>fim-200:
            jogo_fim=True
            mensagem="VITÓRIA!"

        offset=max(0,min(player.rect.x-LARG//2,fim-LARG))

    TELA.fill((80,80,180))
    pygame.draw.rect(TELA,(100,200,100),(chao.x-offset,chao.y,chao.w,chao.h))

    for i in inimigos: i.draw(TELA,offset)
    player.draw(TELA,offset)

    if jogo_fim:
        f1=pygame.font.SysFont(None,90)
        t1=f1.render(mensagem,True,(255,255,255))
        TELA.blit(t1,(LARG//2-t1.get_width()//2,ALT//2-50))
        f2=pygame.font.SysFont(None,40)
        t2=f2.render("Pressione qualquer tecla para sair",True,(255,255,255))
        TELA.blit(t2,(LARG//2-t2.get_width()//2,ALT//2+10))

    pygame.display.update()
jj