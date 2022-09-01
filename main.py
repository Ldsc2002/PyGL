from PyGL.gl import *

render = gl()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)

render.lookAt((1, 0, 5), (0, 0, 0), (0, 1, 0))

t = texture('Assets/face.bmp')
render.load('Assets/face.obj', (0, 0, 0), (1, 1, 1), (0, 0, 0), t)
render.finish('models')