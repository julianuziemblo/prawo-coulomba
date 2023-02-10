from __future__ import annotations
import numpy as np
from point import Point, Charge


def get_inside(image: np.ndarray):
    inside = []
    for i, row in enumerate(image):
        for j, cell in enumerate(row):
            if not image[i][j]:
                inside.append(Point(j, i))
    return inside


def get_closest_inside(particle: Charge, image: np.ndarray) -> Charge:
    # if particle.x > image.shape[0] // 2:
    #     x1 = np.ceil(particle.x)
    # else:
    #     x1 = np.floor(particle.x)
    # if particle.y > image.shape[1] // 2:
    #     y1 = np.ceil(particle.y)
    # else:
    #     y1 = np.floor(particle.y)
    # x = int(x1)
    # y = int(y1)
    # vx = -0.5*np.sign(particle.vx)
    # vy = -0.5*np.sign(particle.vy)
    #
    # curr_point = Point(x, y)
    # while image[int(curr_point.y), int(curr_point.x)]:
    #     if int(np.floor(curr_point.x + vx)) < 0 or int(np.ceil(curr_point.x + vx)) >= image.shape[0]:
    #         vx = -vx
    #     if int(np.floor(curr_point.y + vy)) < 0 or int(np.ceil(curr_point.y + vy)) >= image.shape[1]:
    #         vy = -vy
    #     curr_point.x += vx
    #     curr_point.y += vy
    #     print(curr_point, vx, vy)
    # particle.x = curr_point.x
    # particle.y = curr_point.y

    if particle.x > image.shape[0] // 2:
        x1 = np.ceil(particle.x)
    else:
        x1 = np.floor(particle.x)
    if particle.y > image.shape[1] // 2:
        y1 = np.ceil(particle.y)
    else:
        y1 = np.floor(particle.y)
    x = int(x1)
    y = int(y1)
    min_point = cast_rays(x, y, image)
    particle.x = min_point.x
    particle.y = min_point.y
    return particle


def prevent_leak(particle: Charge, image: np.ndarray) -> Charge:
    if particle.x > image.shape[0] // 2:
        x1 = np.ceil(particle.x)
    else:
        x1 = np.floor(particle.x)
    if particle.y > image.shape[1] // 2:
        y1 = np.ceil(particle.y)
    else:
        y1 = np.floor(particle.y)
    x = int(x1)
    y = int(y1)
    if image[y - 1][x] or image[y + 1][x] or image[y][x - 1] or image[y][x + 1]:
        print("PREVENTING")
        particle = get_closest_inside(particle, image)
    return particle


def main():
    image = np.array([[False, False, False],
                      [False, False, True],
                      [False, True, True]])
    print(image)
    print(prevent_leak(Charge(1, 1, 1), image))
    print(get_closest_inside(Charge(2, 2, 1), image))


if __name__ == '__main__':
    main()


def cast_rays(x: int, y: int, image: np.ndarray):
    points = []

    # Top
    last_color = True
    for i in range(y, 0):
        if last_color and not image[i][x]:
            points.append(Point(x, i))
            break
        last_color = image[i][x]

    # Right
    last_color = True
    for i in range(x, image.shape[0]):
        if last_color and not image[y][i]:
            points.append(Point(i, y))
            break
        last_color = image[y][i]

    # Bottom
    last_color = True
    for i in range(y, image.shape[0]):
        if last_color and not image[i][x]:
            points.append(Point(x, i))
            break
        last_color = image[i][x]

    # Left
    last_color = True
    for i in range(x, 0):
        if last_color and not image[y][i]:
            points.append(Point(i, y))
            break
        last_color = image[y][i]

    min_dist = float('inf')
    min_point = Point(0, 0)
    for point in points:
        dist = point.distance(x, y)
        if dist < min_dist:
            min_dist = dist
            min_point = Point(x, y)

    return min_point
#
#
# def is_inside(x: int, y: int, image: np.ndarray) -> bool:
#     # top -> right -> bottom -> left
#     if not image[y][x]:
#         return False
#     rays = list(cast_rays(x, y, image))
#     # print(rays)
#     t = 0
#     f = 0
#     for i in rays:
#         if i:
#             t += 1
#         else:
#             f += 1
#     return t > f
#
#
# def get_neighbours(x: int, y: int, image: np.ndarray):
#     """
#     public static ArrayList<Punkt> bieliSasiedzi(Punkt punkt) {
#         int x = punkt.x;
#         int y = punkt.y;
#         ArrayList<Punkt> listaIndeksow = new ArrayList<>();
#
#         for(int k=x-1;k<=x+1;k++) {
#             for(int l=y-1;l<=y+1;l++) {
#                 if((!(k<0 || k>=plansza.length) && !(l<0 || l>=plansza[0].length))&& plansza[k][l]!=0) {
#                     listaIndeksow.add(new Punkt(k,l));
#                 }
#             }
#         }
#         return listaIndeksow;
#     }
#     """
#     pass

# def save_to_file(arr: np.ndarray):
#     new_arr = np.ndarray(arr.shape, bool)
#     new_arr[arr == 1.] = True
#     new_arr[arr == 0.] = False
#     im = Image.fromarray(new_arr)
#     print("new_arr:")
#     print(new_arr.shape)
#     im.save("your_file.bmp")
