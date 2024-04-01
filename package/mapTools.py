from package.conf import *

class MapPencil():
    def __init__(self):
        self.selectTile = 0
        self.action = []
    def startPaint(self):
        self.action.append(dict())
    def paint(self, x, y, map, zoom, cam, layer):
        print(1, layer)
        var1 = pixToTail([x * zoom + cam[0] - 50, y * zoom + cam[1] - 50])
        if len(map[0].matrix[var1[0], var1[1]])-1<layer:
            newTile = map[0].matrix[var1[0], var1[1]]
            newTile.append(self.selectTile)

            self.action[-1][var1[0], var1[1]] = map[0].matrix[var1[0], var1[1]]
            map[0].matrix[var1[0], var1[1]] = newTile
            del map[0].spriteTiles[var1[0], var1[1]]
        elif map[0].matrix[var1[0], var1[1]][layer] != self.selectTile:
            newTile = map[0].matrix[var1[0], var1[1]]
            newTile[layer] = self.selectTile

            self.action[-1][var1[0], var1[1]] = map[0].matrix[var1[0], var1[1]]
            map[0].matrix[var1[0], var1[1]] = newTile
            del map[0].spriteTiles[var1[0], var1[1]]

    def undo(self, map):
        print(self.action)
        action = self.action[len(self.action)-1]
        for i in action:
            try:
                map[0].matrix[i[0]][i[1]] = action[i]
                print("gg", i,  action[i][0], action[i])
                del map[0].spriteTiles[i]
            except: pass
        self.action.pop(len(action)-1)
        print(self.action)
