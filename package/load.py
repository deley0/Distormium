
import pyglet
from package.conf import tileParam, void
import os
import pickle

class Tile():
    def __init__(self, texture=void, empty=False):
        self.name = ""
        self.texture = texture
        self.solid = False
        self.empty = empty
        self.friction = 1.05
        self.rotation = 0
        self.damage = 0
def paramToTile(tile, param):
    tile.solid = param["solid"]
    tile.friction = param["friction"]
    tile.name = param["name"]
    tile.rotation = param["rotation"]
    tile.damage = int(param["damage"])
    #print("rot", param["rotation"])

def parsTilesId():
    file = open("res/tilesId.txt", "r")
    lines = file.read()
    file.close()

    lines = lines.replace(" ", "")
    lines = lines.split("\n")
    return emptyToVoid(lines)

def emptyToVoid(lines):
    i = 0
    while i<len(lines):
        if lines[i] == "":
            lines.pop(i)
            i-=1
        i+=1
    return lines




def addNewTilesToCfg(newTiles):
    file = open("res/tilesId.txt", "r")
    text = file.read()
    file.close()

    file = open("res/tilesId.txt", "w")
    file.write(text)
    for i in range(len(newTiles)):
        file.write("\n" + str(newTiles[i][0]) + "," + newTiles[i][1])
    file.close()



def loadTilesFromKfg(tileSet, workTiles, workTilesInt):
    for i in range(len(tileSet)):
        for i2 in range(len(workTiles)):
            if workTilesInt[i2] == i:
                tileSet[i] = loadTile(workTiles[i2])
                pass
    return tileSet

def addNewTilesToCfgOnEmpty(tileSet, listOfLoadingTile):
    newTiles = []

    i2 = 0

    for i in range(len(tileSet)):
        if i2 == len(listOfLoadingTile):
            break
        if tileSet[i].empty == True:
            newTiles.append([i, listOfLoadingTile[i2]])

            tileSet[i] = loadTile(listOfLoadingTile[i2])

            listOfLoadingTile[i2] = ""
            i2 += 1
    return newTiles, listOfLoadingTile

def addNewTiles(listOfLoadingTile, newTiles, tileSet):

    for i in range(len(listOfLoadingTile)):
        newTiles.append([len(tileSet), listOfLoadingTile[i]])
        tileSet.append(loadTile(listOfLoadingTile[i]))
def loadTileSet():
    lines = parsTilesId()  # парсим TilesId.txt
    
    listOfLoadingTile = os.listdir("res/tiles")  # Загружаем список тайлов в папке tiles

    workTiles, workTilesInt = getWorkTiles(lines, listOfLoadingTile)  # Проверяем тайлы которые и в TilesId.txt и в /tiles/

    tileSet = createEmptyTileSet(workTilesInt)  # Создаём пустой tileSet

    tileSet = loadTilesFromKfg(tileSet, workTiles, workTilesInt)  # Загружаем тайлы по TilesId.txt

    newTiles, listOfLoadingTile = addNewTilesToCfgOnEmpty(tileSet, listOfLoadingTile)  # Добавление в пустые тайлы новых
    addNewTiles(listOfLoadingTile, newTiles, tileSet)  # Добавление через append

    addNewTilesToCfg(newTiles)  # Добавление в TilesId.txt новых тайлов

    return tileSet


def loadPick(path):
    with open(path+'/tilesId.pickle', 'rb') as handle:
        b = pickle.load(handle)
    return b

def savePick(path, a):
    with open(path+'/tilesId.pickle', 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

def getWorkTiles(tilesId):
    existTiles = os.listdir("res\\tiles")
    res = []
    for i in tilesId:
        for i2 in existTiles:
            if i == i2:
                res.append(i)
    return res

def loadTile(name):
    tile = Tile(pyglet.image.load(f"res/tiles/{name}/image.png"))

    param = tileParam(f"res/tiles/{name}")
    paramToTile(tile, param)
    return tile


def createEmptyTileSet(workTilesInt):
    workTilesInt = list(workTilesInt)
    for i in range(len(workTilesInt)):
        workTilesInt[i] = int(workTilesInt[i][1])
    var = max(workTilesInt) + 1

    tileSet = [Tile(empty=True)] * var
    tileSet[0] = Tile()

    return tileSet

def getNotWorkTiles(workTiles, listDir):
    res = []
    for i in range(len(listDir)):
        for i2 in range(len(workTiles)):
            if listDir[i] == workTiles[i2]:
                break
            if i2 == len(workTiles)-1:
                res.append(listDir[i])
    return res

def newLoadTileSet(pathToMap = "maps\\test"):

    res = []

    listDir = os.listdir(pathToMap)
    listDirTiles = os.listdir("res/tiles/")
    existFlag = False
    for i in range(len(listDir)):
        if listDir[i] == "tilesId.pickle":
            existFlag = True
            break
    if existFlag:
        tilesId = loadPick(f"{pathToMap}")

        workTiles = getWorkTiles(tilesId)
        items = tilesId.items()
        res = createEmptyTileSet(items)
        #print(tilesId)
        for i in tilesId:

            if i != "":
                try:
                    res[tilesId[i]] = loadTile(i.split("/")[-1])
                except: pass
        forAdd = getNotWorkTiles(workTiles, listDirTiles)

        numAdd = len(forAdd)
        #print("forAdd", forAdd)
        for i in range(1, len(res)):
            if len(forAdd) == 0:
                break
            if res[i].empty:
                res[i] = loadTile(forAdd[0])
                numAdd -=1
                forAdd.pop(0)

        for i in range(len(forAdd)):
            res.append(loadTile(forAdd[i]))
    else:
        res.append(Tile())
        for i in listDirTiles:
            res.append(loadTile(i))
    forSave = dict()
    for i in range(len(res)):
        forSave[res[i].name] = i

    savePick(pathToMap, forSave)
    return res