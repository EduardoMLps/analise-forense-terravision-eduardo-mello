import glfw
from OpenGL.GL import *
from objs import renderObjs as objs
import ctypes

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

VAOId = 0

def init():
    global VAOId

    glClearColor(0,0,0,1)
    #iniciar VBO - obter id
    VBOId = glGenBuffers(1)

    VAOId = glGenVertexArrays(1)
    glBindVertexArray(VAOId)


    #Ativar VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBOId)
    #colocar atributos no VBO
    glBufferData(
        GL_ARRAY_BUFFER,
        t1.getVerticesSize(),
        t1.getVertices(),
        GL_STATIC_DRAW
    )
    #descrever atributos
    glVertexAttribPointer(
        0, #Código do atributo
        2, #Quantos valores por atributo
        GL_FLOAT, #Tipo de dado
        GL_FALSE,
        2*4, #qnt de bytes entre um atributo e o próximo
        ctypes.c_void_p(0) #ponteiro para o vazio
    )
    #Ativar atributos
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    #Criar shaders

    #Código fonte do shader:

def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glBindVertexArray(VAOId)
    glDrawArrays(GL_TRIANGLES, 0, len(t1.getVertices()))
    

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