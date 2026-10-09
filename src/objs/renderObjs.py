import numpy as np

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