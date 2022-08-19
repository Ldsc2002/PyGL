from PyGL.gl import *

render = gl()

render.init()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)

render.load('Assets/Porsche_911.obj', (1, 1, 0),  (400, 400, 400))
render.finish('Porsche')
render.showZbuffer()