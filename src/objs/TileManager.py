
import os
import math
from PIL import Image
import numpy as np
from OpenGL.GL import *

from objs.Tile import Tile


class TileManager:

    def __init__(self, directory, radius=0.5, max_zoom=8):

        self.directory = directory
        self.radius = radius
        self.max_zoom = max_zoom

        self.tiles = {}

    def get_zoom(self, camera_distance):

        surface_distance = max(
            camera_distance - self.radius, 0.01
        )

        zoom = math.floor(
            math.log2(1.5 / surface_distance)
        )

        return max(0, min(self.max_zoom, zoom))

    def load_tile(self, zoom, x, y):

        key = (zoom, x, y)

        if key in self.tiles:
            return self.tiles[key]

        path = os.path.join(
            self.directory,
            f"{zoom}_{x}_{y}.png"
        )

        if not os.path.exists(path):
            return None

        tile = Tile(zoom, x, y, self.radius)

        image = Image.open(path).convert("RGB")
        image = image.transpose(
            Image.Transpose.FLIP_TOP_BOTTOM
        )

        width, height = image.size
        data = np.array(image, dtype=np.uint8)

        texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texture)

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

        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_MIN_FILTER,
            GL_LINEAR
        )

        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_MAG_FILTER,
            GL_LINEAR
        )

        glBindTexture(GL_TEXTURE_2D, 0)

        tile.texture = texture
        tile.upload()

        self.tiles[key] = tile

        return tile

    def update(self, camera_distance, rotation_x, rotation_y):

        zoom = self.get_zoom(camera_distance)

        n = 2 ** zoom

        visible = set()

        cx = math.cos(rotation_x)
        sx = math.sin(rotation_x)

        cy = math.cos(rotation_y)
        sy = math.sin(rotation_y)

        tile_radius = min(math.pi / 2, 2 * math.pi / n)

        for y in range(n):
            for x in range(n):

                lon = 2 * math.pi * (x + 0.5) / n - math.pi

                lat = math.atan(
                    math.sinh(
                        math.pi * (1 - 2 * (y + 0.5) / n)
                    )
                )

                px = math.cos(lat) * math.cos(lon)
                py = math.sin(lat)
                pz = -math.cos(lat) * math.sin(lon)

                # Aplicar a mesma rotação da esfera
                # Rotação Y
                rx = cy * px - sy * pz
                rz = sy * px + cy * pz

                # Rotação X
                wy = cx * py - sx * rz
                wz = sx * py + cx * rz

                # Aproximação da região visível
                #tile_radius = math.pi / n

                if wz > -math.sin(tile_radius):

                    visible.add((zoom, x, y))

        # Carregar os tiles visíveis
        for z, x, y in visible:
            self.load_tile(z, x, y)

        # Remover tiles que não são mais necessários
        for key in list(self.tiles.keys()):

            if key not in visible:

                self.tiles[key].destroy()
                del self.tiles[key]

    def draw(self, shader):

        for tile in self.tiles.values():
            tile.draw(shader)

    def destroy(self):

        for tile in self.tiles.values():
            tile.destroy()

        self.tiles.clear()
