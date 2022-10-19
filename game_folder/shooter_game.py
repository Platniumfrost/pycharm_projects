import pygame as pg
import random as r
import math
from os import *


# Game object classes
####################################################################

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pg.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH / 2)
        self.rect.bottom = (HEIGHT - (HEIGHT * .05))
        self.speedx = 0

    def update(self):

        # basic movement side to side
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.speedx = 5
        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.speedx = -5
        # if keystate[pg.K_SPACE]:
        #     self.shoot()

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

        self.rect.x += self.speedx

    def shoot(self):
        b = Bullet(self.rect.centerx,self.rect.top+1)
        all_sprites.add(b)
        bullet_group.add(b)



class Bullet(pg.sprite.Sprite):
    def __init__(self, x,y):
        super(Bullet,self).__init__()
        self.image = pg.Surface((5, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        # kill the bullet when bottom < screen
        if self.rect.bottom < 0:
            self.kill()




class NPC(pg.sprite.Sprite):
    def __init__(self):
        super(NPC, self).__init__()
        #self.image = pg.Surface((25, 25))
        #self.image.fill(RED)

        self.image = npc_img
        self.image = pg.transform.scale(self.image,(50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.75/2)
        pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = (WIDTH / 2)
        self.rect.top = (0)
        self.rsx = r.randint(-5,5)
        self.rsy = r.randint(1, 10)
        # self.speed = -10
        #self.rect.x = r.randrange(WIDTH - self.rect.width)
        #self.rect.y = r.randrange(-100, -40)
        #self.speedy = r.randrange(1, 8)
        self.speedx = self.rsx
        self.speedy = self.rsy

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = r.randrange(WIDTH - self.rect.width)
            self.rect.y = r.randrange(-100, -40)
            self.speedy = r.randrange(1, 8)


####################################################################


# Game Constants
####################################################################
HEIGHT = 900
WIDTH = 600
FPS = 60

# Colors (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

title = "Shmup"

####################################################################
###################################################################
# folder variables #
game_folder = path.dirname(__file__)
imgs_folder = path.join(game_folder,"imgs")



###################################################################
# initialize pygame and create window
####################################################################
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(title)
clock = pg.time.Clock()
####################################################################

# load imgs
####################################################################

####################################################################

# create Sprite groups
####################################################################
all_sprites = pg.sprite.Group()
players_group = pg.sprite.Group()
npc_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
####################################################################

# create Game Objects
####################################################################
player = Player()
npc = NPC()
for i in range(10):
    npc = NPC()
    npc_group.add(npc)
# bullet = Bullet(HEIGHT,WIDTH/2)
####################################################################

# add objects to sprite groups
####################################################################
players_group.add(player)
# bullet_group.add(Bullet)
npc_group.add(npc)

for i in players_group:
    all_sprites.add(i)

for i in npc_group:
    all_sprites.add(i)
####################################################################


# Game Loop
###################
# game update Variables
########################################
playing = True

########################################
################################################################
while playing:
    # timing
    ##################################################
    clock.tick(FPS)
    ##################################################

    # collecting Input
    ##################################################

    # Quiting the game when we hit the x
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
            if event.key == pg.K_ESCAPE:
                playing = False
        if event.type == pg.QUIT:
            playing = False

    ##################################################
    # Updates
    ##################################################
    all_sprites.update()

    # if NPC hits player
    hits = pg.sprite.spritecollide(player,npc_group,False)
    if hits:
        playing = False
        #npc.spawn()
    # if bullet hits npc
    hits = pg.sprite.groupcollide(npc_group,bullet_group,True,True)
    for hit in hits:
        npc = NPC()
        npc_group.add(npc)
        all_sprites.add(npc)

    ##################################################
    # Render
    ##################################################

    screen.fill(BLACK)
    screen.blit(background,background_rect)


    all_sprites.draw(screen)

    pg.display.flip()
    ##################################################

pg.quit()
################################################################
#####################
