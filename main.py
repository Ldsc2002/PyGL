from PyGL.gl import *

render = gl()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)

t = texture('Assets/model.bmp')
render.load('Assets/model.obj', (2.5, 2.5, 0),  (200, 200, 200), t)
render.finish('Face')

render.clear()
render.load('Assets/Porsche.obj', (2.5, 1, 0),  (200, 200, 200))
render.finish('Porsche')