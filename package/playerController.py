from package.conf import *
from package.gui import PlayerHud
class PlayerController:
    def __init__(self, players, cam, window):
        self.selectPlayer = 0
        self.players = players
        self.playerHud = PlayerHud(cam, len(players), self.getHps(), window)
    def getHps(self):
        hps = []
        for i in range(len(self.players)):
            hps.append(self.players[i].hp/self.players[i].maxHp)
        return hps
    def controlPress(self, symbol):
        self.players[self.selectPlayer].controlPress(symbol)
    def controlRel(self, symbol):
        self.players[self.selectPlayer].controlRel(symbol)

    def phys(self, dt):
        for player in self.players: player.phys(dt)
        if self.selectPlayer > len(self.players)-1:
            self.selectPlayer = len(self.players)-1
        if self.selectPlayer <0:
            self.selectPlayer = 0
    def ai(self, t, map):
        for i in range(1, len(self.players)):
            if i != self.selectPlayer:
                self.players[i].ai(t, map, tuple(pixToTail(self.getSelectPlayer().pos)))
    def colis(self, map, dt):
        for player in self.players: player.colis(map, dt)

    def getSelectPlayer(self):
        return self.players[self.selectPlayer]

    def draw(self, cam, zoom, x, y, mousePress, drHp):
        for player in self.players: player.draw(cam, zoom)

    def movement(self, dt):
        for player in self.players: player.movement(dt)
    def restart(self):
        self.getSelectPlayer().pos = [100, 100]
        self.getSelectPlayer().isDead = False
        self.getSelectPlayer().hp = 100

    def drawGui(self, cam, zoom, x, y, mousePress, drHp):
        if drHp:
            self.playerHud.draw(self.getSelectPlayer().isDead, x, y, mousePress, self.getSelectPlayer(), self.restart)
