import struct
from PyGL.utils import *

class texture(object):
    def __init__(this, path):
        this.path = path
        this.read()

    def read(this):
        image = open(this.path, "rb")

        image.seek(2 + 4 + 4) 
        header_size = struct.unpack("=l", image.read(4))[0] 
        image.seek(2 + 4 + 4 + 4 + 4)
        
        this.width = struct.unpack("=l", image.read(4))[0]
        this.height = struct.unpack("=l", image.read(4))[0]
        this.pixels = []

        image.seek(header_size)
        for y in range(this.height):
            this.pixels.append([])
            for x in range(this.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                this.pixels[y].append(color(r,g,b))

        image.close()

    def getColor(this, x, y, intensity = 1):
        if x >= 0 and x < 1 and y >= 0 and y < 1:
            x = int(x * this.width)
            y = int(y * this.height)

            return bytes(map(lambda b: round(b*intensity) if b*intensity > 0 else 0, this.pixels[y][x]))
        else:
            return bytes([0, 0, 0])
