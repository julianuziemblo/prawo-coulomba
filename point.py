from __future__ import annotations
import numpy as np


class Constants:
    e0 = (8.9875 * 10 ** 9)
    et = 250
    k = 1 / (4 * np.pi * e0 * et)
    podzialka = 0.3


class Point:
    def __init__(self, x: float, y: float, color: bool = False):
        self.x: float = x
        self.y: float = y
        self.color = color

    def distance(self, other_x: float, other_y: float) -> float:
        dist = np.sqrt((other_x - self.x) ** 2 + (other_y - self.y) ** 2)
        if dist <= abs(0.00001):
            del self
        return dist

    def _angle(self, other):
        return np.arctan2((self.y - other.y), (self.x - other.x))

    def _scalar(self, other):
        return self.x * other.x + self.y + other.y

    def project(self, other):
        scaling = (self._scalar(other) / (abs(other) ** 2))
        return self.__init__(scaling * other.x, scaling * other.y)

    def __str__(self):
        return f'P(x={self.x}, y={self.y})'

    def __eq__(self, other: Point):
        return self.x == other.x and self.y == other.y


class Charge(Point):
    def __init__(self, x: float, y: float, q: float = 0):
        super().__init__(x, y)
        self.q: float = q
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.ax: float = 0.0
        self.ay: float = 0.0
        self.m = 9.1093837 * 10 ** (-17)
        self.last_inside = Point(x, y)

    def get_color(self) -> str:
        return 'b' if self.q < 0 else 'r'

    def _force(self, other):
        return Constants.k * abs(self.q * other.q) / (self.distance(other.x, other.y) ** 2)

    def forceX(self, other):
        return np.cos(self._angle(other)) * self._force(other)

    def forceY(self, other):
        return np.sin(self._angle(other)) * self._force(other)

    def __str__(self) -> str:
        return f'Charge(x={self.x}, y={self.y}, q={self.q})'

    def __hash__(self):
        return hash((self.x, self.y, self.q, self.vx, self.vy, self.ax, self.ay))


class Force:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return np.sqrt(self.x**2 + self.y**2)

    def __str__(self):
        return f'F(Fx={self.x}, Fy={self.y})'

    def __mul__(self, other):
        return Force(self.x * other.x, self.y * other.y)

    def __add__(self, other):
        return Force(self.x + other.x, self.y + other.y)


class Velocity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return np.sqrt(self.x**2 + self.y**2)

    def __str__(self):
        return f'V(Vx={self.x}, Vy={self.y})'


class Edge:
    def __init__(self, p: Point, v: Velocity):
        self.p = p
        self.v = v

    def __str__(self):
        return f'Edge in point {self.p}, vector {self.v}'
