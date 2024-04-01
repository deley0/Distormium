from test.support import interpreters
from threading import Thread

import pyglet.graphics

cod = """

for i in range(10000000000000):
    pass

"""

version = "0.1"

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
from colorama import init as colorama_init
from colorama import Back,  Fore
from colorama import Style
from pypresence import Presence
import time

start = int(time.time())
client_id = "1224296426432102442" #your application's client id
RPC = Presence(client_id)
RPC.connect()


RPC.update(
    large_image = "distormium", #name of your asset
    large_text = "distormium",
    details = "The game is in development.",
    state = "testing",
    start = start
)


colorama_init(autoreset=True)

def quadDist(pos1, pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

pyglet.image.Texture.default_min_filter = GL_NEAREST
pyglet.image.Texture.default_mag_filter = GL_NEAREST

config = pyglet.gl.Config(double_buffer=True)
window = pyglet.window.Window(900,900, "Distormium", config=config, resizable=True)

icon = pyglet.image.load('res/icon.ico')
window.set_icon(icon)

limitFps = False
window.set_vsync(limitFps)


fps_display = pyglet.window.FPSDisplay(window=window, color=(70, 255, 70, 255), samples=10)
zoomText = pyglet.text.Label(color=(70, 255, 70, 255))






numFire = 0

#playerController.getSelectPlayer().hp
players = [Player([200, 200], [1/32*100,1/32*100])]
players[0].hp = 100
for i in range(0):
    players.append(Char1([randint(0,1000), randint(0,1000)], [1/32*100,1/32*100]))
cam = Camera([0,0], 1, resolution, window)

playerController = PlayerController(players, cam, window)
dia = DialogWin(cam)



selectLayer = 0


tileSet = newLoadTileSet()

loadMap = "testPlace"
map = [Map(loadMap)]
#13, 26
#map[0].matrix = np.load("save.npy", allow_pickle=True)
#np.save("maps/test/grid.npy", map[0].matrix, allow_pickle=True)
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



tilesMenu = TilesMenu(cam, cam.zoom, resolution, tileSet, f"maps\\{loadMap}")
layerMenu = LayerMenu(cam, cam.zoom, resolution, tileSet)
fade = Fade(255)
fade.set(0, 100)
tick = 0



def console():
    while True:
        comand = input()
        if comand.split(" ")[0] != "createMap":
            try:
                exec(f"{comand}")
            except Exception as e:
                print(f"{Fore.RED}{e}")
        else:
            splited = comand.split(" ")
            name = splited[1]
            sizeX = int(splited[2])
            sizeY = int(splited[3])
            map[0].create2(name, sizeX, sizeY)


consoleThread = Thread(target=console, args=[])
consoleThread.start()

def sizeUpdate():
    dia.sizeUpdate()
    tilesMenu.sizeUpdate()



@window.event
def on_key_release(symbol, modifiers):
    playerController.controlRel(symbol)

@window.event
def on_key_press(symbol, modifiers):
    global menu, dia, map, selectLayer, playerController, mouseX, mouseY

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
        dia.textProcess = 0

    if symbol == key.TAB and menu == False:
        menu = True
        soundMenu.play()
    elif symbol == key.TAB and menu == True:
        menu = False
        soundMenu.play()
    playerController.controlPress(symbol) ##########

    if symbol == key.Q:
        cam.zoom-=0.1
        cam.pos[0]+= abs(resolution[0]*(cam.zoom+0.1)-resolution[0]*cam.zoom)/2
        cam.pos[1] += abs(resolution[1] * (cam.zoom + 0.1) - resolution[1] * cam.zoom)/2
        soundZoom1.play()
        if cam.zoom<0.1:
            cam.zoom = 0.1

    if symbol == key.E:
        cam.zoom+=0.1
        cam.pos[0] -= abs(resolution[0] * (cam.zoom + 0.1) - resolution[0] * cam.zoom) / 2
        cam.pos[1] -= abs(resolution[1] * (cam.zoom + 0.1) - resolution[1] * cam.zoom) / 2
        soundZoom2.play()



    if menu:
        tilesMenu.keyboard(symbol)
    else:
        if symbol == key.DELETE:
            var1 = pixToTail([mouseX * cam.zoom + cam.pos[0] - 50, mouseY * cam.zoom + cam.pos[1] - 50])
            map[0].matrix[var1[0]][var1[1]] = map[0].matrix[var1[0]][var1[1]][:len(map[0].matrix[var1[0]][var1[1]])-1]
            del map[0].spriteTiles[var1[0], var1[1]]

    if symbol == key.Z:
        mapPencil.undo(map)

mouseX = 0
mouseY = 0
mousePress = False

canPaint = True
@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouseTiles, mouseX, mouseY, canPaint
    var1 = pixToTail([x * cam.zoom + cam.pos[0] - 50, y * cam.zoom + cam.pos[1] - 50])
    mouseTiles = map[0].matrix[var1[0]][var1[1]]
    mouseX = x
    mouseY = y
    #print(var1[1], var1[0])
    if var1[1] > 12 or var1[0] > 25:
        canPaint = True
    else:
        canPaint = False


@window.event
def on_mouse_release(x, y, button, modifiers):
    global mousePress
    mousePress = False

@window.event
def on_mouse_press(x, y, button, modifiers):
    global map, cam, select, goSelect, selectTile, tilesMenu, mouseX, mouseY, mousePress, canPaint
    mousePress = True
    var1 = pixToTail([x * cam.zoom + cam.pos[0] - 50, y * cam.zoom + cam.pos[1] - 50])
    if var1[1] > 12 or var1[0] > 25:
        canPaint = True
    else:
        canPaint = False

    if not menu:
        if canPaint:
            mapPencil.startPaint()
            mapPencil.paint(x, y, map, cam.zoom, cam.pos, selectLayer)

    if menu:
        v = tilesMenu.control(x, y)
        if v != -1:
            mapPencil.selectTile = v






@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    global zoom, map, cam, selectTile, menu, selectLayer
    var1 = pixToTail([x * cam.zoom + cam.pos[0] - 50, y * cam.zoom + cam.pos[1] - 50])
    if var1[1] > 12 or var1[0] > 25:
        canPaint = True
    else:
        canPaint = False

    if not menu:

        if canPaint:
            mapPencil.paint(x, y, map, cam.zoom, cam.pos, selectLayer)
            soundSet.play()

def update(dt):
    #print(dt)
    playerController.phys(dt)
    fade.on(dt)
    playerController.playerHud.update(playerController.players)
    playerController.movement(dt)
    playerController.colis(map[0], dt)
    pos = playerController.getSelectPlayer().pos
    cam.center(pos, dt)
catTex = pyglet.image.load('res/cat.png')
cat = pyglet.sprite.Sprite(catTex, 200, 1100)
catPos = list(cat.position)
catPos[0] += 48
catPos[1] += 48
catPos = [catPos[0], catPos[1]]
cat.scale_x = 3
cat.scale_y = 3

canCat = False
hpDr = True

depressed_img = pyglet.image.load('res\pl.png')

batch = pyglet.graphics.Batch()

def ab():
    print(13)

#frame = pyglet.gui.Frame(window, order=4)
#pushbutton = pyglet.gui.PushButton(0,0, pressed = void, depressed=depressed_img, batch=batch)
#pushbutton2 = pyglet.gui.PushButton(0+20,0, pressed = void, depressed=depressed_img, batch=batch)
#ent = pyglet.gui.TextEntry("text\nfds", 100, 100, 200, color=(255, 255, 255, 255), text_color=(0, 0, 0, 255), caret_color=(0, 0, 0, 255), batch=batch, group=None)
#frame.add_widget(ent)
#frame.add_widget(pushbutton2)
#push_label = pyglet.text.Label("Push Button: False", x=300, y=300, batch=batch, color=(0, 0, 0, 255))

#pushbutton.aabb = (100,100,100+50,100+50)
#window.push_handlers(pushbutton)
#pushbutton.set_handler('on_press', ab)
pResolution = [0,0]

@window.event
def on_draw():

    global zoom, map, cam, menu, select, goSelect, selectTile, tick, selectLayer, mouseTiles, mouseX, mouseY, canPaint, canCat, hpDr, pResolution



    #print(catPos, playerController.getSelectPlayer().pos)

    if dist(catPos, [playerController.getSelectPlayer().pos[0]+50, playerController.getSelectPlayer().pos[1]+50])<150:
        canCat = True
    else:
        canCat = False

    tick+=1
    if tick%100==0:
        np.save(f"maps/{loadMap}/grid.npy", map[0].matrix, allow_pickle=True)

    window.clear()

    cam.begin()

    v = int(70+cos(tick/10)*33)
    pyglet.shapes.Rectangle(0,0, 69 *100, 69 *100, color=(v,v,v,255)).draw()

    playerController.ai(tick, map[0])




    map[0].draw(cam.pos, cam.zoom)

    pResolution = cam.resolution.copy()
    resolution[0] = window.width
    resolution[1] = window.height
    if cam.resolution[0] != pResolution[0] or cam.resolution[1] != pResolution[1]:
        sizeUpdate()

    try:
        fps_display.label.position = (0, 0, 0)
        pass
    except:
        pass




    zoomText.position = ([resolution[0]-200, resolution[1]-(resolution[1])/7,0])
    zoomText.font_size = 30
    zoomText.text = f"zoom: {cam.zoom:.2f}"


    cat.draw()










    playerController.draw(cam, cam.zoom, mouseX, mouseY, mousePress, hpDr)
    cam.end()

    playerController.drawGui(cam, cam.zoom, mouseX, mouseY, mousePress, hpDr)
    fps_display.draw()
    fade.draw(cam)
    zoomText.draw()
    batch.draw()

    if canCat:
        dia.draw(cam.pos, cam.resolution, cam.zoom)
    else:
        dia.textProcess = 0

    if canPaint:
        if menu:
            tilesMenu.draw(cam.zoom)
            hpDr = False
        else:
            layerMenu.draw(cam.zoom, mouseTiles, selectLayer)
            hpDr = True
    else:
        hpDr = True

if limitFps:
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run(interval=1 / 60)
else:
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run(interval=1 / 600000)
