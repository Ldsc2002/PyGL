import struct
from collections import namedtuple

V2 = namedtuple('Point2D', ['x', 'y'])
V3 = namedtuple('Point3D', ['x', 'y', 'z'])

def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
	return V3(
		v0.x - v1.x,
		v0.y - v1.y,
		v0.z - v1.z
	)

def mul(v0, k):
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1): 
	cx = v0.y * v1.z - v0.z * v1.y
	cy = v0.z * v1.x - v0.x * v1.z
	cz = v0.x * v1.y - v0.y * v1.x
	return V3(cx, cy, cz)

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  l = length(v0)

  if l == 0:return V3(0, 0, 0)

  return V3(
		v0.x/l,
		v0.y/l,
		v0.z/l
		)

def bbox(A, B, C):
	xs = [A.x, B.x, C.x]
	xs.sort()
	ys = [A.y, B.y, C.y]
	ys.sort()
	return xs[0], xs[-1], ys[0], ys[-1]

def barycentric(A, B, C, P):
	cx, cy, cz = cross(
		V3(B.x - A.x, C.x - A.x, A.x - P.x),
		V3(B.y - A.y, C.y - A.y, A.y - P.y)
	)

	if cz == 0:
		return -1, -1, -1
	u = cx/cz
	v = cy/cz
	w = 1 - (cx + cy) / cz
	return w, v, u

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def doubleword(d):
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([b, g, r])

def writeBMP(pixels, name):
    # Prints the pixels to the screen
    width = len(pixels)
    height = len(pixels[0])
    
    name  = name + '.bmp'
    f = open(name, 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(doubleword(14 + 40 + width * height * 3))
    f.write(doubleword(0))
    f.write(doubleword(14 + 40))

    # Image header (40 bytes)
    f.write(doubleword(40))
    f.write(doubleword(width))
    f.write(doubleword(height))
    f.write(word(1))
    f.write(word(24))
    f.write(doubleword(0))
    f.write(doubleword(width * height * 3))
    f.write(doubleword(0))
    f.write(doubleword(0))
    f.write(doubleword(0))
    f.write(doubleword(0))

    for y in range (0, height):
        for x in range (0, width):
            f.write(pixels[y][x])

    f.close()
    print('Image saved as ' + name)