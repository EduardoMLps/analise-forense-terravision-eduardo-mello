import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
from objs import renderObjs as objs
import ctypes

m1 = objs.VertexMatrix()

t1 = objs.Triangle()
t1.setVertices(
    [-0.5, 0.5, 1, 0, 0],
    [0.5, 0.5, 0, 1, 0],
    [0.5, -0.5, 0, 0, 1]
)

t2 = objs.Triangle()
t2.setVertices(
    [-0.5, 0.5, 1, 0, 0],
    [0.5, -0.5, 0, 0, 1],
    [-0.5, -0.5, 1, 0, 1]
)

#Eu não sei o porque, mas adicionar o primeiro triângulo à matriz adiciona todos os triângulos...
m1.addElement(t1)
m1.addElement(t2)

VAOId = 0
shaderId = 0

def init():
    global VAOId, shaderId

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
        m1.getVerticesSize(),
        m1.getVertices(),
        GL_STATIC_DRAW
    )
    #descrever atributos
    glVertexAttribPointer(
        0, #Código do atributo (posição)
        2, #Quantos valores por atributo
        GL_FLOAT, #Tipo de dado
        GL_FALSE, #Deve ser normalizado
        5*4, #qnt de bytes entre um atributo e o próximo
        ctypes.c_void_p(0) #ponteiro para onde começa os parâmetros
    )
    glVertexAttribPointer(
        1, #Código do atributo (cor)
        3, #Quantos valores por atributo
        GL_FLOAT, #Tipo de dado
        GL_FALSE, #Deve ser normalizado
        5*4, #qnt de bytes entre um atributo e o próximo
        ctypes.c_void_p(2*4) #ponteiro para onde começa os parâmetros
    )
    #Ativar atributos
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    #Criar shaders

    #Código fonte do shader:
    #ler vertex shader:
    with open("src/shaders/vertexShader.glsl", "r") as file:
        vsSource = file.read()
    #ler fragment shader:
    with open("src/shaders/fragmentShader.glsl", "r") as file:
        fsSource = file.read()

    #Compilar shaders
    vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
    fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)

    #criar shader program:
    shaderId = gls.compileProgram(vsId, fsId)
     

def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shaderId)

    glBindVertexArray(VAOId)
    glDrawArrays(GL_TRIANGLES, 0, len(m1.getVertices()))
    

def main():
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