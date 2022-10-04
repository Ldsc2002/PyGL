from PyGL.utils import *
from PyGL.obj import obj
from PyGL.texture import texture
from random import randint, uniform

BLACK = 0, 0, 0
RED = 255, 0, 0
ORANGE = 255, 165, 0
WHITE = 255, 255, 255
ORANGERED = 255, 67, 20
YELLOW = 255, 255, 0

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
        this.activeShader = None
        this.activeTexture = None
        this.activeNormalMap = None

        this.backgroundColor = color(0, 0, 0) # Default background is black
        this.cursorColor = color(255, 255, 255) # Default color is white

    def setBackground(this, filename):
        this.pixels = filename

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

    def setColor(this, r, g, b):
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

        for x in range(int(x1), int(x2)):
            if steep:
                this.vertex(this, y, x)
            else:
                this.vertex(this, x, y)
            
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

    def load(this, filename, translate = (0, 0, 0), scale = (1, 1, 1), rotate = (0, 0, 0), texture = None, shader = None, normal = None):
        model = obj(filename)
        this.loadMatrix(translate, scale, rotate)
        this.activeShader = shader
        this.activeTexture = texture
        this.activeNormalMap = normal

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

                    tn1 = face[0][2] - 1
                    tn2 = face[1][2] - 1
                    tn3 = face[2][2] - 1

                    try:
                        tnA = V3(*model.nvertices[tn1])
                        tnB = V3(*model.nvertices[tn2])
                        tnC = V3(*model.nvertices[tn3])
                    except:
                        tnA = V3(0, 0, 0)
                        tnB = V3(0, 0, 0)
                        tnC = V3(0, 0, 0)

                    this.triangle(a, b, c, None, texture, (tA, tB, tC), (tnA,tnB,tnC), intensity)

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

                    tn1 = face[0][2] - 1
                    tn2 = face[1][2] - 1
                    tn3 = face[2][2] - 1
                    tn4 = face[3][2] - 1
                    
                    try:
                        tnA = V3(*model.nvertices[tn1])
                        tnB = V3(*model.nvertices[tn2])
                        tnC = V3(*model.nvertices[tn3])
                        tnD = V3(*model.nvertices[tn4])
                    except:
                        tnA = V3(0, 0, 0)
                        tnB = V3(0, 0, 0)
                        tnC = V3(0, 0, 0)
                        tnD = V3(0, 0, 0)
                    
                    this.triangle(A, B, C, None, texture, (tA, tB, tC), (tnA, tnB, tnC), intensity)
                    this.triangle(A, C, D, None, texture, (tA, tC, tD), (tnA, tnC, tnD), intensity)

    def triangle(this, A, B, C, color = None, texture = None, position = (0, 0, 0), normals = (0, 0, 0), intensity = 1):
        xmin, xmax, ymin, ymax = bbox(A, B, C)
        xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)

        for y in range(ymin, ymax + 1):
            for x in range(xmin, xmax + 1):
                P = V2(x, y)
                w, v, u = barycentric(A, B, C, P)
                
                if w < 0 or v < 0 or u < 0:
                    continue
        
                tA, tB, tC = position
                tnA, tnB, tnC = normals
                                    
                z = A.z * w + B.z * v + C.z * u

                if y < len(this.zbuffer) - 1 and x < len(this.zbuffer[0]) - 1 and x >= 0 and y >= 0:
                    if z > this.zbuffer[y][x]:
                        if this.activeShader:
                            this.cursorColor = this.shader((w,u,v), this.light, (tA, tB, tC), (tnA,tnB,tnC), (x,y))
                        elif texture:
                            tx = tA.x * w + tB.x * v + tC.x * u
                            ty = tA.y * w + tB.y * v + tC.y * u
                    
                            color = texture.getColor(tx, ty, intensity)
                            this.cursorColor = color
                        else:
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

    def shader(this, bar, light, textureCoords, normals, coords, vertices = (0, 0, 0)):
        w, u, v = bar
        L = light
        tA, tB, tC = textureCoords
        nA, nB, nC = normals
        x, y = coords
        A, B, C = vertices

        if this.activeTexture:
            nx = nA.x * w + nB.x * u + nC.x * v
            ny = nA.y * w + nB.y * u + nC.y * v
            nz = nA.z * w + nB.z * u + nC.z * v

            i = dot(norm(V3(nx,ny,nz)),L)

            tx = tA.x * w + tB.x * u + tC.x * v
            ty = tA.y * w + tB.y * u + tC.y * v

            if this.activeNormalMap:
                normal = (nx, ny, nz)

                ta = (tA.x, tA.y)
                tb = (tB.x, tB.y)
                tc = (tC.x, tC.y)

                texNormal = this.activeNormalMap.get_color(tx, ty)
                texNormal = V3((texNormal[2]) * 2 - 1,
                            (texNormal[1]) * 2 - 1,
                            (texNormal[0]) * 2 - 1)

                texNormal = div(texNormal, length(texNormal))

                # B - A
                edge1 = sub(B[0], A[0], B[1], A[1], B[2], A[2])
                # C - A
                edge2 = sub(C[0], A[0], C[1], A[1], C[2], A[2])
                # tb - ta 
                deltaUV1 = sub2(tb[0], ta[0], tb[1], ta[1])
                # tc - ta
                deltaUV2 = sub2(tc[0], ta[0], tc[1], ta[1])

                tangent = [0,0,0]
                f = 1 / (deltaUV1[0] * deltaUV2[1] - deltaUV2[0] * deltaUV1[1])
                tangent.x = f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0])
                tangent.y = f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1])
                tangent.z = f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])
                tangent = div(tangent, length(tangent))
                tangent = div(tangent, length(tangent))
                tangent = subVectors(tangent, dot(dot2(tangent, normal[0], normal[1], normal[2]), normal))
                tangent = tangent / length(tangent)

                bitangent = cross(normal, tangent)
                bitangent = bitangent / length(bitangent)

                tangentMatrix = [
                    [tangent[0],bitangent[0],normal[0]],
                    [tangent[1],bitangent[1],normal[1]],
                    [tangent[2],bitangent[2],normal[2]]
                ]

                light = L 
                light = multiplyVM(light, tangentMatrix)
                light = div(light, norm(light))

                intensity = dot(texNormal, light[0], light[1], light[2])

                r, g, b = this.activeTexture.get_color(tx, ty, intensity)

                if intensity > 0:
                    return color(r, g, b)

                else:
                    return color(0,0,0)
            
            else:             
                return this.activeTexture.getColor(tx, ty, i)


        else:
            r1, g1, b1 = BLACK
            r2, g2, b2 = BLACK
            percentage = 1
            r,g,b = BLACK

            if (this.activeShader == "mars"):
                if y > 0 and y <= 1000:
                    r1, g1, b1 = ORANGERED
                    r2, g2, b2 = ORANGE
                    percentage = 0

                if x > 0 and x <= 350:
                    r1, g1, b1 = ORANGERED
                    r2, g2, b2 = YELLOW
                    percentage = abs(x - 350) / 350

                if x > 500 and x <= 800:
                    r1, g1, b1 = ORANGERED
                    r2, g2, b2 = BLACK
                    percentage = abs((x - 500) / 300)

                if (((x - 450) ** 2) / (144 ** 2) + ((y - 450) ** 2) / (9 ** 2)) <= 1:
                    r1, g1, b1 = ORANGERED
                    r2, g2, b2 = BLACK
                    percentage = 0.5

                if (((x - 550) ** 2) / (100 ** 2) + ((y - 440) ** 2) / (16 ** 2)) <= 1:
                    r1, g1, b1 = ORANGERED
                    r2, g2, b2 = BLACK
                    percentage = 0.5

                if (((x - 600) ** 2) / (36 ** 2) + ((y - 600) ** 2) / (36 ** 2)) <= 1:
                    r1, g1, b1 = ORANGERED
                    r2, g2, b2 = BLACK
                    percentage = 0.5

                if (((x - 650) ** 2) / (16 ** 2) + ((y - 500) ** 2) / (16 ** 2)) <= 1:
                    r1, g1, b1 = ORANGERED
                    r2, g2, b2 = BLACK
                    percentage = 0.7
                
                if (((x - 700) ** 2) / (16 ** 2) + ((y - 600) ** 2) / (16 ** 2)) <= 1:
                    r1, g1, b1 = ORANGERED
                    r2, g2, b2 = BLACK
                    percentage = 0.9

                if (((x - 650) ** 2) / (16 ** 2) + ((y - 375) ** 2) / (16 ** 2)) <= 1:
                    r1, g1, b1 = ORANGERED
                    r2, g2, b2 = BLACK
                    percentage = 0.8

            if (this.activeShader == "moon"):
                if x > 700 and y <= 1000:
                    r1, g1, b1 = WHITE
                    r2, g2, b2 = BLACK
                    percentage = abs((x - 700) / 300)

                if (((x - 835) ** 2) / (16 ** 2) + ((y - 825) ** 2) / (16 ** 2)) <= 1:
                    r1, g1, b1 = WHITE
                    r2, g2, b2 = BLACK
                    percentage = 0.75

                if (((x - 855) ** 2) / (9 ** 2) + ((y - 885) ** 2) / (9 ** 2)) <= 1:
                    r1, g1, b1 = WHITE
                    r2, g2, b2 = BLACK
                    percentage = 0.75

                if (((x - 880) ** 2) / (9 ** 2) + ((y - 845) ** 2) / (9 ** 2)) <= 1:
                    r1, g1, b1 = WHITE
                    r2, g2, b2 = BLACK
                    percentage = 0.75

            r = r1 + percentage * (r2 - r1)
            g = g1 + percentage * (g2 - g1)
            b = b1 + percentage * (b2 - b1)

            return color(r, g, b)

    def randomPoints(this, iterations, color = color(255, 255, 255)):
        prevColor = this.cursorColor
        
        for i in range(iterations):
            this.cursorColor = color

            x = uniform(0, this.imageSize[0])
            y = uniform(0, this.imageSize[1])
            this.vertex(x,y)

        this.cursorColor = prevColor

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