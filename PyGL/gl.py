from PyGL.utils import *
from random import randint

class gl(object):
    def init(this):
        this.windowSize = [None, None]
        this.imageSize = [None, None]
        this.offset = [None, None]
        this.pixels = [[None]]

        this.backgroundColor = color(0, 0, 0) # Default background is black
        this.cursorColor = color(255, 255, 255) # Default color is white

    def createWindow(this, newWidth, newHeight):
        if not (newWidth > 0) or not (newHeight > 0):
            raise Exception('Window size must be greater than 0')

        # Creates window and fills window with simulated static
        this.windowSize = [newWidth, newHeight]
        this.pixels = [[color(randint(0, 255), randint(0, 255), randint(0, 255)) for x in range(this.windowSize[0])] for y in range(this.windowSize[1])] 

    def viewPort(this, x, y, width, height):
        if not (-1 <= x <= 1) or not (-1 <= y <= 1):
            raise Exception('Viewport offset must be between -1 and 1 (inclusive)')

        if (width > this.windowSize[0]) or (height > this.windowSize[1]):
            raise Exception('Viewport size must be less than or equal to window size')

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
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('Color value must be between 0 and 1 (inclusive)')

        # Changes the background color
        this.backgroundColor = color(int(r * 255), int(g * 255), int(b * 255))

    def vertex(this, x, y):
        if not (-1 <= x <= 1) or not (-1 <= y <= 1):
            raise Exception('Vertex offset must be between -1 and 1 (inclusive)')

        # Draws a pixel at the given coordinates
        offsetX = (this.imageSize[0] / 2)
        offsetY = (this.imageSize[1] / 2)

        x = int(offsetX + (offsetX * x) + this.offset[0])
        y = int(offsetY + (offsetY * y) + this.offset[1])

        this.pixels[y][x] = this.cursorColor

    def color(this, r, g, b):
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('Color value must be between 0 and 1 (inclusive)')

        # Changes the cursor color
        this.cursorColor = color(int(r * 255), int(g * 255), int(b * 255))

    def line(this, x1, y1, x2, y2):
        if not (-1 <= x1 <= 1) or not (-1 <= y1 <= 1) or not (-1 <= x2 <= 1) or not (-1 <= y2 <= 1):
            raise Exception('Line offset must be between -1 and 1 (inclusive)')

        x1 = int(x1 * this.imageSize[0] / 2)
        y1 = int(y1 * this.imageSize[1] / 2)
        x2 = int(x2 * this.imageSize[0] / 2)
        y2 = int(y2 * this.imageSize[1] / 2)

        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
    
        offset = 0
        threshold = dx

        steep = dy > dx
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

            dy = abs(y2 - y1)
            dx = abs(x2 - x1)

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1 

        y = y1

        for x in range(x1, x2 + 1):
            if steep:
                gl.vertex(this, y / (this.imageSize[1] / 2), x /(this.imageSize[0] / 2))
            else:
                gl.vertex(this, x / (this.imageSize[0] / 2), y /(this.imageSize[1] / 2))
            
            offset += dy
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx


    def poligon(this, poligon):
        with open(poligon) as f:
            lines = f.read().splitlines()

            for i in range(len(lines)):
                x1, y1 = lines[i % len(lines)].split(', ')
                x2, y2 = lines[(i + 1) % len(lines)].split(', ')

                x1 = float(x1)
                y1 = float(y1)
                x2 = float(x2)
                y2 = float(y2)

                this.line((x1 / (this.imageSize[0] / 2)), (y1 / (this.imageSize[1] / 2)), (x2 / (this.imageSize[0] / 2)), (y2 / (this.imageSize[1] / 2)))

    def fill(this, poligon):
        fill = []
        poligonY = []
        poligonX = []

        with open(poligon) as f:
            lines = f.read().splitlines()
            
            for i in range(len(lines)):
                x1, y1 = lines[i % len(lines)].split(', ')
                poligonY.append(int(y1))
                poligonX.append(int(x1))
        
        xmin, ymin, xmax, ymax = min(poligonX), min(poligonY), max(poligonX), max(poligonY)
        
        offsetX = (this.imageSize[0] / 2)
        offsetY = (this.imageSize[1] / 2)

        for y in range(ymin, ymax + 1):
            y = int(offsetY + (y) + this.offset[1])

            for x in range(xmin, xmax + 1):
                x = int(offsetX + (x) + this.offset[0])

                if this.pixels[y][x] == this.cursorColor and this.pixels[y][x - 1] != this.cursorColor and this.pixels[y][x - 2] != this.cursorColor:
                    fill.append(x)

            if len(fill) > 1:
                if len(fill) % 2 == 0:
                    for i in range(0, len(fill) - 1, 2):
                        for num in range(fill[i], fill[i + 1]):
                            this.pixels[y][num] = this.cursorColor
                else:
                    for i in range(len(fill) - 1):
                        for num in range(fill[i], fill[i + 1]):
                            this.pixels[y][num] = this.cursorColor
                fill = []


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