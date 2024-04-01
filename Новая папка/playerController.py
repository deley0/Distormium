from package.conf import *
from package.gui import PlayerHud
class PlayerController:
    def __init__(self, players, cam):
        self.selectPlayer = 0
        self.players = players
        self.playerHud = PlayerHud(cam, len(players), self.getHps())
    def getHps(self):
        hps = []
        for i in range(len(self.players)):
            hps.append(self.players[i].hp/self.players[i].maxHp)
        return hps
    def control(self, symbol):
        self.players[self.selectPlayer].control(symbol)

    def phys(self):
        for player in self.players: player.phys()
        if self.selectPlayer > len(self.players)-1:
            self.selectPlayer = len(self.players)-1
        if self.selectPlayer <0:
            self.selectPlayer = 0
    def ai(self, t, map):
        for i in range(1, len(self.players)):
            if i != self.selectPlayer:
                self.players[i].ai(t, map, tuple(pixToTail(self.getSelectPlayer().pos)))
    def colis(self, map):
        for player in self.players: player.colis(map)

    def getSelectPlayer(self):
        return self.players[self.selectPlayer]
    def draw(self, cam, zoom):
        for player in self.players: player.draw(cam, zoom)
        self.playerHud.draw()