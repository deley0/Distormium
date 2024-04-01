from test.support import interpreters

cod = """

for i in range(10000000000000):
    pass

"""
def f():
    interp = interpreters.create()
    interp.run(cod)
#t1 = Thread(target=f)
#t1.start()

from pyglet.gl import *
from package.player import *
from pyglet.window import key
from numpy import asarray
from package.map import *
from package.gui import *
from package.playerController import PlayerController
from package.characters import *
from package.dialogWin import *
from package.conf import *
from package.camera import Camera
from package.load import newLoadTileSet
from package.mapTools import *


def quadDist(pos1, pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

pyglet.image.Texture.default_min_filter = GL_NEAREST
pyglet.image.Texture.default_mag_filter = GL_NEAREST

config = pyglet.gl.Config(double_buffer=True)
window = pyglet.window.Window(900,900, config=config, resizable=True)

limitFps = False
window.set_vsync(limitFps)


fps_display = pyglet.window.FPSDisplay(window=window, color=(70, 255, 70, 255), samples=10)
zoomText = pyglet.text.Label(color=(70, 255, 70, 255))






numFire = 0
dia = DialogWin()

players = [Player([0, 0], [1/32*100,1/32*100]), Char1([0, 0], [1/32*100,1/32*100])]
for i in range(0):
    players.append(Char1([randint(0,1000), randint(0,1000)], [1/32*100,1/32*100]))
cam = Camera([0,0], 1, resolution)
playerController = PlayerController(players, cam)




selectLayer = 0


tileSet = newLoadTileSet()

map = [Map([20,20], tileSet)]

#map[0].matrix = np.load("save.npy", allow_pickle=True)

menu = False

goSelect = False
select = [0, 0]



selectTile = 0

mouseTiles = []


mapPencil = MapPencil()

soundMenu = pyglet.media.load('res/audio/menu.mp3', streaming=False)
soundSet = pyglet.media.load('res/audio/set.mp3')
soundSelectLayer = pyglet.media.load('res/audio/selectLayer.mp3')

soundZoom1 = pyglet.media.load('res/audio/zoom+.mp3')
soundZoom2 = pyglet.media.load('res/audio/zoom-.mp3')



tilesMenu = TilesMenu(cam, cam.zoom, resolution, tileSet, "maps\\test")
layerMenu = LayerMenu(cam, cam.zoom, resolution, tileSet)
tick = 0

@window.event
def on_key_press(symbol, modifiers):
    global menu, dia, map, selectLayer, playerController

    if symbol == key.I:
        playerController.selectPlayer+=1
    if symbol == key.K:
        playerController.selectPlayer-=1
    if playerController.selectPlayer<0:
        playerController.selectPlayer = 0
    if playerController.selectPlayer> len(playerController.players)-1:
        playerController.selectPlayer = len(playerController.players)-1

    if symbol == key.UP:
        selectLayer+=1
        soundSelectLayer.play()
    if symbol == key.DOWN:
        selectLayer -= 1
        soundSelectLayer.play()
    if symbol == key.R:
        dia.openProcess = 20
        dia.textProcess = 0

    if symbol == key.TAB and menu == False:
        menu = True
        soundMenu.play()
    elif symbol == key.TAB and menu == True:
        menu = False
        soundMenu.play()
    playerController.control(symbol)

    if symbol == key.Q:
        cam.zoom-=0.1
        soundZoom1.play()
        if cam.zoom<0.1:
            cam.zoom = 0.1

    if symbol == key.E:
        cam.zoom+=0.1
        soundZoom2.play()

    if menu:
        tilesMenu.keyboard(symbol)

    if symbol == key.Z:
        mapPencil.undo(map)




@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouseTiles
    var1 = pixToTail([x * cam.zoom + cam.pos[0] - 50, y * cam.zoom + cam.pos[1] - 50])
    mouseTiles = map[0].matrix[var1[0]][var1[1]]

@window.event
def on_mouse_release(x, y, button, modifiers):
    pass

@window.event
def on_mouse_press(x, y, button, modifiers):
    global map, cam, select, goSelect, selectTile, tilesMenu

    if not menu:
        mapPencil.startPaint()
        mapPencil.paint(x, y, map, cam.zoom, cam.pos, selectLayer)
    if menu:
        v = tilesMenu.control(x, y)
        if v != -1:
            mapPencil.selectTile = v


@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    global zoom, map, cam, selectTile, menu, selectLayer

    if not menu:
        mapPencil.paint(x, y, map, cam.zoom, cam.pos, selectLayer)
        soundSet.play()



@window.event
def on_draw():
    global zoom, map, cam, menu, select, goSelect, selectTile, tick, selectLayer, mouseTiles


    tick+=1
    if tick%100==0:
        np.save("save", map[0].matrix)
    window.clear()
    v = int(70+cos(tick/10)*33)
    pyglet.shapes.Rectangle(0,0, 100 *100, 100 *100, color=(v,v,v,255)).draw()

    playerController.ai(tick, map[0])

    playerController.phys()
    playerController.colis(map[0])

    map[0].draw(cam.pos, cam.zoom)


    dia.draw(cam.pos, cam.resolution, cam.zoom)

    resolution[0] = window.width
    resolution[1] = window.height
    try:
        fps_display.label.position = ([cam[0]+resolution[0]*cam.zoom-(resolution[0]*cam.zoom)/7, cam[1]+resolution[1]*cam.zoom-(resolution[1]*cam.zoom)/20, 0])
        fps_display.label.font_size = 30*cam.zoom

    except:
        pass




    zoomText.position = ([cam.pos[0]+resolution[0]*cam.zoom-(resolution[0]*cam.zoom)/7, cam.pos[1]+resolution[1]*cam.zoom-(resolution[1]*cam.zoom)/10, 0])
    zoomText.font_size = 30*cam.zoom
    zoomText.text = f"zoom: {cam.zoom:.2f}"

    if menu:
        tilesMenu.draw(cam.zoom)
    else:
        layerMenu.draw(cam.zoom, mouseTiles, selectLayer)

    pos = playerController.getSelectPlayer().pos

    cam.center(pos)
    cam.set(window)
    playerController.draw(cam, cam.zoom)


    fps_display.draw()
    zoomText.draw()




if limitFps:
    pyglet.app.run(interval=1 / 60)
else:
    pyglet.app.run(interval=1 / 60000)
