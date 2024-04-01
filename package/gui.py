import pyglet.sprite
from pyglet.window import key
import os
from package.load import savePick
import stat
from math import dist
soundSelect = pyglet.media.load('res/audio/select.mp3')
from random import randint
def fadeNormal(progress, target, speed, dt):
    if progress < target:
        progress += speed * dt
    else:
        progress -= speed * dt
    if dist([progress], [target]) <= speed * dt:
        progress = target
    return progress

class Fade:
    def __init__(self, start):
        self.batc = pyglet.graphics.Batch()
        texture = pyglet.image.load("res/gui/fade.png")
        self.sp = pyglet.sprite.Sprite(texture, 0, 0, batch=self.batc)
        self.progress = start
        self.func = "normal"
        self.speed = 50
        self.target = 0

    def on(self, dt):
        match self.func:
            case "normal":
                self.progress = fadeNormal(self.progress, self.target, self.speed, dt)

    def set(self, target, speed):
        self.target = target
        self.speed = speed

    def draw(self, cam):
        self.sp.scale_x = 1 / 800 * cam.resolution[0]
        self.sp.scale_y = 1 / 600 * cam.resolution[1]
        self.sp.opacity = self.progress
        self.sp.draw()


class PlayerHud:
    def __init__(self, cam, numPl, hps, window):
        pass
        self.batch = pyglet.graphics.Batch()
        self.cam = cam
        self.div = 1/numPl
        self.sp = []
        self.numPl = numPl
        self.hps = hps
        self.window = window
        self.texGameOver = pyglet.image.load(f"res/gui/gameOvers/winGameOver1.png")
        self.texBut = pyglet.image.load(f"res/gui/butReborn.png")
        self.batch = pyglet.graphics.Batch()
        self.spGameOver = pyglet.sprite.Sprite(self.texGameOver, 0, 0)
        #self.spBut = pyglet.sprite.Sprite(self.texBut, 0, 0)
        self.pushbutton = pyglet.gui.PushButton(0, 0, pressed=self.texBut, depressed=self.texBut, batch=self.batch)
        self.pIsGameOver = False
    def update(self, players):
        for i in range(len(players)):
            self.hps[i] = players[i].hp
    def toHudX(self, var):
        return self.cam.pos[0] + (self.cam.resolution[0] * self.cam.zoom) * var

    def toHudY(self, var):
        return self.cam.pos[1] + (self.cam.resolution[1] * self.cam.zoom) * var

    def toHudX2(self, var):
        return (self.cam.resolution[0] * self.cam.zoom) * var

    def toHudY2(self, var):
        return (self.cam.resolution[1] * self.cam.zoom) * var

    def toHudSizeX(self, var):
        return (self.cam.resolution[0] * self.cam.zoom) * var
    def kostili(self, var):
        size = self.toHudSize(self.div * self.cam.resolution[0] - self.cam.resolution[0] * 0.1)-18
        return (size * self.cam.zoom) * var
    def toHudSize(self, var):
        return var * self.cam.zoom

    def on_hint(self, x, y, butX, butY, butSizeX , butSizeY):

        if butX < x < (butX + butSizeX) and butY < y < (butY + butSizeY):

            return True

        else:

            return False



    def draw(self, isGameOver, x, y, mousePress, player, restart):
        if isGameOver != self.pIsGameOver:
            rand = randint(1,4)
            self.texGameOver = pyglet.image.load(f"res/gui/gameOvers/winGameOver{rand}.png")
            self.spGameOver = pyglet.sprite.Sprite(self.texGameOver, 0, 0)
        for i in range(self.numPl):

            if self.hps[i] < 0:
                newHps = 0
            else:
                newHps = self.hps[i]/100

            div = self.cam.resolution[0]/self.numPl

            pad = div*0.1
            padSize = 5
            posX = div*i + pad
            posY = self.cam.resolution[1] - 40
            sizeX = div - pad*2
            sizeY = 30
            pyglet.shapes.Rectangle(posX, posY, sizeX, sizeY, color=(40, 40, 40)).draw()
            pyglet.shapes.Rectangle(posX + padSize, posY + padSize, (sizeX - padSize*2) * newHps, sizeY - padSize*2, color=(200,100,100)).draw()
        self.pIsGameOver = isGameOver
        if isGameOver:
            #if self.on_hint(x, y, self.toHudX2(0.5)-254/2, self.toHudY2(0.5)-280/2+30, 254, 68) and mousePress:
            #    player.pos = [200, 200]
            #    return True

            center = [self.cam.resolution[0] / 2, self.cam.resolution[1] / 2]


            self.spGameOver.position = (center[0]-400/2, center[1]-280/2, 0)
            self.spGameOver.draw()

            #pushbutton = pyglet.gui.PushButton(0, 0, pressed=self.texBut, depressed=self.texBut, batch=self.batch)
            self.pushbutton.x = center[0]-254/2
            self.pushbutton.y = center[1]-280/2+30
            #self.spBut.position = (center[0]-254/2, center[1]-280/2+30, 0)
            #self.spBut.draw()
            self.window.push_handlers(self.pushbutton)
            self.pushbutton.set_handler('on_press', restart)

            self.batch.draw()
        return False

