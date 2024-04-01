class Camera:
    def __init__(self, pos, zoom, resolution):
        self.pos = pos
        self.zoom = zoom
        self.var1 = 0.5
        self.resolution = resolution
        self.speedMag = 15
    def on(self):
        self.var1 = self.zoom / 2
        if self.var1 == 0:
            self.var1 = 0.01
    def go(self, pos):
        self.pos = [pos[0]-self.resolution[0]*self.var1, pos[1]-self.resolution[1]*self.var1]

    def set(self, window):
        window.view = window.view.from_translation((int(-self.pos[0] / self.zoom), int(-self.pos[1] / self.zoom), 0))
        window.view = window.view.scale((1 / self.zoom, 1 / self.zoom, 1))

    def center(self, pos):
        posTo = [pos[0]-self.zoom*(self.resolution[0]/2),
                pos[1]-self.zoom*(self.resolution[1]/2)]
        self.pos[0] -= (self.pos[0] - posTo[0]) / self.speedMag
        self.pos[1] -= (self.pos[1] - posTo[1]) / self.speedMag