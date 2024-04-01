from math import *
from random import randint
from numpy import asarray, linalg, array
from PIL import Image
from pyglet.gl import GL_LINEAR

from package.conf import *
from pyglet.window import key
from package.entity import Entity
source = pyglet.media.load('res/audio/step.mp3', streaming=False)


class Player(Entity):

    def __init__(self, pos, size, textures ={"default": None}):
        super().__init__(pos, size, textures ={"default": pyglet.image.load(f"res/player/playerS1.png")})
        self.speed = 0.3
        self.maxHp = 100
        #self.hud = PlayerHud(self.batc)
        self.cam = [0,0]
        self.pVelocity = [self.velocity[0], self.velocity[1]]
        self.keys = {'w':False,'s':False, 'd':False, 'a':False}
        self.t = 0
        self.tp = 0
        self.animW = [pyglet.image.load('res/player/playerW1.png'), pyglet.image.load('res/player/playerW2.png'), pyglet.image.load('res/player/playerW3.png')]
        self.animA = [pyglet.image.load('res/player/playerA1.png'), pyglet.image.load('res/player/playerA2.png'), pyglet.image.load('res/player/playerA3.png')]
        self.animS = [pyglet.image.load('res/player/playerS1.png'), pyglet.image.load('res/player/playerS2.png'), pyglet.image.load('res/player/playerS3.png')]
        self.animD = [pyglet.image.load('res/player/playerD1.png'), pyglet.image.load('res/player/playerD2.png'), pyglet.image.load('res/player/playerD3.png')]


        self.upProgress = 0
    def draw(self, cam, zoom):


        if self.keys['w']==True or self.keys['a']==True or self.keys['s']==True or self.keys['d']==True:
            self.tp = self.t
            self.t += 3


        if self.t>33 and self.tp <= 33:
            source.play()
            self.spr = pyglet.sprite.Sprite(self.animW[1], 0, 0, batch = self.batc)
            self.spr.scale_x = self.size[0]
            self.spr.scale_y = self.size[1]
        if self.t > 66 and self.tp <= 66:
            source.play()
            self.spr = pyglet.sprite.Sprite(self.animW[2], 0, 0, batch=self.batc)
            self.spr.scale_x = self.size[0]
            self.spr.scale_y = self.size[1]
        if self.t > 100:
            source.play()
            self.t = 0
            self.spr = pyglet.sprite.Sprite(self.animW[0], 0, 0, batch=self.batc)
            self.spr.scale_x = self.size[0]
            self.spr.scale_y = self.size[1]


        if self.isDead == False:
            pass


        self.cam = cam
        super().draw()

    def phys(self):
        super().phys()
        if self.pos[0]<0:
            self.pos[0] = 0
        if self.pos[1]<0:
            self.pos[1] = 0

        if self.pos[0]>100*70-200:
            self.pos[0] = 100*70-200
        if self.pos[1]>100*70-200:
            self.pos[1] = 100*70-200

    def colis(self, map):
        super().colis(map)

