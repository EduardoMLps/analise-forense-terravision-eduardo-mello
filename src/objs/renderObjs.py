import numpy as np
from OpenGL.GL import *
from PIL import Image


class Material:
    texture = None
    def load_from_file(self, path):
        image = Image.open(path).convert("RGB")
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        width, height = image.size

        data = np.array(image, dtype=np.uint8)

        self.texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            width,
            height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            data
        )

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)

    def destroy(self):
        if self.texture is not None:
            glDeleteTextures(1, [self.texture])
            self.texture = None

    def use(self, program):
        if self.texture is None:
            raise RuntimeError("A textura não foi carregada!")

        glUseProgram(program)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        location = glGetUniformLocation(program, "uTexture")

        if location == -1 or location is None:
            raise RuntimeError(
                "Uniform 'uTexture' não encontrado no shader!"
            )

        glUniform1i(location, 0)
        

    def destroy(self):
        glDeleteTextures(1, (self.texture,))

class VertexMatrix:
    vertices = None

    def addElement(self, element):
        if self.vertices is None:
            self.vertices = element.getVertices()
        else:
            self.vertices = np.concatenate((self.vertices, element.getVertices()), axis=0)
    
    def addSphere(self, radius=1.0, sectors=32, stacks=16, center=(0.0, 0.0, 0.0)):

        vertices = []

        cx, cy, cz = center

        for i in range(stacks):
            phi1 = np.pi * i / stacks
            phi2 = np.pi * (i + 1) / stacks

            for j in range(sectors):
                theta1 = 2.0 * np.pi * j / sectors
                theta2 = 2.0 * np.pi * (j + 1) / sectors

                def vertex(phi, theta):
                    x = radius * np.sin(phi) * np.cos(theta)
                    y = radius * np.cos(phi)
                    z = radius * np.sin(phi) * np.sin(theta)

                    u = theta / (2.0 * np.pi)
                    v = 1.0 - phi / np.pi

                    return [
                        cx + x,
                        cy + y,
                        cz + z,
                        u,
                        v
                    ]

                v1 = vertex(phi1, theta1)
                v2 = vertex(phi2, theta1)
                v3 = vertex(phi2, theta2)
                v4 = vertex(phi1, theta2)

                # Primeiro triângulo
                vertices.extend([v1, v2, v3])

                # Segundo triângulo
                vertices.extend([v1, v3, v4])

        vertices = np.array(vertices, dtype=np.float32)

        if self.vertices is None:
            self.vertices = vertices
        else:
            self.vertices = np.concatenate(
                (self.vertices, vertices),
                axis=0
            )

    def getVertices(self):
        return np.array(self.vertices, np.dtype(np.float32))
    
    def getVerticesSize(self):
        return self.getVertices().nbytes

    def getUniquesVertices(self):
        self.faces = np.empty((int(len(self.vertices) / 3), 3))
        v2 = []
        for vertice in self.vertices:
            for value in v2:
                if np.array_equal(vertice, value):
                    break
            else:
                v2.append(vertice)
            
        return np.array(v2, dtype=np.float32)

    def getFacesIndex(self):
        uniques = self.getUniquesVertices()
        a = np.empty((int(len(self.vertices) / 3), 3), dtype=np.float32)
        for i1, v1 in enumerate(self.vertices):
            triangleNum = int(np.floor(i1 / 3))
            for i2, v2 in enumerate(uniques):
                if np.array_equal(v1, v2):
                    a[triangleNum][i1 % 3] = i2 

        return np.array(a, dtype=np.uint32)


class Triangle:
    vertices = []
    colors = []
    angle = 0

    def __init__(self):
        pass

    def setVertices(self, v1, v2, v3):
        self.vertices.append(v1)
        self.vertices.append(v2)
        self.vertices.append(v3)

    def setColors(self, c1, c2, c3):
        self.colors.append(c1)
        self.colors.append(c2)
        self.colors.append(c3)

    def getVertices(self):
        return np.array(self.vertices, np.dtype(np.float32))

    def getVerticesSize(self):
        return self.getVertices().nbytes