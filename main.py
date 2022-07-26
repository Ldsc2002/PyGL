from PyGL.gl import gl

render = gl()

render.init()
render.createWindow(900, 900)
render.viewPort(0, 0, 800, 800)

render.poligon('Assets/1.txt')
render.fill('Assets/1.txt')

render.poligon('Assets/2.txt')
render.fill('Assets/2.txt')

render.poligon('Assets/3.txt')
render.fill('Assets/3.txt')

render.poligon('Assets/4.txt')
render.fill('Assets/4.txt')

render.color(0, 0, 0)
render.poligon('Assets/5.txt')
render.fill('Assets/5.txt')

render.finish()