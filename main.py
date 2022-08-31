from PyGL.gl import *

render = gl()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)

render.lookAt((1, 1, 1), (0, 0, 0), (0, 1, 0))

t = texture('Assets/x35.bmp')
render.load('Assets/x35.obj', (300, 400, 0),  (6, 6, 6), (0.25, 0.25, 0.25), t)
render.load('Assets/Porsche.obj', (700, 300, 0),  (50, 50, 50), (0.25, 0.25, 0.25))
render.finish('models')