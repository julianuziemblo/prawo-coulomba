import numpy as np


class Constants:
    e0 = (8.9875 * 10**9)
    et = 250
    k = 1 / (4 * np.pi * e0 * et)


class Point:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def distance(self, other_x: float, other_y: float) -> float:
        return np.sqrt((other_x - self.x) ** 2 + (other_y - self.y) ** 2)

    def __str__(self):
        return f'P(x={self.x}, y={self.y})'


class Charge(Point):
    def __init__(self, x: float, y: float, q: float):
        super().__init__(x, y)
        self.q: float = q
        self.vx: float = 0.0
        self.vy: float = 0.0
        self.ax: float = 0.0
        self.ay: float = 0.0

    def get_color(self) -> str:
        return 'b' if self.q < 0 else 'r'

    def _force(self, other):
        return Constants.k * abs(self.q * other.q) / (self.distance(other.x, other.y) ** 2)

    def _angle(self, other):
        return np.arctan(abs(self.y - other.y) / abs(self.x - other.x))

    def forceX(self, other):
        return np.cos(self._angle(other)) * self._force(other)

    def forceY(self, other):
        return np.sin(self._angle(other)) * self._force(other)

    def __str__(self) -> str:
        return f'Charge(x={self.x}, y={self.y}, q={self.q})'

    def __hash__(self):
        return hash([self.x, self.y, self.q, self.vx, self.vy, self.ax, self.ay])

