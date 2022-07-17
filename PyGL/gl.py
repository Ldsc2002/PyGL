from PyGL.utils import *
from random import randint

global windowSize

class gl(object):
    def init(this):
        this.windowSize = [None, None]
        this.imageSize = [None, None]
        this.offset = [None, None]
        this.pixels = [[None]]

        this.backgroundColor = color(0, 0, 0) # Default background is black
        this.cursorColor = color(255, 255, 255) # Default color is white

    def createWindow(this, newWidth, newHeight):
        # Creates window and fills window with simulated static
        this.windowSize = [newWidth, newHeight]
        this.pixels = [[color(randint(0, 255), randint(0, 255), randint(0, 255)) for x in range(this.windowSize[0])] for y in range(this.windowSize[1])] 

    def viewPort(this, x, y, width, height):
        # Creates viewport with given dimensions and offset from center
        offsetX = int((this.windowSize[0] - width) / 2)
        offsetY = int((this.windowSize[1] - height) / 2)

        offsetX = offsetX + (offsetX * x)
        offsetY = offsetY + (offsetY * y)

        this.offset = [offsetX, offsetY]
        this.imageSize = [width, height]

        for x in range (0, this.imageSize[0]):
            for y in range (0, this.imageSize[1]):
                this.pixels[x + offsetX][y + offsetY] = this.backgroundColor

    def clear(this):
        # Clears the viewport 
        for x in range (0, this.imageSize[0]):
            for y in range (0, this.imageSize[1]):
                this.pixels[x + this.offset[0]][y + this.offset[1]] = this.backgroundColor

    def clearColor(this, r, g, b):
        # Changes the background color
        this.backgroundColor = color(int(r * 255), int(g * 255), int(b * 255))

    def vertex(this, x, y):
        # Draws a pixel at the given coordinates
        offsetX = int(this.imageSize[0] / 2)
        offsetY = int(this.imageSize[1] / 2)

        x = offsetX + int(offsetX * x) + this.offset[0]
        y = offsetY + int(offsetY * y) + this.offset[1]

        this.pixels[x][y] = this.cursorColor

    def color(this, r, g, b):
        # Changes the cursor color
        this.cursorColor = color(int(r * 255), int(g * 255), int(b * 255))

    def finish(this):
        # Prints the pixels to the screen
        f = open('out.bmp', 'bw')

        # File header (14 bytes)
        f.write(char('B'))
        f.write(char('M'))
        f.write(doubleword(14 + 40 + this.windowSize[0] * this.windowSize[1] * 3))
        f.write(doubleword(0))
        f.write(doubleword(14 + 40))

        # Image header (40 bytes)
        f.write(doubleword(40))
        f.write(doubleword(this.windowSize[0]))
        f.write(doubleword(this.windowSize[1]))
        f.write(word(1))
        f.write(word(24))
        f.write(doubleword(0))
        f.write(doubleword(this.windowSize[0] * this.windowSize[1] * 3))
        f.write(doubleword(0))
        f.write(doubleword(0))
        f.write(doubleword(0))
        f.write(doubleword(0))

        for x in range (0, this.windowSize[0]):
            for y in range (0, this.windowSize[1]):
                f.write(this.pixels[x][y])

        f.close()