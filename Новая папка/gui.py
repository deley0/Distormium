import pyglet.sprite
from pyglet.window import key
import os
from package.load import savePick
import stat
soundSelect = pyglet.media.load('res/audio/select.mp3')

class PlayerHud:
    def __init__(self, cam, numPl, hps):
        pass
        self.batch = pyglet.graphics.Batch()
        self.cam = cam
        self.div = 1/numPl
        self.sp = []
        self.numPl = numPl
        self.hps = hps

    def toHudX(self, var):
        return self.cam.pos[0] + (self.cam.resolution[0] * self.cam.zoom) * var

    def toHudY(self, var):
        return self.cam.pos[1] + (self.cam.resolution[1] * self.cam.zoom) * var

    def toHudSize(self, var):
        return var * self.cam.zoom

    def draw(self):
        for i in range(self.numPl):

            pyglet.shapes.Rectangle(self.toHudX(i * self.div + 0.05), self.toHudY(1 - 0.1),
                                    self.toHudSize(self.div * self.cam.resolution[0] - self.cam.resolution[0] * 0.1),
                                    50, color=(40, 40, 40)).draw()
            var = self.cam.resolution[1]/100
            pyglet.shapes.Rectangle(self.toHudX(i*self.div+0.05)+var,self.toHudY( 1-0.1)+var, self.toHudSize(self.div*self.cam.resolution[0]-self.cam.resolution[0]*0.1)*self.hps[i]-var*2, 50-var*2, color=(200,100,100)).draw()

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
        pyglet.shapes.BorderedRectangle(self.toHudX(1) - 100 * zoom-5, self.toHudY(0)-5,
                                        100 * zoom+10, 100 * zoom*(len(tiles))+10, color=(60,60,60),
                                        border_color=(150, 150, 150, 255), border=10).draw()
        try:
            for i in range(len(tiles)):
                self.sprites.append(pyglet.sprite.Sprite(self.tileSet[tiles[i]].texture,    self.toHudX(1)-100*zoom,    self.toHudY(0)+100*zoom*(i), batch=self.batch))
                self.sprites[-1].scale_x = 1 / 32* 100 * zoom
                self.sprites[-1].scale_y = 1 / 32 * 100 * zoom


            self.batch.draw()
            pyglet.shapes.BorderedRectangle(self.toHudX(1)-100*zoom,    self.toHudY(0)+100*zoom*(layer), 100*zoom, 100*zoom,
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
        endFlag = False
        i = 0
        for y in range(5):
            if endFlag:
                break
            for x in range(10):
                if i == len(tileSet):
                    endFlag = True
                    break
                self.sprites.append(pyglet.sprite.Sprite(tileSet[i].texture,    self.toHudX(x * 0.1),    self.toHudY(0.9 - y * 0.1)  , batch=self.batch))


                i += 1

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

        self.spCurs = pyglet.sprite.Sprite(self.tileSet[self.selectTile].texture,    self.toHudX(1)-100*zoom,    self.toHudY(0), batch=self.batch)
        self.spCurs.scale_x = 1 / 32* 100 * zoom
        self.spCurs.scale_y = 1 / 32 * 100 * zoom

        for i in range(len(self.sprites)):
            y = i//10
            x = i % 10
            self.sprites[i].position = (self.toHudX(x * 0.1), self.toHudY(0.9 - y * 0.1), 0)
            self.sprites[i].scale_x = 1 / 32 * (self.resolution[1] * self.zoom) * 0.1
            self.sprites[i].scale_y = 1 / 32 * (self.resolution[1] * self.zoom) * 0.1

        self.batch.draw()
        pyglet.shapes.BorderedRectangle(self.toHudX(1) - 100*zoom, self.toHudY(0), 100*zoom, 100*zoom,
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




