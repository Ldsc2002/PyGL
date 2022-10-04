from PyGL.gl import *

render = gl()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)
render.lookAt(V3(0 ,0 , 50), V3(0, 0, 0), V3(0, 1, 0))
render.setBackground(texture("Assets/background.bmp").pixels)

# 5 models
render.load('Assets/x35.obj', (0.1, -0.5, 0), (0.006, 0.006, 0.006), (pi/6, 19 * pi/18, 0), texture('Assets/x35.bmp'))
render.load('Assets/p38.obj', (-0.03, 0, 0), (0.065, 0.065, 0.065), (0, -8.5 * pi/18, -pi/8), texture('Assets/p38.bmp'))
render.load('Assets/harley.obj', (0.745, 0.25, 0), (0.05, 0.05, 0.05), (0, -pi/2, 0), texture('Assets/harley.bmp'))
render.load('Assets/b17.obj', (-0.125, 0.5, 0), (0.03, 0.03, 0.03), (0, -8.5 * pi/18, -pi/8), texture('Assets/b17.bmp'))
render.load('Assets/helicopter.obj', (0.7, 0.45, 0), (0.03, 0.03, 0.03), (0, 0, 0), texture('Assets/helicopter.bmp'))

# Model with normal mapping
render.load('Assets/flag.obj', (-0.75, -0.5, 0), (0.3, 0.3, 0.3), (0, 0, 0), texture('Assets/flag.bmp'), None, texture('Assets/flagNorm.bmp'))

render.finish('scene')
