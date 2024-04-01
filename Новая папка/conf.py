import pyglet
#global void
void = pyglet.image.load('res/texture/void.png')

resolution = [900, 900]
def pixToTail(pos):
    return [int((pos[0] + 50) / 100),int((pos[1] + 50) / 100)]

def tileParam(pathToConf):
    config = dict()
    config["solid"] = False
    config["friction"] = 1.05
    config["name"] = pathToConf.split("/")[-1]
    file = open(f"{pathToConf}/params.txt", "r")
    lines = file.readlines()
    file.close()
    try:
        for line in lines:
            line = line.replace(" ", "").split("#")[0]
            if line.find("=") != -1:
                div = line.split("=")
                if line.find(",") != -1:
                    var = div[1].replace("\n", "").split(",")
                    for i in range(len(var)):
                        var[i] = int(var[i])
                    config[div[0]] = var
                else:
                    config[div[0]] = div[1]
        for i in config:
            config[i] = str(config[i]).replace("\n", "").replace(" ", "")
            if config[i] == "True":
                config[i] = True
            elif config[i] == "False":
                config[i] = False
            elif config[i].find(".") != -1:
                config[i] = float(config[i])
                print(2)
            else:
                config[i] = int(config[i])
                print(3)
    except:
        a, b, c, d, e, f, g, h, i = "w" + "s" * 7, " " * 10 + "w" + " " * 17 + "w\n", "w" + " " * 37 + "w \n", 13, 12, 11, 17, 31, 35
        s = ((
                     " " * d + "s" * d + "\n" + " " * e + "d" + " " * 6 + "w" + " " * 6 + "a " + "\n" + " " * f + "w" + " " * 7 + "w" + " " * 7 + "w" + "\n" + " " * f + a * 2 + "w\n" + b * 8 + " " * 5 +
                     "s" * 5 + "d" + " " * g + "\\" + "s" * 5 + "\n" + " " * 3 + "d" + " " * h + "a \n" + " d" + " " * i + "a \n" + c * 3 + " \\" + " " * i + "d" + "\n" + " " * 3 + "\\" + "s" * h + "d")
             .replace("s", "_").replace("w", "|").replace("d", "/").replace("a", "\\"))
        print(s)
    return config
def limitCam(vec, size):
    if vec[0]<0:
        vec[0] = 0
    if vec[1]<0:
        vec[1] = 0
    if vec[0]>size[0]-1:
        vec[0] = size[0]-1
    if vec[1]>size[1]-1:
        vec[1] = size[1]-1
    return vec