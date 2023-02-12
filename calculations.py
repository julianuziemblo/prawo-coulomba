from __future__ import annotations
import random
import numpy as np
from image_parser import prevent_leak
from point import Charge, Constants, Point, Force


def total_force(particle: Charge, particles: list[Charge]) -> Force:
    force = Force(0.0, 0.0)
    for particle2 in particles:
        if particle2 != particle:
            if np.sign(particle.q) == np.sign(particle2.q):
                force.x += particle.forceX(particle2)
                force.y += particle.forceY(particle2)
            else:
                force.x -= particle.forceX(particle2)
                force.y -= particle.forceY(particle2)
    return force


def acceleration(particle: Charge, particles: list[Charge]) -> Charge:
    F = total_force(particle, particles)
    particle.ax = Constants.podzialka * F.x / particle.m
    particle.ay = Constants.podzialka * F.y / particle.m
    return particle


def update_particle(particle: Charge, image: np.ndarray, inside: list[Point]) -> Charge:
    if (particle.x < 0 or particle.x >= image.shape[1]) or (particle.y < 0 or particle.y >= image.shape[0]):
        particle.x = particle.last_inside.x
        particle.y = particle.last_inside.y
        particle.vx -= 0.1*particle.vx
        particle.vy -= 0.1*particle.vy
    if (particle.x < 0 or particle.x >= image.shape[1]) or (particle.y < 0 or particle.y >= image.shape[0]):
        point = random.choice(inside)
        particle.x = point.x
        particle.y = point.y
        particle.vx = 0
        particle.vy = 0
        # del particle
        # return
    particle = prevent_leak(particle, image)
    # if Point(int(particle.x), int(particle.y)) not in inside:
    #   print("NIE W ŚRODKU:", particle)

    return particle


# TEST
def main():
    c1 = Charge(0, 0, 1)
    c2 = Charge(1, 0, 1)
    c3 = Charge(0, 1, -1)
    # print(total_force(c1, [c1, c2, c3]))


if __name__ == '__main__':
    main()
