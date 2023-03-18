import math


class Point:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, string: str = None):
        if string is not None:
            lst = string.split(',')
            self.x = float(lst[0])
            self.y = float(lst[1])
            self.z = float(lst[2])
        else:
            self.x = x
            self.y = y
            self.z = z

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

    def __repr__(self):
        return self.__str__()

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setZ(self, z):
        self.z = z

    def distance(self, p1) -> float:
        """Calculates distance between 2 points. Returns it."""
        return math.sqrt((self.x - p1.x) ** 2 + (self.y - p1.y) ** 2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

