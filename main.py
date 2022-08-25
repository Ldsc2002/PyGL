from PyGL.gl import *

render = gl()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)

t = texture('Assets/x35.bmp')
render.load('Assets/x35.obj', (50, 20, 0),  (10, 10, 10), t)
render.finish('x35')