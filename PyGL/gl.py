from sympy import product
from PyGL.utils import *
from PyGL.obj import obj
from PyGL.texture import texture
from random import randint

class gl(object):
    def __init__(this):
        this.windowSize = [None, None]
        this.imageSize = [None, None]
        this.offset = [None, None]
        this.pixels = []
        this.zbuffer = []
        this.light = V3(0, 0, 1)
        this.model = None
        this.viewMatrix = None
        this.projectionMatrix = None
        this.viewPortMatrix = None

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
                bufferRow.append(-float('inf'))

            this.pixels.append(row)
            this.zbuffer.append(bufferRow)

    def viewPort(this, offsetX, offsetY, width, height):
        if (width > this.windowSize[0]) or (height > this.windowSize[1]):
            raise Exception('Viewport size must be less than or equal to window size')

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
                this.zbuffer[y][x] = -float('inf')

    def clearColor(this, r, g, b):
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('Color value must be between 0 and 1 (inclusive)')

        # Changes the background color
        this.backgroundColor = color(int(r * 255), int(g * 255), int(b * 255))

    def vertex(this, x, y):
        x = int(x + this.offset[0])
        y = int(y + this.offset[1])

        if (x > 0 and y > 0):
            this.pixels[y][x] = this.cursorColor

    def setLight(this, x, y, z):
        this.light = V3(x, y, z)

    def color(this, r, g, b):
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('Color value must be between 0 and 1 (inclusive)')

        # Changes the cursor color
        this.cursorColor = color(int(r * 255), int(g * 255), int(b * 255))

    def line(this, x1, y1, x2, y2):
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
    
        offset = 0
        threshold = dx

        steep = False
        if dy > dx:
            steep = True
            x1, y1 = y1, x1
            x2, y2 = y2, x2

            dy = abs(y2 - y1)
            dx = abs(x2 - x1)

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1 

        y = y1

        for x in range(x1, x2):
            if steep:
                gl.vertex(this, y, x)
            else:
                gl.vertex(this, x, y)
            
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

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

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

    def loadMatrix(this, translate = (0, 0, 0), scale = (1, 1, 1), rotate = (0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)
        
        translateMatrix = [
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1]
        ]

        scaleMatrix = [
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ]

        rotateXMatrix = [
            [1, 0, 0, 0],
            [0, cos(rotate.x), -sin(rotate.x), 0],
            [0, sin(rotate.x), cos(rotate.x), 0],
            [0, 0, 0, 1]
        ]

        rotateYMatrix = [
            [cos(rotate.y), 0, sin(rotate.y), 0],
            [0, 1, 0, 0],
            [-sin(rotate.y), 0, cos(rotate.y), 0],
            [0, 0, 0, 1]
        ]

        rotateZMatrix = [
            [cos(rotate.z), -sin(rotate.z), 0, 0],
            [sin(rotate.z), cos(rotate.z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        rotateMatrix = productMatrix(productMatrix(rotateXMatrix, rotateYMatrix), rotateZMatrix)
        this.model = productMatrix(productMatrix(translateMatrix, scaleMatrix), rotateMatrix)

    def load(this, filename, translate = (0, 0, 0), scale = (1, 1, 1), rotate = (0, 0, 0), texture = None):
        model = obj(filename)
        this.loadMatrix(translate, scale, rotate)
        
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

                a = this.transform(model.vertices[f1])
                b = this.transform(model.vertices[f2])
                c = this.transform(model.vertices[f3])

                normal = norm (cross(sub(b, a), sub(c, a)))
                intensity = dot(normal, this.light)

                if not texture:
                    colorIntensity = round(255 * intensity)

                    if colorIntensity < 0:
                        colorIntensity = 0

                    this.triangle(a, b, c, color(colorIntensity, colorIntensity, colorIntensity))
                else:
                    t1 = face[0][1] - 1
                    t2 = face[1][1] - 1
                    t3 = face[2][1] - 1
                    tA = V3(*model.tvertices[t1])
                    tB = V3(*model.tvertices[t2])
                    tC = V3(*model.tvertices[t3])

                    this.triangle(a, b, c, None, texture, (tA, tB, tC), intensity)

            elif count == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                vertices = [
                    this.transform(model.vertices[f1]),
                    this.transform(model.vertices[f2]),
                    this.transform(model.vertices[f3]),
                    this.transform(model.vertices[f4])
                ]

                normal = norm (cross(sub(vertices[1], vertices[0]), sub(vertices[2], vertices[0])))
                intensity = dot(normal, this.light)
                
                A, B, C, D = vertices

                if not texture:
                    colorIntensity = round(255 * intensity)
                    if colorIntensity < 0:
                        colorIntensity = 0

                    this.triangle(A, B, C, color(colorIntensity, colorIntensity, colorIntensity))
                    this.triangle(A, C, D, color(colorIntensity, colorIntensity, colorIntensity))            
                else:
                    t1 = face[0][1] - 1
                    t2 = face[1][1] - 1
                    t3 = face[2][1] - 1
                    t4 = face[3][1] - 1
                    
                    tA = V3(*model.tvertices[t1])
                    tB = V3(*model.tvertices[t2])
                    tC = V3(*model.tvertices[t3])
                    tD = V3(*model.tvertices[t4])
                    
                    this.triangle(A, B, C, None, texture, (tA, tB, tC), intensity)
                    this.triangle(A, C, D, None, texture, (tA, tC, tD), intensity)


    def triangle(this, A, B, C, color = None, texture = None, position = None, intensity = 1):
        xmin, xmax, ymin, ymax = bbox(A, B, C)
        xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)

        for y in range(ymin, ymax + 1):
            for x in range(xmin, xmax + 1):
                P = V2(x, y)
                w, v, u = barycentric(A, B, C, P)
                
                if w < 0 or v < 0 or u < 0:
                    continue
        
                if texture:
                    tA, tB, tC = position
                    tx = tA.x * w + tB.x * v + tC.x * u
                    ty = tA.y * w + tB.y * v + tC.y * u
                    
                    color = texture.getColor(tx, ty, intensity)
                
                z = A.z * w + B.z * v + C.z * u

                if y < len(this.zbuffer) - 1 and x < len(this.zbuffer[0]) - 1 and x >= 0 and y >= 0:
                    if z > this.zbuffer[y][x]:
                        this.cursorColor = color
                        this.vertex(x, y)

                        this.zbuffer[y + this.offset[1]][x + this.offset[0]] = z
    
    def transform(this, vertex):
        augmentedVertex = V4(vertex[0], vertex[1], vertex[2], 1)

        res1 = productMatrixVector(this.model, augmentedVertex)
        res2 = productMatrixVector(this.viewMatrix, res1)
        res3 = productMatrixVector(this.projectionMatrix, res2)
        transformedVertex = productMatrixVector(this.viewPortMatrix, res3)

        transformedVertex = V4(*transformedVertex)

        return V3(
            transformedVertex.x / transformedVertex.w,
            transformedVertex.y / transformedVertex.w,
            transformedVertex.z / transformedVertex.w
        )

    def lookAt(this, eye, center, up):
        eye = V3(*eye)
        center = V3(*center)
        up = V3(*up)

        z = norm(sub(eye, center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))

        this.loadProjectionMatrix(eye, center)
        this.loadViewMatrix(x, y, z, center)
        this.loadViewPortMatrix()

    def loadViewMatrix(this, x, y, z, center):
        inverse = [
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1]
        ]

        primeO = [
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]
        ]
        
        this.viewMatrix = productMatrix(inverse, primeO)

    def loadProjectionMatrix(this, eye, center):
        c = -1 / length(sub(eye, center))
        
        this.projectionMatrix = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, c, 1]
        ]

    def loadViewPortMatrix(this):
        w = len(this.pixels)
        h = len(this.pixels[0])

        this.viewPortMatrix = [
            [w / 2, 0, 0, w / 2],
            [0, h / 2, 0, h / 2],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ]

    def finish(this, name):
        writeBMP(this.pixels, name)

    def showZbuffer(this, name):
        zbuffer = []
        zmax = max(max(this.zbuffer))

        # Convert zbuffer to color values
        for y in range (0, this.windowSize[1]):
            bufferRow = []
            for x in range (0, this.windowSize[0]):
                if (this.zbuffer[y][x] == -float('inf')):
                    z = 0
                else:
                    z = int((this.zbuffer[y][x] / zmax) * 255)

                # Shouldn't be necessary, but it's here just in case
                if z > 255: 
                    z = 255

                if z < 0:
                    z = 0

                bufferRow.append(color(z, z, z))
            zbuffer.append(bufferRow)

        writeBMP(zbuffer, 'zbuffer_' + name)