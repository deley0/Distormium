from PIL import ImageFont, ImageDraw, Image
import pyglet
font = ImageFont.truetype("arial", 36)

class DialogWin:
    def __init__(self):
        self.size = [300,100]
        self.pos = [0.1,0.1]
        self.openProcess = 20
        self.textProcess = 0
        self.text = "1 234 56  78 9 12345 67 89 1 23456 789 1 234 567 89 12 34 678 9"
        self.plim = 0
        self.text1 = ""
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


        return lines
    def draw(self, cam, resolution, zoom):
        #def toHudX(var):
        #    return cam[0] + (resolution[0] * zoom) * var
#
        #def toHudY(var):
        #    return cam[1] + (resolution[1] * zoom) * var
#
        #def toHudSize(var):
        #    return var * zoom
#
#
        #v = self.text[0:int(self.textProcess)]
        #s = self.get_text_dimensions(self.text[0:int(self.textProcess)], font)[0]
#
        #pyglet.shapes.Rectangle(toHudX(0.1)+s, toHudY(0)+10,10,10).draw()
#
        #self.openProcess-=1
        #if self.openProcess > 20:
        #    self.openProcess = 20
        #if self.openProcess < 1:
        #    self.openProcess = 1
        #if self.openProcess==1:
        #    self.textProcess +=0.4
        #if self.textProcess > len(self.text):
        #    self.textProcess = len(self.text)
#
#
#
#
        #var = resolution[0] / 100
        #wid = 10/self.openProcess
        #var2 = abs((resolution[1] / 5+wid*2)/self.openProcess - (resolution[1] / 5+wid*2))
#
#
        #lim = (var * 80+wid*2)*self.openProcess-170
        ##print(lim)
        #pyglet.shapes.Rectangle((toHudX(self.pos[0])-wid)-var2, toHudY(self.pos[1])-wid, (var * 80+wid*2)*self.openProcess, (resolution[1] / 5+wid*2)/self.openProcess, color=(255,255,255,255)).draw()
#
        #pyglet.shapes.Rectangle((toHudX(self.pos[0]))-var2, toHudY(self.pos[1]), var*80*self.openProcess, (resolution[1] / 5)/self.openProcess, color=(0,0,0,255)).draw()
        #fontName = "Arial"
        #fontSize = 36
        #if self.plim != lim:
        #    self.text1 = self.trans(self.text, lim)
        #    #print("PID")
        #self.plim = lim
#
        #for i in range(5):
#
        #    #print(text)
        #    text = self.text1
        #    text = text[0][0:int(self.textProcess)]
        #    text = text.split("\n")
        #    if i == len(text):
        #        break
#
        #    var = 36*i
        #    pyglet.text.Label(text[i], font_name=fontName, font_size=fontSize, x=int((toHudX(self.pos[0])) - var2), y=-var + int(toHudY(self.pos[1]) + (resolution[1] / 5) / self.openProcess), anchor_x='left', anchor_y='top').draw()
        pass
