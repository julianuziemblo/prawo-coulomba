import numpy as np

from point import Charge


class Force:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return np.sqrt(self.x**2 + self.y**2)


def get_total_force(charge: Charge, charges: list[Charge]) -> list[float, float]:
    force = [0.0, 0.0]
    for particle in charges:
        if particle != charge:
            if particle.q == charge.q:
                force[0] -= charge.forceX(particle)
                force[1] -= charge.forceY(particle)
            else:
                force[0] += charge.forceX(particle)
                force[1] += charge.forceY(particle)
    return force


# TEST
def main():
    c1 = Charge(0, 0, 1)
    c2 = Charge(1, 1, -1)
    print(get_total_force(c1, [c1, c2]))


if __name__ == '__main__':
    main()
