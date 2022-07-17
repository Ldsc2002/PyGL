from PyGL.utils import *

global window

class gl(object):
    def init(this):
        this.window = [None, None]
        this.viewport = [None, None, None, None]
        this.pixels = [[None]]

        this.backgroundColor = color(0, 0, 0)
        this.cursorColor = color(255, 255, 255)      


    def createWindow(this, newWidth, newHeight):
        this.window = [newWidth, newHeight]

    def viewPort(this, x, y, width, height):
        this.viewport = [x, y, width, height]
        this.pixels = [[this.backgroundColor for x in range(this.viewport[2])] for y in range(this.viewport[3])] 

    def clear(this):
        this.pixels = [[this.backgroundColor for x in range(this.viewport[2])] for y in range(this.viewport[3])] 

    def clearColor(this, r, g, b):
        this.backgroundColor = color(int(r * 255), int(g * 255), int(b * 255))

    def vertex(this, x, y):
        offsetX = int(this.viewport[2] / 2)
        offsetY = int(this.viewport[3] / 2)

        x = offsetX + int(offsetX * x)
        y = offsetY + int(offsetY * y)

        this.pixels[x][y] = this.cursorColor

    def color(this, r, g, b):
        this.cursorColor = color(int(r * 255), int(g * 255), int(b * 255))

    def finish(this):
        f = open('out.bmp', 'bw')

        # File header (14 bytes)
        f.write(char('B'))
        f.write(char('M'))
        f.write(doubleword(14 + 40 + this.window[0] * this.window[1] * 3))
        f.write(doubleword(0))
        f.write(doubleword(14 + 40))

        # Image header (40 bytes)
        f.write(doubleword(40))
        f.write(doubleword(this.window[0]))
        f.write(doubleword(this.window[1]))
        f.write(word(1))
        f.write(word(24))
        f.write(doubleword(0))
        f.write(doubleword(this.window[0] * this.window[1] * 3))
        f.write(doubleword(0))
        f.write(doubleword(0))
        f.write(doubleword(0))
        f.write(doubleword(0))

        offsetX = int((this.window[0] - this.viewport[2]) / 2)
        offsetY = int((this.window[1] - this.viewport[3]) / 2)

        offsetX = offsetX + (offsetX * this.viewport[0])
        offsetY = offsetY + (offsetY * this.viewport[1])

        image = [[color(255, 255, 255) for x in range(this.window[0])] for y in range(this.window[1])] 

        for x in range (0, this.viewport[2]):
            for y in range (0, this.viewport[3]):
                image[x + offsetX][y + offsetY] = this.pixels[x][y]

        for x in range (0, this.window[0]):
            for y in range (0, this.window[1]):
                f.write(image[x][y])

        f.close()