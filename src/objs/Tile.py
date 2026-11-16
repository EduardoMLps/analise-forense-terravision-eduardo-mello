
import numpy as np
from OpenGL.GL import *
import ctypes
import math


def mercator_to_latitude(y, zoom):
    n = 2 ** zoom

    return math.atan(
        math.sinh(math.pi * (1 - 2 * y / n))
    )


class Tile:

    def __init__(self, zoom, x, y, radius=0.5, segments=16):
        self.zoom = zoom
        self.x = x
        self.y = y

        self.radius = radius
        self.segments = segments

        self.vertices = []
        self.indices = []

        self.texture = None
        self.vao = None
        self.vbo = None
        self.ebo = None

        self.generate_mesh()

    def generate_mesh(self):

        n = 2 ** self.zoom

        lon_west = 2 * math.pi * self.x / n - math.pi
        lon_east = 2 * math.pi * (self.x + 1) / n - math.pi

        lat_north = mercator_to_latitude(self.y, self.zoom)
        lat_south = mercator_to_latitude(self.y + 1, self.zoom)

        for j in range(self.segments + 1):

            v = j / self.segments

            lat = mercator_to_latitude(
                self.y + v,
                self.zoom
            )

            for i in range(self.segments + 1):

                u = i / self.segments

                lon = lon_west + (lon_east - lon_west) * u

                px = self.radius * math.cos(lat) * math.cos(lon)
                py = self.radius * math.sin(lat)
                pz = -self.radius * math.cos(lat) * math.sin(lon)

                # v=1 corresponde ao topo da imagem
                self.vertices.append([
                    px, py, pz,
                    u, 1.0 - v
                ])

        for j in range(self.segments):
            for i in range(self.segments):

                a = j * (self.segments + 1) + i
                b = a + self.segments + 1

                self.indices.extend([
                    a, b, a + 1,
                    a + 1, b, b + 1
                ])

        self.vertices = np.array(
            self.vertices, dtype=np.float32
        )

        self.indices = np.array(
            self.indices, dtype=np.uint32
        )

    def upload(self):

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.vertices.nbytes,
            self.vertices,
            GL_STATIC_DRAW
        )

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            self.indices.nbytes,
            self.indices,
            GL_STATIC_DRAW
        )

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE,
            5 * 4, ctypes.c_void_p(0)
        )

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(
            2, 2, GL_FLOAT, GL_FALSE,
            5 * 4, ctypes.c_void_p(3 * 4)
        )

        glBindVertexArray(0)

    def draw(self, shader):

        if self.vao is None or self.texture is None:
            return

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        location = glGetUniformLocation(shader, "uTexture")
        glUniform1i(location, 0)

        glBindVertexArray(self.vao)

        glDrawElements(
            GL_TRIANGLES,
            len(self.indices),
            GL_UNSIGNED_INT,
            None
        )

        glBindVertexArray(0)

    def destroy(self):

        if self.texture is not None:
            glDeleteTextures(1, [self.texture])

        if self.vao is not None:
            glDeleteVertexArrays(1, [self.vao])

        if self.vbo is not None:
            glDeleteBuffers(1, [self.vbo])

        if self.ebo is not None:
            glDeleteBuffers(1, [self.ebo])
