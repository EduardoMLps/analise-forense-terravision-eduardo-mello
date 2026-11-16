import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders as gls
from objs import renderObjs as objs
import ctypes
import numpy as np
import math
from objs.TileManager import TileManager

tileManager = None

m1 = objs.VertexMatrix()

#t1 = objs.Triangle()
#t1.setVertices( # x, y, z, u, v
#    [-0.5, 0.5, 1, 0, 1.0],
#    [0.5, 0.5, 0, 1.0, 1.0],
#    [0.5, -0.5, 0, 1.0, 0]
#)

#t2 = objs.Triangle()
#t2.setVertices(
#    [-0.5, 0.5, 1, 0, 1.0],
#    [0.5, -0.5, 0, 1.0, 0],
#    [-0.5, -0.5, 1, 0, 0]
#)

#Eu não sei o porque, mas adicionar o primeiro triângulo à matriz adiciona todos os triângulos...
#m1.addElement(t1)
#m1.addElement(t2)

rotationY = 0.0
rotationX = 0.0
cameraDistance = 2.0
cameraPosition = [0.0, 0.0, 2.0]


m1.addSphere(radius=0.5)

tex1 = objs.Material() 

VAOId = 0
shaderId = 0
amountOfFaces = None

def lookAt(eye, target, up):

    forward = np.array(target) - np.array(eye)
    forward = forward / np.linalg.norm(forward)

    right = np.cross(forward, up)
    right = right / np.linalg.norm(right)

    up = np.cross(right, forward)

    view = np.identity(4, dtype=np.float32)

    view[0, :3] = right
    view[1, :3] = up
    view[2, :3] = -forward

    view[0, 3] = -np.dot(right, eye)
    view[1, 3] = -np.dot(up, eye)
    view[2, 3] = np.dot(forward, eye)

    return view

def perspective(fov, aspect, near, far):

    f = 1.0 / math.tan(math.radians(fov) / 2.0)

    projection = np.zeros((4, 4), dtype=np.float32)

    projection[0, 0] = f / aspect
    projection[1, 1] = f

    projection[2, 2] = (far + near) / (near - far)
    projection[2, 3] = (2.0 * far * near) / (near - far)

    projection[3, 2] = -1.0

    return projection

def init():
    global VAOId, shaderId, amountOfFaces, tileManager

    tileManager = TileManager(
        directory="src/websearch/tiles",
        radius=0.5,
        max_zoom=8
    )

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClearDepth(1.0)

    glClearColor(0,0,0,1)

    #Texturas:


    #iniciar VBO - obter id
    VBOId = glGenBuffers(1)

    VAOId = glGenVertexArrays(1)
    glBindVertexArray(VAOId)

    #Ativar VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBOId)
    #colocar atributos no VBO
    glBufferData(
        GL_ARRAY_BUFFER,
        m1.getUniquesVertices().nbytes,
        m1.getUniquesVertices(),
        GL_DYNAMIC_DRAW
    )
    glEnableVertexAttribArray(0)
    #descrever atributos
    glVertexAttribPointer(
        0, #Código do atributo (posição)
        3, #Quantos valores por atributo
        GL_FLOAT, #Tipo de dado
        GL_FALSE, #Deve ser normalizado
        5*4, #qnt de bytes entre um atributo e o próximo
        ctypes.c_void_p(0) #ponteiro para onde começa os parâmetros
    )
    #glEnableVertexAttribArray(1)
    #glVertexAttribPointer(
    #    1, #Código do atributo (cor)
    #    3, #Quantos valores por atributo
    #    GL_FLOAT, #Tipo de dado
    #    GL_FALSE, #Deve ser normalizado
    #    7*4, #qnt de bytes entre um atributo e o próximo
    #    ctypes.c_void_p(2*4) #ponteiro para onde começa os parâmetros
    #)
    #Atributo de coordenadas UV
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(
        2,
        2,
        GL_FLOAT,
        GL_FALSE,
        5*4,
        ctypes.c_void_p(3*4)
    )
    #Ativar atributos

    

    # criar EBO:
    EBOid = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBOid)

    glBufferData(
        GL_ELEMENT_ARRAY_BUFFER,
        m1.getFacesIndex().nbytes,
        m1.getFacesIndex(),
        GL_DYNAMIC_DRAW
    )

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

    

    amountOfFaces = len(m1.getFacesIndex().flatten())
     

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(shaderId)
    rotationYLocation = glGetUniformLocation(shaderId, "rotationY")
    rotationXLocation = glGetUniformLocation(shaderId, "rotationX")
    glUniform1f(rotationYLocation, rotationY)
    glUniform1f(rotationXLocation, rotationX)
    
    eye = np.array(
        [0.0, 0.0, cameraDistance],
        dtype=np.float32
    )

    target = np.array([0.0, 0.0, 0.0], dtype=np.float32)

    up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

    view = lookAt(eye, target, up)

    projection = perspective(
        45.0,
        500 / 500,
        0.1,
        100.0
    )

    viewLocation = glGetUniformLocation(shaderId, "view")
    projectionLocation = glGetUniformLocation(shaderId, "projection")

    glUniformMatrix4fv(viewLocation, 1, GL_TRUE, view)
    glUniformMatrix4fv(projectionLocation, 1, GL_TRUE, projection)


    
    tileManager.update(
        cameraDistance,
        rotationX,
        rotationY
    )

    tileManager.draw(shaderId)
    glUseProgram(0)
    

def key_callback(window, key, scancode, action, mods):
    global rotationY, rotationX, cameraDistance
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, 1)
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_RIGHT:
            rotationY += 0.05
        if key == glfw.KEY_LEFT:
            rotationY -= 0.05
        if key == glfw.KEY_UP:
            rotationX -= 0.05
        if key == glfw.KEY_DOWN:
            rotationX += 0.05
        if key == glfw.KEY_KP_ADD:
            cameraDistance = max(0.6, cameraDistance - 0.03)
        if key == glfw.KEY_KP_SUBTRACT:
            cameraDistance += 0.03

def main():
    glfw.init()
    window = glfw.create_window(500, 500, "G.R.E.E.N", None, None)
    glfw.make_context_current(window)
    
    glfw.set_key_callback(window, key_callback)

    init()
    while not glfw.window_should_close(window):
        render()
        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()
    tileManager.destroy()

main()