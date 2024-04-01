from math import *
from random import randint

import pyglet.shapes
from numpy import asarray
from PIL import Image
from package.conf import *
from pyglet.window import key



class Entity:
    def __init__(self,pos, size, textures ={"default": None}):
        global void
        if textures["default"] == None:
            textures["default"] = void

        self.colisSize = 50
        self.pos = pos
        self.size = size
        self.velocity = [0,0]
        self.hp = 100
        self.textures = textures
        self.batc = pyglet.graphics.Batch()

        self.friction = 1.05
        self.isDead = False

        self.spr = pyglet.sprite.Sprite(self.textures["default"], 0, 0, batch = self.batc)
        self.spr.scale_x = self.size[0]
        self.spr.scale_y = self.size[1]
        self.damageProgress = 0
    def draw(self):
        if self.hp <= 0:
            self.isDead = True
        self.spr.position = [self.pos[0], self.pos[1], 0]
        self.batc.draw()
        #pyglet.shapes.Circle(self.pos[0]+self.colisSize, self.pos[1]+self.colisSize, self.colisSize, color=(255, 255, 255, 255)).draw()
    def phys(self, dt):


        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt
        #print(self.friction, dt)
        #print(self.friction * dt)
        self.velocity[0] /= (self.friction-1)*dt+1
        self.velocity[1] /= (self.friction-1)*dt+1


        if self.velocity[0]<0.1 and self.velocity[0]> -0.1:
            self.velocity[0] = 0
        if self.velocity[1]<0.1 and self.velocity[1]> -0.1:
            self.velocity[1] = 0

    def colis(self, map, dt):
        var = pixToTail(self.pos)
        try:
            self.friction = map.simpleTiles[map.matrix[var[0]][var[1]][0]].friction
            if self.damageProgress <= 0:
                # print(type(map.simpleTiles[map.matrix[rayTile[0], rayTile[1]][i2]].damage))
                # print(map.simpleTiles[map.matrix[rayTile[0], rayTile[1]][i2]].damage)
                if map.simpleTiles[map.matrix[var[0]][var[1]][1]].damage > 0:
                    self.hp -= map.simpleTiles[map.matrix[var[0]][var[1]][1]].damage
                    self.damageProgress = 0.5

        except:
            pass
        if self.damageProgress >= 0:
            self.damageProgress -= 1*dt


        numRays = 50
        step = (pi*2)/10
        sizeRay = self.colisSize
        endFlag = True
        while endFlag:
            for i in range(numRays):
                ray = [self.pos[0]+cos(step*i)*sizeRay,self.pos[1]+sin(step*i)*sizeRay]
                rayTile = pixToTail(ray)
                rayTile = limitCam(rayTile, map.size)


                endFlag = False
                for i2 in range(len(map.matrix[rayTile[0], rayTile[1]])):
                    if map.simpleTiles[map.matrix[rayTile[0], rayTile[1]][i2]].solid == True:
                        self.pos[0] -= cos(step * i) * 1
                        self.pos[1] -= sin(step * i) * 1
                        #self.velocity[0] -= cos(step * i) * abs(self.velocity[0])/100
                        #self.velocity[1] -= sin(step * i) * abs(self.velocity[1])/100
                        endFlag = True



