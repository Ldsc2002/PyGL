from PyGL.gl import gl

render = gl()

render.init()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)

render.load('Assets/Porsche_911.obj', (0, 0), 1)

render.finish()