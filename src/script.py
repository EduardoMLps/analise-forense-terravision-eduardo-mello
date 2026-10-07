import glfw
from OpenGL.GL import *
from objs import renderObjs as objs

t1 = objs.Triangle()
t1.setVertices(
    [-0.5, 0.5],
    [0.0, -0.5],
    [0.5, 0.5]
)
t1.setColors(
    [1,0,0],
    [0,1,0],
    [0,0,1]
)

def init():
    glClearColor(0,0,0,1)

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for v, c in zip(t1.vertices, t1.colors):
        glColor3fv(c)
        glVertex2fv(v)
    glEnd()

def main():
    print(t1.colors)
    print(t1.vertices)
    
    glfw.init()
    window = glfw.create_window(500, 500, "G.R.E.E.N", None, None)
    glfw.make_context_current(window)
    
    init()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()

main()