class LayerMenu:
    def __init__(self, camPos, zoom, resolution, tileSet):
        self.cam = camPos
        self.zoom = zoom
        self.resolution = resolution
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.tileSet = tileSet
        self.selectTile = 0
        self.selectProc = 255

    def toHudX(self, var):
        return self.cam.pos[0] + (self.resolution[0] * self.zoom) * var

    def toHudY(self, var):
        return self.cam.pos[1] + (self.resolution[1] * self.zoom) * var

    def toHudSize(self, var):
        return var * self.zoom

    def draw(self, zoom, tiles, layer):
        self.zoom = zoom
        self.sprites = []
        #print(tiles)
        pyglet.shapes.BorderedRectangle(self.cam.resolution[0] - 100-10, 0,
                                        100 + 10, 100 * (len(tiles))+10, color=(60,60,60),
                                        border_color=(60,60,60), border=10).draw()
        try:
            for i in range(len(tiles)):
                self.sprites.append(pyglet.sprite.Sprite(self.tileSet[tiles[i]].texture,    self.cam.resolution[0]-100, 100 * (i), batch=self.batch))
                self.sprites[-1].scale_x = 1 / 32 * 100
                self.sprites[-1].scale_y = 1 / 32 * 100


            self.batch.draw()
            pyglet.shapes.BorderedRectangle(self.resolution[0]-100,    100*(layer), 100, 100,
                                            border_color=(100, 100, 255, 100), border=10).draw()

        except: print("error")
        #print("munany", layer)
class TilesMenu:
    def __init__(self, camPos, zoom, resolution, tileSet, pathToMap):
        self.cam = camPos
        self.zoom = zoom
        self.resolution = resolution
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.tileSet = tileSet
        self.selectTile = 0
        self.selectProc = 255
        self.pathToMap = pathToMap
        self.spCurs = pyglet.sprite.Sprite(tileSet[self.selectTile].texture,    self.toHudX(0.5),    self.toHudY(0.5), batch=self.batch)

        self.sizeUpdate()

    def toHudX(self, var):
        return self.cam.pos[0] + (self.resolution[0] * self.zoom) * var

    def toHudY(self, var):
        return self.cam.pos[1] + (self.resolution[1] * self.zoom) * var

    def toHudSize(self, var):
        return var * self.zoom

    def draw(self, zoom):
        self.zoom = zoom
        self.selectProc-=30
        if self.selectProc<0:
            self.selectProc = 0
        self.sizeUpdate()
        self.spCurs = pyglet.sprite.Sprite(self.tileSet[self.selectTile].texture,    self.resolution[0]-100, 0, batch=self.batch)
        self.spCurs.scale_x = 1 / 32 * 100
        self.spCurs.scale_y = 1 / 32 * 100

        #for i in range(len(self.sprites)):
        #    y = i//10
        #    x = i % 10
            #self.sprites[i].position = (self.toHudX(x * 0.1), self.toHudY(0.9 - y * 0.1), 0)
            #self.sprites[i].scale_x = 1 / 32 * (self.resolution[1] * self.zoom) * 0.1
            #self.sprites[i].scale_y = 1 / 32 * (self.resolution[1] * self.zoom) * 0.1

        self.batch.draw()
        pyglet.shapes.BorderedRectangle(self.resolution[0]-100, 0, 100, 100,
                                        border_color=(255, 255, 100, self.selectProc), border=10).draw()
    def control(self, x, y):
        self.selectProc = 255
        select = [int((x) / self.resolution[0] * 10), int((self.resolution[1] - y) / self.resolution[1] * 10)]
        for i in range(len(self.sprites)):
            y = i // 10
            x = i % 10
            if x == select[0] and y == select[1]:
                if i <= len(self.tileSet):
                    self.selectTile = i
                    soundSelect.play()

        return self.selectTile
    def sizeUpdate(self):
        self.sprites = []
        endFlag = False
        i = 0
        for y in range(5):
            if endFlag:
                break
            for x in range(10):
                if i == len(self.tileSet):
                    endFlag = True
                    break
                self.sprites.append(pyglet.sprite.Sprite(self.tileSet[i].texture, x * (self.resolution[0] / 10),
                                                         self.resolution[1] - (1+y) * 100,
                                                         batch=self.batch))
                self.sprites[len(self.sprites)-1].scale_x = 1/32 * self.resolution[1]/10
                self.sprites[len(self.sprites) - 1].scale_y = 1/32 * self.resolution[1]/10

                i += 1
    def keyboard(self, symbol):
        if symbol == key.DELETE:

            listDir = os.listdir("res/tiles")
            for i in range(len(listDir)):
                #print(self.tileSet[self.selectTile].name,  listDir[i])
                if self.tileSet[self.selectTile].name == listDir[i]:
                    #print(f"res/tiles/{self.tileSet[self.selectTile].name}")
                    dirPath = f"res/tiles/{self.tileSet[self.selectTile].name}"
                    #os.chmod(f"res/tiles/{self.tileSet[self.selectTile].name}", stat.S_IWRITE)
                    listDir2 = os.listdir(dirPath)
                    for i2 in range(len(listDir2)):
                        os.remove(dirPath+"/"+listDir2[i2])
                    os.rmdir(dirPath)
                    break

            self.tileSet[self.selectTile] = self.tileSet[0]
            self.tileSet[self.selectTile].empty = True

            forSave = dict()
            for i in range(len(self.tileSet)):
                forSave[self.tileSet[i].name] = i

            savePick(self.pathToMap, forSave)
            self.sprites[self.selectTile] = pyglet.sprite.Sprite(self.tileSet[0].texture,    0,    0  , batch=self.batch)




