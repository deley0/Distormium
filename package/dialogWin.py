from PIL import ImageFont, ImageDraw, Image
import pyglet
font = ImageFont.truetype("arial", 36)

class DialogWin:
    def __init__(self, cam):
        self.size = [300,100]
        self.pos = [0.1,0.1]
        self.openProcess = 0
        self.textProcess = 0
        self.t = 0
        self.text = "GEGWEK{{GP G_)3038-0)#GIK 3i-0i3-3 t2=WEK{{GPG_)3i -0i3-i-0i3-90t23- t-0i3-038-0)3 i-0i3-3t2=WEK s{{GPG_)3-0i3-90t23-ti- 0i3-i-#GIK30=- )@#t3=i-0i3-90t23-t2"
        self.plim = 0
        self.fontSize = 36

        self.cam = cam

        self.pad = 50
        self.padMini = 10
        self.posX = self.pad
        self.sizeX = cam.resolution[0] - self.pad * 2
        self.sizeY = cam.resolution[1] / 4

        self.label = pyglet.text.Label("",
                                  font_name='Times New Roman',
                                  font_size=self.fontSize,
                                  x=self.posX + self.padMini, y=self.sizeY - self.fontSize - self.padMini,
                                  multiline=True, width=self.sizeX - self.padMini)
    def get_text_dimensions(self, text_string, font):
        if text_string != "":
            ascent, descent = font.getmetrics()
            text_string = text_string.replace(" ", "W")
            text_width = font.getmask(text_string).getbbox()[2]
            text_height = font.getmask(text_string).getbbox()[3] + descent

            return (text_width, text_height)
        else:
            return (0, 0)

    def trans(self, text, max_text_length):
        words = text.split(" ")
        enter = 0
        newText = ""
        extreme = max_text_length
        for word in words:
            line = newText.split("\n")
            if self.get_text_dimensions(line[len(line) - 1] + word, font)[0] > extreme:
                newText = newText + "\n"
                enter += 1
            newText = newText + " " + word
        return (newText, enter)

    def toHudX(self, var,cam, resolution, zoom):
        return cam[0] + (resolution[0] * zoom) * var
    def toHudY(self, var, cam, resolution, zoom):
        return cam[1] + (resolution[1] * zoom) * var
    def toHudSize(self, var,  zoom):
        return var * zoom


        return lines
    def sizeUpdate(self):
        self.sizeX = self.cam.resolution[0] - self.pad * 2
        self.sizeY = self.cam.resolution[1] / 4
        self.label.x = self.posX + self.padMini
        self.label.y = self.sizeY - self.fontSize - self.padMini
        self.label.width = self.sizeX - self.padMini

    def draw(self, cam, resolution, zoom):


        self.openProcess-=1
        if self.openProcess > 20:
            self.openProcess = 20
        if self.openProcess < 1:
            self.openProcess = 1

        if self.openProcess==1:
            self.textProcess +=0.4
        if self.textProcess > len(self.text):
            self.textProcess = len(self.text)



        pyglet.shapes.Rectangle(self.posX, 0, self.sizeX, self.sizeY, color=(255, 255, 255, 255)).draw()
        pyglet.shapes.Rectangle(self.posX+self.padMini, 0+self.padMini, self.sizeX-self.padMini*2, self.sizeY-self.padMini*2, color=(0, 0, 0, 255)).draw()
        newText = self.text[:int(self.textProcess)]
        self.label.text = newText


        self.label.draw()
