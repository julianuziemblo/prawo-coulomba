import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other_x, other_y):
        return np.sqrt((other_x - self.x) ** 2 + (other_y - self.y) ** 2)

    def __str__(self):
        return f'P(x={self.x}, y={self.y})'


class Charge(Point):
    def __init__(self, x, y, q):
        super().__init__(x, y)
        self.q = q

    def get_color(self):
        return 'b' if self.q < 0 else 'r'

    def __str__(self):
        return f'Charge(x={self.x}, y={self.y}, q={self.q})'

