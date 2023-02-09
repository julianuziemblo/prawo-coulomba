import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other_x, other_y):
        return np.sqrt((other_x - self.x) ** 2 + (other_y - self.y) ** 2)


class Charge(Point):
    def __init__(self, x, y, charge):
        super().__init__(x, y)
        self.charge = charge

    def get_color(self):
        return 'bo' if self.charge < 0 else 'ro'

