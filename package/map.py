import os
import numpy as np
import time
from package.conf import *
from math import cos, sin, radians, pi
from package.load import newLoadTileSet
from colorama import init as colorama_init
from colorama import Back,  Fore
from colorama import Style
# createMap testPlace 70 70
class Tile():
    def __init__(self, texture=void, empty=False):
        self.name = ""
        self.texture = texture
        self.solid = False
        self.empty = empty
        self.friction = 1.05
        self.rotation = 0
        self.damage = 0


class Map():
    def __init__(self, name):
        self.pos = [0, 0]

        self.load(name)

        self.sizeTile = [100, 100]
        self.tick = 0

        self.batchNums = 100
        self.batchForTiles = []
        for i in range(self.batchNums):
            self.batchForTiles.append(pyglet.graphics.Batch())
        self.spriteTiles = {}

    def load(self, name):
        error = 0
        try:
            error = 0
            mapPar = mapParam(f"maps/{name}")
            error = 1
            self.size = [mapPar["sizeX"], mapPar["sizeY"]]
            error = 2
            self.matrix = np.load(f"maps/{name}/grid.npy", allow_pickle=True)
            error = 3
            self.simpleTiles = newLoadTileSet(pathToMap=f"maps/{name}")
            print(f"{Fore.GREEN}Карта успешно загружена !!!")
        except:
            message = ""
            match error:
                case 0:
                    message = "Ошибка во время загрузки параметров карты, возможно нету файла 'params.txt' либо путь к карте указан не верно."
                case 1:
                    message = "Ошибка во время загрузки параметров размера карты, возможно параметры отсутствуют."
                case 2:
                    message = "Ошибка во время загрузки сетки карты, её нету или она задана не верно."
                case 3:
                    message = "Ошибка во время загрузки набора тайлов карты, их нету или они заданы не верно."
            print(message)
    def create(self, name):
        mapPar = mapParam(f"maps/{name}")
        self.size = [mapPar["sizeX"], mapPar["sizeY"]]
        self.matrix = np.empty((mapPar["sizeX"], mapPar["sizeY"]), dtype="object")
        self.fill([4])
        self.simpleTiles = newLoadTileSet(pathToMap=f"maps/{name}")

    def create2(self, name, sizeX, sizeY):
        os.mkdir(f"maps/{name}")
        #mapPar = mapParam(f"maps/{name}")
        self.size = [sizeX, sizeY]
        self.matrix = np.empty((sizeX, sizeY), dtype="object")
        self.fill([4])
        self.simpleTiles = newLoadTileSet(pathToMap=f"maps/test")
        np.save(f"maps/{name}/grid.npy", self.matrix, allow_pickle=True)


    def findTile(self, x, y):
        return (x, y) in self.spriteTiles

    def intToTile(self, pos):
        self.matrix[pos[0],pos[1]] = self.simpleTiles[self.matrix[pos[0],pos[1]]]
    #def intToTile(self, pos):
    #    self.matrix[pos[0],pos[1]] = self.simpleTiles[self.matrix[pos[0],pos[1]]]
    def fill(self, tile):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.matrix[x][y] = tile.copy()
                #self.matrix[x][y].append(tile)
                #print(self.matrix[x][y])

    def betwen(self, vec1, vec2, pos):
        if pos[0] > vec1[0] - 10 and pos[0] < vec2[0] + 10 and pos[1] > vec1[1] - 10 and pos[1] < vec2[1] + 10:
            return True
        return False
    def draw(self, cam, zoom):
        timeS1 = time.time()
        def toHudX(var):
            return cam[0] + (resolution[0] * zoom) * var

        def toHudY(var):
            return cam[1] + (resolution[1] * zoom) * var

        def toHudSize(var):
            return var * zoom

        timeE1 = time.time()
        self.tick += 1
        timeS2 = time.time()
        vec1 = [0, 0]
        vec2 = [0, 0]
        camPos = cam
        vec1 = [camPos[0]+200, camPos[1]+200]
        vec2 = [camPos[0]+resolution[0]*zoom, camPos[1]+resolution[1]*zoom]
        vec1 = pixToTail(vec1)
        vec2 = pixToTail(vec2)
        vec1[0] -= 3
        vec1[1] -= 3
        vec2[0] += 3
        vec2[1] += 3###############################################3
        vec1 = limitCam(vec1, self.size)
        vec2 = limitCam(vec2, self.size)
        #for i in self.spriteTiles:
        #    for i2 in range(len(self.spriteTiles[i])):
        #        v = (self.tick+i[0])/10
        #        v1 = (self.tick + i[1]) / 10
        #        self.spriteTiles[i][i2].position = (self.spriteTiles[i][i2].position[0]+cos(v)*30, self.spriteTiles[i][i2].position[1],0)
        #pyglet.sprite.Sprite(image, pos_x, pos_y, batch=self.batchForTiles)
        timeE2 = time.time()
        va = 100 / 32
        for x in range(vec1[0], vec2[0]):
            for y in range(vec1[1], vec2[1]):
                if type(self.matrix[x][y]) == list:
                    if self.findTile(x, y) != True:

                        self.spriteTiles[x, y] = []
                        #print("leh")
                        for i in range(len(self.matrix[x][y])):
                            #pyglet.sprite.Sprite(self.simpleTiles[self.matrix[x][y]].texture, self.pos[0]+x*self.sizeTile[0], self.pos[1]+y*self.sizeTile[1],batch= self.batchForTiles)
                            thisTile = self.simpleTiles[self.matrix[x][y][i]]
                            match thisTile.rotation:
                                case 0:
                                    smeh = [0,0]
                                case 90:
                                    smeh = [0, 100]
                                case 180:
                                    smeh = [100, 100]
                                case 270:
                                    smeh = [100, 0]
                                case 360:
                                    smeh = [0, 0]

                            self.spriteTiles[x, y].append(pyglet.sprite.Sprite(self.simpleTiles[self.matrix[x][y][i]].texture, self.pos[0]+x*self.sizeTile[0], self.pos[1]+y*self.sizeTile[1], self.simpleTiles[self.matrix[x][y][i]].rotation,batch= self.batchForTiles[i]))
                            self.spriteTiles[x, y][i].scale_x = va
                            self.spriteTiles[x, y][i].scale_y = va
                            self.spriteTiles[x, y][i].position = (self.spriteTiles[x, y][i].position[0]+smeh[0], self.spriteTiles[x, y][i].position[1]+smeh[1], 0)
                            self.spriteTiles[x, y][i].rotation = self.simpleTiles[self.matrix[x][y][i]].rotation
                            #print(self.simpleTiles[self.matrix[x][y][i]].name)
                            #self.spriteTiles[x, y].rotation = self.tick*10
                        #self.spriteTiles[x, y].pos = (x, y) # это создаёт попы

        timeS3 = time.time()
        #for i in self.spriteTiles:
        #    if self.betwen(vec1, vec2, self.spriteTiles[i].pos):
        #        pass
        #    else:
        #        del self.spriteTiles[i]

        keys = list(self.spriteTiles.keys())
        values = list(self.spriteTiles.values())
        popi = 0
        i = 0
        while i < len(keys):
            key = keys[i]
            #value = values[i]
            if self.betwen(vec1, vec2, key):
                pass
            else:
                del self.spriteTiles[key]
                popi += 1
            i += 1
        #print("popi = ",popi)
                #else:
                #    var = self.matrix[x][y]
                #    while True:
                #        if type(var) == type(1):
                #            self.simpleTiles[var].texture.blit(self.pos[0] + x * self.sizeTile[0],
                #                                                                   self.pos[1] + y * self.sizeTile[1],
                #                                                                   self.sizeTile[0], self.sizeTile[1])
                #            break
                #        var.texture.blit(self.pos[0]+x*self.sizeTile[0], self.pos[1]+y*self.sizeTile[1], self.sizeTile[0], self.sizeTile[1])
                #        if var.parent != None:
                #            var = var.parent
                #        else:
                #            break
        timeE3 = time.time()
        timeS4 = time.time()
        #self.batchForTiles[1].draw()
        for i in range(self.batchNums):
            self.batchForTiles[i].draw()
        timeE4 = time.time()
        #print(timeE1-timeS1, timeE2-timeS2, timeE3-timeS3, timeE4-timeS4)
