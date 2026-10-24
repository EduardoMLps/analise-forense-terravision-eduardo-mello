import numpy as np

class VertexMatrix:
    vertices = None

    def addElement(self, element):
        if self.vertices is None:
            self.vertices = element.getVertices()
        else:
            np.concatenate((self.vertices, element.getVertices()), axis=0)

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