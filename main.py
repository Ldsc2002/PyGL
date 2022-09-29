from PyGL.gl import *

render = gl()
render.createWindow(1000, 1000)
render.viewPort(0, 0, 1000, 1000)
render.lookAt(V3(0 ,0 , 50), V3(0, 0, 0), V3(0, 1, 0))

render.randomPoints(1000)
render.load('Assets/sphere.obj',(0, 0, 0), (1, 1, 1), (0, 0, 0), None, "planet")
render.load('Assets/sphere.obj',(0.7, 0.7, 0), (0.25, 0.25, 0.25), (0, 0, 0), None, "moon")

render.finish('planet')
