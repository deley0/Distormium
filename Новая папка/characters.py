from math import *
from random import randint
from numpy import asarray, linalg, array
from PIL import Image
from pyglet.gl import GL_LINEAR

from package.conf import *
from pyglet.window import key
from package.dijkstra import *

from package.player import Player

def finb(str, text):
    if str.find(text) != -1:
        return True

class Char1(Player):

    def __init__(self, pos, size, textures ={"default": None}):
        super().__init__(pos, size, textures ={"default": pyglet.image.load(f"res/pl.png")})
        self.target = pos.copy()
    def cond(self, text):
        return finb(self.condition, text)
    def draw(self, cam, zoom):
        super().draw(cam, zoom)

    def phys(self):
        super().phys()

    def colis(self, map):
        super().colis(map)

    def up(self):
        super().up()

    def down(self):
        super().down()

    def right(self):
        super().right()

    def left(self):
        super().left()

    def ai(self, t, map, cel):

        if self.pos[0]>self.target[0]:
            self.velocity[0]-=0.15
        if self.pos[0]<self.target[0]:
            self.velocity[0]+=0.15
        if self.pos[1]>self.target[1]:
            self.velocity[1]-=0.15
        if self.pos[1]<self.target[1]:
            self.velocity[1]+=0.15
        if t%60 == 0:
            mat = map.matrix.copy()

            vec1 = pixToTail(self.pos)
            vec2 = vec1.copy()
            pVec1 = vec1.copy()
            pVec2 = vec2.copy()
            vec1[0] -= 25
            vec1[1] -= 25
            vec2[0] += 25
            vec2[1] += 25

            mapSize = [len(mat), len(mat[0])] # когда то error

            vec1 = limitCam(vec1, mapSize)
            vec2 = limitCam(vec2, mapSize)

            frame = [row[vec1[1]:vec2[1]] for row in mat[vec1[0]:vec2[0]]]

            frameSize = [len(frame), len(frame[0])]

            newFrame = []
            for x in range(frameSize[0]):
                    newFrame.append([-1] * frameSize[1])
            for x in range(frameSize[0]):
                for y in range(frameSize[1]):
                    if type(frame[x][y]) == int:
                        frame[x][y] = [frame[x][y]]
                    for i in range(len(frame[x][y])):
                        if map.simpleTiles[frame[x][y][i]].solid == True:
                            newFrame[x][y] = 9
                            #print("popa")
                            break
                        if i == len(frame[x][y]) - 1: # когда то error
                            newFrame[x][y] = 0
            #print(vec1, vec2)
            #print(frameSize)
            a = tuple(pixToTail(self.pos))
            b = cel
            print(vec1, vec2)
            a = (a[0], a[1])
            b = (b[0], b[1])
            newFrame2 = []
            for i in range(len(newFrame[0])):
                newFrame2.append([0]*len(newFrame))
            for x in range(len(newFrame2)):
                for y in range(len(newFrame2[0])):
                    newFrame2[x][y] = newFrame[y][x]
            print(vec1[0] - vec2[0], 1)
            ret = pathSearch(a, b, newFrame2)
            print(vec1[0] - vec2[0], 1)
            print(pVec1[0]-vec1[0], 1)
            print(pVec2[0]-vec2[0], 2)

            try:
                print(ret)
                self.target = [ret[len(ret)-2][0]*100+vec1[0], ret[len(ret)-2][1]*100+vec1[1]]
            except: pass



    def control(self, symbol):

        if symbol == key.W:
            self.up()

        if symbol == key.S:
            self.down()

        if symbol == key.A:
            self.left()

        if symbol == key.D:
            self.right()

