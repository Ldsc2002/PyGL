from PyGL.utils import *
from PyGL.obj import obj
from random import randint

class gl(object):
    def init(this):
        this.windowSize = [None, None]
        this.imageSize = [None, None]
        this.offset = [None, None]
        this.pixels = []
        this.zbuffer = []

        this.backgroundColor = color(0, 0, 0) # Default background is black
        this.cursorColor = color(255, 255, 255) # Default color is white

    def createWindow(this, newWidth, newHeight):
        if not (newWidth > 0) or not (newHeight > 0):
            raise Exception('Window size must be greater than 0')

        # Creates window and fills window with simulated static
        this.windowSize = [newWidth, newHeight]
        this.pixels = []
        this.zbuffer = []

        for y in range (0, this.windowSize[1]):
            row = []
            bufferRow = []

            for x in range (0, this.windowSize[0]):
                row.append(color(randint(0, 255), randint(0, 255), randint(0, 255)))
                bufferRow.append(0)

            this.pixels.append(row)
            this.zbuffer.append(bufferRow)

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
                this.pixels[y + offsetY][x + offsetX] = this.backgroundColor

    def clear(this):
        # Clears the viewport 
        for x in range (0, this.imageSize[0]):
            for y in range (0, this.imageSize[1]):
                this.pixels[y + this.offset[1]][x + this.offset[0]] = this.backgroundColor

        for x in range (0, this.imageSize[0]):
            for y in range (0, this.imageSize[1]):
                this.zbuffer[y][x] = 0

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

    def absoluteVertex(this, x, y):
        # Draws a pixel at the given coordinates
        offsetX = (this.imageSize[0] / 2)
        offsetY = (this.imageSize[1] / 2)

        x = int(offsetX + x + this.offset[0])
        y = int(offsetY + y + this.offset[1])

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

        dy, dx = abs(y2 - y1), abs(x2 - x1)
    
        offset = 0
        threshold = dx

        steep = False
        if dy > dx:
            steep = True
            x1, y1 = y1, x1
            x2, y2 = y2, x2

            dy, dx = abs(y2 - y1), abs(x2 - x1)

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
        f = open(poligon)
        lines = f.read().splitlines()

        for i in range(len(lines)):
            x1, y1 = lines[i % len(lines)].split(', ')
            x2, y2 = lines[(i + 1) % len(lines)].split(', ')

            x1 = (float(x1) - this.imageSize[0] / 2) / (this.imageSize[0] / 2)
            y1 = (float(y1) - this.imageSize[1] / 2) / (this.imageSize[1] / 2)
            x2 = (float(x2) - this.imageSize[0] / 2) / (this.imageSize[0] / 2)
            y2 = (float(y2) - this.imageSize[1] / 2) / (this.imageSize[1] / 2)

            this.line(x1, y1, x2, y2)

    def fill(this, poligon):
        fill = []
        poligonY = []
        poligonX = []

        f = open(poligon)
        lines = f.read().splitlines()
        
        for i in range(len(lines)):
            x1, y1 = lines[i % len(lines)].split(', ')
            poligonY.append(int(y1))
            poligonX.append(int(x1))
        
        xmin, ymin, xmax, ymax = min(poligonX), min(poligonY), max(poligonX), max(poligonY)

        for y in range(ymin, ymax + 1):
            y = int((y) + this.offset[1])

            for x in range(xmin, xmax + 1):
                x = int((x) + this.offset[0])

                if this.pixels[y][x] == this.cursorColor and this.pixels[y][x - 1] != this.cursorColor:
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

    def load(this, filename, translate, scale):
        model = obj(filename)

        light = V3(0,0,1)
        
        for face in model.faces:
            count = len(face)

            if count == 2: 
                for j in range(count):
                    f1 = face[j][0]
                    f2 = face[(j + 1) % count][0]

                    v1 = model.vertices[f1 - 1]
                    v2 = model.vertices[f2 - 1]
                    
                    x1 = (v1[0] + translate[0]) * scale[0]
                    y1 = (v1[1] + translate[1]) * scale[1]
                    x2 = (v2[0] + translate[0]) * scale[0]
                    y2 = (v2[1] + translate[1]) * scale[1]

                    this.line(x1, y1, x2, y2)

            elif count == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                a = this.transform(model.vertices[f1], translate, scale)
                b = this.transform(model.vertices[f2], translate, scale)
                c = this.transform(model.vertices[f3], translate, scale)

                normal = norm (cross(sub(b, a), sub(c, a)))
                intensity = dot(normal, light)
                colorTransparency = round(255 * intensity)

                if intensity < 0:
                    colorTransparency = 0

                this.triangle(a, b, c, color(colorTransparency, colorTransparency, colorTransparency))

            elif count == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                vertices = [
                    this.transform(model.vertices[f1], translate, scale),
                    this.transform(model.vertices[f2], translate, scale),
                    this.transform(model.vertices[f3], translate, scale),
                    this.transform(model.vertices[f4], translate, scale)
                ]

                normal = norm (cross(sub(vertices[1], vertices[0]), sub(vertices[2], vertices[0])))
                intensity = dot(normal, light)

                colorTransparency = round(255 * intensity)

                if colorTransparency < 0:
                    colorTransparency = 0
                
                A, B, C, D = vertices

                this.triangle(A, B, C, color(colorTransparency, colorTransparency, colorTransparency))
                this.triangle(A, C, D, color(colorTransparency, colorTransparency, colorTransparency))


    def triangle(this, A, B, C, color = None):
        xmin, xmax, ymin, ymax = bbox(A, B, C)

        for y in range(ymin, ymax + 1):
            for x in range(xmin, xmax + 1):
                P = V2(x, y)
                w, v, u = barycentric(A, B, C, P)
                
                if w < 0 or v < 0 or u < 0:
                    continue
                
                z = A.z * w + B.z * v + C.z * u

                if z > this.zbuffer[y][x]:
                    this.cursorColor = color
                    this.absoluteVertex(x, y)

                    this.zbuffer[y][x] = z
    
    def transform(self, vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
        return V3(
            round((vertex[0] + translate[0]) * scale[0]),
            round((vertex[1] + translate[1]) * scale[1]),
            round((vertex[2] + translate[2]) * scale[2])
    )

    def finish(this, name):
        # Prints the pixels to the screen
        name  = name + '.bmp'
        f = open(name, 'bw')

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

        for y in range (0, this.windowSize[1]):
            for x in range (0, this.windowSize[0]):
                f.write(this.pixels[y][x])

        f.close()
        print('Image saved as ' + name)

    def showZbuffer(this):
        # Prints the pixels to the screen
        f = open('zbuffer.bmp', 'bw')

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

        zmax = max(max(this.zbuffer))

        offsetX = int(this.imageSize[0] / 2) + this.offset[0]
        offsetY = int(this.imageSize[1] / 2) + this.offset[1]

        for y in range (0, this.windowSize[1]):
            for x in range (0, this.windowSize[0]):
                z = int((this.zbuffer[y - offsetY][x - offsetX] / zmax) * 255)

                if z > 255:
                    z = 255

                toWrite = color(z, z, z)

                f.write(toWrite)

        f.close()