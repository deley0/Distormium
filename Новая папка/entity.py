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

        self.textures = textures
        self.batc = pyglet.graphics.Batch()

        self.friction = 1.05


        self.spr = pyglet.sprite.Sprite(self.textures["default"], 0, 0, batch = self.batc)
        self.spr.scale_x = self.size[0]
        self.spr.scale_y = self.size[1]

    def draw(self):

        self.spr.position = [self.pos[0], self.pos[1], 0]
        self.batc.draw()
        #pyglet.shapes.Circle(self.pos[0]+self.colisSize, self.pos[1]+self.colisSize, self.colisSize, color=(255, 255, 255, 255)).draw()
    def phys(self):


        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.velocity[0] /= self.friction
        self.velocity[1] /= self.friction


        if self.velocity[0]<0.1 and self.velocity[0]> -0.1:
            self.velocity[0] = 0
        if self.velocity[1]<0.1 and self.velocity[1]> -0.1:
            self.velocity[1] = 0

    def colis(self, map):
        var = pixToTail(self.pos)
        try:
            self.friction = map.simpleTiles[map.matrix[var[0]][var[1]][0]].friction
        except:
            pass

        numRays = 40
        step = (pi*2)/10
        sizeRay = self.colisSize
        for i in range(numRays):
            ray = [self.pos[0]+cos(step*i)*sizeRay,self.pos[1]+sin(step*i)*sizeRay]
            rayTile = pixToTail(ray)
            rayTile = limitCam(rayTile, map.size)
            for i2 in range(len(map.matrix[rayTile[0], rayTile[1]])):
                if map.simpleTiles[map.matrix[rayTile[0], rayTile[1]][i2]].solid == True:
                    self.pos[0] -= cos(step * i) * abs(self.velocity[0])
                    self.pos[1] -= sin(step * i) * abs(self.velocity[1])
                    self.velocity[0] -= cos(step * i) * abs(self.velocity[0])/10
                    self.velocity[1] -= sin(step * i) * abs(self.velocity[1])/10