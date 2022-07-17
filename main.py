from PyGL.gl import gl

render = gl()

render.init()
render.createWindow(500, 500)
render.viewPort(0, 0, 400, 400)

render.clearColor(0, 0.5, 0.5)
render.color(0, 0, 0)

render.clear()
render.vertex(0, 0)

render.finish()