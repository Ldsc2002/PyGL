from PyGL.gl import *

pi = 3.1415926535897932
render = gl()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)

t = texture('Assets/x35.bmp')
model = 'Assets/x35.obj'

# Medium shot
render.lookAt((15, 0, 0), (0, 0, 0), (0, 1, 0))
render.clear()
render.load(model, (-0.2, -0.9, 0), (0.0225, 0.0225, 0.0225), (0, pi / 2, 0), t)
render.finish('mediumShot')

# Low angle
render.lookAt((15, -5, 0), (0, 0, 0), (0, 1, 0))
render.clear()
render.load(model, (-0.2, -0.5, 0), (0.0225, 0.0225, 0.0225), (0, pi / 2, 0), t)
render.finish('lowAngle')

# High angle
render.lookAt((15, 5, 0), (0, 0, 0), (0, 1, 0))
render.clear()
render.load(model, (-0.2, -0.5, 0), (0.0225, 0.0225, 0.0225), (0, pi / 2, 0), t)
render.finish('highAngle')

# Dutch angle
render.lookAt((15, 5, 0), (0, 0, 0), (0, 1, 0.5))
render.clear()
render.load(model, (-0.15, -0.75, 0), (0.0225, 0.0225, 0.0225), (0, pi / 2, 0), t)
render.finish('dutchAngle')