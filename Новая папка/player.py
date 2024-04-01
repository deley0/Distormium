from math import *
from random import randint
from numpy import asarray, linalg, array
from PIL import Image
from pyglet.gl import GL_LINEAR

from package.conf import *
from pyglet.window import key
source = pyglet.media.load('res/audio/step.mp3', streaming=False)
def layer(img1, img2):
    numpydata1 = asarray(img1.image).copy()
    numpydata2 = asarray(img2.image).copy()
    for x in range(len(numpydata1)):
        for y in range(len(numpydata1[0])):
            if numpydata2[x][y][3]>200:
                numpydata1[x][y][0]=numpydata2[x][y][0]
                numpydata1[x][y][1] = numpydata2[x][y][1]
                numpydata1[x][y][2] = numpydata2[x][y][2]
    return Image.fromarray(numpydata1.astype('uint8'), 'RGBA')

def finb(str, text):
    if str.find(text) != -1:
        return True


from package.entity import Entity
class Player(Entity):

    def __init__(self, pos, size, textures ={"default": None}):
        super().__init__(pos, size, textures ={"default": pyglet.image.load(f"res/pl.png")})
        self.speed = 3*3
        self.maxHp = 100
        self.hp = 100
        #self.hud = PlayerHud(self.batc)
        self.cam = [0,0]
        self.pVelocity = [self.velocity[0], self.velocity[1]]

        self.upProgress = 0
    def cond(self, text):
        return finb(self.condition, text)
    def draw(self, cam, zoom):
        self.cam = cam
        super().draw()

    def phys(self):
        super().phys()

    def colis(self, map):
        super().colis(map)

    def up(self):
        self.velocity[1] += self.speed

    def down(self):
       self.velocity[1] -= self.speed

    def right(self):
        self.velocity[0] += self.speed

    def left(self):
        self.velocity[0] -= self.speed

    def control(self, symbol):

        if symbol == key.W:
            self.up()
            source.play()

        if symbol == key.S:
            self.down()
            source.play()

        if symbol == key.A:
            self.left()
            source.play()

        if symbol == key.D:
            self.right()
            source.play()
