from PyGL.gl import gl

render = gl()

render.init()
render.createWindow(1100, 1100)
render.viewPort(0, 0, 1000, 1000)

render.poligon('Assets/star.txt')
render.fill('Assets/star.txt')

render.finish()