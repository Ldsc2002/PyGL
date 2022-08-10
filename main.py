from PyGL.gl import *

render = gl()

render.init()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)

render.load('Assets/Porsche_911.obj', (0, 0, 0),  (500, 500, 500))
render.finish('Porsche')