from PyGL.gl import *

render = gl()

render.init()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)

render.load('Assets/Porsche.obj', (2.5, 1, 0),  (200, 200, 200))
render.finish('Porsche')
render.showZbuffer()